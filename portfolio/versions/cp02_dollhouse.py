# -*- coding: utf-8 -*-
"""VERSION 02 — DOLLHOUSE.  Reference 2.

Y2K web boutique: a pastel storefront rendered as a portfolio. Announcement
banner, nav, window cards with title bars, sidebar widgets, pixel UI labels and
a taskbar. Dense and modular.
"""
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import deckkit as dk
import brief as b

BG, PINK, LILAC, MINT, VIOLET = "FFF0F7", "FF6FB5", "C9B6FF", "B9F0E4", "4A2E6B"
SKY, CREAM, MUTE = "DCEEFF", "FFFDF6", "8A76A8"
HEAD, UI, BODY = "Fredoka", "VT323", "Poppins"

def checker(s, x, y, w, cell=22, c1=VIOLET, c2="FFFFFF"):
    for i in range(int(w // cell)):
        s.rect(x + i * cell, y, cell, cell, fill=c1 if i % 2 == 0 else c2)

def chrome(s, tab="home"):
    s.bg(fill=BG)
    s.rect(0, 0, 1920, 34, fill=PINK)
    s.text(36, 0, 1300, 34, "NEW  ·  CONTENT PRODUCTION PORTFOLIO 2026  ·  SCROLL 4 MORE",
           font=UI, size=15, color="FFFFFF", anchor=MSO_ANCHOR.MIDDLE, tracking=2)
    s.text(1500, 0, 384, 34, "sign in     say hi     [ x ]", font=UI, size=15,
           color="FFFFFF", anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)
    s.text(44, 44, 460, 58, "zahra.house", font=HEAD, size=23, color=PINK, bold=True)
    for i, n in enumerate(["home", "about", "process", "work", "contact"]):
        fill = LILAC if n == tab else "FFFFFF"
        col = "FFFFFF" if n == tab else VIOLET
        s.pill(430 + i * 184, 48, n, size=11.5, pad=22, h=48, fill=fill, color=col,
               line=LILAC, font=BODY, tracking=1, width=172)
    s.rrect(1390, 48, 480, 48, fill="FFFFFF", line=LILAC, lw=1.5, radius=0.5)
    s.text(1418, 48, 420, 48, "search the site...", font=BODY, size=11.5, color="A796BC",
           anchor=MSO_ANCHOR.MIDDLE)
    checker(s, 0, 122, 1920, 18)
    s.rect(0, 1016, 1920, 64, fill=LILAC)
    s.pill(18, 1026, "start", size=13, pad=20, h=44, fill=MINT, color=VIOLET, font=BODY,
           tracking=1, width=124, radius=0.3)
    s.rrect(158, 1026, 340, 44, fill="FFFFFF", radius=0.3)
    s.text(180, 1026, 300, 44, "portfolio_2026.html", font=UI, size=16, color=VIOLET,
           anchor=MSO_ANCHOR.MIDDLE)
    s.rrect(1706, 1026, 196, 44, fill="FFFFFF", radius=0.3)
    s.text(1706, 1026, 196, 44, "10:30 PM", font=UI, size=16, color=VIOLET,
           anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

def card(s, x, y, w, h, title, bar=LILAC, body="FFFFFF"):
    s.rrect(x, y, w, h, fill=body, line=VIOLET, lw=1.5, radius=0.04)
    s.rect(x + 2, y + 2, w - 4, 38, fill=bar)
    s.text(x + 14, y + 2, w - 96, 38, title, font=UI, size=16, color="FFFFFF",
           anchor=MSO_ANCHOR.MIDDLE)
    for i in range(3):
        s.rect(x + w - 26 - i * 24, y + 13, 14, 14, fill="FFFFFF", line=VIOLET, lw=1)
    return x, y + 40, w, h - 40

def shot(s, kind, x, y, w, h, label="", rot=0):
    return s.cut(kind, x, y, w, h, label, fill=SKY, line=VIOLET, lw=2, rot=rot,
                 radius=0.12 if kind in ("rrect", "arch") else None,
                 label_color="6E86A8", size=9.5, font=BODY)

def build(deck):
    # 01 · cover
    s = deck.new(); chrome(s, "home")
    bx, by, bw, bh = card(s, 44, 162, 1160, 700, "welcome_2_my_world.html", bar=PINK)
    y = s.head(bx + 46, by + 30, "hi! i'm", font=HEAD, size=30, color=LILAC, gap=6)
    y = s.head(bx + 44, y, "zahra", font=HEAD, size=76, color=PINK, bold=True, gap=4)
    y = s.head(bx + 46, y, "levina", font=HEAD, size=38, color=VIOLET, gap=18)
    y = s.para(bx + 46, y, 520, b.TAGLINE, font=BODY, size=12.5, color=VIOLET,
               spacing=1.55, gap=22)
    y = s.head(bx + 46, y, "  ·  ".join(b.KICKER), font=UI, size=17, color=MUTE, gap=20)
    s.pill(bx + 46, y, "see my work →", size=13, pad=26, h=58, fill=PINK, color="FFFFFF",
           font=BODY, tracking=1, width=290, radius=0.3)
    s.pill(bx + 352, y, "about me", size=13, pad=26, h=58, fill="FFFFFF", color=VIOLET,
           line=LILAC, font=BODY, tracking=1, width=210, radius=0.3)
    shot(s, "arch", bx + 700, by + 34, 400, 500, "drop portrait")
    shot(s, "oval", bx + 620, by + 430, 170, 170, "photo")
    sx, sy, sw, sh = card(s, 1234, 162, 642, 330, "quick links", bar=MINT)
    for i, t in enumerate(["what i do", "selected work", "how i work", "say hi"]):
        s.rect(sx + 18, sy + 18 + i * 62, sw - 36, 50, fill="FFF7FC", line=LILAC, lw=1)
        s.text(sx + 40, sy + 18 + i * 62, 420, 50, t, font=BODY, size=12.5, color=VIOLET,
               anchor=MSO_ANCHOR.MIDDLE)
        s.text(sx + sw - 76, sy + 18 + i * 62, 40, 50, "›", font=BODY, size=17,
               color=PINK, anchor=MSO_ANCHOR.MIDDLE)
    mx, my, mw, mh = card(s, 1234, 512, 642, 350, "new message!", bar=PINK)
    s.heart(mx + 30, my + 30, 54, fill=PINK)
    s.para(mx + 104, my + 34, 480, "you have (1) new message — open to see what i make.",
           font=BODY, size=13, color=VIOLET, spacing=1.5)
    for i, (lab, val) in enumerate(b.CONTACT):
        s.text(mx + 30, my + 132 + i * 54, 200, 40, lab.lower(), font=UI, size=17,
               color=PINK, anchor=MSO_ANCHOR.MIDDLE)
        s.text(mx + 210, my + 132 + i * 54, 400, 40, val, font=BODY, size=11.5,
               color=VIOLET, anchor=MSO_ANCHOR.MIDDLE)

    # 02 · about
    s = deck.new(); chrome(s, "about")
    bx, by, bw, bh = card(s, 44, 162, 1160, 700, "about_zahra.txt", bar=LILAC)
    y = s.head(bx + 46, by + 26, b.ABOUT_TITLE.lower(), font=HEAD, size=44, color=PINK,
               bold=True, max_w=900, one_line=True, gap=14)
    s.rect(bx + 48, y, 220, 8, fill=MINT)
    s.para(bx + 46, y + 28, 1040, b.ABOUT, font=BODY, size=13.5, color=VIOLET,
           spacing=1.8, after=18, max_h=380)
    sx, sy, sw, sh = card(s, 1234, 162, 642, 430, "me.jpg", bar=PINK)
    shot(s, "arch", sx + 24, sy + 22, sw - 48, sh - 46, "drop photo")
    nx, ny, nw, nh = card(s, 1234, 612, 642, 250, "what i do all day", bar=MINT)
    for i, t in enumerate(["☆ create + edit content", "☆ design visual materials",
                           "☆ prepare + publish posts"]):
        s.text(nx + 26, ny + 16 + i * 52, 560, 46, t, font=BODY, size=12.5, color=VIOLET,
               anchor=MSO_ANCHOR.MIDDLE)

    # 03 · from idea to publish
    s = deck.new(); chrome(s, "process")
    y = s.head(44, 158, b.FLOW_TITLE.lower(), font=HEAD, size=42, color=PINK, bold=True,
               max_w=900, one_line=True, gap=8)
    y = s.para(46, y, 1100, b.FLOW_NOTE[0], font=BODY, size=13, color=VIOLET, gap=18)
    cols = [PINK, LILAC, MINT, SKY, PINK, LILAC, MINT]
    for i, step in enumerate(b.FLOW):
        x = 44 + i * 266
        cx, cy, cw, ch = card(s, x, y, 246, 200, "0%d" % (i + 1), bar=cols[i])
        s.rect(cx + 18, cy + 16, cw - 36, 74, fill=["FFE6F3", "F0EAFF", "E6FBF6",
                                                    "E8F5FF", "FFE6F3", "F0EAFF",
                                                    "E6FBF6"][i], line=LILAC, lw=1)
        s.text(cx, cy + 100, cw, 50, step, font=HEAD, size=19, color=VIOLET,
               align=PP_ALIGN.CENTER)
        if i < 6:
            s.text(x + 246, cy + 60, 22, 40, "›", font=BODY, size=18, color=PINK,
                   align=PP_ALIGN.CENTER)
    ny = y + 230
    nx, nyy, nw, nh = card(s, 44, ny, 1100, 210, "note.txt", bar=LILAC)
    s.para(nx + 26, nyy + 20, 1040, b.FLOW_NOTE[1], font=BODY, size=13.5, color=VIOLET,
           spacing=1.7, max_h=150)
    shot(s, "rrect", 1180, ny, 340, 210, "content prep")
    shot(s, "oval", 1550, ny, 200, 200, "photo")
    shot(s, "snip", 1770, ny + 20, 106, 170, "photo", rot=5)

    # 04 · content, in different forms
    s = deck.new(); chrome(s, "work")
    y = s.head(44, 158, b.FORMS_TITLE.lower(), font=HEAD, size=40, color=PINK, bold=True,
               max_w=1300, one_line=True, gap=16)
    kinds = ["oval", "hex", "arch", "snip"]
    for i, (group, items) in enumerate(b.FORMS):
        x = 44 + i * 462
        cx, cy, cw, ch = card(s, x, y, 436, 600, group.lower(),
                              bar=[PINK, LILAC, MINT, SKY][i])
        shot(s, kinds[i], cx + 30, cy + 20, cw - 60, 190, "")
        for j, it in enumerate(items):
            s.rect(cx + 24, cy + 232 + j * 74, cw - 48, 60, fill="FFF7FC", line=LILAC,
                   lw=1)
            s.text(cx + 46, cy + 232 + j * 74, cw - 90, 60, it, font=BODY, size=12,
                   color=VIOLET, anchor=MSO_ANCHOR.MIDDLE)

    # 05 · sawala space
    s = deck.new(); chrome(s, "work")
    bx, by, bw, bh = card(s, 44, 162, 1832, 700, "sawalaspace — project page", bar=PINK)
    shot(s, "arch", bx + 34, by + 26, 520, 420, b.SAWALA_SHOTS[0])
    for i in range(3):
        shot(s, "rrect", bx + 34 + i * 178, by + 464, 164, 150, b.SAWALA_SHOTS[i + 1])
    y = s.head(bx + 610, by + 24, b.SAWALA_TITLE.lower(), font=HEAD, size=44, color=PINK,
               bold=True, max_w=900, one_line=True, gap=8)
    y = s.head(bx + 612, y, b.SAWALA_SUB.lower(), font=BODY, size=13.5, color=VIOLET,
               gap=14)
    s.rect(bx + 612, y, 180, 8, fill=MINT)
    y = s.para(bx + 610, y + 26, 880, b.SAWALA_BODY, font=BODY, size=13, color=VIOLET,
               spacing=1.75, max_h=240, gap=24)
    y = s.head(bx + 612, y, "my role:", font=UI, size=19, color=PINK, gap=12)
    x = bx + 610
    for i, t in enumerate(b.SAWALA_TAGS):
        if i == 3:
            x, y = bx + 610, y + 60
        x += s.pill(x, y, t.lower(), size=12, pad=20, h=50, fill="FFF7FC", color=VIOLET,
                    line=LILAC, font=BODY, tracking=1) + 12
    shot(s, "oval", bx + 1560, by + 400, 230, 230, b.SAWALA_SHOTS[5])

    # 06 · content in practice
    s = deck.new(); chrome(s, "work")
    y = s.head(44, 158, "content in practice", font=HEAD, size=40, color=PINK, bold=True,
               gap=6)
    y = s.para(46, y, 1500, b.PRACTICE_TITLE, font=BODY, size=13, color=VIOLET, gap=16)
    kinds = ["arch", "oval", "snip", "hex", "rrect", "oct"]
    for i, (lab, sub) in enumerate(b.PRACTICE):
        x = 44 + (i % 3) * 620
        cy = y + (i // 3) * 340
        cx, cyy, cw, ch = card(s, x, cy, 596, 316, "0%d" % (i + 1),
                               bar=[PINK, LILAC, MINT][i % 3])
        shot(s, kinds[i], cx + 24, cyy + 20, 240, 220, "")
        ly = s.head(cx + 288, cyy + 26, lab.lower(), font=HEAD, size=17, color=VIOLET,
                    max_w=290, gap=10)
        s.para(cx + 288, ly, 290, sub, font=BODY, size=11.5, color=MUTE, spacing=1.5)

    # 07 · stretch for stray
    s = deck.new(); chrome(s, "work")
    s.rrect(44, 156, 1832, 72, fill=MINT, line=VIOLET, lw=1.5, radius=0.3)
    s.text(44, 156, 1832, 72, "★  " + b.STRAY_SUB + "  ★", font=UI, size=21, color=VIOLET,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    bx, by, bw, bh = card(s, 44, 252, 760, 610, "stretch_for_stray.jpg", bar=PINK)
    shot(s, "arch", bx + 26, by + 22, bw - 52, bh - 48, b.STRAY_SHOTS[0])
    sx, sy, sw, sh = card(s, 836, 252, 1040, 610, "event details", bar=LILAC)
    y = s.head(sx + 34, sy + 22, b.STRAY_TITLE.lower(), font=HEAD, size=38, color=PINK,
               bold=True, max_w=900, one_line=True, gap=12)
    y = s.para(sx + 34, y, 880, b.STRAY_BODY, font=BODY, size=13, color=VIOLET,
               spacing=1.6, gap=18)
    y = s.head(sx + 34, y, "what i did:", font=UI, size=19, color=PINK, gap=12)
    for i, it in enumerate(b.STRAY_LIST):
        ry = y + i * 50
        s.rrect(sx + 34, ry + 6, 22, 22, fill=MINT, line=VIOLET, lw=1, radius=0.25)
        s.text(sx + 74, ry, 560, 40, it, font=BODY, size=12.5, color=VIOLET,
               anchor=MSO_ANCHOR.MIDDLE)
    shot(s, "rrect", sx + 680, sy + 200, 300, 200, b.STRAY_SHOTS[1])
    shot(s, "oval", sx + 700, sy + 420, 180, 160, b.STRAY_SHOTS[2])

    # 08 · behind the content
    s = deck.new(); chrome(s, "process")
    y = s.head(44, 158, b.BEHIND_TITLE.lower(), font=HEAD, size=40, color=PINK, bold=True,
               max_w=1100, one_line=True, gap=14)
    x = 44
    for i, step in enumerate(b.BEHIND_STEPS):
        x += s.pill(x, y, step.lower(), size=12, pad=20, h=48,
                    fill=[PINK, LILAC, MINT, SKY, PINK][i],
                    color="FFFFFF" if i in (0, 1, 4) else VIOLET, font=BODY,
                    tracking=1) + 12
    y += 68
    gx, gy, gw, gh = card(s, 44, y, 1832, 1000 - y, "process_gallery", bar=LILAC)
    kinds = ["snip", "oval", "rrect", "hex", "arch", "snip1", "oct", "rrect"]
    for i, (cap, step) in enumerate(b.BEHIND_SHOTS):
        cx = gx + 28 + (i % 4) * 448
        cy = gy + 20 + (i // 4) * ((gh - 40) / 2)
        shot(s, kinds[i], cx, cy, 420, (gh - 40) / 2 - 62, cap)
        s.text(cx + 2, cy + (gh - 40) / 2 - 56, 300, 30, step.lower(), font=UI, size=15,
               color=PINK)

    # 09 · tools
    s = deck.new(); chrome(s, "about")
    y = s.head(44, 158, b.TOOLS_TITLE.lower(), font=HEAD, size=42, color=PINK, bold=True,
               max_w=900, one_line=True, gap=18)
    for i, (group, items) in enumerate(b.TOOLS):
        x = 44 + i * 620
        cx, cy, cw, ch = card(s, x, y, 596, 420, group.lower(),
                              bar=[PINK, LILAC, MINT][i])
        for j, it in enumerate(items):
            s.rect(cx + 26, cy + 24 + j * 84, cw - 52, 68, fill="FFF7FC", line=LILAC,
                   lw=1)
            s.rrect(cx + 46, cy + 40 + j * 84, 36, 36, fill=[PINK, LILAC, MINT][i],
                    radius=0.2)
            s.text(cx + 100, cy + 24 + j * 84, 380, 68, it, font=BODY, size=13,
                   color=VIOLET, anchor=MSO_ANCHOR.MIDDLE)
    ny = y + 450
    nx, nyy, nw, nh = card(s, 44, ny, 1832, 1000 - ny, "note", bar=SKY)
    s.para(nx + 30, nyy + 18, 1400, b.TOOLS_NOTE, font=BODY, size=13.5, color=VIOLET,
           spacing=1.6)
    shot(s, "oval", nx + 1560, nyy + 6, 150, 150, "photo")

    # 10 · closing
    s = deck.new(); chrome(s, "contact")
    bx, by, bw, bh = card(s, 380, 230, 1160, 620, "new message!", bar=PINK)
    s.heart(bx + 50, by + 40, 70, fill=PINK)
    y = s.head(bx + 150, by + 36, b.END_TITLE[0].lower(), font=HEAD, size=34, color=PINK,
               bold=True, max_w=900, one_line=True, gap=2)
    y = s.head(bx + 150, y, b.END_TITLE[1].lower(), font=HEAD, size=34, color=PINK,
               bold=True, gap=20)
    y = s.head(bx + 50, y, b.NAME.title(), font=HEAD, size=24, color=VIOLET, gap=6)
    y = s.head(bx + 50, y, b.END_ROLE + "  ·  " + b.END_SUB, font=BODY, size=12.5,
               color=MUTE, gap=24)
    for i, (lab, val) in enumerate(b.CONTACT):
        ry = y + i * 76
        s.rect(bx + 50, ry, bw - 100, 62, fill="FFF7FC", line=LILAC, lw=1)
        s.text(bx + 78, ry, 260, 62, lab.lower(), font=UI, size=18, color=PINK,
               anchor=MSO_ANCHOR.MIDDLE)
        s.text(bx + 350, ry, 560, 62, val, font=BODY, size=12.5, color=VIOLET,
               anchor=MSO_ANCHOR.MIDDLE)
    return deck
