# -*- coding: utf-8 -*-
"""PORTFOLIO 06 — LONGSHOT.  Reference 6.

Y2K collage poster: airbrushed colour-field grounds, chrome italic display type
on dark blurred blobs, outlined starbursts, glowing photo cut-outs, dense
overlapping layers. Loud, printed, early-2000s magazine-ad energy.

Backgrounds and chrome lettering are images (a blend and a metal gradient are
not shapes); every panel, tile, chip, star and line of copy is native.
"""
import hashlib, os
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import deckkit as dk
import content as c
import poster as P

HERE = os.path.dirname(os.path.abspath(__file__))
ORN = os.path.join(HERE, "ornaments06")
os.makedirs(ORN, exist_ok=True)

RED, BLUE, CYAN, YELLOW = "E8352B", "2B4FD8", "35C5F0", "FFE400"
INK, WHITE, CREAM = "0C1024", "FFFFFF", "FFF6D8"
BODY, LABEL = "Poppins", "Poppins"

_cache = {}
def _png(name, maker):
    key = hashlib.md5(name.encode()).hexdigest()[:10]
    path = os.path.join(ORN, "%s.png" % key)
    if key not in _cache:
        if not os.path.exists(path):
            maker().save(path, optimize=True)
        _cache[key] = path
    return _cache[key]

def _jpg(name, maker):
    key = hashlib.md5(name.encode()).hexdigest()[:10]
    path = os.path.join(ORN, "%s.jpg" % key)
    if key not in _cache:
        if not os.path.exists(path):
            maker().convert("RGB").save(path, quality=86, optimize=True)
        _cache[key] = path
    return _cache[key]

def chrome(s, text, size, x, y, stops=None, gold=False):
    st = P.GOLD if gold else (stops or P.CHROME)
    tag = "c|%s|%s|%s" % (text, size, "gold" if gold else "chrome")
    path = _png(tag, lambda: P.chrome_text(text, size, stops=st))
    from PIL import Image
    im = Image.open(path)
    w = im.size[0] / P.S
    s.pic(path, x, y, w)
    return w, im.size[1] / P.S

def blob(s, x, y, w, h, alpha=215, blur=26):
    path = _png("b|%s|%s|%s|%s" % (w, h, alpha, blur),
                lambda: P.blob((w, h), alpha=alpha, blur=blur))
    from PIL import Image
    im = Image.open(path)
    s.pic(path, x - (im.size[0] / P.S - w) / 2, y - (im.size[1] / P.S - h) / 2,
          im.size[0] / P.S)

def ground(s, blocks, seed=3, blur=90):
    path = _jpg("g|%s|%s|%s" % (blocks, seed, blur),
                lambda: P.wash((1920, 1080), blocks, blur=blur, seed=seed))
    s.pic(path, 0, 0, 1920, 1080)
    gp = _png("grain", lambda: P.grain((1920, 1080), 22, seed=7))
    s.pic(gp, 0, 0, 1920, 1080)

def burst(s, x, y, size, fill=YELLOW, rot=0, points=10):
    col = tuple(int(fill[i:i + 2], 16) for i in (0, 2, 4))
    path = _png("bu|%s|%s|%s|%s" % (size, fill, rot, points),
                lambda: P.burst(size, fill=col, rot=rot, points=points))
    from PIL import Image
    im = Image.open(path)
    s.pic(path, x - im.size[0] / P.S / 2, y - im.size[1] / P.S / 2, im.size[0] / P.S)

def star(s, x, y, size, fill=WHITE, edge=BLUE, rot=0):
    f = tuple(int(fill[i:i + 2], 16) for i in (0, 2, 4))
    e = tuple(int(edge[i:i + 2], 16) for i in (0, 2, 4))
    path = _png("st|%s|%s|%s|%s" % (size, fill, edge, rot),
                lambda: P.star5(size, fill=f, edge=e, rot=rot))
    from PIL import Image
    im = Image.open(path)
    s.pic(path, x - im.size[0] / P.S / 2, y - im.size[1] / P.S / 2, im.size[0] / P.S)

