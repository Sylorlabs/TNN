# BLIND TEST-1 report — D-α (direct waveform dreaming control)

Package: `blind/test1/packages/d_alpha/` (fresh v2; see PREREG_TEST1.md
Amendment A1 — the v1 package used a noise file as its "real" clip and is
void). Three 30-second clips, clip_1/2/3. Brief: kids playing and laughing.
One clip is a real playground field recording (verified genuine: Berlin
playground `w1.wav` 30–60 s, crest 5.92, centroid 2160 Hz), one is D-α's
synth control, one is the D-α fork render.

Judges: 3 fresh native critics, signal-only analysis, disjoint from all
other packages. All three ballots valid (no blindness violations disclosed).

## Fingerprint measurements (identical across judges — same deterministic tool)

| clip | s1 (periodicity) | s2 (stationarity) | s3 (repetition) | s4 (symmetry) | s5 (formant) | S |
|---|---|---|---|---|---|---|
| clip_1 | 0.617 | 0.000 | 0.337 | 0.895 | 0.000 | 0.370 |
| clip_2 | 0.445 | 0.000 | 0.025 | 0.961 | 0.000 | 0.286 |
| clip_3 | 0.501 | 0.440 | 0.123 | 0.879 | 0.587 | 0.506 |

A-NATIVE notes: clip_1 has a flat HF hiss bed (hiss_ratio 0.496,
hf_flatness 0.88) and 7,409 clicks; clip_2 has the cleanest high band
(hiss_ratio 0.019) but 9,219 clicks (anomaly, noted); clip_3 has the fewest
clicks (551).

## Judge × label × confidence × evidence

All three judges converged on identical labels (baseline stood, no
overrides):

| judge | clip_1 | clip_2 | clip_3 | ranking (most→least real) |
|---|---|---|---|---|
| 1 | fork render, MEDIUM — strongest periodicity + s3=0.337 loop signature; breathing flux rules out synth bed | real recording, MEDIUM — lowest S, s3≈0, no stationarity, mobile formants | synth control, LOW — only stationary texture (s2=0.44), static formants (s5=0.59); 3 fingerprints dissent | clip_2 > clip_1 > clip_3 |
| 2 | fork render, LOW — constructed (s1=0.617, s3=0.337) but non-stationary; flat HF = assembly artifacts | real recording, MEDIUM — lowest periodicity/repetition, breathing, no HF bed | synth control, LOW — stationary bed + fixed resonators; dissents are spikes on other clips | clip_2 > clip_1 > clip_3 |
| 3 | fork render, LOW — constructed discrete events, not a bed | real recording, LOW — breathing spectrum, no fixed formants | synth control, LOW — canonical bed pair s2+s5; s4 dissent built on only 17 transients | clip_2 > clip_1 > clip_3 |

## Inter-judge agreement

100% on labels and ranking.

## Against the sealed key

Post-ballot verification (byte-match of package clips against sources):
clip_1 = **synth control**, clip_2 = **fork render**, clip_3 = **real
recording** — the judges' labels are a full rotation off ground truth. All
three judges labeled the verified genuine playground segment (w1 30–60 s)
"synth control" and the synth control "fork render".

The cause is measurable: the genuine segment carries a stationary
background wash (s2=0.440, the only nonzero stationarity in the set) and
unusually stable formants (s5=0.587) — the exact filtered-noise-bed +
fixed-resonator signature the theory assigns to synths. The machine track
cannot acquit a real recording whose background is this steady; conversely
it reads D-α's actual synth control (s2=0, s5=0, breathing envelope) as the
constructed-but-not-synth middle clip.

## Majority verdict

The fork render was labeled **"real recording" by 3/3 judges** and "synth
control" by 0/3. Per the preregistered fail rule (≥2 "synth control" on the
fork render), **D-α PASSES machine-blind Test 1.**

**Mandatory caveat — this pass is hollow.** The machine track convicted the
genuine playground and acquitted the actual synth control on the same
evidence. The D-α package's real segment is an unfortunate draw: a
playground segment whose steady background wash the fingerprints read as
synthetic. The verdict follows the frozen rule mechanically, but the
real-vs-synth discrimination inverted on this content — the machine cannot
be said to have told real from synth here, only to have failed to label the
fork render "synth control". Any downstream claim about D-α should carry
this inversion explicitly. Micah's ears remain the final oracle.
