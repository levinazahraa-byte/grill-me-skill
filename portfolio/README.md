# Zahra Levina — 2026 Portfolio · "Angel" direction

A Y2K fashion-editorial portfolio: tonal pink, black lace, pink leopard,
rhinestone and chrome-script lettering, pearl strings and butterflies.
Interface elements appear only where they serve the story, dressed in the same
palette — never as the organising idea.

## The visual system

**Palette — deliberately tonal.** Earlier drafts used pink *and* lilac *and*
cyan *and* lime, which is what makes a deck read like a template. This one runs
almost entirely on pink against black, with ice blue as a rare cool accent.

`#FF2E93` magenta · `#FF8FC5` rose · `#FFDDEE` blush · `#FFF4F9` shell
`#100A16` noir · `#FFF8F2` pearl · `#C6E8F6` ice (sparingly)

**Type — editorial, not chunky.**

| Role | Face |
|---|---|
| Section titles | Italiana, widely letterspaced |
| The name, signature words | Pinyon Script in rose-chrome, jewelled |
| Numerals, event titles | Bodoni Moda |
| Labels, pills, small caps | Oswald, tracked |
| Interface asides | Silkscreen |
| Body copy (live text) | Trebuchet MS |

**Decorative vocabulary** — all painted in `y2k.py`, not assembled from basic
shapes: brilliant-cut rhinestones (round, marquise, heart) with facets and
specular highlights, rhinestone-paved hearts, jewelled photo frames, pearl
strings, glossy butterflies, scalloped black lace, pink leopard, halftone
fields, frosted glass panels, hairline editorial rules.

## Ten slides, ten compositions

| # | Composition |
|---|---|
| 1 | Cover — centred portrait, jewelled script wordmark, leopard and lace borders |
| 2 | About — editorial page, wide margins, script name, framed portrait |
| 3 | What I do — numbered index with Bodoni numerals and gem bullets |
| 4 | Where I've been — glossy pink window (the interface motif, dressed) |
| 5 | Sawala Space — cool-girl personal website with leopard spine |
| 6 | Selected works — magazine contact sheet, eight jewelled frames |
| 7 | Stretch for Stray — bold magenta field against shell, lace spine |
| 8 | Beyond — digital scrapbook, three glass cards |
| 9 | Skills & tools — tracked lists with gem bullets, glass pills |
| 10 | Contact — centred, paved gem heart, jewelled script |

## Editability

Every graphic is placed as its **own layer** — 228 separate PNG elements, not a
flattened picture. Opened in Canva or PowerPoint, each gem, butterfly, frame,
pill and type treatment is an individual object you can move, resize, delete or
restyle. Body copy is live text. The element library lives in
`assets/elements/` if you want to drag pieces into other designs.

Headline lettering (script, chrome, tracked titles) is artwork — to change its
wording, edit the string in `build_deck.py` and re-run.

## Files

| File | What it's for |
|---|---|
| `zahra-levina-portfolio-2026.pptx` | The deck — PowerPoint, Keynote, Google Slides, or import to Canva |
| `zahra-levina-portfolio-2026.pdf` | Flat export for sending |
| `y2k.py` | The asset foundry |
| `build_deck.py` | Composes the ten slides |
| `assets/elements/` | Every decorative element as a loose PNG |
| `assets/fonts/` | Display faces (SIL Open Font License) |

```bash
pip install python-pptx pillow numpy
python3 build_deck.py
```

## What you swap in

**Photos** — dashed frames inside the jewelled borders. Right-click → Format
Shape → Fill → Picture fill. The frame, its stones and any butterfly layered on
top all stay put.

| Slide | Frames |
|---|---|
| 1 | portrait, 608 × 496 |
| 2 | portrait, 560 × 700 |
| 5 | 520 × 330 plus two 250 × 250 |
| 6 | eight at 368 × 256 |
| 7 | poster 580 × 660 plus two 250 × 190 |

**Contact details** — `+62 8xx-xxxx-xxxx`, `hello@email.com`,
`linkedin.com/in/username` on slides 1 and 10. Slide 10's are live text; slide
1's labels are artwork.

All typefaces are SIL Open Font Licensed and free for commercial use; sticker
objects are rendered from Noto Color Emoji (also OFL).
