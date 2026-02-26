#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pymupdf",
# ]
# ///
"""
Extract laws from Moselle PDFs and generate Hugo markdown files.
Uses the index.json to know which pages correspond to which law,
then extracts the text from the PDF and creates markdown files.
"""

import json
import os
import re
import unicodedata

import pymupdf

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "static", "pdfs", "moselle", "index.json")
PDF_DIR = os.path.join(BASE_DIR, "static", "pdfs", "moselle")
OUTPUT_DIR = os.path.join(BASE_DIR, "content", "textes")


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    # Normalize unicode characters
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    # Convert to lowercase
    text = text.lower()
    # Replace common patterns
    text = re.sub(r"1er", "1", text)
    # Replace non-alphanumeric characters with hyphens
    text = re.sub(r"[^a-z0-9]+", "-", text)
    # Remove leading/trailing hyphens
    text = text.strip("-")
    # Collapse multiple hyphens
    text = re.sub(r"-+", "-", text)
    return text


def extract_date_from_title(title: str) -> str | None:
    """Extract a date from a law title and return it in YYYY-MM-DD format."""
    # French month mapping
    months = {
        "janvier": "01",
        "février": "02",
        "fevrier": "02",
        "mars": "03",
        "avril": "04",
        "mai": "05",
        "juin": "06",
        "juillet": "07",
        "août": "08",
        "aout": "08",
        "septembre": "09",
        "octobre": "10",
        "novembre": "11",
        "décembre": "12",
        "decembre": "12",
    }

    # Try to match "du DD month YYYY" or "du 1er month YYYY"
    patterns = [
        r"du\s+(\d{1,2}(?:er)?)\s+(janvier|février|fevrier|mars|avril|mai|juin|juillet|août|aout|septembre|octobre|novembre|décembre|decembre)\s+(\d{4})",
    ]

    for pattern in patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            day = match.group(1).replace("er", "")
            month = months.get(match.group(2).lower(), "01")
            year = match.group(3)
            return f"{year}-{month}-{int(day):02d}"

    return None


def detect_type_texte(title: str) -> str:
    """Detect the type of legal text from its title."""
    title_lower = title.lower()

    # Match on the START of the title to avoid substring false positives
    # (e.g., "Décision ... modifiant l'instruction" should be Décision, not Instruction)
    prefix_mapping = [
        ("code civil local", "Code"),
        ("code local de procédure civile", "Code"),
        ("code pénal local", "Code"),
        ("code de commerce", "Code"),
        ("code des assurances sociales", "Code"),
        ("convention", "Convention"),
        ("règlement ministériel", "Règlement"),
        ("arrêté ministériel", "Arrêté"),
        ("arrêté", "Arrêté"),
        ("proclamation ministérielle", "Proclamation"),
        ("décision", "Décision"),
        ("instruction", "Instruction"),
        ("ordonnance ministérielle", "Ordonnance"),
        ("ordonnance impériale", "Ordonnance"),
        ("ordonnance", "Ordonnance"),
        ("loi d'empire", "Loi"),
        ("loi d'alsace-lorraine", "Loi"),
        ("loi communale", "Loi"),
        ("loi pénale", "Loi"),
        ("loi", "Loi"),
    ]

    for pattern, type_texte in prefix_mapping:
        if title_lower.startswith(pattern):
            return type_texte

    return "Texte"


