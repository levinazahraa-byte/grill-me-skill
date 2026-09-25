# -*- coding: utf-8 -*-
"""Zahra Levina — 2026 portfolio. "Angel" direction.

Y2K fashion editorial first: tonal pink, black lace, leopard, rhinestone and
chrome-script lettering, pearl strings, butterflies. Interface elements appear
only where they serve the story, dressed in the same palette.

Every graphic is placed as its OWN layer (a separate PNG), so the deck opens in
Canva or PowerPoint as movable objects rather than a flattened picture. Body
copy stays live text.
"""

import hashlib, math, os
from PIL import Image
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE

import y2k as y
from y2k import (font, u, S, MAGENTA, ROSE, BLUSH, SHELL, NOIR, PEARL, ICE,
                 ITALIANA, BODONI, CORMORANT, PINYON, ALLURA, OSWALD, ARCHIVO,
                 ARCHIVO_BLACK, SILK, SILKB)

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "assets", "slides")
ELEM = os.path.join(HERE, "assets", "elements")
for d in (ART, ELEM):
    os.makedirs(d, exist_ok=True)

INK, MUTE, PINK_HEX = "100A16", "7A6478", "FF2E93"
BODY_F = "Trebuchet MS"

def px(v):
    return Emu(int(round(v * 6350)))

prs = Presentation()
prs.slide_width, prs.slide_height = px(1920), px(1080)
BLANK = prs.slide_layouts[6]

_written = {}

def _save_element(img, name):
    data = img.tobytes()
    key = hashlib.md5(data + str(img.size).encode()).hexdigest()[:12]
    if key in _written:
        return _written[key]
    path = os.path.join(ELEM, "%s_%s.png" % (name, key))
    img.save(path, optimize=True)
    _written[key] = path
    return path


