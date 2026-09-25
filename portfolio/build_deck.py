# -*- coding: utf-8 -*-
"""Zahra Levina — 2026 portfolio deck, Y2K edition.

Each slide is composed as layered artwork in Pillow (asset foundry: y2k.py),
exported full-bleed, and assembled into a 16:9 .pptx with live editable body
copy and picture-fillable photo frames on top.

Ten slides, ten formats: poster, scrapbook, magazine spread, desktop explorer,
personal website, contact sheet, event flyer, cut-and-paste page, sticker
sheet, chat thread.
"""

import math, os
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE

import y2k as y
from y2k import (paste, font, u, S, HOT, BUBBLEGUM, BABY, LILAC, CYBER, LIME, BUTTER,
                 INKY, CREAM, BUBBLE, SHADE, BUNGEE, INLINE, PIXEL, TERM, SIGMAR,
                 MODAK, SILK, SILKB, BAGEL, CHICLE)

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "assets", "slides")
os.makedirs(ART, exist_ok=True)

INK_HEX, MUTE_HEX = "1C1430", "6B5A82"
BODY_F, UI_F = "Verdana", "Tahoma"

def px(v):
    return Emu(int(round(v * 6350)))

def canvas(bg=None):
    im = Image.new("RGBA", (y.W, y.H), (255, 255, 255, 255))
    if bg is not None:
        paste(im, bg, (0, 0))
    return im

def photo_card(art, pos, size, angle, caption, slots, lip=18, fill=(252, 250, 255)):
    """Photo card into the art + the matching fillable slot for pptx."""
    card, inner, csize = y.polaroid(size, caption=caption, fill=fill, lip=lip)
    rot = card.rotate(angle, resample=Image.BICUBIC, expand=True) if angle else card
    x0, y0 = u(pos[0]), u(pos[1])
    art.alpha_composite(rot, (x0, y0))
    icx, icy = (inner[0] + inner[2]) / 2, (inner[1] + inner[3]) / 2
    cw, ch = csize
    th = math.radians(angle)
    dx, dy = icx - cw / 2, icy - ch / 2
    nx = dx * math.cos(th) + dy * math.sin(th)
    ny = -dx * math.sin(th) + dy * math.cos(th)
    slots.append(dict(cx=(x0 + rot.size[0] / 2 + nx) / S, cy=(y0 + rot.size[1] / 2 + ny) / S,
                      w=(inner[2] - inner[0]) / S, h=(inner[3] - inner[1]) / S, rot=angle))
    return rot.size

def stickers(art, items):
    for ch, size, pos, rot in items:
        paste(art, y.emoji(ch, size, rot=rot), pos, anchor="c")

def desk_icon(art, pos, ch, label, size=86):
    paste(art, y.emoji(ch, size), (pos[0], pos[1]), anchor="tc")
    paste(art, y.pixel_text(label, 12, (32, 24, 56), shadow=u(1), shadow_c=(255, 255, 255)),
          (pos[0], pos[1] + size + 14), anchor="tc")

# ------------------------------------------------------------ pptx helpers
prs = Presentation()
prs.slide_width, prs.slide_height = px(1920), px(1080)
BLANK = prs.slide_layouts[6]

