#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pdfminer.six",
# ]
# ///
"""
Extract laws from two Droit Local PDFs and write Hugo markdown content files.
"""

import re
import unicodedata
from pathlib import Path
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / "content" / "textes"

PDFS = [
    {
        "path": BASE_DIR
        / "Recueil spécial DROIT LOCAL du 15 mai 2013 - publication traduction lois et règlements locaux maintenus en vigueur par les lois du 1er juin 1924.pdf",
        "recueil": "RAA spécial du 15 mai 2013",
        "content_start_page": 8,
    },
    {
        "path": BASE_DIR
        / "Recueil spécial DROIT LOCAL du 29 août 2013 - publication traduction lois et règlements locaux maintenus en vigueur par les lois du 1er juin 1924 .pdf",
        "recueil": "RAA spécial du 29 août 2013",
        "content_start_page": 7,
    },
]

LAW_HEADING_RE = re.compile(
    r"^("
    r"Loi\s+(?:d[u'\x27]|de\s+|du\s+|n[°o]\s*\d+\s+du\s+|d'Alsace|d'Empire|d'introduction|communale|pénale|relative|sur\s+)"
    r"|Ordonnance\s+(?:du|impériale|ministérielle|de\s+l'|du\s+Gouverneur|du\s+Président|du\s+Chancelier|modificative)"
    r"|Code\s+(?:pénal|civil|local|des\s+assurances|de\s+procédure)"
    r"|Arrêté\s+(?:du|ministériel|pris\s+en\s+vertu)"
    r"|Règlement\s+(?:ministériel\s+du|du\s+\d)"
    r"|Proclamation\s+ministérielle\s+du"
    r"|Instruction\s+pour\s+les\s+écoles"
    r"|Convention\s+du\s+\d"
    r"|Décision\s+du\s+\d"
    r").{5,}",
    re.IGNORECASE,
)

CATEGORY_RULES = [
    (
        [
            "enseignement",
            "école",
            "écoles",
            "scolaire",
            "instituteur",
            "instruction pour les écoles",
        ],
        "enseignement",
        "Enseignement",
    ),
    (
        [
            "culte",
            "cultes",
            "église",
            "consistoire",
            "synode",
            "rabbin",
            "rabbinique",
            "pasteur",
            "protestant",
            "catholique",
            "théologie",
            "séminaire",
            "confession d'augsbourg",
            "réformée",
            "israélite",
            "presbytéral",
        ],
        "cultes-religions",
        "Cultes et religions",
    ),
    (
        [
            "fonctionnaire",
            "pension",
            "retraite",
            "veuve",
            "orphelin",
            "statut des fonctionnaires",
            "ministre des cultes rétribués",
            "traitements et pensions",
        ],
        "fonctionnaires",
        "Fonctionnaires",
    ),
    (
        [
            "chasse",
            "gibier",
            "oiseau",
            "oiseaux",
            "tétras",
            "caille",
            "canard",
            "police rurale",
        ],
        "chasse-environnement",
        "Chasse et environnement",
    ),
    (
        [
            "code civil",
            "civil local",
            "introduction du code civil",
            "patrimoine",
            "sections de communes",
            "ventes à tempérament",
            "navigation intérieure",
            "eaux",
            "hydraulique",
            "drainage",
            "irrigation",
            "taureaux reproducteurs",
        ],
        "droit-civil",
        "Droit civil",
    ),
    (
        [
            "pénal",
            "code pénal",
            "construire",
            "construction",
            "police des constructions",
            "affichage",
            "liberté de construire",
        ],
        "droit-penal-urbanisme",
        "Droit pénal et urbanisme",
    ),
    (
        [
            "commerce",
            "professions",
            "assurance",
            "coopérative",
            "employé",
            "assurances sociales",
            "code du commerce",
            "travail dominical",
            "repos dominical",
            "industries extractives",
            "économie forestière",
            "travail de la pierre",
        ],
        "commerce-professions",
        "Commerce et professions",
    ),
    (
        [
            "organisation de l'administration",
            "budget d'alsace",
            "impôt foncier",
            "cadastre",
            "jours fériés",
            "bulletin de vote",
            "honoraires des notaires",
            "interprètes",
            "exécution forcée",
            "non-dommageabilité",
            "associations et des réunions",
            "réunions et des associations",
            "droit public des associations",
            "district",
            "administration",
            "loi communale",
            "commune",
            "domicile de secours",
        ],
        "administration",
        "Administration",
    ),
    (
        [
            "justice",
            "frais de justice",
            "procédure civile",
            "judiciaire",
            "notaire",
            "indemnit",
            "témoins et experts",
            "charges judiciaires",
        ],
        "justice",
        "Justice",
    ),
]

DEFAULT_CATEGORY = ("autres", "Autres textes")