class Slide(object):
    """Collects a flattened background plus an ordered stack of live layers."""

    def __init__(self, idx, bg=None):
        self.idx = idx
        self.bg = Image.new("RGBA", (y.W, y.H), SHELL + (255,))
        if bg is not None:
            y.paste(self.bg, bg, (0, 0))
        self.layers = []

    # --- background (textures only; flattened into one image) ---
    def wash(self, img, xy=(0, 0)):
        y.paste(self.bg, img, xy)

    # --- layers ---
    def el(self, img, xy, anchor="tl", name="el", rot=None):
        if rot:
            img = img.rotate(rot, resample=Image.BICUBIC, expand=True)
        x, yy = xy
        if anchor in ("c", "tc"):
            x -= img.size[0] / S / 2
        if anchor == "c":
            yy -= img.size[1] / S / 2
        self.layers.append(("img", img, x, yy, name))
        return img.size[0] / S, img.size[1] / S

    def slot(self, cx, cy, w, h, rot=0):
        self.layers.append(("slot", dict(cx=cx, cy=cy, w=w, h=h, rot=rot)))

    def text(self, x, yy, w, h, text, size=13.5, bold=False, color=INK,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.5, after=10,
             font_name=None):
        self.layers.append(("text", dict(x=x, y=yy, w=w, h=h, text=text, size=size,
                                         bold=bold, color=color, align=align,
                                         anchor=anchor, spacing=spacing, after=after,
                                         font_name=font_name or BODY_F)))

    # --- composition helpers ---
    def framed_slot(self, pos, size, stone=15, color=MAGENTA, caption=None, tilt=0):
        fr, inner = y.gem_frame(size, stone=stone, color=color, fill=(243, 238, 246))
        self.el(fr, pos, name="gemframe", rot=tilt)
        cx = pos[0] + ((inner[0] + inner[2]) / 2) / S
        cy = pos[1] + ((inner[1] + inner[3]) / 2) / S
        self.slot(cx, cy, (inner[2] - inner[0]) / S, (inner[3] - inner[1]) / S, -tilt)
        if caption:
            self.el(y.tracked(caption.upper(), font(SILK, 11), (150, 128, 150), tracking=3),
                    (cx, pos[1] + size[1] + 16), anchor="tc", name="caption")
        return cx, cy

    def panel(self, size, pos, **kw):
        """Glass panel positioned by its visible rectangle (the bitmap carries pad)."""
        self.el(y.glass_panel(size, **kw), (pos[0] - 18, pos[1] - 18), name="panel")

    def pill(self, text, pos, height=46, pad=42, tint=(255, 238, 247), color=MAGENTA, size=13):
        w = pad + len(text) * 12.5
        self.panel((w, height), pos, radius=height / 2, tint=tint, alpha=244)
        self.el(y.tracked(text, font(OSWALD, size), color, tracking=5),
                (pos[0] + w / 2, pos[1] + (height - 22) / 2), anchor="tc", name="pilltext")
        return w

    def hairline(self, x, yy, length, color=NOIR, weight=1.1, vertical=False):
        self.el(y.hairline(length, color, weight, horizontal=not vertical), (x, yy), name="rule")

    def label(self, x, yy, text, size=17, color=NOIR, tracking=8, fnt=OSWALD, anchor="tl"):
        return self.el(y.tracked(text, font(fnt, size), color, tracking=tracking),
                       (x, yy), anchor=anchor, name="label")

    def jewels(self, items):
        for spec in items:
            kind = spec[0]
            if kind == "gem":
                _, size, pos, col, cut, rot = spec
                self.el(y.gem(size, col, cut=cut, rot=rot), pos, anchor="c", name="gem")
            elif kind == "sparkle":
                _, size, pos, col = spec
                self.el(y.sparkle(size, col, glow_c=ROSE), pos, anchor="c", name="sparkle")
            elif kind == "butterfly":
                _, size, pos, c1, c2, rot = spec
                self.el(y.butterfly(size, c1, c2, rot=rot), pos, anchor="c", name="butterfly")
            elif kind == "pearl":
                _, length, pos, bead, arc, rot = spec
                self.el(y.pearl_string(length, bead, arc=arc), pos, anchor="c",
                        name="pearls", rot=rot)
            elif kind == "obj":
                _, ch, size, pos, rot = spec
                self.el(y.emoji(ch, size, rot=rot), pos, anchor="c", name="object")

    # --- output ---
    def build(self):
        bgp = os.path.join(ART, "s%02d.jpg" % self.idx)
        self.bg.convert("RGB").save(bgp, quality=94, optimize=True)
        sl = prs.slides.add_slide(BLANK)
        sl.shapes.add_picture(bgp, px(0), px(0), px(1920), px(1080))
        for layer in self.layers:
            if layer[0] == "img":
                _, img, x, yy, name = layer
                path = _save_element(img, name)
                sl.shapes.add_picture(path, px(x), px(yy),
                                      px(img.size[0] / S), px(img.size[1] / S))
            elif layer[0] == "slot":
                d = layer[1]
                shp = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(d["cx"] - d["w"] / 2),
                                          px(d["cy"] - d["h"] / 2), px(d["w"]), px(d["h"]))
                shp.shadow.inherit = False
                shp.fill.solid()
                shp.fill.fore_color.rgb = RGBColor.from_string("F3EEF6")
                shp.line.color.rgb = RGBColor.from_string("FF2E93")
                shp.line.width = Pt(1)
                shp.line.dash_style = MSO_LINE_DASH_STYLE.DASH
                if d["rot"]:
                    shp.rotation = d["rot"]
                p = shp.text_frame.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                r = p.add_run()
                r.text = "drop photo"
                r.font.name = BODY_F
                r.font.size = Pt(9)
                r.font.color.rgb = RGBColor.from_string("B99BB3")
            else:
                d = layer[1]
                tb = sl.shapes.add_textbox(px(d["x"]), px(d["y"]), px(d["w"]), px(d["h"]))
                tf = tb.text_frame
                tf.word_wrap = True
                tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
                tf.vertical_anchor = d["anchor"]
                lines = d["text"] if isinstance(d["text"], (list, tuple)) else [d["text"]]
                for i, t in enumerate(lines):
                    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                    p.alignment = d["align"]
                    p.line_spacing = d["spacing"]
                    p.space_after = Pt(d["after"] if len(lines) > 1 else 0)
                    r = p.add_run()
                    r.text = t
                    r.font.name = d["font_name"]
                    r.font.size = Pt(d["size"])
                    r.font.bold = d["bold"]
                    r.font.color.rgb = RGBColor.from_string(d["color"])
        return sl


def page_marks(s, n, title):
    """Editorial furniture: corner rules and a folio."""
    s.hairline(96, 62, 1728, NOIR, 1)
    s.hairline(96, 1018, 1728, NOIR, 1)
    s.label(96, 30, title.upper(), 13, NOIR, 9)
    s.label(1824, 30, "%02d" % n, 13, MAGENTA, 6, fnt=ITALIANA, anchor="tr")


