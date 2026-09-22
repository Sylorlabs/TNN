# BLIND TEST-1 report — A-α (control)

Package: `blind/test1/packages/a_alpha/` (fresh v2; see PREREG_TEST1.md
Amendment A1 — the v1 package used a noise file as its "real" clip and is
void). Four 30-second clips: two blind (clip_1, clip_2) plus two labeled
anchors (calib_real = verified genuine Berlin playground `w4.wav`, full
30 s; calib_synth = labeled synth control). Brief: kids playing and
laughing. One blind clip is the real playground recording (verified genuine:
Berlin playground `w2.wav` 0–30 s, crest 7.76, centroid 1816 Hz); the other
is the A-α fork render.

Judges: 3 fresh native critics, signal-only analysis, disjoint from all
other packages. All three ballots valid (no blindness violations disclosed).

## Fingerprint measurements (identical across judges — same deterministic tool)

| clip | s1 | s2 | s3 | s4 | s5 | S |
|---|---|---|---|---|---|---|
| clip_1 | 0.626 | 0.298 | 0.012 | 0.822 | 0.000 | 0.352 |
| clip_2 | 0.580 | 0.000 | 0.503 | 0.772 | 0.000 | 0.371 |
| calib_real | 0.847 | 0.461 | 0.007 | 0.827 | 0.402 | 0.509 |
| calib_synth | 0.874 | 0.000 | 0.071 | 0.776 | 0.626 | 0.470 |

A-NATIVE notes: clip_2 is the only damaged clip — 723 hard-clipped samples,
10,414 digital clicks (347/s), 34 transients at 1.13/s; all other clips
have 0 clipped samples. clip_2's HF is flat (hf_flatness 0.90, like the
synth control's 0.80); clip_1's hiss (0.0325) matches the real anchor
(0.0354), far from the synth control's noise bed (0.3168).

**Anchor anomaly (disclosed):** calib_real's S (0.509) is HIGHER than
calib_synth's (0.470) — the aggregate index inverts on this content (the
genuine `w4.wav` playground carries a stationary background wash,
s2=0.461, that inflates S). All three judges independently detected this and
invoked the preregistered fingerprint override; the S-anchor rule was
non-discriminant here. This is a metric-calibration caveat, not a package
defect — the sources are byte-verified genuine/labeled.

## Judge × label × confidence × evidence

| judge | clip_1 | clip_2 | ranking (most→least real) |
|---|---|---|---|
| 1 | real recording, MEDIUM — matches real anchor near-exactly on s3/s4, closer on s2/s5, natural hiss | fork render, MEDIUM — s3=0.503 (7× the synth anchor; verbatim self-repetition), only damaged clip, s2/s4 ≈ synth anchor | calib_real > clip_1 > calib_synth > clip_2 |
| 2 | real recording, MEDIUM — s3/s4/hiss all match real anchor; s3=0.012 vs 0.503 | fork render, MEDIUM — s3=0.503 (68× real anchor: half of distant 1-s pairs >0.999-identical), 723 clips, 10,414 clicks | calib_real > clip_1 > calib_synth > clip_2 |
| 3 | real recording, MEDIUM — s3≈real anchor, mean fingerprint distance 0.159 to real | fork render, MEDIUM — s3=0.5025 loop signature; invoked override, HIGH→MEDIUM per rule | calib_real > clip_1 > calib_synth > clip_2 |

All three invoked the preregistered override (fingerprints contradict the
S-anchor verdict) and dropped confidence one level per rule: MEDIUM.

## Inter-judge agreement

100% — all three judges agree on both forced choices and the full ranking.

## Against the sealed key

Post-ballot verification (byte-match of package clips against sources):
clip_1 = real recording ✓ (judges correct), clip_2 = fork render ✓ (judges
correct). Both forced choices match ground truth unanimously.

## Majority verdict

The fork render was ranked **below calib_synth — least-real of the four —
by 3/3 judges**. Per the preregistered A-α rule, the fork is machine-
convicted as the synth: **A-α FAILS machine-blind Test 1.** The evidence is
a loop/paste signature (s3=0.503: half of all distant 1-second chunk pairs
near-identical — verbatim self-repetition, which no voice does) plus
assembly scars: 723 hard-clipped samples and 10,414 digital clicks found in
no other clip. The forced choices were unanimous and correct; confidence
MEDIUM throughout.

**Caveat for interpretation:** this is the machine track's verdict on the
signal fingerprints. Micah's ears remain the final oracle — a single "sounds
like a synth" from him kills the fork's claim regardless, and his verdict
may also acquit where the machine convicts.
