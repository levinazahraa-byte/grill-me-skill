# -*- coding: utf-8 -*-
"""Raster foundry for the LONGSHOT poster direction.

Only the things a PowerPoint shape genuinely cannot be: chrome italic display
type, film grain, airbrush blends, soft glows. Everything else in v06 stays a
native editable shape.
"""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = "/root/.local/share/fonts/deck"
S = 2.0                                   # render scale (design px -> px)

def u(v):
    return int(round(v * S))

_fc = {}
def font(name, size):
    key = (name, int(size * S))
    if key not in _fc:
        _fc[key] = ImageFont.truetype(os.path.join(FONTS, name), max(6, int(size * S)))
    return _fc[key]

BLACK = "ArchivoBlack-Regular.ttf"
ANTON = "Anton-Regular.ttf"

CHROME = [(0.00, (255, 255, 255)), (0.13, (226, 238, 252)), (0.34, (128, 156, 196)),
          (0.46, (30, 46, 86)), (0.505, (30, 46, 86)), (0.55, (120, 166, 220)),
          (0.68, (255, 255, 255)), (0.84, (198, 220, 248)), (1.00, (96, 130, 190))]
GOLD = [(0.00, (255, 252, 214)), (0.30, (255, 214, 82)), (0.48, (150, 92, 10)),
        (0.53, (240, 190, 70)), (0.74, (255, 250, 210)), (1.00, (196, 140, 30))]


def _grad(size, stops):
    w, h = size
    col = Image.new("RGB", (1, h))
    d = ImageDraw.Draw(col)
    for i in range(h):
        t = i / max(1, h - 1)
        lo, hi = stops[0], stops[-1]
        for j in range(len(stops) - 1):
            if stops[j][0] <= t <= stops[j + 1][0]:
                lo, hi = stops[j], stops[j + 1]
                break
        span = max(1e-6, hi[0] - lo[0])
        k = (t - lo[0]) / span
        d.point((0, i), fill=tuple(int(lo[1][c] + (hi[1][c] - lo[1][c]) * k) for c in range(3)))
    return col.resize((w, h), Image.BILINEAR)


def chrome_text(text, size=100, stops=None, shear=0.22, outline=7, rim=9, shadow=12,
                font_name=BLACK, rim_color=(255, 255, 255), outline_color=(8, 10, 24)):
    """Big italic chrome lettering — the poster's voice."""
    stops = stops or CHROME
    f = font(font_name, size)
    pad = u(40)
    tmp = ImageDraw.Draw(Image.new("L", (10, 10)))
    bb = tmp.textbbox((0, 0), text, font=f)
    w, h = bb[2] - bb[0] + pad * 2, bb[3] - bb[1] + pad * 2
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).text((pad - bb[0], pad - bb[1]), text, font=f, fill=255)
    if shear:
        w2 = w + int(h * abs(shear))
        m = m.transform((w2, h), Image.AFFINE, (1, shear, -shear * h if shear > 0 else 0, 0, 1, 0),
                        resample=Image.BICUBIC)
        w = w2
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ow, rw = u(outline), u(rim)
    if shadow:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sh.paste(Image.new("RGBA", (w, h), (0, 0, 0, 170)), (0, 0),
                 m.filter(ImageFilter.MaxFilter(ow * 2 + 1)))
        out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(u(5))), (u(shadow), u(shadow)))
    if rw:
        r = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        r.paste(Image.new("RGBA", (w, h), rim_color + (255,)), (0, 0),
                m.filter(ImageFilter.MaxFilter((ow + rw) * 2 + 1)))
        out.alpha_composite(r)
    if ow:
        o = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        o.paste(Image.new("RGBA", (w, h), outline_color + (255,)), (0, 0),
                m.filter(ImageFilter.MaxFilter(ow * 2 + 1)))
        out.alpha_composite(o)
    body = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    body.paste(_grad((w, h), stops).convert("RGBA"), (0, 0), m)
    out.alpha_composite(body)
    gl = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(gl).ellipse([-w * .2, -h * .5, w * 1.2, h * .34], fill=(255, 255, 255, 96))
    g2 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g2.paste(gl, (0, 0), m)
    out.alpha_composite(g2.filter(ImageFilter.GaussianBlur(u(1.5))))
    return out


