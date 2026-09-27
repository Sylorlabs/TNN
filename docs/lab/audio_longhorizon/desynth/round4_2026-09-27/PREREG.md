# Audio Round 4 — FROZEN PREREG

**Date:** 2026-09-27. **Status:** FROZEN. **Line:** audio_longhorizon desynth planner.
**Parent evidence:** round 3 commits `d1b943161e8a` (planner walls verdict) and
`7aad68fadb70` (independent red-team report, V-D finding).

## 1. What round 3 settled (not re-litigated)

- The unconditional median-rescale candidate is KILLED: mean 425.10 → 405.30,
  but t5/t9/t10/t13 regressed. The absolute no-regression bar is load-bearing.
- t17 octaves are unfixable at planner level (17/109 harmonic captures re-verified).
- The MP3 "32 kHz n_long_bands discrepancy" never existed (oracle branch is
  MPEG-2.5-only; this decoder is MPEG-1-only). Mixed-block stride 39→40 stands verified.
- Residual corruption is the planner's arithmetic mean over spike-carrying
  16-point contours (telemetry decomposition: e_renderer = 0, e_instrument = 0.15 Hz).

## 2. The candidate under test: the V-D directional rule (existence proof only)

Round-3 red team (post-hoc, same 20-target battery that discovered the pattern —
**no held-out validation**) found:

> Use `interp_median` for `fcmd` ONLY IF `median > mean`, else keep the baseline mean.

Dev result: t12 172→0, t14 146→0, total 8502→8184 (−318), **zero regressions**.
Byte-identity proven: V-D t12/t14 iter3 WAVs == candidate WAVs; V-D t5/t9/t10/t13 == baseline.

Mechanism story (to be tested, not assumed): when low outliers drag the contour
mean DOWN (median > mean), the median is the robust rescale statistic; when the
mean is dragged UP (median < mean), the median locks onto a low mode and hurts.
**This round tests whether the directional pattern generalizes to unseen contours.**

## 3. Candidate specification (frozen — implement exactly this, nothing more)

In the contour-correction block, replace the fcmd computation with:

```
let csum0: i64 = 0; let ccnt0: i64 = 0;
qq0 in 0..16: vv0 = get64(CC, qq0*8); if (vv0 > 0) { csum0 = csum0 + vv0; ccnt0 = ccnt0 + 1; }
let cmean0: i64 = 0; if (ccnt0 > 0) { cmean0 = csum0 / ccnt0; }
let med0: i64 = interp_median(CC, fcur);
let fcmd: i64 = 0;
if (ccnt0 > 0 && med0 > cmean0) {
    let bac: i64 = bias_ppm_at(CALIB, timbre_of(am), med0);
    fcmd = med0 + med0 * bac / 1000000;
} else if (ccnt0 > 0) {
    let bac: i64 = bias_ppm_at(CALIB, timbre_of(am), cmean0);
    fcmd = cmean0 + cmean0 * bac / 1000000;
}
```

- Comparison is STRICT `>` on integer mHz (med0 is 1-Hz-quantized). No margin, no `>=`.
- Everything else in the planner is byte-identical to the frozen round-3 candidate
  source (`plan_r3.zag`, SHA-256 `1a0e82abf900983b4a6d51d7afb15106389f0360920610eb19d0bb0fc1cd96f6`),
  including the R4 gatekeeper's mean-based `fpred2`. No other change is permitted.
- The baseline arm is the mean-only path (closure `plan_final_full.zag` fcmd block,
  verified below). Two sources: `plan_r4base.zag` (mean-only), `plan_r4vd.zag` (rule).
- Pure Zag, zero RNG. Pinned toolchain `znc_linux_x86_64_abed8aa1`.

## 4. Held-out fixtures (round-3's 20 targets are DEV now — never score on them)

- 20 fresh targets from `~/workspace/audio_longhorizon/corpus/`, format `L <wav>`
  (same as the dev battery, which used kind=L for all 20).
- Exclusions: the 20 dev refs (listed in §4.1) and every file in
  `REJECTIONS.csv`. No other filtering.
