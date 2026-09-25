# -*- coding: utf-8 -*-
"""PORTFOLIO 05 — CHAT.  Reference 5.

A blown-up messaging thread: acid yellow-to-lime gradient, thick black
outlines, speech bubbles, tilted photo cards on starbursts, an input bar at the
foot of every slide. Loud, playful, high contrast.
"""
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import deckkit as dk
import content as c

YEL, LIME, SKY, WHITE, BLACK = "FFE83D", "9BE22B", "CFEFFF", "FFFFFF", "000000"
RED, BLUE, GREEN, PINK = "FF3B30", "2B6CFF", "34C759", "FF7BC4"
HEAD, MONO, BODY = "Anton", "Space Mono", "Poppins"

def frame(s, title, sub=None):
    s.bg(grad=(YEL, LIME), angle=90)
    s.rect(0, 0, 1920, 128, grad=(YEL, "F5D800"), angle=90)
    s.rect(0, 126, 1920, 5, fill=BLACK)
    s.oval(46, 30, 68, 68, fill=WHITE, line=BLACK, lw=3)
    s.oval(62, 46, 36, 36, fill=PINK)
    s.text(140, 14, 1100, 62, title, font=HEAD, size=34, color=BLACK,
           anchor=MSO_ANCHOR.MIDDLE)
    if sub:
        s.text(142, 84, 900, 34, sub, font=MONO, size=11, color="3A3A3A")
    for i in range(3):
        s.oval(1848, 46 + i * 18, 10, 10, fill=BLACK)
    s.rect(0, 946, 1920, 5, fill=BLACK)
    s.rect(0, 951, 1920, 129, grad=("F5D800", YEL), angle=90)
    s.rrect(120, 984, 1560, 66, fill=WHITE, line=BLACK, lw=3, radius=0.5)
    s.text(160, 984, 1200, 66, "type a message...", font=BODY, size=13, color="8A8A8A",
           anchor=MSO_ANCHOR.MIDDLE)
    s.oval(40, 984, 66, 66, fill=GREEN, line=BLACK, lw=3)
    s.oval(1714, 984, 66, 66, fill=GREEN, line=BLACK, lw=3)
    s.shape(MSO_SHAPE.ISOSCELES_TRIANGLE, 1736, 1002, 26, 30, fill=WHITE, line=BLACK,
            lw=2, rot=90)
    s.rect(0, 131, 1920, 815, fill=SKY)

def msg(s, x, y, w, h, text, side="l", fill=WHITE, size=15, font=BODY, color=BLACK,
        spacing=1.5):
    s.bubble(x, y, w, h, text, fill=fill, line=BLACK, lw=3, color=color, font=font,
             size=size, tail="bl" if side == "l" else "br", radius=0.3, spacing=spacing)

def avatar(s, x, y, size=56, fill=PINK):
    s.oval(x, y, size, size, fill=WHITE, line=BLACK, lw=3)
    s.oval(x + size * 0.22, y + size * 0.22, size * 0.56, size * 0.56, fill=fill)

def photo_card(s, x, y, w, h, label, rot=-6, burst=True, burst_col=LIME):
    if burst:
        s.star(x - 60, y - 50, max(w, h) * 0.55, fill=burst_col, line=BLACK, lw=3,
               points=16, rot=12)
        s.star(x + w - 90, y + h - 80, max(w, h) * 0.42, fill=YEL, line=BLACK, lw=3,
               points=16, rot=-8)
    s.photo(x, y, w, h, label, fill=WHITE, line=BLACK, radius=0.05, rot=rot, dash=False,
            label_color="7A7A7A", size=11)

def stamp(s, x, y, text, fill=RED, w=None, size=13):
    return s.pill(x, y, text, size=size, pad=24, h=48, fill=fill, color=WHITE,
                  line=BLACK, font=MONO, tracking=2, radius=0.4, width=w)

