# -*- coding: utf-8 -*-
"""VERSION 03 — SOFT DESK.  Reference 3.

Clean creator-desktop: a white browser window floating on soft blue, heavy
Archivo Black headlines with a yellow highlighter, folder tabs, taped photo
cards, sticky notes and a dock. Calm, but never bare.
"""
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import deckkit as dk
import brief as b

SKY, WHITE, INK, YELLOW = "BBD7F0", "FFFFFF", "0D0D10", "FFE45C"
GREY, SOFT, PINKY, MINT = "8B93A1", "F3F5F9", "FFD3E4", "D7F0E2"
HEAD, BODY, MONO = "Archivo Black", "Inter", "Space Mono"

def ground(s):
    s.bg(grad=(SKY, "DCEBF8"), angle=90)
    s.oval(-180, 620, 780, 560, fill=WHITE, alpha=22)
    s.oval(1420, -160, 700, 520, fill=WHITE, alpha=18)

def win(s, x, y, w, h, url="www.zahralevina.com"):
    s.rrect(x, y, w, h, fill=WHITE, radius=0.03,
            shadow={"blur": 44, "dist": 15, "alpha": 17, "color": "24405E"})
    s.rect(x + 2, y + 2, w - 4, 58, fill=SOFT)
    for i, col in enumerate(["FF6058", "FFBE2F", "28C840"]):
        s.oval(x + 24 + i * 26, y + 21, 16, 16, fill=col)
    s.rrect(x + 122, y + 14, w - 244, 30, fill=WHITE, radius=0.5)
    s.text(x + 122, y + 14, w - 244, 30, url, font=MONO, size=10, color=GREY,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return x, y + 60, w, h - 60

def tab(s, x, y, w, h, label, fill=PINKY, rot=0):
    s.rect(x, y, w * 0.42, 20, fill=fill, rot=rot)
    s.rect(x, y + 18, w, h, fill=fill, rot=rot)
    s.text(x + 16, y + 18, w - 32, 36, label, font=MONO, size=9.5, color=INK,
           anchor=MSO_ANCHOR.MIDDLE)

def note(s, x, y, w, h, text, fill=YELLOW, rot=-2):
    s.rect(x, y, w, h, fill=fill, rot=rot,
           shadow={"blur": 14, "dist": 5, "alpha": 14, "color": "24405E"})
    s.text(x + 18, y + 14, w - 36, h - 28, text, font=MONO, size=10, color=INK,
           spacing=1.5)

def hl(s, x, y, w, h=30, color=YELLOW):
    s.rect(x, y, w, h, fill=color)

def mark(s, x, y, text, size=44, color=INK, max_w=None, gap=0, one_line=True,
         band=YELLOW, font=HEAD):
    """Heading with a highlighter bar sized and placed from the measured text."""
    if max_w and one_line:
        while size > 10 and dk.measure(text, font, size, 0) > max_w * dk.SAFETY:
            size -= 0.5
    w = dk.measure(text, font, size, 0)
    lh = dk.line_height(font, size, 1.15)
    s.rect(x - 6, y + lh * 0.40, w + 20, lh * 0.52, fill=band)
    return s.head(x, y, text, font=font, size=size, color=color, max_w=max_w,
                  one_line=one_line, gap=gap)

def shot(s, kind, x, y, w, h, label="", rot=0, fill=SOFT):
    return s.cut(kind, x, y, w, h, label, fill=fill, line="D5DEE9", lw=2, rot=rot,
                 radius=0.05 if kind in ("rrect", "arch") else None,
                 label_color=GREY, size=9.5, font=BODY)

def dock(s, y=986):
    s.rrect(700, y, 520, 76, fill=WHITE, radius=0.28,
            shadow={"blur": 26, "dist": 8, "alpha": 14, "color": "24405E"})
    for i, col in enumerate(["FF6FB5", "FFBE2F", "28C840", "5AA9E6", "C9B6FF", "FF8A65"]):
        s.rrect(726 + i * 80, y + 13, 50, 50, fill=col, radius=0.26)

def build(deck):
    # 01 · cover
    s = deck.new(); ground(s)
    bx, by, bw, bh = win(s, 180, 110, 1560, 810)
    y = s.head(bx + 74, by + 46, b.KICKER[0], font=MONO, size=12, color=GREY,
               tracking=5, gap=12)
    y = mark(s, bx + 74, y, "content", 52, max_w=620, gap=0)
    y = s.head(bx + 74, y, "production", font=HEAD, size=52, color=INK, max_w=640,
               one_line=True, gap=0)
    y = s.head(bx + 74, y, "portfolio", font=HEAD, size=52, color=INK, gap=22)
    s.rect(bx + 74, y, 150, 6, fill=INK)
    y = s.head(bx + 74, y + 24, b.NAME.title(), font=HEAD, size=20, color=INK, gap=10)
    s.para(bx + 76, y, 540, b.TAGLINE, font=MONO, size=10.5, color=GREY, spacing=1.6)
    shot(s, "arch", bx + 840, by + 54, 440, 560, "drop portrait")
    shot(s, "rrect", bx + 1180, by + 380, 260, 240, "photo", rot=6, fill=PINKY)
    shot(s, "oval", bx + 740, by + 430, 200, 200, "photo")
    tab(s, 96, 740, 200, 118, "editing.jpg")
    tab(s, 1706, 250, 200, 120, "shoot.png", fill=MINT)
    note(s, 1660, 640, 230, 150, "prep → shoot →\nedit → publish", rot=3)
    dock(s)

    # 02 · about
    s = deck.new(); ground(s)
    bx, by, bw, bh = win(s, 150, 120, 1620, 810, "www.zahralevina.com/about")
    y = s.head(bx + 70, by + 46, "hi! i'm", font=HEAD, size=34, color=GREY, gap=6)
    y = mark(s, bx + 70, y, "zahra.", 50, max_w=600, gap=26)
    s.para(bx + 72, y, 700, b.ABOUT, font=BODY, size=12.5, color="2B3038", spacing=1.8,
           after=18, max_h=330)
    shot(s, "arch", bx + 880, by + 44, 480, 580, "drop portrait")
    shot(s, "oval", bx + 1300, by + 120, 230, 230, "photo")
    shot(s, "snip", bx + 1290, by + 400, 250, 220, "photo", rot=-5, fill=MINT)
    note(s, bx + 80, by + 596, 300, 120, "content · creative ·\ncommunication")
    tab(s, 1730, 640, 180, 110, "me.jpg")
    s.annot(bx + 880, by + 650, "SELECTED FRAMES", color=GREY, size=9.5, font=MONO,
            leader=50)

    # 03 · from idea to publish
    s = deck.new(); ground(s)
    bx, by, bw, bh = win(s, 150, 120, 1620, 810, "www.zahralevina.com/process")
    y = mark(s, bx + 70, by + 40, b.FLOW_TITLE.lower(), 42, max_w=900, gap=28)
    for i, step in enumerate(b.FLOW):
        x = bx + 70 + i * 208
        s.rrect(x, y, 180, 92, fill=SOFT, radius=0.16)
        s.text(x, y, 180, 92, step, font=MONO, size=12, color=INK, tracking=3,
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        s.text(x + 4, y - 28, 100, 26, "0%d" % (i + 1), font=MONO, size=9.5, color=GREY)
        if i < 6:
            s.text(x + 182, y + 28, 26, 36, "→", font=BODY, size=14, color=GREY,
                   align=PP_ALIGN.CENTER)
    y += 130
    s.para(bx + 70, y, 760, b.FLOW_NOTE, font=BODY, size=13, color="2B3038",
           spacing=1.8, after=14, max_h=210)
    shot(s, "rrect", bx + 900, y - 10, 300, 210, "content prep")
    shot(s, "oval", bx + 1230, y - 10, 210, 210, "photo")
    shot(s, "snip", bx + 1240, y + 220, 300, 160, "photo", rot=4, fill=PINKY)
    note(s, bx + 900, y + 230, 300, 150, "check before publish:\ncaption · crop · date")
    dock(s)

    # 04 · content, in different forms
    s = deck.new(); ground(s)
    bx, by, bw, bh = win(s, 150, 120, 1620, 810, "www.zahralevina.com/work")
    y = mark(s, bx + 70, by + 36, b.FORMS_TITLE.lower(), 38, max_w=1100, gap=26)
    kinds = ["oval", "hex", "arch", "snip"]
    for i, (group, items) in enumerate(b.FORMS):
        x = bx + 70 + i * 372
        shot(s, kinds[i], x, y, 240, 180, "", fill=[SOFT, PINKY, MINT, SOFT][i])
        gy = s.head(x, y + 202, group.lower(), font=HEAD, size=20, color=INK, gap=10)
        s.line(x, gy, 200, "E3E8EF", 1.4)
        for j, it in enumerate(items):
            s.text(x, gy + 16 + j * 40, 320, 36, it, font=BODY, size=12,
                   color="5B6472", anchor=MSO_ANCHOR.MIDDLE)
    tab(s, 1740, 300, 170, 110, "assets", fill=MINT)

    # 05 · sawala space
    s = deck.new(); ground(s)
    bx, by, bw, bh = win(s, 150, 120, 1620, 810, "sawalaspace — project")
    shot(s, "arch", bx + 60, by + 46, 520, 520, b.SAWALA_SHOTS[0])
    shot(s, "rrect", bx + 60, by + 586, 240, 150, b.SAWALA_SHOTS[1])
    shot(s, "oval", bx + 330, by + 586, 150, 150, b.SAWALA_SHOTS[2])
    y = s.head(bx + 650, by + 44, "selected project", font=MONO, size=11, color=GREY,
               tracking=5, gap=14)
    y = mark(s, bx + 650, y, b.SAWALA_TITLE.lower(), 40, max_w=700, gap=14)
    y = s.head(bx + 650, y, b.SAWALA_SUB.lower(), font=BODY, size=14, color="2B3038",
               gap=20)
    y = s.para(bx + 650, y, 760, b.SAWALA_BODY, font=BODY, size=12.5, color="5B6472",
               spacing=1.8, max_h=240, gap=26)
    x = bx + 650
    for i, t in enumerate(b.SAWALA_TAGS):
        if i == 3:
            x, y = bx + 650, y + 58
        x += s.pill(x, y, t.lower(), size=11, pad=18, h=46, fill=SOFT, color=INK,
                    font=BODY, tracking=1) + 12
    shot(s, "snip", bx + 1240, by + 560, 300, 180, b.SAWALA_SHOTS[3], rot=-4, fill=PINKY)
    note(s, bx + 1290, by + 44, 250, 110, "concept → content\n→ event")

    # 06 · content in practice
    s = deck.new(); ground(s)
    bx, by, bw, bh = win(s, 120, 110, 1680, 830, "www.zahralevina.com/content")
    y = mark(s, bx + 60, by + 34, b.PRACTICE_TITLE.lower(), 33, max_w=1400, gap=26)
    kinds = ["arch", "oval", "snip", "hex", "rrect", "oct"]
    for i, (lab, sub) in enumerate(b.PRACTICE):
        x = bx + 60 + (i % 3) * 528
        cy = y + (i // 3) * 286
        shot(s, kinds[i], x, cy, 240, 200, "", rot=(-3, 0, 3)[i % 3],
             fill=[SOFT, PINKY, MINT][i % 3])
        s.text(x + 260, cy, 80, 26, "0%d" % (i + 1), font=MONO, size=9.5, color=GREY)
        ly = s.head(x + 260, cy + 30, lab.lower(), font=HEAD, size=15, color=INK,
                    max_w=250, gap=10)
        s.para(x + 260, ly, 250, sub, font=BODY, size=11, color="5B6472", spacing=1.5)

    # 07 · stretch for stray
    s = deck.new(); ground(s)
    bx, by, bw, bh = win(s, 150, 120, 1620, 810, "www.zahralevina.com/stretch-for-stray")
    shot(s, "arch", bx + 56, by + 46, 460, 560, b.STRAY_SHOTS[0])
    y = s.head(bx + 580, by + 44, b.STRAY_SUB.lower(), font=MONO, size=11, color=GREY,
               tracking=5, gap=12)
    y = mark(s, bx + 580, y, b.STRAY_TITLE.lower(), 40, max_w=860, gap=18)
    y = s.para(bx + 580, y, 720, b.STRAY_BODY, font=BODY, size=13.5, color="2B3038",
               spacing=1.6, gap=24)
    y = s.head(bx + 580, y, "my contribution", font=MONO, size=10.5, color=GREY,
               tracking=5, gap=14)
    for i, it in enumerate(b.STRAY_LIST):
        ry = y + i * 48
        s.rrect(bx + 580, ry + 12, 16, 16, fill=YELLOW, radius=0.4)
        s.text(bx + 618, ry, 560, 40, it, font=BODY, size=12.5, color="2B3038",
               anchor=MSO_ANCHOR.MIDDLE)
    shot(s, "rrect", bx + 1200, by + 330, 320, 200, b.STRAY_SHOTS[1], rot=4, fill=PINKY)
    shot(s, "oval", bx + 1230, by + 560, 180, 180, b.STRAY_SHOTS[2])
    tab(s, 1736, 660, 170, 110, "docs", fill=MINT)

    # 08 · behind the content
    s = deck.new(); ground(s)
    bx, by, bw, bh = win(s, 110, 110, 1700, 840, "process — camera roll")
    y = mark(s, bx + 50, by + 28, b.BEHIND_TITLE.lower(), 35, max_w=1100, gap=18)
    x = bx + 50
    for step in b.BEHIND_STEPS:
        x += s.pill(x, y, step.lower(), size=11, pad=18, h=44, fill=SOFT, color=INK,
                    font=MONO, tracking=2) + 12
    y += 62
    kinds = ["snip", "oval", "rrect", "hex", "arch", "snip1", "oct", "rrect"]
    for i, (cap, step) in enumerate(b.BEHIND_SHOTS):
        cx = bx + 50 + (i % 4) * 402
        cy = y + (i // 4) * 258
        shot(s, kinds[i], cx, cy, 360, 190, cap, rot=(-3, 2, -2, 3)[i % 4],
             fill=[SOFT, PINKY, MINT, SOFT][i % 4])
        s.text(cx + 2, cy + 200, 300, 28, step.lower(), font=MONO, size=9.5, color=GREY)

    # 09 · tools
    s = deck.new(); ground(s)
    bx, by, bw, bh = win(s, 150, 120, 1620, 810, "www.zahralevina.com/tools")
    y = mark(s, bx + 70, by + 36, b.TOOLS_TITLE.lower(), 36, max_w=900, gap=30)
    for i, (group, items) in enumerate(b.TOOLS):
        x = bx + 70 + i * 500
        gy = s.head(x, y, group.lower(), font=MONO, size=11, color=GREY, tracking=5,
                    gap=12)
        s.line(x, gy, 420, "E3E8EF", 1.4)
        for j, it in enumerate(items):
            ry = gy + 20 + j * 76
            s.rrect(x, ry, 420, 62, fill=SOFT, radius=0.16)
            s.rrect(x + 20, ry + 15, 32, 32, fill=[YELLOW, PINKY, MINT][i], radius=0.22)
            s.text(x + 70, ry, 330, 62, it, font=BODY, size=13, color=INK,
                   anchor=MSO_ANCHOR.MIDDLE)
    note(s, bx + 70, by + 560, 900, 130, b.TOOLS_NOTE, fill=YELLOW, rot=-1)
    shot(s, "arch", bx + 1180, by + 400, 300, 280, "photo")
    tab(s, 1734, 320, 180, 110, "exports", fill=MINT)

    # 10 · closing
    s = deck.new(); ground(s)
    bx, by, bw, bh = win(s, 280, 130, 1360, 740, "mail — new message")
    y = s.head(bx + 70, by + 60, "say hi", font=MONO, size=11, color=GREY, tracking=6,
               gap=18)
    y = mark(s, bx + 70, y, b.END_TITLE[0].lower(), 38, max_w=820, gap=0)
    y = s.head(bx + 70, y, b.END_TITLE[1].lower(), font=HEAD, size=38, color=INK,
               max_w=820, one_line=True, gap=22)
    y = s.head(bx + 70, y, b.NAME.title(), font=HEAD, size=19, color=INK, gap=6)
    y = s.head(bx + 70, y, b.END_ROLE + "  ·  " + b.END_SUB, font=MONO, size=10,
               color=GREY, tracking=2, gap=22)
    for i, (lab, val) in enumerate(b.CONTACT):
        ry = y + i * 62
        s.text(bx + 70, ry, 220, 46, lab.lower(), font=MONO, size=10.5, color=GREY,
               tracking=3, anchor=MSO_ANCHOR.MIDDLE)
        s.text(bx + 300, ry, 700, 46, val, font=BODY, size=14, color=INK,
               anchor=MSO_ANCHOR.MIDDLE)
        s.line(bx + 70, ry + 50, 880, "E3E8EF", 1)
    shot(s, "arch", bx + 1060, by + 100, 250, 320, "photo")
    note(s, bx + 1060, by + 450, 250, 130, "open to new\ncontent projects", rot=2)
    dock(s)
    return deck
