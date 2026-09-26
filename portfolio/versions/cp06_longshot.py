# -*- coding: utf-8 -*-
"""VERSION 06 — LONGSHOT.  Reference 6.

Y2K collage poster: airbrushed colour-field grounds with film grain, chrome
italic display type on dark blurred blobs, outlined starbursts, glowing photo
cut-outs and hard colour panels. Printed, dense, early-2000s magazine-ad.

Grounds, grain, chrome lettering and bursts are images (a metal gradient and a
blend are not shapes). Panels, tiles, chips, rules and all copy stay native.
"""
import hashlib, os
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import deckkit as dk
import brief as b
import poster as P

HERE = os.path.dirname(os.path.abspath(__file__))
ORN = os.path.join(HERE, "ornaments06")
os.makedirs(ORN, exist_ok=True)

RED, BLUE, CYAN, YELLOW = "E8352B", "2B4FD8", "35C5F0", "FFE400"
INK, WHITE, CREAM = "0C1024", "FFFFFF", "FFF6D8"
BODY, LABEL = "Poppins", "Poppins"

_cache = {}
def _asset(name, maker, ext="png", **save):
    key = hashlib.md5(name.encode()).hexdigest()[:10]
    path = os.path.join(ORN, "%s.%s" % (key, ext))
    if key not in _cache:
        if not os.path.exists(path):
            img = maker()
            if ext == "jpg":
                img.convert("RGB").save(path, quality=86, optimize=True)
            else:
                img.save(path, optimize=True)
        _cache[key] = path
    return _cache[key]

def chrome(s, text, size, x, y, gold=False):
    st = P.GOLD if gold else P.CHROME
    path = _asset("c|%s|%s|%s" % (text, size, gold), lambda: P.chrome_text(text, size, stops=st))
    from PIL import Image
    im = Image.open(path)
    w, h = im.size[0] / P.S, im.size[1] / P.S
    s.pic(path, x, y, w)
    return y + h * 0.78          # chrome art carries padding; this is the optical foot

def blob(s, x, y, w, h, alpha=215, blur=26):
    path = _asset("b|%s|%s|%s|%s" % (w, h, alpha, blur),
                  lambda: P.blob((w, h), alpha=alpha, blur=blur))
    from PIL import Image
    im = Image.open(path)
    s.pic(path, x - (im.size[0] / P.S - w) / 2, y - (im.size[1] / P.S - h) / 2,
          im.size[0] / P.S)

def ground(s, blocks, seed=3, blur=90):
    path = _asset("g|%s|%s|%s" % (blocks, seed, blur),
                  lambda: P.wash((1920, 1080), blocks, blur=blur, seed=seed), ext="jpg")
    s.pic(path, 0, 0, 1920, 1080)
    s.pic(_asset("grain", lambda: P.grain((1920, 1080), 22, seed=7)), 0, 0, 1920, 1080)

def burst(s, x, y, size, fill=YELLOW, rot=0, points=10):
    col = tuple(int(fill[i:i + 2], 16) for i in (0, 2, 4))
    path = _asset("bu|%s|%s|%s|%s" % (size, fill, rot, points),
                  lambda: P.burst(size, fill=col, rot=rot, points=points))
    from PIL import Image
    im = Image.open(path)
    s.pic(path, x - im.size[0] / P.S / 2, y - im.size[1] / P.S / 2, im.size[0] / P.S)

def star(s, x, y, size, fill=WHITE, edge=BLUE, rot=0):
    f = tuple(int(fill[i:i + 2], 16) for i in (0, 2, 4))
    e = tuple(int(edge[i:i + 2], 16) for i in (0, 2, 4))
    path = _asset("st|%s|%s|%s|%s" % (size, fill, edge, rot),
                  lambda: P.star5(size, fill=f, edge=e, rot=rot))
    from PIL import Image
    im = Image.open(path)
    s.pic(path, x - im.size[0] / P.S / 2, y - im.size[1] / P.S / 2, im.size[0] / P.S)

