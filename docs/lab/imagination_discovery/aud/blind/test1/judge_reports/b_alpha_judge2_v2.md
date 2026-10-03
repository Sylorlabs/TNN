# BLIND TEST-1 · Package B-ALPHA · Judge 2 (native critic) ballot

- **Judge:** blind native critic #2. Cannot hear; signal-only analysis.
- **Method:** `measure_test1.py` run once on the three listed clips. No other inputs.
- **Date:** 2026-09-22.

## 1. Per-clip measurements and labels

| clip | s1 (rhythm periodicity) | s2 (stationarity) | s3 (near-exact repetition) | s4 (transient symmetry) | s5 (formant stability) | S (syntheticity) | key A-NATIVE notes | label | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| clip_1 | 0.8744 | 0.0000 | 0.0714 | 0.7759 | 0.6261 | **0.4696** | clicks 5790 (193/s), hiss_ratio 0.317, hf_flatness 0.796, 29 transients (0.97/s), dc 5.6e-06, 0 clips | **synth control** | LOW | Highest S; extreme envelope periodicity (0.874) + highest s5 (0.626) + flat hissy high band (0.80/0.317). |
| clip_2 | 0.6323 | 0.1877 | 0.0764 | 0.7273 | 0.3421 | **0.3932** | clicks 1437, hiss_ratio 0.071, hf_flatness 0.534, 5 transients (0.17/s), dc 4.2e-07, 0 clips | **fork render** | LOW | Middle S; the only clip with s2>0 (0.188) AND the highest s3 loop score (0.076) — slightly loop-y, slightly stationary texture. |
| clip_3 | 0.6929 | 0.0000 | 0.0000 | 0.7231 | 0.3387 | **0.3509** | clicks 872 (lowest), hiss_ratio 0.050 (lowest), hf_flatness 0.559, 4 transients (0.13/s), flux_cv 1.734 / rms_cv 0.601 (highest variability), dc 3.9e-07, 0 clips | **real recording** | LOW | Lowest S; s3 = 0.000 (zero near-exact 1 s repeats), s2 = 0.000, lowest s5 (0.339) — messy, unrepeatable, breathing. |

Baseline applied: highest S → synth, lowest S → real, middle → fork. No override (see §3).

### A-NATIVE anomaly notes
- DC offset is negligible on all three (≤ 5.6e-06); zero digital clipping on all three. No A-NATIVE rejectors fire anywhere.
- The large click-count spread (5790 / 1437 / 872) and the hf_flatness 0.80 on clip_1 (high band flat, noise-like) are noted as anomalies, not as identity proof. The click counts likely reflect transient/edge density rather than clean real-world mic handling.
- clip_3's flux_cv (1.73) and rms_cv (0.60) are the highest — envelope variability consistent with a living, gusting ambience.

## 2. Forced ranking by "most likely to be a real field recording"

1. **clip_3** — zero near-exact repetition, zero stationarity, lowest formant stability, highest envelope variability.
2. **clip_2** — middle syntheticity; mild stationarity + highest loop score keep it below clip_3.
3. **clip_1** — highest syntheticity on 3 of 5 fingerprints with a wide margin; least real-like.

## 3. Overrides

**None.** Baseline stands. The dissenting fingerprints (s2 and s3 rank clip_2 above clip_1) do not meet the bar for an override: clip_1's lead is driven by s1 (0.8744 vs next 0.6929), s4 (0.7759 vs next 0.7273), and s5 (0.6261 vs next 0.3421) — three of the five fingerprints, including the two largest margins — and its S margin over clip_2 (0.0764) exceeds the MEDIUM-gap threshold. The cited-evidence condition for overriding (top-S clip's evidence undermined, middle clip carrying the synth signature) is not met: clip_2's s2/s3 elevation is mild, while clip_1's periodicity + static-formant + flat-hiss profile is the coherent synth signature.

## Confidence computation (per frozen rules)

- S ranking gaps: 0.4696 − 0.3932 = **0.0764**; 0.3932 − 0.3509 = **0.0423**.
- Fingerprint agreement on the top-S clip's rank: s1 ✓, s4 ✓, s5 ✓ agree (clip_1 highest); s2 ✗ and s3 ✗ dissent (both rank clip_2 highest).
- Rule application: any gap < 0.05 (0.0423) → **LOW**; also ≥2 fingerprints dissent → **LOW**. Confidence is LOW on all three labels, driven by the narrow S2–S3 gap (0.0423) and the s2/s3 dissent. The synth label on clip_1 is the strongest individual leg (gap 0.0764 ≥ 0.05, 3/5 fingerprints agree), but the per-label confidence rule's LOW clause on the narrow middle gap keeps it at LOW overall.

## 4. DISCLOSURE

- I opened **only** the three listed clips (via the measurement tool on their paths) and nothing else in the test-1 directory. I did **not** open anything under `keys/` or any other package, documentation, or report.
- I did **not** recognize any of the three clips — I have never encountered them before this ballot.
- I used **no non-signal information**: no web search, no prior knowledge of the forks, no metadata beyond the tool's numbers. Only the measurement numbers and the fingerprint theory supplied in the task.
- **My ballot is valid (not void).**

---
*Submitted by Judge 2 · blind native critic · B-ALPHA package*
