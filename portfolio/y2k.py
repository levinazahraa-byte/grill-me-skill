# -*- coding: utf-8 -*-
"""Y2K asset foundry.

Paints the graphic language the deck is built from: leopard, gingham, lace and
halftone textures; chrome, bubble and bedazzled type treatments; glossy gel
UI; polaroids, tape and torn paper; and emoji-cutout stickers.

Everything is drawn at RENDER scale but addressed in 1920x1080 design units.
"""

import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "assets", "fonts")
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

S = 1.5                       # render scale
W, H = int(1920 * S), int(1080 * S)

def u(v):                     # design units -> render px
    return int(round(v * S))

_font_cache = {}
def font(name, size):
    key = (name, int(size * S))
    if key not in _font_cache:
        path = os.path.join(FONTS, name)
        if not os.path.exists(path):
            path = {"sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                    "sans-bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                    }.get(name, name)
        _font_cache[key] = ImageFont.truetype(path, max(6, int(size * S)))
    return _font_cache[key]

BUBBLE, SHADE, BUNGEE, INLINE = ("RubikBubbles-Regular.ttf", "BungeeShade-Regular.ttf",
                                 "Bungee-Regular.ttf", "BungeeInline-Regular.ttf")
PIXEL, TERM, SIGMAR = "PressStart2P-Regular.ttf", "VT323-Regular.ttf", "SigmarOne-Regular.ttf"
MODAK, SILK, SILKB = "Modak-Regular.ttf", "Silkscreen-Regular.ttf", "Silkscreen-Bold.ttf"
BAGEL, CHICLE = "BagelFatOne-Regular.ttf", "Chicle-Regular.ttf"

# ------------------------------------------------------------------ colour
HOT = (255, 61, 158)
BUBBLEGUM = (255, 143, 208)
BABY = (255, 209, 235)
LILAC = (178, 123, 255)
CYBER = (77, 200, 255)
LIME = (198, 242, 78)
BUTTER = (255, 233, 107)
INKY = (28, 20, 48)
CREAM = (255, 248, 252)

CHROME_STOPS = [(0.00, (255, 255, 255)), (0.10, (232, 243, 255)), (0.33, (143, 166, 200)),
                (0.465, (38, 54, 82)), (0.485, (38, 54, 82)), (0.52, (120, 158, 212)),
                (0.60, (226, 240, 255)), (0.70, (255, 255, 255)), (0.86, (255, 186, 226)),
                (1.00, (126, 168, 224))]
SILVER_STOPS = [(0.0, (255, 255, 255)), (0.35, (226, 232, 242)), (0.5, (150, 163, 186)),
                (0.62, (238, 243, 250)), (1.0, (186, 199, 220))]

def mix(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))

def linear_gradient(size, stops, horizontal=False):
    w, h = size
    img = Image.new("RGB", (1, h) if not horizontal else (w, 1))
    d = ImageDraw.Draw(img)
    n = h if not horizontal else w
    for i in range(n):
        t = i / max(1, n - 1)
        lo = stops[0]
        hi = stops[-1]
        for j in range(len(stops) - 1):
            if stops[j][0] <= t <= stops[j + 1][0]:
                lo, hi = stops[j], stops[j + 1]
                break
        span = max(1e-6, hi[0] - lo[0])
        c = mix(lo[1], hi[1], (t - lo[0]) / span)
        d.point((0, i) if not horizontal else (i, 0), fill=c)
    return img.resize((w, h), Image.BILINEAR)

def radial_gradient(size, inner, outer):
    w, h = size
    img = Image.new("RGB", (w, h), outer)
    d = ImageDraw.Draw(img)
    steps = max(w, h) // 2
    for i in range(steps, 0, -1):
        t = i / steps
        c = mix(inner, outer, t)
        d.ellipse([w / 2 - w / 2 * t, h / 2 - h / 2 * t, w / 2 + w / 2 * t, h / 2 + h / 2 * t], fill=c)
    return img

# --------------------------------------------------------------- textures
def leopard(size, base=BABY, ring=(120, 40, 90), core=HOT, density=0.00022, seed=7):
    w, h = size
    img = Image.new("RGB", (w, h), base)
    d = ImageDraw.Draw(img, "RGBA")
    rnd = random.Random(seed)
    for _ in range(int(w * h * density)):
        cx, cy = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.uniform(u(14), u(30))
        for k in range(rnd.randint(2, 3)):     # broken ring of arcs
            a0 = rnd.uniform(0, 360)
            ax, ay = cx + rnd.uniform(-r * .3, r * .3), cy + rnd.uniform(-r * .3, r * .3)
            d.arc([ax - r, ay - r * .8, ax + r, ay + r * .8], a0, a0 + rnd.uniform(110, 210),
                  fill=ring + (255,), width=int(r * .42))
        rr = r * rnd.uniform(.25, .42)
        d.ellipse([cx - rr, cy - rr * .8, cx + rr, cy + rr * .8], fill=core + (255,))
    return img

def gingham(size, c=BUBBLEGUM, bg=(255, 255, 255), cell=None):
    w, h = size
    cell = cell or u(26)
    img = Image.new("RGB", (w, h), bg)
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for x in range(0, w, cell * 2):
        d.rectangle([x, 0, x + cell, h], fill=c + (110,))
    for y in range(0, h, cell * 2):
        d.rectangle([0, y, w, y + cell], fill=c + (110,))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def checkerboard(size, cell=None, c1=INKY, c2=(255, 255, 255)):
    w, h = size
    cell = cell or u(18)
    img = Image.new("RGB", (w, h), c2)
    d = ImageDraw.Draw(img)
    for j, y in enumerate(range(0, h, cell)):
        for i, x in enumerate(range(0, w, cell)):
            if (i + j) % 2 == 0:
                d.rectangle([x, y, x + cell, y + cell], fill=c1)
    return img