def tile(s, x, y, w, h, label="drop photo", rot=0, border=7):
    path = _png("gl|%s|%s" % (w, h), lambda: P.glow_cut((w, h)))
    from PIL import Image
    im = Image.open(path)
    s.pic(path, x - (im.size[0] / P.S - w) / 2, y - (im.size[1] / P.S - h) / 2,
          im.size[0] / P.S)
    s.photo(x, y, w, h, label, fill="D9DEE8", line=WHITE, rot=rot, dash=False,
            label_color="6B7488", size=10)
    return x, y

def credit(s, text="ZAHRA LEVINA · PORTFOLIO 2026"):
    s.text(1180, 1024, 700, 34, text, font=LABEL, size=10, bold=True, color=WHITE,
           align=PP_ALIGN.RIGHT, tracking=4)

def panel(s, x, y, w, h, fill, alpha=None, line=WHITE, lw=5):
    return s.rect(x, y, w, h, fill=fill, line=line, lw=lw, alpha=alpha)


def build(deck):
    Q = [(0, 0, 960, 540, (232, 53, 43)), (960, 0, 1920, 540, (43, 79, 216)),
         (0, 540, 960, 1080, (255, 228, 0)), (960, 540, 1920, 1080, (53, 197, 240))]

    # 1 · cover -------------------------------------------------------------
    s = deck.new(); ground(s, Q, seed=3)
    blob(s, 60, 74, 980, 190)
    chrome(s, "ZAHRA", 116, 70, 60)
    chrome(s, "LEVINA", 84, 96, 216, gold=True)
    s.text(104, 366, 560, 40, c.KICKER, font=LABEL, size=15, bold=True, color=WHITE,
           tracking=6)
    s.text(104, 412, 520, 160, c.DISCIPLINES, font=BODY, size=17, italic=True,
           color=WHITE, spacing=1.5)
    panel(s, 96, 600, 580, 62, INK, line=None)
    s.text(96, 600, 580, 62, "PORTFOLIO / VOL.01", font=LABEL, size=15, bold=True,
           color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, tracking=5)
    tile(s, 1150, 200, 600, 740, "drop portrait")
    tile(s, 120, 706, 250, 200, "photo")
    tile(s, 400, 760, 220, 176, "photo", rot=-6)
    burst(s, 1046, 176, 190, YELLOW, rot=8)
    s.text(964, 138, 164, 78, "NEW\n2026", font=LABEL, size=13, bold=True, color=INK,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=1.1)
    star(s, 700, 640, 150, WHITE, BLUE, rot=8)
    star(s, 1810, 470, 110, RED, WHITE)
    star(s, 640, 300, 90, WHITE, RED, rot=-12)
    star(s, 1100, 980, 86, YELLOW, INK)
    credit(s)

    # 2 · about -------------------------------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (43, 79, 216)), (0, 0, 820, 1080, (232, 53, 43)),
               (1200, 0, 1920, 620, (53, 197, 240)), (0, 760, 900, 1080, (255, 228, 0))],
           seed=5)
    blob(s, 70, 70, 760, 150)
    chrome(s, "ABOUT ME", 78, 80, 60)
    s.text(96, 250, 720, 620, c.ABOUT, font=BODY, size=12.5, italic=True, color=WHITE,
           spacing=1.7, after=16)
    tile(s, 900, 180, 560, 700, "drop portrait")
    tile(s, 1520, 640, 300, 240, "photo", rot=5)
    panel(s, 900, 916, 560, 60, INK, line=None)
    s.text(900, 916, 560, 60, "CREATIVE · CONTENT · MARKETING", font=LABEL, size=14,
           bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
           tracking=4)
    star(s, 1490, 170, 120, WHITE, BLUE, rot=10)
    star(s, 830, 560, 96, YELLOW, INK)
    burst(s, 1810, 260, 150, RED, rot=14)
    credit(s)

    # 3 · what i do ---------------------------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (255, 228, 0)), (0, 0, 1920, 380, (232, 53, 43)),
               (1180, 300, 1920, 1080, (43, 79, 216))], seed=9)
    blob(s, 70, 66, 840, 160)
    chrome(s, "WHAT I DO", 82, 80, 56)
    cols = [RED, BLUE, CYAN, INK]
    for i, (title, sub) in enumerate(c.DO):
        x = 96 + (i % 2) * 900
        y = 320 + (i // 2) * 330
        panel(s, x, y, 820, 290, cols[i], lw=6)
        s.text(x + 34, y + 24, 200, 70, "0%d" % (i + 1), font=LABEL, size=34, bold=True,
               color=WHITE if i != 2 else INK, italic=True)
        s.text(x + 34, y + 104, 740, 80, title, font=LABEL, size=25, bold=True,
               color=WHITE if i != 2 else INK, italic=True)
        s.text(x + 36, y + 186, 740, 90, sub, font=BODY, size=13, italic=True,
               color=WHITE if i != 2 else INK, spacing=1.5)
    star(s, 1810, 210, 120, WHITE, RED, rot=-8)
    burst(s, 980, 300, 130, YELLOW, rot=20)
    credit(s)

    # 4 · experience --------------------------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (43, 79, 216)), (0, 0, 1920, 330, (12, 16, 36)),
               (0, 700, 760, 1080, (232, 53, 43)), (1500, 620, 1920, 1080, (53, 197, 240))],
           seed=11)
    chrome(s, "EXPERIENCE", 76, 80, 54)
    for i, (org, role) in enumerate(c.EXP):
        y = 320 + i * 132
        panel(s, 96, y, 1320, 112, WHITE if i % 2 == 0 else CREAM, line=INK, lw=4)
        s.rect(96, y, 22, 112, fill=[RED, YELLOW, CYAN, BLUE, RED][i])
        s.text(150, y + 16, 900, 44, org, font=LABEL, size=21, bold=True, color=INK,
               italic=True)
        s.text(152, y + 62, 1000, 36, role, font=BODY, size=12.5, italic=True,
               color="4A4F63")
        s.text(1250, y, 140, 112, "0%d" % (i + 1), font=LABEL, size=24, bold=True,
               color="B9BFD0", align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, italic=True)
    tile(s, 1490, 320, 330, 260, "photo", rot=4)
    tile(s, 1520, 640, 300, 250, "photo", rot=-5)
    star(s, 1450, 940, 120, YELLOW, INK, rot=12)
    burst(s, 1760, 190, 150, RED, rot=6)
    credit(s)

    # 5 · sawala space ------------------------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (53, 197, 240)), (0, 0, 1000, 1080, (255, 228, 0)),
               (1080, 0, 1920, 480, (232, 53, 43))], seed=13)
    blob(s, 70, 62, 1080, 170)
    chrome(s, "SAWALA SPACE", 74, 80, 54)
    tile(s, 110, 290, 620, 620, "drop photo")
    panel(s, 800, 290, 1020, 300, INK, line=WHITE, lw=6)
    s.text(838, 316, 940, 50, c.SAWALA_SUB, font=LABEL, size=17, bold=True, color=YELLOW,
           italic=True, tracking=2)
    s.text(838, 374, 940, 200, c.SAWALA_BODY, font=BODY, size=14, italic=True,
           color=WHITE, spacing=1.6)
    s.text(800, 618, 400, 40, "MY ROLE", font=LABEL, size=15, bold=True, color=INK,
           tracking=5)
    x, y = 800, 664
    for i, r in enumerate(c.SAWALA_ROLE):
        if i == 3:
            x, y = 800, 736
        x += s.pill(x, y, r.upper(), size=12, pad=20, h=56, fill=[RED, BLUE, CYAN][i % 3],
                    color=WHITE if i % 3 != 2 else INK, line=WHITE, font=LABEL,
                    tracking=2, radius=0.12) + 16
    tile(s, 800, 830, 320, 200, "event")
    tile(s, 1160, 830, 320, 200, "community")
    star(s, 1790, 690, 120, WHITE, BLUE, rot=-10)
    burst(s, 760, 240, 140, YELLOW, rot=16)
    credit(s)

    # 6 · selected works ----------------------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (232, 53, 43)), (0, 0, 1920, 300, (43, 79, 216)),
               (0, 660, 1920, 1080, (255, 228, 0))], seed=17)
    blob(s, 70, 56, 720, 150)
    chrome(s, "MY WORK", 74, 80, 48)
    s.text(860, 74, 1000, 110, c.WORKS_BODY, font=BODY, size=12, italic=True,
           color=WHITE, spacing=1.5)
    x0 = 96
    for i, tag in enumerate(c.WORKS_TAGS):
        x0 += s.pill(x0, 232, tag.upper(), size=11, pad=16, h=46,
                     fill=[YELLOW, WHITE, CYAN, INK][i],
                     color=INK if i != 3 else WHITE, line=INK if i != 3 else WHITE,
                     font=LABEL, tracking=2, radius=0.1) + 14
    for i, cap in enumerate(c.WORKS_CAPS):
        gx = 96 + (i % 4) * 442
        gy = 314 + (i // 4) * 352
        tile(s, gx, gy, 400, 250, cap, rot=(-4, 3, -2, 4)[i % 4])
        s.text(gx + 4, gy + 262, 340, 34, cap.upper(), font=LABEL, size=11, bold=True,
               color=WHITE if i < 4 else INK, tracking=3)
    star(s, 1850, 300, 110, WHITE, RED, rot=8)
    burst(s, 60, 640, 130, YELLOW, rot=-12)
    credit(s)

    # 7 · stretch for stray -------------------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (255, 228, 0)), (700, 0, 1920, 1080, (53, 197, 240)),
               (0, 0, 820, 420, (232, 53, 43))], seed=19)
    blob(s, 640, 58, 1180, 170)
    chrome(s, "STRETCH FOR STRAY", 62, 650, 52)
    s.text(660, 232, 900, 44, c.STRAY_SUB.upper(), font=LABEL, size=16, bold=True,
           color=INK, tracking=5)
    tile(s, 110, 260, 500, 660, "drop poster", rot=-3)
    panel(s, 660, 300, 1160, 150, INK, line=WHITE, lw=5)
    s.text(696, 300, 1090, 150, c.STRAY_BODY, font=BODY, size=16, italic=True,
           color=WHITE, anchor=MSO_ANCHOR.MIDDLE, spacing=1.45)
    s.text(660, 486, 500, 40, "MY CONTRIBUTION", font=LABEL, size=15, bold=True,
           color=INK, tracking=5)
    for i, it in enumerate(c.STRAY_LIST):
        y = 538 + i * 74
        panel(s, 660, y, 660, 60, WHITE, line=INK, lw=3)
        s.rect(660, y, 16, 60, fill=[RED, BLUE, YELLOW, CYAN, RED][i])
        s.text(700, y, 600, 60, it, font=BODY, size=13.5, italic=True, color=INK,
               anchor=MSO_ANCHOR.MIDDLE)
    tile(s, 1390, 540, 420, 300, "documentation", rot=4)
    star(s, 1840, 300, 110, YELLOW, INK, rot=-6)
    burst(s, 600, 220, 140, RED, rot=10)
    credit(s)

    # 8 · other works -------------------------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (43, 79, 216)), (0, 300, 1920, 1080, (53, 197, 240)),
               (1300, 0, 1920, 1080, (255, 228, 0))], seed=23)
    blob(s, 70, 58, 900, 160)
    chrome(s, "OTHER WORKS", 72, 80, 52)
    s.text(96, 240, 1200, 60, c.BEYOND_BODY, font=BODY, size=14, italic=True, color=WHITE,
           spacing=1.5)
    for i, (title, sub) in enumerate(c.BEYOND):
        x = 96 + i * 590
        panel(s, x, 350, 540, 600, [RED, INK, WHITE][i], lw=6,
              line=WHITE if i != 2 else INK)
        col = WHITE if i != 2 else INK
        tile(s, x + 30, 404, 480, 226, "photo")
        s.text(x + 32, 660, 480, 130, title, font=LABEL, size=21, bold=True, color=col,
               italic=True, spacing=1.2)
        s.text(x + 34, 804, 470, 120, sub, font=BODY, size=12, italic=True, color=col,
               spacing=1.5)
        s.text(x + 400, 356, 120, 44, "0%d" % (i + 1), font=LABEL, size=18, bold=True,
               color=col, italic=True, align=PP_ALIGN.RIGHT)
    star(s, 1850, 250, 110, RED, WHITE, rot=14)
    burst(s, 60, 980, 130, YELLOW, rot=8)
    credit(s)

    # 9 · skills & tools ----------------------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (53, 197, 240)), (0, 0, 1920, 360, (12, 16, 36)),
               (960, 360, 1920, 1080, (255, 228, 0))], seed=29)
    chrome(s, "SKILLS + TOOLS", 72, 80, 52)
    for i, (title, items) in enumerate(c.SKILLS):
        x = 96 + i * 900
        panel(s, x, 350, 820, 380, [RED, BLUE][i], lw=6)
        s.text(x + 32, 368, 600, 56, title.upper(), font=LABEL, size=22, bold=True,
               color=WHITE, italic=True, tracking=3)
        for j, it in enumerate(items):
            y = 442 + j * 68
            s.rect(x + 32, y, 756, 54, fill=WHITE)
            s.text(x + 60, y, 520, 54, it, font=BODY, size=13.5, italic=True, color=INK,
                   anchor=MSO_ANCHOR.MIDDLE)
            s.rect(x + 600, y + 20, 160, 14, fill="D9DEE8")
            s.rect(x + 600, y + 20, 160 - j * 16, 14, fill=[RED, BLUE][i])
    s.text(96, 772, 400, 44, "TOOLS", font=LABEL, size=18, bold=True, color=INK,
           tracking=5)
    x, y = 96, 826
    for i, t in enumerate(c.TOOLS):
        if i == 4:
            x, y = 96, 908
        x += s.pill(x, y, t.upper(), size=12, pad=18, h=62,
                    fill=[RED, BLUE, CYAN, INK, WHITE, RED, BLUE][i],
                    color=INK if i in (2, 4) else WHITE, line=INK, font=LABEL,
                    tracking=2, radius=0.1) + 16
    star(s, 1840, 640, 120, WHITE, RED, rot=-10)
    burst(s, 1700, 180, 150, YELLOW, rot=12)
    credit(s)

    # 10 · contact ----------------------------------------------------------
    s = deck.new()
    ground(s, [(0, 0, 1920, 1080, (232, 53, 43)), (0, 0, 1920, 520, (43, 79, 216)),
               (0, 520, 1920, 1080, (255, 228, 0)), (1240, 0, 1920, 1080, (53, 197, 240))],
           seed=31)
    blob(s, 90, 150, 1320, 320)
    chrome(s, "LET'S WORK", 96, 100, 140)
    chrome(s, "TOGETHER", 96, 150, 300, gold=True)
    s.text(110, 486, 980, 160, c.END_BODY, font=BODY, size=14, italic=True, color=WHITE,
           spacing=1.6)
    for i, (lab, val) in enumerate(c.CONTACT):
        y = 664 + i * 106
        panel(s, 96, y, 900, 90, [WHITE, INK, WHITE][i], line=INK, lw=4)
        s.rect(96, y, 20, 90, fill=[RED, YELLOW, CYAN][i])
        s.text(150, y, 300, 90, lab.upper(), font=LABEL, size=16, bold=True,
               color=INK if i != 1 else YELLOW, anchor=MSO_ANCHOR.MIDDLE, tracking=3,
               italic=True)
        s.text(440, y, 520, 90, val, font=BODY, size=14, italic=True,
               color=INK if i != 1 else WHITE, anchor=MSO_ANCHOR.MIDDLE)
    tile(s, 1120, 240, 580, 640, "drop photo", rot=3)
    burst(s, 1006, 948, 200, YELLOW, rot=14)
    s.text(918, 914, 176, 78, "THX 4\nLOOKN", font=LABEL, size=14, bold=True, color=INK,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=1.1)
    star(s, 1850, 190, 120, WHITE, BLUE, rot=8)
    star(s, 1020, 170, 96, RED, WHITE, rot=-14)
    credit(s)
    return deck