# ============================================================ 1 — the cover
def slide01():
    s = Slide(1, y.linear_gradient((y.W, y.H), [(0, BLUSH), (.45, SHELL), (1, (255, 226, 241))]))
    s.wash(y.feather(y.halftone((y.W, u(520)), ROSE, SHELL).convert("RGBA"), t=u(360)), (0, 520))
    s.wash(y.leopard_chic((y.W, u(108))), (0, 0))
    s.wash(y.lace_black(y.W, u(46)), (0, 104))
    s.wash(y.leopard_chic((y.W, u(76)), seed=14), (0, 1004))
    s.wash(y.lace_black(y.W, u(46), flip=True), (0, 960))

    s.label(960, 176, "2026 PORTFOLIO", 26, NOIR, 22, fnt=ITALIANA, anchor="tc")
    s.el(y.hairline(280, MAGENTA, 1.4), (820, 222), name="rule")
    s.label(960, 244, "CREATIVE · CONTENT · MARKETING · VISUAL COMMUNICATION",
            14, MAGENTA, 8, anchor="tc")

    s.framed_slot((656, 282), (608, 496), stone=17)
    s.el(y.jewel_outline(y.script("Zahra", 158), stone=23), (960, 602), anchor="tc",
         name="wordmark")
    s.label(960, 818, "L E V I N A", 46, NOIR, 22, fnt=ITALIANA, anchor="tc")
    s.el(y.tracked("WHATSAPP  ·  EMAIL  ·  LINKEDIN", font(SILK, 12), (150, 120, 142),
                   tracking=4), (960, 896), anchor="tc", name="contact")

    s.jewels([
        ("butterfly", 152, (560, 386), MAGENTA, ROSE, -16),
        ("butterfly", 104, (1382, 344), ROSE, BLUSH, 14),
        ("butterfly", 76, (1330, 800), ICE, (150, 205, 232), -8),
        ("gem", 62, (1318, 262), MAGENTA, "heart", 0),
        ("gem", 48, (608, 572), ROSE, "marquise", 20),
        ("gem", 44, (1344, 560), MAGENTA, "round", 0),
        ("gem", 40, (612, 790), ICE, "round", 0),
        ("gem", 36, (1320, 742), MAGENTA, "heart", 0),
        ("sparkle", 46, (486, 556), (255, 255, 255)),
        ("sparkle", 36, (1442, 470), (255, 255, 255)),
        ("sparkle", 28, (656, 274), (255, 255, 255)),
        ("pearl", 300, (300, 560), 24, 26, -8),
        ("pearl", 300, (1620, 570), 24, 26, 8),
        ("obj", "\U0001F4BF", 92, (318, 318), -12),
        ("obj", "\U0001F4F1", 86, (1608, 300), 10),
        ("obj", "\U0001F4F7", 88, (306, 822), 8),
        ("obj", "\U0001F484", 78, (1626, 830), -10),
    ])
    return s.build()


# ============================================================ 2 — about
def slide02():
    s = Slide(2, y.linear_gradient((y.W, y.H), [(0, SHELL), (1, (255, 240, 248))]))
    s.wash(y.feather(y.halftone((u(760), u(620)), ROSE, SHELL).convert("RGBA"),
                     r=u(420), b=u(380)), (0, 0))
    page_marks(s, 2, "about")

    s.label(140, 168, "HI, I'M", 58, NOIR, 18, fnt=ITALIANA)
    s.el(y.script("Zahra", 118), (128, 236), name="script")
    s.hairline(140, 430, 620, MAGENTA, 1.4)
    s.label(140, 456, "CREATIVE · MARKETING · COMMUNITY", 14, MAGENTA, 7)

    s.text(140, 508, 870, 420, [
        "I'm a creative and marketing enthusiast with experience in content creation, social media, graphic design, event management, and brand partnerships.",
        "With a background in agricultural community development, I've had the opportunity to work across different environments—from student organizations and research projects to building a wellness community through Sawala Space.",
        "I enjoy turning ideas into clear, engaging, and purposeful creative work.",
    ], size=11.5, spacing=1.8, after=14)

    s.framed_slot((1120, 180), (560, 700), stone=16, caption="portrait.jpg")
    s.jewels([
        ("pearl", 380, (1400, 160), 22, 20, 0),
        ("butterfly", 120, (1096, 268), MAGENTA, ROSE, -18),
        ("butterfly", 72, (1714, 786), ROSE, BLUSH, 12),
        ("gem", 44, (1706, 232), MAGENTA, "marquise", 70),
        ("gem", 34, (1080, 736), MAGENTA, "round", 0),
        ("sparkle", 38, (1044, 520), (255, 255, 255)),
        ("obj", "\U0001F4AC", 66, (912, 880), -8),
    ])
    s.el(y.tracked("ABOUT_ZAHRA.TXT", font(SILK, 11), (170, 146, 168), tracking=3), (140, 978),
         name="filelabel")
    return s.build()


