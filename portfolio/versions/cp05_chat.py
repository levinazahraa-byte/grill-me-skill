# -*- coding: utf-8 -*-
"""VERSION 05 — CHAT.  Reference 5.

A blown-up messaging thread: acid yellow-to-lime ground, thick black outlines,
speech bubbles, starbursts and tilted photo cards with an input bar at the
foot of every slide. Loud, playful, high contrast.
"""
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import deckkit as dk
import brief as b

YEL, LIME, SKY, WHITE, BLACK = "FFE83D", "9BE22B", "CFEFFF", "FFFFFF", "000000"
RED, BLUE, GREEN, PINK = "FF3B30", "2B6CFF", "34C759", "FF7BC4"
HEAD, MONO, BODY = "Anton", "Space Mono", "Poppins"

def frame(s, title, sub=None):
    s.bg(grad=(YEL, LIME), angle=90)
    s.rect(0, 0, 1920, 124, grad=(YEL, "F5D800"), angle=90)
    s.rect(0, 122, 1920, 5, fill=BLACK)
    s.oval(42, 28, 64, 64, fill=WHITE, line=BLACK, lw=3)
    s.oval(57, 43, 34, 34, fill=PINK)
    s.head(130, 14, title, font=HEAD, size=32, color=BLACK, max_w=1100, one_line=True)
    if sub:
        s.text(132, 80, 900, 32, sub, font=MONO, size=11, color="3A3A3A")
    for i in range(3):
        s.oval(1852, 44 + i * 17, 9, 9, fill=BLACK)
    s.rect(0, 946, 1920, 5, fill=BLACK)
    s.rect(0, 951, 1920, 129, grad=("F5D800", YEL), angle=90)
    s.rrect(116, 984, 1560, 64, fill=WHITE, line=BLACK, lw=3, radius=0.5)
    s.text(156, 984, 1200, 64, "type a message...", font=BODY, size=12.5,
           color="8A8A8A", anchor=MSO_ANCHOR.MIDDLE)
    s.oval(38, 984, 64, 64, fill=GREEN, line=BLACK, lw=3)
    s.oval(1712, 984, 64, 64, fill=GREEN, line=BLACK, lw=3)
    s.rect(0, 127, 1920, 819, fill=SKY)

def bub(s, x, y, w, body, size=13.5, fill=WHITE, side="l", font=BODY, pad=30,
        spacing=1.55, min_h=0):
    h = max(min_h, dk.block_height(body, font, size, w - pad * 2, spacing, 12) + 44)
    s.bubble(x, y, w, h, body, fill=fill, line=BLACK, lw=3, font=font, size=size,
             tail="bl" if side == "l" else "br", radius=0.3, spacing=spacing, pad=pad)
    return y + h + 34

def avatar(s, x, y, size=54, fill=PINK):
    s.oval(x, y, size, size, fill=WHITE, line=BLACK, lw=3)
    s.oval(x + size * 0.22, y + size * 0.22, size * 0.56, size * 0.56, fill=fill)

def shot(s, kind, x, y, w, h, label="", rot=-5, burst=None):
    if burst:
        s.star(x - 52, y - 46, max(w, h) * 0.5, fill=burst, line=BLACK, lw=3, points=16,
               rot=12)
    return s.cut(kind, x, y, w, h, label, fill=WHITE, line=BLACK, lw=4, rot=rot,
                 radius=0.06 if kind in ("rrect", "arch") else None,
                 label_color="7A7A7A", size=10, font=BODY)

def stamp(s, x, y, text, fill=RED, size=12):
    return s.pill(x, y, text, size=size, pad=20, h=48, fill=fill, color=WHITE,
                  line=BLACK, font=MONO, tracking=2, radius=0.4)