def build(deck):
    # 1 · cover
    s = deck.new(); frame(s, "zahra levina", "online now")
    msg(s, 120, 200, 700, 130, "hey!! welcome 2 my portfolio", size=18)
    msg(s, 120, 360, 860, 150, c.DISCIPLINES, size=16)
    s.rect(1010, 200, 820, 640, fill=WHITE, line=BLACK, lw=4)
    photo_card(s, 1080, 250, 480, 520, "drop portrait", rot=-5)
    stamp(s, 120, 556, "2026 PORTFOLIO", fill=BLACK, size=15, w=350)
    s.text(118, 624, 1000, 300, "ZAHRA\nLEVINA", font=HEAD, size=70, color=BLACK,
           spacing=0.94)
    avatar(s, 1730, 236, 72, fill=YEL)
    s.star(940, 690, 130, fill=RED, line=BLACK, lw=3, points=16, rot=20)
    s.text(940, 690, 130, 130, "NEW", font=HEAD, size=22, color=WHITE,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # 2 · about
    s = deck.new(); frame(s, "about me", "3 new messages")
    s.text(120, 160, 900, 100, "HI, I'M ZAHRA.", font=HEAD, size=40, color=BLACK)
    for i, t in enumerate(c.ABOUT):
        msg(s, 120, 288 + i * 208, 1120, 176, t, size=13.5, spacing=1.6,
            fill=[WHITE, WHITE, YEL][i])
        avatar(s, 40, 288 + i * 208 + 58, 60)
    photo_card(s, 1360, 250, 420, 480, "drop photo", rot=6)

    # 3 · what i do
    s = deck.new(); frame(s, "what i do", "4 things")
    for i, (title, sub) in enumerate(c.DO):
        x = 100 + (i % 2) * 900
        y = 190 + (i // 2) * 350
        s.rrect(x, y, 820, 300, fill=WHITE, line=BLACK, lw=4, radius=0.1)
        s.rect(x, y, 820, 60, fill=[PINK, LIME, BLUE, YEL][i])
        s.rect(x, y + 57, 820, 4, fill=BLACK)
        s.text(x + 24, y, 700, 60, "0%d" % (i + 1), font=MONO, size=15,
               color=WHITE if i in (0, 2) else BLACK, anchor=MSO_ANCHOR.MIDDLE,
               tracking=3)
        s.text(x + 34, y + 86, 740, 70, title, font=HEAD, size=30, color=BLACK)
        s.text(x + 36, y + 166, 740, 110, sub, font=BODY, size=13, color="333333",
               spacing=1.55)
    s.star(1760, 150, 130, fill=RED, line=BLACK, lw=3, points=16, rot=14)

    # 4 · experience
    s = deck.new(); frame(s, "where i've been", "5 messages")
    for i, (org, role) in enumerate(c.EXP):
        y = 176 + i * 150
        left = i % 2 == 0
        x = 120 if left else 700
        avatar(s, 40 if left else 1810, y + 40, 56, fill=[PINK, LIME, BLUE, YEL, RED][i])
        s.rrect(x, y, 1100, 118, fill=WHITE if left else YEL, line=BLACK, lw=3,
                radius=0.28)
        s.text(x + 34, y + 14, 900, 50, org, font=HEAD, size=20, color=BLACK)
        s.text(x + 36, y + 70, 900, 36, role, font=BODY, size=12, color="333333")
        s.text(x + 980, y, 100, 118, "0%d" % (i + 1), font=MONO, size=12, color="666666",
               anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)

    # 5 · sawala space
    s = deck.new(); frame(s, "sawala space", c.SAWALA_SUB.lower())
    photo_card(s, 130, 210, 620, 560, "drop photo", rot=-4)
    s.text(840, 170, 1000, 130, "SAWALA SPACE", font=HEAD, size=50, color=BLACK)
    stamp(s, 840, 318, "WELLNESS × COMMUNITY", fill=BLUE, size=12)
    msg(s, 840, 400, 980, 220, c.SAWALA_BODY, size=13.5, spacing=1.6)
    s.text(840, 656, 400, 44, "MY ROLE", font=MONO, size=13, color=BLACK, tracking=4)
    x, y = 840, 704
    for i, r in enumerate(c.SAWALA_ROLE):
        if i == 3:
            x, y = 840, 776
        x += stamp(s, x, y, r.upper(), fill=[PINK, LIME, YEL, BLUE, GREEN, RED][i],
                   size=12) + 14

    # 6 · selected works
    s = deck.new(); frame(s, "my work", "8 files")
    for i, cap in enumerate(c.WORKS_CAPS):
        gx = 110 + (i % 4) * 440
        gy = 200 + (i // 4) * 370
        s.rrect(gx, gy, 400, 300, fill=WHITE, line=BLACK, lw=4, radius=0.07)
        s.photo(gx + 20, gy + 20, 360, 200, "drop photo", fill="F0F0F0", line="CCCCCC",
                radius=0.04, label_color="999999", size=10)
        s.text(gx + 22, gy + 236, 300, 40, cap, font=MONO, size=12, color=BLACK,
               anchor=MSO_ANCHOR.MIDDLE)
    s.star(1740, 150, 120, fill=RED, line=BLACK, lw=3, points=16, rot=10)

    # 7 · stretch for stray
    s = deck.new(); frame(s, "stretch for stray", c.STRAY_SUB.lower())
    photo_card(s, 120, 200, 520, 600, "drop poster", rot=-5)
    s.text(730, 164, 1100, 280, "STRETCH\nFOR STRAY", font=HEAD, size=46, color=BLACK,
           spacing=0.96)
    msg(s, 730, 406, 1050, 134, c.STRAY_BODY, size=14, fill=YEL)
    s.text(730, 574, 500, 44, "MY CONTRIBUTION", font=MONO, size=13, color=BLACK,
           tracking=4)
    for i, it in enumerate(c.STRAY_LIST):
        y = 626 + i * 60
        s.rrect(730, y, 620, 50, fill=WHITE, line=BLACK, lw=3, radius=0.4)
        s.oval(748, y + 13, 24, 24, fill=[PINK, LIME, BLUE, YEL, GREEN][i], line=BLACK,
               lw=2)
        s.text(792, y, 520, 50, it, font=BODY, size=12.5, color=BLACK,
               anchor=MSO_ANCHOR.MIDDLE)
    photo_card(s, 1420, 600, 380, 280, "documentation", rot=5, burst_col=PINK)

    # 8 · beyond
    s = deck.new(); frame(s, "other works", "organisations & projects")
    s.text(120, 166, 1300, 60, c.BEYOND_BODY, font=BODY, size=14, color=BLACK)
    for i, (title, sub) in enumerate(c.BEYOND):
        x = 110 + i * 580
        s.rrect(x, 270, 540, 560, fill=WHITE, line=BLACK, lw=4, radius=0.08)
        s.rect(x, 270, 540, 70, fill=[PINK, LIME, BLUE][i])
        s.rect(x, 337, 540, 4, fill=BLACK)
        s.text(x + 24, 270, 400, 70, "0%d" % (i + 1), font=MONO, size=15,
               color=WHITE if i != 1 else BLACK, anchor=MSO_ANCHOR.MIDDLE, tracking=3)
        s.photo(x + 30, 370, 480, 190, "drop photo", fill="F0F0F0", line="CCCCCC",
                radius=0.04, label_color="999999", size=10)
        s.text(x + 32, 584, 470, 120, title, font=HEAD, size=26, color=BLACK,
               spacing=1.05)
        s.text(x + 34, 712, 470, 110, sub, font=BODY, size=12.5, color="333333",
               spacing=1.5)

    # 9 · skills
    s = deck.new(); frame(s, "skills & tools", "what i bring")
    for i, (title, items) in enumerate(c.SKILLS):
        x = 110 + i * 900
        s.rrect(x, 180, 820, 420, fill=WHITE, line=BLACK, lw=4, radius=0.08)
        s.rect(x, 180, 820, 66, fill=[PINK, BLUE][i])
        s.rect(x, 243, 820, 4, fill=BLACK)
        s.text(x + 28, 180, 600, 66, title.upper(), font=HEAD, size=26, color=WHITE,
               anchor=MSO_ANCHOR.MIDDLE)
        for j, it in enumerate(items):
            y = 276 + j * 76
            s.text(x + 34, y, 460, 56, it, font=BODY, size=14, color=BLACK,
                   anchor=MSO_ANCHOR.MIDDLE)
            s.rrect(x + 520, y + 20, 260, 20, fill="EAEAEA", line=BLACK, lw=2,
                    radius=0.5)
            s.rrect(x + 520, y + 20, 260 - j * 22, 20, fill=[PINK, BLUE][i], line=BLACK,
                    lw=2, radius=0.5)
    s.text(112, 636, 400, 44, "TOOLS", font=MONO, size=14, color=BLACK, tracking=4)
    x, y = 110, 690
    for i, t in enumerate(c.TOOLS):
        if i == 4:
            x, y = 110, 788
        x += stamp(s, x, y, t.upper(),
                   fill=[YEL, LIME, PINK, BLUE, GREEN, YEL, RED][i], size=11) + 14

    # 10 · contact
    s = deck.new(); frame(s, "let's talk", "always open")
    msg(s, 120, 200, 900, 150, "thanks 4 scrolling!! ♥", size=18, fill=WHITE)
    msg(s, 120, 380, 1120, 200, c.END_BODY, size=14.5, fill=YEL, spacing=1.6)
    s.text(120, 620, 1000, 300, "LET'S WORK\nTOGETHER.", font=HEAD, size=50, color=BLACK,
           spacing=0.98)
    for i, (lab, val) in enumerate(c.CONTACT):
        x = 1180
        y = 200 + i * 150
        s.rrect(x, y, 640, 120, fill=WHITE, line=BLACK, lw=4, radius=0.24)
        s.oval(x + 26, y + 30, 60, 60, fill=[GREEN, RED, BLUE][i], line=BLACK, lw=3)
        s.text(x + 116, y + 22, 460, 40, lab.upper(), font=MONO, size=13, color=BLACK,
               tracking=3)
        s.text(x + 116, y + 62, 480, 40, val, font=BODY, size=14, color="333333")
    s.star(1180, 640, 180, fill=PINK, line=BLACK, lw=4, points=16, rot=16)
    s.text(1180, 640, 180, 180, "HI!", font=HEAD, size=36, color=BLACK,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    photo_card(s, 1430, 620, 380, 260, "drop photo", rot=5, burst=False)
    return deck
