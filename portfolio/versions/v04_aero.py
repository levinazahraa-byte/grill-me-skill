# -*- coding: utf-8 -*-
"""PORTFOLIO 04 — AERO.  Reference 4.

Frutiger Aero: chartreuse-to-aqua gradients, glossy rounded panels tiled into
dense app modules, a status bar and a dock. Techy, bright, optimistic.
"""
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import deckkit as dk
import content as c

LIME, CHART, AQUA, BLUE, DEEP = "D7F062", "B8E62E", "7FD4F7", "2C7FC9", "0E3B6B"
WHITE, GLASS, INK = "FFFFFF", "FFFFFF", "10283F"
HEAD, BODY, LABEL = "Nunito", "Nunito", "Poppins"

def panel(s, x, y, w, h, title=None, tint=WHITE, radius=0.06, accent=AQUA, gloss=True,
          title_color=None):
    s.rrect(x, y, w, h, fill=tint, radius=radius,
            shadow={"blur": 30, "dist": 10, "alpha": 22, "color": "15507F"})
    if gloss:
        s.rrect(x + 6, y + 5, w - 12, h * 0.42, fill="FFFFFF", radius=radius,
                alpha=38)
    top = y
    if title:
        s.rrect(x, y, w, 52, fill=accent, radius=radius * 1.6)
        s.rect(x, y + 26, w, 26, fill=accent)
        s.rrect(x + 6, y + 4, w - 12, 22, fill="FFFFFF", radius=0.5, alpha=42)
        s.text(x + 22, y, w - 44, 52, title, font=LABEL, size=12.5, bold=True,
               color=title_color or WHITE, anchor=MSO_ANCHOR.MIDDLE, tracking=2)
        top = y + 52
    return x, top, w, h - (top - y)

def statusbar(s):
    s.rect(0, 0, 1920, 46, fill=DEEP)
    s.text(28, 0, 700, 46, "zahra levina  ·  portfolio 2026", font=LABEL, size=12,
           bold=True, color=LIME, anchor=MSO_ANCHOR.MIDDLE, tracking=2)
    for i in range(5):
        s.rrect(1620 + i * 34, 15, 18, 16, fill=AQUA, radius=0.3)
    s.text(1740, 0, 150, 46, "10:30 PM", font=LABEL, size=11.5, color=WHITE,
           anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)

def dock(s, items=6, y=990):
    s.rrect(620, y, 680, 74, fill=WHITE, radius=0.3, alpha=72,
            shadow={"blur": 26, "dist": 8, "alpha": 20, "color": "15507F"})
    cols = [LIME, AQUA, "8ED9A0", "F7D046", "F79BC4", BLUE]
    for i in range(items):
        s.rrect(648 + i * 108, y + 12, 50, 50, fill=cols[i % 6], radius=0.28)

def bg(s):
    s.bg(grad=(LIME, AQUA), angle=45)
    s.oval(-160, 620, 900, 620, fill=WHITE, alpha=26)
    s.oval(1320, -220, 820, 620, fill=WHITE, alpha=22)
    statusbar(s)