# ============================================================ 3 — what i do
def slide03():
    s = Slide(3, y.linear_gradient((y.W, y.H), [(0, SHELL), (1, (255, 238, 247))]))
    s.wash(y.feather(y.halftone((u(880), y.H), ROSE, SHELL).convert("RGBA"), l=u(480)),
           (1040, 0))
    page_marks(s, 3, "services")

    s.label(140, 136, "WHAT I DO", 76, NOIR, 16, fnt=ITALIANA)
    s.hairline(140, 268, 1080, NOIR, 1.2)
    s.label(140, 292, "FOUR WAYS I WORK", 14, MAGENTA, 8)

    rows = [("01", "CONTENT & SOCIAL MEDIA", "Content creation · social media · copywriting"),
            ("02", "CREATIVE & VISUAL", "Graphic design · visual communication · campaign materials"),
            ("03", "MARKETING & EVENTS", "Campaign development · event management · brand partnerships"),
            ("04", "COMMUNICATION", "Community engagement · collaboration · project coordination")]
    for i, (num, title, sub) in enumerate(rows):
        ry = 372 + i * 158
        s.el(y.grad_text(num, font(BODONI, 62), [(0, ROSE), (1, MAGENTA)], outline=0,
                         rim=0, shadow=0, gloss=False), (142, ry - 14), name="numeral")
        s.label(296, ry + 6, title, 22, NOIR, 10)
        s.text(298, ry + 52, 880, 56, sub, size=12, color=MUTE, spacing=1.4)
        s.el(y.gem(24, MAGENTA), (274, ry + 26), anchor="c", name="gem")
        if i < 3:
            s.hairline(140, ry + 116, 1080, (222, 200, 216), 1)

    s.el(y.gem_heart(230), (1500, 250), anchor="tc", name="gemheart")
    s.jewels([
        ("butterfly", 132, (1320, 600), MAGENTA, ROSE, -14),
        ("butterfly", 86, (1664, 700), ROSE, BLUSH, 16),
        ("pearl", 320, (1500, 810), 24, 24, 0),
        ("gem", 44, (1300, 302), MAGENTA, "marquise", 110),
        ("gem", 36, (1712, 400), ICE, "round", 0),
        ("sparkle", 42, (1660, 180), (255, 255, 255)),
        ("sparkle", 30, (1288, 460), (255, 255, 255)),
        ("gem", 30, (1400, 896), ROSE, "round", 0),
        ("gem", 26, (1600, 908), MAGENTA, "marquise", 50),
        ("sparkle", 26, (1500, 880), (255, 255, 255)),
    ])
    return s.build()


# ============================================================ 4 — experience
def slide04():
    s = Slide(4, y.linear_gradient((y.W, y.H), [(0, (255, 236, 246)), (1, SHELL)]))
    s.wash(y.feather(y.halftone((u(820), u(560)), ROSE, (255, 236, 246)).convert("RGBA"),
                     r=u(460), b=u(340)), (0, 0))
    page_marks(s, 4, "experience")

    s.label(140, 126, "WHERE I'VE BEEN", 58, NOIR, 14, fnt=ITALIANA)
    win, body = y.chic_window((1500, 700), "experience.exe", accent=MAGENTA)
    s.el(win, (196, 250), name="window")
    bx = 196 + body[0] / S
    by = 250 + body[1] / S
    inner_w = (body[2] - body[0]) / S

    orgs = [("SAWALA SPACE", "Co-Founder · Creative & Marketing"),
            ("KEMENTERIAN PERTANIAN RI", "Intern · Administration & Partnership Support"),
            ("IPB UNIVERSITY", "Research Assistant"),
            ("NABILA FARM LEMBANG", "Intern · Agriculture & Content Creation"),
            ("HIMPUNAN MAHASISWA PPP", "Head of Media & Branding")]
    for i, (org, role) in enumerate(orgs):
        ry = by + 40 + i * 126
        s.el(y.gem(24, MAGENTA if i % 2 == 0 else ROSE), (bx + 58, ry + 28), anchor="c", name="gem")
        s.label(bx + 100, ry + 8, org, 21, NOIR, 9)
        s.text(bx + 102, ry + 52, 900, 44, role, size=12.5, color=MUTE)
        s.el(y.tracked("0%d" % (i + 1), font(ITALIANA, 22), (214, 180, 206), tracking=4),
             (bx + inner_w - 70, ry + 14), name="rownum")
        if i < 4:
            s.hairline(bx + 56, ry + 100, inner_w - 120, (232, 212, 228), 1)

    s.jewels([
        ("pearl", 420, (430, 246), 22, 26, -6),
        ("butterfly", 118, (1720, 306), MAGENTA, ROSE, 16),
        ("butterfly", 70, (250, 872), ROSE, BLUSH, -12),
        ("gem", 40, (1776, 660), MAGENTA, "heart", 0),
        ("gem", 32, (148, 630), ICE, "round", 0),
        ("sparkle", 36, (1792, 496), (255, 255, 255)),
        ("obj", "\U0001F4BE", 72, (150, 320), -10),
    ])
    return s.build()


