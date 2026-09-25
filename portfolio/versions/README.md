# Five art directions · one portfolio

Same ten slides, same copy, five completely different visual systems — one per
reference. Built to be compared, then developed.

| | Direction | Reference | Mood |
|---|---|---|---|
| **01** | **BEDAZZLED** | Ref 1 | Maximalist Y2K glam — tonal hot pink, leopard, black lace, script + rhinestones. Symmetrical, centred, dense |
| **02** | **DOLLHOUSE** | Ref 2 | Y2K web boutique — pastel storefront, sidebar, window cards, pixel UI, taskbar. Cute, modular, busy |
| **03** | **SOFT DESK** | Ref 3 | Clean creator energy — white browser on soft blue, Archivo Black + yellow highlighter. Airy, minimal, calm |
| **04** | **AERO** | Ref 4 | Frutiger Aero — lime-to-aqua gradients, glossy app panels, status bar and dock. Techy, bright |
| **05** | **CHAT** | Ref 5 | Blown-up message thread — acid yellow/lime, thick black outlines, bubbles, starbursts. Loud, playful |

`00-compare-all-five.png` puts five slides from each side by side.

## Files

Each direction ships as `portfolio-0N-name.pptx` (editable) and `.pdf` (flat).

## Editability

These are **native PowerPoint objects, not flattened images**:

- Text is live text — retype it, restyle it, change the font
- Backgrounds, cards, panels, bars and pills are real shapes with editable
  fills, gradients, outlines and corner radii
- Photo frames are shapes: right-click → Format Shape → Fill → Picture fill
- Direction 01 is the only one using images, for four ornaments that can't be
  shapes (leopard, lace, rhinestones, butterflies). Each is its own layer and
  can be moved or deleted; the source PNGs are in `ornaments/`

Every typeface is a Google Font available in Canva, so nothing substitutes:

| | Display | Secondary | Body |
|---|---|---|---|
| 01 | Great Vibes, Italiana | Oswald | Poppins |
| 02 | Fredoka | VT323 | Poppins |
| 03 | Archivo Black | Space Mono | Inter |
| 04 | Nunito | Poppins | Nunito |
| 05 | Anton | Space Mono | Poppins |

## Code

`deckkit.py` is the shared toolkit (shapes, text, windows, pills, bubbles,
photo frames). `content.py` holds the copy once — edit it and every version
updates. `v01_*.py` … `v05_*.py` are the five layout systems; they share no
layout code, only primitives.

```bash
pip install python-pptx pillow lxml
python3 build_all.py
```

## Status

These are direction explorations, not finished decks. Type is sized by
calculation rather than measurement, so a few labels still sit tighter than
ideal. Pick a direction and it gets a proper typesetting pass.
