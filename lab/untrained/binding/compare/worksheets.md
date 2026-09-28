# Claim worksheets — BINDING confirmatory run (2026-09-26)
Human descriptions sealed 2026-09-26 20:32:37 UTC (human/SEAL.log), BEFORE any analyzer run.
TNN outputs: `out/T-C*_r1.txt` (r2 byte-identical for all six).
Analyzer: repaired uanalyze (source SHA bca26720..., binary SHA 53caf899...; rebuild reproduces binary SHA byte-exactly).

Scoring: MATCH / MISS / WEAK MISS / PARTIAL / HALLUCINATION.
A hallucination is a FALSE POSITIVE: TNN asserts structure that is not there.
False positives fail the bar; withholding does not (withheld genuine structure
is noted, not penalized — the honest boundary).

---

## C1 — Dyad swells (H-C1 vs T-C1)

| # | TNN claim | Human | Score |
|---|-----------|-------|-------|
| 1 | DURATION ~12 s | 12.0 s | MATCH |
| 2 | DYNAMICS large swings; "loud events rise far above a quiet bed" | ~10 dB smooth swells; continuous tone, NO quiet bed (troughs 0.085 RMS) | PARTIAL |
| 3 | PITCH tonal ~164.900 Hz sustained | Dyad 330+495 Hz; 165 Hz is the common subharmonic (missing fundamental — the perceived pitch) | PARTIAL |
| 4 | ONSETS no clear repeating transient events | No discrete transients | MATCH |
| 5 | SPECTRUM energy concentrated below ~400 Hz | 52% <400 Hz / 48% 400-2000 Hz; nothing above 2 kHz | PARTIAL |
| 6 | RHYTHM no slow amplitude cycle detected | The ONLY periodicity is the 4 s slow swell (3 swells) | MISS |
| 7 | LAYERS a single tonal process, no separable transient layer | Single AM tonal process | MATCH |

C1: 4 MATCH / 1 MISS / 2 PARTIAL / 0 HALLUCINATION.
- #2: the 9.75 dB swell is real, but "large" overstates it and no quiet bed exists.
- #3: the 165 Hz periodicity is physically in the waveform (autocorr strength
  1.000) and is the perceived missing-fundamental pitch — not invented — but
  the single-component wording misses the true 330+495 dyad structure.
- #5: low-frequency emphasis is real (band_low 0.585) but "concentrated"
  overstates a 58/42 split.
- #6 MISS mechanism: slow-swell detector requires >=3 detected swells
  (uanalyze.zag:1140); C1 has exactly 3 true swells but only 2 detected
  (partial first/last swells lost at clip edges), so it withheld. Honest
  false negative at the sensitivity edge — the B1 (12 swells) and B2
  (5 swells) cases still pass.

---

## C2 — Soft phrases (H-C2 vs T-C2)

| # | TNN claim | Human | Score |
|---|-----------|-------|-------|
| 1 | DURATION ~10 s | 10.0 s | MATCH |
| 2 | DYNAMICS large swings; quiet bed | Digital silence vs phrase bodies (~0.26 RMS) | MATCH |
| 3 | PITCH tonal in active regions, median ~842.1 Hz, span 800-888.8 Hz; quiet gaps | 880->840 Hz glides + harmonics; strongly tonal in phrases, silence between | MATCH |
| 4 | ONSETS no discrete transients; 4 gradual swell onsets | 4 phrases, 80 ms raised-cosine attacks, no sharp transients | MATCH |
| 5 | ONSETS irregular intervals | Gaps 1.2 / 2.0 / 1.4 s, irregular | MATCH |
| 6 | SPECTRUM mid (400 Hz-2 kHz) | 97% of energy 400-2000 Hz | MATCH |
| 7 | RHYTHM no slow amplitude cycle detected | No periodic rhythm | MATCH |
| 8 | LAYERS single AM process; no separable transient layer | Single tonal process; bed is silence | MATCH |

C2: 8 MATCH / 0 / 0 / 0. Clean pass: onset taxonomy correctly called the
80 ms attacks non-transient, active-region pitch recovered the glide,
irregularity reported, silence correctly not called a noise bed.

---

## C3 — Rumble + hum (H-C3 vs T-C3)

| # | TNN claim | Human | Score |
|---|-----------|-------|-------|
| 1 | DURATION ~15 s | 15.0 s | MATCH |
| 2 | DYNAMICS moderate variation | ~8 dB envelope depth from beating | MATCH |
| 3 | PITCH none; inharmonic/noise-like (withheld) | 250 Hz harmonic stack clearly present (strongest spectral peak) + inharmonic rumble | MISS |
| 4 | ONSETS no discrete transients; gradual fluctuations | Continuous; no discrete events | MATCH |
| 5 | SPECTRUM energy concentrated below ~400 Hz | 89% below 400 Hz | MATCH |
| 6 | SPECTRUM few tonal below ~4 kHz: noise-like, no stacked harmonics | 250/500/750 Hz stacked harmonics present | MISS |
| 7 | RHYTHM amplitude repeats on ~0.860 s cycle | Real ~9.3 Hz inter-partial beating (roughness); 0.860 s = its exact 8th subharmonic (9.3/8 = 1.1625 Hz) | PARTIAL |
| 8 | LAYERS single AM process; no separable transient layer | One continuous mixed process | MATCH |

C3: 5 MATCH / 2 MISS / 1 PARTIAL / 0 HALLUCINATION.
- #3/#6 MISS mechanism: the pitch detector MEASURED f0 = 250.0 Hz
  (f0_med_dhz 2500) but the voicing-strength gate (0.495) vetoed it because
  the inharmonic rumble bed dilutes harmonicity — a genuine sensitivity gap
  when a strong inharmonic bed accompanies a real tone. False negative, not
  invention. Named follow-up for the repair line.
