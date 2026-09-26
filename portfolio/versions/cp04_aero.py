# -*- coding: utf-8 -*-
"""VERSION 04 — AERO.  Reference 4.

Frutiger Aero: chartreuse-to-aqua gradients, glossy rounded modules tiled
densely, a status bar and a dock. Techy, bright, optimistic.
"""
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import deckkit as dk
import brief as b

LIME, CHART, AQUA, BLUE, DEEP = "D7F062", "B8E62E", "7FD4F7", "2C7FC9", "0E3B6B"
WHITE, INK, PALE = "FFFFFF", "10283F", "EAF6FF"
HEAD, BODY, LABEL = "Nunito", "Nunito", "Poppins"

def ground(s):
    s.bg(grad=(LIME, AQUA), angle=45)
    s.oval(-180, 600, 900, 620, fill=WHITE, alpha=24)
    s.oval(1340, -220, 820, 600, fill=WHITE, alpha=20)
    s.rect(0, 0, 1920, 44, fill=DEEP)
    s.text(26, 0, 1400, 44, "zahra levina  ·  content production portfolio 2026",
           font=LABEL, size=11, bold=True, color=LIME, anchor=MSO_ANCHOR.MIDDLE,
           tracking=2, wrap_text=False)
    for i in range(5):
        s.rrect(1630 + i * 32, 14, 16, 15, fill=AQUA, radius=0.3)
    s.text(1760, 0, 134, 44, "10:30 PM", font=LABEL, size=11, color=WHITE,
           anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)

def panel(s, x, y, w, h, title=None, accent=AQUA, tint=WHITE, title_color=None,
          radius=0.06):
    s.rrect(x, y, w, h, fill=tint, radius=radius,
            shadow={"blur": 28, "dist": 9, "alpha": 20, "color": "15507F"})
    s.rrect(x + 6, y + 5, w - 12, h * 0.4, fill=WHITE, radius=radius, alpha=36)
    top = y
    if title:
        s.rrect(x, y, w, 48, fill=accent, radius=radius * 1.7)
        s.rect(x, y + 24, w, 24, fill=accent)
        s.rrect(x + 6, y + 4, w - 12, 20, fill=WHITE, radius=0.5, alpha=40)
        s.text(x + 20, y, w - 40, 48, title, font=LABEL, size=12, bold=True,
               color=title_color or WHITE, anchor=MSO_ANCHOR.MIDDLE, tracking=2)
        top = y + 48
    return x, top, w, h - (top - y)

def dock(s, y=986, n=6):
    s.rrect(660, y, 600, 68, fill=WHITE, radius=0.3, alpha=70,
            shadow={"blur": 24, "dist": 8, "alpha": 18, "color": "15507F"})
    cols = [LIME, AQUA, "8ED9A0", "F7D046", "F79BC4", BLUE]
    for i in range(n):
        s.rrect(686 + i * 96, y + 11, 46, 46, fill=cols[i % 6], radius=0.28)

def shot(s, kind, x, y, w, h, label="", rot=0):
    return s.cut(kind, x, y, w, h, label, fill=PALE, line="9FC9E4", lw=2.5, rot=rot,
                 radius=0.08 if kind in ("rrect", "arch") else None,
                 label_color="5B87A8", size=9.5, font=BODY)

