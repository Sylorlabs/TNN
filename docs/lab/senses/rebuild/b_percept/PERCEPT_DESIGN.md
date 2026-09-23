# PERCEPT_DESIGN.md — Approach B ("human-style") percept vocabulary

Built 2026-09-21. Pure Zag, zero RNG, deterministic.

## The boundary (load-bearing)

- `transducer.zag` is the ONLY module that touches raw sensory numbers
  (RGB channels, PCM samples, pixel values, frame bytes). It converts
  numbers into opaque percept handles and never passes numbers up.
- `percept.zag` operates ONLY on handles, fixed relation tables, and
  small tuples. It imports nothing, reads no fixtures, and compiles
  standalone (verified: `znc check percept.zag` → "OK — all capability
  claims proven"). A reviewer may delete every numeric line of the
  transducer and `percept.zag` still compiles with its tables intact.
- `sense.zag` is the CLI: loads fixture bytes, calls the transducer,
  asks the percept side for the decision, prints the report.
- Handle decoding (e.g. handle → hue/light/sat fields) is vocabulary
  structure, not raw data: the fields ARE the percept, fixed at compile
  time. No percept-side arithmetic ever touches a channel value.

## Vocabulary (155 handles, all fixed at compile time)

| Domain | Handles | Layout | Count |
|---|---|---|---:|
| Color (chromatic) | 1000–1071 | `1000 + hue*6 + light*2 + sat`; 12 hues × 3 lightness × 2 saturation | 72 |
| Color (achromatic) | 2000–2004 | BLACK, DARK_GRAY, GRAY, LIGHT_GRAY, WHITE | 5 |
| Shape (corners) | 3000–3003 | CORNERS_0, CORNERS_3, CORNERS_4, CORNERS_MANY | 4 |
| Shape (curvature) | 3100–3102 | CURVED, STRAIGHT, MIXED | 3 |
| Shape (symmetry) | 3200–3203 | SYM_FULL, SYM_4, SYM_3, SYM_NONE | 4 |
| Pitch | 4000–4047 | 48 ordered semitone bins, 12-TET from 110 Hz | 48 |
| Timbre | 5000–5003 | PURE, BRIGHT, DARK, RICH | 4 |
| Timbre evidence | 5100–5102 | EV_WEAK, EV_MEDIUM, EV_STRONG | 3 |
| Motion direction | 6000–6008 | STILL, N, NE, E, SE, S, SW, W, NW | 9 |
| Motion speed | 6100–6102 | SPD_SLOW, SPD_MEDIUM, SPD_FAST | 3 |
| **Total** | | | **155** |

Hue wheel (fixed order): 0 RED, 1 RED_ORANGE, 2 ORANGE, 3 AMBER,
4 YELLOW, 5 YELLOW_GREEN, 6 GREEN, 7 TEAL, 8 CYAN, 9 SKY, 10 BLUE,
11 VIOLET. Lightness: 0 DARK, 1 MID, 2 LIGHT. Saturation: 0 MUTED,
1 SATURATED.

Pitch bins: `edge[b] = round(110 * 2^((b − 0.5)/12))` Hz, b = 0..48
(107 Hz … 1710 Hz edges; bin centers 110 Hz … ~1650 Hz in exact
semitone steps). The bin ORDER is the relation: a higher handle IS a
higher pitch, by vocabulary definition.

## Fixed relation structures (the only things percept.zag may use)

- **Color**: hue-wheel cyclic adjacency (12-wheel, short-way distance);
  lightness rank order (DARK < MID < LIGHT, shared with achromatic
  ranks); saturation order. `pc_color_dist` = wheel steps + lightness
  steps + saturation steps (chromatic pair); axis steps (achromatic
  pair); 4 + lightness mismatch (mixed pair, far by construction).
- **Shape**: prototype table over the 3-tuple —
  CIRCLE = (CORNERS_0, CURVED, SYM_FULL),
  TRIANGLE = (CORNERS_3, STRAIGHT, SYM_3),
  SQUARE = (CORNERS_4, STRAIGHT, SYM_4).
  Decision = argmax of per-axis matches (eliminative vote).
- **Pitch**: total order on the 48 bins. `pc_pitch_cmp(a,b)` ∈
  {−1, 0, 1} from handle order alone.
- **Timbre**: 4 nominal quality classes; evidence handles ordered
  WEAK < MEDIUM < STRONG.
- **Motion**: 8-wind compass adjacency for directions; speed order
  SLOW < MEDIUM < FAST; STILL is its own direction.

## Confidence rules (percept-level evidence only)

No confidence input is a raw number; every rule reads handles,
distances on the fixed tables, or the evidence handle.

| Task | Rule |
|---|---|
| colordisc | color distance 0 → 950; 1 → 700; 2 → 750; 3 → 850; ≥4 → 950 |
| colorconst | same table as colordisc |
| shapetrans | 3/3 tuple axes match prototype → 950; 2/3 → 700; else 400 |
| pitchdisc | bin distance 0 → 950; 1 → 600; 2 → 750; ≥3 → 900 |
| timbredisc | EV_STRONG → 950; EV_MEDIUM → 750; EV_WEAK → 500 |
| motiondir | STILL → 900; SPD_FAST → 950; SPD_MEDIUM → 800; else 650 |

Rationale for the non-monotonic color/pitch tables: confidence is in
the JUDGMENT, not the distance. Distance 0 = confident SAME (950);
distance 1 = near the same/different boundary = least certain (600–700);
large distance = confident DIFFERENT (900–950).

## Transducer mechanisms (numbers → handles; nothing else)

- **Color**: average patch RGB → max/min chroma analysis → fixed
  qualitative handle (hue bin from dominant-channel sector,
  lightness from max channel, saturation from chroma ratio).
- **Color constancy**: von Kries-style white-point adaptation. The
  fixture half's BORDER is the neutral illuminant reference; the
  center inset is the surface. Border mean estimates the illuminant,
  the surface mean is rescaled by it, THEN the percept forms. The
  vocabulary never moves — adaptation is retinal, not conceptual.
- **Shape**: background mask (luminance threshold), centroid, 36-ray
  radial profile marched from the centroid, corner prominence from
  profile curvature, rotational self-match (shifts 9/12/18 of 36) →
  (corners, curvature, symmetry) tuple. Rotation-invariant by
  construction (profile is cyclic).
- **Pitch**: autocorrelation over lags 31..630 (70–1400 Hz at
  44.1 kHz), first prominent local maximum (≥50% of global max) as
  the period → fixed semitone-bin edge table → ordered handle.
- **Timbre**: transducer-only f0-normalized features —
  brightness (per-mille energy of the f0-normalized difference
  signal), crest (per-mille peak/RMS), form factor (per-mille
  peak/mean|s|). Thresholds calibrated on 440 Hz canonical tones:
  sine≈(9, 1414, 1571), sawtooth≈(300, 1732, 2000),
  triangle≈(12, 1732, 2000), square≈(200, 1000, 1000).
  Decision: crest ≤ 1150 → RICH; brightness ≥ 60 → BRIGHT;
  form factor ≥ 1780 → DARK; else PURE. Evidence handle from the
  numeric margin to the nearest threshold (transducer-side), seen
  by the percept side only as WEAK/MEDIUM/STRONG.
- **Motion**: frame-0 difference → motion-pixel count vs still
  threshold → motion centroids per frame → displacement vector →
  compass octant + speed category (displacement per frame).

## Fixture-pair conventions (assumed; not fully pinned in INTERFACE.md)

| Task | Convention used |
|---|---|
| colordisc | left half vs right half of one image |
| colorconst | left/right halves; each half's border = neutral illuminant reference, inset center = surface |
| pitchdisc | first half vs second half of the PCM stream |
| shapetrans | one shape per image |
| timbredisc | one tone per PCM |
| motiondir | one clip per video |

Fixture container formats (as implemented): image = u32 w, u32 h,
then w*h RGB triplets; PCM = u32 sample-rate, u32 count, then
count i16-LE samples; video = u32 frame-count, u32 w, u32 h, then
nf*w*h RGB triplets.

## Design bets (documented, honest)

1. Color same/different threshold at distance ≤ 1 (identical, or one
   step on one vocabulary axis). Affects near-boundary pairs only.
2. Timbre thresholds calibrated on four canonical syntheses
   (sine/sawtooth/triangle/square at 440 Hz). Real-harness tones with
   different harmonic recipes may shift the brightness/crest/form
   values; the decision ORDER (crest → brightness → form factor) is
   chosen so the most distinctive cue fires first.
3. Pitch bins are exact semitones; pairs closer than ~1 semitone may
   fall in one bin (SAME) or straddle (distance 1, conf 600).
4. Shape symmetry uses exact rotational self-match tolerances; an
   imperfect triangle yields SYM_NONE but still classifies by
   corners+curvature (2/3 vote, conf 700) — the tuple degrades
   gracefully rather than failing.
5. Motion STILL threshold (200 changed pixels/frame) and speed
   bands (≤1.5 SLOW, ≤4 MEDIUM px/frame) are tuned to the 64×64
   5×5-dot smoke clips.
