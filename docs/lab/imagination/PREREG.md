# IMAGINATION-DESIGN TRIAL — Preregistration (frozen 2026-09-22)

**Order:** Micah 2026-09-21 — "humans we can imagine things like audio images
video all in our heads and visualize stuecture everything in our head TNN
should be able to as well now the bridge is whether a machine way of doing
that or human way is better thats what needs to be tested."
**Test medium:** imagination, not code output and not external rendering.
**Status:** FROZEN. Any change to questions, batteries, bars, metrics, or the
taste functions needs a dated amendment.
**Commit rule:** this file is committed alone before any build or scored run.

## The question

Can TNN hold a sensory scene "in its head" — a visual layout, a sound, a
structure — as an internal representation it can consult and manipulate
without rendering it? And when it designs from imagination, is the
MACHINE way (raw values: RGB triples, coordinates, Hz, ms) or the HUMAN way
(qualitative percepts: warm red, balanced, airy, rising, tense) better —
judged by (a) imagination fidelity, (b) design quality under brief, and
(c) agreement with documented human design preferences?

## Q0 — BASELINE AUDIT (pre-build): does any imagination mechanism exist?

Source audit of the repo for: a scene buffer, an offline simulation
partition, any construct-then-query sensory representation, any
"imagine/visualize in head" construct. Expected result: NONE — the
b_percept machinery classifies LIVE transducer input only (fixtures in,
handles out); nothing holds a scene offline. Document the finding with
file/line evidence. No numeric bar; the audit establishes "not done, so we
build it" per Micah's order ("if not done then it needs to be").

## The mechanism to be built: `imagine.zag` (pure Zag, zero RNG)

An IMAGINATION PARTITION: a deliberately-managed arena holding a SCENE of up
to 32 ELEMENTS. Each element has a domain (VISUAL / AUDIO / STRUCT), a kind,
and 8 attribute slots. The MODE decides which slots are populated and which
query ops are legal:

| Domain | MACHINE-WAY attrs (raw values) | HUMAN-WAY attrs (percept handles) |
|---|---|---|
| VISUAL | kind∈{rect,circle,triangle,text}; x,y,w,h in 0..1000; r,g,b in 0..255 | kind; zone∈{0..8} (3×3: TL,TC,TR,ML,C,MR,BL,BC,BR); color handle from the 155-vocab (1000–1071 chromatic, 2000–2004 achromatic); shape tuple (corners 3000–3003, curvature 3100–3102, symmetry 3200–3203) |
| AUDIO | freq_hz (i32), dur_ms, amp 0..1000 | pitch-bin handle 4000–4047 (bin = round(12·log2(f/110)), clamped); timbre handle 5000–5003 |
| STRUCT | x,y,z in cm 0..1000; size 1..500 | zone 0..8; rel∈{NONE,LEFT_OF,RIGHT_OF,ABOVE,BELOW,STACKED_ON,NEAR} + rel_target element index |

Ops (both modes, answered ONLY from the partition — the brief text is
discarded after construction): `place`, `query_attr`, `query_zone`,
`query_relation(a,b)`, `query_warmest`, `query_harmony(a,b)`,
`query_balance`, `query_contour` (audio), `query_tension(a,b)` (audio),
`query_support` (struct), `edit` (move / re-attribute / re-relate),
`describe` (emit the design spec), `clear`.

Fixed relation tables (frozen; human-way never touches a raw number):
- Warmth: hue-wheel sector table — hues 0–4 WARM, 5–7 NEUTRAL, 8–11 COOL
  (hue order per b_percept PERCEPT_DESIGN.md); achromatic → NEUTRAL.
- Harmony: `pc_color_dist` from PERCEPT_DESIGN.md (wheel steps + lightness
  steps + saturation steps; achromatic/mixed rules as specified there).
- Pitch order: handle order IS pitch order (`pc_pitch_cmp`), per b_percept.
- Zones: 3×3 grid; mirror pairs (TL↔TR, ML↔MR, BL↔BR; TC/BC/C self).

### The two "tastes" (frozen design-quality functions, 0..1000 each)

