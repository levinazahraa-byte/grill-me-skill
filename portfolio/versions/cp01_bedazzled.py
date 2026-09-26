# -*- coding: utf-8 -*-
"""VERSION 01 — BEDAZZLED.  Reference 1.

Y2K glam editorial: tonal pink, leopard and black lace borders, script against
high-contrast display caps, rhinestones, butterflies, pearls. Photos are arch,
oval and clipped silhouettes — never plain boxes.
"""
import os
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import deckkit as dk
import brief as b

ORN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ornaments")
PINK, ROSE, BLUSH, SHELL, NOIR = "FF2E93", "FF8FC5", "FFDDEE", "FFF4F9", "100A16"
MUTE, PAPER = "7A6478", "F1EBF2"
SCRIPT, DISPLAY, LABEL, BODY = "Great Vibes", "Italiana", "Oswald", "Poppins"

def orn(s, name, x, y, w=1920):
    p = os.path.join(ORN, name + ".png")
    if os.path.exists(p):
        s.pic(p, x, y, w)

def ground(s):
    s.bg(grad=(BLUSH, SHELL), angle=90)
    orn(s, "leopard_band", 0, 0)
    orn(s, "lace_band", 0, 104)
    orn(s, "leopard_band_b", 0, 990)
    orn(s, "lace_band_flip", 0, 946)

def gems(s, items):
    for name, x, y, w in items:
        orn(s, name, x, y, w)

def cut(s, kind, x, y, w, h, label="", rot=0, strong=False):
    return s.cut(kind, x, y, w, h, label, fill=PAPER, line=PINK if strong else ROSE,
                 lw=3 if strong else 2.2, rot=rot,
                 radius=0.3 if kind in ("arch", "rrect") else None,
                 label_color="A08FA8", size=9.5)

def eyebrow(s, x, y, text, color=PINK):
    return s.head(x, y, text, font=LABEL, size=11, color=color, tracking=6, caps=True,
                  gap=10)