def tile(s, x, y, w, h, label="drop photo", kind="rect", rot=0):
    path = _asset("gl|%s|%s" % (w, h), lambda: P.glow_cut((w, h)))
    from PIL import Image
    im = Image.open(path)
    s.pic(path, x - (im.size[0] / P.S - w) / 2, y - (im.size[1] / P.S - h) / 2,
          im.size[0] / P.S)
    return s.cut(kind, x, y, w, h, label, fill="D9DEE8", line=WHITE, lw=7, rot=rot,
                 radius=0.06 if kind in ("rrect", "arch") else None,
                 label_color="6B7488", size=10, font=BODY)

def panel(s, x, y, w, h, fill, line=WHITE, lw=5):
    return s.rect(x, y, w, h, fill=fill, line=line, lw=lw)

def credit(s, text="ZAHRA LEVINA · CONTENT PRODUCTION 2026"):
    s.text(1120, 1026, 760, 32, text, font=LABEL, size=10, bold=True, color=WHITE,
           align=PP_ALIGN.RIGHT, tracking=3, wrap_text=False)

Q = [(0, 0, 960, 540, (232, 53, 43)), (960, 0, 1920, 540, (43, 79, 216)),
     (0, 540, 960, 1080, (255, 228, 0)), (960, 540, 1920, 1080, (53, 197, 240))]


