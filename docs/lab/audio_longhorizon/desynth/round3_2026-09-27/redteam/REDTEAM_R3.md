# RED TEAM REPORT — TNN Audio Round 3 (independent)

**Target commit:** `d1b943161e8ace5b8b117b3c452e866c27539e15` ("Audio round 3 (2026-09-27)")
**Date:** 2026-09-27
**Role:** Independent red team. Committed source only; path-scoped `git archive` extraction; never worker scratch.
**Deliverable:** `~/workspace/audio_r3/redteam/REDTEAM_R3.md` (this file). Not committed.

## Method

- All tested source/docs/fixtures extracted from `d1b943161e8a` via scoped `git archive`.
- MP3: committed Zag decoder rebuilt with the pinned toolchain
  (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`); Python oracle
  is the committed `mp3ref.py`. Pure Zag, zero RNG, byte-identical reruns.
- Planner: committed `plan_r3.zag` and closure baseline `plan_final_full.zag`
  rebuilt; full 20-target batteries re-run independently.
- Measurements first: HNR, spectra, envelope stationarity, spectral drift,
  loop periodicity, transient regularity, 50/60 Hz + harmonics, deltas vs
  prior, SHA-256 of every audio file. No prose-only waveform conclusions.
- Verdict labels per attack: **CONFIRMED / REFUTED / NEW FINDING**.

---

## Attack 1 — MP3 32 kHz mixed-block re-derivation

**Verdict: CONFIRMED** (strongly, on two independent fixtures).

### Committed round-3 fixture (`clicks_32k.mp3` / `clicks_32k_mx.mp3`)

- 86 frames, 44 short granules, 44 mixed granules.
- Zag vs oracle: 99,072 samples, max **1 LSB**, mean **0.000212 LSB**.
- Oracle mixed vs unflipped: max **35,802 LSB** (non-vacuous mixed path).
- Zag ×2 reruns: byte-identical.
- Zag PCM SHA-256: `e77041990243773c14789410967c4b36f0280b6621a1cd0aa91888ef55827510`.

### Independent fresh 32 kHz fixture (built by this red team)

- 330/495 Hz dyad with tremolo, logarithmic chirps, deterministic texture
  bursts; encoded MPEG-1 32 kHz / 96 kbps. Independent side-info walker flipped
  9 short granules to mixed.
- Input SHAs: unflipped
  `6dc209324497c322a7d0aaaae45135c777d28cd974f4cffd6f2c3bfa2a651527`,
  mixed `bd71fa7d173b85950733c014a27c3b3e6d0c5b1e1ff22cbbd4936cc1a1269098`.
- Zag vs oracle: 99,072 samples, max **1 LSB**, mean **0.000313 LSB**.
- Oracle mixed vs unflipped: max **51,444 LSB**.
- Zag ×2: byte-identical.
- Zag PCM SHA-256: `fbf0ab6aab9f5a61870075b8474eecf7579c5792236f68a05def3a0751fd6b6e`.

### Oracle-shift logic (formal)

- Oracle and Zag both compute
  `my_sr = sr + (((hdr[1]>>3)&1)+((hdr[1]>>4)&1))*3`.
- MPEG-1 ⇒ `my_sr ∈ {6,7,8}`. The oracle's `<<1` shift fires only at
  `my_sr==2` (MPEG-2.5, 12 kHz). No MPEG-1 input can reach it.
- Direct oracle test of the 12 kHz mixed row (`n_long_bands=4`) crashes:
  `IndexError: index 504 is out of bounds for axis 0 with size 504` — the
  path is untestable even in the reference.
- Qualification: the Zag decoder does not explicitly reject non-MPEG-1
  version bits; it applies MPEG-1 frame math regardless. Mutating one frame's
  version bits to MPEG-2.5 left Zag output byte-identical (sync/resync
  skipped the malformed frame). "my_sr is always 6/7/8" holds **for correctly
  supported MPEG-1 inputs**, not as an explicit parser invariant.

---

## Attack 2 — MP3 fixture regression (comment-only change)

**Verdict: CONFIRMED.**

| Fixture | Samples | Zag vs oracle max | mean (LSB) | Zag ×2 | Zag PCM SHA-256 |
|---|---|---|---|---|---|
| `t_128cbr` | 69,120 | 1 LSB | 0.000145 | identical | `f72aca836ff4ddc69e6a084e302302243750e0857a7bc0a36de533a8b10bb467` |
| `t_128js` | 138,240 | 1 LSB | 0.000072 | identical | `711f0f067397f1439f62f18275b88e0e25df86875936e11f27be0d65318209b0` |
| `t_vbr` | 69,120 | 1 LSB | 0.000188 | identical | `7abcd3cb239f530cbc583ff9427738f2a2276bb47a14ae885551d7be63e4c6d5` |
| `fx_mxflip_drums_all` | 359,424 | 1 LSB | 0.000106 | identical | `e05f88a213764f07251f4e0dec2bfb141899832db62b086f38ff5ca2e61c013a` |
| `fx_mxflip_drums_alt` | 359,424 | 1 LSB | 0.000095 | identical | `dee54dc830e8dac27e1f1bfc0f08d075e4f0c3e7e694abe69b7a0e74e3c5d02c` |
| `fx_mxflip_rapid_all` | 359,424 | 1 LSB | 0.000256 | identical | `4393a477266f4d8af859c577dde9edc5318dca71c752bf4602d706490ce1dc1f` |
| `fx_mxflip_rapid_alt` | 359,424 | 1 LSB | 0.000134 | identical | `98386475fe98edd07e59a74cb94f6caca6d679906b6e7b2b215035151698d5f0` |

Git diff parent `4a7b8d6ce` → target shows exactly eight added comment lines
in `mp3dec.zag`, no executable change. A rebuild with those eight lines
removed produces byte-identical PCM on all 10 tested inputs (3 standard +
4 mixed + committed 32k pair + independent 32k mixed).

---

## Attack 3 — Manifest checks

**Verdict: CONFIRMED (hashes valid) + NEW FINDING (coverage gap).**

- MP3 `MANIFEST.sha256`: all five listed files verify cleanly.
- Planner `SHA256SUMS`: all three listed files verify cleanly.
- **NEW FINDING (process):** planner `EVIDENCE.md` line 198 calls `SHA256SUMS`
  a "manifest of every delivered file," but the committed directory contains
  six files and `SHA256SUMS` lists only three (`WHITEBOX.md`, `EVIDENCE.md`,
  `plan_r3.zag`). `zai_q1_answer.txt` and `zai_q1_question.txt` are unlisted.
  The listed hashes are valid; the "every delivered file" coverage claim is
  false.

---

## Attack 4 — Atom identities

**Verdict: CONFIRMED.** All six current atoms match the committed claims:

| atom | SHA-256 |
|---|---|
| atom0 | `05f95cf1e225d55073520681452bc6a849e33d55e95214c96f0004aa92d8aeea` |
| atom1 | `8ea7e03d8e497c0a517da94f9938241fb4e03b3843b56ec63381a2174af3783f` |
| atom2 | `63fda95d62e3d0aaa7445756a38ffb560fed6bcda7603881b19622e78288a662` |
| atom3 | `f3edca7a629c26feba274dea139097cc8cd576c94b17e5c847c0d9e996288a9a` |
| atom4 | `abaa8313e8981cd82639db83f8db28d9b6fb54aaf45502e103e265e92db7deee` |
| atom5 | `cd802ea5e8eaf97e9acdb0d5a2e5569d5c189c661c36aef7a04cb4aafb9a6837` |

---

## Attack 5 — Planner battery re-derivation (independent)

**Verdict: CONFIRMED** — full 20-target batteries re-run from committed
source; every claimed score reproduced exactly, and all 13 checked WAVs
(7 baseline + 6 candidate) are byte-identical to the committed SHAs.

Final `err_pm` per target (baseline → candidate):

| t | base | cand | Δ | t | base | cand | Δ |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 0 | 0 | 11 | 80 | 77 | −3 |
| 2 | 145 | 129 | −16 | 12 | 172 | 0 | **−172** |
| 3 | 536 | 524 | −12 | 13 | 520 | 529 | **+9** ✗ |
| 4 | 592 | 586 | −6 | 14 | 146 | 0 | **−146** |
| 5 | 624 | 637 | **+13** ✗ | 15 | 567 | 527 | −40 |
| 6 | 43 | 36 | −7 | 16 | 510 | 510 | 0 |
| 7 | 471 | 471 | 0 | 17 | 381 | 376 | −5 |
| 8 | 816 | 814 | −2 | 18 | 874 | 860 | −14 |
| 9 | 351 | 355 | **+4** ✗ | 19 | 500 | 500 | 0 |
| 10 | 674 | 675 | **+1** ✗ | 20 | 500 | 500 | 0 |

Total: 8502 → 8106 (−396). The four claimed regressions (t5 +13, t9 +4,
t10 +1, t13 +9) and the two claimed wins (t12 172→0, t14 146→0) reproduce
**exactly**. Cross-run determinism: this independent run's per-target scores
match the committed battery's scores, and the WAVs are byte-identical
(SHA prefixes match on all 13 checked).

### EVIDENCE.md §4.1 spot-check (baseline WAV analyzer)

| t | peak | rms | env_cv | SHA |
|---|---|---|---|---|
| 1 | 6329 ✓ | 1001.3 ✓ | 1.159 vs 1.117 | `205f8cc5…` identical |
| 2 | 6338 ✓ | 1001.4 ✓ | 1.161 vs 1.123 | `94d4e682…` identical |
| 3 | 1835 ✓ | 667.2 ✓ | 0.327 vs 0.300 | `f9e73154…` identical |
| 4 | 16638 ✓ | 1201.4 ✓ | 1.457 vs 1.429 | `c88f0392…` identical |
| 5 | 16057 ✓ | 1213.3 ✓ | 1.452 vs 1.431 | `1e40a35c…` identical |
| 6 | 1850 ✓ | 667.5 ✓ | 0.328 vs 0.301 | `1c4c9583…` identical |
| 7 | 6381 ✓ | 1004.3 ✓ | 1.160 vs … | `85d74fa9…` identical |

(✓ = exact match. `f0est`/HNR/centroid/hum differ in details between
independent analyzer implementations; the EVIDENCE.md itself notes `f0est`
may lock to a partial on harmonically rich renders and is not used for
scoring.)

### EVIDENCE.md §4.2 spot-check (candidate deltas)

| t | cand SHA | rms_diff | max_abs_diff | err Δ |
|---|---|---|---|---|
| 5 | `bdc146d0…` identical | 1169.6 ✓ | 14088 ✓ | +13 |
| 9 | `d6b068df…` identical | 1059.9 ✓ | 2925 ✓ | +4 |
| 10 | `5df08afb…` identical | 1626.6 ✓ | 28283 ✓ | +1 |
| 12 | `deabf296…` identical | 944.3 ✓ | 3523 ✓ | −172 |
| 13 | `4f6c228c…` identical | 1957.5 ✓ | 26152 ✓ | +9 |
| 14 | `2c1eff8c…` identical | 939.8 ✓ | 3293 ✓ | −146 |

(✓ = exact match to claimed values.)

---

## Attack 6 — Adversarial variants (spike-conditional median)

**Verdict: V-A REFUTED; V-D NEW FINDING — TRAP REFUTED.**

### V-A (preregistered 5% magnitude threshold): REFUTED

Design (preregistered before full battery results): compute both the baseline
16-pt mean and the candidate interpolated median; use the median for `fcmd`
only when `|mean−median|/median > 5%`, otherwise preserve the baseline mean.
This directly tests whether a magnitude threshold isolates t12/t14.

Instrumented battery (candidate + STAT prints, verified neutral: all 20
scores identical to candidate) measured per-target disagreements:

| t | disagreement | err base→cand | t | disagreement | err base→cand |
|---|---|---|---|---|---|
| 5 | 1.2%, 1.0% | 624→637 (+13) ✗ | 12 | 14.8%, 14.6% | 172→0 (−172) ✓ |
| 9 | 89.7% | 351→355 (+4) ✗ | 13 | 1.0%, 1.1% | 520→529 (+9) ✗ |
| 10 | 26.7% | 674→675 (+1) ✗ | 14 | 12.8% | 146→0 (−146) ✓ |

**No magnitude threshold separates wins from regressions:** t9 (89.7%) and
t10 (26.7%) have HIGHER disagreement than t12 (14.8%) and t14 (12.8%), yet
the median made t9/t10 WORSE. Any T < 12.8% (to keep t12/t14 wins) also
applies the median to t9/t10 (regressions). Any T ≥ 26.7% (to avoid t9/t10
regressions) loses t12/t14 wins. **V-A is refuted.**

### Directional pattern (post-hoc observation)

The DIRECTION of the discrepancy, not its magnitude, predicts the outcome:

| t | mean | median | direction | outcome |
|---|---|---|---|---|
| 12 | 376,384 | 442,000 | median ABOVE mean (+14.8%) | WIN (−172) |
| 14 | 490,746 | 563,000 | median ABOVE mean (+12.8%) | WIN (−146) |
| 9 | 254,196 | 134,000 | median BELOW mean (−89.7%) | REGRESSION (+4) |
| 10 | 225,497 | 178,000 | median BELOW mean (−26.7%) | REGRESSION (+1) |
| 5 | 162,983 | 161,000 | median below (−1.2%) | REGRESSION (+13) |
| 13 | 379,655 | 376,000 | median below (−1.0%) | REGRESSION (+9) |

When the mean is dragged DOWN by low outliers (median > mean), the median is
the robust statistic and fixes the rescale (t12/t14). When the mean is
dragged UP (median < mean), the median locks onto a low mode while the mean
is closer to the true pitch (t9/t10) — using the median hurts.

### V-D (post-hoc directional rule): NEW FINDING — TRAP REFUTED

Rule: use `interp_median` for `fcmd` ONLY IF `median > mean`, else keep the
baseline mean. Explicitly post-hoc (designed after seeing the directional
pattern), not preregistered.

**Result: the trap is broken.** Full 20-target battery:

| t | base | V-D | Δ | t | base | V-D | Δ |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 0 | 0 | 11 | 80 | 80 | 0 |
| 2 | 145 | 145 | 0 | 12 | 172 | 0 | **−172** ✓ |
| 3 | 536 | 536 | 0 | 13 | 520 | 520 | 0 |
| 4 | 592 | 592 | 0 | 14 | 146 | 0 | **−146** ✓ |
| 5 | 624 | 624 | 0 | 15 | 567 | 567 | 0 |
| 6 | 43 | 43 | 0 | 16 | 510 | 510 | 0 |
| 7 | 471 | 471 | 0 | 17 | 381 | 381 | 0 |
| 8 | 816 | 816 | 0 | 18 | 874 | 874 | 0 |
| 9 | 351 | 351 | 0 | 19 | 500 | 500 | 0 |
| 10 | 674 | 674 | 0 | 20 | 500 | 500 | 0 |

Total: 8502 → 8184 (−318). **Zero regressions.**

Byte-identity proof:
- V-D t12/t14 iter3 WAVs are byte-identical to candidate t12/t14
  (`deabf296…`, `2c1eff8c…`) — wins preserved via the identical trajectory.
- V-D t5/t9/t10/t13 iter3 WAVs are byte-identical to baseline — regressions
  eliminated by preserving the baseline mean.
- V-D matches baseline on 17/20 targets, candidate on 3/20 (t12, t14, t16).

**Interpretation:** The report's "trap still holds" conclusion is refuted.
A simple, principled directional rule — use the median only when the mean is
dragged down by low outliers (median > mean), otherwise trust the mean —
isolates the t12/t14 spike wins with zero regressions. The candidate's
failure was not that the median is wrong, but that it applied the median
unconditionally. The median is the right statistic when the corruption is
downward (low dips); the mean is safer when the median would lock onto a low
mode (t9/t10).

Caveats: V-D is post-hoc (not preregistered); it forgoes the candidate's
smaller improvements on t2/t3/t4/t6/t8/t11/t15/t17/t18 (it matches baseline
there); it was tested on the same 20-target battery used to discover the
pattern (no held-out validation). It is a red-team existence proof that the
trap is not fundamental, not a shipped fix.

---

## Attack 7 — Telemetry decomposition (independent re-derivation)

**Verdict: CONFIRMED** (independent YIN, independent contour set, committed
renderer via a `rendercon` harness added to a COPY of `plan_r3.zag`).

- `e_renderer = 0` by construction, verified by code inspection of the
  committed `render_plan`: per-sample `f0t` is the analytic linear
  interpolation of the 16-pt contour, and phase advances by
  `NBINS·f0t/sr` — the realized instantaneous F0 **is** `f0t`.
- `e_instrument` measured with a fresh, independently written YIN
  (rectangular window; validated unbiased: +0.001 Hz on synthetic 220 Hz
  harmonic stack; the Hanning-windowed variant showed +0.49 Hz systematic
  bias and was discarded) on 11 contours DIFFERENT from the round-3 canonical
  11 (flat 220/440, glides 200→400 / 500→250 / 200→800 / 300→320,
  vibrato 220±10@5Hz / 440±30@7Hz, spike_hi, spike_lo, stepped):

| contour | mean\|e\| (Hz) | contour | mean\|e\| (Hz) |
|---|---|---|---|
| flat220 | 0.154 | vibrato_a | 0.180 |
| flat440 | 0.230 | vibrato_b | 0.231 |
| glide_up | 0.239 | spike_hi | 0.663 |
| glide_down | 0.255 | spike_lo | 0.684 |
| fast_glide | 0.449 | stepped | 2.491 |
| slow_glide | 0.220 | | |

- Smooth class: 0.26 Hz mean|e| (theirs: 0.16 Hz on their 10 smooth).
  flat220 = 0.154 Hz reproduces their 0.15 Hz flat claim almost exactly.
- Spiky class: 0.67 Hz (theirs: 0.59 Hz), with 11–12/169 frames unscored
  (YIN loses lock at the spike instant).
- Scale comparison (the decisive point): t12's baseline error is 172 ppm at
  376 Hz ≈ **65 Hz absolute** — ~250× the tracker error. The tracker cannot
  explain the planner's errors; the planner's mean-vs-median discrepancy on
  t12 (383.2 vs 442.1 Hz = 58.9 Hz) matches the observed error scale. The
  problem is narrowly the spike-carrying contours corrupting the planner's
  mean statistic, not the renderer or the tracker.
- Nuance: fast_glide (300 Hz/s) shows 0.449 Hz — very fast glides stress the
  tracker slightly, but still ~100× below planner error scale. The
  "flat-probe calibration is valid for smooth contours" claim holds in the
  sense that smooth-contour tracker error stays at the flat-probe bias level
  rather than growing with contour movement.

---

## Attack 8 — Waveform audit (measurement-first)

**Verdict: CONFIRMED** (no anomalous artifacts; §4.1/§4.2 spot-checks pass
exactly — see Attack 5).

MP3 PCM audit (all 11 decoder outputs): comment/no-comment pairs
byte-identical; mixed fixtures show strong deltas vs unflipped (rms 4494 vs
2228 on 32k); hum 50/60 Hz + harmonics ≤ −16 dB everywhere; no clipping
beyond the source material's own peaks.

---

## Attack 9 — Huffman / pow_43 exercise

**Verdict: CONFIRMED** (linbits claim), with a precision footnote.

- Instrumented the committed oracle (exact loop copy + coverage counters) and
  decoded all 9 committed fixtures: **30/32 Huffman tables exercised**.
  Tables 4 and 14 never fire.
- **All 16 linbits tables (16–31) had the escape path fire** — the EVIDENCE.md
  §5 claim ("mixed fixtures use Huffman tables across all 16 linbits
  tables") is confirmed. Small widths achieved 100% of possible escape
  values (tables 16,17,18,19,24,25); large widths substantial partial
  coverage (table 31: 1351/8192).
- `pow_43_z`: exact Python port of the committed Zag function vs strict
  pure-Python `x**(4/3)` over the full reachable domain 0..8206: max relative
  error **1.325e-06 at x=132**, matching the claimed 1.32e-6.
- Footnote: if any committed text claims "every Huffman table" without
  qualification, that phrasing overstates by 2 tables (4, 14).

---

## Attack 10 — Close-call hunt (mixed-block n_long_bands)

**Verdict: REFUTED** (no counterexample; the hardcoded 2 is exactly right).

Exhaustive check over all 8 mixed rows: table-derived `n_long_bands` =
sum(first 8 widths)/18.

| row | version/rate | Σ first 8 | derived | hardcoded |
|---|---|---|---|---|
| 5 | MPEG-1 48 kHz | 36 | 2.0 | 2 ✓ |
| 6 | MPEG-1 44.1 kHz | 36 | 2.0 | 2 ✓ |
| 7 | MPEG-1 32 kHz | 36 | 2.0 | 2 ✓ |

All three MPEG-1 rows derive exactly 2. Non-MPEG-1 rows diverge (different
standards), but the decoder is MPEG-1-only and the oracle crashes on the
12 kHz row — no valid-input divergence exists.

---

## Overall judgment

**The round-3 evidence HOLDS on every technical claim, but the "trap still
holds" conclusion is REFUTED by a red-team variant.**

What holds (independently reproduced from committed source):
- MP3 32 kHz mixed-block decode: bit-exact vs oracle (1 LSB max) on two
  fixtures; the `my_sr` shift analysis is correct; the hardcoded
  `n_long_bands=2` is exactly right for all MPEG-1 rows.
- Comment-only change: verified (8 comment lines, byte-identical output).
- Planner battery: all 20 scores reproduced exactly; 13/13 WAVs byte-identical
  to committed SHAs; §4.1/§4.2 analyzer values match exactly.
- Telemetry: independent YIN + independent contours confirm the tracker is
  ~250× too accurate to explain planner errors; the problem is narrowly the
  spike-corrupted mean statistic.
- Huffman: all 16 linbits tables exercised (escape paths fired); pow_43_z
  1.325e-6 confirmed.
- Manifests: all listed hashes valid.

What is new:
1. **Planner manifest coverage gap:** `SHA256SUMS` claims "every delivered
   file" but omits `zai_q1_answer.txt` and `zai_q1_question.txt`. (Process.)
2. **V-A refuted:** No magnitude threshold on `|mean−median|/median` separates
   wins from regressions (t9/t10 disagree MORE than t12/t14 yet regress).
3. **V-D refutes the trap:** A post-hoc directional rule (median iff
   median > mean) keeps t12/t14 at zero with zero regressions (total −318,
   byte-identical trajectories). The candidate's error was unconditional
   median application, not the median itself.

The round-3 team correctly killed their candidate under their
absolute-no-regression bar. This red team shows the bar was achievable: the
trap was in the unconditional application, not the mechanism. V-D is an
existence proof, not a validated fix (post-hoc, no held-out test).

---

## Limitations and open items

- The instrumented/variant batteries each cost ~40 min on this 2-core box;
  Attack 6 results follow.
- The `rendercon` harness, instrumented printer, and variant are RED-TEAM
  tools built from copies of committed source; they are not committed and
  do not affect the verdict on the committed code.
- Telemetry contour renders used atom0-contour (amode=2); timbre does not
  affect the tracker-error conclusions.
- `/tmp` was avoided throughout (shared tmpfs); all scratch under
  `~/workspace/audio_r3/redteam/`.

## Reproduction commands

```bash
# MP3 decoder build + 32k re-derivation
cd ~/workspace/audio_r3/redteam/work/mp3src/docs/lab/universal_intake/mp3/zag_full
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 mp3dec.zag -o ~/workspace/audio_r3/redteam/bin/mp3dec
# Planner batteries
cd ~/workspace/audio_r3/redteam
bin/plan_baseline batch targets.txt planout/base_full
bin/plan_r3 batch targets.txt planout/cand_full
# Telemetry
cd work/telemetry && python3 gen_contours.py && python3 telemetry.py
# Huffman coverage
cd work && python3 huffcov.py
# Waveform audit
cd ~/workspace/audio_r3/redteam && python3 work/waveaudit.py <files...>
```
