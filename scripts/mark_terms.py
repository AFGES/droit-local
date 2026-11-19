#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""Insert {{< t >}} / {{< m >}} shortcodes in content/textes/**/*.md.

Usage: mark_terms.py [--dry-run]. Idempotent. Reports ambiguous words left untouched.
Texts are hard-wrapped, so matching runs per paragraph: a term or an amount split by a
line break is still found (the break becomes a space inside the shortcode).
"""
import pathlib
import re
import sys

import yaml

BASE = pathlib.Path(__file__).resolve().parent.parent
TERMS = yaml.safe_load((BASE / "data" / "correspondances.yaml").read_text("utf-8"))
SC = re.compile(r"\{\{<.*?>\}\}")
# Amount (digits; space, nbsp or dot as thousands separator), then "mark(s)", maybe after a line break.
MARKS = re.compile(r"(?<![\w,.])(\d{1,3}(?:[  .]\d{3})+|\d+)(\s+)(marks?)\b")
SPELLED_MARKS = re.compile(r"\b(?:[a-zéè-]+\s+){1,3}marks?\b", re.I)
NUMBER_WORDS = {
    "un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5, "six": 6, "sept": 7,
    "huit": 8, "neuf": 9, "dix": 10, "onze": 11, "douze": 12, "treize": 13, "quatorze": 14,
    "quinze": 15, "seize": 16, "vingt": 20, "vingts": 20, "trente": 30, "quarante": 40,
    "cinquante": 50, "soixante": 60,
}
SPELLED_AMOUNT = re.compile(
    r"\b((?:(?:%s|cents?|mille|demi|et)[\s-]+)+)(marks?)\b" % "|".join(NUMBER_WORDS), re.I
)
CELL_AMOUNT = re.compile(r"\d{1,3}(?:[  ]\d{3})*|\d+")
AMBIGUOUS = re.compile(r"\b(cercles?|provinces?|allemande?s?)\b", re.I)


def term_regex(orig: str) -> re.Pattern:
    """Literal term; any whitespace (newline included) between words; either apostrophe."""
    words = [re.sub(r"['’]", "['’]", re.escape(w)) for w in orig.split()]
    return re.compile(r"\s+".join(words), re.I)


TERM_RES = [(t, term_regex(t["orig"])) for t in TERMS]


def esc(s: str) -> str:
    return " ".join(s.split()).replace('"', "&quot;")


def parse_spelled(words: str) -> float | None:
    """French number words -> value, None when the phrase is not understood."""
    toks = [t.lower() for t in re.split(r"[\s-]+", words.strip()) if t]
    while toks and toks[0] == "et":
        toks.pop(0)
    if toks in (["un", "demi"], ["une", "demi"]):
        return 0.5
    total = cur = 0
    for t in toks:
        if t in NUMBER_WORDS:
            n = NUMBER_WORDS[t]
            # "quatre-vingt(s)" is 80, "quatre-vingt-dix" 90.
            cur = cur * n if (t.startswith("vingt") and cur == 4) else cur + n
        elif t.startswith("cent"):
            cur = max(cur, 1) * 100
        elif t == "mille":
            total += max(cur, 1) * 1000
            cur = 0
        elif t != "et":
            return None
    return float(total + cur) if total + cur else None


def spelled_to_shortcode(m: re.Match) -> str:
    value = parse_spelled(m.group(1))
    if value is None:
        return m.group(0)
    return '{{< m "%s" "marks" "%s" >}}' % (f"{value:g}", esc(m.group(0)))


def mark_table(block: list[str]) -> list[str]:
    """In a table whose header says « en marks », turn the numeric cells of that column into {{< mb >}}."""
    cells = block[0].split("|")
    idx = next((k for k, c in enumerate(cells) if "(en marks)" in c), None)
    if idx is None:
        return block
    out = [block[0]]
    for row in block[1:]:
        parts = row.split("|")
        if idx < len(parts) and CELL_AMOUNT.fullmatch(parts[idx].strip()):
            digits = re.sub(r"\D", "", parts[idx])
            parts[idx] = ' {{< mb "%s" >}} ' % digits
        out.append("|".join(parts))
    return out


def mark_text(text: str) -> str:
    # Protect existing shortcodes.
    parts = SC.split(text)
    codes = SC.findall(text)
    out = []
    for p in parts:
        for t, rx in TERM_RES:
            def rep(m, t=t):
                new = t["new"]
                if m.group(0)[0].isupper():
                    new = new[0].upper() + new[1:]
                return '{{< t "%s" "%s" >}}' % (esc(m.group(0)), esc(new))
            p = rx.sub(rep, p)
        p = SPELLED_AMOUNT.sub(spelled_to_shortcode, p)
        p = MARKS.sub(
            lambda m: '{{< m "%s" "%s" >}}' % (re.sub(r"\D", "", m.group(1)), m.group(3)),
            p,
        )
        out.append(p)
    res = out[0]
    for c, p in zip(codes, out[1:]):
        res += c + p
    return res


def is_plain(line: str) -> bool:
    return bool(line.strip()) and not line.startswith(("|", "#", "---", "```"))


def mark_body(lines: list[str]) -> list[str]:
    """Process paragraph by paragraph. Tables, headings and blank lines stand alone."""
    new: list[str] = []
    i = 0
    while i < len(lines):
        j = i + 1
        if is_plain(lines[i]):
            while j < len(lines) and is_plain(lines[j]):
                j += 1
        if lines[i].startswith("|"):
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            block = [mark_text(l) for l in mark_table(lines[i:j])]
            new.extend(block)
        else:
            new.extend(mark_text("\n".join(lines[i:j])).split("\n"))
        i = j
    return new


def main() -> None:
    dry = "--dry-run" in sys.argv
    changed = 0
    for f in sorted((BASE / "content" / "textes").rglob("*.md")):
        if f.name in ("_index.md", "correspondances.md"):
            continue
        lines = f.read_text("utf-8").split("\n")
        end = 0  # front matter ends at the second "---"
        if lines and lines[0].strip() == "---":
            end = next((k for k in range(1, len(lines)) if lines[k].strip() == "---"), 0) + 1
        new = lines[:end] + mark_body(lines[end:])
        plain = "\n".join(SC.sub("", l) for l in new[end:])
        for m in AMBIGUOUS.finditer(plain):
            print(f"AMBIGU {f.relative_to(BASE)}: {m.group(0)}")
        for m in SPELLED_MARKS.finditer(plain):
            print(f"AMBIGU-MARKS {f.relative_to(BASE)}: {' '.join(m.group(0).split())}")
        if new != lines:
            changed += 1
            if not dry:
                f.write_text("\n".join(new), "utf-8")
    print(f"{changed} fichiers {'à modifier' if dry else 'modifiés'}")


if __name__ == "__main__":
    main()