def halftone(size, dot=HOT, bg=(255, 255, 255), cell=None, fade=True, angle=0):
    w, h = size
    cell = cell or u(16)
    big = Image.new("RGB", (int(w * 1.5), int(h * 1.5)), bg)
    d = ImageDraw.Draw(big)
    bw, bh = big.size
    for j, y in enumerate(range(0, bh, cell)):
        for x in range(0, bw, cell):
            t = 1 - (y / bh) if fade else 1
            r = cell * 0.48 * max(0.08, t)
            d.ellipse([x - r, y - r, x + r, y + r], fill=dot)
    if angle:
        big = big.rotate(angle, resample=Image.BICUBIC, fillcolor=bg)
    return big.crop(((bw - w) // 2, (bh - h) // 2, (bw - w) // 2 + w, (bh - h) // 2 + h))

def grid_paper(size, bg=CREAM, line=(210, 224, 240), cell=None):
    w, h = size
    cell = cell or u(28)
    img = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(img)
    for x in range(0, w, cell):
        d.line([(x, 0), (x, h)], fill=line, width=max(1, u(1)))
    for y in range(0, h, cell):
        d.line([(0, y), (w, y)], fill=line, width=max(1, u(1)))
    return img

def sky(size, top=(150, 214, 255), bottom=(228, 246, 214), clouds=9, seed=3):
    w, h = size
    img = linear_gradient((w, h), [(0, top), (1, bottom)])
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    rnd = random.Random(seed)
    for _ in range(clouds):
        cx, cy = rnd.uniform(0, w), rnd.uniform(0, h * .8)
        for k in range(rnd.randint(4, 7)):
            r = rnd.uniform(u(40), u(120))
            d.ellipse([cx + rnd.uniform(-r, r) - r, cy + rnd.uniform(-r / 2, r / 2) - r * .6,
                       cx + rnd.uniform(-r, r) + r, cy + rnd.uniform(-r / 2, r / 2) + r * .6],
                      fill=(255, 255, 255, 120))
    ov = ov.filter(ImageFilter.GaussianBlur(u(16)))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def holo_sheet(size, seed=1):
    w, h = size
    img = linear_gradient((w, h), [(0.0, (255, 190, 235)), (0.22, (196, 214, 255)),
                                   (0.45, (186, 255, 236)), (0.62, (255, 246, 186)),
                                   (0.8, (255, 186, 214)), (1.0, (206, 196, 255))], horizontal=True)
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    rnd = random.Random(seed)
    for i in range(0, w * 2, u(26)):
        a = rnd.randint(0, 46)
        d.polygon([(i, 0), (i + u(14), 0), (i + u(14) - h, h), (i - h, h)], fill=(255, 255, 255, a))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def feather(img, l=0, r=0, t=0, b=0):
    """Ramp a patch's alpha out to nothing on the named edges."""
    img = img.convert("RGBA")
    w, h = img.size
    m = np.ones((h, w), dtype=np.float32)
    l, r, t, b = (min(int(v), w if v in (l, r) else h) for v in (l, r, t, b))
    if l:
        m[:, :l] *= np.linspace(0, 1, l)[None, :]
    if r:
        m[:, w - r:] *= np.linspace(1, 0, r)[None, :]
    if t:
        m[:t, :] *= np.linspace(0, 1, t)[:, None]
    if b:
        m[h - b:, :] *= np.linspace(1, 0, b)[:, None]
    a = np.asarray(img.split()[3], dtype=np.float32) * m
    img.putalpha(Image.fromarray(a.astype("uint8")))
    return img


def perforate(img, pitch=None, r=None, color=(255, 255, 255)):
    """Sticker-sheet punched edge."""
    pitch = pitch or u(22)
    r = r or u(7)
    d = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    for x in range(0, w + pitch, pitch):
        for yy in (0, h):
            d.ellipse([x - r, yy - r, x + r, yy + r], fill=color + (255,))
    for yy in range(0, h + pitch, pitch):
        for x in (0, w):
            d.ellipse([x - r, yy - r, x + r, yy + r], fill=color + (255,))
    return img


def scanlines(img, alpha=26, step=None):
    step = step or u(3)
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for y in range(0, img.size[1], step):
        d.line([(0, y), (img.size[0], y)], fill=(0, 0, 40, alpha))
    return Image.alpha_composite(img.convert("RGBA"), ov)

def glitter(layer, n=60, box=None, seed=5, colors=((255, 255, 255), (255, 214, 245), (198, 242, 78))):
    d = ImageDraw.Draw(layer, "RGBA")
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box or (0, 0, layer.size[0], layer.size[1])
    for _ in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        r = rnd.uniform(u(2), u(7))
        c = rnd.choice(colors)
        d.polygon([(x, y - r * 2.6), (x + r * .55, y - r * .55), (x + r * 2.6, y),
                   (x + r * .55, y + r * .55), (x, y + r * 2.6), (x - r * .55, y + r * .55),
                   (x - r * 2.6, y), (x - r * .55, y - r * .55)], fill=c + (rnd.randint(170, 255),))
    return layer

def lace_strip(width, depth, color=(255, 255, 255), flip=False, scallop=None):
    """A scalloped, eyelet-punched lace edge."""
    scallop = scallop or u(34)
    img = Image.new("RGBA", (width, depth), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, width, depth - scallop * .55], fill=color + (255,))
    x = 0
    while x < width + scallop:
        d.ellipse([x - scallop * .5, depth - scallop * 1.1, x + scallop * .5, depth - scallop * .1],
                  fill=color + (255,))
        x += scallop * .92
    x = 0
    while x < width + scallop:                       # eyelet holes
        d.ellipse([x - scallop * .16, depth - scallop * .86, x + scallop * .16, depth - scallop * .54],
                  fill=(0, 0, 0, 0))
        d.ellipse([x - scallop * .1 + scallop * .46, depth * .18,
                   x + scallop * .1 + scallop * .46, depth * .18 + scallop * .2], fill=(0, 0, 0, 0))
        x += scallop * .92
    if flip:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    return img

def zigzag_strip(width, depth, c1=HOT, c2=(255, 255, 255)):
    img = Image.new("RGBA", (width, depth), c2 + (255,))
    d = ImageDraw.Draw(img)
    step = depth
    for i, x in enumerate(range(-step, width + step, step)):
        d.polygon([(x, 0), (x + step / 2, depth), (x + step, 0)], fill=c1 + (255,))
    return img

# ------------------------------------------------------------ type effects
def _mask(text, fnt, pad):
    tmp = Image.new("L", (10, 10))
    box = ImageDraw.Draw(tmp).textbbox((0, 0), text, font=fnt)
    w, h = box[2] - box[0] + pad * 2, box[3] - box[1] + pad * 2
    m = Image.new("L", (max(1, w), max(1, h)), 0)
    ImageDraw.Draw(m).text((pad - box[0], pad - box[1]), text, font=fnt, fill=255)
    return m

def _outline(mask, width):
    if width <= 0:
        return Image.new("L", mask.size, 0)
    grown = mask.filter(ImageFilter.MaxFilter(int(width) * 2 + 1))
    return ImageChops.subtract(grown, mask)

def grad_text(text, fnt, stops, outline=0, outline_c=INKY, shadow=0, shadow_c=(0, 0, 0, 110),
              gloss=True, pad=None, rim=None, rim_c=(255, 255, 255)):
    """Gradient-filled display type with outline, inner gloss and drop shadow."""
    pad = pad if pad is not None else u(28) + outline * 2
    m = _mask(text, fnt, pad)
    w, h = m.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sh.paste(Image.new("RGBA", (w, h), shadow_c), (0, 0), m.filter(ImageFilter.MaxFilter(3)))
        sh = sh.filter(ImageFilter.GaussianBlur(u(5)))
        out.alpha_composite(sh, (int(shadow), int(shadow)))
    if rim:                                          # outer white rim (sticker cut)
        r = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        r.paste(Image.new("RGBA", (w, h), rim_c + (255,)), (0, 0),
                mask=m.filter(ImageFilter.MaxFilter(int(rim) * 2 + 1)))
        out.alpha_composite(r)
    if outline:
        o = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        o.paste(Image.new("RGBA", (w, h), outline_c + (255,)), (0, 0),
                mask=m.filter(ImageFilter.MaxFilter(int(outline) * 2 + 1)))
        out.alpha_composite(o)
    body = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    body.paste(linear_gradient((w, h), stops).convert("RGBA"), (0, 0), m)
    out.alpha_composite(body)
    if gloss:                                        # specular sweep across the top third
        g = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        gd.ellipse([-w * .2, -h * .55, w * 1.2, h * .42], fill=(255, 255, 255, 92))
        gm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        gm.paste(g, (0, 0), m)
        out.alpha_composite(gm.filter(ImageFilter.GaussianBlur(u(1.2))))
    return out

def chrome_text(text, fnt, **kw):
    kw.setdefault("outline", u(4))
    kw.setdefault("shadow", u(5))
    return grad_text(text, fnt, CHROME_STOPS, **kw)

def sticker_text(text, fnt, color=HOT, rim=None, outline=None, shadow=None):
    """Flat fill, fat white cut-out rim — the classic sticker."""
    rim = rim if rim is not None else u(9)
    outline = outline if outline is not None else u(3)
    shadow = shadow if shadow is not None else u(6)
    return grad_text(text, fnt, [(0, color), (1, color)], outline=outline, rim=rim,
                     shadow=shadow, gloss=False)

def bedazzled(text, fnt, stops=None, gem_r=None, gem_c=(255, 255, 255), step=None, outline=None):
    """Bubble type ringed with rhinestones."""
    stops = stops or [(0, (255, 140, 210)), (0.5, (255, 61, 158)), (1, (198, 40, 140))]
    base = grad_text(text, fnt, stops, outline=outline if outline is not None else u(3),
                     rim=u(7), shadow=u(6))
    m = _mask(text, fnt, u(28) + u(6))
    if m.size != base.size:
        m = m.resize(base.size)
    edge = _outline(m, u(5))
    pts = edge.load()
    w, h = edge.size
    gem_r = gem_r or max(u(3), int(fnt.size * 0.052))
    step = step or int(gem_r * 2.5)
    d = ImageDraw.Draw(base, "RGBA")
    placed = []
    for y in range(0, h, max(2, int(step * .34))):
        for x in range(0, w, max(2, int(step * .34))):
            if pts[x, y] > 120 and all((x - px) ** 2 + (y - py) ** 2 > step ** 2 for px, py in placed[-90:]):
                placed.append((x, y))
                d.ellipse([x - gem_r, y - gem_r, x + gem_r, y + gem_r], fill=(236, 244, 255, 255))
                d.ellipse([x - gem_r * .62, y - gem_r * .62, x + gem_r * .62, y + gem_r * .62],
                          fill=gem_c + (255,))
                d.ellipse([x - gem_r * .3, y - gem_r * .42, x + gem_r * .12, y - gem_r * .02],
                          fill=(255, 255, 255, 255))
    return base

def pixel_text(text, size, color=INKY, bold=True, shadow=None, shadow_c=(255, 255, 255)):
    fnt = font(SILKB if bold else SILK, size)
    pad = u(6)
    m = _mask(text, fnt, pad)
    out = Image.new("RGBA", m.size, (0, 0, 0, 0))
    if shadow:
        s = Image.new("RGBA", m.size, (0, 0, 0, 0))
        s.paste(Image.new("RGBA", m.size, shadow_c + (255,)), (0, 0), m)
        out.alpha_composite(s, (int(shadow), int(shadow)))
    body = Image.new("RGBA", m.size, (0, 0, 0, 0))
    body.paste(Image.new("RGBA", m.size, color + (255,)), (0, 0), m)
    out.alpha_composite(body)
    return out

# ----------------------------------------------------------------- objects
def emoji(ch, size, rim=None, shadow=True, rot=0):
    """Colour-emoji cut-out sticker with a white rim and soft shadow."""
    f = ImageFont.truetype(EMOJI_FONT, 109)
    raw = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(raw).text((20, 16), ch, font=f, embedded_color=True)
    bb = raw.getbbox()
    if not bb:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    raw = raw.crop(bb)
    px = u(size)
    raw = raw.resize((px, int(px * raw.size[1] / raw.size[0])), Image.LANCZOS)
    rim = rim if rim is not None else max(2, u(size) // 14)
    pad = rim * 3
    out = Image.new("RGBA", (raw.size[0] + pad * 2, raw.size[1] + pad * 2), (0, 0, 0, 0))
    a = Image.new("L", out.size, 0)
    a.paste(raw.split()[3], (pad, pad))
    if shadow:
        sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
        sh.paste(Image.new("RGBA", out.size, (90, 40, 90, 120)), (0, 0),
                 a.filter(ImageFilter.MaxFilter(rim * 2 + 1)))
        out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(rim * 1.6)), (0, u(3)))
    white = Image.new("RGBA", out.size, (0, 0, 0, 0))
    white.paste(Image.new("RGBA", out.size, (255, 255, 255, 255)), (0, 0),
                a.filter(ImageFilter.MaxFilter(rim * 2 + 1)))
    out.alpha_composite(white)
    out.alpha_composite(raw, (pad, pad))
    return out.rotate(rot, resample=Image.BICUBIC, expand=True) if rot else out

