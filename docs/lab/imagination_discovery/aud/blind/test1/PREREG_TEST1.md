# BLIND TEST-1 — preregistration (machine-blind judging of the five audio forks)

Written 2026-09-22 **before** any blind package was assembled, any key file
was opened, or any measurement was run. Frozen: once the judge crews are
dispatched, the scoring below does not change.

## 1. What is being judged

Test 1 (kids playing and laughing) for the five audio forks B-α, B-β, B-γ,
A-α, D-α. The lead's ears are the final oracle and still rule each fork's
claim; this is the parallel **machine-blind** track. Judges cannot hear;
they analyze signal only.

## 2. Packages

| Package | Unlabeled clips | Labeled |
|---|---|---|
| b_beta | blind_A/B/C.wav (sealed; never open KEY.sealed.txt) | none |
| b_gamma | judge_A/B/C.wav (sealed; never open ORDER_SEALED.md; do NOT open clip_real/clip_synth/clip_method.wav — those are unblinded sources) | none |
| b_alpha | clip_1/2/3.wav (fresh; see §3) | none |
| d_alpha | clip_1/2/3.wav (fresh; see §3) | none |
| a_alpha | clip_1/2.wav (fork render, real recording; fresh) | calib_real.wav (known real), calib_synth.wav (known synth) |

Labels for fresh packages are assigned deterministically by
sha256(fork_name + "blind_test1_v1") — no RNG anywhere. Keys live in
`blind/test1/keys/`; no judge may read them. Judge sets are **disjoint per
package** (no critic judges two packages, so no cross-package clip
recognition can leak).

## 3. Fresh package contents

- b_alpha: `b_alpha_kids_v1.wav` (fork render) + `control_synth_kids.wav`
  (its synth control) + real playground clip (Wikimedia Commons CC0 Berlin
  playground, 0–30 s segment, resampled 48k→44.1k stereo→mono).
- d_alpha: `d_alpha_kids.wav` + `synth_control_kids.wav` + real playground
  clip (Berlin 60–90 s segment).
- a_alpha: `kids_a_alpha.wav` + real playground clip (kids_playground.wav
  0–30 s) as the two unlabeled clips; labeled calibration pair =
  Berlin 30–60 s segment (known real) + `control_synth_kids.wav` (known
  synth, borrowed as calibration; it also appears inside the b_alpha
  package, but judge sets are disjoint).
- All fresh clips normalized: 30.0 s, mono, 44.1 kHz, 16-bit, same RMS
  level, identical WAV container — no format tells.

## 4. Metrics (measure_test1.py)

Synth-smell fingerprints from AUDIO_DEBATE.md §3, per clip:

- s1 envelope periodicity — event-rhythm regularity (periodic oscillators,
  regular spacing)
- s2 stationarity — 1 − clipped spectral-flux / RMS-envelope CV (filtered
  noise beds)
- s3 loop score — fraction of distant (≥2 s apart) 1 s chunk pairs with
  log-mel cosine > 0.999 (near-exact repetition, the loop/assembly smell)
- s4 transient symmetry — mean attack/decay symmetry of transients
  (symmetric envelopes)
- s5 formant stability — 1 − clipped spectral-centroid CV on high-energy
  frames (static formants / fixed ring)

**S (syntheticity index) = mean(s1..s5), 0..1. Higher = more synth-like.**

A-NATIVE checks per clip: DC offset, hiss ratio (8–20 kHz / 0.3–8 kHz),
high-band spectral flatness, clip count, click count, transients/s.

## 5. Scoring rules

### 5a. Triple packages (b_beta, b_gamma, b_alpha, d_alpha)

Each contains exactly one {real recording, synth control, fork render}.

- Baseline prediction from S: argmax S → "synth control"; argmin S →
  "real recording"; middle → "fork render".