These are the operationalized aesthetics under test. They were written
BEFORE any Q3 outcome was seen and are frozen here. The comparison is
encoding-style, not survey-grade measurement: machine encodings of real
designs are approximate values from reference descriptions (±tolerance);
human encodings are the same facts as percept handles.

**MACHINE taste (visual):** ALIGNMENT 0..400 = 400 × (coords divisible by
50)/ (2·n_coords); SYMMETRY 0..300 = 300 × mirror-matched/n, mirror =
(1000−x, y) same kind, |Δrgb|≤30/channel, |Δw|,|Δh|≤40; CONTRAST 0..300 =
300 × (maxL−minL)/765, L=(r+g+b)/3, n≥2 else 0.
**HUMAN taste (visual):** HARMONY 0..400 = mean over pairs of
max(0, 400−50·pc_color_dist); BALANCE 0..300 = 300 × (elements whose mirror
zone holds a same-color-handle element)/n (n=1 in TC/BC/C → 300);
SIMPLICITY 0..300 = 300 × max(0, 1−(n−1)/8).
**MACHINE taste (audio):** CONSONANCE 0..500 = 500 × pairs with freq ratio
within 1.5% of {2:1, 3:2, 4:3, 5:4} / total pairs; REGULARITY 0..500 =
500 if all dur_ms equal, 250 if within 10%, else 0.
**HUMAN taste (audio):** CONTOUR 0..500 = 500 rising (each bin ≥ prev, last
> first), 350 arch (rises then falls), 200 flat, 100 falling, 0 jagged;
STABILITY 0..500 = max(0, 500 − 60 × max adjacent bin distance).
**MACHINE taste (struct):** GROUNDING 0..500 = 500 × (z==0)/n; GRID 0..500
= 500 × (y divisible by 100)/(n).
**HUMAN taste (struct):** SUPPORT 0..500 = 500 if every STACKED_ON has a
target with BELOW/STACKED support chain to z-ground, else proportional;
SPREAD 0..500 = 500 × distinct_zones/n.

Generation = deterministic lexicographic candidate enumeration (fixed
order, NO randomness), keep max taste score, ties → lowest index. Brief
constraints are hard filters. This is deliberate selection among
alternatives by a quality criterion — the honest v1 of "designing."

## Q1 — IMAGINATION PROBE (built mechanism, both modes)

12 NOVEL construction procedures (4 visual, 4 audio, 4 structural; authored
for this trial, never in any training data). Each: build scene → 2 questions
about EMERGENT properties (not stated in the procedure text) → EDIT the
scene → 1 question about the post-edit state. 36 questions per mode.
Questions require consulting the partition (spatial relations, warmest
color, largest interval, what supports what, zone occupancy after a move).

| Bar | Rule |
|---|---|
| IMAG-1 | ≥ 26/36 per mode → the imagination mechanism works in that mode; < 26/36 → FAIL for that mode |

Memorization guard: all scenes novel; emergent-property questions are
unanswerable from the procedure text alone (verified by a text-only control:
the procedure text without the partition must score < 12/36).

## Q2 — DESIGN GENERATION (6 briefs × 2 modes = 12 designs)

Briefs (fictional, novel): V1 logo for bakery "Crumb & Craft" (grain motif,
warm palette, ≤4 elements, legible small); V2 poster for a jazz night (night
feel, text zones for date/venue, cool palette + one warm accent); A1
4-note shop-door chime (welcoming = rising contour, ends stable); A2 3-note
kiosk error buzz (attention-getting, tense intervals); S1 five blocks on a
shelf (largest at bottom, no overhang, all front-visible); S2 four stones in
a garden square (asymmetric balance, one dominant stone, airy = ≥3 empty
zones of 9).

| Bar | Rule |
|---|---|
| GEN-1 brief compliance | ≥ 10/12 designs satisfy ALL brief constraints (mechanical check of emitted spec) else FAIL |
| GEN-2 mode fidelity | 12/12 specs use only their mode's vocabulary else FAIL |
| GEN-3 internal consistency | ≥ 20/24 probe questions on the generated designs (2 each, asked of the partition) match the emitted spec else FAIL |

