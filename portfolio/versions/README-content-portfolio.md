# Content Production Portfolio — five art directions

Ten slides, one set of copy, five visual systems. Built for a Content
Production Specialist application: the work and the process carry it, not
claims about being qualified.

| | Direction | Feel |
|---|---|---|
| **01** | **BEDAZZLED** | Y2K glam editorial — tonal pink, leopard + black lace, script against display caps, rhinestones, arch and oval photo cut-outs |
| **02** | **DOLLHOUSE** | Pastel Y2K web boutique — banner, nav, window cards, sidebar widgets, pixel UI, taskbar |
| **03** | **SOFT DESK** | Clean creator desktop — white browser on soft blue, Archivo Black + yellow highlighter, folder tabs, sticky notes, dock |
| **04** | **AERO** | Frutiger Aero — lime-to-aqua gradients, glossy app modules, status bar, dock |
| **05** | **CHAT** | Blown-up message thread — acid yellow/lime, thick black outlines, bubbles, starbursts, tilted cards |

`00-compare-content-portfolio.png` shows five slides from each, side by side.

## The ten slides

1. Cover · 2. About · 3. From idea to publish (7-step workflow) · 4. Content, in
different forms (social / visual / production / editing) · 5. Sawala Space ·
6. Content in practice (six pieces with contribution captions) · 7. Stretch for
Stray · 8. Behind the final post (prepare → create → edit → refine → finalize) ·
9. Tools + workflow · 10. Closing.

## Editing in Canva

Nothing is a flattened slide. Text is live text; panels, cards, bars, pills and
frames are real shapes with editable fills, outlines and corner radii.

**Photo frames are shaped placeholders** — arch, oval, hexagon, clipped-corner,
parallelogram — not plain rectangles. Right-click → Format Shape → Fill →
Picture fill and the silhouette is kept. Each carries a caption saying what
belongs there (`event visual`, `content preparation`, `design versions`…).

Direction 01 is the only one using images, for four ornaments that can't be
shapes (leopard, lace, rhinestones, butterflies); each is its own layer and
sources are in `ornaments/`.

Typefaces are Google Fonts available in Canva: Italiana, Great Vibes, Oswald,
Fredoka, VT323, Archivo Black, Inter, Space Mono, Nunito, Anton, Poppins.

## Content notes

Copy lives once in `brief.py` — edit there and all five rebuild in step.

Nothing is claimed that wasn't given: no fashion-industry or brand experience,
no invented clients or metrics, and the tools are only Canva, Adobe Illustrator,
Adobe Photoshop, CapCut, Google Workspace and Microsoft Office. Minitab and the
agriculture/research work are left out as not central to the role.

Contact details are placeholders: `+62 8xx-xxxx-xxxx`, `hello@email.com`,
`linkedin.com/in/username`.

```bash
pip install python-pptx pillow lxml
python3 build_cp.py
```
