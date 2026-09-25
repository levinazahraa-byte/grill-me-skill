# -*- coding: utf-8 -*-
"""PORTFOLIO 01 — BEDAZZLED.  Reference 1.

Maximalist Y2K glam: tonal hot pink, black lace and leopard borders, script
lettering, rhinestones. Symmetrical, centred, dense — a fan-poster turned
portfolio. Ornaments are separate PNG layers; everything else is a live shape.
"""
import os
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import deckkit as dk
import content as c

ORN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ornaments")
PINK, ROSE, BLUSH, SHELL, NOIR = "FF2E93", "FF8FC5", "FFDDEE", "FFF4F9", "100A16"
SCRIPT, DISPLAY, LABEL, BODY = "Great Vibes", "Italiana", "Oswald", "Poppins"

def orn(s, name, x, y, w=1920):
    s.pic(os.path.join(ORN, name + ".png"), x, y, w)

def chrome(s, top=True, bottom=True):
    s.bg(grad=(BLUSH, SHELL), angle=90)
    if top:
        orn(s, "leopard_band", 0, 0, 1920)
        orn(s, "lace_band", 0, 104, 1920)
    if bottom:
        orn(s, "leopard_band_b", 0, 968)
        orn(s, "lace_band_flip", 0, 924, 1920)

def heading(s, script_text, caps_text, y=176, script_size=56, caps_size=22, center=True):
    a = PP_ALIGN.CENTER if center else PP_ALIGN.LEFT
    x, w = (0, 1920) if center else (140, 1000)
    s.text(x, y, w, caps_size * 2.4, caps_text, font=DISPLAY, size=caps_size, color=NOIR,
           align=a, tracking=20, caps=True)
    s.text(x, y + caps_size * 2.4, w, script_size * 1.7, script_text, font=SCRIPT,
           size=script_size, color=PINK, align=a)

def gems(s, items):
    for name, x, y, w in items:
        orn(s, name, x, y, w)

def frame(s, x, y, w, h, label="drop photo"):
    s.rrect(x - 12, y - 12, w + 24, h + 24, fill="FFFFFF", line=PINK, lw=2, radius=0.04,
            shadow={"blur": 26, "dist": 8, "alpha": 20, "color": "C4568F"})
    return s.photo(x, y, w, h, label=label, fill="F3EEF6", line=ROSE, radius=0.03,
                   label_color="B99BB3")

