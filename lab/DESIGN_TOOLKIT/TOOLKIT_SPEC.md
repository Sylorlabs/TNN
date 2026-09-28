# Zag UI Toolkit — spec (v1, built 2026-09-22)

Pure-Zag 2D UI toolkit. Every delivered pixel is produced by Zag code compiled
with the lab znc toolchain; no image libraries, no OS drawing, no browser.

## Pipeline

```
theme words (24) → screen builders → spec records (mental model)
                                     → rasterizer → RGB canvas → BMP writer → .bmp
                                                        ↘ .png (transport only)
```

BMP bytes are emitted by `d_emit_bmp` in `toolkit.zag` via native syscalls.
PNG files in `your_files/imagination_design/` are pixel-identical conversions
of those BMPs (verified byte-for-byte on decode, B-D3) for viewing only.

## Theme (24 words, `th_new`)

| # | token | # | token |
|---|-------|---|-------|
| 0-2 | bg RGB | 12-14 | text RGB |
| 3-5 | surface RGB | 15 | corner radius px |
| 6-8 | accent RGB | 16 | spacing unit px |
| 9-11 | muted RGB | 17 | screen pad-h px |
| 18 | title scale | 21 | body scale |
| 19 | shadow on/off | 22 | title scale (dup slot, kept for compat) |
| 20 | border on/off | 23 | caption scale |
| 24 | pad-v px | 25 | v-rhythm px |
| 26 | section gap px | | |

## Primitives (`toolkit.zag`)

Canvas/pixel: `d_new`, `d_fill`, `d_px`, `d_rect`, `d_rrect` (rounded rect),
`d_circle`, `d_ring`, `d_line`, `d_trif` (filled triangle, scanline),
`d_blend` (alpha), `d_shadow` (directional soft shadow).
Text: 5x7 bitmap font, ASCII 32-126, packed column-major (`font.zag`,
475 bytes); `d_glyph`, `d_text`, `d_text_c` (centered), `d_text_r`,
`d_text_w` (measure). Scales 1-3 used.
Output: `d_emit_bmp` — BMP header + bottom-up BGR rows, native `writev`-loop.

## Components (`screens.zag`)

`c_navbar` (title, back chevron, battery), `c_tabbar` (3 tabs, active dot),
`c_button` (filled / outline), `c_textfield` (icon + placeholder),
`c_listrow` (art thumb, title, artist, duration, playing state w/ EQ bars),
`c_toggle`, `c_slider` (fill + knob), `c_avatar` (ring + person glyph),
`c_settingrow` (label + toggle / chevron), `c_ibtn` (play/prev/next/shuffle/repeat),
`c_card`, `c_dialog`, `c_progressbar`, `art_album` (deterministic seeded
procedural art: dark field + concentric accent rings), `thumb` (seeded thumb).

## Dual-path builders

Every screen builder takes `mode`: 0 = draw only, 1 = record only,
2 = both. Mode 1 writes `(screen, kind, name, x, y, w, h, label, extra)`
records into the spec arena without meaningful rasterization — this is the
"mental model" the query engine answers from. Mode 2 renders pixels AND
records; the verifier checks the two agree.

## Determinism

Same spec re-renders byte-identically (sha256, 8/8). No RNG anywhere:
procedural art is a seeded hash (`d_hash`) of the song index.

## Files

| file | role |
|------|------|
| `imagination/design/toolkit.zag` | primitives, font import, BMP writer |
| `imagination/design/font.zag` | 5x7 font, 475 packed bytes |
| `imagination/design/screens.zag` | themes, candidates, scorer, components, screens |
| `imagination/design/render.zag` | `render_bin`: `score` / `render <v1\|v2> <screen\|all> <dir>` |
| `imagination/design/mind.zag` | `mind_bin`: spec dump + 24 query answers, no render |
