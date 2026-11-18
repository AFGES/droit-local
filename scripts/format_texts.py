#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""Deterministic typography/structure cleanup of content/textes/**/*.md.

Usage: format_texts.py [--dry-run]. Idempotent. Skips front matter and {{< >}} shortcodes.
Rules: curly apostrophes, no space before , and ., nbsp before : (narrow nbsp before ; ? !),
nbsp inside « », "x" -> « x », heading levels (no h1 in body, no skipped level).
"""
import pathlib
import re
import sys
from collections import Counter

BASE = pathlib.Path(__file__).resolve().parent.parent
SC = re.compile(r"(\{\{<.*?>\}\}|\]\([^)]*\))")  # shortcodes and link targets: keep verbatim
NBSP, NNBSP = " ", " "
stats: Counter = Counter()


def sub(rule: str, pat: str, repl, s: str, flags=0) -> str:
    out, n = re.subn(pat, repl, s, flags=flags)
    stats[rule] += n
    return out


def fix_text(s: str) -> str:
    s = sub("apostrophe-escaped", r"\\'", "’", s)
    s = sub("apostrophe", r"(?<=\w)'(?=\w)", "’", s)
    s = sub("quotes", r'"([^"\n]+)"', "«" + NBSP + r"\1" + NBSP + "»", s)
    s = sub("space-before-comma-dot", r"(?<=[\w)\]»]) +([.,])(?=\s|$)", r"\1", s)
    s = sub("nbsp-colon", r"(?<=[\w)»’]) +:(?=\s|$)", NBSP + ":", s)
    s = sub("nnbsp-semicolon-qm-excl", r"(?<=[\w)»’]) +([;?!])(?=\s|$)", NNBSP + r"\1", s)
    s = sub("guillemets-space", r"«[ ]+", "«" + NBSP, s)
    s = sub("guillemets-space", r"[ ]+»", NBSP + "»", s)
    return s


def fix_line(line: str) -> str:
    parts = SC.split(line)  # odd indexes are protected
    return "".join(p if i % 2 else fix_text(p) for i, p in enumerate(parts))


def fix_headings(lines: list[str], start: int) -> None:
    idx = [i for i in range(start, len(lines)) if re.match(r"#{1,6} ", lines[i])]
    if not idx:
        return
    lv = {i: len(lines[i].split(" ", 1)[0]) for i in idx}
    shift = 1 if min(lv.values()) < 2 else 0
    prev = 1
    for i in idx:
        new = min(min(lv[i] + shift, 6), prev + 1)
        if new != lv[i]:
            stats["heading-level"] += 1
            lines[i] = "#" * new + " " + lines[i].split(" ", 1)[1]
        prev = new


def main() -> None:
    dry = "--dry-run" in sys.argv
    changed = 0
    for f in sorted((BASE / "content" / "textes").rglob("*.md")):
        if f.name == "_index.md":
            continue
        lines = f.read_text("utf-8").split("\n")
        fm, start = 0, 0
        for i, l in enumerate(lines):
            if l.strip() == "---":
                fm += 1
                if fm == 2:
                    start = i + 1
                    break
        new = lines[:start] + [fix_line(l) for l in lines[start:]]
        fix_headings(new, start)
        if new != lines:
            changed += 1
            if not dry:
                f.write_text("\n".join(new), "utf-8")
    print(dict(stats))
    print(f"{changed} fichiers {'à modifier' if dry else 'modifiés'}")


if __name__ == "__main__":
    main()