def build(deck):
    # 01 · cover ------------------------------------------------------------
    s = deck.new(); ground(s, Q, seed=3)
    blob(s, 60, 80, 1000, 300)
    y = chrome(s, "CONTENT", 92, 70, 70)
    y = chrome(s, "PRODUCTION", 92, 70, y - 20)
    y = chrome(s, "PORTFOLIO", 60, 76, y - 16, gold=True)
    s.text(104, y + 16, 560, 44, b.KICKER[0], font=LABEL, size=17, bold=True,
           color=WHITE, tracking=8)
    panel(s, 96, y + 84, 560, 62, INK, line=None)
    s.text(96, y + 84, 560, 62, b.NAME, font=LABEL, size=19, bold=True, color=WHITE,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, tracking=6)
    s.text(104, y + 170, 580, 100, b.TAGLINE, font=BODY, size=15, italic=True,
           color=WHITE, spacing=1.5)
    tile(s, 1150, 200, 600, 740, "drop portrait", rot=-2)
    tile(s, 120, 726, 250, 200, "photo")
    tile(s, 402, 780, 220, 146, "photo", rot=-6)
    burst(s, 1046, 176, 190, YELLOW, rot=8)
    s.text(964, 138, 164, 78, "NEW\n2026", font=LABEL, size=13, bold=True, color=INK,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=1.1)
    star(s, 700, 620, 150, WHITE, BLUE, rot=8)
    star(s, 1812, 470, 110, RED, WHITE)
    star(s, 660, 320, 90, WHITE, RED, rot=-12)
    credit(s)

    # 02 · about ------------------------------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (43, 79, 216)), (0, 0, 840, 1080, (232, 53, 43)),
               (1200, 0, 1920, 620, (53, 197, 240)), (0, 780, 900, 1080, (255, 228, 0))],
           seed=5)
    blob(s, 70, 74, 700, 190)
    y = chrome(s, "ABOUT ME", 74, 80, 64)
    s.text(96, y + 24, 660, 540, b.ABOUT, font=BODY, size=15, italic=True, color=WHITE,
           spacing=1.7, after=20)
    tile(s, 900, 180, 560, 700, "drop portrait")
    tile(s, 1520, 640, 300, 240, "photo", rot=5)
    panel(s, 900, 916, 560, 58, INK, line=None)
    s.text(900, 916, 560, 58, "CONTENT · CREATIVE · COMMUNICATION", font=LABEL, size=13,
           bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
           tracking=4)
    star(s, 1490, 170, 120, WHITE, BLUE, rot=10)
    burst(s, 1810, 260, 150, RED, rot=14)
    credit(s)

    # 03 · from idea to publish ---------------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (255, 228, 0)), (0, 0, 1920, 360, (232, 53, 43)),
               (1180, 320, 1920, 1080, (43, 79, 216))], seed=9)
    blob(s, 70, 70, 1040, 190)
    y = chrome(s, "FROM IDEA TO PUBLISH", 62, 80, 58)
    cols = [RED, BLUE, CYAN, INK, RED, BLUE, CYAN]
    for i, step in enumerate(b.FLOW):
        x = 96 + i * 250
        panel(s, x, y + 40, 226, 150, cols[i], lw=5)
        s.text(x, y + 56, 226, 40, "0%d" % (i + 1), font=LABEL, size=15, bold=True,
               color=WHITE if i != 2 else INK, align=PP_ALIGN.CENTER, italic=True)
        s.text(x, y + 100, 226, 60, step, font=LABEL, size=19, bold=True,
               color=WHITE if i != 2 else INK, align=PP_ALIGN.CENTER, italic=True)
    ny = y + 230
    panel(s, 96, ny, 1040, 214, INK, lw=5)
    s.text(132, ny + 20, 968, 180, b.FLOW_NOTE, font=BODY, size=12.5, italic=True,
           color=WHITE, spacing=1.55, after=10)
    tile(s, 1190, ny - 30, 300, 220, "content prep")
    tile(s, 1520, ny - 10, 300, 200, "photo", rot=4)
    tile(s, 1300, ny + 216, 420, 150, "photo", rot=-3)
    burst(s, 1810, 210, 150, YELLOW, rot=20)
    star(s, 1140, 330, 110, WHITE, RED, rot=-8)
    credit(s)

    # 04 · content, in different forms --------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (53, 197, 240)), (0, 0, 1920, 340, (12, 16, 36)),
               (0, 700, 1920, 1080, (255, 228, 0))], seed=15)
    y = chrome(s, "CONTENT, IN DIFFERENT FORMS.", 54, 80, 54)
    cols = [RED, BLUE, INK, CYAN]
    for i, (group, items) in enumerate(b.FORMS):
        x = 96 + i * 440
        panel(s, x, y + 40, 412, 540, cols[i], lw=5)
        s.text(x + 26, y + 60, 366, 56, group, font=LABEL, size=20, bold=True,
               color=WHITE if i != 3 else INK, italic=True, tracking=1,
               wrap_text=False)
        tile(s, x + 26, y + 130, 360, 170, "", kind="rect")
        for j, it in enumerate(items):
            ry = y + 322 + j * 60
            s.rect(x + 26, ry, 360, 48, fill=WHITE)
            s.text(x + 46, ry, 320, 48, it, font=BODY, size=12.5, italic=True,
                   color=INK, anchor=MSO_ANCHOR.MIDDLE)
    star(s, 1852, 660, 110, WHITE, RED, rot=8)
    credit(s)

    # 05 · sawala space ------------------------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (53, 197, 240)), (0, 0, 1020, 1080, (255, 228, 0)),
               (1100, 0, 1920, 500, (232, 53, 43))], seed=13)
    blob(s, 70, 66, 960, 180)
    y = chrome(s, "SAWALA SPACE", 72, 80, 56)
    tile(s, 110, y + 40, 620, 600, b.SAWALA_SHOTS[0])
    tile(s, 110, y + 660, 300, 190, b.SAWALA_SHOTS[1])
    tile(s, 432, y + 660, 298, 190, b.SAWALA_SHOTS[2], rot=3)
    panel(s, 800, y + 40, 1020, 300, INK, lw=6)
    s.text(838, y + 62, 946, 44, b.SAWALA_SUB, font=LABEL, size=16, bold=True,
           color=YELLOW, italic=True, tracking=2)
    s.text(838, y + 118, 946, 200, b.SAWALA_BODY, font=BODY, size=14, italic=True,
           color=WHITE, spacing=1.6)
    s.text(800, y + 372, 400, 40, "MY ROLE", font=LABEL, size=15, bold=True, color=INK,
           tracking=5)
    x, ry = 800, y + 418
    for i, t in enumerate(b.SAWALA_TAGS):
        if i == 3:
            x, ry = 800, y + 490
        x += s.pill(x, ry, t, size=12, pad=20, h=56, fill=[RED, BLUE, CYAN][i % 3],
                    color=WHITE if i % 3 != 2 else INK, line=WHITE, font=LABEL,
                    tracking=2, radius=0.12) + 16
    tile(s, 800, y + 570, 500, 280, b.SAWALA_SHOTS[3])
    tile(s, 1330, y + 570, 490, 280, b.SAWALA_SHOTS[4], rot=-2)
    burst(s, 760, 240, 140, YELLOW, rot=16)
    credit(s)

    # 06 · content in practice ----------------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (232, 53, 43)), (0, 0, 1920, 300, (43, 79, 216)),
               (0, 680, 1920, 1080, (255, 228, 0))], seed=17)
    blob(s, 70, 58, 1280, 170)
    y = chrome(s, "MAKING CONTENT THAT HAS SOMEWHERE TO GO.", 44, 80, 50)
    kinds = ["rect", "rect", "rect", "rect", "rect", "rect"]
    for i, (lab, sub) in enumerate(b.PRACTICE):
        gx = 96 + (i % 3) * 590
        gy = y + 40 + (i // 3) * 330
        panel(s, gx, gy, 566, 300, WHITE, line=INK, lw=4)
        tile(s, gx + 18, gy + 18, 250, 264, "", kind=kinds[i])
        s.text(gx + 292, gy + 26, 250, 30, "0%d" % (i + 1), font=LABEL, size=13,
               bold=True, color="B9BFD0", italic=True)
        s.text(gx + 292, gy + 62, 258, 100, lab, font=LABEL, size=13, bold=True,
               color=INK, italic=True, spacing=1.2)
        s.text(gx + 292, gy + 174, 258, 110, sub, font=BODY, size=11, italic=True,
               color="4A4F63", spacing=1.5)
    star(s, 1856, 320, 110, WHITE, RED, rot=8)
    credit(s)

    # 07 · stretch for stray -------------------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (255, 228, 0)), (700, 0, 1920, 1080, (53, 197, 240)),
               (0, 0, 820, 420, (232, 53, 43))], seed=19)
    blob(s, 640, 58, 1180, 170)
    y = chrome(s, "STRETCH FOR STRAY", 62, 650, 52)
    s.text(660, y + 24, 900, 44, b.STRAY_SUB, font=LABEL, size=16, bold=True, color=INK,
           tracking=5)
    tile(s, 110, 260, 500, 660, b.STRAY_SHOTS[0], rot=-3)
    panel(s, 660, y + 86, 1160, 130, INK, lw=5)
    s.text(696, y + 86, 1090, 130, b.STRAY_BODY, font=BODY, size=16, italic=True,
           color=WHITE, anchor=MSO_ANCHOR.MIDDLE, spacing=1.45)
    s.text(660, y + 248, 500, 40, "MY CONTRIBUTION", font=LABEL, size=15, bold=True,
           color=INK, tracking=5)
    for i, it in enumerate(b.STRAY_LIST):
        ry = y + 296 + i * 62
        panel(s, 660, ry, 620, 50, WHITE, line=INK, lw=3)
        s.rect(660, ry, 14, 50, fill=[RED, BLUE, YELLOW, CYAN, RED, BLUE][i])
        s.text(698, ry, 560, 50, it, font=BODY, size=13, italic=True, color=INK,
               anchor=MSO_ANCHOR.MIDDLE)
    tile(s, 1340, y + 296, 480, 280, b.STRAY_SHOTS[1], rot=4)
    tile(s, 1340, y + 600, 480, 220, b.STRAY_SHOTS[2], rot=-2)
    burst(s, 600, 220, 140, RED, rot=10)
    credit(s)

    # 08 · behind the final post ---------------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (43, 79, 216)), (0, 320, 1920, 1080, (53, 197, 240)),
               (1320, 0, 1920, 1080, (255, 228, 0))], seed=23)
    blob(s, 70, 58, 1060, 170)
    y = chrome(s, "BEHIND THE FINAL POST.", 56, 80, 52)
    x = 96
    for i, step in enumerate(b.BEHIND_STEPS):
        x += s.pill(x, y + 30, step, size=12, pad=20, h=52,
                    fill=[RED, BLUE, INK, CYAN, YELLOW][i],
                    color=INK if i in (3, 4) else WHITE, line=WHITE, font=LABEL,
                    tracking=2, radius=0.12) + 14
    gy = y + 110
    for i, (cap, step) in enumerate(b.BEHIND_SHOTS):
        cx = 96 + (i % 4) * 442
        cyy = gy + (i // 4) * 300
        panel(s, cx, cyy, 418, 268, WHITE, line=INK, lw=4)
        tile(s, cx + 16, cyy + 16, 386, 190, cap)
        s.text(cx + 18, cyy + 216, 300, 40, step, font=LABEL, size=12, bold=True,
               color=INK, tracking=3, anchor=MSO_ANCHOR.MIDDLE)
    credit(s)

    # 09 · tools --------------------------------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (53, 197, 240)), (0, 0, 1920, 360, (12, 16, 36)),
               (960, 340, 1920, 1080, (255, 228, 0))], seed=29)
    y = chrome(s, "THE TOOLS I WORK WITH", 60, 80, 54)
    for i, (group, items) in enumerate(b.TOOLS):
        x = 96 + i * 590
        panel(s, x, y + 40, 566, 380, [RED, BLUE, INK][i], lw=6)
        s.text(x + 30, y + 62, 500, 56, group, font=LABEL, size=24, bold=True,
               color=WHITE, italic=True, tracking=3)
        for j, it in enumerate(items):
            ry = y + 134 + j * 76
            s.rect(x + 30, ry, 506, 62, fill=WHITE)
            s.text(x + 58, ry, 450, 62, it, font=BODY, size=14, italic=True, color=INK,
                   anchor=MSO_ANCHOR.MIDDLE)
    panel(s, 96, y + 460, 1160, 150, INK, lw=5)
    s.text(132, y + 460, 1090, 150, b.TOOLS_NOTE, font=BODY, size=15, italic=True,
           color=WHITE, anchor=MSO_ANCHOR.MIDDLE, spacing=1.5)
    tile(s, 1300, y + 440, 520, 300, "photo", rot=3)
    star(s, 1860, y + 120, 110, WHITE, RED, rot=-10)
    credit(s)

    # 10 · closing ------------------------------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (232, 53, 43)), (0, 0, 1920, 520, (43, 79, 216)),
               (0, 520, 1920, 1080, (255, 228, 0)), (1240, 0, 1920, 1080, (53, 197, 240))],
           seed=31)
    blob(s, 90, 150, 1320, 320)
    y = chrome(s, "LET'S MAKE SOMETHING", 72, 100, 150)
    y = chrome(s, "WORTH SHARING.", 72, 140, y - 18, gold=True)
    panel(s, 104, y + 40, 520, 62, INK, line=None)
    s.text(104, y + 40, 520, 62, b.NAME, font=LABEL, size=18, bold=True, color=WHITE,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, tracking=6)
    s.text(110, y + 124, 900, 44, b.END_ROLE + "  ·  " + b.END_SUB, font=BODY, size=14,
           italic=True, color=WHITE)
    for i, (lab, val) in enumerate(b.CONTACT):
        ry = y + 194 + i * 100
        panel(s, 104, ry, 900, 82, [WHITE, INK, WHITE][i], line=INK, lw=4)
        s.rect(104, ry, 18, 82, fill=[RED, YELLOW, CYAN][i])
        s.text(156, ry, 300, 82, lab.upper(), font=LABEL, size=15, bold=True,
               color=INK if i != 1 else YELLOW, anchor=MSO_ANCHOR.MIDDLE, tracking=3,
               italic=True)
        s.text(440, ry, 520, 82, val, font=BODY, size=13.5, italic=True,
               color=INK if i != 1 else WHITE, anchor=MSO_ANCHOR.MIDDLE)
    tile(s, 1120, 240, 580, 620, "drop photo", rot=3)
    burst(s, 980, 880, 200, YELLOW, rot=14)
    s.text(892, 846, 176, 70, "THX 4\nLOOKN", font=LABEL, size=13, bold=True, color=INK,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=1.1)
    star(s, 1850, 190, 120, WHITE, BLUE, rot=8)
    credit(s)
    return deck