- Selection: deterministic — sorted filename listing per category
  (child, field, lowf0, prosody, speech), fixed stride, first 20 valid picks,
  4 per category. No cherry-picking, no listening-first.
- The fixture crew is BLIND to §2–§3 (they receive only this section and the
  format spec). They never open the planner source or the round-3 reports.
- Sealed with SHA-256 manifest before the build crew runs.

### 4.1 Dev refs (excluded from held-out)

field/field-fsd50k-100019.wav, field/field-fsd50k-100036.wav,
field/field-fsd50k-100039.wav, field/field-tau-airport-barcelona-0-0-0-a.wav,
field/field-usn-C-AS-roos-001.200120.141819.06.wav, lowf0/lowf0-ptdb-012-M05_sa1.wav,
lowf0/lowf0-ptdb-016-M01_si459.wav, lowf0/lowf0-ptdb-020-M08_sa2.wav,
lowf0/lowf0-ptdb-022-M07_sa1.wav, lowf0/lowf0-ptdb-027-M10_sa1.wav,
prosody/prosody-cremad-1002-DIS.wav, prosody/prosody-emov-Amused-009.wav,
prosody/prosody-emov-Disgusted-004.wav, prosody/prosody-emov-Sleepy-019.wav,
prosody/prosody-mir1k-bug_5_04.wav, prosody/prosody-ravdess-17-05.wav,
prosody/prosody-ravdess-18-06.wav, prosody/prosody-ravdess-24-05.wav,
speech/speech-e22-001.wav, speech-e22-022.wav

## 5. Implementation-verification gate (dev set — must pass before held-out)

Before the sealed set is opened:
- `plan_r4base.zag` on the 20 dev targets reproduces the committed round-3
  baseline err_pm table 20/20 (EVIDENCE.md §1.1).
- `plan_r4vd.zag` on the 20 dev targets reproduces the V-D table 20/20
  (t12 172→0, t14 146→0, total 8502→8184, zero regressions).
- Failure here = implementation drift, not a mechanism verdict. Fix and re-verify.

## 6. Kill bars (frozen)

| Bar | Criterion | Verdict on failure |
|---|---|---|
| K1 improvement | mean err_pm over 20 held-out targets strictly < baseline mean | KILL |
| K2 no-regression (ABSOLUTE, load-bearing) | no held-out target's err_pm exceeds its baseline err_pm | KILL |
| K3 determinism | 2× runs + MALLOC_PERTURB_ perturbation byte-identical (logs + WAV SHAs) | KILL |
| K4 waveform-first | every claimed improvement backed by waveform analysis showing real f0 movement (analyzer-first; no metric-only claims) | KILL |
| K5 red team | independent red team fails to kill | KILL |

Diagnostics (reported, not gated): rule fire count (targets where med0 > cmean0 fired),
per-fire Δ, per-category breakdown.

**Inconclusive clause:** if the rule fires on 0/20 held-out targets, the verdict is
INCONCLUSIVE (battery lacked the phenomenon), not PASS or KILL.

## 7. Out of bounds

- No tuning on held-out fixtures. No rule-text change (no margin, no `>=`, no
  additional conditions). No re-litigation of §1 kills.
- The dev set is for implementation verification (§5) only — never for scoring.
- No per-target special-casing, no hardcodes, no new statistics.

## 8. Red-team mandate

Independent crew, not involved in build/run. Attack: (a) construct or find a
contour where median > mean but the median rescale hurts (counterexample hunt);
(b) prove the implementation contains per-item patches or hardcodes;
(c) verify the fixture crew's blindness (no rule leakage into selection);
(d) verify determinism independently; (e) verify the dev-gate tables were
reproduced honestly. A kill on held-out data is a kill of the candidate.

## 9. Commit

Prereg committed first (this file). Results commit: source files, battery logs,
WAV SHA manifest, waveform analysis, red-team report, verdict —
`docs/lab/audio_longhorizon/desynth/round4_2026-09-27/`, branch `tnn-native-lab`.
No binaries, no caches, no WAVs in the repo (SHAs only).
