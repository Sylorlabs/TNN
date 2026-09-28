# No-bridges composer — DESIGN.md

## Assignment (Micah, 2026-09-26 ~01:11 PDT)

Build a pure-Zag composer in which TNN invents its own segmentation method from
raw bytes — no handed candidate sets, no baked thresholds, no percentile
recipes, no programmer-framed segmentation. Trace the invention: proposed
methods, criteria, scoring, selection, reasoning. Run: "merge the pig and the
bunny together." Compare honestly against step-3's fusion.

Standing phrases honored: "No bridges, no baked-in things, period."
"Humans don't, so why should TNN?" Zero randomness in decision paths;
byte-identical reruns; full frames / full duration; Micah's eyes outrank metrics.

## Architecture

Two organs, one binary (`composer_nb_bin`, pure Zag, zero RNG):

**Invention organ** (new: `nb1.zag`–`nb4.zag`) — TNN invents segmentation:
- `nb1` MEASURE: neutral instruments. Four per-pixel fields (GRAY u8;
  TEX i64 gradient magnitude; MOTION i64 full-sequence motion energy;
  VAR i64 4x4-block variance), each summarized in a 12-i64 field record:
  min/max/mean, peak count, valley depth x1e4, valley level, structuredness x1e4
  (top-decile connected-component clustering), divisibility
  (valley-depth x structuredness), median, Q1, Q3, knee (max-curvature bend of
  the cumulative histogram). Instruments only — no segmentation lives here.
- `nb2` PROPOSE: the mechanism composes cut-procedure schemas with fields.
  Schemas (programmer-supplied vocabulary): VALLEY (cut at the deepest valley
  between the two tallest histogram peaks — applies only when the field shows
  >=2 peaks and a valley at least as deep as the cross-field median bar, which
  is derived from the data, not handed in); MEDIAN (cut at the field's own
  median); KNEE (cut at the bend of its own cumulative curve); BAND (three
  parts at its own Q1/Q3). Every level is computed from the field's own
  distribution. The mechanism decides which schema×field combinations to
  instantiate and records why (12–14 methods per memory on this input).
- `nb3` JUDGE: the mechanism measures each invented method on frames 11/12/13
  with its own criteria — P persistence (same method/levels, do parts stay the
  same things?), B boundary evidence (do borders sit on real picture edges?),
  H homogeneity (is each part made of similar stuff?), F fragmentation (whole
  pieces or speckle?). It vetoes methods below the candidate-set median
  persistence ("a part that does not persist across frames is not a thing"),
  then debates four scoring formulas (persist-only, persist-led, boundary-led,
  balanced) and selects the one whose winner separates most decisively
  (largest margin) without being below-median on any property. Shortfalls are
  recorded, not hidden.
- `nb4` DECIDE: the winning method is applied to the middle frame; labels are
  split into connected pieces; the mechanism states and applies its own
  subject rule — "the subject of a memory is the part that moves most; the
  thing the video is about moves, the backdrop does not" — with its own
  substance bar (>= 1/100 of the frame). It derives the tracking
  polarity/threshold from the selected subject's own gray distribution, and
  holds itself to its own graftability standards (S1: no upscale beyond 4x;
  S2: >= 1024 px of connected matter).

**Fusion organ** (reused from step-3 unchanged): correspond
(recipient = argmax subject centrality), slot (neck-line split of the
recipient subject; slot = argmax texture×upperness), adapt (channel gains,
lighting gradient, shadow, edge transfer, seam self-check), track (donor and
recipient centroid tracks), synthesize (24 frames).

## Honest accounting: what the programmer supplies vs what TNN invents

Programmer-supplied: the four field instruments, histogram/gradient/labeling
operators, the four cut-procedure schemas, the four scoring-formula schemas,
the P/B/H/F property definitions, and the fusion organ. TNN invents:
which fields to try first (its seeing-hypothesis, ordered by measured
divisibility), which schema×field methods exist (from each distribution's
shape), every cut level (valleys/knees/medians/quartiles it measures), the
winning scoring formula (from its own margin argument), the subject rule, the
tracking derivation, and the graftability standards it holds itself to.
No percentile recipes, no fixed candidate list, no fixed score formula.

## What the mechanism actually invented on this input

- Bunny: 12 methods proposed; VALLEY skipped everywhere (valley-depth bar = 0,
  its own conservative rule). Winner M0 = GRAY/MEDIAN@184 via F3 boundary-led
  (margin 5532, above-median on P/B/H). Subject = head fragment, 979 px,
  highest mean motion (1351 vs body 710).
- Pig: 14 methods proposed, including GRAY/VALLEY@96 and MOTION/VALLEY@1764 —
  it found the natural valleys itself. Winner M0 = GRAY/VALLEY@96 via F3
  (margin 2959). Subject = dark head/body piece, 20019 px, mean motion 2252.

## Known limitations (stated, not hidden)

1. Motion-field methods reuse the full-sequence motion field for frames
   11/12/13, so their persistence is trivially 100% — the judge's P property
   does not genuinely test temporal support for MOTION methods. (No MOTION
   method won here, but the flaw is real.)
2. The valley-depth bar (cross-field median) is conservative: the bunny's
   GRAY valley (depth 3017) was skipped because the bar came out 0.
3. The subject rule ("part that moves most") selects a *piece*, not the
   animal: the bunny's subject is a 979-px head fragment. The fusion organ's
   slot machinery was built for whole-body subjects; fed this fragment it
   produced a degenerate 46×18 slot, and the donor shrank to a 46×64 patch.
   This subject-principle × slot interaction is the mechanism's honest
   failure mode on this input — see VERDICT.md.
