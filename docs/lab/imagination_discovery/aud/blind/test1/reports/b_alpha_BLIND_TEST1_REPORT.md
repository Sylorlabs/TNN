# BLIND TEST-1 report — B-α (pure study-then-invent)

Package: `blind/test1/packages/b_alpha/` (fresh v2; see PREREG_TEST1.md
Amendment A1 — the v1 package used a noise file as its "real" clip and is
void). Three 30-second clips, clip_1/2/3. Brief: kids playing and laughing.
One clip is a real playground field recording (verified genuine: Berlin
playground `w1.wav` 0–30 s, crest 7.17, centroid 2149 Hz), one is B-α's
synth control, one is the B-α fork render.

Judges: 3 fresh native critics, signal-only analysis, disjoint from all
other packages. All three ballots valid (no blindness violations disclosed).

## Fingerprint measurements (identical across judges — same deterministic tool)

| clip | s1 (periodicity) | s2 (stationarity) | s3 (repetition) | s4 (symmetry) | s5 (formant) | S |
|---|---|---|---|---|---|---|
| clip_1 | 0.874 | 0.000 | 0.071 | 0.776 | 0.626 | 0.470 |
| clip_2 | 0.632 | 0.188 | 0.076 | 0.727 | 0.342 | 0.393 |
| clip_3 | 0.693 | 0.000 | 0.000 | 0.723 | 0.339 | 0.351 |

A-NATIVE notes: clip_1 carries 5,790 digital clicks and a flat high-band
hiss bed (hiss_ratio 0.317, hf_flatness 0.80); clip_3 has the highest
spectral-flux variability (1.73) — the messiest, most breathing envelope.

## Judge × label × confidence × evidence

All three judges converged on identical labels (baseline stood, no
overrides):

| judge | clip_1 | clip_2 | clip_3 | ranking (most→least real) |
|---|---|---|---|---|
| 1 | synth control, LOW — s1/s4/s5 lead; dissents weak | fork render, LOW | real recording, LOW — s3=0, most mobile formants, lowest hiss | clip_3 > clip_2 > clip_1 |
| 2 | synth control, LOW — periodic + static formants + flat hiss | fork render, LOW — mildly stationary/loop-y (s2=0.19, s3=0.076) | real recording, LOW — zero repeats, breathing flux | clip_3 > clip_2 > clip_1 |
| 3 | synth control, LOW — strongest constellation (s1=0.87, s5=0.63, flat HF) | fork render, LOW | real recording, LOW — messy, non-repeating | clip_3 > clip_2 > clip_1 |

All confidences LOW per the frozen rule (middle S gap 0.0423 < 0.05; two
fingerprints dissent on clip_1's top rank). Every judge flagged the
clip_2-vs-clip_3 (real-vs-fork) call as the genuinely uncertain one.

## Inter-judge agreement

100% on labels and ranking.

## Against the sealed key

Post-ballot verification (byte-match of package clips against sources):
clip_1 = synth control ✓ (judges correct), clip_2 = **real recording**,
clip_3 = **fork render** — the judges unanimously swapped the real↔fork
pair. The B-α fork render (S=0.351) scored *more real-like* than the genuine
Berlin playground (S=0.393): the playground's steady background wash
(s2=0.19) reads as mildly stationary next to the render's messier envelope.

## Majority verdict

The fork render was labeled **"real recording" by 3/3 judges** and "synth
control" by 0/3. **B-α PASSES machine-blind Test 1** — and then some: no
judge put the fork render last on realness; all three ranked it first. The
fail bar (≥2 judges labeling the fork render "synth control") was not met.
Caveat: confidence LOW throughout; the machine track finds B-α's render
indistinguishable from — here slightly *more* real-like than — the genuine
playground on the syntheticity index.
