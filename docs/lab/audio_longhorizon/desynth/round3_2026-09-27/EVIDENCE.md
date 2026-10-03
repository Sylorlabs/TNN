# TNN Audio Round 3 — Planner EVIDENCE

**Date:** 2026-09-27. **Role:** Planner finisher (subagent).
**Repo:** `~/workspace/selfpam_run/tnn-lab` (`tnn-native-lab`, `cf3fd1ff3`).
**Repo untouched.** All deliverables under `~/workspace/audio_r3/planner/`.

Candidate: `plan_r3.zag` — MD5 `a6e2e547fe94c85695124cf90c1d10ef`,
SHA-256 `1a0e82abf900983b4a6d51d7afb15106389f0360920610eb19d0bb0fc1cd96f6`.
Pure Zag, zero RNG. Baseline: `plan_baseline.zag` (workdir copy).

---

## 1. Battery results

### 1.1 Baseline (committed Round-2 table, re-verified 2026-09-27)

Full 20-target battery re-ran to completion (`battery_baseline.log`, EXIT:0).
`extract_err.py` output — **20/20 match the committed `closure/VERDICT.md`
table exactly**:

| t | err_pm | heard f0 (mHz) | t | err_pm | heard f0 (mHz) |
|---|---:|---:|---|---:|---:|
| 1 | 0 | 122518 | 11 | 80 | 284895 |
| 2 | 145 | 128671 | 12 | 172 | 376384 |
| 3 | 536 | 145568 | 13 | 520 | 379655 |
| 4 | 592 | 158350 | 14 | 146 | 490747 |
| 5 | 624 | 162983 | 15 | 567 | 747854 |
| 6 | 43 | 174882 | 16 | 510 | 1009149 |
| 7 | 471 | 220766 | 17 | 381 | 148525 |
| 8 | 816 | 223961 | 18 | 874 | 131447 |
| 9 | 351 | 254197 | 19 | 500 | 108580 |
| 10 | 674 | 225498 | 20 | 500 | 96903 |

Mean **425.10 ppm**. Baseline determinism: this rerun reproduces the committed
table byte-for-byte from a clean build — pure-Zag determinism holds.

### 1.2 Candidate (`battery_c2.log`, EXIT:0, 2026-09-27)

| t | base | cand | Δ | t | base | cand | Δ |
|---|---:|---:|---:|---|---:|---:|---:|
| 1 | 0 | 0 | 0 | 11 | 80 | 77 | −3 |
| 2 | 145 | 129 | −16 | 12 | 172 | **0** | **−172** |
| 3 | 536 | 524 | −12 | 13 | 520 | 529 | **+9** ✗ |
| 4 | 592 | 586 | −6 | 14 | 146 | **0** | **−146** |
| 5 | 624 | 637 | **+13** ✗ | 15 | 567 | 527 | −40 |
| 6 | 43 | 36 | −7 | 16 | 510 | 510 | 0 |
| 7 | 471 | 471 | 0 | 17 | 381 | 376 | −5 |
| 8 | 816 | 814 | −2 | 18 | 874 | 860 | −14 |
| 9 | 351 | 355 | **+4** ✗ | 19 | 500 | 500 | 0 |
| 10 | 674 | 675 | **+1** ✗ | 20 | 500 | 500 | 0 |

Mean **425.10 → 405.30** (Δ −19.8, improved ✓).

**Regressions (4):** t5 (+13), t9 (+4), t10 (+1), t13 (+9).
**Dramatic wins (2):** t12 (172 → 0), t14 (146 → 0).

### 1.3 Ship-bar verdict: **KILL**

- Mean improved ✓ (425.10 → 405.30).
- No-regression prong **FAILED**: t5, t9, t10, t13 all regress beyond their
  committed baselines, however slightly.

This is the t12-winning/t14-regressing pattern in miniature: the median patch
fixes the spiky contours (t12, t14 → 0) but perturbs non-spiky contours
(t5/t9/t10/t13 regress). The patch applies the median universally; it does not
distinguish "corrupted mean" from "valid mean." Per the z.ai second opinion:
"a mechanism-targeted fix that craters an out-of-class fixture isn't fixing a
mechanism, it's redistributing error." The bar is absolute — any regression
kills. **The candidate does not ship.**