def build(deck):
    # 1 · cover
    s = deck.new(); bg(s)
    x, y, w, h = panel(s, 90, 120, 1000, 560, "welcome.app", accent=BLUE)
    s.text(x + 50, y + 34, 900, 70, "hi, i'm", font=HEAD, size=28, color=BLUE)
    s.text(x + 46, y + 86, 900, 180, "ZAHRA", font=HEAD, size=76, bold=True, color=DEEP)
    s.text(x + 46, y + 258, 900, 140, "LEVINA", font=HEAD, size=58, bold=True, color=BLUE)
    s.text(x + 50, y + 392, 800, 80, c.DISCIPLINES, font=BODY, size=14, color=INK,
           spacing=1.4)
    x2, y2, w2, h2 = panel(s, 1130, 120, 700, 560, "portrait.jpg", accent=AQUA,
                           title_color=DEEP)
    s.photo(x2 + 30, y2 + 26, w2 - 60, h2 - 60, "drop portrait", fill="EAF6FF",
            line="9FC9E4", radius=0.04, label_color="5B87A8")
    x3, y3, w3, h3 = panel(s, 90, 706, 620, 240, "now playing", accent=LIME,
                           title_color=DEEP)
    s.text(x3 + 34, y3 + 26, 520, 44, "portfolio_2026.mp4", font=BODY, size=16, bold=True,
           color=DEEP)
    s.rrect(x3 + 34, y3 + 86, 520, 14, fill="D8E8F2", radius=0.5)
    s.rrect(x3 + 34, y3 + 86, 320, 14, fill=BLUE, radius=0.5)
    s.text(x3 + 34, y3 + 116, 520, 40, "creative · content · marketing", font=BODY,
           size=12, color="53728B")
    x4, y4, w4, h4 = panel(s, 750, 706, 1080, 240, "contact.app", accent=BLUE)
    for i, (lab, val) in enumerate(c.CONTACT):
        cx = x4 + 40 + i * 340
        s.rrect(cx, y4 + 34, 310, 110, fill="EAF6FF", radius=0.16)
        s.text(cx, y4 + 52, 310, 34, lab, font=LABEL, size=12, bold=True, color=BLUE,
               align=PP_ALIGN.CENTER)
        s.text(cx, y4 + 92, 310, 34, val, font=BODY, size=11.5, color=INK,
               align=PP_ALIGN.CENTER)

    # 2 · about
    s = deck.new(); bg(s)
    x, y, w, h = panel(s, 90, 120, 1120, 826, "about_me.app", accent=BLUE)
    s.text(x + 50, y + 40, 900, 110, c.ABOUT_TITLE, font=HEAD, size=46, bold=True,
           color=DEEP)
    s.rrect(x + 52, y + 178, 200, 12, fill=LIME, radius=0.5)
    s.text(x + 50, y + 220, 1000, 520, c.ABOUT, font=BODY, size=14, color=INK,
           spacing=1.85, after=20)
    x2, y2, w2, h2 = panel(s, 1250, 120, 580, 520, "me.jpg", accent=AQUA,
                           title_color=DEEP)
    s.photo(x2 + 26, y2 + 24, w2 - 52, h2 - 54, "drop photo", fill="EAF6FF",
            line="9FC9E4", radius=0.04, label_color="5B87A8")
    x3, y3, w3, h3 = panel(s, 1250, 666, 580, 280, "quick facts", accent=LIME,
                           title_color=DEEP)
    for i, t in enumerate(c.DISCIPLINE_LIST):
        s.rrect(x3 + 30, y3 + 22 + i * 52, w3 - 60, 42, fill="EAF6FF", radius=0.3)
        s.text(x3 + 58, y3 + 22 + i * 52, 400, 42, t, font=BODY, size=13, color=INK,
               anchor=MSO_ANCHOR.MIDDLE)

    # 3 · what i do
    s = deck.new(); bg(s)
    s.text(90, 70, 900, 100, c.DO_TITLE, font=HEAD, size=42, bold=True, color=DEEP)
    for i, (title, sub) in enumerate(c.DO):
        px_ = 90 + (i % 2) * 890
        py_ = 220 + (i // 2) * 382
        x, y, w, h = panel(s, px_, py_, 840, 350, "0%d · module" % (i + 1),
                           accent=[BLUE, AQUA, LIME, "8ED9A0"][i],
                           title_color=DEEP if i >= 1 else WHITE)
        s.rrect(x + 36, y + 34, 96, 96, fill=[BLUE, AQUA, CHART, "8ED9A0"][i],
                radius=0.26)
        s.text(x + 36, y + 56, 96, 60, "0%d" % (i + 1), font=HEAD, size=30, bold=True,
               color=WHITE, align=PP_ALIGN.CENTER)
        s.text(x + 164, y + 40, 620, 70, title, font=HEAD, size=25, bold=True, color=DEEP)
        s.text(x + 166, y + 112, 620, 110, sub, font=BODY, size=13, color="46688A",
               spacing=1.55)
    dock(s)

    # 4 · experience
    s = deck.new(); bg(s)
    x, y, w, h = panel(s, 90, 108, 1240, 838, c.EXP_TITLE.lower(), accent=BLUE)
    for i, (org, role) in enumerate(c.EXP):
        ry = y + 34 + i * 148
        s.rrect(x + 34, ry, w - 68, 128, fill="EAF6FF", radius=0.14)
        s.rrect(x + 60, ry + 26, 76, 76, fill=[BLUE, AQUA, CHART, "8ED9A0", "F79BC4"][i],
                radius=0.24)
        s.text(x + 170, ry + 24, 800, 48, org, font=HEAD, size=22, bold=True, color=DEEP)
        s.text(x + 172, ry + 72, 800, 38, role, font=BODY, size=13, color="46688A")
        s.text(x + w - 130, ry, 80, 128, "0%d" % (i + 1), font=LABEL, size=14, bold=True,
               color="9DBDD6", anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)
    x2, y2, w2, h2 = panel(s, 1370, 108, 460, 500, "folders", accent=LIME,
                           title_color=DEEP)
    for i in range(5):
        s.rrect(x2 + 30, y2 + 26 + i * 78, w2 - 60, 62, fill="EAF6FF", radius=0.24)
        s.rrect(x2 + 52, y2 + 40 + i * 78, 34, 34, fill=AQUA, radius=0.3)
        s.text(x2 + 106, y2 + 26 + i * 78, 300, 62, c.EXP[i][0].split()[0],
               font=BODY, size=12.5, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    x3, y3, w3, h3 = panel(s, 1370, 636, 460, 310, "photo", accent=AQUA,
                           title_color=DEEP)
    s.photo(x3 + 26, y3 + 24, w3 - 52, h3 - 54, "drop photo", fill="EAF6FF",
            line="9FC9E4", radius=0.05, label_color="5B87A8")

    # 5 · sawala space
    s = deck.new(); bg(s)
    x, y, w, h = panel(s, 90, 108, 760, 838, "sawala_space.jpg", accent=AQUA,
                       title_color=DEEP)
    s.photo(x + 30, y + 26, w - 60, 520, "drop photo", fill="EAF6FF", line="9FC9E4",
            radius=0.04, label_color="5B87A8")
    s.photo(x + 30, y + 566, 320, 200, "event", fill="EAF6FF", line="9FC9E4",
            radius=0.05, label_color="5B87A8")
    s.photo(x + 370, y + 566, 320, 200, "community", fill="EAF6FF", line="9FC9E4",
            radius=0.05, label_color="5B87A8")
    x2, y2, w2, h2 = panel(s, 890, 108, 940, 560, "project.app", accent=BLUE)
    s.text(x2 + 44, y2 + 34, 800, 100, c.SAWALA_TITLE, font=HEAD, size=40, bold=True,
           color=DEEP)
    s.text(x2 + 46, y2 + 158, 800, 44, c.SAWALA_SUB, font=BODY, size=15, color=BLUE)
    s.rrect(x2 + 46, y2 + 212, 160, 10, fill=LIME, radius=0.5)
    s.text(x2 + 46, y2 + 244, 830, 200, c.SAWALA_BODY, font=BODY, size=13, color=INK,
           spacing=1.75)
    x3, y3, w3, h3 = panel(s, 890, 696, 940, 250, "my role", accent=LIME,
                           title_color=DEEP)
    px2, py2 = x3 + 34, y3 + 30
    for i, r in enumerate(c.SAWALA_ROLE):
        if i == 3:
            px2, py2 = x3 + 34, y3 + 96
        px2 += s.pill(px2, py2, r, size=12, pad=22, h=52, fill="EAF6FF", color=DEEP,
                      font=BODY, tracking=1, radius=0.3) + 14

    # 6 · selected works
    s = deck.new(); bg(s)
    s.text(90, 68, 1000, 100, c.WORKS_TITLE, font=HEAD, size=38, bold=True, color=DEEP)
    s.text(92, 174, 1000, 44, c.WORKS_BODY, font=BODY, size=11.5, color="2B5474")
    x0 = 1150
    for i, tag in enumerate(c.WORKS_TAGS):
        x0 += s.pill(x0, 84, tag, size=11, pad=14, h=44, fill=WHITE, color=DEEP,
                     font=BODY, tracking=1, radius=0.3) + 8
    for i, cap in enumerate(c.WORKS_CAPS):
        gx = 90 + (i % 4) * 452
        gy = 250 + (i // 4) * 352
        x, y, w, h = panel(s, gx, gy, 420, 320, cap,
                           accent=[BLUE, AQUA, LIME, "8ED9A0"][i % 4],
                           title_color=DEEP if i % 4 >= 1 else WHITE)
        s.photo(x + 22, y + 20, w - 44, h - 46, "drop photo", fill="EAF6FF",
                line="9FC9E4", radius=0.05, label_color="5B87A8")

    # 7 · stretch for stray
    s = deck.new(); bg(s)
    x, y, w, h = panel(s, 90, 108, 620, 838, "poster.jpg", accent=AQUA, title_color=DEEP)
    s.photo(x + 28, y + 26, w - 56, h - 56, "drop poster", fill="EAF6FF", line="9FC9E4",
            radius=0.04, label_color="5B87A8")
    x2, y2, w2, h2 = panel(s, 750, 108, 1080, 420, "event.app", accent=BLUE)
    s.text(x2 + 44, y2 + 30, 600, 44, c.STRAY_SUB, font=LABEL, size=13, bold=True,
           color=BLUE, tracking=3)
    s.text(x2 + 42, y2 + 76, 1000, 100, c.STRAY_TITLE, font=HEAD, size=38, bold=True,
           color=DEEP)
    s.rrect(x2 + 46, y2 + 190, 160, 10, fill=LIME, radius=0.5)
    s.text(x2 + 44, y2 + 222, 900, 110, c.STRAY_BODY, font=BODY, size=14, color=INK,
           spacing=1.6)
    x3, y3, w3, h3 = panel(s, 750, 556, 660, 390, "my contribution", accent=LIME,
                           title_color=DEEP)
    for i, it in enumerate(c.STRAY_LIST):
        ry = y3 + 26 + i * 60
        s.rrect(x3 + 30, ry, w3 - 60, 48, fill="EAF6FF", radius=0.3)
        s.oval(x3 + 50, ry + 14, 20, 20, fill=BLUE)
        s.text(x3 + 90, ry, 480, 48, it, font=BODY, size=12.5, color=INK,
               anchor=MSO_ANCHOR.MIDDLE)
    x4, y4, w4, h4 = panel(s, 1450, 556, 380, 390, "docs", accent=AQUA, title_color=DEEP)
    s.photo(x4 + 24, y4 + 22, w4 - 48, 140, "documentation", fill="EAF6FF",
            line="9FC9E4", radius=0.06, label_color="5B87A8")
    s.photo(x4 + 24, y4 + 178, w4 - 48, 140, "social post", fill="EAF6FF",
            line="9FC9E4", radius=0.06, label_color="5B87A8")

    # 8 · beyond
    s = deck.new(); bg(s)
    s.text(90, 68, 1100, 100, c.BEYOND_TITLE, font=HEAD, size=38, bold=True, color=DEEP)
    s.text(92, 178, 1400, 44, c.BEYOND_BODY, font=BODY, size=12.5, color="2B5474")
    for i, (title, sub) in enumerate(c.BEYOND):
        x, y, w, h = panel(s, 90 + i * 590, 252, 560, 548,
                           ["organisation", "arts", "academic"][i],
                           accent=[BLUE, AQUA, LIME][i],
                           title_color=DEEP if i >= 1 else WHITE)
        s.rrect(x + 36, y + 34, 90, 90, fill=[BLUE, AQUA, CHART][i], radius=0.26)
        s.text(x + 36, y + 56, 90, 50, "0%d" % (i + 1), font=HEAD, size=26, bold=True,
               color=WHITE, align=PP_ALIGN.CENTER)
        s.text(x + 36, y + 160, w - 72, 140, title, font=HEAD, size=24, bold=True,
               color=DEEP, spacing=1.3)
        s.text(x + 38, y + 306, w - 76, 140, sub, font=BODY, size=13, color="46688A",
               spacing=1.6)
    dock(s, y=846)

    # 9 · skills
    s = deck.new(); bg(s)
    s.text(90, 68, 900, 100, c.SKILLS_TITLE, font=HEAD, size=38, bold=True, color=DEEP)
    for i, (title, items) in enumerate(c.SKILLS):
        x, y, w, h = panel(s, 90 + i * 890, 200, 840, 430, title.lower(),
                           accent=[BLUE, AQUA][i], title_color=DEEP if i else WHITE)
        for j, it in enumerate(items):
            ry = y + 28 + j * 88
            s.rrect(x + 32, ry, w - 64, 72, fill="EAF6FF", radius=0.2)
            s.text(x + 66, ry, 400, 72, it, font=BODY, size=14, color=INK,
                   anchor=MSO_ANCHOR.MIDDLE)
            s.rrect(x + 500, ry + 30, 260, 14, fill="D8E8F2", radius=0.5)
            s.rrect(x + 500, ry + 30, 260 - j * 22, 14, fill=[BLUE, AQUA][i], radius=0.5)
    x, y, w, h = panel(s, 90, 664, 1740, 250, "tools", accent=LIME, title_color=DEEP)
    px2, py2 = x + 36, y + 32
    for i, t in enumerate(c.TOOLS):
        if i == 4:
            px2, py2 = x + 36, y + 106
        px2 += s.pill(px2, py2, t, size=12.5, pad=24, h=58, fill="EAF6FF", color=DEEP,
                      font=BODY, tracking=1, radius=0.3) + 16
    dock(s, y=940)

    # 10 · contact
    s = deck.new(); bg(s)
    x, y, w, h = panel(s, 420, 180, 1080, 700, "share.app", accent=BLUE)
    s.oval(x + w / 2 - 60, y + 44, 120, 120, fill=AQUA)
    s.text(x, y + 186, w, 100, c.END_TITLE.replace(".", ""), font=HEAD, size=40,
           bold=True, color=DEEP, align=PP_ALIGN.CENTER)
    s.text(x + 140, y + 296, w - 280, 120, c.END_BODY, font=BODY, size=13.5, color=INK,
           align=PP_ALIGN.CENTER, spacing=1.7)
    for i, (lab, val) in enumerate(c.CONTACT):
        cx = x + 60 + i * 330
        s.rrect(cx, y + 434, 300, 120, fill="EAF6FF", radius=0.18)
        s.text(cx, y + 456, 300, 34, lab, font=LABEL, size=12.5, bold=True, color=BLUE,
               align=PP_ALIGN.CENTER)
        s.text(cx, y + 498, 300, 34, val, font=BODY, size=11.5, color=INK,
               align=PP_ALIGN.CENTER)
    s.rrect(x + 300, y + 586, 480, 66, fill=LIME, radius=0.3)
    s.text(x + 300, y + 586, 480, 66, "Accept", font=HEAD, size=20, bold=True,
           color=DEEP, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    dock(s)
    return deck