def classify_law(title: str) -> list[str]:
    """Classify a law into categories based on its title content.

    Categories (12):
      enseignement, cultes-religions, fonctionnaires,
      chasse, eaux,
      droit-civil, droit-penal, urbanisme,
      commerce-professions, droit-social,
      administration, justice
    """
    title_lower = title.lower()
    categories = []

    # Enseignement
    if any(
        kw in title_lower
        for kw in [
            "enseignement",
            "écoles",
            "instituteurs",
            "instruction",
            "scolaire",
            "faculté de théologie",
            "séminaire",
            "université",
        ]
    ):
        categories.append("enseignement")

    # Cultes / Religions
    if any(
        kw in title_lower
        for kw in [
            "consistoire",
            "culte",
            "pasteur",
            "rabbin",
            "synagogue",
            "église",
            "confession",
            "israélite",
            "protestant",
            "catholique",
            "réformée",
            "augsbourg",
            "presbytér",
            "synode",
            "synodale",
            "circonscrip",
            "théologie",
            "lieu de culte",
            "lieux de culte",
            "ministres des cultes",
            "inspecteurs ecclésiastiques",
            "rabbinique",
        ]
    ):
        categories.append("cultes-religions")

    # Fonctionnaires
    if any(
        kw in title_lower
        for kw in [
            "fonctionnaire",
            "pension",
            "retraite",
            "veuves et orphelins",
            "employés de secrétariat",
        ]
    ):
        # If about ministers of religion pensions, also put in cultes
        if "ministres des cultes" in title_lower:
            if "cultes-religions" not in categories:
                categories.append("cultes-religions")
            categories.append("fonctionnaires")
        elif "autorités supérieures des cultes" in title_lower:
            if "cultes-religions" not in categories:
                categories.append("cultes-religions")
            categories.append("fonctionnaires")
        else:
            categories.append("fonctionnaires")
    # "traitement" only triggers fonctionnaires when about salary/pay
    if "traitement" in title_lower and "fonctionnaires" not in categories:
        categories.append("fonctionnaires")

    # Chasse (hunting law — word boundaries to avoid false matches like "nouveau")
    chasse_patterns = [
        r"\bchasses?\b",
        r"\bgibier\b",
        r"\boiseaux\b",
        r"\btétras\b",
        r"\bcaille\b",
        r"\bcanards?\b",
        r"\bpolice rurale\b",
        r"\btaureaux reproducteurs\b",
    ]
    if any(re.search(p, title_lower) for p in chasse_patterns):
        categories.append("chasse")

    # Eaux (water law)
    eaux_patterns = [
        r"\beaux\b",
        r"\bhydraul",
        r"\bd'eau\b",
        r"\bcanalisations d'eau\b",
    ]
    if any(re.search(p, title_lower) for p in eaux_patterns):
        categories.append("eaux")

    # Droit civil
    if any(
        kw in title_lower
        for kw in [
            "code civil",
            "droit privé",
            "ventes à tempérament",
            "régime des associations",
            "honoraires des notaires",
            "frais de justice",
            "procédure civile",
            "patrimoines des sections",
            "patrimoine possédé",
            "fondations",
        ]
    ):
        categories.append("droit-civil")

    # Droit pénal (criminal law only)
    if any(
        kw in title_lower
        for kw in [
            "code pénal",
            "pénal",
        ]
    ):
        categories.append("droit-penal")

    # Urbanisme (construction/building/posting law)
    if any(
        kw in title_lower
        for kw in [
            "construire",
            "construction",
            "urbanisme",
            "affichage",
            "police des constructions",
        ]
    ):
        categories.append("urbanisme")

    # Droit social (social insurance, labour law)
    if any(
        kw in title_lower
        for kw in [
            "assurances sociales",
            "assurance des employés",
            "repos dominical",
            "travail dominical",
        ]
    ):
        categories.append("droit-social")

    # Commerce / Professions (commercial law, economic law, cooperatives)
    if any(
        kw in title_lower
        for kw in [
            "commerce",
            "profession",
            "coopérative",
            "tempérament",
            "navigation intérieure",
        ]
    ):
        categories.append("commerce-professions")
    # "assurance" triggers commerce only if NOT already classified as droit-social
    if "assurance" in title_lower and "droit-social" not in categories:
        if "commerce-professions" not in categories:
            categories.append("commerce-professions")
    # "employés" only triggers commerce if not in a cultes or droit-social context
    if "employés" in title_lower:
        if "cultes-religions" not in categories and "droit-social" not in categories:
            if "commerce-professions" not in categories:
                categories.append("commerce-professions")

    # Administration
    if any(
        kw in title_lower
        for kw in [
            "administration",
            "communale",
            "communes",
            "cadastre",
            "impôt foncier",
            "budget",
            "jours fériés",
            "bulletin de vote",
            "élections",
            "canalisations",
            "recouvrement",
            "exécution forcée",
            "compétence",
            "conseil impérial",
            "organisation de l'administration",
            "non-dommageabilité",
        ]
    ):
        categories.append("administration")

    # Justice
    if any(
        kw in title_lower
        for kw in [
            "charges judiciaires",
            "indemnités accordées aux témoins",
            "interprètes",
            "indemnisation des titulaires",
        ]
    ):
        categories.append("justice")

    # Default: if no category matched, try broader classification
    if not categories:
        if "instituteur" in title_lower:
            categories.append("enseignement")
        elif "droit public" in title_lower:
            categories.append("administration")
        else:
            categories.append("administration")  # fallback

    return categories


def extract_law_text(doc: pymupdf.Document, first_page: int, last_page: int) -> str:
    """Extract text from a range of PDF pages (1-indexed)."""
    text_parts = []
    for page_num in range(first_page - 1, last_page):
        page = doc[page_num]
        text = page.get_text()
        text_parts.append(text)

    # Join all pages
    raw_text = "\n".join(text_parts)

    return raw_text