Novelty: each design's signature (palette-handle set + layout-zone set, or
contour + interval set) checked against the 8 Q3 famous designs; report only.
Quality ranking: SEE Q4 (human rater required — flagged).

## Q3 — HUMAN-AGREEMENT (8 documented preference pairs × 2 modes)

Each pair: two real designs, one documented human preference. Both designs
are encoded by the crew in EACH mode from factual references (same facts,
different encoding), imagined by the TNN, scored by the mode's taste; the
TNN predicts humans preferred the higher-scoring design. Ties → the
first-listed design, recorded as ties.

| # | Pair | Human preference (documented) | Evidence tier | Source |
|---|---|---|---|---|
| 1 | Gap logo: 2010 redesign vs classic blue box | CLASSIC (old) | STRONG (6-day revert after backlash) | BBC/Branding Journal via press; 2000+ protest comments, parody acct 5000+ followers |
| 2 | Tropicana packaging 2009 vs straw-in-orange | ORIGINAL (old) | STRONG (−20% sales, reverted ~46 days) | SEC filings via Medill; $35M campaign scrapped |
| 3 | New Coke 1985 vs Coca-Cola Classic | CLASSIC (old) | STRONG (79 days, 8,000 calls/day, 40,000 letters, reverted 1985-07-11) | HISTORY.com; Coca-Cola Company |
| 4 | UC 2012 monogram vs century-old seal | SEAL (old) | STRONG (50,000+ petition, use suspended Dec 2012) | Higher Ed Dive; UC statement |
| 5 | Cracker Barrel 2025 rebrand vs old-timer logo | ORIGINAL (old) | STRONG (backlash, market-value drop, reverted within days Aug 2025) | press reports |
| 6 | Starbucks 2011 (wordless siren) vs 1992 logo | NEW | MODERATE (documented positive reception, still in use 15 yrs) | design press consensus |
| 7 | Mastercard 2016 (flat interlocking circles) vs old | NEW | MODERATE (award-winning, cited as model rebrand) | design press consensus |
| 8 | Apple 1998 monochrome vs rainbow | NEW (mono) | MODERATE (critical consensus: mono among greatest marks ever) | design press consensus |

| Bar | Rule |
|---|---|
| AGREE-1 design sense | higher-scoring mode ≥ 7/8 → "TNN design sense works"; 6/8 → MARGINAL; ≤ 5/8 → FAIL |
| AGREE-2 mode superiority | \|machine − human\| ≥ 3 pairs → the leading mode wins for design; else NO-DIFFERENTIATION |

Report per-tier (STRONG 5 / MODERATE 3) as secondary. Chance = 0.50/pair;
7/8 has one-sided p ≈ 0.035.

Circularity guard: taste functions frozen in this prereg before Q3
encodings were authored; encodings are faithful facts in two codecs, not
tuned to outcomes. The TNN learner has no training data about any of these
brands/events — nothing to memorize.

## Q4 — HUMAN QUALITY RATING (protocol frozen; EXECUTION NEEDS A RATER)

The 12 Q2 designs, blinded and order-randomized (deterministic shuffle with
a FIXED seed — the shuffle is presentation order, not a decision path),
rated 1–10 "how good is this design" by a human judge. **Micah: this is the
one place the trial needs you as a rater — or say the word and we run it
with an outside panel instead.** Until rated, Q4 stays PENDING.

## Determinism

Zero RNG in any decision path (the Q4 presentation shuffle uses a fixed
constant seed and is not part of any decision). Q1–Q3: 5 reps byte-identical
(SHA256 of full logs). Independent `verify_imag.py` recomputes all metrics
from logs.

## Deliverables

`imagination/`: PREREG.md (this file), src/imagine.zag, batteries/
(q1_scenes.txt, q2_briefs.txt, q3_pairs.txt — both codecs), driver.py,
AUDIT-Q0.md, VERDICT.md, SHA256SUMS, run logs, verify_imag.py. Night-run
log updated. Final report: Q0–Q4 answers with numbers, mode verdict, what
the imagination mechanism IS representationally (representations, not
vibes), and the explicit rater request if Q4 is still pending.