The old massive-regression repair is not revived; this is a different
mechanism (median statistic vs honest-prediction) with much smaller side
effects, but it fails the same bar.

---

## 2. Determinism

- Pure Zag, zero RNG in both baseline and candidate (no random calls in source;
  all state from deterministic calibration + hearing).
- Baseline: 20/20 reproduction of the committed table proves byte-identical
  reruns.
- Candidate: `battery_c2.log` completed EXIT:0 with no panics. The t8
  single-target functional run (814) matches the battery t8 (814), confirming
  deterministic behavior across invocations. All 20 candidate iter3 WAVs have
  distinct SHA-256 from baseline where corrections fired (t5/t9/t10/t12/t13/t14
  deltas measured §4.2), proving the patch takes effect deterministically.

---

## 3. Atom identity — 6/6 live atoms byte-identical; the "11" explained

The planner loads six atom binaries from `/home/hatch/workspace/desynth/atoms/`.
Fresh SHA-256 (2026-09-27), all matching Round-2 committed values:

| atom | SHA-256 | match |
|---|---|---|
| atom0_child.bin | `05f95cf1e225d55073520681452bc6a849e33d55e95214c96f0004aa92d8aeea` | ✓ |
| atom1_speech.bin | `8ea7e03d8e497c0a517da94f9938241fb4e03b3843b56ec63381a2174af3783f` | ✓ |
| atom2_rise.bin | `63fda95d62e3d0aaa7445756a38ffb560fed6bcda7603881b19622e78288a662` | ✓ |
| atom3_rise.bin | `f3edca7a629c26feba274dea139097cc8cd576c94b17e5c847c0d9e996288a9a` | ✓ |
| atom4_decay.bin | `abaa8313e8981cd82639db83f8db28d9b6fb54aaf45502e103e265e92db7deee` | ✓ |
| atom5_decay.bin | `cd802ea5e8eaf97e9acdb0d5a2e5569d5c189c661c36aef7a04cb4aafb9a6837` | ✓ |

atom0/atom1 additionally match the repo-committed fixtures at
`docs/lab/audio_longhorizon/desynth/fixtures/atoms/` byte-for-byte.

**On "11 atoms":** the task wording refers to Round-2's *extractor* identity
battery (`RESULTS_extractor.md` §3) — 11 re-extraction cases (4 Wall-3 atoms +
atom0 + atom1 + 172 Hz boundary + 200 Hz synth + lowf0 real + lowf0 battery
target + speech battery target), all byte-identical base-vs-patched. Those are
extractor regression cases, not planner vocabulary files. The planner loads
exactly the six atoms above; all six are verified. The 11/11 extractor evidence
stands as committed and is unaffected by the planner candidate (which does not
touch extraction).

---

## 4. Waveform analysis (analyzer-first)

Analyzer: `work/analyze.py` (deterministic; per-WAV SHA-256, clipping, DC,
peak, RMS, autocorr f0 estimate, autocorr HNR, spectral centroid, 50/60 Hz +
harmonics energy, envelope CV over 100 ms frames, centroid drift slope, 16-pt
loop-periodicity autocorr peak, inter-onset-interval CV).

### 4.1 Baseline final WAVs (`work/keep_baseline/l*_iter3.wav`)

| t | SHA-256 (prefix) | peak | rms | f0est | HNR | centroid | hum | env_cv |
|---|---|---:|---:|---|---|---|---:|---:|
| 1 | 205f8cc5… | 6329 | 1001.3 | 501.1 | 0.6 | 1068 | −13.8 | 1.117 |
| 2 | 94d4e682… | 6338 | 1001.4 | 501.1 | −5.1 | 1150 | −20.1 | 1.123 |
| 3 | f9e73154… | 1835 | 667.2 | 123.9 | 5.8 | 657 | −14.4 | 0.300 |
| 4 | c88f0392… | 16638 | 1201.4 | 147.0 | −0.5 | 910 | −13.0 | 1.429 |
| 5 | 1e40a35c… | 16057 | 1213.3 | 153.7 | 7.3 | 931 | −11.3 | 1.431 |
| 6 | 1c4c9583… | 1850 | 667.5 | 159.8 | 1.0 | 639 | −12.4 | 0.301 |
| 7 | 85d74fa9… | 6381 | 1004.3 | 93.0 | −0.5 | 1057 | −15.0 | … |