def build(deck):
    # 1 · cover -------------------------------------------------------------
    s = deck.new(); chrome(s)
    s.text(0, 168, 1920, 44, c.KICKER, font=DISPLAY, size=24, color=NOIR,
           align=PP_ALIGN.CENTER, tracking=24, caps=True)
    s.line(820, 226, 280, PINK, 2)
    s.text(0, 240, 1920, 40, c.DISCIPLINES, font=LABEL, size=13, color=PINK,
           align=PP_ALIGN.CENTER, tracking=8, caps=True)
    frame(s, 680, 296, 560, 452, "drop portrait")
    s.text(0, 604, 1920, 200, c.NAME_TITLE.split()[0], font=SCRIPT, size=62, color=PINK,
           align=PP_ALIGN.CENTER)
    s.text(0, 812, 1920, 70, c.NAME.split()[1], font=DISPLAY, size=34, color=NOIR,
           align=PP_ALIGN.CENTER, tracking=22)
    s.text(0, 870, 1920, 34, "WhatsApp · Email · LinkedIn", font=LABEL, size=10,
           color="8A7386", align=PP_ALIGN.CENTER, tracking=7, caps=True)
    gems(s, [("butterfly_pink", 470, 330, 150), ("butterfly_rose", 1330, 380, 110),
             ("gem_heart", 1300, 250, 66), ("gem_marquise_rose", 560, 560, 52),
             ("gem_round", 1360, 620, 48), ("gem_round_rose", 600, 790, 40),
             ("pearl_string", 250, 520, 300), ("pearl_string", 1400, 800, 300)])

    # 2 · about -------------------------------------------------------------
    s = deck.new(); chrome(s)
    s.text(140, 186, 900, 60, "ABOUT", font=DISPLAY, size=24, color=NOIR, tracking=22)
    s.text(132, 214, 900, 150, "Hi, I'm Zahra.", font=SCRIPT, size=62, color=PINK)
    s.line(140, 400, 460, PINK, 2)
    s.text(140, 412, 830, 460, c.ABOUT, font=BODY, size=11.5, color="2A1F30",
           spacing=1.75, after=16)
    frame(s, 1120, 230, 560, 600, "drop portrait")
    gems(s, [("butterfly_pink", 1040, 280, 120), ("gem_heart", 1700, 250, 54),
             ("gem_round", 1080, 760, 42), ("pearl_string", 1290, 170, 300)])

    # 3 · what i do ---------------------------------------------------------
    s = deck.new(); chrome(s)
    heading(s, "what i do", "SERVICES", y=170, script_size=58)
    for i, (title, sub) in enumerate(c.DO):
        x = 140 + (i % 2) * 830
        y = 444 + (i // 2) * 226
        s.rrect(x, y, 790, 200, fill="FFFFFF", line=ROSE, lw=1.5, radius=0.06,
                shadow={"blur": 20, "dist": 6, "alpha": 14, "color": "C4568F"})
        orn(s, "gem_round" if i % 2 == 0 else "gem_marquise_rose", x + 40, y + 56, 46)
        s.text(x + 110, y + 40, 650, 70, title, font=LABEL, size=16, color=NOIR,
               tracking=5, caps=True, spacing=1.25)
        s.text(x + 112, y + 116, 640, 70, sub, font=BODY, size=11.5, color="6B5A68",
               spacing=1.45)
    gems(s, [("butterfly_rose", 1700, 330, 92), ("gem_heart", 160, 330, 46)])

    # 4 · experience --------------------------------------------------------
    s = deck.new(); chrome(s)
    heading(s, "where i've been", "EXPERIENCE", y=168, script_size=54)
    for i, (org, role) in enumerate(c.EXP):
        y = 446 + i * 92
        orn(s, "gem_round" if i % 2 == 0 else "gem_round_rose", 190, y + 18, 38)
        s.text(258, y + 6, 900, 46, org, font=LABEL, size=19, color=NOIR, tracking=6,
               caps=True)
        s.text(260, y + 50, 900, 36, role, font=BODY, size=12, color="6B5A68")
        s.text(1560, y + 10, 170, 40, "0%d" % (i + 1), font=DISPLAY, size=20,
               color="D9B6CC", align=PP_ALIGN.RIGHT, tracking=4)
        if i < 4:
            s.line(190, y + 94, 1540, "EBD6E4", 1)
    gems(s, [("butterfly_pink", 1660, 360, 100), ("pearl_string", 240, 330, 280)])

    # 5 · sawala space ------------------------------------------------------
    s = deck.new(); chrome(s)
    frame(s, 150, 250, 640, 580, "drop photo")
    s.text(880, 210, 900, 50, "FEATURED PROJECT", font=DISPLAY, size=20, color=NOIR,
           tracking=20)
    s.text(872, 236, 900, 150, "Sawala Space", font=SCRIPT, size=60, color=PINK)
    s.text(880, 410, 820, 40, c.SAWALA_SUB, font=LABEL, size=14, color=NOIR, tracking=7,
           caps=True)
    s.line(880, 462, 460, PINK, 2)
    s.text(880, 494, 800, 220, c.SAWALA_BODY, font=BODY, size=12, color="2A1F30",
           spacing=1.7)
    s.text(880, 720, 400, 34, "MY ROLE", font=LABEL, size=12, color=PINK, tracking=8)
    x, y = 880, 762
    for i, r in enumerate(c.SAWALA_ROLE):
        if i == 3:
            x, y = 880, 822
        x += s.pill(x, y, r, size=11, pad=26, h=46, fill="FFFFFF", color=NOIR,
                    line=ROSE, font=LABEL, tracking=5) + 14
    gems(s, [("gem_heart", 806, 244, 56), ("butterfly_rose", 1700, 760, 90)])

    # 6 · selected works ----------------------------------------------------
    s = deck.new(); chrome(s)
    heading(s, "selected works", "PORTFOLIO", y=160, script_size=50)
    s.text(0, 382, 1920, 40, " · ".join(c.WORKS_TAGS), font=LABEL, size=12, color=PINK,
           align=PP_ALIGN.CENTER, tracking=8, caps=True)
    for i, cap in enumerate(c.WORKS_CAPS):
        x = 148 + (i % 4) * 412
        y = 452 + (i // 4) * 232
        frame(s, x, y, 368, 166, cap)
    gems(s, [("gem_round", 1790, 400, 40), ("gem_marquise_rose", 92, 640, 44)])

    # 7 · stretch for stray -------------------------------------------------
    s = deck.new(); chrome(s)
    frame(s, 150, 250, 520, 580, "drop poster")
    s.text(760, 208, 900, 44, c.STRAY_SUB, font=LABEL, size=13, color=PINK, tracking=8,
           caps=True)
    s.text(760, 232, 1000, 120, "Stretch", font=SCRIPT, size=64, color=PINK)
    s.text(766, 406, 1000, 70, "FOR STRAY", font=DISPLAY, size=44, color=NOIR, tracking=18)
    s.line(768, 494, 420, PINK, 2)
    s.text(768, 536, 700, 90, c.STRAY_BODY, font=BODY, size=12.5, color="2A1F30",
           spacing=1.6)
    s.text(768, 656, 500, 34, "MY CONTRIBUTION", font=LABEL, size=12, color=PINK,
           tracking=8)
    for i, it in enumerate(c.STRAY_LIST):
        y = 700 + i * 44
        orn(s, "gem_round" if i % 2 == 0 else "gem_round_rose", 772, y + 10, 26)
        s.text(818, y, 560, 42, it, font=BODY, size=12.5, color="2A1F30",
               anchor=MSO_ANCHOR.MIDDLE)
    frame(s, 1420, 624, 330, 232, "documentation")
    gems(s, [("butterfly_pink", 640, 236, 104), ("gem_heart", 1740, 250, 54)])

    # 8 · beyond ------------------------------------------------------------
    s = deck.new(); chrome(s)
    heading(s, "beyond creative work", "ORGANISATIONS", y=160, script_size=48)
    s.text(0, 400, 1920, 60, c.BEYOND_BODY, font=BODY, size=13, color="6B5A68",
           align=PP_ALIGN.CENTER, spacing=1.5)
    for i, (title, sub) in enumerate(c.BEYOND):
        x = 150 + i * 548
        s.rrect(x, 480, 500, 348, fill="FFFFFF", line=ROSE, lw=1.5, radius=0.07,
                shadow={"blur": 22, "dist": 7, "alpha": 16, "color": "C4568F"})
        orn(s, ["gem_heart", "gem_marquise", "gem_round"][i], x + 46, 522, 48)
        s.text(x + 46, 598, 410, 140, title, font=LABEL, size=14, color=NOIR, tracking=4,
               caps=True, spacing=1.3)
        s.line(x + 46, 736, 150, PINK, 2)
        s.text(x + 46, 760, 410, 90, sub, font=BODY, size=10.5, color="6B5A68",
               spacing=1.45)

    # 9 · skills ------------------------------------------------------------
    s = deck.new(); chrome(s)
    heading(s, "skills & tools", "CAPABILITIES", y=160, script_size=50)
    for i, (title, items) in enumerate(c.SKILLS):
        x = 160 + i * 860
        s.text(x, 400, 500, 40, title, font=LABEL, size=17, color=PINK, tracking=8,
               caps=True)
        s.line(x, 446, 300, PINK, 2)
        for j, it in enumerate(items):
            y = 486 + j * 62
            orn(s, "gem_round" if j % 2 == 0 else "gem_marquise_rose", x, y + 8, 30)
            s.text(x + 52, y, 500, 42, it, font=BODY, size=13, color="2A1F30",
                   anchor=MSO_ANCHOR.MIDDLE)
    s.text(160, 754, 400, 40, "TOOLS", font=LABEL, size=15, color=PINK, tracking=8)
    s.line(160, 800, 1600, "EBD6E4", 1)
    x, y = 160, 824
    for i, t in enumerate(c.TOOLS):
        if i == 4:
            x, y = 160, 876
        x += s.pill(x, y, t, size=10.5, pad=16, h=42, fill="FFFFFF", color=NOIR,
                    line=ROSE, font=BODY, tracking=0) + 12
    gems(s, [("butterfly_rose", 1720, 760, 94)])

    # 10 · contact ----------------------------------------------------------
    s = deck.new(); chrome(s)
    orn(s, "gem_heart_paved", 850, 158, 220)
    s.text(0, 408, 1920, 60, "LET'S WORK", font=DISPLAY, size=32, color=NOIR,
           align=PP_ALIGN.CENTER, tracking=22)
    s.text(0, 452, 1920, 190, "together", font=SCRIPT, size=66, color=PINK,
           align=PP_ALIGN.CENTER)
    s.line(860, 652, 200, PINK, 2)
    s.text(460, 680, 1000, 100, c.END_BODY, font=BODY, size=12.5, color="2A1F30",
           align=PP_ALIGN.CENTER, spacing=1.6)
    for i, (lab, val) in enumerate(c.CONTACT):
        x = 420 + i * 380
        s.rrect(x, 806, 320, 92, fill="FFFFFF", line=ROSE, lw=1.5, radius=0.18,
                shadow={"blur": 18, "dist": 6, "alpha": 14, "color": "C4568F"})
        s.text(x, 826, 320, 30, lab, font=LABEL, size=12, color=PINK,
               align=PP_ALIGN.CENTER, tracking=6, caps=True)
        s.text(x, 856, 320, 30, val, font=BODY, size=11, color="6B5A68",
               align=PP_ALIGN.CENTER)
    gems(s, [("butterfly_pink", 250, 380, 120), ("butterfly_rose", 1560, 420, 96),
             ("gem_marquise", 1700, 250, 50), ("gem_round_rose", 210, 690, 40),
             ("pearl_string", 210, 690, 250), ("pearl_string", 1460, 690, 250)])
    return deck