- A judge MAY override the baseline, but only with a written justification
  citing individual fingerprint evidence (e.g. "top-S is driven solely by
  s5 while s1/s2/s3 all rank it lowest; the middle clip shows stationary
  high-band hiss and periodic envelope, so I label the middle one the
  synth"). An override without cited fingerprint evidence is invalid.
- Forced-choice label per clip, plus confidence per label:
  - **high**: both S ranking gaps ≥ 0.10 AND all five fingerprints agree on
    the top-S clip's rank;
  - **medium**: ranking clear (both gaps ≥ 0.05) but ≥1 fingerprint
    dissents from the baseline ranking;
  - **low**: any S gap < 0.05, or ≥2 fingerprints dissent.
- Synth-smell evidence table per clip: all five fingerprints + the two or
  three A-NATIVE numbers that most discriminate.
- **Forced ranking**: rank the three by "most likely to be a real field
  recording."

### 5b. A-α package (calibration-anchor design)

Unlabeled clip_1/clip_2; labeled calib_real / calib_synth. Judges:

- measure S on all four;
- forced choice: which unlabeled clip is the real recording (the other is
  the fork render);
- forced ranking of all four by "most likely to be a real field
  recording";
- confidence: **high** if |S(u) − S(nearest anchor)| ≥ 0.10 on the chosen
  side; **medium** if ≥ 0.05; **low** otherwise.

### 5c. Disclosures

Any judge who opened a key file, recognized a clip from prior work, or
used anything other than signal analysis invalidates their own ballot —
the report is still published, the ballot is excluded from the majority.
This is disclosed per judge in the report.

## 6. Verdict rules (machine level)

- Triple packages: the fork **FAILS machine-blind Test 1** iff a majority
  (≥2 of 3 judges) labels the fork render "synth control".
- A-α: the fork **FAILS** iff a majority (≥2 of 3) ranks the fork render
  below calib_synth (least-real of the four).
- Otherwise the fork **PASSES at the machine level**.
- Reported per fork: judge × label × confidence × synth-smell evidence
  table; inter-judge agreement (pairwise % agreement on the fork render's
  label); majority verdict.
- The lead's ear verdict still rules the fork's claim regardless.

## 7. Notes

- Judges are fresh native critics only — no builder agents from any fork
  crew appear anywhere in this wave.
- The B-β and B-γ sealed packages are used as-is; their keys stay sealed
  through the whole wave.

## 8. Amendment A1 (2026-09-22, before any v2 judging; b_beta/b_gamma
ballots unaffected)

The v1 real clips were built from `b_alpha/study/s1_playground_berlin.wav`
(segments 0–30 / 30–60 / 60–90 s). Post-assembly verification showed that
file is NOT a playground recording: both channels are uncorrelated
stationary noise (crest 3.0 constant, spectral centroid 11.8 kHz constant,
zero-crossing rate 0.48 ≈ white noise), despite the study log listing it as
a CC0 Berlin playground. The same noise file also exists as
`b_beta/sources/kids_berlin.wav` (flagged for the lead: B-β's study log
says it used `kids_berlin` for background voices — provenance caveat on
B-β's render, not adjudicated here).

Consequences:
- v1 packages for b_alpha, d_alpha, a_alpha are VOID; their keys are
  preserved as `keys/<fork>_key_v1_VOID.json`; any v1 judge ballots are
  void (the three completed B-α v1 ballots correctly identified the noise
  clip as the most synth-like, S≈0.87 — the metric machinery worked).
- v2 packages rebuilt with VERIFIED-genuine real clips (crest > 5,
  centroid < 4 kHz, 44.1 kHz mono):
  - b_alpha real: `b_alpha/study/w1.wav` 0–30 s (crest 7.17, 2149 Hz)
  - d_alpha real: `b_alpha/study/w1.wav` 30–60 s (crest 5.92, 2160 Hz)
  - a_alpha real: `b_alpha/study/w2.wav` 0–30 s (crest 7.76, 1816 Hz)
  - a_alpha calib_real: `b_alpha/study/w4.wav` full 30 s (crest 7.77, 1628 Hz)
- v2 label mapping uses seed "<fork>blind_test1_v2" (same deterministic
  scheme). v2 judge reports are suffixed `_v2`.
- B-β's sealed `real_calib_30s.wav` verified genuine (crest 7.77,
  centroid 1628 Hz); the sealed B-β/B-γ packages and their judges are
  unaffected.

- Judges are fresh native critics only — no builder agents from any fork
  crew appear anywhere in this wave.
- The B-β and B-γ sealed packages are used as-is; their keys stay sealed
  through the whole wave.
- This document was written before any package was built, any key opened,
  or any measurement computed.