def build(deck):
    # 01 · cover ------------------------------------------------------------
    s = deck.new(); ground(s)
    y = s.head(146, 180, b.KICKER[0], font=DISPLAY, size=22, color=PINK, tracking=9, gap=4)
    y = s.head(146, y, b.KICKER[1], font=DISPLAY, size=26, color=NOIR, tracking=3,
               max_w=680, one_line=True, gap=2)
    y = s.head(146, y, b.KICKER[2], font=DISPLAY, size=28, color=NOIR, tracking=4, gap=18)
    s.line(150, y, 280, PINK, 2)
    y = s.head(140, y + 16, "Zahra", font=SCRIPT, size=70, color=PINK, gap=2)
    y = s.head(150, y, b.LAST, font=DISPLAY, size=25, color=NOIR, tracking=7, gap=16)
    y = s.para(150, y, 540, b.TAGLINE, font=BODY, size=11.5, color=MUTE, italic=True,
               spacing=1.6, gap=22)
    for i, (lab, _) in enumerate(b.CONTACT):
        s.head(150 + i * 172, y, lab, font=LABEL, size=10, color=NOIR, tracking=4,
               caps=True)
    cut(s, "arch", 880, 196, 560, 730, "drop portrait", strong=True)
    cut(s, "oval", 1490, 286, 300, 300, "photo")
    cut(s, "snip", 1500, 646, 290, 250, "photo", rot=5)
    gems(s, [("butterfly_pink", 790, 246, 150), ("butterfly_rose", 1414, 200, 100),
             ("gem_heart", 1806, 580, 64), ("gem_marquise_rose", 826, 690, 54),
             ("gem_round", 1452, 894, 44), ("pearl_string", 600, 300, 250),
             ("pearl_string", 1450, 172, 230)])
    s.annot(880, 948, "PORTFOLIO / 2026", color=MUTE, size=9.5, font=LABEL, leader=54)

    # 02 · about ------------------------------------------------------------
    s = deck.new(); ground(s)
    y = eyebrow(s, 146, 184, "ABOUT")
    y = s.head(146, y, "HI, I'M", font=DISPLAY, size=30, color=NOIR, tracking=6, gap=4)
    y = s.head(140, y, "Zahra.", font=SCRIPT, size=68, color=PINK, gap=10)
    s.line(150, y, 400, PINK, 2)
    s.annot(150, y - 4, "CONTENT · CREATIVE · COMMUNICATION", color=PINK, size=9.5,
            font=LABEL, leader=60, width=620)
    s.para(150, y + 44, 620, b.ABOUT, font=BODY, size=12.5, color="2A1F30",
           spacing=1.8, after=18, max_h=300)
    cut(s, "arch", 880, 190, 500, 690, "drop portrait", strong=True)
    cut(s, "oval", 1440, 250, 330, 330, "photo")
    cut(s, "hex", 1450, 618, 310, 280, "photo")
    gems(s, [("butterfly_pink", 800, 596, 120), ("gem_heart", 1396, 176, 56),
             ("gem_round_rose", 842, 206, 46), ("pearl_string", 1410, 584, 230)])

    # 03 · from idea to publish ---------------------------------------------
    s = deck.new(); ground(s)
    y = eyebrow(s, 146, 184, "PROCESS")
    y = s.head(146, y, "FROM IDEA", font=DISPLAY, size=32, color=NOIR, tracking=6, gap=4)
    y = s.head(140, y, "to publish", font=SCRIPT, size=62, color=PINK, gap=26)
    for i, step in enumerate(b.FLOW):
        x = 146 + i * 236
        sy = y + (i % 2) * 44
        s.rrect(x, sy, 196, 92, fill="FFFFFF", line=PINK, lw=2, radius=0.16,
                shadow={"blur": 14, "dist": 4, "alpha": 12, "color": "C4568F"})
        s.text(x, sy, 196, 92, step, font=LABEL, size=13.5, color=NOIR, tracking=3,
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        s.head(x + 6, sy - 30, "0%d" % (i + 1), font=DISPLAY, size=12, color=ROSE,
               tracking=2)
        if i < 6:
            orn(s, "gem_round" if i % 2 == 0 else "gem_round_rose", x + 202, sy + 30, 30)
    ny = y + 158
    s.para(150, ny, 660, b.FLOW_NOTE, font=BODY, size=11.5, color="2A1F30",
           spacing=1.7, after=10, max_h=170)
    cut(s, "oval", 880, ny - 40, 210, 210, "photo")
    cut(s, "arch", 1134, ny - 60, 280, 240, "photo", strong=True)
    cut(s, "snip", 1456, ny - 36, 240, 210, "photo", rot=-4)

    gems(s, [("butterfly_rose", 1716, 212, 106), ("gem_heart", 1120, 206, 56),
             ("pearl_string", 1360, 186, 230)])

    # 04 · content, in different forms --------------------------------------
    s = deck.new(); ground(s)
    y = eyebrow(s, 146, 178, "WHAT I WORK WITH")
    y = s.head(146, y, "CONTENT, IN", font=DISPLAY, size=30, color=NOIR, tracking=5,
               gap=4)
    y = s.head(140, y, "different forms.", font=SCRIPT, size=52, color=PINK, gap=14)
    y = max(y, 430)
    shapes = ["oval", "hex", "arch", "snip"]
    for i, (group, items) in enumerate(b.FORMS):
        x = 146 + i * 420
        cut(s, shapes[i], x, y, 250, 166, "")
        gy = s.head(x, y + 186, group, font=LABEL, size=14, color=PINK, tracking=5, gap=4)
        s.line(x + 2, gy, 210, "E8CFDE", 1.4)
        for j, it in enumerate(items):
            s.text(x + 2, gy + 12 + j * 35, 340, 32, it, font=BODY, size=10.5,
                   color="2A1F30", anchor=MSO_ANCHOR.MIDDLE)
        orn(s, ["gem_round", "gem_marquise", "gem_heart", "gem_round_rose"][i],
            x + 216, y - 22, 38)
    gems(s, [("butterfly_pink", 1732, 196, 108), ("pearl_string", 1400, 172, 230)])

    # 05 · sawala space -----------------------------------------------------
    s = deck.new(); ground(s)
    y = eyebrow(s, 146, 182, "SELECTED PROJECT")
    y = s.head(146, y, b.SAWALA_TITLE, font=DISPLAY, size=38, color=NOIR, tracking=4,
               max_w=720, one_line=True, gap=12)
    y = s.head(150, y, b.SAWALA_SUB, font=LABEL, size=10.5, color=PINK, tracking=4,
               max_w=600, one_line=True, gap=16)
    s.line(150, y, 340, PINK, 2)
    y = s.para(150, y + 24, 580, b.SAWALA_BODY, font=BODY, size=12.5, color="2A1F30",
               spacing=1.8, max_h=280, gap=30)
    x = 150
    for i, t in enumerate(b.SAWALA_TAGS):
        if i == 3:
            x, y = 150, y + 58
        x += s.pill(x, y, t, size=10, pad=16, h=46, fill="FFFFFF", color=NOIR,
                    line=ROSE, font=LABEL, tracking=3) + 12
    cut(s, "arch", 800, 196, 450, 620, b.SAWALA_SHOTS[0], strong=True)
    cut(s, "oval", 1300, 206, 260, 260, b.SAWALA_SHOTS[1])
    cut(s, "snip", 1594, 244, 210, 190, b.SAWALA_SHOTS[2], rot=4)
    cut(s, "hex", 1292, 510, 250, 230, b.SAWALA_SHOTS[3])
    cut(s, "rrect", 1584, 496, 220, 250, b.SAWALA_SHOTS[4], rot=-4)
    s.annot(800, 846, "CONCEPT → CONTENT → EVENT", color=MUTE, size=9.5, font=LABEL,
            leader=54)
    gems(s, [("butterfly_rose", 1246, 166, 100), ("gem_heart", 760, 686, 56),
             ("pearl_string", 1290, 782, 240)])

    # 06 · content in practice ----------------------------------------------
    s = deck.new(); ground(s)
    y = eyebrow(s, 146, 176, "IN PRACTICE")
    y = s.head(146, y, b.PRACTICE_TITLE, font=DISPLAY, size=36, color=NOIR, tracking=4,
               max_w=1500, gap=34)
    kinds = ["arch", "oval", "snip", "hex", "rrect", "oct"]
    for i, (lab, sub) in enumerate(b.PRACTICE):
        x = 146 + (i % 3) * 546
        cy = y + (i // 3) * 276
        cut(s, kinds[i], x, cy, 240, 196, "", rot=(-3, 0, 3)[i % 3])
        s.head(x + 262, cy - 2, "0%d" % (i + 1), font=DISPLAY, size=12, color=ROSE,
               tracking=2)
        ly = s.head(x + 262, cy + 28, lab, font=LABEL, size=12, color=PINK, tracking=4,
                    max_w=250, gap=8)
        s.para(x + 264, ly, 250, sub, font=BODY, size=10.5, color="2A1F30", spacing=1.5)
    gems(s, [("gem_round", 1800, y + 10, 40), ("butterfly_pink", 1740, y + 300, 100)])

    # 07 · stretch for stray ------------------------------------------------
    s = deck.new(); ground(s)
    cut(s, "arch", 146, 210, 440, 650, b.STRAY_SHOTS[0], strong=True)
    y = eyebrow(s, 660, 192, b.STRAY_SUB)
    y = s.head(656, y, b.STRAY_TITLE, font=DISPLAY, size=40, color=NOIR, tracking=4,
               max_w=960, one_line=True, gap=18)
    s.line(660, y, 300, PINK, 2)
    y = s.para(660, y + 24, 660, b.STRAY_BODY, font=BODY, size=13, color="2A1F30",
               spacing=1.6, gap=28)
    y = s.head(660, y, "MY CONTRIBUTION", font=LABEL, size=11, color=PINK, tracking=5,
               gap=14)
    for i, it in enumerate(b.STRAY_LIST):
        ry = y + i * 52
        orn(s, "gem_round" if i % 2 == 0 else "gem_round_rose", 662, ry + 10, 26)
        s.text(702, ry, 520, 44, it, font=BODY, size=12, color="2A1F30",
               anchor=MSO_ANCHOR.MIDDLE)
    cut(s, "oval", 1290, 470, 240, 240, b.STRAY_SHOTS[1])
    cut(s, "snip", 1562, 486, 230, 210, b.STRAY_SHOTS[2], rot=5)
    cut(s, "rrect", 1300, 754, 490, 150, b.STRAY_SHOTS[3])
    gems(s, [("butterfly_pink", 1214, 206, 116), ("gem_heart", 1770, 300, 58),
             ("pearl_string", 1290, 400, 240)])

    # 08 · behind the content -----------------------------------------------
    s = deck.new(); ground(s)
    y = eyebrow(s, 146, 178, "PROCESS")
    y = s.head(146, y, b.BEHIND_TITLE, font=DISPLAY, size=34, color=NOIR, tracking=4,
               max_w=1080, one_line=True, gap=24)
    x = 146
    for step in b.BEHIND_STEPS:
        x += s.pill(x, y, step, size=10, pad=14, h=40, fill=PINK, color="FFFFFF",
                    font=LABEL, tracking=3) + 10
    y += 66
    kinds = ["snip", "oval", "rrect", "hex", "arch", "snip1", "oct", "rrect"]
    for i, (cap, step) in enumerate(b.BEHIND_SHOTS):
        cx = 146 + (i % 4) * 424
        cy = y + (i // 4) * 258
        cut(s, kinds[i], cx, cy, 376, 186, cap, rot=(-3, 2, -2, 3)[i % 4])
        s.head(cx + 2, cy + 196, step, font=LABEL, size=9, color=PINK, tracking=4)
    gems(s, [("gem_marquise", 1812, y - 40, 42), ("butterfly_rose", 1776, 902, 92)])

    # 09 · tools ------------------------------------------------------------
    s = deck.new(); ground(s)
    y = eyebrow(s, 146, 184, "TOOLS + WORKFLOW")
    y = s.head(146, y, "THE TOOLS", font=DISPLAY, size=32, color=NOIR, tracking=6,
               gap=4)
    y = s.head(140, y, "i work with", font=SCRIPT, size=58, color=PINK, gap=24)
    for i, (group, items) in enumerate(b.TOOLS):
        x = 146 + i * 468
        gy = s.head(x, y, group, font=LABEL, size=14, color=PINK, tracking=6, gap=8)
        s.line(x + 2, gy, 290, "E8CFDE", 1.4)
        for j, it in enumerate(items):
            iy = gy + 22 + j * 68
            s.rrect(x, iy, 400, 56, fill="FFFFFF", line=ROSE, lw=1.6, radius=0.2)
            orn(s, "gem_round" if j % 2 == 0 else "gem_round_rose", x + 16, iy + 15, 26)
            s.text(x + 58, iy, 320, 56, it, font=BODY, size=12, color="2A1F30",
                   anchor=MSO_ANCHOR.MIDDLE)
    s.para(150, 872, 1180, b.TOOLS_NOTE, font=BODY, size=10.5, color=MUTE, italic=True,
           spacing=1.5)
    cut(s, "arch", 1566, y + 20, 230, 320, "photo", strong=True)
    gems(s, [("butterfly_pink", 1490, 200, 116), ("pearl_string", 1520, 836, 230)])

    # 10 · closing ----------------------------------------------------------
    s = deck.new(); ground(s)
    orn(s, "gem_heart_paved", 872, 186, 180)
    y = s.head(0, 396, b.END_TITLE[0], font=DISPLAY, size=32, color=NOIR, tracking=6,
               align=PP_ALIGN.CENTER, max_w=1920, gap=6)
    y = s.head(0, y, "worth sharing.", font=SCRIPT, size=60, color=PINK,
               align=PP_ALIGN.CENTER, max_w=1920, gap=16)
    s.line(870, y, 180, PINK, 2)
    y = s.head(0, y + 24, b.NAME, font=DISPLAY, size=22, color=NOIR, tracking=8,
               align=PP_ALIGN.CENTER, max_w=1920, gap=6)
    y = s.head(0, y, b.END_ROLE + "  ·  " + b.END_SUB, font=LABEL, size=10.5,
               color=PINK, tracking=4, align=PP_ALIGN.CENTER, max_w=1920, caps=True,
               gap=24)
    for i, (lab, val) in enumerate(b.CONTACT):
        x = 420 + i * 376
        s.rrect(x, y, 316, 88, fill="FFFFFF", line=ROSE, lw=1.6, radius=0.18,
                shadow={"blur": 14, "dist": 4, "alpha": 10, "color": "C4568F"})
        s.text(x, y + 18, 316, 28, lab, font=LABEL, size=10.5, color=PINK,
               align=PP_ALIGN.CENTER, tracking=4, caps=True)
        s.text(x, y + 48, 316, 28, val, font=BODY, size=10, color=MUTE,
               align=PP_ALIGN.CENTER)
    gems(s, [("butterfly_pink", 232, 470, 118), ("butterfly_rose", 1576, 470, 98),
             ("gem_marquise", 1690, 226, 50), ("gem_round_rose", 224, 682, 42),
             ("pearl_string", 232, 246, 240), ("pearl_string", 1440, 692, 240)])
    return deck