def gel(size, color=HOT, radius=None, label=None, fnt=None, text_c=(255, 255, 255), border=True):
    """Aqua-era glossy pill/button."""
    w, h = u(size[0]), u(size[1])
    radius = u(radius) if radius else h // 2
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius, fill=255)
    body = linear_gradient((w, h), [(0.0, mix(color, (255, 255, 255), .55)),
                                    (0.48, color),
                                    (0.52, mix(color, (0, 0, 0), .22)),
                                    (1.0, mix(color, (255, 255, 255), .30))]).convert("RGBA")
    img.paste(body, (0, 0), m)
    gl = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(gl).ellipse([w * .05, h * .06, w * .95, h * .52], fill=(255, 255, 255, 140))
    g2 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g2.paste(gl, (0, 0), m)
    img.alpha_composite(g2.filter(ImageFilter.GaussianBlur(u(1))))
    if border:
        bd = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(bd).rounded_rectangle([0, 0, w - 1, h - 1], radius,
                                             outline=(255, 255, 255, 235), width=max(2, u(2)))
        img.alpha_composite(bd)
    if label:
        f = fnt or font(SILKB, max(12, int(h / S * 0.32)))
        d = ImageDraw.Draw(img)
        bb = d.textbbox((0, 0), label, font=f)
        d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], (h - (bb[3] - bb[1])) / 2 - bb[1] - u(1)),
               label, font=f, fill=(40, 20, 50, 120))
        d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], (h - (bb[3] - bb[1])) / 2 - bb[1] - u(2)),
               label, font=f, fill=text_c + (255,))
    return img

