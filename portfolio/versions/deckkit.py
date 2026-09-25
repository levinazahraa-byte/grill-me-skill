# -*- coding: utf-8 -*-
"""Native PPTX toolkit — everything it makes is an editable shape or text box.

No flattened slides: fills, gradients, outlines, corner radii and copy all stay
live so the decks can be reworked in Canva or PowerPoint.
"""

import copy, os
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE, MSO_THEME_COLOR
from pptx.oxml.ns import qn
from lxml import etree

W, H = 1920, 1080

def px(v):
    return Emu(int(round(v * 6350)))

def C(h):
    return RGBColor.from_string(h.lstrip("#").upper())


def _shadow(shape, blur=28, dist=10, direction=5400000, color="000000", alpha=22):
    """Outer shadow via DrawingML (PowerPoint keeps it live and editable)."""
    spPr = shape._element.spPr
    for tag in ("a:effectLst",):
        for e in spPr.findall(qn(tag)):
            spPr.remove(e)
    ns = "http://schemas.openxmlformats.org/drawingml/2006/main"
    eff = etree.SubElement(spPr, "{%s}effectLst" % ns)
    sh = etree.SubElement(eff, "{%s}outerShdw" % ns)
    sh.set("blurRad", str(int(blur * 12700)))
    sh.set("dist", str(int(dist * 12700)))
    sh.set("dir", str(int(direction)))
    sh.set("rotWithShape", "0")
    clr = etree.SubElement(sh, "{%s}srgbClr" % ns)
    clr.set("val", color.lstrip("#").upper())
    a = etree.SubElement(clr, "{%s}alpha" % ns)
    a.set("val", str(int(alpha * 1000)))