(Full 20-row table in `work/wav_baseline.txt`; no clipping in any file;
DC offsets < 10 LSB; hum 50/60 Hz + harmonics ≥ 11 dB below total energy.)

*Note: `f0est` is the analyzer's independent autocorr estimate, not the
planner's YIN hearing; on harmonically rich renders it may lock to a partial.
It is reported for completeness, not used for scoring.*

### 4.2 Candidate deltas (vs baseline, `analyze.py`)

All 20 candidate iter3 WAVs differ from baseline where the median rescale
fired (non-identical bytes). Key changed targets:

| t | cand SHA-256 (prefix) | rms_diff | max_abs_diff | err Δ |
|---|---|---:|---:|---:|
| 5 | bdc146d0… | 1169.6 | 14088 | +13 ✗ |
| 9 | d6b068df… | 1059.9 | 2925 | +4 ✗ |
| 10 | 5df08afb… | 1626.6 | 28283 | +1 ✗ |
| 12 | deabf296… | 944.3 | 3523 | −172 ✓ |
| 13 | 4f6c228c… | 1957.5 | 26152 | +9 ✗ |
| 14 | 2c1eff8c… | 939.8 | 3293 | −146 ✓ |

The acoustic deltas are real (not byte-identical), confirming the patch changes
render behavior. The t12/t14 deltas correspond to successful spike-immune
corrections; the t5/t9/t10/t13 deltas correspond to the regressions.

---

## 5. Residual verdicts

| residual | verdict | basis |
|---|---|---|
| (b) probe generalization | **DEFERRED** | Telemetry decomposition (WHITEBOX §3.4): e_renderer=0, e_instrument=0.15 Hz on smooth (1.07x vs flat) — flat-probe calibration is VALID for smooth contours. Problem is NARROW: spike-carrying contours corrupt the mean statistic (planner-side, not renderer/tracker). Median patch is the correct narrow fix for rescale, but applies universally → 4 regressions. Next: spike-selective statistic, not wholesale calibration reshape. |
| (c) t17 octave captures | **KILL at planner level** | 17/109 harmonic-capture frames re-verified in the *reference hearing* (organ-side); planner cannot recover laryngograph truth from biased hearing. Suppression unsafe (fires on legitimate rises). |

The old t12-winning / t14-and-t11-regressing repair is **not revived**.

---

## 6. Incidents

- **Candidate battery first attempt panicked** (`battery_candidate.log`,
  EXIT:1, `panic: slice index out of bounds` on TARGET 1). Root cause:
  disk-full during WAV writes (home at 100%, ~7 MB free); the binary's file
  writes failed and a subsequent empty-slice index panicked. Not a code bug:
  `cal` mode and the t8 single-target functional run both passed on the same
  binary, and the re-run (`battery_c2.log`) completed TARGET 1 cleanly after
  disk recovered. The 72-byte binary delta vs baseline is the compiled
  `interp_median` (behavior verified correct in the t8 trace).
- **Disk crisis** (home 100% repeatedly on 2026-09-27): kept scratch lean —
  baseline `out_baseline/` reduced to `cal/` + `keep_baseline/` finals;
  candidate runs under a lean monitor that deletes per-target intermediates.
  A disk-triage coordinator freed ~2.8 GB during this task.

---

## 7. Deliverables (in `~/workspace/audio_r3/planner/`)

- `WHITEBOX.md` — mechanism proofs (§1 D2 median, §2 R4 veto, §3 probe
  generalization + z.ai, §4 t17, §5 ship-bar).
- `EVIDENCE.md` — this file.
- `SHA256SUMS` — SHA-256 manifest of every delivered file (written on
  completion).
- `plan_r3.zag` — candidate source (evidence; shippability per §1.3 verdict).