def bevel_panel(size, fill=(255, 255, 255), radius=0, light=(255, 255, 255), dark=(150, 130, 170)):
    """Chunky 2000s bevelled panel."""
    w, h = u(size[0]), u(size[1])
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = u(radius)
    d.rounded_rectangle([0, 0, w - 1, h - 1], r, fill=fill + (255,))
    t = max(2, u(3))
    d.line([(t, t), (w - t, t)], fill=light + (255,), width=t)
    d.line([(t, t), (t, h - t)], fill=light + (255,), width=t)
    d.line([(t, h - t), (w - t, h - t)], fill=dark + (255,), width=t)
    d.line([(w - t, t), (w - t, h - t)], fill=dark + (255,), width=t)
    d.rounded_rectangle([0, 0, w - 1, h - 1], r, outline=INKY + (255,), width=max(2, u(2)))
    return img

def tape(length, depth=None, color=(255, 236, 160), angle=0, alpha=205, seed=2):
    depth = depth or 42
    w, h = u(length), u(depth)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rnd = random.Random(seed)
    pts_top = [(0, rnd.uniform(0, h * .18))]
    x = 0
    while x < w:
        x += rnd.uniform(w * .06, w * .16)
        pts_top.append((min(x, w), rnd.uniform(0, h * .2)))
    pts_bot = []
    x = w
    while x > 0:
        pts_bot.append((max(x, 0), h - rnd.uniform(0, h * .2)))
        x -= rnd.uniform(w * .06, w * .16)
    pts_bot.append((0, h - rnd.uniform(0, h * .18)))
    d.polygon(pts_top + pts_bot, fill=color + (alpha,))
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(sh).polygon(pts_top + pts_bot, fill=(255, 255, 255, 70))
    img.alpha_composite(sh.crop((0, 0, w, int(h * .45))).resize((w, int(h * .45))), (0, 0))
    return img.rotate(angle, resample=Image.BICUBIC, expand=True) if angle else img

def torn_paper(size, color=(255, 255, 255), seed=4, shadow=True):
    w, h = u(size[0]), u(size[1])
    pad = u(14)
    img = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    rnd = random.Random(seed)
    pts = []
    step = u(22)
    for x in range(0, w + step, step):
        pts.append((min(x, w) + pad, pad + rnd.uniform(-u(5), u(5))))
    for y in range(0, h + step, step):
        pts.append((w + pad + rnd.uniform(-u(5), u(5)), min(y, h) + pad))
    for x in range(w, -step, -step):
        pts.append((max(x, 0) + pad, h + pad + rnd.uniform(-u(5), u(5))))
    for y in range(h, -step, -step):
        pts.append((pad + rnd.uniform(-u(5), u(5)), max(y, 0) + pad))
    if shadow:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).polygon(pts, fill=(120, 70, 120, 90))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(u(6))), (0, u(4)))
    ImageDraw.Draw(img).polygon(pts, fill=color + (255,))
    return img

def polaroid(size, angle=0, caption=None, fill=(252, 250, 255), lip=None, cap_c=(120, 105, 140)):
    """Photo card; returns (card, inner_rect_in_card_coords)."""
    w, h = u(size[0]), u(size[1])
    lip = u(lip) if lip else u(18)
    bottom = lip * 3
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([lip, lip, w - lip, h - lip], fill=(110, 60, 110, 120))
    card.alpha_composite(sh.filter(ImageFilter.GaussianBlur(u(7))), (0, u(5)))
    d = ImageDraw.Draw(card)
    d.rectangle([0, 0, w - 1, h - 1], fill=fill + (255,), outline=(226, 214, 238, 255), width=u(1))
    inner = (lip, lip, w - lip, h - bottom)
    d.rectangle(inner, fill=(238, 240, 250, 255))
    if caption:
        f = font(SILK, 13)
        bb = d.textbbox((0, 0), caption, font=f)
        d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], h - bottom + lip * .5), caption, font=f,
               fill=cap_c + (255,))
    if angle:
        rot = card.rotate(angle, resample=Image.BICUBIC, expand=True)
        return rot, inner, card.size
    return card, inner, card.size

def starburst(r, points=14, color=BUTTER, edge=INKY, inner=0.52, rot=0):
    R = u(r)
    img = Image.new("RGBA", (R * 2 + u(8), R * 2 + u(8)), (0, 0, 0, 0))
    cx = cy = img.size[0] / 2
    pts = []
    for i in range(points * 2):
        a = math.pi * i / points + math.radians(rot)
        rad = R if i % 2 == 0 else R * inner
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    ImageDraw.Draw(img).polygon(pts, fill=color + (255,), outline=edge + (255,), width=u(3))
    return img

