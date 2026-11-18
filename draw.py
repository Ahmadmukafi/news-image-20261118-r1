#!/usr/bin/env python3
"""Render the 18 November 2026 world-news front page, 1024x1024 PNG.

Drawn entirely with PIL primitives and real text (no downloaded images,
no image model) so every headline stays perfectly legible.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
NAVY = (20, 38, 76)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
GREY = (90, 90, 90)
SKY = (168, 205, 232)
SEA = (46, 111, 160)
LIGHT = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top red rule + masthead ----
    d.rectangle([0, 0, W, 8], fill=RED)
    d.rectangle([0, 8, W, 108], fill=NAVY)
    title_f = font(SERIF_B, 44)
    d.text((36, 34), "THE WORLD IN ONE DAY", font=title_f, fill=LIGHT)
    date_f = font(SANS_B, 24)
    d.text((W - 36 - d.textlength("WEDNESDAY", font=date_f), 24),
           "WEDNESDAY", font=date_f, fill=GOLD)
    date2_f = font(SANS_B, 20)
    d.text((W - 36 - d.textlength("18 NOVEMBER 2026", font=date2_f), 56),
           "18 NOVEMBER 2026", font=date2_f, fill=LIGHT)
    d.rectangle([0, 108, W, 112], fill=GOLD)

    # ---- lead story: Trump in Manila ----
    kick_f = font(SANS_B, 22)
    d.text((36, 130), "MANILA  ·  THE QUAD SUMMIT", font=kick_f, fill=RED)
    head_f = font(SERIF_B, 60)
    d.text((36, 158), "TRUMP LANDS", font=head_f, fill=INK)
    d.text((36, 228), "IN MANILA", font=head_f, fill=INK)
    sub_f = font(SANS, 25)
    sub = wrap(d, "Quad talks open as the ASEAN summit wraps — ahead of a historic meeting with China\u2019s Xi.", sub_f, 540)
    text_block(d, 36, 322, sub, sub_f, INK, 33)
    cap_f = font(SERIF, 20)
    cap = wrap(d, "The US president opens his Asia tour; Beijing is next.", cap_f, 540)
    text_block(d, 36, 428, cap, cap_f, GREY, 26)

    # lead illustration: Manila skyline + Quad flags + plane (right panel)
    px0, py0, px1, py1 = 612, 128, 988, 452
    d.rectangle([px0, py0, px1, py1], fill=SKY)
    d.ellipse([px1 - 90, py0 + 18, px1 - 26, py0 + 82], fill=(255, 214, 90))
    # skyline
    base = py1
    towers = [(px0 + 8, 120), (px0 + 62, 170), (px0 + 118, 95),
              (px0 + 176, 150), (px0 + 232, 110), (px0 + 290, 180)]
    for tx, th in towers:
        d.rectangle([tx, base - th, tx + 48, base], fill=NAVY)
        for wy in range(base - th + 12, base - 10, 22):
            for wx in range(tx + 8, tx + 42, 14):
                d.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 220, 120))
    # plane: thin fuselage, tail fin, swept wing
    d.polygon([(px0 + 60, py0 + 40), (px0 + 168, py0 + 40),
               (px0 + 186, py0 + 45), (px0 + 168, py0 + 50),
               (px0 + 60, py0 + 50)], fill=INK)
    d.polygon([(px0 + 60, py0 + 40), (px0 + 74, py0 + 18),
               (px0 + 84, py0 + 40)], fill=INK)
    d.polygon([(px0 + 104, py0 + 50), (px0 + 122, py0 + 68),
               (px0 + 132, py0 + 50)], fill=INK)
    # Quad flags row
    flag_y = py1 - 34
    flags = [("USA", (178, 34, 34)), ("IND", (255, 153, 51)),
             ("JPN", (220, 220, 220)), ("AUS", (0, 47, 108))]
    fx = px0 + 14
    lab_f = font(SANS_B, 15)
    for name, col in flags:
        d.rectangle([fx, flag_y, fx + 74, flag_y + 22], fill=col, outline=INK)
        d.text((fx + 20, flag_y + 3), name, font=lab_f, fill=LIGHT if col != (220, 220, 220) else INK)
        fx += 88
    d.text((px0 + 6, py1 + 8), "Four leaders, one table — in Manila.",
           font=font(SANS, 16), fill=GREY)

    # ---- divider ----
    d.line([36, 486, W - 36, 486], fill=INK, width=2)

    # ---- middle: two stories ----
    # left: Crimea bridge
    x0, x1 = 36, 488
    d.text((x0, 504), "UKRAINE  ·  WAR", font=kick_f, fill=RED)
    h2_f = font(SERIF_B, 38)
    d.text((x0, 536), "CRIMEA BRIDGE", font=h2_f, fill=INK)
    d.text((x0, 580), "HIT AGAIN", font=h2_f, fill=INK)
    body_f = font(SANS, 19)
    b = wrap(d, "Kyiv\u2019s drones strike the bridge to Crimea for a second day in a 1,336-drone barrage — as Russia pounds bridges in Kyiv.",
             body_f, x1 - x0)
    text_block(d, x0, 626, b, body_f, INK, 25)
    # bridge drawing
    # water
    d.rectangle([x0, 752, x1, 830], fill=SEA)
    # bridge deck + arc + pillars
    d.rectangle([x0, 742, x1, 752], fill=INK)
    d.arc([x0 + 60, 706, x1 - 60, 806], start=180, end=360, fill=INK, width=6)
    for px in (x0 + 90, x0 + 220, x0 + 350):
        d.rectangle([px, 752, px + 10, 762], fill=INK)
    # explosion burst
    cx, cy = x0 + 330, 726
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 12, 30
        a = math.radians(ang)
        d.line([cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                cx + r2 * math.cos(a), cy + r2 * math.sin(a)],
               fill=(255, 140, 0), width=5)
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(255, 200, 40))
    d.text((x0, 838), "A bridge burns: the Kerch crossing, struck twice.",
           font=font(SANS, 16), fill=GREY)

    # right: Gulf escalation
    x0, x1 = 536, 988
    d.text((x0, 504), "THE GULF  ·  ESCALATION", font=kick_f, fill=RED)
    d.text((x0, 536), "IRAN HITS US", font=h2_f, fill=INK)
    d.text((x0, 580), "RADAR IN BAHRAIN", font=h2_f, fill=INK)
    b = wrap(d, "Tehran\u2019s drones strike a US radar site; Washington hits an IRGC missile base on Qeshm. A tanker is attacked in the Strait of Hormuz.",
             body_f, x1 - x0)
    text_block(d, x0, 626, b, body_f, INK, 25)
    # radar + sea drawing
    d.rectangle([x0, 752, x1, 830], fill=SEA)
    # tanker
    d.rectangle([x0 + 30, 762, x0 + 200, 792], fill=(60, 60, 60))
    d.rectangle([x0 + 160, 742, x0 + 186, 762], fill=(60, 60, 60))
    d.rectangle([x0 + 40, 792, x0 + 190, 798], fill=RED)
    # radar dish: bowl opening upward + feed dot + pole
    rx, ry = x0 + 340, 800
    d.arc([rx - 44, ry - 88, rx + 44, ry - 8], start=0, end=180,
          fill=LIGHT, width=5)
    d.ellipse([rx - 5, ry - 58, rx + 5, ry - 48], fill=LIGHT)
    d.rectangle([rx - 4, ry - 8, rx + 4, ry + 30], fill=INK)
    # drones as dots with trails, flying just above the sea
    for dx, dy in ((x0 + 250, 716), (x0 + 290, 700), (x0 + 330, 716)):
        d.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=INK)
        d.line([dx - 22, dy + 8, dx - 6, dy + 2], fill=INK, width=2)
    d.text((x0, 838), "Drones over the Gulf: the US–Iran exchange widens.",
           font=font(SANS, 16), fill=GREY)

    # ---- divider + also-today strip ----
    d.line([36, 872, W - 36, 872], fill=INK, width=2)
    d.text((36, 888), "ALSO TODAY", font=font(SANS_B, 22), fill=NAVY)
    items = [
        ("TRADE", "Canada, China extend deals before APEC."),
        ("WEST BANK", "Britain sanctions Israeli settlement firms."),
        ("STORM", "Cyclone Akvan nears the Bay of Bengal."),
        ("CRICKET", "Dhoni retires from the IPL; becomes CSK mentor."),
    ]
    lab_f = font(SANS_B, 17)
    it_f = font(SANS, 17)
    col_w = 226
    for i, (lab, txt) in enumerate(items):
        cx0 = 36 + i * (col_w + 12)
        d.text((cx0, 924), lab, font=lab_f, fill=RED)
        lines = wrap(d, txt, it_f, col_w)
        text_block(d, cx0, 950, lines, it_f, INK, 22)

    # ---- footer ----
    d.rectangle([0, 1004, W, H], fill=NAVY)
    foot_f = font(SANS, 15)
    msg = "THE WORLD IN ONE DAY  ·  18 NOVEMBER 2026"
    d.text(((W - d.textlength(msg, font=foot_f)) / 2, 1005), msg,
           font=foot_f, fill=LIGHT)

    img.save("entry.png")
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
