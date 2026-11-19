#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Link citations of other laws in content/textes/**/*.md to the cited page.

Usage: link_laws.py [--dry-run]. Idempotent. A citation ("loi du 7 mai 1883", "ordonnance du 22 avril 1902")
becomes a Markdown link when exactly one page of the corpus matches (front matter date, then type and title
words for dates shared by several texts). Unknown or ambiguous citations are reported and left as is.
Texts are hard-wrapped, so matching runs per paragraph; a line break inside a citation is kept in the link text.
"""
import pathlib
import re
import sys
from collections import defaultdict

BASE = pathlib.Path(__file__).resolve().parent.parent
TEXTES = BASE / "content" / "textes"
MONTHS = "janvier février mars avril mai juin juillet août septembre octobre novembre décembre".split()
SC = re.compile(r"\{\{<.*?>\}\}")
LINK = re.compile(r"\[[^\]]*\]\([^)]*\)")
TYPE = (
    r"(?:[Ll]oi|[Oo]rdonnance|[Aa]rrêté|[Dd]écret|[Rr]èglement|[Cc]ode civil local)"
    r"(?:\s+(?:d['’]Empire|d['’]Alsace-Lorraine|impériale?|ministériel(?:le)?|communale?|locale?))*"
)
CITATION = re.compile(
    rf"(?P<cite>{TYPE}\s+(?:du|de)\s+(?P<d>\d{{1,2}})(?:er)?\s+(?P<m>{'|'.join(MONTHS)})\s+(?P<y>\d{{4}}))"
    r"(?P<after>.{0,70})",
    re.S,
)
STOP = {"relative", "relatif", "portant", "concernant", "pour", "dans", "avec", "sont", "cette", "leur", "ainsi"}


def words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-zéèêàâîôûç'’-]{4,}", s.lower()) if w not in STOP}


def front(text: str) -> dict[str, str]:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    out = {}
    for line in (m.group(1) if m else "").split("\n"):
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip().strip('"')
    return out


def build_index() -> dict[tuple[int, int, int], list[dict]]:
    idx = defaultdict(list)
    for f in sorted(TEXTES.rglob("*.md")):
        if f.name in ("_index.md", "correspondances.md"):
            continue
        fm = front(f.read_text("utf-8"))
        try:
            y, mo, d = map(int, fm["date"].split("-"))
        except (KeyError, ValueError):
            continue
        rel = f.relative_to(BASE / "content").with_suffix("")
        idx[(d, mo, y)].append({"file": f, "url": f"/{rel}/", "title": fm.get("title", "")})
    return idx


def resolve(cands: list[dict], cite: str, after: str, here: pathlib.Path) -> dict | None:
    if len(cands) == 1:
        return cands[0]
    cw = words(cite + " " + after)
    first = cite.split()[0].lower()
    scored = []
    for c in cands:
        t = c["title"].lower()
        scored.append((len(cw & words(t)) + (2 if t.startswith(first) else 0), c))
    scored.sort(key=lambda x: -x[0])
    if scored[0][0] > scored[1][0]:
        return scored[0][1]
    # Tie: prefer the only candidate in the same section as the citing page.
    same = [c for c in cands if c["file"].parent == here.parent]
    return same[0] if len(same) == 1 else None


def link_text(text: str, idx, here: pathlib.Path, report: list[str]) -> str:
    parts = SC.split(text)
    shortcodes = SC.findall(text)
    out = []
    for i, part in enumerate(parts):
        segs = []
        pos = 0
        for lm in LINK.finditer(part):
            segs.append((part[pos:lm.start()], True))
            segs.append((lm.group(0), False))
            pos = lm.end()
        segs.append((part[pos:], True))
        buf = []
        for seg, editable in segs:
            if editable:
                seg = link_seg(seg, idx, here, report)
            buf.append(seg)
        out.append("".join(buf))
        if i < len(shortcodes):
            out.append(shortcodes[i])
    return "".join(out)


def link_seg(seg: str, idx, here: pathlib.Path, report: list[str]) -> str:
    res, pos = [], 0
    while True:
        m = CITATION.search(seg, pos)
        if not m:
            res.append(seg[pos:])
            return "".join(res)
        cite = m.group("cite")
        key = (int(m.group("d")), MONTHS.index(m.group("m")) + 1, int(m.group("y")))
        res.append(seg[pos:m.start()])
        pos = m.end("cite")
        cands = idx.get(key, [])
        flat = " ".join(cite.split())
        if not cands:
            report.append(f"ABSENT {here.relative_to(BASE)}: {flat}")
            res.append(cite)
            continue
        target = resolve(cands, cite, m.group("after"), here)
        if target is None:
            report.append(f"AMBIGU {here.relative_to(BASE)}: {flat} -> {[c['url'] for c in cands]}")
            res.append(cite)
        elif target["file"] == here:
            res.append(cite)
        else:
            report.append(f"LIEN {here.relative_to(BASE)}: {flat} -> {target['url']}")
            res.append(f"[{cite}]({target['url']})")


def link_body(lines: list[str], idx, here, report) -> list[str]:
    new, i = [], 0
    while i < len(lines):
        if not lines[i].strip():
            new.append(lines[i]); i += 1; continue
        j = i
        while j < len(lines) and lines[j].strip():
            j += 1
        block = lines[i:j]
        if block[0].lstrip().startswith(("#", "|")):
            new.extend(block)
        else:
            new.extend(link_text("\n".join(block), idx, here, report).split("\n"))
        i = j
    return new


def main() -> None:
    dry = "--dry-run" in sys.argv
    idx = build_index()
    changed, report = 0, []
    for f in sorted(TEXTES.rglob("*.md")):
        if f.name in ("_index.md", "correspondances.md"):
            continue
        lines = f.read_text("utf-8").split("\n")
        end = 0
        if lines and lines[0].strip() == "---":
            end = next((k for k in range(1, len(lines)) if lines[k].strip() == "---"), 0) + 1
        new = lines[:end] + link_body(lines[end:], idx, f, report)
        if new != lines:
            changed += 1
            if not dry:
                f.write_text("\n".join(new), "utf-8")
    print("\n".join(report))
    print(f"{changed} fichiers {'à modifier' if dry else 'modifiés'}")


if __name__ == "__main__":
    main()
