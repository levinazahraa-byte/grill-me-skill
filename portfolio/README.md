# Zahra Levina — 2026 Portfolio Deck

A 10-slide, 16:9 (1920×1080) portfolio deck styled as a 2000s desktop OS:
every slide is a window on a patterned desktop, bound together by a taskbar
that runs across all ten slides.

## Files

| File | What it's for |
|---|---|
| `zahra-levina-portfolio-2026.pptx` | The editable deck — open in PowerPoint, Keynote, Google Slides, or import to Canva |
| `zahra-levina-portfolio-2026.pdf` | Flat export for emailing or attaching to applications |
| `build_deck.py` | Regenerates the .pptx from scratch (`pip install python-pptx && python3 build_deck.py`) |

## Design system

**Palette** — split by section, bound by shared window chrome:

- Candy pink (slides 1, 2, 5, 10): `#FF6FB5` → `#C77DFF` title bars, `#FFE3F1` desktop
- Frutiger aero (slides 3, 4, 6, 7, 8, 9): `#7FD4F7` → `#3A8FD6` title bars, lime→sky desktop
- Ink `#2B2340`, muted `#6E6486`, lime pop `#C6F24E`

**Type** — all system-safe, so the file looks the same on any machine:

- Headlines: Arial Black
- UI chrome, chips, labels: Tahoma
- Mono details (paths, filenames, contact): Courier New
- Body copy: Verdana

Every ornament (stars, hearts, arrows, window buttons) is a drawn shape, not a
font glyph — nothing breaks if a machine lacks a symbol font.

## What you need to swap in

**Photos** — dashed frames marked with their exact pixel size:

- Slide 1: portrait, 410 × 412, in the tilted polaroid
- Slide 2: photo, 368 × 380, in the webcam window
- Slide 5: Sawala Space visual 470 × 300, plus two 225 × 236 photos
- Slide 6: eight gallery thumbnails, 386 × 164 each
- Slide 7: event poster 470 × 620, plus two 186 × 130 documentation shots

To replace one in PowerPoint: right-click the dashed frame → Format Shape →
Fill → Picture or texture fill → Insert. The frame keeps its size and position.
Then delete the caption text box sitting on top of it.

**Contact details** — currently placeholders, on slides 1 and 10:

- `+62 8xx-xxxx-xxxx`
- `hello@email.com`
- `linkedin.com/in/username`
