# BLIND TEST-1 — D-ALPHA — Blind Native Critic Ballot (judge3, v2)

**Role:** blind native critic. No hearing; signal-only analysis. Method: the
frozen measurement tool on the three clips, scored against the agreed
synth-smell fingerprint theory.

## Per-clip results

| clip | s1 (periodicity) | s2 (stationarity) | s3 (loop/repetition) | s4 (transient symmetry) | s5 (formant stability) | S (syntheticity) | A-NATIVE notes | label | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| clip_1 | 0.6171 | 0.0000 | 0.3374 | 0.8945 | 0.0000 | **0.3698** | dc≈0, 0 clipped, clicks 7409, **hiss_ratio 0.496** (hissy), hf_flatness 0.88, 1.43 transients/s | **fork render** | LOW | middle S; strongest periodicity+repetition of the three (s1 #1, s3 #1) — constructed events, not a bed |
| clip_2 | 0.4454 | 0.0000 | 0.0246 | 0.9606 | 0.0000 | **0.2861** | dc≈0, 0 clipped, **clicks 9219** (high), hiss_ratio 0.019 (clean HF), hf_flatness 0.79, 0.40 transients/s, flux_cv 1.39 / rms_cv 1.37 (breathing) | **real recording** | LOW | lowest S; near-zero loop score, non-stationary spectrum, most HF-clean |
| clip_3 | 0.5012 | 0.4399 | 0.1232 | 0.8794 | 0.5868 | **0.5061** | dc≈0, 0 clipped, clicks 551, hiss_ratio 0.067, hf_flatness 0.53, 0.57 transients/s, centroid_cv 0.145 (rigid) | **synth control** | LOW | highest S; only clip with stationary texture (s2 #1 by a mile) AND fixed resonances (s5 #1) |

S gaps: clip_3 − clip_1 = **0.1363**; clip_1 − clip_2 = **0.0837**.

## Forced ranking by "most likely a real field recording"

1. **clip_2** (S = 0.2861 — least synth-smell)
2. **clip_1** (S = 0.3698)
3. **clip_3** (S = 0.5061 — most synth-smell)

## Baseline vs override

**Baseline stands; no override.** Per the preregistered rule, highest S →
synth control (clip_3), lowest S → real recording (clip_2), middle →
fork render (clip_1).

Justification for keeping clip_3 as the synth despite dissenting fingerprints:
- The two fingerprints that pin clip_3 are the canonical bed-texture pair —
  **s2 stationarity 0.4399** (others exactly 0.0) and **s5 formant stability
  0.5868** (others exactly 0.0), with the lowest spectral-centroid movement
  (centroid_cv 0.145 vs 0.659 / 0.7804). A stationary spectral bed with fixed
  resonances is the filtered-noise synth fingerprint the theory predicts.
- The dissents are thin: s1 and s3 rank clip_1 above clip_3 (clip_1 looks like
  *constructed, repeated events* — consistent with a fork rendering discrete
  play events, not a continuous bed), and s4 ranks clip_3 last, but s4 is
  computed on only 17 transients at 0.57/s with low attack amplitude — weak
  evidence vs clip_3's s2+s5 double signature.
- clip_2 keeps the "real" label: lowest loop score (0.0246 — nothing repeats),
  flux_cv/rms_cv highest among the low-S pair (breathes), cleanest high band
  (hiss_ratio 0.019), no clipped samples, no fixed formants (s5 = 0). The high
  s4 (0.9606) on only 12 detected transients is a detector-noise artifact, not
  a real symmetric-boom signature; it does not overturn four of five
  fingerprints ranking it least synthetic.

## Confidence: LOW (all three)

LOW per the frozen rule: ≥2 fingerprints dissent on the top-S clip's rank
(s1: clip_1 > clip_3; s3: clip_1 > clip_3; s4: clip_2, clip_1 > clip_3), even
though both S gaps ≥ 0.05 (0.1363 and 0.0837). The middle clip's
periodicity/repetition lead (s1 0.6171, s3 0.3374) is a genuine counter-signal
consistent with a *loop-based* synth design, so the clip_1-vs-clip_3 split
(constructed events vs stationary bed) is a judgment call, not a slam dunk.

## A-NATIVE anomalies (noted, not decisive)

- clip_1: hiss_ratio 0.496 with hf_flatness 0.88 — very hissy high band;
  under A-NATIVE this would fail field-recording quality, but identity is
  decided on fingerprints, where clip_1 sits middle.
- clip_2: 9219 clicks in 30 s — notable; may be natural mouth/hand transients
  or a recording artifact. Not identity-relevant without a listen.
- No clip has DC offset, clipped samples, or a concerning hiss flatness
  otherwise.

## DISCLOSURE

I opened **only** the three listed clip files
(`d_alpha/clip_1.wav`, `clip_2.wav`, `clip_3.wav`) plus the measurement tool
specified in the task. I did **not** open anything under
`.../blind/test1/keys/` (sealed mappings) or any other package, report, or
source file. I did not recognize any clip — no prior exposure to these
recordings. No web search was used. No non-signal information influenced the
ballot. Ballot is valid.