def speech_bubble(size, color=(255, 255, 255), edge=INKY, tail="bl", radius=26):
    w, h = u(size[0]), u(size[1])
    img = Image.new("RGBA", (w, h + u(26)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], u(radius), fill=color + (255,),
                        outline=edge + (255,), width=u(3))
    if tail == "bl":
        tp = [(u(40), h - u(4)), (u(34), h + u(24)), (u(92), h - u(4))]
    else:
        tp = [(w - u(40), h - u(4)), (w - u(34), h + u(24)), (w - u(92), h - u(4))]
    d.polygon(tp, fill=color + (255,), outline=edge + (255,), width=u(3))
    d.line([tp[0], tp[2]], fill=color + (255,), width=u(5))
    return img

def cursor(size=46, color=(255, 255, 255), edge=INKY):
    s = u(size)
    img = Image.new("RGBA", (s, int(s * 1.5)), (0, 0, 0, 0))
    ImageDraw.Draw(img).polygon([(0, 0), (0, s * 1.26), (s * .32, s * .96), (s * .56, s * 1.42),
                                 (s * .78, s * 1.3), (s * .54, s * .86), (s * .95, s * .82)],
                                fill=color + (255,), outline=edge + (255,), width=max(2, u(2)))
    return img

def win_frame(size, title, bar=(HOT, LILAC), body=(255, 255, 255), fnt=None, glossy=True):
    """Glossy XP-era window; returns (image, body_rect)."""
    w, h = u(size[0]), u(size[1])
    bh = u(46)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([0, 0, w - 1, h - 1], u(14), fill=(90, 50, 100, 130))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(u(8))), (0, u(6)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], u(14), fill=body + (255,), outline=INKY + (255,), width=u(3))
    barimg = linear_gradient((w, bh), [(0, mix(bar[0], (255, 255, 255), .45)), (.5, bar[0]),
                                       (.52, bar[1]), (1, mix(bar[1], (0, 0, 0), .12))]).convert("RGBA")
    bm = Image.new("L", (w, bh), 0)
    ImageDraw.Draw(bm).rounded_rectangle([0, 0, w - 1, bh * 2], u(14), fill=255)
    img.paste(barimg, (0, 0), bm)
    if glossy:
        gl = Image.new("RGBA", (w, bh), (0, 0, 0, 0))
        ImageDraw.Draw(gl).ellipse([-w * .1, -bh * .8, w * 1.1, bh * .58], fill=(255, 255, 255, 110))
        g2 = Image.new("RGBA", (w, bh), (0, 0, 0, 0))
        g2.paste(gl, (0, 0), bm)
        img.alpha_composite(g2)
    d.line([(0, bh), (w, bh)], fill=INKY + (255,), width=u(3))
    f = fnt or font(SILKB, 15)
    d.text((u(18), bh / 2 - f.size * .62), title, font=f, fill=(60, 20, 60, 160))
    d.text((u(17), bh / 2 - f.size * .68), title, font=f, fill=(255, 255, 255, 255))
    for i, c in enumerate([(160, 220, 255), (198, 242, 78), (255, 120, 170)]):
        bx = w - u(30) - i * u(40)
        img.alpha_composite(gel((22, 22), c, radius=11), (int(bx - u(22)), int(bh / 2 - u(11))))
    return img, (u(3), bh + u(3), w - u(3), h - u(3))

def dotted_note(size, fill=(255, 253, 214), edge=(226, 196, 120)):
    w, h = u(size[0]), u(size[1])
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([0, 0, w, h], fill=(120, 90, 60, 90))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(u(6))), (u(3), u(5)))
    d.rectangle([0, 0, w - 1, h - 1], fill=fill + (255,), outline=edge + (255,), width=u(2))
    return img

def marquee(size, text, bg=None, fnt=None, text_c=INKY):
    w, h = u(size[0]), u(size[1])
    strip = (bg or holo_sheet((w, h))).convert("RGBA")
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], h // 2, fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(strip, (0, 0), m)
    d = ImageDraw.Draw(out)
    d.rounded_rectangle([0, 0, w - 1, h - 1], h // 2, outline=INKY + (255,), width=u(2))
    f = fnt or font(SILKB, 13)
    bb = d.textbbox((0, 0), text, font=f)
    d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], (h - (bb[3] - bb[1])) / 2 - bb[1]), text, font=f,
           fill=text_c + (255,))
    return out

def rainbow_rule(length, depth=10):
    w, h = u(length), u(depth)
    img = linear_gradient((w, h), [(0, (255, 90, 140)), (.2, (255, 190, 90)), (.4, (230, 245, 110)),
                                   (.6, (120, 230, 180)), (.8, (120, 190, 255)), (1, (200, 140, 255))],
                          horizontal=True).convert("RGBA")
    return img

def film_strip(size, frames=4, bg=INKY):
    w, h = u(size[0]), u(size[1])
    img = Image.new("RGBA", (w, h), bg + (255,))
    d = ImageDraw.Draw(img)
    hole_h = h * .1
    for x in range(int(w * .02), w, int(w * .075)):
        d.rounded_rectangle([x, h * .035, x + w * .04, h * .035 + hole_h], u(3), fill=(255, 255, 255, 255))
        d.rounded_rectangle([x, h - h * .035 - hole_h, x + w * .04, h - h * .035], u(3), fill=(255, 255, 255, 255))
    rects = []
    pad = w * .015
    fw = (w - pad * (frames + 1)) / frames
    for i in range(frames):
        x0 = pad + i * (fw + pad)
        r = [x0, h * .19, x0 + fw, h * .81]
        d.rectangle(r, fill=(244, 246, 252, 255))
        rects.append(tuple(int(v) for v in r))
    return img, rects