def build(deck):
    # 01 · cover
    s = deck.new(); ground(s)
    x, y, w, h = panel(s, 80, 96, 980, 610, "welcome.app", accent=BLUE)
    ty = s.head(x + 44, y + 28, b.KICKER[0], font=LABEL, size=13, bold=True, color=BLUE,
                tracking=4, gap=10)
    ty = s.head(x + 42, ty, "CONTENT", font=HEAD, size=50, bold=True, color=DEEP, gap=0)
    ty = s.head(x + 42, ty, "PRODUCTION", font=HEAD, size=50, bold=True, color=BLUE,
                max_w=880, one_line=True, gap=0)
    ty = s.head(x + 42, ty, "PORTFOLIO", font=HEAD, size=36, bold=True, color=DEEP,
                gap=16)
    s.para(x + 44, ty, 820, b.TAGLINE, font=BODY, size=13, color=INK, spacing=1.5)
    x2, y2, w2, h2 = panel(s, 1100, 96, 740, 610, "portrait.jpg", accent=AQUA,
                           title_color=DEEP)
    shot(s, "arch", x2 + 30, y2 + 24, w2 - 60, h2 - 54, "drop portrait")
    x3, y3, w3, h3 = panel(s, 80, 730, 600, 212, "name", accent=LIME, title_color=DEEP)
    s.head(x3 + 34, y3 + 22, b.NAME.title(), font=HEAD, size=30, bold=True, color=DEEP)
    s.para(x3 + 36, y3 + 90, 520, b.END_ROLE + " · " + b.END_SUB, font=BODY, size=12,
           color="46688A", spacing=1.5)
    x4, y4, w4, h4 = panel(s, 720, 730, 1120, 212, "contact.app", accent=BLUE)
    for i, (lab, val) in enumerate(b.CONTACT):
        cx = x4 + 36 + i * 356
        s.rrect(cx, y4 + 18, 326, 100, fill=PALE, radius=0.16)
        s.text(cx, y4 + 32, 326, 30, lab, font=LABEL, size=12, bold=True, color=BLUE,
               align=PP_ALIGN.CENTER)
        s.text(cx, y4 + 68, 326, 30, val, font=BODY, size=11, color=INK,
               align=PP_ALIGN.CENTER)

    # 02 · about
    s = deck.new(); ground(s)
    x, y, w, h = panel(s, 80, 106, 1120, 836, "about_me.app", accent=BLUE)
    ty = s.head(x + 44, y + 30, b.ABOUT_TITLE, font=HEAD, size=46, bold=True, color=DEEP,
                max_w=900, one_line=True, gap=16)
    s.rrect(x + 46, ty, 190, 11, fill=LIME, radius=0.5)
    s.para(x + 44, ty + 32, 1020, b.ABOUT, font=BODY, size=14, color=INK, spacing=1.85,
           after=20, max_h=440)
    x2, y2, w2, h2 = panel(s, 1240, 106, 600, 470, "me.jpg", accent=AQUA,
                           title_color=DEEP)
    shot(s, "arch", x2 + 26, y2 + 22, w2 - 52, h2 - 50, "drop photo")
    x3, y3, w3, h3 = panel(s, 1240, 602, 600, 340, "what i do", accent=LIME,
                           title_color=DEEP)
    for i, t in enumerate(["content + social", "visual + design", "events + campaigns",
                           "editing + publishing"]):
        s.rrect(x3 + 28, y3 + 20 + i * 62, w3 - 56, 50, fill=PALE, radius=0.3)
        s.text(x3 + 56, y3 + 20 + i * 62, 440, 50, t, font=BODY, size=12.5, color=INK,
               anchor=MSO_ANCHOR.MIDDLE)

    # 03 · from idea to publish
    s = deck.new(); ground(s)
    y = s.head(80, 66, b.FLOW_TITLE, font=HEAD, size=44, bold=True, color=DEEP,
               max_w=1100, one_line=True, gap=22)
    cols = [BLUE, AQUA, CHART, "8ED9A0", BLUE, AQUA, CHART]
    for i, step in enumerate(b.FLOW):
        px_ = 80 + i * 254
        x, yy, w, h = panel(s, px_, y, 234, 200, "0%d" % (i + 1), accent=cols[i],
                            title_color=DEEP if i in (2, 3, 6) else WHITE)
        s.rrect(x + 70, yy + 22, 94, 68, fill=cols[i], radius=0.22)
        s.text(x, yy + 104, w, 50, step, font=HEAD, size=17, bold=True, color=DEEP,
               align=PP_ALIGN.CENTER)
    y += 236
    x, yy, w, h = panel(s, 80, y, 1080, 250, "note", accent=BLUE)
    s.para(x + 34, yy + 22, 1000, b.FLOW_NOTE, font=BODY, size=13.5, color=INK,
           spacing=1.7, after=12, max_h=170)
    x2, y2, w2, h2 = panel(s, 1200, y, 640, 250, "camera roll", accent=AQUA,
                           title_color=DEEP)
    shot(s, "rrect", x2 + 24, y2 + 20, 280, 150, "content prep")
    shot(s, "oval", x2 + 330, y2 + 20, 150, 150, "photo")
    shot(s, "snip", x2 + 500, y2 + 30, 120, 130, "photo", rot=5)
    dock(s)

    # 04 · content, in different forms
    s = deck.new(); ground(s)
    y = s.head(80, 64, b.FORMS_TITLE, font=HEAD, size=42, bold=True, color=DEEP,
               max_w=1200, one_line=True, gap=22)
    kinds = ["oval", "hex", "arch", "snip"]
    for i, (group, items) in enumerate(b.FORMS):
        x, yy, w, h = panel(s, 80 + i * 460, y, 430, 660, group.lower(),
                            accent=[BLUE, AQUA, CHART, "8ED9A0"][i],
                            title_color=DEEP if i >= 1 else WHITE)
        shot(s, kinds[i], x + 40, yy + 22, w - 80, 190, "")
        for j, it in enumerate(items):
            ry = yy + 236 + j * 82
            s.rrect(x + 28, ry, w - 56, 66, fill=PALE, radius=0.18)
            s.text(x + 56, ry, w - 100, 66, it, font=BODY, size=12.5, color=INK,
                   anchor=MSO_ANCHOR.MIDDLE)

    # 05 · sawala space
    s = deck.new(); ground(s)
    x, y, w, h = panel(s, 80, 96, 720, 846, "sawala_space.jpg", accent=AQUA,
                       title_color=DEEP)
    shot(s, "arch", x + 28, y + 22, w - 56, 480, b.SAWALA_SHOTS[0])
    shot(s, "rrect", x + 28, y + 520, 300, 180, b.SAWALA_SHOTS[1])
    shot(s, "oval", x + 350, y + 520, 180, 180, b.SAWALA_SHOTS[2])
    shot(s, "snip", x + 550, y + 530, 140, 160, b.SAWALA_SHOTS[3], rot=4)
    x2, y2, w2, h2 = panel(s, 840, 96, 1000, 520, "project.app", accent=BLUE)
    ty = s.head(x2 + 40, y2 + 26, b.SAWALA_TITLE, font=HEAD, size=42, bold=True,
                color=DEEP, max_w=880, one_line=True, gap=10)
    ty = s.head(x2 + 42, ty, b.SAWALA_SUB, font=BODY, size=13.5, color=BLUE, gap=14)
    s.rrect(x2 + 42, ty, 150, 10, fill=LIME, radius=0.5)
    s.para(x2 + 40, ty + 26, 900, b.SAWALA_BODY, font=BODY, size=12.5, color=INK,
           spacing=1.7, max_h=200)
    x3, y3, w3, h3 = panel(s, 840, 646, 1000, 296, "my role", accent=LIME,
                           title_color=DEEP)
    px2, py2 = x3 + 32, y3 + 28
    for i, t in enumerate(b.SAWALA_TAGS):
        if i == 3:
            px2, py2 = x3 + 32, y3 + 110
        px2 += s.pill(px2, py2, t, size=11.5, pad=20, h=56, fill=PALE, color=DEEP,
                      font=BODY, tracking=2, radius=0.3) + 14
    shot(s, "rrect", x3 + 32, y3 + 192, 920, 76, b.SAWALA_SHOTS[4])

    # 06 · content in practice
    s = deck.new(); ground(s)
    y = s.head(80, 62, b.PRACTICE_TITLE, font=HEAD, size=36, bold=True, color=DEEP,
               max_w=1500, one_line=True, gap=20)
    kinds = ["arch", "oval", "snip", "hex", "rrect", "oct"]
    for i, (lab, sub) in enumerate(b.PRACTICE):
        px_ = 80 + (i % 3) * 600
        py_ = y + (i // 3) * 392
        x, yy, w, h = panel(s, px_, py_, 570, 360, lab.lower(),
                            accent=[BLUE, AQUA, CHART][i % 3],
                            title_color=DEEP if i % 3 else WHITE)
        shot(s, kinds[i], x + 26, yy + 20, 250, 240, "")
        s.para(x + 300, yy + 26, 250, sub, font=BODY, size=11.5, color="46688A",
               spacing=1.5, max_h=150)
        s.text(x + 300, yy + 200, 240, 40, "0%d" % (i + 1), font=LABEL, size=13,
               bold=True, color="9DBDD6")

    # 07 · stretch for stray
    s = deck.new(); ground(s)
    x, y, w, h = panel(s, 80, 96, 620, 846, "poster.jpg", accent=AQUA, title_color=DEEP)
    shot(s, "arch", x + 26, y + 22, w - 52, h - 50, b.STRAY_SHOTS[0])
    x2, y2, w2, h2 = panel(s, 740, 96, 1100, 420, "event.app", accent=BLUE)
    ty = s.head(x2 + 40, y2 + 24, b.STRAY_SUB, font=LABEL, size=12.5, bold=True,
                color=BLUE, tracking=3, gap=10)
    ty = s.head(x2 + 38, ty, b.STRAY_TITLE, font=HEAD, size=40, bold=True, color=DEEP,
                max_w=980, one_line=True, gap=14)
    s.rrect(x2 + 42, ty, 150, 10, fill=LIME, radius=0.5)
    s.para(x2 + 40, ty + 30, 980, b.STRAY_BODY, font=BODY, size=14, color=INK,
           spacing=1.6)
    x3, y3, w3, h3 = panel(s, 740, 546, 660, 396, "my contribution", accent=LIME,
                           title_color=DEEP)
    for i, it in enumerate(b.STRAY_LIST):
        ry = y3 + 20 + i * 52
        s.rrect(x3 + 26, ry, w3 - 52, 44, fill=PALE, radius=0.3)
        s.oval(x3 + 44, ry + 13, 18, 18, fill=BLUE)
        s.text(x3 + 80, ry, 480, 44, it, font=BODY, size=12, color=INK,
               anchor=MSO_ANCHOR.MIDDLE)
    x4, y4, w4, h4 = panel(s, 1440, 546, 400, 396, "docs", accent=AQUA, title_color=DEEP)
    shot(s, "rrect", x4 + 24, y4 + 20, w4 - 48, 150, b.STRAY_SHOTS[1])
    shot(s, "snip", x4 + 24, y4 + 186, w4 - 48, 130, b.STRAY_SHOTS[2])

    # 08 · behind the content
    s = deck.new(); ground(s)
    y = s.head(80, 62, b.BEHIND_TITLE, font=HEAD, size=40, bold=True, color=DEEP,
               max_w=1100, one_line=True, gap=16)
    px_ = 80
    for i, step in enumerate(b.BEHIND_STEPS):
        px_ += s.pill(px_, y, step, size=11.5, pad=20, h=52, fill=WHITE, color=DEEP,
                      font=LABEL, tracking=2, radius=0.3) + 14
    y += 74
    kinds = ["snip", "oval", "rrect", "hex", "arch", "snip1", "oct", "rrect"]
    for i, (cap, step) in enumerate(b.BEHIND_SHOTS):
        cx = 80 + (i % 4) * 452
        cy = y + (i // 4) * 270
        x, yy, w, h = panel(s, cx, cy, 420, 246, step.lower(),
                            accent=[BLUE, AQUA, CHART, "8ED9A0"][i % 4],
                            title_color=DEEP if i % 4 else WHITE)
        shot(s, kinds[i], x + 20, yy + 16, w - 40, h - 36, cap)

    # 09 · tools
    s = deck.new(); ground(s)
    y = s.head(80, 64, b.TOOLS_TITLE, font=HEAD, size=42, bold=True, color=DEEP,
               max_w=1100, one_line=True, gap=22)
    for i, (group, items) in enumerate(b.TOOLS):
        x, yy, w, h = panel(s, 80 + i * 600, y, 570, 440, group.lower(),
                            accent=[BLUE, AQUA, CHART][i],
                            title_color=DEEP if i else WHITE)
        for j, it in enumerate(items):
            ry = yy + 26 + j * 96
            s.rrect(x + 28, ry, w - 56, 78, fill=PALE, radius=0.2)
            s.rrect(x + 50, ry + 19, 40, 40, fill=[BLUE, AQUA, CHART][i], radius=0.24)
            s.text(x + 110, ry, w - 150, 78, it, font=BODY, size=13.5, color=INK,
                   anchor=MSO_ANCHOR.MIDDLE)
    ny = y + 470
    x, yy, w, h = panel(s, 80, ny, 1160, 942 - ny, "note", accent=LIME, title_color=DEEP)
    s.para(x + 32, yy + 20, 1080, b.TOOLS_NOTE, font=BODY, size=13.5, color=INK,
           spacing=1.6)
    x2, y2, w2, h2 = panel(s, 1280, ny, 560, 942 - ny, "exports", accent=AQUA,
                           title_color=DEEP)
    shot(s, "rrect", x2 + 24, y2 + 18, 240, 110, "photo")
    shot(s, "oval", x2 + 290, y2 + 18, 110, 110, "photo")
    shot(s, "snip", x2 + 416, y2 + 24, 120, 100, "photo", rot=4)
    dock(s)

    # 10 · closing
    s = deck.new(); ground(s)
    x, y, w, h = panel(s, 380, 150, 1160, 720, "share.app", accent=BLUE)
    s.oval(x + w / 2 - 54, y + 32, 108, 108, fill=AQUA)
    ty = s.head(x, y + 164, b.END_TITLE[0], font=HEAD, size=40, bold=True, color=DEEP,
                align=PP_ALIGN.CENTER, max_w=w, one_line=True, gap=2)
    ty = s.head(x, ty, b.END_TITLE[1], font=HEAD, size=40, bold=True, color=DEEP,
                align=PP_ALIGN.CENTER, max_w=w, gap=18)
    ty = s.head(x, ty, b.NAME.title(), font=HEAD, size=22, bold=True, color=BLUE,
                align=PP_ALIGN.CENTER, max_w=w, gap=8)
    ty = s.head(x, ty, b.END_ROLE + "  ·  " + b.END_SUB, font=BODY, size=12.5,
                color="46688A", align=PP_ALIGN.CENTER, max_w=w, gap=26)
    for i, (lab, val) in enumerate(b.CONTACT):
        cx = x + 56 + i * 350
        s.rrect(cx, ty, 320, 116, fill=PALE, radius=0.18)
        s.text(cx, ty + 22, 320, 32, lab, font=LABEL, size=12.5, bold=True, color=BLUE,
               align=PP_ALIGN.CENTER)
        s.text(cx, ty + 62, 320, 32, val, font=BODY, size=11.5, color=INK,
               align=PP_ALIGN.CENTER)
    dock(s)
    return deck
