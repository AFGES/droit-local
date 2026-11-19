#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""Build data/modifs/<texte>.json from audit/<texte>.yaml (audit files).

Usage: build_modifications.py [--check]. Idempotent. For each audit entry, find where to show it:
  - "heading": the article exists in the Markdown ("## Article N"): the banner follows that heading;
  - "page":    the entry targets the whole text ("tout");
  - "extra":   no matching heading (inserted or absent articles): listed at the end of the page.
scope "full" (the whole article is concerned) lets the layout replace the article body in "droit en vigueur" mode;
scope "partial" (alinéa, phrase, point) only adds the new wording next to the original.
Entries with confiance "a_verifier" never replace the original (layout rule, see layouts/_default/_markup).
--check exits 1 when data/modifs is out of date (CI).
"""
import json
import pathlib
import re
import sys

import yaml

BASE = pathlib.Path(__file__).resolve().parent.parent
TEXTES = BASE / "content" / "textes"
SRC = BASE / "audit"
OUT = BASE / "data" / "modifs"
HEADING = re.compile(r"^#{2,6}\s+Article\s+(.+?)\s*$", re.M)
NUM = re.compile(r"^(\d+(?:er)?(?:\s+[a-z]\d*)?)(?=\s|$|\()", re.I)
PARTIAL = re.compile(r"\((?:al\.|alin|phrase|[0-9]+°|point|deuxi|premi|derni|2e|3e)|\bal\. ", re.I)


def norm(s: str) -> str:
    return re.sub(r"^(\d+)er\b", r"\1", re.sub(r"\s+", " ", s.strip()).lower())


def pages() -> dict[str, pathlib.Path]:
    return {p.stem: p for p in TEXTES.rglob("*.md") if not p.name.startswith("_")}


def classify(article: str, headings: dict[str, str]) -> tuple[str, str, str]:
    """Return (placement, heading text, scope) for an audit "article" key."""
    key = article.strip()
    if norm(key) == "tout":
        return "page", "", "full"
    if key.lower().startswith("apres-") or re.search(r"\bà\b", key) or "absent" in key.lower():
        return "extra", "", "full"
    m = NUM.match(key)
    if not m:
        return "extra", "", "full"
    heading = headings.get(norm(m.group(1)))
    if not heading:
        return "extra", "", "full"
    rest = key[m.end():].strip()
    return "heading", heading, "partial" if rest and PARTIAL.search(rest) else ("partial" if rest else "full")


def build() -> dict[str, str]:
    md = pages()
    out: dict[str, str] = {}
    for src in sorted(SRC.glob("*.yaml")):
        slug = src.stem
        if slug not in md:
            print(f"WARN: {src.name}: aucun texte {slug}.md", file=sys.stderr)
            continue
        headings: dict[str, str] = {}
        for h in HEADING.findall(md[slug].read_text("utf-8")):
            headings.setdefault(norm(h), f"Article {h}")
        entries = []
        for e in yaml.safe_load(src.read_text("utf-8")) or []:
            placement, heading, scope = classify(str(e["article"]), headings)
            entries.append({
                "article": str(e["article"]),
                "placement": placement,
                "heading": heading,
                "scope": scope,
                "statut": e["statut"],
                "date": str(e.get("date") or ""),
                "source": e.get("source") or "",
                "jorf": e.get("jorf") or "",
                "confiance": e.get("confiance") or "a_verifier",
                "officiel": bool(e.get("texte_actuel_officiel", False)),
                "texte_actuel": (e.get("texte_actuel") or "").strip(),
                "texte_origine": (e.get("texte_origine") or "").strip(),
                "texte_origine_allemand": (e.get("texte_origine_allemand") or "").strip(),
                "note": e.get("note") or "",
            })
        out[slug + ".json"] = json.dumps({"entries": entries}, ensure_ascii=False, indent=1) + "\n"
    return out


def main() -> int:
    files = build()
    if "--check" in sys.argv:
        stale = [n for n, t in files.items() if not (OUT / n).exists() or (OUT / n).read_text("utf-8") != t]
        stale += [p.name for p in OUT.glob("*.json") if p.name not in files] if OUT.exists() else []
        for n in stale:
            print("obsolète :", n)
        return 1 if stale else 0
    OUT.mkdir(parents=True, exist_ok=True)
    for p in OUT.glob("*.json"):
        if p.name not in files:
            p.unlink()
    for n, t in files.items():
        (OUT / n).write_text(t, "utf-8")
    kinds: dict[str, int] = {}
    for t in files.values():
        for e in json.loads(t)["entries"]:
            kinds[e["placement"]] = kinds.get(e["placement"], 0) + 1
    print(f"{len(files)} textes, placements : {kinds}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