def paste(base, img, xy, anchor="tl", rot=None):
    """Alpha-composite at design coordinates."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    if rot:
        img = img.rotate(rot, resample=Image.BICUBIC, expand=True)
    x, y = u(xy[0]), u(xy[1])
    if anchor == "c":
        x -= img.size[0] // 2
        y -= img.size[1] // 2
    elif anchor == "tc":
        x -= img.size[0] // 2
    elif anchor == "tr":
        x -= img.size[0]
    base.alpha_composite(img, (int(x), int(y)))
    return img.size


# =====================================================================
#  ANGEL SYSTEM — the chic Y2K vocabulary
#  Tonal pink · black lace · chrome · rhinestone. Editorial, not cartoon.
# =====================================================================

MAGENTA = (255, 46, 147)
ROSE = (255, 143, 197)
BLUSH = (255, 221, 238)
SHELL = (255, 244, 249)
NOIR = (16, 10, 22)
PEARL = (255, 248, 242)
ICE = (198, 232, 246)

ITALIANA, BODONI, CORMORANT = "Italiana-Regular.ttf", "BodoniModa.ttf", "CormorantGaramond.ttf"
PINYON, ALLURA, MONSIEUR = "PinyonScript-Regular.ttf", "Allura-Regular.ttf", "MonsieurLaDoulaise-Regular.ttf"
OSWALD, ARCHIVO, ARCHIVO_BLACK = "Oswald.ttf", "Archivo.ttf", "ArchivoBlack-Regular.ttf"

PEARL_STOPS = [(0.0, (255, 255, 255)), (0.3, (255, 246, 250)), (0.55, (246, 220, 234)),
               (0.75, (255, 255, 255)), (1.0, (232, 206, 222))]
ROSE_CHROME = [(0.00, (255, 255, 255)), (0.12, (255, 236, 246)), (0.36, (255, 138, 196)),
               (0.475, (176, 24, 104)), (0.495, (176, 24, 104)), (0.54, (255, 120, 186)),
               (0.66, (255, 250, 253)), (0.82, (255, 190, 224)), (1.00, (214, 96, 162))]


def tracked(text, fnt, color=NOIR, tracking=8, shadow=None):
    """Letterspaced type — the editorial label voice."""
    pad = u(10)
    tr = u(tracking)
    tmp = ImageDraw.Draw(Image.new("L", (10, 10)))
    widths = [tmp.textlength(c, font=fnt) for c in text]
    box = tmp.textbbox((0, 0), text, font=fnt)
    w = int(sum(widths) + tr * max(0, len(text) - 1)) + pad * 2
    h = box[3] - box[1] + pad * 2
    img = Image.new("RGBA", (max(1, w), max(1, h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = pad
    for ch, cw in zip(text, widths):
        if shadow:
            d.text((x + shadow, pad - box[1] + shadow), ch, font=fnt, fill=(255, 255, 255, 180))
        d.text((x, pad - box[1]), ch, font=fnt, fill=color + (255,))
        x += cw + tr
    return img


def _facet_poly(cx, cy, r, n=8, phase=0):
    return [(cx + r * math.cos(phase + 2 * math.pi * i / n),
             cy + r * math.sin(phase + 2 * math.pi * i / n)) for i in range(n)]


def gem(size, color=MAGENTA, cut="round", rot=0, glow=None):
    """A faceted rhinestone — brilliant cut, table facets, specular."""
    s = u(size)
    if glow is None:
        glow = size >= 30
    pad = int(s * 0.28)
    img = Image.new("RGBA", (s + pad * 2, s + pad * 2), (0, 0, 0, 0))
    cx = cy = (s + pad * 2) / 2
    r = s / 2
    d = ImageDraw.Draw(img, "RGBA")
    if glow:
        g = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse([cx - r * 1.05, cy - r * 1.05, cx + r * 1.05, cy + r * 1.05],
                                  fill=mix(color, (255, 255, 255), .6) + (70,))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(s * 0.2)))

    if cut == "marquise":
        pts = []
        for i in range(24):
            t = 2 * math.pi * i / 24
            pts.append((cx + r * math.cos(t), cy + r * 0.52 * math.sin(t)))
        pts[0] = (cx + r * 1.12, cy)
        pts[12] = (cx - r * 1.12, cy)
    elif cut == "heart":
        pts = []
        for i in range(60):
            t = 2 * math.pi * i / 60
            hx = 16 * math.sin(t) ** 3
            hy = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
            pts.append((cx + hx * r / 17, cy + hy * r / 15))
    else:
        pts = _facet_poly(cx, cy, r, 8, math.pi / 8)

    body = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    bd.polygon(pts, fill=mix(color, (255, 255, 255), .35) + (255,))
    # crown facets: alternate light / deep wedges around the table
    for i in range(8):
        a0 = math.pi * 2 * i / 8 + math.radians(rot)
        a1 = math.pi * 2 * (i + 1) / 8 + math.radians(rot)
        shade = mix(color, (255, 255, 255), .82) if i % 2 == 0 else mix(color, (0, 0, 0), .22)
        bd.polygon([(cx, cy), (cx + r * math.cos(a0), cy + r * math.sin(a0) * (0.55 if cut == "marquise" else 1)),
                    (cx + r * math.cos(a1), cy + r * math.sin(a1) * (0.55 if cut == "marquise" else 1))],
                   fill=shade + (255,))
    # table
    bd.polygon(_facet_poly(cx, cy, r * 0.42, 8, math.pi / 8),
               fill=mix(color, (255, 255, 255), .72) + (255,))
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    clipped = Image.new("RGBA", img.size, (0, 0, 0, 0))
    clipped.paste(body, (0, 0), m)
    img.alpha_composite(clipped)
    d.polygon(pts, outline=(255, 255, 255, 220), width=max(1, u(1.2)))
    d.ellipse([cx - r * .34, cy - r * .58, cx - r * .02, cy - r * .22], fill=(255, 255, 255, 250))
    d.ellipse([cx + r * .16, cy + r * .2, cx + r * .34, cy + r * .38], fill=(255, 255, 255, 190))
    return img


def pearl(size, tint=PEARL):
    s = u(size)
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    base = radial_gradient((s, s), (255, 255, 255), mix(tint, (214, 158, 186), .62))
    m = Image.new("L", (s, s), 0)
    ImageDraw.Draw(m).ellipse([0, 0, s - 1, s - 1], fill=255)
    img.paste(base.convert("RGBA"), (0, 0), m)
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([s * .2, s * .14, s * .46, s * .38], fill=(255, 255, 255, 235))
    d.ellipse([s * .58, s * .62, s * .8, s * .82], fill=(255, 255, 255, 110))
    d.ellipse([0, 0, s - 1, s - 1], outline=(255, 255, 255, 140), width=max(1, u(1)))
    return img


def pearl_string(length, bead=20, spacing=1.05, tint=PEARL, arc=0):
    n = int(length / (bead * spacing))
    w, h = u(length), u(bead + abs(arc) + 6)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    b = pearl(bead, tint)
    for i in range(n + 1):
        x = i * u(bead * spacing)
        t = i / max(1, n)
        yy = u(abs(arc)) * math.sin(math.pi * t) if arc else 0
        img.alpha_composite(b, (int(x), int(yy)))
    return img


def sparkle(size, color=(255, 255, 255), glow_c=None, tails=1.9):
    s = u(size)
    pad = int(s * tails)
    img = Image.new("RGBA", (pad * 2, pad * 2), (0, 0, 0, 0))
    cx = cy = pad
    if glow_c:
        g = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse([cx - s * .8, cy - s * .8, cx + s * .8, cy + s * .8],
                                  fill=glow_c + (110,))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(s * .32)))
    d = ImageDraw.Draw(img, "RGBA")
    long_r, short_r = s * tails, s * 0.19
    d.polygon([(cx, cy - long_r), (cx + short_r, cy - short_r), (cx + long_r * .62, cy),
               (cx + short_r, cy + short_r), (cx, cy + long_r), (cx - short_r, cy + short_r),
               (cx - long_r * .62, cy), (cx - short_r, cy - short_r)], fill=color + (255,))
    d.ellipse([cx - s * .12, cy - s * .12, cx + s * .12, cy + s * .12], fill=(255, 255, 255, 255))
    return img


def butterfly(size, c1=MAGENTA, c2=ROSE, rot=0):
    """Glossy silhouette butterfly, traced from an explicit wing path."""
    s = u(size)
    cx, cy = s / 2, s / 2
    half = [(0.02, -0.32), (0.09, -0.43), (0.20, -0.50), (0.33, -0.50), (0.43, -0.44),
            (0.47, -0.33), (0.45, -0.21), (0.37, -0.11), (0.24, -0.04), (0.31, 0.03),
            (0.39, 0.12), (0.42, 0.24), (0.36, 0.34), (0.25, 0.38), (0.14, 0.33),
            (0.07, 0.22), (0.03, 0.08)]
    pts = [(cx + x * s, cy + yy * s) for x, yy in half]
    pts += [(cx - x * s, cy + yy * s) for x, yy in reversed(half)]
    m = Image.new("L", (s, s), 0)
    md = ImageDraw.Draw(m)
    md.polygon(pts, fill=255)
    md.ellipse([cx - s * .032, cy - s * .33, cx + s * .032, cy + s * .30], fill=255)
    md.ellipse([cx - s * .05, cy - s * .38, cx + s * .05, cy - s * .27], fill=255)
    grad = linear_gradient((s, s), [(0, mix(c1, (255, 255, 255), .5)), (.42, c1),
                                    (1, mix(c2, (0, 0, 0), .16))])
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    img.paste(grad.convert("RGBA"), (0, 0), m)
    for sgn in (-1, 1):                                   # wing-edge sheen, not eyes
        gl = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        ImageDraw.Draw(gl).ellipse([cx + sgn * s * .34 - s * .18, cy - s * .44,
                                    cx + sgn * s * .34 + s * .18, cy - s * .30],
                                   fill=(255, 255, 255, 130))
        gl = gl.rotate(-24 * sgn, resample=Image.BICUBIC, center=(cx, cy))
        g2 = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        g2.paste(gl, (0, 0), m)
        img.alpha_composite(g2.filter(ImageFilter.GaussianBlur(u(4))))
    d = ImageDraw.Draw(img, "RGBA")
    d.polygon(pts, outline=NOIR + (255,), width=max(2, u(1.6)))
    d.ellipse([cx - s * .032, cy - s * .33, cx + s * .032, cy + s * .30],
              outline=NOIR + (255,), width=max(2, u(1.4)), fill=mix(c1, (0, 0, 0), .25) + (255,))
    for sgn in (-1, 1):                                   # antennae, drawn in ink so they read
        d.line([(cx + sgn * s * .015, cy - s * .31), (cx + sgn * s * .11, cy - s * .42),
                (cx + sgn * s * .19, cy - s * .46)], fill=NOIR + (255,), width=max(2, u(1.6)),
               joint="curve")
        d.ellipse([cx + sgn * s * .19 - u(4), cy - s * .46 - u(4),
                   cx + sgn * s * .19 + u(4), cy - s * .46 + u(4)], fill=NOIR + (255,))
    rim = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    rim.paste(Image.new("RGBA", (s, s), (255, 255, 255, 255)), (0, 0),
              ImageChops.subtract(m.filter(ImageFilter.MaxFilter(max(3, u(3) * 2 + 1))), m))
    out = Image.alpha_composite(rim, img)
    return out.rotate(rot, resample=Image.BICUBIC, expand=True) if rot else out


def jewel_outline(art, stone=17, color=MAGENTA, step=None, pad=None):
    """Scatter stones sparsely around a silhouette — jewels beside the letters,
    never paved over them, so thin script stays legible."""
    pad = pad if pad is not None else u(stone)
    base = Image.new("RGBA", (art.size[0] + pad * 2, art.size[1] + pad * 2), (0, 0, 0, 0))
    base.alpha_composite(art, (pad, pad))
    a = base.split()[3].point(lambda v: 255 if v > 120 else 0)
    ring = ImageChops.subtract(a.filter(ImageFilter.MaxFilter(u(9) * 2 + 1)),
                               a.filter(ImageFilter.MaxFilter(u(4) * 2 + 1)))
    px = ring.load()
    g = gem(stone, color)
    step = step or u(stone) * 2.9
    placed = []
    w, h = ring.size
    for yy in range(0, h, max(2, int(step / 3))):
        for xx in range(0, w, max(2, int(step / 3))):
            if px[xx, yy] > 120 and all((xx - a0) ** 2 + (yy - b0) ** 2 > step ** 2
                                        for a0, b0 in placed[-120:]):
                placed.append((xx, yy))
                base.alpha_composite(g, (int(xx - g.size[0] / 2), int(yy - g.size[1] / 2)))
    return base


def gem_heart(size, color=MAGENTA, stone=13):
    """A heart paved with rhinestones."""
    s = u(size)
    img = Image.new("RGBA", (s, int(s * .92)), (0, 0, 0, 0))
    m = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(m)
    cx, cy = s / 2, s * .46
    pts = []
    for i in range(80):
        t = 2 * math.pi * i / 80
        hx = 16 * math.sin(t) ** 3
        hy = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + hx * s / 36, cy + hy * s / 32))
    md.polygon(pts, fill=255)
    px = m.load()
    g = gem(stone, color)
    step = u(stone) * 0.86
    yy = 0
    row = 0
    while yy < img.size[1]:
        xx = (row % 2) * step / 2
        while xx < img.size[0]:
            ix, iy = int(min(xx, img.size[0] - 1)), int(min(yy, img.size[1] - 1))
            if px[ix, iy] > 160:
                img.alpha_composite(g, (int(xx - g.size[0] / 2), int(yy - g.size[1] / 2)))
            xx += step
        yy += step * 0.88
        row += 1
    return img


def gem_trim(length, horizontal=True, stone=15, color=MAGENTA, spacing=0.92):
    n = int(length / (stone * spacing))
    g = gem(stone, color)
    if horizontal:
        img = Image.new("RGBA", (u(length), g.size[1]), (0, 0, 0, 0))
        for i in range(n + 1):
            img.alpha_composite(g, (int(i * u(stone * spacing)), 0))
    else:
        img = Image.new("RGBA", (g.size[0], u(length)), (0, 0, 0, 0))
        for i in range(n + 1):
            img.alpha_composite(g, (0, int(i * u(stone * spacing))))
    return img


def gem_frame(size, stone=16, color=MAGENTA, fill=None, inset=None):
    """Photo frame paved with stones. Returns (image, inner_rect)."""
    w, h = u(size[0]), u(size[1])
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = u(stone) * 0.9
    if fill:
        d.rectangle([pad * .5, pad * .5, w - pad * .5, h - pad * .5], fill=fill + (255,))
    g = gem(stone, color)
    step = u(stone) * 0.82
    gx = g.size[0] / 2
    x = 0
    while x <= w:
        img.alpha_composite(g, (int(x - gx), int(-gx)))
        img.alpha_composite(g, (int(x - gx), int(h - gx)))
        x += step
    yy = 0
    while yy <= h:
        img.alpha_composite(g, (int(-gx), int(yy - gx)))
        img.alpha_composite(g, (int(w - gx), int(yy - gx)))
        yy += step
    ins = inset if inset is not None else int(pad)
    return img, (ins, ins, w - ins, h - ins)


def glass_panel(size, radius=18, tint=(255, 255, 255), alpha=214, edge=(255, 255, 255), shadow=True):
    w, h = u(size[0]), u(size[1])
    pad = u(18)
    img = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    r = u(radius)
    if shadow:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([pad, pad, pad + w, pad + h], r, fill=(190, 110, 160, 110))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(u(11))), (0, u(5)))
    body = Image.new("RGBA", (w, h), tint + (alpha,))
    gl = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(gl).rectangle([0, 0, w, h * 0.40], fill=(255, 255, 255, 95))
    body.alpha_composite(gl.filter(ImageFilter.GaussianBlur(u(16))))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    panel = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    panel.paste(body, (0, 0), m)
    ImageDraw.Draw(panel).rounded_rectangle([0, 0, w - 1, h - 1], r, outline=edge + (230,),
                                            width=max(2, u(1.6)))
    img.alpha_composite(panel, (pad, pad))
    return img


def hairline(length, color=NOIR, weight=1.2, horizontal=True):
    if horizontal:
        img = Image.new("RGBA", (u(length), max(1, u(weight))), color + (255,))
    else:
        img = Image.new("RGBA", (max(1, u(weight)), u(length)), color + (255,))
    return img


def lace_black(width, depth, color=NOIR, flip=False):
    return lace_strip(width, depth, color=color, flip=flip, scallop=u(26))


def leopard_chic(size, seed=7):
    return leopard(size, base=BLUSH, ring=NOIR, core=MAGENTA, density=0.00019, seed=seed)


def script(text, size, stops=None, gems=False, font_name=None, rim=None, shadow=None):
    """The signature: script lettering in rose-chrome, optionally jewelled."""
    fnt = font(font_name or PINYON, size)
    stops = stops or ROSE_CHROME
    if gems:
        return bedazzled(text, fnt, stops=stops, gem_r=max(u(3), int(fnt.size * 0.035)),
                         outline=u(2))
    return grad_text(text, fnt, stops, outline=u(2), outline_c=NOIR,
                     rim=rim if rim is not None else u(6),
                     shadow=shadow if shadow is not None else u(5))


def chic_window(size, title, accent=MAGENTA, body=(255, 255, 255), alpha=236):
    """A glossy pink window — the interface motif, dressed up."""
    w, h = u(size[0]), u(size[1])
    bh = u(44)
    pad = u(16)
    img = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([pad, pad, pad + w, pad + h], u(16), fill=(190, 100, 155, 120))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(u(10))), (0, u(5)))
    panel = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(panel)
    d.rounded_rectangle([0, 0, w - 1, h - 1], u(16), fill=body + (alpha,))
    bar = linear_gradient((w, bh), [(0, mix(accent, (255, 255, 255), .62)), (.46, accent),
                                    (.54, mix(accent, (0, 0, 0), .18)), (1, mix(accent, (0, 0, 0), .04))])
    bm = Image.new("L", (w, bh), 0)
    ImageDraw.Draw(bm).rounded_rectangle([0, 0, w - 1, bh * 2], u(16), fill=255)
    panel.paste(bar.convert("RGBA"), (0, 0), bm)
    gl = Image.new("RGBA", (w, bh), (0, 0, 0, 0))
    ImageDraw.Draw(gl).ellipse([-w * .1, -bh * .85, w * 1.1, bh * .5], fill=(255, 255, 255, 120))
    g2 = Image.new("RGBA", (w, bh), (0, 0, 0, 0))
    g2.paste(gl, (0, 0), bm)
    panel.alpha_composite(g2)
    t = tracked(title.upper(), font(OSWALD, 15), (255, 255, 255), tracking=5)
    panel.alpha_composite(t, (u(20), int(bh / 2 - t.size[1] / 2)))
    for i in range(3):
        cxx = w - u(28) - i * u(30)
        panel.alpha_composite(pearl(15), (int(cxx - u(7)), int(bh / 2 - u(7))))
    d.rounded_rectangle([0, 0, w - 1, h - 1], u(16), outline=(255, 255, 255, 230), width=max(2, u(2)))
    img.alpha_composite(panel, (pad, pad))
    return img, (pad, pad + bh, pad + w, pad + h)


def bloom(img, strength=0.4, radius=22):
    """Soft glossy bloom over the whole composition."""
    base = img.convert("RGBA")
    bright = base.filter(ImageFilter.GaussianBlur(u(radius)))
    return Image.blend(base, Image.alpha_composite(base, bright), strength * 0.35)