def clean_law_text(raw_text: str, title: str) -> str:
    """Clean extracted PDF text into readable markdown content."""
    lines = raw_text.split("\n")
    cleaned_lines = []
    skip_header = True

    for line in lines:
        stripped = line.strip()

        # Skip empty lines at the start
        if skip_header and not stripped:
            continue

        # Skip page numbers (standalone numbers)
        if re.match(r"^\d+$", stripped):
            continue

        # Skip the repeated title header at the top (we have it in frontmatter)
        # We skip until we find the first "Article" or substantive content
        if skip_header:
            # Check if this is the start of actual content
            if (
                stripped.startswith("Article")
                or stripped.startswith("§")
                or stripped.startswith("Art.")
            ):
                skip_header = False
            elif "en vertu" in stripped.lower() or "il est" in stripped.lower():
                skip_header = False
            elif stripped and not any(
                stripped.lower().startswith(prefix)
                for prefix in [
                    "loi",
                    "ordonnance",
                    "arrêté",
                    "code",
                    "convention",
                    "règlement",
                    "proclamation",
                    "instruction",
                    "décision",
                    "relative",
                    "relatif",
                    "concernant",
                    "portant",
                    "sur l",
                    "pour l",
                    "modifiant",
                    "d'alsace",
                    "d'empire",
                    "du gouverneur",
                    "du chancelier",
                    "du président",
                    "annexe",
                    "note",
                    "en vue",
                    "communale",
                    "pénale",
                    "local",
                    "d'introduction",
                    "d'application",
                    "d'exécution",
                    "civil",
                    "(extraits)",
                ]
            ):
                skip_header = False

        if not skip_header:
            cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)

    # Clean up excessive whitespace while preserving paragraph structure
    # Replace multiple blank lines with double newline
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Make Article headers bold
    text = re.sub(r"^(Article\s+\d+\w*(?:\s*er)?)", r"**\1**", text, flags=re.MULTILINE)
    text = re.sub(r"^(Art\.\s+\d+\w*)", r"**\1**", text, flags=re.MULTILINE)
    text = re.sub(r"^(§\s*\d+\w*)", r"**\1**", text, flags=re.MULTILINE)

    return text.strip()


def generate_markdown(
    title: str,
    date_str: str,
    type_texte: str,
    categories: list[str],
    content: str,
    pdf_filename: str,
    law_number: int,
) -> str:
    """Generate a Hugo markdown file with frontmatter."""
    cats_yaml = "\n".join(f'  - "{cat}"' for cat in categories)

    md = f"""---
title: "{title}"
date: {date_str}
type_texte: "{type_texte}"
categories:
{cats_yaml}
---

{content}
"""
    return md


def make_filename(title: str, law_number: int, pdf_idx: int) -> str:
    """Create a unique filename for the law."""
    # Extract date part for filename
    date_match = re.search(
        r"du\s+(\d{1,2}(?:er)?)\s+(janvier|février|fevrier|mars|avril|mai|juin|juillet|août|aout|septembre|octobre|novembre|décembre|decembre)\s+(\d{4})",
        title,
        re.IGNORECASE,
    )

    if date_match:
        slug = slugify(title)
    else:
        slug = slugify(title)

    # Truncate slug if too long
    if len(slug) > 80:
        slug = slug[:80].rsplit("-", 1)[0]

    return slug + ".md"


def main():
    # Load index
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index = json.load(f)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    seen_filenames = set()

    for pdf_idx, pdf_info in enumerate(index["pdfs"]):
        pdf_path = os.path.join(PDF_DIR, pdf_info["filename"])
        print(f"\nProcessing: {pdf_info['filename']}")
        print(f"  Laws: {len(pdf_info['laws'])}")

        doc = pymupdf.open(pdf_path)

        for law in pdf_info["laws"]:
            title = law["title"]
            first_page = law["first_page"]
            last_page = law["last_page"]

            print(f"  [{law['number']}] {title} (pp. {first_page}-{last_page})")

            # Extract date
            date_str = extract_date_from_title(title)
            if not date_str:
                print(f"    WARNING: Could not extract date from title, using fallback")
                date_str = "1900-01-01"

            # Detect type
            type_texte = detect_type_texte(title)

            # Classify
            categories = classify_law(title)

            # Extract text
            raw_text = extract_law_text(doc, first_page, last_page)
            content = clean_law_text(raw_text, title)

            # Generate filename
            filename = make_filename(title, law["number"], pdf_idx)

            # Handle duplicates
            if filename in seen_filenames:
                filename = filename.replace(".md", f"-{pdf_idx + 1}.md")
            seen_filenames.add(filename)

            # Generate markdown
            md_content = generate_markdown(
                title=title,
                date_str=date_str,
                type_texte=type_texte,
                categories=categories,
                content=content,
                pdf_filename=pdf_info["filename"],
                law_number=law["number"],
            )

            # Use the first category as the subfolder
            primary_category = categories[0]
            category_dir = os.path.join(OUTPUT_DIR, primary_category)
            os.makedirs(category_dir, exist_ok=True)

            # Write file
            output_path = os.path.join(category_dir, filename)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md_content)

            print(f"    -> {primary_category}/{filename} ({type_texte}, {categories})")

        doc.close()

    print(f"\nDone! Generated files in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
