# -*- coding: utf-8 -*-
"""PORTFOLIO 02 — DOLLHOUSE.  Reference 2.

Y2K web boutique: a pastel storefront rendered as a portfolio. Modular card
grid, sidebar navigation, window title bars, pixel UI labels, announcement
banner and taskbar. Dense, cute, structured. 100% editable shapes.
"""
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import deckkit as dk
import content as c

BG, PINK, LILAC, MINT, VIOLET = "FFF0F7", "FF6FB5", "C9B6FF", "B9F0E4", "4A2E6B"
CREAM, DEEP, SKY = "FFFDF6", "3A1E55", "BFE4FF"
HEAD, UI, BODY = "Fredoka", "VT323", "Poppins"

def checker(s, x, y, w, cell=24, c1=VIOLET, c2="FFFFFF"):
    for i in range(int(w // cell)):
        s.rect(x + i * cell, y, cell, cell, fill=c1 if i % 2 == 0 else c2)

def chrome(s, tab="home"):
    s.bg(fill=BG)
    s.rect(0, 0, 1920, 34, fill=PINK)
    s.text(40, 0, 1400, 34, "NEW DROP ALERT  ·  2026 PORTFOLIO OUT NOW  ·  SCROLL 4 MORE",
           font=UI, size=15, color="FFFFFF", anchor=MSO_ANCHOR.MIDDLE, tracking=3)
    s.text(1500, 0, 380, 34, "sign in     join now!     [ x ]", font=UI, size=15,
           color="FFFFFF", anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)
    s.text(48, 42, 520, 60, "zahra.house", font=HEAD, size=23, color=PINK, bold=True)
    nav = ["home", "about", "work", "lookbook", "contact"]
    for i, n in enumerate(nav):
        fill = LILAC if n == tab else "FFFFFF"
        col = "FFFFFF" if n == tab else VIOLET
        s.pill(430 + i * 184, 48, n, size=11.5, pad=20, h=48, fill=fill, color=col,
               line=LILAC, font=BODY, tracking=1, width=174)
    s.rrect(1390, 48, 480, 48, fill="FFFFFF", line=LILAC, lw=1.5, radius=0.5)
    s.text(1420, 48, 400, 48, "search the site...", font=BODY, size=11.5, color="A796BC",
           anchor=MSO_ANCHOR.MIDDLE)
    checker(s, 0, 122, 1920, 16)
    # taskbar
    s.rect(0, 1016, 1920, 64, fill=LILAC)
    s.pill(18, 1026, "start", size=14, pad=24, h=44, fill=MINT, color=VIOLET, font=BODY,
           tracking=2, width=132, radius=0.3)
    s.rrect(168, 1026, 360, 44, fill="FFFFFF", radius=0.3)
    s.text(192, 1026, 330, 44, "portfolio_2026.html", font=UI, size=16, color=VIOLET,
           anchor=MSO_ANCHOR.MIDDLE)
    s.rrect(1700, 1026, 200, 44, fill="FFFFFF", radius=0.3)
    s.text(1700, 1026, 200, 44, "10:30 PM", font=UI, size=16, color=VIOLET,
           anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

def card(s, x, y, w, h, title, bar=LILAC, body="FFFFFF"):
    s.rrect(x, y, w, h, fill=body, line=VIOLET, lw=1.5, radius=0.04)
    s.rect(x + 2, y + 2, w - 4, 40, fill=bar)
    s.text(x + 16, y + 2, w - 100, 40, title, font=UI, size=17, color="FFFFFF",
           anchor=MSO_ANCHOR.MIDDLE)
    for i in range(3):
        s.rect(x + w - 30 - i * 26, y + 14, 16, 16, fill="FFFFFF", line=VIOLET, lw=1)
    return x, y + 42, w, h - 42

def build(deck):
    # 1 · cover
    s = deck.new(); chrome(s, "home")
    bx, by, bw, bh = card(s, 48, 168, 1180, 700, "welcome_2_my_world.html", bar=PINK)
    s.text(bx + 56, by + 40, 700, 90, "hi! i'm", font=HEAD, size=34, color=LILAC)
    s.text(bx + 52, by + 96, 900, 200, "zahra", font=HEAD, size=88, color=PINK, bold=True)
    s.text(bx + 56, by + 316, 800, 90, c.NAME.split()[1].lower(), font=HEAD, size=40,
           color=VIOLET)
    s.text(bx + 58, by + 406, 600, 90, c.DISCIPLINES, font=BODY, size=12.5, color=VIOLET,
           spacing=1.5)
    s.pill(bx + 56, by + 506, "view my work →", size=13, pad=28, h=60, fill=PINK,
           color="FFFFFF", font=BODY, tracking=1, width=300, radius=0.3)
    s.pill(bx + 376, by + 506, "about me", size=13, pad=28, h=60, fill="FFFFFF",
           color=VIOLET, line=LILAC, font=BODY, tracking=1, width=220, radius=0.3)
    s.photo(bx + 700, by + 54, 420, 500, "drop portrait", fill=SKY, line=VIOLET,
            radius=0.03, label_color=VIOLET)
    sx, sy, sw, sh = card(s, 1260, 168, 612, 340, "quick links", bar=MINT)
    for i, (lab, val) in enumerate([("new arrivals", "→"), ("best sellers", "→"),
                                    ("my story", "→"), ("say hi", "→")]):
        s.rect(sx + 18, sy + 22 + i * 66, sw - 36, 54, fill="FFF7FC", line=LILAC, lw=1)
        s.text(sx + 40, sy + 22 + i * 66, 400, 54, lab, font=BODY, size=13, color=VIOLET,
               anchor=MSO_ANCHOR.MIDDLE)
        s.text(sx + sw - 90, sy + 22 + i * 66, 40, 54, "›", font=BODY, size=18,
               color=PINK, anchor=MSO_ANCHOR.MIDDLE)
    mx, my, mw, mh = card(s, 1260, 528, 612, 340, "new message!", bar=PINK)
    s.heart(mx + 36, my + 40, 60, fill=PINK)
    s.text(mx + 120, my + 44, 420, 120, "you have (1) new message", font=BODY, size=15,
           color=VIOLET, spacing=1.4)
    s.pill(mx + 120, my + 150, "ok", size=13, pad=24, h=48, fill=LILAC, color="FFFFFF",
           font=BODY, width=140, radius=0.3)
    s.text(mx + 36, my + 232, 540, 60, "xoxo — thanks 4 stopping by", font=UI, size=18,
           color="A796BC")

    # 2 · about
    s = deck.new(); chrome(s, "about")
    bx, by, bw, bh = card(s, 48, 168, 1180, 700, "about_zahra.txt", bar=LILAC)
    s.text(bx + 56, by + 40, 800, 110, "about me!", font=HEAD, size=50, color=PINK, bold=True)
    s.rect(bx + 58, by + 172, 240, 8, fill=MINT)
    s.text(bx + 56, by + 212, 1060, 420, c.ABOUT, font=BODY, size=13, color=VIOLET,
           spacing=1.8, after=18)
    sx, sy, sw, sh = card(s, 1260, 168, 612, 470, "cute.jpg", bar=PINK)
    s.photo(sx + 26, sy + 26, sw - 52, sh - 52, "drop photo", fill=SKY, line=VIOLET,
            radius=0.03, label_color=VIOLET)
    nx, ny, nw, nh = card(s, 1260, 658, 612, 210, "don't forget!", bar=MINT)
    for i, t in enumerate(["☆ content & social", "☆ design & visuals", "☆ events & partnerships"]):
        s.text(nx + 30, ny + 14 + i * 46, 540, 42, t, font=BODY, size=13, color=VIOLET,
               anchor=MSO_ANCHOR.MIDDLE)

    # 3 · what i do
    s = deck.new(); chrome(s, "work")
    s.text(48, 152, 900, 90, c.DO_TITLE.lower(), font=HEAD, size=46, color=PINK, bold=True)
    s.text(50, 276, 900, 40, "4 things i'm good at", font=BODY, size=13, color=VIOLET)
    for i, (title, sub) in enumerate(c.DO):
        x = 48 + (i % 4) * 462
        bx2, by2, bw2, bh2 = card(s, x, 336, 436, 530,
                                  ["content", "creative", "marketing", "comms"][i],
                                  bar=[PINK, LILAC, MINT, SKY][i])
        s.rect(bx2 + 24, by2 + 20, bw2 - 48, 176, fill=["FFE6F3", "F0EAFF", "E6FBF6",
                                                        "E8F5FF"][i], line=LILAC, lw=1)
        s.text(bx2 + 24, by2 + 70, bw2 - 48, 80, "0%d" % (i + 1), font=HEAD, size=46,
               color=["FF6FB5", "C9B6FF", "7FD8C4", "8CC6F0"][i], align=PP_ALIGN.CENTER)
        s.text(bx2 + 30, by2 + 216, bw2 - 60, 110, title, font=HEAD, size=19, color=VIOLET,
               spacing=1.25)
        s.text(bx2 + 30, by2 + 332, bw2 - 60, 120, sub, font=BODY, size=11.5,
               color="7A669A", spacing=1.5)
        s.pill(bx2 + 30, by2 + 432, "learn more", size=11.5, pad=18, h=42, fill=PINK,
               color="FFFFFF", font=BODY, width=170, radius=0.3)

    # 4 · experience
    s = deck.new(); chrome(s, "about")
    bx, by, bw, bh = card(s, 48, 168, 1300, 700, "my_experience — folder", bar=LILAC)
    s.text(bx + 40, by + 24, 800, 60, c.EXP_TITLE.lower(), font=HEAD, size=36, color=PINK)
    for i, (org, role) in enumerate(c.EXP):
        y = by + 132 + i * 102
        s.rect(bx + 34, y, bw - 68, 88, fill="FFF7FC" if i % 2 == 0 else "FFFFFF",
               line=LILAC, lw=1)
        s.rrect(bx + 56, y + 18, 52, 50, fill=[PINK, LILAC, MINT, SKY, PINK][i], radius=0.2)
        s.text(bx + 136, y + 10, 800, 42, org, font=HEAD, size=17, color=VIOLET)
        s.text(bx + 138, y + 50, 800, 32, role, font=BODY, size=11, color="7A669A")
        s.text(bx + bw - 130, y, 80, 92, "›", font=BODY, size=22, color=PINK,
               anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    sx, sy, sw, sh = card(s, 1380, 168, 492, 700, "my faves", bar=MINT)
    for i, (lab, n) in enumerate([("saved items", "(12)"), ("wish list", "(8)"),
                                  ("recently viewed", "(15)"), ("size guide", ">>")]):
        s.rect(sx + 22, sy + 24 + i * 72, sw - 44, 58, fill="FFFDF6", line=LILAC, lw=1)
        s.text(sx + 46, sy + 24 + i * 72, 300, 58, lab, font=BODY, size=12.5, color=VIOLET,
               anchor=MSO_ANCHOR.MIDDLE)
        s.text(sx + sw - 140, sy + 24 + i * 72, 90, 58, n, font=UI, size=17, color=PINK,
               anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)
    s.photo(sx + 22, sy + 330, sw - 44, 270, "drop photo", fill=SKY, line=VIOLET,
            radius=0.03, label_color=VIOLET)

    # 5 · sawala space
    s = deck.new(); chrome(s, "work")
    bx, by, bw, bh = card(s, 48, 168, 1824, 700, "sawalaspace.com — product page", bar=PINK)
    s.photo(bx + 40, by + 34, 560, 440, "drop photo", fill=SKY, line=VIOLET, radius=0.03,
            label_color=VIOLET)
    for i in range(3):
        s.photo(bx + 40 + i * 190, by + 492, 176, 120, "", fill=SKY, line=VIOLET,
                radius=0.03)
    s.text(bx + 650, by + 34, 900, 100, c.SAWALA_TITLE.lower(), font=HEAD, size=46,
           color=PINK, bold=True)
    s.text(bx + 652, by + 160, 900, 44, c.SAWALA_SUB, font=BODY, size=15, color=VIOLET)
    s.rect(bx + 652, by + 214, 200, 8, fill=MINT)
    s.text(bx + 652, by + 244, 820, 200, c.SAWALA_BODY, font=BODY, size=13,
           color="5A4676", spacing=1.7)
    s.text(bx + 652, by + 420, 400, 40, "my role:", font=UI, size=20, color=PINK)
    x, y = bx + 652, by + 466
    for i, r in enumerate(c.SAWALA_ROLE):
        if i == 3:
            x, y = bx + 652, by + 524
        x += s.pill(x, y, r, size=12, pad=20, h=48, fill="FFF7FC", color=VIOLET,
                    line=LILAC, font=BODY, tracking=1) + 12
    s.pill(bx + 652, by + 588, "view the project →", size=14, pad=30, h=60, fill=PINK,
           color="FFFFFF", font=BODY, width=330, radius=0.3)

    # 6 · selected works
    s = deck.new(); chrome(s, "lookbook")
    s.text(48, 148, 900, 80, "new arrivals", font=HEAD, size=42, color=PINK, bold=True)
    s.text(50, 250, 1500, 40, c.WORKS_BODY, font=BODY, size=11.5, color=VIOLET)
    x = 48
    for i, tag in enumerate(c.WORKS_TAGS):
        x += s.pill(x, 298, tag, size=12, pad=20, h=46, fill=[PINK, LILAC, MINT, SKY][i],
                    color="FFFFFF" if i < 2 else VIOLET, font=BODY, tracking=1) + 12
    for i, cap in enumerate(c.WORKS_CAPS):
        gx = 48 + (i % 4) * 462
        gy = 366 + (i // 4) * 326
        s.rrect(gx, gy, 436, 300, fill="FFFFFF", line=VIOLET, lw=1.5, radius=0.05)
        s.photo(gx + 18, gy + 18, 400, 190, cap, fill=SKY, line=LILAC, radius=0.03,
                label_color=VIOLET)
        s.text(gx + 22, gy + 220, 260, 34, cap, font=BODY, size=11.5, color=VIOLET)
        s.pill(gx + 306, gy + 224, "view", size=11, pad=14, h=40, fill=PINK,
               color="FFFFFF", font=BODY, width=104, radius=0.3)

    # 7 · stretch for stray
    s = deck.new(); chrome(s, "work")
    s.rrect(48, 152, 1824, 84, fill=MINT, line=VIOLET, lw=1.5, radius=0.3)
    s.text(48, 152, 1824, 84, "★  FEATURED EVENT  ·  " + c.STRAY_SUB.upper() + "  ★",
           font=UI, size=22, color=VIOLET, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    bx, by, bw, bh = card(s, 48, 262, 820, 606, "stretch_for_stray.jpg", bar=PINK)
    s.photo(bx + 30, by + 26, bw - 60, bh - 56, "drop poster", fill=SKY, line=VIOLET,
            radius=0.03, label_color=VIOLET)
    sx, sy, sw, sh = card(s, 900, 262, 972, 606, "event details", bar=LILAC)
    s.text(sx + 40, sy + 30, 880, 110, c.STRAY_TITLE.lower(), font=HEAD, size=38,
           color=PINK, bold=True)
    s.text(sx + 42, sy + 128, 820, 90, c.STRAY_BODY, font=BODY, size=13, color=VIOLET,
           spacing=1.6)
    s.text(sx + 42, sy + 240, 500, 40, "what i did:", font=UI, size=20, color=PINK)
    for i, it in enumerate(c.STRAY_LIST):
        y = sy + 290 + i * 52
        s.rrect(sx + 42, y + 8, 26, 26, fill=MINT, line=VIOLET, lw=1, radius=0.25)
        s.text(sx + 88, y, 700, 42, it, font=BODY, size=13, color=VIOLET,
               anchor=MSO_ANCHOR.MIDDLE)

    # 8 · beyond
    s = deck.new(); chrome(s, "about")
    s.text(48, 148, 1000, 80, "community corner", font=HEAD, size=40, color=PINK, bold=True)
    s.text(50, 248, 1400, 44, c.BEYOND_BODY, font=BODY, size=13, color=VIOLET)
    for i, (title, sub) in enumerate(c.BEYOND):
        x = 48 + i * 618
        bx2, by2, bw2, bh2 = card(s, x, 310, 588, 550, ["media", "arts", "academic"][i],
                                  bar=[PINK, LILAC, MINT][i])
        s.photo(bx2 + 26, by2 + 26, bw2 - 52, 200, "drop photo", fill=SKY, line=LILAC,
                radius=0.03, label_color=VIOLET)
        s.text(bx2 + 30, by2 + 248, bw2 - 60, 130, title, font=HEAD, size=20, color=VIOLET,
               spacing=1.25)
        s.text(bx2 + 30, by2 + 386, bw2 - 60, 110, sub, font=BODY, size=12,
               color="7A669A", spacing=1.5)

    # 9 · skills
    s = deck.new(); chrome(s, "about")
    s.text(48, 148, 900, 80, "my skill tree", font=HEAD, size=42, color=PINK, bold=True)
    for i, (title, items) in enumerate(c.SKILLS):
        x = 48 + i * 618
        bx2, by2, bw2, bh2 = card(s, x, 292, 588, 396, title.lower(),
                                  bar=[PINK, LILAC][i])
        for j, it in enumerate(items):
            y = by2 + 30 + j * 80
            s.rect(bx2 + 26, y, bw2 - 52, 62, fill="FFF7FC", line=LILAC, lw=1)
            s.text(bx2 + 50, y, 320, 62, it, font=BODY, size=13, color=VIOLET,
                   anchor=MSO_ANCHOR.MIDDLE)
            s.rrect(bx2 + 360, y + 22, 180, 18, fill="FFFFFF", line=LILAC, lw=1,
                    radius=0.5)
            s.rrect(bx2 + 360, y + 22, 180 - j * 18, 18, fill=[PINK, LILAC][i], radius=0.5)
    tx, ty, tw, th = card(s, 1284, 292, 588, 396, "tools.exe", bar=MINT)
    x, y = tx + 24, ty + 26
    for i, t in enumerate(c.TOOLS):
        wpill = s.pill(x, y, t, size=11, pad=14, h=44, fill="FFFDF6", color=VIOLET,
                       line=LILAC, font=BODY, tracking=0)
        x += wpill + 10
        if x > tx + tw - 180:
            x, y = tx + 24, y + 56
    s.rrect(48, 724, 1824, 140, fill="FFFFFF", line=VIOLET, lw=1.5, radius=0.06)
    s.text(80, 748, 900, 44, "blog corner", font=HEAD, size=22, color=PINK)
    s.text(82, 800, 1700, 60, "  ·  ".join(c.DISCIPLINE_LIST), font=BODY, size=12.5,
           color=VIOLET)

    # 10 · contact
    s = deck.new(); chrome(s, "contact")
    bx, by, bw, bh = card(s, 420, 240, 1080, 620, "new message!", bar=PINK)
    s.heart(bx + 60, by + 54, 84, fill=PINK)
    s.text(bx + 180, by + 44, 840, 80, "let's work together!", font=HEAD, size=32,
           color=PINK, bold=True)
    s.text(bx + 182, by + 140, 820, 130, c.END_BODY, font=BODY, size=13, color=VIOLET,
           spacing=1.7)
    for i, (lab, val) in enumerate(c.CONTACT):
        y = by + 292 + i * 84
        s.rect(bx + 60, y, bw - 120, 68, fill="FFF7FC", line=LILAC, lw=1)
        s.text(bx + 92, y, 280, 68, lab.lower(), font=UI, size=19, color=PINK,
               anchor=MSO_ANCHOR.MIDDLE)
        s.text(bx + 380, y, 520, 68, val, font=BODY, size=13, color=VIOLET,
               anchor=MSO_ANCHOR.MIDDLE)
    s.pill(bx + 60, by + 540, "send me a message →", size=13, pad=26, h=60, fill=PINK,
           color="FFFFFF", font=BODY, width=400, radius=0.3)
    s.text(bx + 500, by + 540, 500, 60, "xoxo, zahra", font=UI, size=22, color=LILAC,
           anchor=MSO_ANCHOR.MIDDLE)
    return deck