class Slide(object):
    def __init__(self, sl):
        self.sl = sl

    # ---------------------------------------------------------------- shapes
    def shape(self, kind, x, y, w, h, fill=None, grad=None, angle=90, line=None,
              lw=1.5, radius=None, rot=0, dash=None, shadow=None, adj=None, alpha=None):
        s = self.sl.shapes.add_shape(kind, px(x), px(y), px(w), px(h))
        s.shadow.inherit = False
        if radius is not None:
            try:
                s.adjustments[0] = radius
            except Exception:
                pass
        if adj is not None:
            for i, v in enumerate(adj):
                try:
                    s.adjustments[i] = v
                except Exception:
                    pass
        if grad:
            s.fill.gradient()
            stops = s.fill.gradient_stops
            stops[0].color.rgb = C(grad[0])
            stops[0].position = 0.0
            stops[1].color.rgb = C(grad[1])
            stops[1].position = 1.0
            s.fill.gradient_angle = angle
        elif fill:
            s.fill.solid()
            s.fill.fore_color.rgb = C(fill)
            if alpha is not None:
                ns = "http://schemas.openxmlformats.org/drawingml/2006/main"
                clr = s.fill._xPr.find(qn("a:solidFill")).find(qn("a:srgbClr"))
                a = etree.SubElement(clr, "{%s}alpha" % ns)
                a.set("val", str(int(alpha * 1000)))
        else:
            s.fill.background()
        if line:
            s.line.color.rgb = C(line)
            s.line.width = Pt(lw)
            if dash:
                s.line.dash_style = dash
        else:
            s.line.fill.background()
        if rot:
            s.rotation = rot
        if shadow:
            _shadow(s, **shadow) if isinstance(shadow, dict) else _shadow(s)
        s.text_frame.word_wrap = True
        return s

    def rect(self, *a, **k):
        return self.shape(MSO_SHAPE.RECTANGLE, *a, **k)

    def rrect(self, *a, **k):
        k.setdefault("radius", 0.08)
        return self.shape(MSO_SHAPE.ROUNDED_RECTANGLE, *a, **k)

    def oval(self, *a, **k):
        return self.shape(MSO_SHAPE.OVAL, *a, **k)

    def bg(self, fill=None, grad=None, angle=90):
        return self.rect(0, 0, W, H, fill=fill, grad=grad, angle=angle)

    def line(self, x, y, length, color="000000", weight=1.2, vertical=False, dash=None):
        s = self.rect(x, y, weight if vertical else length, length if vertical else weight,
                      fill=color)
        if dash:
            s.line.color.rgb = C(color)
            s.line.width = Pt(weight)
            s.line.dash_style = dash
        return s

    # ---------------------------------------------------------------- text
    def text(self, x, y, w, h, body, font="Poppins", size=14, bold=False, italic=False,
             color="000000", align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.4,
             tracking=0, after=8, shape=None, caps=False):
        if shape is None:
            tb = self.sl.shapes.add_textbox(px(x), px(y), px(w), px(h))
        else:
            tb = shape
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = anchor
        lines = body if isinstance(body, (list, tuple)) else [body]
        for i, t in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            p.line_spacing = spacing
            p.space_after = Pt(after if len(lines) > 1 else 0)
            r = p.add_run()
            r.text = t.upper() if caps else t
            r.font.name = font
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.italic = italic
            r.font.color.rgb = C(color)
            if tracking:
                r.font._rPr.set("spc", str(int(tracking * 100)))
        return tb

    def label(self, x, y, w, text, size=12, color="000000", tracking=6, font="Oswald",
              align=PP_ALIGN.LEFT, bold=False, caps=True):
        return self.text(x, y, w, size * 2.4, text, font=font, size=size, bold=bold,
                         color=color, align=align, tracking=tracking, caps=caps)

    # ---------------------------------------------------------------- parts
    def photo(self, x, y, w, h, label="drop photo", fill="EDEDF2", line="B9B4C6",
              radius=None, rot=0, dash=True, font="Poppins", size=10,
              label_color="8C8698", shadow=None):
        kind = MSO_SHAPE.ROUNDED_RECTANGLE if radius is not None else MSO_SHAPE.RECTANGLE
        s = self.shape(kind, x, y, w, h, fill=fill, line=line, lw=1.25, radius=radius,
                       rot=rot, dash=MSO_LINE_DASH_STYLE.DASH if dash else None,
                       shadow=shadow)
        p = s.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        s.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        r = p.add_run()
        r.text = label
        r.font.name = font
        r.font.size = Pt(size)
        r.font.color.rgb = C(label_color)
        return s

    def pill(self, x, y, text, size=12, pad=34, h=44, fill="FFFFFF", color="000000",
             line=None, font="Oswald", tracking=5, bold=False, radius=0.5, width=None):
        w = width or (pad * 2 + len(text) * (size * 1.3 + tracking * 2.2))
        s = self.shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=fill, line=line,
                       lw=1.25, radius=radius)
        tf = s.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = text
        r.font.name = font
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = C(color)
        if tracking:
            r.font._rPr.set("spc", str(int(tracking * 100)))
        return w

    def window(self, x, y, w, h, title, bar="FF6FB5", bar2=None, body="FFFFFF",
               radius=0.05, bar_h=46, title_font="Poppins", title_size=13,
               title_color="FFFFFF", dots=True, dot_colors=("FFFFFF",) * 3,
               line=None, shadow=True, tracking=2):
        """A window card: frame, title bar, buttons — all separate editable shapes."""
        frame = self.rrect(x, y, w, h, fill=body, line=line, lw=1.5, radius=radius,
                           shadow={} if shadow else None)
        if bar2:
            self.rrect(x, y, w, bar_h * 2, grad=(bar, bar2), angle=90, radius=radius * 2)
        else:
            self.rrect(x, y, w, bar_h * 2, fill=bar, radius=radius * 2)
        self.rect(x, y + bar_h - 2, w, 2, fill=bar2 or bar)
        self.text(x + 22, y, w - 140, bar_h, title, font=title_font, size=title_size,
                  color=title_color, anchor=MSO_ANCHOR.MIDDLE, tracking=tracking)
        if dots:
            for i, c in enumerate(dot_colors):
                self.oval(x + w - 34 - i * 30, y + bar_h / 2 - 9, 18, 18, fill=c)
        return frame, (x, y + bar_h, w, h - bar_h)

    def bubble(self, x, y, w, h, text, fill="FFFFFF", line="000000", lw=2.5, color="000000",
               font="Poppins", size=14, tail="bl", radius=0.28, spacing=1.45, pad=34):
        self.rrect(x, y, w, h, fill=fill, line=line, lw=lw, radius=radius)
        if tail:
            tx = x + 44 if tail.endswith("l") else x + w - 76
            t = self.shape(MSO_SHAPE.ISOSCELES_TRIANGLE, tx, y + h - 4, 34, 26,
                           fill=fill, line=line, lw=lw)
            t.rotation = 180
            self.rect(tx + 2, y + h - 8, 30, 8, fill=fill)
        self.text(x + pad, y + 18, w - pad * 2, h - 34, text, font=font, size=size,
                  color=color, spacing=spacing, anchor=MSO_ANCHOR.MIDDLE)

    def pic(self, path, x, y, w, h=None):
        if h is None:
            from PIL import Image
            im = Image.open(path)
            h = w * im.size[1] / im.size[0]
        return self.sl.shapes.add_picture(path, px(x), px(y), px(w), px(h))

    def star(self, x, y, size, fill="FFE83D", line=None, lw=2, points=5, rot=0):
        kind = {4: MSO_SHAPE.STAR_4_POINT, 5: MSO_SHAPE.STAR_5_POINT,
                8: MSO_SHAPE.STAR_8_POINT, 16: MSO_SHAPE.STAR_16_POINT,
                24: MSO_SHAPE.STAR_24_POINT}[points]
        return self.shape(kind, x, y, size, size, fill=fill, line=line, lw=lw, rot=rot)

    def heart(self, x, y, size, fill="FF2E93", line=None, lw=2, rot=0):
        return self.shape(MSO_SHAPE.HEART, x, y, size, size * 0.92, fill=fill, line=line,
                          lw=lw, rot=rot)


class Deck(object):
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = px(W), px(H)
        self.blank = self.prs.slide_layouts[6]

    def new(self):
        return Slide(self.prs.slides.add_slide(self.blank))

    def save(self, path):
        self.prs.save(path)
        return path
