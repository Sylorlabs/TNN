# TNN Audio Round 3 — Line Verdict (2026-09-27)

**Mission:** resolve the MPEG-1 32 kHz MP3 `n_long_bands` discrepancy; white-box and broadly
repair de-synth planner contour/octave/calibration walls; waveform analysis before every audio
claim; independent red team from committed source (incl. the t12-vs-t14/t11 regression trap).

## Verdicts

| # | Item | Verdict | Detail |
|---|---|---|---|
| 1 | MP3 32 kHz `n_long_bands` discrepancy | **HONEST KILL — no discrepancy exists** | The oracle shifts only for MPEG-2.5 12 kHz (`my_sr == 2`), not MPEG-1 32 kHz. The risk report confused the sr index with the version-offset `my_sr`. This decoder is MPEG-1-only, so the shift is unreachable; hardcoded `2` is correct for 44.1/48/32 kHz. Proven with a minimal 32 kHz mixed-block reproducer (44 mixed granules, ≤1 LSB vs oracle, non-vacuous). Prior "32k" fixtures were 32 kbps, not 32 kHz — why the misdiagnosis survived. Comment-only annotation at the code site; zero behavioral change. |
| 2 | Pre-existing mixed-block stride fix (39→40) | **VERIFIED, already committed** (beb955732, on origin) | All 4 mixed fixtures ≤1 LSB vs oracle; `t_128cbr` SHA reproduced. Round 3 re-verified, not re-fixed. |
| 3 | Planner D2 contour (median-rescale candidate) | **KILL** | Mean err_pm 425.10→405.30, dramatic t12 (172→0) and t14 (146→0) wins — but t5 +13, t9 +4, t10 +1, t13 +9 violate the absolute no-regression bar. Error redistribution, not a mechanism fix (z.ai's warning, validated). Candidate kept as evidence, bannered KILLED. |
| 4 | Planner residual (b) probe generalization | **DEFERRED, mechanism narrowed by measurement** | Telemetry decomposition (new experiment): e_renderer = 0 (wavetable exact), e_instrument = 0.15 Hz on smooth contours (tracker NOT contour-dependent — refines the z.ai hypothesis). The real corruption is the planner's arithmetic mean over spike-carrying 16-pt contours (208 Hz vs true ~145 Hz): a narrow spike-statistic problem, not wholesale calibration failure. Flat-probe calibration is VALID for smooth contours. Next: M3 closed-loop replan per z.ai ordering, or a spike-robust statistic that doesn't perturb non-spiky contours. |
| 5 | Planner residual (c) t17 octaves | **KILL at planner level** | 17/109 harmonic captures re-verified in reference hearing; unfixable at planner level (round-2 proof stands). |

## Evidence committed

- `docs/lab/universal_intake/mp3/round3_2026-09-27/` — MINIMAL_REPRO.md, EVIDENCE.md,
  32 kHz mixed fixtures + generator (`flip_mixed.py`), SHA-256 manifest.
- `docs/lab/universal_intake/mp3/zag_full/mp3dec.zag` — comment-only annotation of the
  honest kill at the `n_long_bands` site (byte-identical behavior, verified by rebuild).
- `docs/lab/audio_longhorizon/desynth/round3_2026-09-27/` — WHITEBOX.md (D2 mechanism,
  R4 veto, telemetry §3.4), EVIDENCE.md (battery tables, waveform data, 6/6 atoms
  byte-identical), SHA256SUMS, `plan_r3.zag` (KILLED candidate, evidence only),
  z.ai second-opinion Q&A.

## Standing notes

- Regression gate is now load-bearing for all future planner acceptance: with byte-identical
  determinism any fixture regression is real; mean-based gates pass bias-shuffling fixes.
- z.ai (GLM-5.3) review folded in: "honest prediction" was the wrong *object* (pointwise map
  vs stateful functional); "measured probe bias" is entangled with the tracker — decompose
  before calibrating. Telemetry decomposition is the standing protocol for such disputes.
- Red-team report follows as a separate commit.