# ============================================================ 5 — sawala space
def slide05():
    s = Slide(5, y.linear_gradient((y.W, y.H), [(0, SHELL), (1, (255, 235, 245))]))
    s.wash(y.leopard_chic((u(132), y.H), seed=22), (0, 0))
    s.wash(y.lace_black(y.H, u(44)).rotate(-90, expand=True), (128, 0))
    s.wash(y.feather(y.halftone((u(700), u(520)), ROSE, SHELL).convert("RGBA"),
                     l=u(380), t=u(300)), (1220, 560))
    s.label(1824, 30, "05", 13, MAGENTA, 6, fnt=ITALIANA, anchor="tr")

    s.el(y.glass_panel((1560, 800), radius=22), (248, 132), name="panel")
    s.el(y.glass_panel((1160, 46), radius=23, tint=(255, 255, 255), alpha=235), (300, 190),
         name="urlbar")
    s.el(y.tracked("HTTP://WWW.SAWALASPACE.COM", font(SILK, 12), (168, 142, 166), tracking=3),
         (340, 206), name="url")
    for i in range(3):
        s.el(y.pearl(18), (300 + i * 30, 204), name="dot")

    s.el(y.script("Sawala Space", 84), (306, 258), name="logo")
    s.label(320, 414, "WELLNESS COMMUNITY & EVENT ORGANIZER", 15, MAGENTA, 8)
    s.hairline(320, 456, 640, NOIR, 1.2)
    s.text(320, 492, 690, 250,
           "As a co-founder, I contribute to the creative and marketing side of Sawala Space, from developing event concepts and promotional content to managing brand partnerships and supporting event execution.",
           size=12, spacing=1.8)

    s.label(320, 740, "MY ROLE", 14, NOIR, 9)
    for row, group in enumerate([["CONTENT", "SOCIAL MEDIA", "CAMPAIGN"],
                                 ["EVENT", "PARTNERSHIP", "BRANDING"]]):
        widths = [42 + len(r) * 12.5 for r in group]
        gap = (690 - sum(widths)) / (len(group) - 1)
        rx, ry = 320, 786 + row * 62
        for r, wv in zip(group, widths):
            s.pill(r, (rx, ry))
            rx += wv + gap

    s.framed_slot((1090, 250), (520, 330), stone=14, caption="sawala_space.jpg")
    s.framed_slot((1090, 640), (250, 250), stone=13, caption="event.jpg")
    s.framed_slot((1360, 640), (250, 250), stone=13, caption="community.jpg")
    s.jewels([
        ("butterfly", 104, (1074, 236), MAGENTA, ROSE, -16),
        ("gem", 40, (1626, 252), MAGENTA, "heart", 0),
        ("gem", 30, (1340, 606), ROSE, "round", 0),
        ("sparkle", 34, (1640, 612), (255, 255, 255)),
        ("pearl", 300, (1350, 950), 20, 18, 0),
    ])
    return s.build()


