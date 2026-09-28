# In-head (mental model) test results — 2026-09-22

## Method

1. `mind_bin` builds the design-spec records in **record-only mode** (mode 1):
   no visible screen is allocated or rasterized; answers derive from the
   spec table, never from pixels.
2. It prints the full SPEC dump (55 records: screen, kind, name, x, y, w, h,
   label, extra) and answers 24 preregistered queries.
3. The verifier (`/tmp/verify_design.py`, kept out of the repo) independently
   recomputes every query from the SPEC dump and compares (L1).
4. The verifier then checks SPEC claims against rendered BMP pixels (L2):
   background color, play-triangle interior, accent ring, prev-triangle color,
   album-art non-background, tabbar dot, toggle knob states, navbar title drawn.

## Query set (preregistered in DESIGN-PREREG.md)

Counts, positions, neighbors ("what is left/right of the play button?"),
theme tokens, centering, gaps, slider values, toggle states, label text,
containment totals — 24 queries x 2 versions.

## Results

| level | checks | pass |
|-------|--------|------|
| L1 mind-vs-recompute (v1) | 24 | 24 |
| L1 mind-vs-recompute (v2) | 24 | 24 |
| L2 spec-vs-pixels (v1) | 8 | 8 |
| L2 spec-vs-pixels (v2) | 8 | 8 |
| B-D1 byte-identical rerender | 8 | 8 |
| B-D3 BMP->PNG pixel-identical | 8 | 8 |
| **total** | **80** | **80** |

Mental-model consistency: 48/48 = **100%** (bar: >=90%). PASS.

## V1 in-head score (prereg B-D5)

Scorer output (frozen): WINNER 14, score 314/500.
Theme: bg(10,10,12) surf(26,26,30) acc(245,245,247) txt(245,245,247)
mut(150,152,160), radius 0, spacing 4, shadow off, border off.
Score landscape: the winning family {spacing 4, dark palette, flat}
scores 314; radius is unscored (all radii tie); contrast cap makes
dark-mono and dark-blue tie.

## Honest limitation

The screen builders feed both the record path and the draw path from the
same declarations, so this test proves **internal consistency of an explicit
design model** (spec table vs renderer), not human-like visual consciousness.
TNN "holding the design in its head" = a 55-record table it can query
before any pixel exists. The queries are answered before rendering, and the
render is then checked against the earlier answers — the ordering is real,
the mechanism is a table, and that is reported without mystique.
