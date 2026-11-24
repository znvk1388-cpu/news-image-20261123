#!/usr/bin/env python3
"""Draws entry.png: one image summing up the world news of Monday 23 November 2026.

Built with PIL only (standard shapes + DejaVu fonts), flat editorial style:
a newspaper front page with a dated masthead, one lead story, four panels
and an "also on Monday" strip. All headlines are as reported on 23 Nov 2026.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 247, 240)
INK = (20, 32, 43)
RED = (179, 53, 43)
BLUE = (36, 80, 122)
GOLD = (201, 146, 46)
LIGHT = (233, 226, 210)
SEA = (58, 110, 150)
SAND = (222, 184, 110)

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, width, leading=1.18):
    x, y = xy
    lines = wrap(draw, text, fnt, width)
    lh = int(fnt.size * leading)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 46  # margin

# ---------- masthead ----------
d.text((M, 30), "T H E   W O R L D   I N   O N E   D A Y", font=font(FB, 25), fill=RED)
_ds = 64
while _ds > 30 and d.textlength("MONDAY 23 NOVEMBER 2026", font=font(FS, _ds)) > W - 2 * M:
    _ds -= 2
d.text((M, 62), "MONDAY 23 NOVEMBER 2026", font=font(FS, _ds), fill=INK)
d.line([(M, 148), (W - M, 148)], fill=INK, width=5)
d.line([(M, 158), (W - M, 158)], fill=INK, width=2)
d.text((M, 168), "The day's biggest stories, in a single picture", font=font(F, 21), fill=BLUE)

# ---------- lead story: COP31 ----------
LY = 208
d.rectangle([M, LY, W - M, LY + 252], outline=INK, width=3)
d.rectangle([M, LY, W - M, LY + 40], fill=INK)
d.text((M + 14, LY + 8), "LEAD STORY · CLIMATE · TÜRKIYE", font=font(FB, 22), fill=PAPER)
_hy = text_block(d, (M + 16, LY + 54), "COP31 ENDS WITHOUT A DEAL", font(FB, 40), INK, 600)
text_block(
    d, (M + 16, _hy + 8),
    "The longest UN climate summit in history closes with no agreement on fossil fuels "
    "or finance. The UN chief is \u201cdeeply disappointed\u201d.",
    font(F, 22), INK, 590,
)
# lead illustration: globe + thermometer
gx, gy, gr = 800, LY + 142, 74
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(120, 178, 205), outline=INK, width=3)
d.ellipse([gx - 30, gy - 48, gx + 18, gy - 8], fill=(96, 160, 96))     # continent blobs
d.ellipse([gx + 8, gy + 6, gx + 52, gy + 52], fill=(96, 160, 96))
d.ellipse([gx - 56, gy + 16, gx - 22, gy + 44], fill=(96, 160, 96))
tx = gx + 96
d.rounded_rectangle([tx - 9, gy - 62, tx + 9, gy + 34], radius=9, fill=RED, outline=INK, width=2)
d.ellipse([tx - 20, gy + 22, tx + 20, gy + 62], fill=RED, outline=INK, width=2)
for i in range(4):
    yy = gy - 48 + i * 22
    d.line([(tx + 14, yy), (tx + 26, yy)], fill=INK, width=3)

# ---------- middle row ----------
MY = 484
PW = (W - 2 * M - 18) // 2
PH = 252


def panel(x, y, tag, headline, caption, draw_art):
    d.rectangle([x, y, x + PW, y + PH], outline=INK, width=3)
    d.text((x + 14, y + 10), tag, font=font(FB, 19), fill=RED)
    text_block(d, (x + 14, y + 40), headline, font(FB, 29), INK, PW - 28)
    draw_art(x, y)
    text_block(d, (x + 14, y + 138), caption, font(F, 21), INK, PW - 28)


def art_ship(x, y):
    # small icon in the tag row, top-right of the panel
    bx, by = x + PW - 84, y + 22
    d.polygon([(bx, by), (bx + 62, by), (bx + 52, by + 10), (bx + 8, by + 10)], fill=INK)
    d.rectangle([bx + 20, by - 9, bx + 42, by], fill=INK)
    d.line([(bx - 4, by + 16), (bx + 68, by + 16)], fill=SEA, width=3)


def art_tanker(x, y):
    bx, by = x + PW - 88, y + 22
    d.polygon([(bx, by), (bx + 66, by), (bx + 56, by + 10), (bx + 8, by + 10)], fill=BLUE)
    d.rectangle([bx + 8, by - 7, bx + 58, by], fill=GOLD)
    d.line([(bx - 4, by + 16), (bx + 72, by + 16)], fill=SEA, width=3)


panel(M, MY, "WAR · MEDITERRANEAN",
      "UKRAINE SINKS RUSSIAN WARSHIP IN LIBYA",
      "Kyiv says seven naval drones struck the vessel in a Libyan port \u2014 the war spills far beyond Europe.",
      art_ship)
panel(M + PW + 18, MY, "MIDDLE EAST",
      "IRAN VOWS TO DEFY U.S. NAVAL BLOCKADE",
      "Tehran says it will use \u201call its tools\u201d against the blockade, as Trump warns of strikes without a nuclear deal.",
      art_tanker)

# ---------- bottom row ----------
BY = 754
BH = 168


def panel2(x, y, tag, headline, caption):
    d.rectangle([x, y, x + PW, y + BH], outline=INK, width=3)
    d.text((x + 14, y + 10), tag, font=font(FB, 19), fill=RED)
    text_block(d, (x + 14, y + 38), headline, font(FB, 27), INK, PW - 28)
    text_block(d, (x + 14, y + 100), caption, font(F, 20), INK, PW - 28)


panel2(M, BY, "TECH & BUSINESS", "NVIDIA BRINGS BACK JENSEN HUANG",
       "The CEO returns in a stunning reversal \u2014 and markets rally.")
panel2(M + PW + 18, BY, "SCIENCE · SPACE", "PROBE REACHES MERCURY AFTER 8 YEARS",
       "BepiColombo slips into orbit around Mercury, a first for Japan and Europe.")

# ---------- footer strip ----------
FY = 934
d.rectangle([M, FY, W - M, FY + 62], fill=LIGHT)
text_block(
    d, (M + 12, FY + 9),
    "ALSO MONDAY:  Belgium strike grounds flights  ·  South Korea reshuffles cabinet  ·  "
    "Kryvyi Rih strikes kill two  ·  49ers rout Vikings in Mexico City",
    font(FB, 18), INK, W - 2 * M - 24,
)

img.save("/home/hatch/workspace/makefun/news-entry/entry.png", optimize=True)
print("saved")
