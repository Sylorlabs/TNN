# RENDER-NOTES — GALLERY crew interpretation layer

Date: 2026-09-21. Renderer: `render_gallery.py` (this dir).
Sources: `../logs/q2m.txt`, `../logs/q2h.txt` (parsed at runtime — the PNGs
reflect the frozen dumps, not a transcription); `../src/imagine.zag` lines
1373–1410 for the Q1 builders (transcribed by hand, verified against the code
below); `../Q4-PACKET.md` for brief texts and design descriptions.

Principle: the scene files hold values/handles, never pixels. Every choice
below is the gallery layer's mapping — no scene datum was altered, rescaled,
or "improved". Where the spec forced an arbitrary choice, it is marked
[GALLERY CHOICE].

## Files produced

16 PNGs in `~/workspace/your_files/imagination_gallery/` + `index.html`:
- `brief<N>_<machine|human>_<letter>.png` — 12 Q2 designs. Letter→(mode,brief)
  mapping from the Q4-PACKET.md footer: A=(m,3) B=(h,3) C=(m,4) D=(h,4) E=(h,1)
  F=(h,2) G=(m,5) H=(m,1) I=(m,2) J=(m,6) K=(h,5) L=(m,6).
- `q1_s<1|2>_<machine|human>.png` — 4 Q1 visual scenes.

## Visual domain

- Canvas 1000×1000, white background.
- MACHINE: x, y are the shape CENTER; draw w×h directly with RGB as given.
  - kind 1 rect: centered rect. kind 2 circle: centered ellipse w×h.
    kind 3 triangle: apex-up, vertices (x, y−h/2), (x±w/2, y+h/2).
    kind 4 text panel: rect + centered "TEXT" label [GALLERY CHOICE: the label
    is a gallery affordance; the scene holds no glyphs].
  - Elements drawn in scene (element-index) order; later elements occlude
    earlier ones. Real consequence: machine brief 2 draws its rectangle over
    its circle and its dark text panel over its warm text panel — exactly as
    the scene orders them.
- HUMAN: draw the kind's shape at the zone center, 120×120 (text panels
  200×60 + "TEXT" label). Shape tuples (corners 3000–3003, curvature
  3100–3102, symmetry 3200–3203) are NOT turned into geometry here — they are
  qualitative labels in the scene (e.g. 3002 = "very angular"); deforming the
  drawn shape from them would invent geometry the scene does not contain.
- Color handles: `1000 + hue×6 + light×2 + sat` per the task's frozen table
  (verified against `b_percept/PERCEPT_DESIGN.md` formula + hue wheel order).
  DARK ×0.55, LIGHT → toward white 40%, MUTED → desaturate 50% toward gray;
  achromatic 2000–2004 per the fixed table.
  Decodes used: 1003→(110,22,22) RED DARK SAT; 1015→(220,130,30) ORANGE MID;
  1023→(234,204,126) AMBER LIGHT; 1027→(210,200,50) YELLOW MID;
  1059→(150,180,228) SKY LIGHT; 2003→(200,200,200) LIGHT_GRAY;
  2004→(245,245,245) WHITE.
  **Mismatch recorded:** Q4-PACKET prose calls 2003 "neutral-gray-blue" and
  1027 "warm-amber"; the frozen handle table says LIGHT_GRAY and YELLOW-MID.
  Render follows the frozen table; the scene holds only the handles.

## Audio domain

- PNG 800×200, per-pixel sampled polyline, zero line, segment boundaries,
  per-note freq labels (rounded Hz).
- MACHINE: freq_hz and dur_ms direct; amplitude = amp/1000 (0.8 in all cases).
- HUMAN: freq = 110 × 2^(bin/12) — matches the builder's own bin↔freq tables
  in imagine.zag (`ig_a_pbin`/`ig_a_pfreq`: bin 15→262 Hz, 26→494, 27→523).
  Timbre: 5000 PURE→sine, 5001 BRIGHT→sine+0.4·2nd harmonic,
  5002 DARK→soft triangle (0.8·2/π·asin(sin)), 5003 RICH→saw-ish (4
  harmonics, 1/n). All human audio elements in this trial are PURE.
- [GALLERY CHOICE] Human scenes carry NO duration and NO amplitude.
  Each human note is rendered at the same brief's machine design per-note
  duration (brief 3: 250 ms, brief 4: 150 ms) and amplitude 0.8. This keeps
  the side-by-side comparison temporal-aligned; it is documented, not data.

## Struct domain

- MACHINE block (kind 1, side view): width=size, height=size×0.6, centered at
  x, bottom edge at `canvas_bottom − z − height` — the task's literal formula.
  The a2 shelf-line value (850) is ignored per spec. CONSEQUENCE: the machine
  blocks float (each bottom edge sits its own height above the canvas bottom).
  This looks odd but is the faithful render of the given formula.
- MACHINE stone (kind 2, top view): circle at (x,y), diameter=size.
- HUMAN block: zone-center position, width=rank×45, height=rank×27.
  rel=NONE → bottom edge at canvas bottom (1000). rel=STACKED_ON → bottom
  edge flush on the target block's top edge, centered on the target
  (targets resolved recursively). Only rel codes 0 and 5 occur in the data.
- HUMAN stone: circle at zone center, diameter=rank×50 (parallel to the
  machine builder's `size = rank×50` at imagine.zag:1284–1287).
- [GALLERY CHOICE] Struct elements carry no color in either mode.
  Blocks render wood-tan (178,142,96), stones gray (155,155,155), dark
  outlines. Pure gallery defaults.

## Q1 scenes

No Q1 scene-dump log exists; the scenes were transcribed from
`ig_q1_sc1` / `ig_q1_sc2` (imagine.zag:1373–1410) into `q1_scene()` in the
renderer, transcribed value-by-value and checked against the source above.

Rendered in the AS-IMAGINED initial state. The Q1 battery itself mutates one
attribute mid-run before its final question (imagine.zag:1387, 1408):
- scene 1: element 2's a1 — machine text x 832→166; human text zone 8→6.
- scene 2: element 1's a1 — machine circle x 166→832; human circle zone 0→2.
Those mutations are test-protocol manipulations, not part of the imagined
scene, so the PNGs show the pre-mutation construction.

## Verification

- All 16 renders visually inspected against the packet descriptions and the
  raw log lines; zone placements, colors, frequencies, block stacks, stone
  positions all match the source data.
- Genuine design differences visible in the gallery (not artifacts):
  human brief-6 dominant stone sits middle-left vs machine's middle-right;
  human brief-3 "low" notes are at 494 Hz vs the machine's 262 Hz.
- Reproducible: `python3 render_gallery.py <out_dir>` regenerates all 16 PNGs
  deterministically (no randomness anywhere in the renderer).