def slugify(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")[:80]


def extract_date_from_title(title: str) -> str:
    months = {
        "janvier": "01",
        "février": "02",
        "mars": "03",
        "avril": "04",
        "mai": "05",
        "juin": "06",
        "juillet": "07",
        "août": "08",
        "septembre": "09",
        "octobre": "10",
        "novembre": "11",
        "décembre": "12",
    }
    m = re.search(
        r"\bdu\s+(\d{1,2})(?:er|ème|e)?\s+("
        + "|".join(months.keys())
        + r")\s+(\d{4})\b",
        title,
        re.IGNORECASE,
    )
    if m:
        day, month_str, year = m.group(1), m.group(2).lower(), m.group(3)
        return f"{year}-{months[month_str]}-{int(day):02d}"
    years = re.findall(r"\b(1[89]\d{2})\b", title)
    if years:
        return f"{years[0]}-01-01"
    return "1900-01-01"


def get_type(title: str) -> str:
    t = title.lower()
    if t.startswith("loi"):
        return "Loi"
    if t.startswith("ordonnance"):
        return "Ordonnance"
    if t.startswith("code"):
        return "Code"
    if t.startswith("arrêté"):
        return "Arrêté"
    if t.startswith("règlement"):
        return "Règlement"
    if t.startswith("proclamation"):
        return "Proclamation"
    if t.startswith("instruction"):
        return "Instruction"
    if t.startswith("convention"):
        return "Convention"
    if t.startswith("décision"):
        return "Décision"
    return "Texte"


def get_category(title: str, body: str = "") -> tuple:
    # Match against title + first 300 chars of body to catch subtitles like
    # "Loi du 12 février 1873" whose subtitle "sur l'enseignement" is in body
    t = (title + " " + body[:300]).lower()
    for keywords, slug, label in CATEGORY_RULES:
        if any(kw in t for kw in keywords):
            return slug, label
    return DEFAULT_CATEGORY


def clean_text(text: str) -> str:
    text = re.sub(r"RAA\s+N°\s+Spécial\s+du\s+\d+\s+\w+\s+\d{4}", "", text)
    text = re.sub(r"^\s*\d{1,3}\s*$", "", text, flags=re.MULTILINE)
    return text


def extract_pages_text(pdf_path: Path, start_page: int) -> list:
    pages = []
    for page_num, page_layout in enumerate(extract_pages(str(pdf_path)), start=1):
        if page_num < start_page:
            continue
        parts = []
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                parts.append(element.get_text())
        pages.append((page_num, "".join(parts)))
    return pages


def _is_valid_heading(line: str) -> bool:
    """
    Filter out false-positive headings:
    - Lines with many double spaces (pdfminer column extraction artifacts)
    - Lines ending mid-sentence (e.g. "Code pénal seront pris par les autorités de")
    - Lines that are clearly body fragments (lowercase start after first word)
    - Lines that don't end with a real word character or known punctuation
    """
    # Reject lines with 3+ consecutive spaces (layout artifacts)
    if re.search(r" {3,}", line):
        return False
    # Reject lines ending with common prepositions/articles (truncated sentence)
    if re.search(
        r"\b(de|du|des|le|la|les|un|une|par|dans|sur|et|ou|à|au|aux|avec|pour|en|d'|l')\s*$",
        line,
        re.IGNORECASE,
    ):
        return False
    # Must be reasonably capitalized (real heading starts with capital)
    if line[0].islower():
        return False
    return True


def split_into_laws(pages: list, recueil: str) -> list:
    laws = []
    current_title = None
    current_body = []

    for _, raw_text in pages:
        text = clean_text(raw_text)
        for line in text.split("\n"):
            stripped = line.strip()
            if (
                stripped
                and LAW_HEADING_RE.match(stripped)
                and _is_valid_heading(stripped)
            ):
                if current_title:
                    laws.append(
                        {
                            "title": current_title,
                            "body": "\n".join(current_body).strip(),
                            "recueil": recueil,
                        }
                    )
                current_title = stripped
                current_body = []
            elif current_title:
                current_body.append(line)

    if current_title:
        laws.append(
            {
                "title": current_title,
                "body": "\n".join(current_body).strip(),
                "recueil": recueil,
            }
        )

    return laws


def format_body(body: str) -> str:
    lines = body.split("\n")
    result = []
    for line in lines:
        s = line.strip()
        if not s:
            result.append("")
            continue
        art = re.match(
            r"^(Article\s+\d+(?:er|ème|e)?|Art\.?\s*\d+(?:er|ème|e)?)\s*$",
            s,
            re.IGNORECASE,
        )
        if art:
            result.append(f"\n### {s}\n")
        elif s.isupper() and len(s) < 80:
            result.append(f"\n**{s.capitalize()}**\n")
        else:
            result.append(s)
    return "\n".join(result)


def write_law(law: dict, output_dir: Path) -> Path:
    title = law["title"]
    body = law["body"]
    recueil = law["recueil"]

    date = extract_date_from_title(title)
    doc_type = get_type(title)
    cat_slug, cat_label = get_category(title, body)
    slug = slugify(title)

    cat_dir = output_dir / cat_slug
    cat_dir.mkdir(parents=True, exist_ok=True)

    filepath = cat_dir / f"{slug}.md"
    if filepath.exists():
        suffix = slugify(recueil.replace("RAA spécial du ", ""))
        filepath = cat_dir / f"{slug}-{suffix}.md"

    safe_title = title.replace('"', '\\"')
    md_body = format_body(body)

    filepath.write_text(
        f'---\ntitle: "{safe_title}"\ndate: {date}\nrecueil: "{recueil}"\ntype_texte: "{doc_type}"\ncategories: ["{cat_label}"]\n---\n\n{md_body}\n',
        encoding="utf-8",
    )
    return filepath


def main():
    print("=== Extracting Droit Local PDFs to Hugo content ===\n")
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    total = 0
    for pdf_info in PDFS:
        print(f"\nProcessing: {pdf_info['path'].name}")
        pages = extract_pages_text(pdf_info["path"], pdf_info["content_start_page"])
        print(f"  {len(pages)} content pages extracted")
        laws = split_into_laws(pages, pdf_info["recueil"])
        print(f"  {len(laws)} legal texts found")
        for law in laws:
            fp = write_law(law, CONTENT_DIR)
            print(f"    -> {fp.relative_to(BASE_DIR)}")
            total += 1
    print(f"\nDone! {total} texts written to {CONTENT_DIR}")


if __name__ == "__main__":
    main()