def blob(size, color=(10, 14, 34), alpha=210, blur=44):
    """The dark blurred ellipse the headline sits on."""
    w, h = u(size[0]), u(size[1])
    pad = u(blur) * 2
    img = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(img).ellipse([pad, pad, pad + w, pad + h], fill=color + (alpha,))
    return img.filter(ImageFilter.GaussianBlur(u(blur)))


def wash(size, blocks, blur=90, seed=3, scale=1.0):
    """Airbrushed colour-field ground: blocks bled into each other.

    Rendered at 1x by default — it is a blur, so extra pixels buy nothing.
    """
    def u(v):
        return int(round(v * scale))
    w, h = u(size[0]), u(size[1])
    img = Image.new("RGB", (w, h), blocks[0][4])
    d = ImageDraw.Draw(img)
    for x0, y0, x1, y1, col in blocks:
        d.rectangle([u(x0), u(y0), u(x1), u(y1)], fill=col)
    img = img.filter(ImageFilter.GaussianBlur(u(blur)))
    return img


def grain(size, amount=20, seed=7, scale=0.5):
    def u(v):
        return int(round(v * scale))
    w, h = u(size[0]), u(size[1])
    rng = np.random.default_rng(seed)
    n = rng.integers(0, 255, (h // 2, w // 2), dtype=np.uint8)
    g = Image.fromarray(n, "L").resize((w, h), Image.NEAREST)
    out = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    out.putalpha(g.point(lambda v: int(v * amount / 255)))
    return out


def glow_cut(size, radius=26, color=(255, 255, 255), alpha=255):
    """White halo used behind cut-out photos."""
    w, h = u(size[0]), u(size[1])
    pad = u(radius) * 3
    img = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(img).rectangle([pad, pad, pad + w, pad + h], fill=color + (alpha,))
    return img.filter(ImageFilter.GaussianBlur(u(radius)))


def burst(size, fill=(255, 228, 0), edge=(12, 16, 40), points=10, inner=0.42, rot=0,
          glow=(255, 255, 255), lw=6):
    """Spiky starburst with outline and halo."""
    s = u(size)
    pad = u(24)
    img = Image.new("RGBA", (s + pad * 2, s + pad * 2), (0, 0, 0, 0))
    cx = cy = (s + pad * 2) / 2
    r = s / 2
    pts = []
    for i in range(points * 2):
        a = math.pi * i / points + math.radians(rot)
        rad = r if i % 2 == 0 else r * inner
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    if glow:
        g = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).polygon(pts, fill=glow + (255,))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(u(9))))
    d = ImageDraw.Draw(img)
    d.polygon(pts, fill=fill + (255,), outline=edge + (255,), width=u(lw))
    return img


def star5(size, fill=(255, 255, 255), edge=(30, 60, 200), rot=0, lw=6, glow=True):
    s = u(size)
    pad = u(20)
    img = Image.new("RGBA", (s + pad * 2, s + pad * 2), (0, 0, 0, 0))
    cx = cy = (s + pad * 2) / 2
    r = s / 2
    pts = []
    for i in range(10):
        a = -math.pi / 2 + math.pi * i / 5 + math.radians(rot)
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    if glow:
        g = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).polygon(pts, fill=(255, 255, 255, 255))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(u(7))))
    ImageDraw.Draw(img).polygon(pts, fill=fill + (255,), outline=edge + (255,), width=u(lw))
    return img


def save_all(outdir):
    os.makedirs(outdir, exist_ok=True)
    return outdir