- #7: the 0.860 s cycle is a mathematically exact subharmonic of the genuine
  9.3 Hz beating (59% of 20 ms-envelope modulation energy at 8.5-10.1 Hz) —
  real periodic structure, wrong octave. Same class as B3's PARTIAL, NOT the
  M1 lag-2 artifact (which would be 0.040-0.100 s; the M1 gate held).

---

## C4 — Pickets (H-C4 vs T-C4)

| # | TNN claim | Human | Score |
|---|-----------|-------|-------|
| 1 | TONE mid-tone overall | Mean brightness 94 (mid-dark gray) | MATCH |
| 2 | TONE high contrast light/dark | Bars 220 vs ground 40 | MATCH |
| 3 | COLOR muted, near-monochrome | Pure grayscale, zero saturation | MATCH |
| 4 | REGIONS 1; largest 100% | Two tones in strict alternation; grain shatters naive flood fill | WEAK MISS |
| 5 | EDGES dense edge structure | 16 full-height bar boundaries + grain | MATCH |
| 6 | EDGES run mostly vertical | Vertical bar boundaries dominant | MATCH |
| 7 | TEXTURE fine-grained across most of frame | Speckle on every pixel; native 8x8 frac 1.000 | MATCH |
| 8 | LAYOUT left/right differ strongly (asymmetric) | Halves identical in content (93.9 vs 94.1); the 40 px bar period does NOT mirror (slr 0.447 is a real mirror difference) | MATCH* |
| 9 | LAYOUT top-bottom mirror symmetric | Stripes run full height; thirds identical | MATCH |
| 10 | LAYOUT mass centered h/v | Centroid 0.470/0.493 | MATCH |

C4: 9 MATCH / 1 WEAK MISS / 0 HALLUCINATION.
- #4: region-count vocabulary mismatch on heavy grain (c2 precedent: WEAK).
- #8*: the slr metric measures MIRROR asymmetry; 0.447 is a large, genuine
  measurement (the bar period genuinely doesn't mirror). True under the
  metric's mirror-semantics; the wording risks misreading as content
  difference, which is absent. Not invented structure — noted as a wording
  caveat, not a hallucination.

---

## C5 — Diagonal wedge (H-C5 vs T-C5)

| # | TNN claim | Human | Score |
|---|-----------|-------|-------|
| 1 | TONE mid-tone overall | Mean ~104 | MATCH |
| 2 | TONE high contrast light/dark | 200 vs 30 halves | MATCH |
| 3 | COLOR muted, near-monochrome | Slight warm tint, muted | MATCH |
| 4 | REGIONS 3; largest ~43% | 2 large halves + boundary band (0.49/0.48/0.03) | MATCH |
| 5 | EDGES run mostly diagonal | Single ~40 deg diagonal boundary dominant (median edge dir 135 deg) | MATCH |
| 6 | TEXTURE mostly smooth, little fine detail | No grain; native frac 0.077 | MATCH |
| 7 | LAYOUT left/right differ strongly | Left 153 vs right 56 | MATCH |
| 8 | LAYOUT top/bottom differ strongly | Top 138 vs bottom 71 | MATCH |
| 9 | LAYOUT mass toward left, vertically centered | Bright mass top-left; centroid 0.348/0.414 | MATCH |

C5: 9 MATCH / 0 / 0 / 0. Clean pass: the T2 component-orientation repair
correctly reports "mostly diagonal" on a novel diagonal (boundary-band
median edge direction 135 deg); native-resolution texture correctly reports
smooth (the T1 repair holds).

---

## C6 — Drift (H-C6 vs T-C6)

| # | TNN claim | Human | Score |
|---|-----------|-------|-------|
| 1 | DURATION 8 frames at 2 fps | 8 frames (2 fps is the analyzer's stated default) | MATCH |
| 2 | MOTION consistent, ~6.578 px/frame at 80x45, right-down diagonal | Centroid-tracked +12/+9 px/frame at 160x90 (= +6/+4.5 at 80x45), constant | MATCH |
| 3 | CUTS none; one continuous shot | Frame diffs stable across all 7 pairs | MATCH |
| 4 | BRIGHTNESS darkens over time | Frame means 171 -> 149 | MATCH |
| 5 | COVERAGE moving areas concentrate on the left side | Square traverses full width; aggregate motion left-heavy (5/8 frames left of center; frame 8 clipped) | WEAK MISS |

C6: 4 MATCH / 1 WEAK MISS / 0 HALLUCINATION.
- #2: magnitude ~12% low (6.58 vs true 7.5 px/frame at 80x45 — frame-8
  clipping + global dimming); direction and consistency correct.
- #5: the left-concentration is an aggregate-trajectory artifact (c2 B6
  precedent: WEAK); the motion genuinely is left-heavy in aggregate but a
  viewer would describe the full traversal.

---

## Totals

| Input | MATCH | MISS | WEAK MISS | PARTIAL | HALLUCINATION |
|---|---|---|---|---|---|
| C1 dyad | 4 | 1 | 0 | 2 | 0 |
| C2 phrases | 8 | 0 | 0 | 0 | 0 |
| C3 rumble | 5 | 2 | 0 | 1 | 0 |
| C4 pickets | 9 | 0 | 1 | 0 | 0 |
| C5 wedge | 9 | 0 | 0 | 0 | 0 |
| C6 drift | 4 | 0 | 1 | 0 | 0 |
| **TOTAL** | **39** | **3** | **2** | **3** | **0** |

**HALLUCINATIONS: 0.**
