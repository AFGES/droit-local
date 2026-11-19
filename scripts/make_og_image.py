#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["cairosvg", "pillow"]
# ///
"""Generate static/og-image.png (1200x630): AFGES logo + site title.

Usage: make_og_image.py. Reads assets/afges-logo.svg, writes static/og-image.png.
"""
import io
import pathlib
import subprocess

import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H = 1200, 630
BG = (248, 250, 252)
FG = (30, 41, 59)
MUTED = (71, 85, 105)


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    pattern = "sans:bold" if bold else "sans"
    path = subprocess.run(
        ["fc-match", "-f", "%{file}", pattern], capture_output=True, text=True, check=True
    ).stdout
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


def main() -> None:
    logo_png = cairosvg.svg2png(url=str(ROOT / "assets/afges-logo.svg"), output_height=360)
    logo = Image.open(io.BytesIO(logo_png)).convert("RGBA")
    img = Image.new("RGB", (W, H), BG)
    img.paste(logo, (90, (H - logo.height) // 2), logo)
    draw = ImageDraw.Draw(img)

    x = 90 + logo.width + 80
    width = W - x - 70
    title_f, sub_f = font(64), font(30, bold=False)
    y = 150
    for line in wrap(draw, "Droit local d’Alsace-Moselle", title_f, width):
        draw.text((x, y), line, font=title_f, fill=FG)
        y += 80
    y += 20
    sub = "Lois et règlements locaux traduits et publiés en 2013"
    for line in wrap(draw, sub, sub_f, width):
        draw.text((x, y), line, font=sub_f, fill=MUTED)
        y += 44
    draw.text((x, H - 90), "droit-local.afges.org", font=sub_f, fill=MUTED)

    img.save(ROOT / "static/og-image.png", optimize=True)


if __name__ == "__main__":
    main()
