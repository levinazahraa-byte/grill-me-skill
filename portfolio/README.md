# Zahra Levina — 2026 Portfolio Deck (Y2K edition)

Ten 16:9 slides (1920×1080) where the Y2K visual language *is* the identity —
leopard and lace, chrome and bedazzled type, halftone, gingham, holographic
foil, glossy gel buttons, torn paper, washi tape, polaroids and sticker
cut-outs. The desktop/interface idea survives as a supporting device on three
slides, not as the design system.

Every slide is a different format:

| # | Format |
|---|---|
| 1 | Cover poster — leopard border, lace trim, bedazzled + chrome name |
| 2 | Scrapbook page — grid paper, torn-paper panel, tape, speech bubble |
| 3 | Magazine spread — halftone field, four cards in four materials |
| 4 | Desktop explorer — sky wallpaper, desk icons, window, taskbar |
| 5 | Early-2000s personal website — marquee, menu, guestbook, under construction |
| 6 | Contact sheet — eight tilted polaroids, tape, checkerboard bands |
| 7 | Event flyer — zigzag borders, starburst, notepad checklist |
| 8 | Cut-and-paste page — gingham, three cards in three materials |
| 9 | Sticker sheet — perforated panel, gel sliders, tool pills |
| 10 | Chat thread — message bubbles, chrome type, contact buttons |

## Files

| File | What it's for |
|---|---|
| `zahra-levina-portfolio-2026.pptx` | The deck — open in PowerPoint, Keynote, Google Slides, or import to Canva |
| `zahra-levina-portfolio-2026.pdf` | Flat export for emailing or attaching |
| `y2k.py` | Asset foundry — textures, type treatments, stickers, glossy UI |
| `build_deck.py` | Composes the ten slides and writes the .pptx |
| `assets/fonts/` | The display typefaces (SIL Open Font License) |
| `assets/slides/` | Rendered slide artwork |

Regenerate after editing either script:

```bash
pip install python-pptx pillow numpy
python3 build_deck.py
```

## How the deck is built

Each slide is **layered artwork** composed in Pillow at 1.5× (2880×1620),
flattened to a full-bleed image, with two live layers on top in PowerPoint:

1. **Background artwork** — textures, type treatments, panels, UI
2. **Photo frames** — real PowerPoint shapes you can picture-fill
3. **Sticker overlay** — transparent PNG so stickers sit *over* your photos
4. **Live text** — your body copy, still editable in PowerPoint

**What this means for editing:** body copy, role lines and list items are live
text you can retype. Headlines and decorative labels are *artwork* — to change
their wording, edit the string in `build_deck.py` and re-run it.

## Typography

Display faces are rendered into the artwork, so nothing needs installing and
nothing substitutes on another machine:

- **Rubik Bubbles** — the bedazzled/chrome name treatments
- **Bungee / Bungee Shade** — chunky headline type
- **Silkscreen · Press Start 2P · VT323** — pixel UI labels
- **Chicle · Modak · Sigmar One · Bagel Fat One** — accents

All are under the SIL Open Font License (free for commercial use). Sticker
graphics are rendered from **Noto Color Emoji**, also OFL. Live body copy uses
Verdana and Tahoma — period-correct for early-2000s web, and on every machine.

## What you need to swap in

**Photos** — dashed frames, already tilted and captioned. In PowerPoint:
right-click the frame → Format Shape → Fill → Picture fill → Insert. The frame
keeps its size, tilt and position, and stickers stay layered on top.

| Slide | Frames |
|---|---|
| 1 | portrait (520×600) + small card (280×300) |
| 2 | webcam photo (480×546) |
| 5 | Sawala Space visual (520×330) + two 250×260 |
| 6 | eight work thumbnails (378×300) |
| 7 | event poster (494×644) + two 424×216 |

**Contact details** — placeholders on slides 1 and 10:
`+62 8xx-xxxx-xxxx` · `hello@email.com` · `linkedin.com/in/username`.
These are drawn into the artwork, so edit them in `build_deck.py` and re-run.

## Palette

`#FF3D9E` hot · `#FF8FD0` bubblegum · `#FFD1EB` baby · `#B27BFF` lilac
`#4DC8FF` cyber · `#C6F24E` lime · `#FFE96B` butter · `#1C1430` ink