# ============================================================ 6 — selected works
def slide06():
    s = Slide(6, y.linear_gradient((y.W, y.H), [(0, SHELL), (1, (255, 241, 248))]))
    page_marks(s, 6, "selected works")
    s.label(140, 120, "SELECTED WORKS", 60, NOIR, 14, fnt=ITALIANA)
    s.hairline(140, 226, 1640, NOIR, 1.2)
    s.label(140, 250, "SOCIAL MEDIA · EVENT VISUALS · PROMOTIONAL MATERIALS · BRANDING",
            13, MAGENTA, 7)
    s.text(1160, 112, 640, 104,
           "A selection of social media content, event materials, promotional visuals, and other creative work I've developed across different projects.",
           size=10.5, color=MUTE, spacing=1.5)

    caps = ["ig carousel", "event poster", "reels cover", "brand kit",
            "feed layout", "promo flyer", "campaign visual", "merch design"]
    for i, cap in enumerate(caps):
        gx = 140 + (i % 4) * 412
        gy = 324 + (i // 4) * 352
        hero = i in (0, 5)
        s.framed_slot((gx, gy), (368, 256), stone=14 if hero else 11,
                      color=MAGENTA if hero else ROSE, caption=cap)
    s.jewels([
        ("butterfly", 96, (1826, 470), MAGENTA, ROSE, 18),
        ("butterfly", 64, (116, 690), ROSE, BLUSH, -14),
        ("gem", 34, (552, 660), MAGENTA, "heart", 0),
        ("gem", 26, (1376, 300), MAGENTA, "round", 0),
        ("sparkle", 30, (964, 662), (255, 255, 255)),
        ("sparkle", 24, (1790, 292), (255, 255, 255)),
    ])
    return s.build()


# ============================================================ 7 — stretch for stray
def slide07():
    s = Slide(7)
    s.wash(y.linear_gradient((y.W, y.H), [(0, SHELL), (1, (255, 240, 248))]))
    s.wash(y.linear_gradient((u(880), y.H), [(0, (255, 92, 174)), (1, MAGENTA)]), (0, 0))
    s.wash(y.feather(y.halftone((u(880), u(520)), (255, 170, 214), MAGENTA).convert("RGBA"),
                     t=u(360)), (0, 560))
    s.wash(y.lace_black(y.H, u(40)).rotate(90, expand=True), (840, 0))
    s.label(1824, 30, "07", 13, MAGENTA, 6, fnt=ITALIANA, anchor="tr")

    s.framed_slot((140, 210), (580, 660), stone=16, color=(255, 255, 255), caption=None)
    s.el(y.tracked("POSTER_FINAL.JPG", font(SILK, 11), (255, 214, 236), tracking=3),
         (430, 890), anchor="tc", name="caption")

    s.label(960, 180, "WELLNESS × SOCIAL IMPACT", 14, MAGENTA, 9)
    s.el(y.grad_text("STRETCH", font(BODONI, 84), [(0, NOIR), (1, NOIR)], outline=0, rim=0,
                     shadow=0, gloss=False), (952, 216), name="title")
    s.el(y.script("for stray", 96), (952, 340), name="scripttitle")
    s.hairline(960, 500, 760, NOIR, 1.2)
    s.text(960, 530, 500, 110,
           "A wellness event combining movement, community, and support for animal welfare.",
           size=13, spacing=1.6)

    s.label(960, 676, "MY CONTRIBUTION", 14, MAGENTA, 9)
    for i, it in enumerate(["Campaign concept", "Event promotion", "Social media content",
                            "Partnership communication", "Event coordination"]):
        iy = 720 + i * 52
        s.el(y.gem(18, MAGENTA if i % 2 == 0 else ROSE), (972, iy + 16), anchor="c", name="gem")
        s.text(1002, iy, 480, 42, it, size=12.5, anchor=MSO_ANCHOR.MIDDLE)

    s.framed_slot((1520, 690), (250, 190), stone=12, caption="documentation")
    s.framed_slot((1520, 430), (250, 190), stone=12, caption="social post")
    s.jewels([
        ("butterfly", 124, (806, 300), (255, 255, 255), BLUSH, -16),
        ("butterfly", 78, (1646, 300), MAGENTA, ROSE, 14),
        ("gem", 48, (784, 640), (255, 255, 255), "heart", 0),
        ("gem", 34, (806, 860), (255, 255, 255), "round", 0),
        ("sparkle", 40, (742, 176), (255, 255, 255)),
        ("sparkle", 30, (1836, 606), (255, 255, 255)),
        ("obj", "\U0001F43E", 70, (172, 950), -12),
        ("gem", 40, (660, 950), (255, 255, 255), "heart", 0),
        ("pearl", 260, (420, 952), 20, 16, 0),
    ])
    return s.build()


# ============================================================ 8 — beyond
def slide08():
    s = Slide(8, y.linear_gradient((y.W, y.H), [(0, (255, 238, 247)), (1, SHELL)]))
    s.wash(y.feather(y.halftone((y.W, u(420)), ROSE, SHELL).convert("RGBA"), b=u(300)), (0, 0))
    s.wash(y.leopard_chic((y.W, u(104)), seed=33), (0, 976))
    s.wash(y.lace_black(y.W, u(46), flip=True), (0, 932))
    s.label(1824, 30, "08", 13, MAGENTA, 6, fnt=ITALIANA, anchor="tr")

    s.label(140, 118, "BEYOND", 56, NOIR, 16, fnt=ITALIANA)
    s.el(y.script("creative work", 76), (470, 100), name="script")
    s.hairline(140, 246, 1000, NOIR, 1.2)
    s.text(140, 272, 1180, 60,
           "My creative experience also grew through student organizations, academic projects, and collaborative work.",
           size=13, color=MUTE)

    blocks = [("HIMPUNAN MAHASISWA PPP", "Head of Media & Branding", -2, MAGENTA),
              ("PEKAN SENI BUDAYA IPB", "Vice Head / Staff DKV", 1.5, ROSE),
              ("ACADEMIC & RESEARCH PROJECTS", "Visual communication · presentation · documentation",
               -1, MAGENTA)]
    for i, (title, sub, tilt, col) in enumerate(blocks):
        cx = 140 + i * 552
        cy = 396 + (12 if i == 1 else 0)
        s.el(y.glass_panel((500, 400), radius=16), (cx - 18, cy - 18), name="card", rot=tilt)
        s.el(y.gem(30, col, cut="heart"), (cx + 56, cy + 62), anchor="c", name="gem")
        s.text(cx + 48, cy + 110, 400, 130, title, size=15, bold=True, spacing=1.35,
               font_name="Trebuchet MS")
        s.el(y.hairline(180, MAGENTA, 1.2), (cx + 48, cy + 244), name="rule")
        s.text(cx + 48, cy + 272, 400, 110, sub, size=12, color=MUTE, spacing=1.5)
    s.jewels([
        ("pearl", 340, (960, 366), 20, 16, 0),
        ("butterfly", 92, (1700, 300), MAGENTA, ROSE, 15),
        ("butterfly", 60, (108, 560), ROSE, BLUSH, -12),
        ("sparkle", 34, (1786, 560), (255, 255, 255)),
        ("gem", 28, (860, 880), MAGENTA, "round", 0),
    ])
    return s.build()


# ============================================================ 9 — skills
def slide09():
    s = Slide(9, y.linear_gradient((y.W, y.H), [(0, SHELL), (1, (255, 237, 246))]))
    s.wash(y.feather(y.halftone((u(820), u(560)), ROSE, SHELL).convert("RGBA"),
                     l=u(460), b=u(340)), (1100, 0))
    page_marks(s, 9, "skills & tools")
    s.label(140, 126, "SKILLS", 62, NOIR, 16, fnt=ITALIANA)
    s.el(y.script("& tools", 82), (450, 112), name="script")
    s.hairline(140, 258, 1640, NOIR, 1.2)

    cols = [("CREATIVE", ["Graphic Design", "Copywriting", "Content Creation",
                          "Visual Communication"], MAGENTA),
            ("MARKETING", ["Social Media", "Campaign Development", "Event Management",
                           "Partnership"], ROSE)]
    for i, (title, items, col) in enumerate(cols):
        cx = 140 + i * 860
        s.label(cx, 306, title, 20, MAGENTA, 10)
        s.el(y.hairline(300, MAGENTA, 1.2), (cx, 348), name="rule")
        for j, it in enumerate(items):
            ry = 392 + j * 74
            s.el(y.gem(20, col, cut="marquise" if j % 2 else "round", rot=j * 20),
                 (cx + 14, ry + 22), anchor="c", name="gem")
            s.text(cx + 48, ry, 460, 48, it, size=13.5, anchor=MSO_ANCHOR.MIDDLE)

    s.label(140, 690, "TOOLS", 20, MAGENTA, 10)
    s.el(y.hairline(1640, (226, 204, 220), 1), (140, 732), name="rule")
    for row, group in enumerate([["CANVA", "ADOBE ILLUSTRATOR", "ADOBE PHOTOSHOP", "CAPCUT"],
                                 ["MICROSOFT OFFICE", "GOOGLE WORKSPACE", "MINITAB"]]):
        widths = [42 + len(t) * 12.5 for t in group]
        gap = (1640 - sum(widths)) / (len(group) - 1)
        tx, ty = 140, 772 + row * 76
        for t, wv in zip(group, widths):
            s.pill(t, (tx, ty), height=50, color=NOIR)
            tx += wv + gap
    s.jewels([
        ("butterfly", 104, (1716, 400), MAGENTA, ROSE, 16),
        ("butterfly", 62, (1846, 812), ROSE, BLUSH, -12),
        ("gem", 42, (1610, 180), MAGENTA, "heart", 0),
        ("sparkle", 36, (1790, 250), (255, 255, 255)),
        ("pearl", 260, (1690, 600), 20, 16, 0),
        ("gem", 34, (1560, 560), ROSE, "round", 0),
        ("gem", 28, (1830, 660), MAGENTA, "marquise", 40),
        ("sparkle", 30, (1470, 640), (255, 255, 255)),
    ])
    return s.build()


# ============================================================ 10 — contact
def slide10():
    s = Slide(10, y.linear_gradient((y.W, y.H), [(0, (255, 228, 243)), (.5, SHELL),
                                                 (1, (255, 224, 241))]))
    s.wash(y.feather(y.halftone((y.W, u(460)), ROSE, SHELL).convert("RGBA"), t=u(320)), (0, 600))
    s.wash(y.leopard_chic((y.W, u(108)), seed=41), (0, 0))
    s.wash(y.lace_black(y.W, u(48)), (0, 104))
    s.wash(y.leopard_chic((y.W, u(72)), seed=55), (0, 1008))
    s.wash(y.lace_black(y.W, u(46), flip=True), (0, 964))

    s.el(y.gem_heart(210), (960, 206), anchor="tc", name="gemheart")
    s.label(960, 418, "LET'S WORK", 44, NOIR, 20, fnt=ITALIANA, anchor="tc")
    s.el(y.jewel_outline(y.script("together", 128), stone=19), (960, 468), anchor="tc",
         name="wordmark")
    s.label(960, 660, "Z A H R A   L E V I N A", 22, NOIR, 12, fnt=ITALIANA, anchor="tc")
    s.el(y.hairline(360, MAGENTA, 1.4), (780, 704), name="rule")
    s.text(490, 726, 940, 90,
           "Thank you for taking the time to explore my work. I'm always open to new creative opportunities, collaborations, and projects.",
           size=12, align=PP_ALIGN.CENTER, spacing=1.6)

    contacts = [("WHATSAPP", "+62 8xx-xxxx-xxxx"), ("EMAIL", "hello@email.com"),
                ("LINKEDIN", "linkedin.com/in/username")]
    for i, (lab, val) in enumerate(contacts):
        cx = 420 + i * 380
        s.el(y.glass_panel((320, 92), radius=20), (cx - 18, 824), name="card")
        s.el(y.tracked(lab, font(OSWALD, 14), MAGENTA, tracking=6), (cx + 160, 864),
             anchor="tc", name="clabel")
        s.text(cx, 892, 320, 34, val, size=11.5, align=PP_ALIGN.CENTER, color=MUTE)

    s.jewels([
        ("butterfly", 128, (300, 400), MAGENTA, ROSE, -18),
        ("butterfly", 96, (1620, 430), ROSE, BLUSH, 16),
        ("butterfly", 64, (1770, 760), ICE, (150, 205, 232), -10),
        ("gem", 52, (1700, 236), MAGENTA, "marquise", 30),
        ("gem", 44, (226, 244), MAGENTA, "heart", 0),
        ("gem", 32, (188, 726), ROSE, "round", 0),
        ("gem", 28, (1782, 604), MAGENTA, "round", 0),
        ("sparkle", 44, (412, 262), (255, 255, 255)),
        ("sparkle", 34, (1544, 250), (255, 255, 255)),
        ("sparkle", 28, (250, 560), (255, 255, 255)),
        ("pearl", 300, (290, 892), 22, 20, -6),
        ("pearl", 300, (1650, 892), 22, 20, 6),
        ("obj", "\U0001F48C", 84, (1560, 606), 10),
        ("obj", "\U0001F484", 72, (380, 606), -8),
    ])
    return s.build()


for fn in [slide01, slide02, slide03, slide04, slide05, slide06, slide07, slide08,
           slide09, slide10]:
    fn()
    print("  composed", fn.__name__)

out = os.path.join(HERE, "zahra-levina-portfolio-2026.pptx")
prs.save(out)
print("saved", out, "| slides:", len(prs.slides._sldIdLst), "| elements:", len(_written))
