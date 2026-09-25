# -*- coding: utf-8 -*-
"""PORTFOLIO 03 — SOFT DESK.  Reference 3.

Clean UGC-creator energy: a white browser window floating on a soft blue sky,
heavy Archivo Black headlines with a yellow highlighter, generous whitespace,
a few scattered photo cards and folder tabs. The calm, minimal option.
"""
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import deckkit as dk
import content as c

SKY, WHITE, INK, YELLOW = "BBD7F0", "FFFFFF", "0D0D10", "FFE45C"
GREY, SOFT, PINKY = "8B93A1", "F3F5F9", "FFD3E4"
HEAD, BODY, MONO = "Archivo Black", "Inter", "Space Mono"

def win(s, x, y, w, h, url="www.zahralevina.com"):
    s.rrect(x, y, w, h, fill=WHITE, radius=0.03,
            shadow={"blur": 46, "dist": 16, "alpha": 18, "color": "24405E"})
    s.rect(x + 2, y + 2, w - 4, 62, fill=SOFT)
    for i, col in enumerate(["FF6058", "FFBE2F", "28C840"]):
        s.oval(x + 26 + i * 28, y + 24, 18, 18, fill=col)
    s.rrect(x + 130, y + 16, w - 260, 34, fill=WHITE, radius=0.5)
    s.text(x + 130, y + 16, w - 260, 34, url, font=MONO, size=10.5, color=GREY,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return x, y + 64, w, h - 64

def dock(s, y=968):
    s.rrect(660, y, 600, 88, fill="FFFFFF", radius=0.28,
            shadow={"blur": 30, "dist": 10, "alpha": 16, "color": "24405E"})
    for i, col in enumerate(["FF6FB5", "FFBE2F", "28C840", "5AA9E6", "C9B6FF", "FF8A65"]):
        s.rrect(690 + i * 92, y + 14, 60, 60, fill=col, radius=0.26)

def tab(s, x, y, w, h, label, fill=PINKY):
    s.rect(x, y, w * 0.44, 22, fill=fill)
    s.rect(x, y + 20, w, h, fill=fill)
    s.text(x + 18, y + 20, w - 36, 40, label, font=MONO, size=10, color=INK,
           anchor=MSO_ANCHOR.MIDDLE)

def highlight(s, x, y, w, h=34, color=YELLOW):
    s.rect(x, y, w, h, fill=color)

def build(deck):
    # 1 · cover
    s = deck.new(); s.bg(grad=(SKY, "DCEBF8"), angle=90)
    bx, by, bw, bh = win(s, 200, 120, 1520, 800)
    highlight(s, bx + 86, by + 150, 530, 86)
    s.text(bx + 90, by + 96, 900, 160, "zahra", font=HEAD, size=72, color=INK)
    s.text(bx + 90, by + 268, 900, 160, "levina", font=HEAD, size=72, color=INK)
    s.text(bx + 94, by + 486, 700, 50, c.DISCIPLINES, font=MONO, size=12.5, color=GREY)
    s.text(bx + 94, by + 546, 700, 40, c.KICKER, font=MONO, size=12.5, color=INK,
           tracking=6)
    s.photo(bx + 880, by + 70, 480, 560, "drop portrait", fill=SOFT, line="C8D2E0",
            radius=0.04, label_color=GREY)
    s.photo(bx + 760, by + 420, 220, 260, "outfit.jpg", fill=PINKY, line="E7B9CD",
            radius=0.05, rot=-8, label_color="8A6478")
    tab(s, 140, 700, 200, 120, "editing.jpg")
    tab(s, 1700, 260, 200, 120, "slay.png", fill="D7F0E2")
    dock(s)

    # 2 · about
    s = deck.new(); s.bg(grad=(SKY, "DCEBF8"), angle=90)
    bx, by, bw, bh = win(s, 160, 130, 1600, 800, "www.zahralevina.com/about")
    s.text(bx + 80, by + 70, 700, 90, "hi! i'm", font=HEAD, size=44, color=GREY)
    highlight(s, bx + 78, by + 186, 470, 70)
    s.text(bx + 80, by + 146, 900, 120, "zahra.", font=HEAD, size=58, color=INK)
    s.text(bx + 82, by + 322, 740, 400, c.ABOUT, font=BODY, size=12.5, color="2B3038",
           spacing=1.8, after=18)
    s.photo(bx + 900, by + 60, 560, 620, "drop photo", fill=SOFT, line="C8D2E0",
            radius=0.03, label_color=GREY)
    s.text(bx + 82, by + 640, 700, 40, "— based in indonesia", font=MONO, size=11,
           color=GREY)
    tab(s, 1740, 620, 170, 110, "me.jpg")

    # 3 · what i do
    s = deck.new(); s.bg(grad=(SKY, "DCEBF8"), angle=90)
    bx, by, bw, bh = win(s, 160, 130, 1600, 800, "www.zahralevina.com/services")
    highlight(s, bx + 78, by + 100, 430, 60)
    s.text(bx + 80, by + 66, 900, 100, "what i do", font=HEAD, size=48, color=INK)
    for i, (title, sub) in enumerate(c.DO):
        x = bx + 80 + (i % 2) * 760
        y = by + 246 + (i // 2) * 240
        s.text(x, y, 100, 50, "0%d" % (i + 1), font=MONO, size=13, color=GREY, tracking=4)
        s.text(x, y + 40, 640, 60, title, font=HEAD, size=24, color=INK)
        s.text(x + 2, y + 104, 640, 90, sub, font=BODY, size=12.5, color="5B6472",
               spacing=1.6)
        s.line(x, y + 200, 640, "E3E8EF", 1.4)

    # 4 · experience
    s = deck.new(); s.bg(grad=(SKY, "DCEBF8"), angle=90)
    bx, by, bw, bh = win(s, 160, 130, 1600, 800, "www.zahralevina.com/experience")
    highlight(s, bx + 78, by + 92, 560, 60)
    s.text(bx + 80, by + 56, 1000, 100, "where i've been", font=HEAD, size=44, color=INK)
    for i, (org, role) in enumerate(c.EXP):
        y = by + 216 + i * 100
        s.text(bx + 80, y + 4, 90, 50, "0%d" % (i + 1), font=MONO, size=12, color=GREY)
        s.text(bx + 180, y - 8, 800, 52, org, font=HEAD, size=19, color=INK)
        s.text(bx + 182, y + 44, 900, 36, role, font=BODY, size=12, color="5B6472")
        s.line(bx + 80, y + 84, 1440, "E3E8EF", 1.2)

    # 5 · sawala space
    s = deck.new(); s.bg(grad=(SKY, "DCEBF8"), angle=90)
    bx, by, bw, bh = win(s, 160, 130, 1600, 800, "www.sawalaspace.com")
    s.photo(bx + 60, by + 56, 640, 580, "drop photo", fill=SOFT, line="C8D2E0",
            radius=0.03, label_color=GREY)
    s.text(bx + 760, by + 60, 700, 50, "featured project", font=MONO, size=12, color=GREY,
           tracking=5)
    highlight(s, bx + 758, by + 138, 520, 60)
    s.text(bx + 760, by + 104, 900, 100, "sawala space", font=HEAD, size=42, color=INK)
    s.text(bx + 762, by + 244, 700, 44, c.SAWALA_SUB, font=BODY, size=15, color="2B3038")
    s.text(bx + 762, by + 302, 700, 200, c.SAWALA_BODY, font=BODY, size=12.5,
           color="5B6472", spacing=1.8)
    s.text(bx + 762, by + 496, 400, 40, "role", font=MONO, size=11, color=GREY, tracking=5)
    x, y = bx + 762, by + 536
    for i, r in enumerate(c.SAWALA_ROLE):
        if i == 3:
            x, y = bx + 762, by + 594
        x += s.pill(x, y, r, size=11, pad=18, h=46, fill=SOFT, color=INK, font=BODY,
                    tracking=1) + 10

    # 6 · selected works
    s = deck.new(); s.bg(grad=(SKY, "DCEBF8"), angle=90)
    bx, by, bw, bh = win(s, 120, 120, 1680, 830, "www.zahralevina.com/work")
    highlight(s, bx + 58, by + 78, 420, 56)
    s.text(bx + 60, by + 48, 900, 90, "my work", font=HEAD, size=40, color=INK)
    s.text(bx + 62, by + 168, 1100, 60, c.WORKS_BODY, font=BODY, size=11.5,
           color="5B6472", spacing=1.5)
    for i, cap in enumerate(c.WORKS_CAPS):
        gx = bx + 60 + (i % 4) * 400
        gy = by + 258 + (i // 4) * 240
        s.photo(gx, gy, 368, 186, "", fill=SOFT, line="C8D2E0", radius=0.04,
                label_color=GREY)
        s.text(gx + 4, gy + 194, 300, 30, cap, font=MONO, size=10, color=GREY)

    # 7 · stretch for stray
    s = deck.new(); s.bg(grad=(SKY, "DCEBF8"), angle=90)
    bx, by, bw, bh = win(s, 160, 130, 1600, 800, "www.zahralevina.com/stretch-for-stray")
    s.photo(bx + 60, by + 56, 520, 580, "drop poster", fill=SOFT, line="C8D2E0",
            radius=0.03, label_color=GREY)
    s.text(bx + 640, by + 60, 700, 44, c.STRAY_SUB.lower(), font=MONO, size=12,
           color=GREY, tracking=5)
    highlight(s, bx + 638, by + 138, 640, 60)
    s.text(bx + 640, by + 104, 1000, 100, "stretch for stray", font=HEAD, size=40,
           color=INK)
    s.text(bx + 642, by + 246, 760, 90, c.STRAY_BODY, font=BODY, size=13.5,
           color="2B3038", spacing=1.6)
    s.text(bx + 642, by + 360, 500, 40, "my contribution", font=MONO, size=11,
           color=GREY, tracking=5)
    for i, it in enumerate(c.STRAY_LIST):
        y = by + 406 + i * 54
        s.rrect(bx + 642, y + 14, 18, 18, fill=YELLOW, radius=0.4)
        s.text(bx + 686, y, 640, 46, it, font=BODY, size=13, color="2B3038",
               anchor=MSO_ANCHOR.MIDDLE)
    s.photo(bx + 1180, by + 380, 240, 240, "documentation", fill=PINKY, line="E7B9CD",
            radius=0.05, rot=6, label_color="8A6478")

    # 8 · beyond
    s = deck.new(); s.bg(grad=(SKY, "DCEBF8"), angle=90)
    bx, by, bw, bh = win(s, 160, 130, 1600, 800, "www.zahralevina.com/more")
    highlight(s, bx + 78, by + 76, 620, 56)
    s.text(bx + 80, by + 48, 1000, 90, "beyond creative work", font=HEAD, size=36,
           color=INK)
    s.text(bx + 82, by + 160, 1200, 60, c.BEYOND_BODY, font=BODY, size=12,
           color="5B6472", spacing=1.5)
    for i, (title, sub) in enumerate(c.BEYOND):
        x = bx + 80 + i * 490
        s.rect(x, by + 250, 440, 380, fill=SOFT)
        s.rect(x, by + 250, 440, 10, fill=[YELLOW, PINKY, "D7F0E2"][i])
        s.text(x + 30, by + 292, 100, 40, "0%d" % (i + 1), font=MONO, size=12, color=GREY)
        s.text(x + 30, by + 340, 380, 130, title, font=HEAD, size=18, color=INK,
               spacing=1.3)
        s.text(x + 32, by + 480, 380, 120, sub, font=BODY, size=11.5, color="5B6472",
               spacing=1.55)

    # 9 · skills
    s = deck.new(); s.bg(grad=(SKY, "DCEBF8"), angle=90)
    bx, by, bw, bh = win(s, 160, 130, 1600, 800, "www.zahralevina.com/skills")
    highlight(s, bx + 78, by + 76, 460, 56)
    s.text(bx + 80, by + 48, 900, 90, "skills & tools", font=HEAD, size=38, color=INK)
    for i, (title, items) in enumerate(c.SKILLS):
        x = bx + 80 + i * 740
        s.text(x, by + 166, 400, 44, title.lower(), font=MONO, size=12, color=GREY,
               tracking=5)
        s.line(x, by + 212, 620, "E3E8EF", 1.2)
        for j, it in enumerate(items):
            y = by + 238 + j * 74
            s.text(x, y, 500, 46, it, font=BODY, size=14, color="2B3038",
                   anchor=MSO_ANCHOR.MIDDLE)
            s.rrect(x + 460, y + 18, 160, 10, fill="E9EDF3", radius=0.5)
            s.rrect(x + 460, y + 18, 160 - j * 14, 10, fill=INK, radius=0.5)
    s.text(bx + 80, by + 580, 400, 40, "tools", font=MONO, size=12, color=GREY,
           tracking=5)
    x, y = bx + 80, by + 622
    for i, t in enumerate(c.TOOLS):
        if i == 4:
            x, y = bx + 80, by + 686
        x += s.pill(x, y, t, size=11.5, pad=22, h=48, fill=SOFT, color=INK, font=BODY,
                    tracking=1) + 14

    # 10 · contact
    s = deck.new(); s.bg(grad=(SKY, "DCEBF8"), angle=90)
    bx, by, bw, bh = win(s, 300, 140, 1320, 720, "mail — new message")
    s.text(bx + 80, by + 80, 700, 50, "say hi", font=MONO, size=12, color=GREY,
           tracking=6)
    highlight(s, bx + 78, by + 168, 700, 72)
    s.text(bx + 80, by + 124, 1100, 120, "let's work together.", font=HEAD, size=50,
           color=INK)
    s.text(bx + 82, by + 288, 900, 110, c.END_BODY, font=BODY, size=13, color="5B6472",
           spacing=1.75)
    for i, (lab, val) in enumerate(c.CONTACT):
        y = by + 412 + i * 72
        s.text(bx + 82, y, 220, 50, lab.lower(), font=MONO, size=11, color=GREY,
               tracking=4, anchor=MSO_ANCHOR.MIDDLE)
        s.text(bx + 320, y, 800, 50, val, font=BODY, size=15, color=INK,
               anchor=MSO_ANCHOR.MIDDLE)
        s.line(bx + 82, y + 56, 1140, "E3E8EF", 1)
    s.text(bx + 82, by + 636, 600, 44, "zahra levina", font=HEAD, size=18, color=INK)
    dock(s)
    return deck
