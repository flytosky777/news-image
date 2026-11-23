#!/usr/bin/env python3
"""Build entry.png for news-image-20261123 v2: an illustrated front page.

Layout (1024x1024, warm paper): masthead with the date, a wide photo of
the empty COP31 hall as the top story, then five rows, each with a small
illustrative picture, a kicker, a headline and one line. Every story is
one of the six verified stories of Monday 23 November 2026; nothing here
is invented. Deterministic: same inputs, same bytes, no network, no
randomness, no timestamps in the PNG.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
GREY = (107, 101, 90)
RED = (166, 30, 30)
RULE = (166, 30, 30)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, start, max_w):
    """Largest font size at or below start whose text fits max_w."""
    size = start
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, 10)


def wrap(draw, text, f, max_w):
    """Greedy word wrap, returns a list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def thumb(path, size):
    """Square thumbnail: centre-crop, resize, rounded corners."""
    im = Image.open(path).convert("RGB")
    w, h = im.size
    side = min(w, h)
    im = im.crop(((w - side) // 2, (h - side) // 2,
                  (w - side) // 2 + side, (h - side) // 2 + side))
    im = im.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size, size], radius=8, fill=255)
    out = Image.new("RGB", (size, size), PAPER)
    out.paste(im, (0, 0), mask)
    return out


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    M = 40                      # margin
    CW = W - 2 * M              # content width: 944

    # Masthead.
    d.text((M, 26), "T H E   W O R L D   I N   O N E   D A Y",
           font=font(SANS_B, 22), fill=GREY)
    f_date = fit(d, "MONDAY 23 NOVEMBER 2026", SERIF_B, 60, CW)
    d.text((M, 54), "MONDAY 23 NOVEMBER 2026", font=f_date, fill=INK)
    d.rectangle([M, 130, W - M, 134], fill=RULE)

    # Hero: the empty COP31 hall, cropped wide.
    hero = Image.open(os.path.join(ASSETS, "hero.png")).convert("RGB")
    hw, hh = hero.size
    target_h = int(hw * 300 / CW)
    top = (hh - target_h) // 2
    hero = hero.crop((0, top, hw, top + target_h))
    hero = hero.resize((CW, 300), Image.LANCZOS)
    page.paste(hero, (M, 146))

    # Top story caption.
    d.text((M, 458), "TOP STORY  \u2022  CLIMATE",
           font=font(SANS_B, 20), fill=RED)
    f_head = fit(d, "COP31 climate talks collapse with no deal",
                 SERIF_B, 44, CW)
    d.text((M, 482), "COP31 climate talks collapse with no deal",
           font=f_head, fill=INK)
    f_deck = font(SANS, 21)
    deck = ("UN negotiations end without an agreement after the EU rejects "
            "any pact with no language on phasing out fossil fuels.")
    lines = wrap(d, deck, f_deck, CW)
    y = 530
    for line in lines[:2]:
        d.text((M, y), line, font=f_deck, fill=INK)
        y += 26
    d.line([M, 590, W - M, 590], fill=(180, 172, 158), width=1)

    # Five stories, each with its own picture.
    rows = [
        ("iran.webp", "U.S. \u2013 IRAN", (31, 78, 121),
         "Trump threatens to sink Iranian ships",
         "After a US strike on an oil tanker; Houthis claim hits on a Saudi refinery."),
        ("markets.webp", "MARKETS", (183, 121, 31),
         "AI sell-off rattles world markets",
         "Seoul's KOSPI plunges 5%; US futures rebound as Nasdaq jumps 3%."),
        ("capitol.webp", "U.S. POLITICS", (46, 125, 50),
         "Democrats win biggest House majority since 1992",
         "258 seats clinched after a North Carolina recount win."),
        ("rescue.webp", "UKRAINE", (106, 63, 160),
         "Boy, 7, pulled alive from rubble",
         "Rescuers free a child hours after a Russian strike on Ukraine."),
        ("baseball.webp", "SPORT", (141, 85, 36),
         "Mets sign Skubal for a record $450m",
         "Nine-year deal is the richest ever for a pitcher."),
    ]
    y = 602
    for name, kicker, colour, headline, sub in rows:
        t = thumb(os.path.join(ASSETS, name), 68)
        page.paste(t, (M, y))
        tx = M + 84
        tw = W - M - tx
        d.text((tx, y + 1), kicker, font=font(SANS_B, 16), fill=colour)
        f_h = fit(d, headline, SERIF_B, 28, tw)
        d.text((tx, y + 20), headline, font=f_h, fill=INK)
        f_s = fit(d, sub, SANS, 19, tw)
        d.text((tx, y + 51), sub, font=f_s, fill=(60, 60, 60))
        y += 76

    # Footer.
    d.rectangle([M, 980, W - M, 982], fill=RULE)
    d.text((M, 987), "All events reported on Monday 23 November 2026",
           font=font(SANS_B, 16), fill=INK)
    d.text((M, 1004), "Sources: BBC  \u2022  The Hindu  \u2022  Fortune  \u2022  "
                       "BusinessLine  \u2022  Indian Express",
           font=font(SANS, 14), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    page.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
