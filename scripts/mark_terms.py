#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""Insert {{< t >}} / {{< m >}} shortcodes in content/textes/**/*.md.

Usage: mark_terms.py [--dry-run]. Idempotent. Reports ambiguous words left untouched.
"""
import pathlib
import re
import sys

import yaml

BASE = pathlib.Path(__file__).resolve().parent.parent
TERMS = yaml.safe_load((BASE / "data" / "correspondances.yaml").read_text("utf-8"))
SC = re.compile(r"\{\{<.*?>\}\}")
MARKS = re.compile(r"(?<![\w,.])(\d{1,3}(?:[  ]\d{3})+|\d+)[  ]marks?\b")
AMBIGUOUS = re.compile(r"\b(cercles?|provinces?|allemande?s?)\b", re.I)


def esc(s: str) -> str:
    return s.replace('"', "&quot;")


def mark_line(line: str) -> str:
    # Protect existing shortcodes.
    parts = SC.split(line)
    codes = SC.findall(line)
    out = []
    for p in parts:
        for t in TERMS:
            def rep(m, t=t):
                new = t["new"]
                if m.group(0)[0].isupper():
                    new = new[0].upper() + new[1:]
                return '{{< t "%s" "%s" >}}' % (esc(m.group(0)), esc(new))
            p = re.sub(re.escape(t["orig"]), rep, p, flags=re.I)
        p = MARKS.sub(
            lambda m: '{{< m "%s" "%s" >}}'
            % (re.sub(r"\D", "", m.group(1)), m.group(0)[len(m.group(1)):].strip()),
            p,
        )
        out.append(p)
    res = out[0]
    for c, p in zip(codes, out[1:]):
        res += c + p
    return res


def main() -> None:
    dry = "--dry-run" in sys.argv
    changed = 0
    for f in sorted((BASE / "content" / "textes").rglob("*.md")):
        if f.name == "_index.md":
            continue
        lines = f.read_text("utf-8").split("\n")
        fm = 0
        new = []
        for i, l in enumerate(lines):
            if l.strip() == "---" and fm < 2:
                fm += 1
                new.append(l)
                continue
            if fm < 2:
                new.append(l)
                continue
            n = mark_line(l)
            for m in AMBIGUOUS.finditer(SC.sub("", n)):
                print(f"AMBIGU {f.relative_to(BASE)}:{i+1}: {m.group(0)}")
            new.append(n)
        if new != lines:
            changed += 1
            if not dry:
                f.write_text("\n".join(new), "utf-8")
    print(f"{changed} fichiers {'à modifier' if dry else 'modifiés'}")


if __name__ == "__main__":
    main()