def T(sl, x, yy, w, h, text, size=15, font_name=BODY_F, bold=False, color=INK_HEX,
      align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.45, after=9):
    tb = sl.shapes.add_textbox(px(x), px(yy), px(w), px(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    lines = text if isinstance(text, (list, tuple)) else [text]
    for i, t in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        p.space_after = Pt(after if len(lines) > 1 else 0)
        r = p.add_run()
        r.text = t
        r.font.name = font_name
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = RGBColor.from_string(color)
    return tb

def add_art(sl, path):
    sl.shapes.add_picture(path, px(0), px(0), px(1920), px(1080))

def add_slots(sl, slots):
    for s in slots:
        shp = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(s["cx"] - s["w"] / 2),
                                  px(s["cy"] - s["h"] / 2), px(s["w"]), px(s["h"]))
        shp.shadow.inherit = False
        shp.fill.solid()
        shp.fill.fore_color.rgb = RGBColor.from_string("EFF1FB")
        shp.line.color.rgb = RGBColor.from_string("B27BFF")
        shp.line.width = Pt(1.5)
        shp.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        if s.get("rot"):
            shp.rotation = s["rot"]
        p = shp.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = "drop photo"
        r.font.name = UI_F
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor.from_string("9A86B5")

def finish(idx, art, overlay=None):
    bgp = os.path.join(ART, "s%02d.jpg" % idx)
    art.convert("RGB").save(bgp, quality=93, optimize=True)
    ovp = None
    if overlay is not None:
        ovp = os.path.join(ART, "s%02d_over.png" % idx)
        overlay.save(ovp, optimize=True)
    return bgp, ovp

def assemble(idx, art, slots=None, over=None):
    bg, ov = finish(idx, art, over)
    sl = prs.slides.add_slide(BLANK)
    add_art(sl, bg)
    if slots:
        add_slots(sl, slots)
    if ov:
        add_art(sl, ov)
    return sl

# =========================================================== 1 — cover poster
def slide01():
    art = canvas(y.linear_gradient((y.W, y.H), [(0, (255, 230, 245)), (.5, (255, 247, 252)),
                                                (1, (255, 224, 242))]))
    paste(art, y.feather(y.halftone((u(1150), u(720)), (255, 186, 224), (255, 245, 251)).convert("RGBA"),
                         r=u(420), t=u(300)), (0, 360))
    paste(art, y.leopard((y.W, u(104))), (0, 0))
    paste(art, y.lace_strip(y.W, u(54), (255, 255, 255)), (0, 100))
    paste(art, y.leopard((y.W, u(104)), seed=11), (0, 976))
    paste(art, y.lace_strip(y.W, u(54), (255, 255, 255), flip=True), (0, 922))

    paste(art, y.marquee((492, 48), "*  2 0 2 6   P O R T F O L I O  *"), (92, 176))
    paste(art, y.bedazzled("ZAHRA", font(BUBBLE, 124)), (70, 224))
    paste(art, y.chrome_text("LEVINA", font(BUBBLE, 124)), (70, 386))
    paste(art, y.sticker_text("creative · content · marketing", font(BUNGEE, 26), LIME), (94, 570))
    paste(art, y.sticker_text("visual communication", font(BUNGEE, 26), CYBER), (94, 638))
    for i, (lab, col) in enumerate([("WHATSAPP", HOT), ("EMAIL", LILAC), ("LINKEDIN", CYBER)]):
        paste(art, y.gel((252, 74), col, label=lab), (94 + i * 268, 724))
    paste(art, y.pixel_text("+62 8xx-xxxx-xxxx   ·   hello@email.com   ·   linkedin.com/in/username",
                            14, (104, 84, 128)), (96, 826))

    slots = []
    photo_card(art, (1236, 196), (520, 600), -6, "me.jpg", slots)
    photo_card(art, (1006, 668), (280, 300), 9, "hi.jpg", slots)
    over = Image.new("RGBA", (y.W, y.H), (0, 0, 0, 0))
    paste(over, y.tape(212, angle=-18), (1212, 192))
    paste(over, y.tape(186, angle=13, color=(255, 200, 235)), (1600, 728))
    paste(over, y.starburst(88, color=BUTTER, rot=6), (1012, 372), anchor="c")
    paste(over, y.pixel_text("NEW\n2026", 13, INKY), (1012, 372), anchor="c")
    stickers(over, [("\U0001F98B", 132, (1210, 186), -14), ("\U0001F4BF", 104, (1836, 340), 8),
                    ("\U0001F4F1", 108, (900, 430), 12), ("\U0001F495", 110, (1798, 800), -8),
                    ("\u2B50", 84, (900, 196), 0), ("\U0001F380", 98, (1858, 172), -10),
                    ("\U0001F48E", 74, (874, 596), 0), ("\U0001F3A7", 88, (676, 902), 6),
                    ("\U0001F338", 70, (1318, 998), 0)])
    y.glitter(over, 120, box=(u(60), u(150), y.W, u(930)), seed=9)
    return assemble(1, art, slots, over)

# ========================================================= 2 — scrapbook page
def slide02():
    art = canvas(y.grid_paper((y.W, y.H), bg=(255, 250, 253), line=(255, 218, 238)))
    paste(art, y.feather(y.halftone((u(700), u(500)), (198, 168, 255), (255, 250, 253)).convert("RGBA"),
                         l=u(300), b=u(280)), (1220, 0))
    paste(art, y.zigzag_strip(y.W, u(26), HOT), (0, 1044))
    paste(art, y.torn_paper((1020, 566), (255, 255, 255)), (76, 306))
    paste(art, y.bedazzled("HI, I'M ZAHRA!", font(BUBBLE, 82)), (70, 130))
    paste(art, y.tape(206, angle=-7, color=(198, 242, 78)), (118, 290))
    paste(art, y.tape(206, angle=5), (872, 294))
    paste(art, y.speech_bubble((330, 118), BABY), (1136, 116))
    paste(art, y.pixel_text("say hi! <3", 18, (150, 40, 110)), (1180, 150))

    slots = []
    photo_card(art, (1210, 274), (480, 546), 5, "webcam.jpg", slots)
    over = Image.new("RGBA", (y.W, y.H), (0, 0, 0, 0))
    paste(over, y.tape(184, angle=16, color=(255, 214, 240)), (1182, 256))
    stickers(over, [("\U0001F4BB", 120, (1084, 826), -10), ("\u2728", 76, (1758, 240), 0),
                    ("\U0001F33F", 96, (1786, 818), 12), ("\U0001F3A7", 92, (162, 872), -8),
                    ("\U0001F31F", 70, (1020, 190), 0), ("\U0001F48C", 84, (330, 906), 7),
                    ("\U0001F338", 76, (556, 926), -6), ("\U0001F4CC", 68, (804, 902), 0)])
    y.glitter(over, 80, seed=4)
    sl = assemble(2, art, slots, over)
    T(sl, 128, 358, 900, 480, [
        "I'm a creative and marketing enthusiast with experience in content creation, social media, graphic design, event management, and brand partnerships.",
        "With a background in agricultural community development, I've had the opportunity to work across different environments—from student organizations and research projects to building a wellness community through Sawala Space.",
        "I enjoy turning ideas into clear, engaging, and purposeful creative work.",
    ], size=13, spacing=1.55, after=12)
    return sl

# ====================================================== 3 — magazine spread
def slide03():
    art = canvas(y.linear_gradient((y.W, y.H), [(0, (255, 255, 255)), (1, (255, 246, 252))]))
    paste(art, y.feather(y.halftone((u(1040), y.H), HOT, (255, 255, 255)).convert("RGBA"),
                         r=u(360)), (0, 0))
    paste(art, y.chrome_text("WHAT", font(BUNGEE, 116)), (58, 92))
    paste(art, y.chrome_text("I DO", font(BUNGEE, 116)), (58, 226))
    paste(art, y.sticker_text("four ways i work", font(BUNGEE, 24), LIME), (86, 392))
    paste(art, y.starburst(104, color=BUTTER, rot=10), (240, 596), anchor="c")
    paste(art, y.pixel_text("PICK\nONE", 15, INKY), (240, 596), anchor="c")
    stickers(art, [("\U0001F4F8", 116, (490, 560), -12), ("\U0001F3A8", 112, (620, 700), 8),
                   ("\U0001F4E3", 104, (420, 800), -6), ("\U0001F4AC", 100, (196, 826), 10)])
    paste(art, y.marquee((y.W / S, 50), "CONTENT  *  DESIGN  *  CAMPAIGNS  *  EVENTS  *  PARTNERSHIPS  *  COMMUNITY  *"),
          (0, 1012))

    geo = [(1010, 74, -2, HOT, "01"), (1046, 306, 2, LILAC, "02"),
           (1010, 538, 2, CYBER, "03"), (1046, 770, -2, LIME, "04")]
    mats = [lambda: y.dotted_note((824, 206)),
            lambda: y.torn_paper((824, 206), (255, 255, 255)),
            lambda: y.bevel_panel((824, 206), fill=(236, 248, 255), radius=12),
            lambda: y.dotted_note((824, 206), fill=(240, 255, 222), edge=(186, 214, 120))]
    for (cx, cy, rot, col, num), mat in zip(geo, mats):
        paste(art, mat(), (cx, cy), rot=rot)
        paste(art, y.gel((74, 74), col, radius=37, label=num), (cx + 34, cy + 30))
    over = Image.new("RGBA", (y.W, y.H), (0, 0, 0, 0))
    for cx, cy, rot, col, num in geo:
        paste(over, y.tape(150, angle=rot * 5, color=(255, 236, 160)), (cx + 330, cy - 22))
    y.glitter(over, 70, seed=11)
    sl = assemble(3, art, None, over)
    body = [("Content & Social Media", "Content creation · social media · copywriting"),
            ("Creative & Visual", "Graphic design · visual communication · campaign materials"),
            ("Marketing & Events", "Campaign development · event management · brand partnerships"),
            ("Communication", "Community engagement · collaboration · project coordination")]
    for (title, sub), (cx, cy, rot, col, num) in zip(body, geo):
        T(sl, cx + 128, cy + 44, 640, 56, title, size=17, font_name=UI_F, bold=True)
        T(sl, cx + 130, cy + 102, 640, 80, sub, size=12.5, color=MUTE_HEX, spacing=1.4)
    return sl

# ==================================================== 4 — desktop explorer
def slide04():
    art = canvas(y.sky((y.W, y.H), top=(150, 210, 255), bottom=(226, 248, 208)))
    art = y.scanlines(art, alpha=22)
    for i, (ch, lab) in enumerate([("\U0001F5A5", "my computer"), ("\U0001F4C2", "my work"),
                                   ("\U0001F5D1", "recycle bin")]):
        desk_icon(art, (112, 96 + i * 190), ch, lab)
    paste(art, y.chrome_text("WHERE I'VE BEEN", font(BUNGEE, 62)), (258, 44))

    win, body = y.win_frame((1560, 716), "C:\\ zahra \\ experience", bar=(LILAC, CYBER))
    paste(art, win, (248, 176))
    bx, by = 248 + body[0] / S, 176 + body[1] / S
    side_w = 286
    paste(art, y.bevel_panel((side_w, 656), fill=(238, 244, 255), radius=8), (bx + 10, by + 10))
    paste(art, y.pixel_text("QUICK LINKS", 13, (90, 70, 140)), (bx + 34, by + 36))
    for i, lnk in enumerate(["> all folders", "> by year", "> by role", "> creative", "> orgs"]):
        paste(art, y.pixel_text(lnk, 12, (110, 96, 150)), (bx + 34, by + 84 + i * 40))
    paste(art, y.dotted_note((228, 132)), (bx + 38, by + 470))
    paste(art, y.pixel_text("visitors\n000512", 14, (150, 110, 60)), (bx + 66, by + 500))
    paste(art, y.emoji("\U0001F6A7", 66), (bx + 150, by + 300), anchor="c")

    marks = ["\U0001F490", "\U0001F3DB", "\U0001F393", "\U0001F33E", "\U0001F4E3"]
    for i in range(5):
        ry = by + 24 + i * 124
        paste(art, y.emoji("\U0001F4C1", 74), (bx + side_w + 54, ry + 10))
        paste(art, y.emoji(marks[i], 60), (bx + side_w + 1126, ry + 44), anchor="c")
        paste(art, y.rainbow_rule(1170, 6), (bx + side_w + 48, ry + 106))

    bar = y.linear_gradient((y.W, u(70)), [(0, (150, 196, 255)), (.5, (96, 150, 232)), (1, (60, 110, 200))])
    paste(art, bar, (0, 1010))
    paste(art, y.gel((170, 50), LIME, label="START"), (18, 1020))
    for i, t in enumerate(["experience.exe", "portfolio_2026"]):
        paste(art, y.bevel_panel((300, 50), fill=(228, 240, 255), radius=8), (206 + i * 316, 1020))
        paste(art, y.pixel_text(t, 12, (60, 50, 100)), (226 + i * 316, 1036))
    paste(art, y.bevel_panel((240, 50), fill=(228, 240, 255), radius=8), (1656, 1020))
    paste(art, y.pixel_text("04/10  10:30 PM", 12, (60, 50, 100)), (1676, 1036))

    over = Image.new("RGBA", (y.W, y.H), (0, 0, 0, 0))
    stickers(over, [("\U0001F4C2", 88, (1854, 206), 10), ("\u2728", 68, (156, 704), 0),
                    ("\U0001F31F", 72, (1844, 880), 0), ("\U0001F4BE", 78, (110, 880), -8)])
    paste(over, y.cursor(56), (1290, 832))
    sl = assemble(4, art, None, over)
    orgs = [("Sawala Space", "Co-Founder · Creative & Marketing"),
            ("Kementerian Pertanian RI", "Intern · Administration & Partnership Support"),
            ("IPB University", "Research Assistant"),
            ("Nabila Farm Lembang", "Intern · Agriculture & Content Creation"),
            ("Himpunan Mahasiswa PPP", "Head of Media & Branding")]
    for i, (org, role) in enumerate(orgs):
        ry = by + 24 + i * 124
        T(sl, bx + side_w + 150, ry + 16, 1000, 46, org, size=18, font_name=UI_F, bold=True)
        T(sl, bx + side_w + 152, ry + 58, 1000, 36, role, size=13, color=MUTE_HEX)
    return sl

# ==================================================== 5 — personal website
def slide05():
    art = canvas(y.holo_sheet((y.W, y.H)))
    paste(art, y.bevel_panel((1700, 830), fill=(255, 255, 255), radius=18), (110, 142))
    paste(art, y.marquee((1700, 48), "*  W E L C O M E   2   S A W A L A   S P A C E  *  WELLNESS COMMUNITY & EVENT ORGANIZER  *  NOW OPEN  *"),
          (110, 96))
    for i, (lab, col) in enumerate([("BACK", CYBER), ("HOME", LIME), ("FAVES", HOT)]):
        paste(art, y.gel((136, 48), col, label=lab, text_c=(40, 26, 60) if col is LIME else (255, 255, 255)),
              (146 + i * 150, 176))
    paste(art, y.bevel_panel((1120, 48), fill=(246, 248, 255), radius=10), (606, 176))
    paste(art, y.pixel_text("http://www.sawalaspace.com/index.html", 13, (120, 104, 140)), (630, 188))

    sx = 146
    paste(art, y.bevel_panel((300, 580), fill=(252, 240, 250), radius=10), (sx, 250))
    paste(art, y.pixel_text("* MENU *", 14, (150, 40, 110)), (sx + 28, 276))
    for i, lnk in enumerate(["> about us", "> events", "> classes", "> partners", "> gallery", "> contact"]):
        paste(art, y.pixel_text(lnk, 12, (120, 96, 150)), (sx + 28, 326 + i * 42))
    paste(art, y.gel((236, 54), LILAC, label="GUESTBOOK"), (sx + 32, 596))
    paste(art, y.emoji("\U0001F6A7", 72), (sx + 150, 704), anchor="c")
    paste(art, y.pixel_text("under\nconstruction", 11, (140, 110, 60)), (sx + 150, 748), anchor="tc")

    mx = 500
    paste(art, y.bedazzled("SAWALA SPACE", font(BUBBLE, 60)), (mx - 14, 258))
    paste(art, y.sticker_text("wellness community & event organizer", font(BUNGEE, 20), LILAC), (mx, 374))
    paste(art, y.rainbow_rule(700, 8), (mx, 432))
    paste(art, y.pixel_text(">> MY ROLE", 14, (150, 40, 110)), (mx, 742))
    for i, lab in enumerate(["CONTENT", "SOCIAL", "CAMPAIGN"]):
        paste(art, y.gel((222, 56), HOT, label=lab), (mx + i * 234, 786))
    for i, lab in enumerate(["EVENT", "PARTNER", "BRANDING"]):
        paste(art, y.gel((222, 56), LILAC, label=lab), (mx + i * 234, 856))

    slots = []
    photo_card(art, (1238, 250), (520, 330), 3, "sawala_space.jpg", slots, lip=14)
    photo_card(art, (1238, 606), (250, 260), -4, "event.jpg", slots, lip=12)
    photo_card(art, (1508, 606), (250, 260), 5, "community.jpg", slots, lip=12)
    over = Image.new("RGBA", (y.W, y.H), (0, 0, 0, 0))
    paste(over, y.tape(156, angle=-14, color=(198, 242, 78)), (1218, 238))
    stickers(over, [("\U0001F33F", 96, (1156, 244), -12), ("\U0001F490", 92, (1812, 560), 10),
                    ("\u2728", 66, (1196, 906), 0), ("\U0001F9FF", 74, (94, 862), 0),
                    ("\U0001F31F", 64, (1860, 214), 0)])
    sl = assemble(5, art, slots, over)
    T(sl, mx, 466, 706, 260,
      "As a co-founder, I contribute to the creative and marketing side of Sawala Space, from developing event concepts and promotional content to managing brand partnerships and supporting event execution.",
      size=12.5, spacing=1.6)
    return sl

# ======================================================= 6 — contact sheet
def slide06():
    art = canvas(y.linear_gradient((y.W, y.H), [(0, (255, 240, 249)), (1, (236, 243, 255))]))
    paste(art, y.checkerboard((y.W, u(52)), c1=INKY), (0, 0))
    paste(art, y.checkerboard((y.W, u(52)), c1=INKY), (0, 1028))
    paste(art, y.sticker_text("SELECTED", font(BUNGEE, 54), HOT), (64, 84), rot=-3)
    paste(art, y.sticker_text("CREATIVE WORKS", font(BUNGEE, 54), LILAC), (64, 164), rot=-3)
    for i, lab in enumerate(["SOCIAL MEDIA", "EVENT VISUALS", "PROMO", "BRANDING"]):
        col = [CYBER, LIME, HOT, BUTTER][i]
        paste(art, y.gel((244, 52), col, label=lab,
                         text_c=(40, 26, 60) if col in (LIME, BUTTER) else (255, 255, 255)),
              (872 + i * 258, 96))
    slots = []
    grid = [(92, 300, -6, "ig_carousel"), (560, 268, 4, "event_poster"), (1028, 302, -3, "reels_cover"),
            (1470, 264, 7, "brand_kit"), (92, 668, 5, "feed_layout"), (560, 700, -4, "promo_flyer"),
            (1028, 664, 3, "campaign"), (1470, 692, -5, "merch")]
    for gx, gy, rot, cap in grid:
        photo_card(art, (gx, gy), (378, 300), rot, cap + ".jpg", slots, lip=15)
    over = Image.new("RGBA", (y.W, y.H), (0, 0, 0, 0))
    for gx, gy, rot, cap in grid[::3]:
        paste(over, y.tape(142, angle=rot * 3, color=(255, 214, 240)), (gx + 116, gy - 18))
    stickers(over, [("\U0001F4F7", 104, (58, 626), -10), ("\U0001F39E", 86, (1874, 604), 8),
                    ("\u2728", 64, (524, 626), 0), ("\U0001F496", 76, (1004, 1004), 0),
                    ("\U0001F31F", 62, (1448, 630), 0)])
    paste(over, y.cursor(58), (1832, 950))
    y.glitter(over, 90, seed=6)
    sl = assemble(6, art, slots, over)
    T(sl, 872, 186, 980, 70,
      "A selection of social media content, event materials, promotional visuals, and other creative work I've developed across different projects.",
      size=12.5, color=MUTE_HEX, spacing=1.4)
    return sl

# ========================================================== 7 — event flyer
def slide07():
    art = canvas(y.linear_gradient((y.W, y.H), [(0, (230, 248, 194)), (.45, (255, 250, 220)),
                                                (1, (202, 238, 255))]))
    paste(art, y.feather(y.halftone((y.W, u(460)), (255, 210, 110), (255, 250, 222)).convert("RGBA"),
                         t=u(300)), (0, 620))
    paste(art, y.zigzag_strip(y.W, u(30), HOT), (0, 0))
    paste(art, y.zigzag_strip(y.W, u(30), LILAC), (0, 1050))
    paste(art, y.chrome_text("STRETCH", font(BUNGEE, 90)), (612, 76))
    paste(art, y.sticker_text("FOR STRAY", font(BUNGEE, 78), HOT), (620, 208))
    paste(art, y.sticker_text("wellness × social impact", font(BUNGEE, 22), LIME), (628, 348))
    paste(art, y.dotted_note((720, 384)), (620, 556))
    paste(art, y.pixel_text("MY CONTRIBUTION", 15, (150, 90, 40)), (660, 588))
    for i in range(5):
        paste(art, y.emoji("\u2705", 34), (666, 638 + i * 56))
    slots = []
    photo_card(art, (86, 196), (494, 644), -4, "poster_final.jpg", slots)
    photo_card(art, (1400, 424), (424, 216), 3, "documentation.jpg", slots, lip=13)
    photo_card(art, (1400, 676), (424, 216), -3, "social_post.jpg", slots, lip=13)
    over = Image.new("RGBA", (y.W, y.H), (0, 0, 0, 0))
    paste(over, y.tape(196, angle=-16, color=(255, 236, 160)), (66, 182))
    paste(over, y.starburst(112, color=BUTTER, rot=8), (1672, 178), anchor="c")
    paste(over, y.pixel_text("FOR THE\nSTRAYS", 14, INKY), (1672, 178), anchor="c")
    stickers(over, [("\U0001F43E", 98, (566, 132), -14), ("\U0001F415", 118, (1376, 306), 8),
                    ("\U0001F49A", 84, (1358, 946), 0), ("\u2728", 68, (1330, 126), 0),
                    ("\U0001F9D8", 108, (300, 946), 6), ("\U0001F33F", 82, (1852, 944), -8),
                    ("\U0001F49D", 78, (1590, 962), 10)])
    sl = assemble(7, art, slots, over)
    T(sl, 624, 428, 730, 100,
      "A wellness event combining movement, community, and support for animal welfare.",
      size=15, spacing=1.45)
    for i, it in enumerate(["Campaign concept", "Event promotion", "Social media content",
                            "Partnership communication", "Event coordination"]):
        T(sl, 716, 636 + i * 56, 560, 46, it, size=13.5, font_name=UI_F, anchor=MSO_ANCHOR.MIDDLE)
    return sl

# =================================================== 8 — cut-and-paste page
def slide08():
    art = canvas(y.gingham((y.W, y.H), c=(255, 168, 214)))
    paste(art, y.torn_paper((1780, 244), (255, 255, 255)), (70, 54))
    paste(art, y.sticker_text("BEYOND CREATIVE WORK", font(BUNGEE, 54), HOT), (104, 88))
    mats = [(y.dotted_note((524, 412)), (100, 392), -3, "\U0001F4E3"),
            (y.torn_paper((524, 412), (255, 255, 255)), (690, 366), 2, "\U0001F3AD"),
            (y.bevel_panel((524, 412), fill=(234, 248, 255), radius=12), (1284, 396), -2, "\U0001F4DA")]
    for card, pos, rot, ch in mats:
        paste(art, card, pos, rot=rot)
        paste(art, y.emoji(ch, 88, rot=rot * 2), (pos[0] + 264, pos[1] + 92), anchor="c")
    over = Image.new("RGBA", (y.W, y.H), (0, 0, 0, 0))
    for pos, rot in [((100, 392), -14), ((690, 366), 10), ((1284, 396), -8)]:
        paste(over, y.tape(176, angle=rot, color=(255, 236, 160)), (pos[0] + 176, pos[1] - 32))
    stickers(over, [("\u2702", 88, (62, 676), -20), ("\U0001F4CC", 78, (1858, 358), 0),
                    ("\u2728", 60, (642, 946), 0), ("\U0001F31F", 66, (1244, 336), 0),
                    ("\U0001F58D", 80, (1846, 946), 12)])
    y.glitter(over, 60, seed=3)
    sl = assemble(8, art, None, over)
    T(sl, 108, 190, 1520, 70,
      "My creative experience also grew through student organizations, academic projects, and collaborative work.",
      size=14, color=MUTE_HEX)
    blocks = [("Himpunan Mahasiswa PPP", "Head of Media & Branding"),
              ("Pekan Seni Budaya IPB", "Vice Head / Staff DKV"),
              ("Academic & Research Projects", "Visual communication · presentation · documentation")]
    for (title, sub), (card, pos, rot, ch) in zip(blocks, mats):
        T(sl, pos[0] + 46, pos[1] + 176, 432, 110, title, size=16, font_name=UI_F, bold=True, spacing=1.25)
        T(sl, pos[0] + 46, pos[1] + 292, 432, 100, sub, size=12.5, color=MUTE_HEX, spacing=1.4)
    return sl

# ======================================================== 9 — sticker sheet
def slide09():
    art = canvas(y.sky((y.W, y.H), top=(184, 226, 255), bottom=(230, 250, 212), seed=8))
    art = y.scanlines(art, alpha=16)
    paste(art, y.feather(y.halftone((u(700), u(460)), (255, 176, 222), (240, 248, 255)).convert("RGBA"),
                         l=u(320), b=u(260)), (1220, 0))
    paste(art, y.chrome_text("SKILLS & TOOLS", font(BUNGEE, 64)), (88, 54))
    icons = [["\U0001F58C", "\u270D", "\U0001F4F8", "\U0001F5BC"],
             ["\U0001F4F1", "\U0001F4C8", "\U0001F389", "\U0001F91D"]]
    cols = [("CREATIVE", ["Graphic Design", "Copywriting", "Content Creation", "Visual Communication"], HOT),
            ("MARKETING", ["Social Media", "Campaign Development", "Event Management", "Partnership"], LILAC)]
    for i, (title, items, col) in enumerate(cols):
        cx = 92 + i * 898
        paste(art, y.bevel_panel((860, 384), fill=(255, 255, 255), radius=16), (cx, 218))
        paste(art, y.gel((258, 54), col, label=title), (cx + 30, 240))
        for j in range(len(items)):
            ry = 330 + j * 74
            paste(art, y.emoji(icons[i][j], 42), (cx + 36, ry + 4))
            paste(art, y.bevel_panel((296, 24), fill=(236, 239, 250), radius=12), (cx + 518, ry + 16))
            paste(art, y.gel((296 - j * 24, 24), col, radius=12), (cx + 518, ry + 16))
    sheet = y.perforate(y.bevel_panel((1756, 246), fill=(255, 244, 251), radius=18))
    paste(art, sheet, (92, 646))
    paste(art, y.pixel_text("TOOLS.PNG  —  drag 2 desktop", 14, (140, 120, 170)), (128, 672))
    tools = [("Canva", CYBER), ("Adobe Illustrator", BUTTER), ("Adobe Photoshop", LILAC),
             ("CapCut", HOT), ("Microsoft Office", LIME), ("Google Workspace", CYBER),
             ("Minitab", BUBBLEGUM)]
    for row, group in enumerate([tools[:4], tools[4:]]):
        widths = [90 + len(t) * 17 for t, _ in group]
        span, left, right = sum(widths), 128, 1812
        gap = (right - left - span) / max(1, len(group) - 1)
        tx, ty = left, 720 if row == 0 else 804
        for (t, col), w in zip(group, widths):
            paste(art, y.gel((w, 62), col, label=t.upper(),
                             text_c=(40, 26, 60) if col in (BUTTER, LIME) else (255, 255, 255)), (tx, ty))
            tx += w + gap
    paste(art, y.marquee((1756, 50), "*  C A N V A  *  ILLUSTRATOR  *  PHOTOSHOP  *  CAPCUT  *  OFFICE  *  WORKSPACE  *  MINITAB  *"),
          (92, 952))
    over = Image.new("RGBA", (y.W, y.H), (0, 0, 0, 0))
    stickers(over, [("\U0001F3A8", 108, (1802, 140), 10), ("\U0001F5B1", 84, (56, 606), -12),
                    ("\U0001F4BE", 90, (1868, 640), 8), ("\u2728", 62, (1010, 614), 0),
                    ("\U0001F4CE", 74, (58, 962), 0), ("\U0001F31F", 66, (1874, 962), 0)])
    y.glitter(over, 60, seed=12)
    sl = assemble(9, art, None, over)
    for i, (title, items, col) in enumerate(cols):
        cx = 92 + i * 898
        for j, it in enumerate(items):
            T(sl, cx + 92, 330 + j * 74, 420, 48, it, size=14, font_name=UI_F, anchor=MSO_ANCHOR.MIDDLE)
    return sl

# ========================================================= 10 — chat thread
def slide10():
    art = canvas(y.linear_gradient((y.W, y.H), [(0, (255, 226, 243)), (1, (250, 236, 255))]))
    paste(art, y.feather(y.halftone((u(900), u(560)), (255, 186, 224), (255, 232, 246)).convert("RGBA"),
                         r=u(340), t=u(240)), (0, 470))
    paste(art, y.leopard((y.W, u(96)), seed=21), (0, 0))
    paste(art, y.lace_strip(y.W, u(50), (255, 255, 255)), (0, 92))
    paste(art, y.leopard((y.W, u(96)), seed=31), (0, 984))
    paste(art, y.lace_strip(y.W, u(50), (255, 255, 255), flip=True), (0, 934))
    paste(art, y.chrome_text("LET'S WORK", font(BUBBLE, 100)), (84, 186))
    paste(art, y.bedazzled("TOGETHER!", font(BUBBLE, 100)), (84, 336))
    paste(art, y.sticker_text("ZAHRA LEVINA", font(BUNGEE, 32), LIME), (100, 512))
    for i, (lab, col) in enumerate([("WHATSAPP", HOT), ("EMAIL", LILAC), ("LINKEDIN", CYBER)]):
        paste(art, y.gel((312, 84), col, label=lab), (98 + i * 332, 606))
    paste(art, y.pixel_text("+62 8xx-xxxx-xxxx            hello@email.com            /in/username",
                            13, (110, 88, 142)), (104, 716))
    paste(art, y.marquee((1724, 52), "*  T H A N K S   4   S T O P P I N G   B Y  *  LET'S CREATE SOMETHING  *"),
          (98, 846))
    paste(art, y.speech_bubble((680, 156), (255, 255, 255)), (1122, 194))
    paste(art, y.speech_bubble((680, 222), BABY, tail="br"), (1122, 424))
    paste(art, y.speech_bubble((410, 104), (255, 255, 255)), (1122, 700))
    paste(art, y.pixel_text("see u soon! <3", 15, (150, 40, 110)), (1162, 738))
    paste(art, y.emoji("\U0001F48C", 100), (1080, 168))
    over = Image.new("RGBA", (y.W, y.H), (0, 0, 0, 0))
    stickers(over, [("\U0001F496", 120, (1846, 648), 10), ("\U0001F380", 96, (1650, 726), -12),
                    ("\u2728", 74, (1812, 186), 0), ("\U0001F4F1", 112, (1790, 872), 8),
                    ("\u2B50", 70, (1032, 452), 0), ("\U0001F3AB", 86, (868, 748), -8),
                    ("\U0001F49E", 74, (676, 792), 0)])
    y.glitter(over, 100, box=(0, u(150), y.W, u(930)), seed=15)
    sl = assemble(10, art, None, over)
    T(sl, 1170, 236, 596, 110, "Thank you for taking the time to explore my work.",
      size=14.5, font_name=UI_F, spacing=1.5)
    T(sl, 1170, 462, 596, 170,
      "I'm always open to new creative opportunities, collaborations, and projects.",
      size=14.5, font_name=UI_F, spacing=1.5)
    return sl

for fn in [slide01, slide02, slide03, slide04, slide05, slide06, slide07, slide08, slide09, slide10]:
    fn()
    print("  rendered", fn.__name__)

out = os.path.join(HERE, "zahra-levina-portfolio-2026.pptx")
prs.save(out)
print("saved", out, "| slides:", len(prs.slides._sldIdLst))