def build(deck):
    # 01 · cover
    s = deck.new(); frame(s, "zahra levina", "online now")
    y = bub(s, 110, 166, 620, "hey!! welcome 2 my portfolio", size=16)
    y = bub(s, 110, y, 740, b.TAGLINE, size=13.5)
    stamp(s, 110, y, "  ·  ".join(b.KICKER), fill=BLACK, size=11)
    hy = s.head(108, y + 64, "CONTENT", font=HEAD, size=44, color=BLACK, gap=0)
    s.head(108, hy, "PRODUCTION", font=HEAD, size=44, color=BLACK, max_w=760,
           one_line=True)
    shot(s, "rrect", 1060, 190, 500, 540, "drop portrait", rot=-4, burst=LIME)
    shot(s, "oval", 1500, 560, 230, 230, "photo", rot=6)
    s.star(880, 640, 130, fill=RED, line=BLACK, lw=3, points=16, rot=20)
    s.text(880, 640, 130, 130, "NEW", font=HEAD, size=20, color=WHITE,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    avatar(s, 1740, 210, 66, fill=YEL)

    # 02 · about
    s = deck.new(); frame(s, "about me", "2 new messages")
    s.head(110, 156, b.ABOUT_TITLE, font=HEAD, size=40, color=BLACK, max_w=900,
           one_line=True)
    y = 250
    for i, t in enumerate(b.ABOUT):
        avatar(s, 40, y + 46, 54)
        y = bub(s, 110, y, 1020, t, size=13.5, fill=[WHITE, YEL][i])
    shot(s, "rrect", 1240, 200, 420, 460, "drop portrait", rot=5, burst=PINK)
    shot(s, "snip", 1560, 640, 260, 220, "photo", rot=-6)
    s.star(1140, 700, 110, fill=BLUE, line=BLACK, lw=3, points=16, rot=8)

    # 03 · from idea to publish
    s = deck.new(); frame(s, b.FLOW_TITLE.lower(), "how it actually goes")
    cols = [PINK, LIME, BLUE, YEL, RED, GREEN, PINK]
    for i, step in enumerate(b.FLOW):
        x = 104 + i * 254
        s.rrect(x, 190, 232, 150, fill=WHITE, line=BLACK, lw=4, radius=0.12)
        s.rect(x, 190, 232, 52, fill=cols[i])
        s.rect(x, 239, 232, 4, fill=BLACK)
        s.text(x, 190, 232, 52, "0%d" % (i + 1), font=MONO, size=13,
               color=WHITE if i in (0, 2, 4, 6) else BLACK, align=PP_ALIGN.CENTER,
               anchor=MSO_ANCHOR.MIDDLE, tracking=2)
        s.text(x, 250, 232, 80, step, font=HEAD, size=21, color=BLACK,
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    y = bub(s, 110, 386, 1000, b.FLOW_NOTE[0], size=15, fill=WHITE)
    y = bub(s, 110, y, 1100, b.FLOW_NOTE[1], size=14, fill=YEL)
    shot(s, "rrect", 1260, 400, 320, 220, "content prep", rot=4, burst=LIME)
    shot(s, "oval", 1600, 440, 200, 200, "photo", rot=-4)
    shot(s, "snip", 1300, 660, 460, 200, "photo", rot=2)

    # 04 · content, in different forms
    s = deck.new(); frame(s, b.FORMS_TITLE.lower(), "4 buckets")
    kinds = ["oval", "hex", "arch", "snip"]
    for i, (group, items) in enumerate(b.FORMS):
        x = 104 + i * 440
        s.rrect(x, 172, 412, 720, fill=WHITE, line=BLACK, lw=4, radius=0.07)
        s.rect(x, 172, 412, 62, fill=[PINK, LIME, BLUE, YEL][i])
        s.rect(x, 231, 412, 4, fill=BLACK)
        s.text(x, 172, 412, 62, group, font=HEAD, size=22,
               color=WHITE if i in (0, 2) else BLACK, align=PP_ALIGN.CENTER,
               anchor=MSO_ANCHOR.MIDDLE)
        shot(s, kinds[i], x + 46, 258, 320, 190, "", rot=(-3, 3)[i % 2])
        for j, it in enumerate(items):
            ry = 480 + j * 96
            s.rrect(x + 28, ry, 356, 76, fill=SKY, line=BLACK, lw=2.5, radius=0.2)
            s.text(x + 50, ry, 320, 76, it, font=BODY, size=12.5, color=BLACK,
                   anchor=MSO_ANCHOR.MIDDLE)

    # 05 · sawala space
    s = deck.new(); frame(s, b.SAWALA_TITLE.lower(), b.SAWALA_SUB.lower())
    shot(s, "rrect", 110, 180, 560, 480, b.SAWALA_SHOTS[0], rot=-4, burst=LIME)
    shot(s, "oval", 130, 690, 200, 200, b.SAWALA_SHOTS[1], rot=4)
    shot(s, "snip", 360, 690, 300, 200, b.SAWALA_SHOTS[2], rot=-3)
    hy = s.head(730, 154, b.SAWALA_TITLE, font=HEAD, size=42, color=BLACK, max_w=1000,
                one_line=True, gap=12)
    y = bub(s, 730, hy, 1050, b.SAWALA_BODY, size=14, fill=WHITE)
    y = s.head(730, y + 6, "MY ROLE", font=MONO, size=13, color=BLACK, tracking=3,
               gap=14)
    x = 730
    for i, t in enumerate(b.SAWALA_TAGS):
        if i == 3:
            x, y = 730, y + 62
        x += stamp(s, x, y, t, fill=[PINK, LIME, YEL, BLUE, GREEN, RED][i],
                   size=11) + 12
    shot(s, "rrect", 1330, 690, 440, 200, b.SAWALA_SHOTS[3], rot=3)

    # 06 · content in practice
    s = deck.new(); frame(s, "content in practice", b.PRACTICE_TITLE.lower())
    kinds = ["arch", "oval", "snip", "hex", "rrect", "oct"]
    for i, (lab, sub) in enumerate(b.PRACTICE):
        x = 104 + (i % 3) * 600
        y = 176 + (i // 3) * 384
        s.rrect(x, y, 570, 350, fill=WHITE, line=BLACK, lw=4, radius=0.08)
        s.rect(x, y, 570, 56, fill=[PINK, LIME, BLUE][i % 3])
        s.rect(x, y + 53, 570, 4, fill=BLACK)
        s.text(x + 20, y, 530, 56, lab, font=MONO, size=12.5,
               color=WHITE if i % 3 != 1 else BLACK, anchor=MSO_ANCHOR.MIDDLE,
               tracking=2)
        shot(s, kinds[i], x + 24, y + 78, 250, 244, "", rot=(-3, 2)[i % 2])
        s.para(x + 300, y + 92, 250, sub, font=BODY, size=12, color=BLACK, spacing=1.6)
        s.text(x + 300, y + 264, 250, 40, "0%d" % (i + 1), font=HEAD, size=22,
               color="C9C9C9")

    # 07 · stretch for stray
    s = deck.new(); frame(s, b.STRAY_TITLE.lower(), b.STRAY_SUB.lower())
    shot(s, "rrect", 110, 180, 460, 560, b.STRAY_SHOTS[0], rot=-5, burst=LIME)
    hy = s.head(630, 152, b.STRAY_TITLE, font=HEAD, size=46, color=BLACK, max_w=1120,
                one_line=True, gap=12)
    y = bub(s, 630, hy, 1100, b.STRAY_BODY, size=15, fill=YEL)
    y = s.head(630, y + 4, "MY CONTRIBUTION", font=MONO, size=13, color=BLACK,
               tracking=3, gap=16)
    for i, it in enumerate(b.STRAY_LIST):
        ry = y + i * 58
        s.rrect(630, ry, 620, 48, fill=WHITE, line=BLACK, lw=3, radius=0.4)
        s.oval(648, ry + 12, 24, 24, fill=[PINK, LIME, BLUE, YEL, GREEN, RED][i],
               line=BLACK, lw=2)
        s.text(690, ry, 520, 48, it, font=BODY, size=12, color=BLACK,
               anchor=MSO_ANCHOR.MIDDLE)
    shot(s, "snip", 1320, 560, 430, 300, b.STRAY_SHOTS[1], rot=4, burst=PINK)
    shot(s, "oval", 130, 770, 180, 120, b.STRAY_SHOTS[2], rot=3)

    # 08 · behind the content
    s = deck.new(); frame(s, b.BEHIND_TITLE.lower(), "process, unfiltered")
    x = 104
    for i, step in enumerate(b.BEHIND_STEPS):
        x += stamp(s, x, 168, step, fill=[PINK, LIME, BLUE, YEL, RED][i], size=12) + 14
    kinds = ["snip", "oval", "rrect", "hex", "arch", "snip1", "oct", "rrect"]
    for i, (cap, step) in enumerate(b.BEHIND_SHOTS):
        cx = 104 + (i % 4) * 436
        cy = 258 + (i // 4) * 330
        s.rrect(cx, cy, 404, 300, fill=WHITE, line=BLACK, lw=4, radius=0.07)
        shot(s, kinds[i], cx + 22, cy + 20, 360, 200, cap, rot=(-3, 2, -2, 3)[i % 4])
        s.text(cx + 24, cy + 240, 300, 42, step, font=MONO, size=12, color=BLACK,
               tracking=2, anchor=MSO_ANCHOR.MIDDLE)

    # 09 · tools
    s = deck.new(); frame(s, b.TOOLS_TITLE.lower(), "what i build with")
    for i, (group, items) in enumerate(b.TOOLS):
        x = 104 + i * 600
        s.rrect(x, 176, 570, 420, fill=WHITE, line=BLACK, lw=4, radius=0.08)
        s.rect(x, 176, 570, 62, fill=[PINK, BLUE, LIME][i])
        s.rect(x, 235, 570, 4, fill=BLACK)
        s.text(x, 176, 570, 62, group, font=HEAD, size=24,
               color=WHITE if i != 2 else BLACK, align=PP_ALIGN.CENTER,
               anchor=MSO_ANCHOR.MIDDLE)
        for j, it in enumerate(items):
            ry = 262 + j * 104
            s.rrect(x + 28, ry, 514, 84, fill=SKY, line=BLACK, lw=2.5, radius=0.2)
            s.text(x + 56, ry, 460, 84, it, font=BODY, size=14, color=BLACK,
                   anchor=MSO_ANCHOR.MIDDLE)
    bub(s, 104, 636, 1180, b.TOOLS_NOTE, size=14, fill=YEL)
    shot(s, "rrect", 1340, 640, 430, 250, "photo", rot=4, burst=LIME)

    # 10 · closing
    s = deck.new(); frame(s, "let's talk", "always open")
    y = bub(s, 110, 180, 900, "thanks 4 scrolling!!", size=17)
    hy = s.head(108, y, b.END_TITLE[0], font=HEAD, size=42, color=BLACK, max_w=1000,
                one_line=True, gap=0)
    hy = s.head(108, hy, b.END_TITLE[1], font=HEAD, size=42, color=BLACK, max_w=1000,
                one_line=True, gap=26)
    hy = s.head(110, hy, b.NAME, font=MONO, size=14, color=BLACK, tracking=3, gap=8)
    s.text(110, hy, 900, 40, b.END_ROLE + "  ·  " + b.END_SUB, font=BODY, size=12,
           color="333333")
    for i, (lab, val) in enumerate(b.CONTACT):
        cy = 200 + i * 150
        s.rrect(1180, cy, 640, 120, fill=WHITE, line=BLACK, lw=4, radius=0.24)
        s.oval(1206, cy + 30, 58, 58, fill=[GREEN, RED, BLUE][i], line=BLACK, lw=3)
        s.text(1294, cy + 22, 460, 38, lab, font=MONO, size=12.5, color=BLACK,
               tracking=2)
        s.text(1294, cy + 62, 480, 38, val, font=BODY, size=13.5, color="333333")
    s.star(1060, 680, 170, fill=PINK, line=BLACK, lw=4, points=16, rot=16)
    s.text(1060, 680, 170, 170, "HI!", font=HEAD, size=32, color=BLACK,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    shot(s, "rrect", 1300, 680, 400, 210, "photo", rot=4)
    return deck
