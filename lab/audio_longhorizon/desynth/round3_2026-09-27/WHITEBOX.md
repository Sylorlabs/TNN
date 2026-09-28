# TNN Audio Round 3 — Planner WHITEBOX

**Role:** Planner finisher (subagent). **Date:** 2026-09-27.
**Repo:** `~/workspace/selfpam_run/tnn-lab`, branch `tnn-native-lab`,
detached HEAD `cf3fd1ff3` (origin `27a4271f2`). **Repo untouched** — no commits,
no working-tree modifications by this task.
**Candidate:** `plan_r3.zag` (MD5 `a6e2e547fe94c85695124cf90c1d10ef`),
pure Zag, zero RNG. **Baseline:** `plan_baseline.zag`.

Committed Round-2 closure baseline (from `closure/VERDICT.md`, err_pm):

| t | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| err | 0 | 145 | 536 | 592 | 624 | 43 | 471 | 816 | 351 | 674 |
| t | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| err | 80 | 172 | 520 | 146 | 567 | 510 | 381 | 874 | 500 | 500 |

Mean **425 ppm**. Ship bar: mean must improve **and** no fixture may regress
beyond its committed baseline. Any t14/t11-style regression kills the candidate.

---

## 1. The D2 contour-dishonesty mechanism (PROVEN)

### 1.1 What the renderer actually plays

The planner stores each contour action as a 16-point F0 contour (`CC`, 16×i64
mHz). The renderer does **not** play 16 discrete steps. It linearly interpolates
between consecutive points across the full 2-second, 88,200-sample render:

- Sample `i` sits at fractional position `p = i × 15 / 88199` in the 16-point grid.
- Its instantaneous F0 is the linear blend of `CC[floor(p)]` and `CC[floor(p)+1]`.

The hearing organ (frozen YIN) therefore hears a *continuously moving* pitch
track, not the 16 points. Any statistic the planner computes over the 16
points is a statistic of a **different signal** than the one rendered.

### 1.2 Why the 16-point arithmetic mean lies

The 16-point contours carry extreme outliers. Two measured examples
(`interp_med.py`, direct read of planner state):

- **t8** CON: `…, 609346, …` — one point at 609 kHz (an octave-class spike from
  a YIN harmonic capture during contour extraction). Interpolated-track
  arithmetic mean: **208.1 Hz**. Interpolated-track median: **144.9 Hz**.
  YIN-heard render: **153.5 Hz**.
- **t17** CON: `…, 609346, …` — same spike class. Mean **134.5 Hz**, median
  **90.8 Hz**, heard **92.6 Hz**.

The spike occupies only ~1/15 of the interpolated time but contributes
~40–45% of the mean's mass. The median is immune: it reports the central
tendency of the *played* track.

The direction of the corruption is **not** always "spike inflates the mean":
t12 and t14 have means *below* their medians (383.2 vs 442.1; 503.8 vs 563.8)
— sparse low excursions and uneven interpolation weight pull the mean down.
The precise statement: linear interpolation over uneven/sparse contour points
makes the arithmetic mean non-representative of the organ's robust central
estimate; the sign varies by contour.

### 1.3 Five-fixture proof (measured 2026-09-27, `wb_median.py`)

Pure-Zag `plan_exp rendercon` + `plan_dump dumpcon` rendered each contour;
Python only binned the 88,200 interpolated samples analytically:

| target | YIN-heard render (Hz) | interp. median (Hz) | interp. mean (Hz) | |heard−median| | |heard−mean| |
|---|---|---|---|---|---|
| t8 | 153.5 | 144.9 | 208.1 | **5.65%** | 35.51% |
| t11 | 262.9 | 262.5 | 308.8 | **0.14%** | 17.47% |
| t12 | 442.1 | 442.1 | 383.2 | **0.00%** | 13.32% |
| t14 | 563.3 | 563.8 | 503.8 | **0.09%** | 10.57% |
| t17 | 92.6 | 90.8 | 134.5 | **1.88%** | 45.36% |

The organ reports something close to the **median of the interpolated track**,
not its arithmetic mean. This validates the *measurement diagnosis*. It does
not by itself prove a scoreboard improvement (see §2, §4).

Caveat: t8 differs by 5.65% — "the organ hears exactly the median" is too
strong. The median is the best available *planner-side* central estimator; the
organ's robust estimator is close but not identical.

---

## 2. The R4 veto — why the stage-1 patch alone is inert (PROVEN)

### 2.1 The patch

`interp_median()` (added `plan_r3.zag` lines ~60–100) analytically bins all
88,200 interpolated samples into a 20–2020 Hz histogram and returns the median.
The contour-correction block now computes:

- `med0 = interp_median(CC, fcur)` — median of the *played* track at the
  current command level.
- `fcmd = f0h × 1e6 / med0` — rescale factor from heard-target over
  median-estimated render.

Previously `fcmd` used the 16-point arithmetic mean (`fmean`), which §1 proves
is corrupted by spikes.

### 2.2 The veto

The R4 gatekeeper (unchanged) then computes the *predicted* post-correction
error from the **old statistic**:

- `fpred2 = f0h × scaled-CC2-mean / fmean` — predicted error uses the
  arithmetic mean of the scaled 16-point contour.
- Gate: hold the correction if `pred_err_pm ≥ meas_err_pm`.

The actuator and the gatekeeper now speak different statistics. For a
spike-carrying contour the mean-based prediction is *more pessimistic* than the
median-based correction warrants, so the gatekeeper vetoes corrections the
actuator computed correctly.

### 2.3 Proof: t8 single-target trace (2026-09-27)

```
ITER 1 ITERHEARD f0_mhz=153548 meas_err_pm=814
DELIBERATED held reason=predicted-no-improvement action=3
    meas_err_pm=814 pred_err_pm=1044 f0-contour-mean-rescale
```

The candidate computed the median rescale (note `f0-contour-mean-rescale` —
the rescale path fired), predicted 1044 via the mean-based `fpred2`, and held
because 1044 ≥ 814. Baseline t8 = 816. Net effect on t8: **816 → 814** (noise).

**Verdict on stage-1:** the patch is mechanism-correct at the actuator but
scoreboard-inert, because the R4 prediction path still uses the dishonest
statistic. A stage-2 (median-based `fpred2`) is the coherent completion, but it
changes the gatekeeper's behavior on all 20 fixtures and must face the full
ship bar on its own — it is **not** smuggled into this candidate.

---

## 3. Residual (b): probe generalization — the complete mechanism

Round-2 §2: flat-probe calibration makes dishonest predictions on moving
contours. The previous "honest prediction" repair (mean 425 → 380.5, t8
816 → 500, t12 172 → 0) regressed t14 (146 → 513) and t11 (80 → 588) and must
not ship.

### 3.1 Why flat probes lie about contours

Calibration renders each atom **flat** (constant F0) at 90/220/1010 Hz and
measures the organ's bias (`bias220_ppm` etc.). The planner then predicts a
contour action's heard F0 by applying the flat-measured bias to the contour's
command level. But:

1. The organ's bias is **F0-dependent** (bias90 ≠ bias220 ≠ bias1010; e.g. t8
   calibration shows bias220_ppm=2054 vs bias90_ppm=13677).
2. A moving contour dwells at many F0 levels; a single flat bias cannot
   represent the track.
3. The candidate-selection predictions (`pred_err_pm=500/1000` constants for
   contour candidates) and the open-loop `PREDICT` are computed in
   flat-calibrated space, then compared against moving-contour measurements.

### 3.2 What the candidate does and does not address

The median patch corrects the *rescale denominator* (command → predicted
render level). It does **not** touch:

- Candidate selection: contour candidates still carry `pred_err_pm=500/0`
  constants derived from flat-probe yields.
- The open-loop PREDICT (iter-0 `errpred0`).
- The R4 `fpred2` (see §2).

So even if the battery shows a mean improvement, residual (b) is **not closed**
by this candidate: the selection and prediction paths remain contour-dishonest.
A genuine fix requires contour-class calibration (measuring bias on moving
contours, not flat probes) or prediction in measured space — both are
larger, separately-validated work.

### 3.3 Second opinion (z.ai, `audio-r3-q1.answer.txt`, 2026-09-27)

An independent review of the "honest prediction" line reached a harsher
verdict that applies to this candidate's scope as well:

- **Wrong layer, and worse, wrong object.** Flat-probe calibration is a
  pointwise map (requested → actual per atom); the renderer under a moving
  contour is a *stateful system* — realized F0 depends on phase-accumulator
  history, resonator state, envelope state. It is a functional, not a
  function. Changing the planner's confidence in a mis-shaped model does not
  reshape it.
- **Smoking gun:** t11 was never in the diagnosed mechanism class (t8/t12/t14)
  yet regressed 80 → 588. A mechanism-targeted fix that craters an
  out-of-class fixture is redistributing error, not fixing a mechanism.
- **The entanglement ignored:** "measured probe bias" is measured *through
  YIN* over a rendered WAV, and YIN's period estimate is itself
  contour-dependent — part of the "bias" may be the tracker, not the renderer.
- **Process:** the 425 → 380.5 mean passed a gate while two fixtures cratered —
  a regression gate is required for acceptance (this task's ship bar implements
  exactly that).

Three broad mechanisms proposed, ordered M3 first (weakest assumptions):
- **M1** — contour-conditioned calibration (bias as a smooth operator over
  contour parameters θ; kill if not grid-spannable).
- **M2** — inverse control in renderer-native space (learn "what to request so
  the output is Y"; kill if LSB sweeps show dead zones).
- **M3** — closed-loop replan: render → measure → residual in measured space →
  fixed correction iteration, retiring open-loop calibration as the sole
  mechanism. M3 absorbs tracker bias rather than fighting it.
- **Distinguishing experiment first:** telemetry decomposition — instrument the
  (deterministic, owned) renderer to log internal realized F0 at full
  precision; decompose `e_renderer = f_int − f_req` vs
  `e_instrument = f_yin − f_int`. If the tracker dominates, fix the probe
  before any calibration work.

This candidate implements none of M1/M2/M3. Its scope is strictly the §1/§2
statistic repair. The telemetry results in §3.4 refine the z.ai hypothesis.

### 3.4 Telemetry decomposition (2026-09-27) — measurement-earned verdict

The authorized experiment ran: 11 canonical contours (1 flat, ±glides at 3
rates, vibrato 2 depths × 2 rates) rendered via `plan_exp rendercon`, Python
YIN per-frame (169 frames/contour), analytical f_req(t) from the known
interpolation.

**Pre-registered decision rule:** if ∫|e_renderer| < 20% of total → instrument
dominates; if renderer dominates → transfer failure; both material →
measurement first.

**Results:**

| contour class | mean |e| (Hz) | frames | ratio vs flat |
|---|---|---|---|
| flat 220 Hz | 0.15 | 169 | 1.00x |
| 10 smooth moving | 0.16 | 1690 | 1.07x |
| spiky (t8-like, non-spike frames) | 0.59 | 109 | 3.93x |

**Decomposition:**
- **e_renderer = 0** by construction (wavetable: `phase += NBINS/Tt`, exact;
  verified by code inspection; flat render confirms).
- **e_instrument (smooth)** = 0.15 Hz — negligible. The tracker is NOT
  contour-dependent on smooth glides/vibrato.
- **e_instrument (spiky)** = 0.59 Hz — small. YIN handles the contour fine
  outside the spike instant.

**Refinement of the z.ai hypothesis:** the "contour-dependent" problem is NOT
general smooth-contour tracker bias (telemetry disproves this: 1.07x ratio).
It is SPECIFICALLY the spike-carrying contours, where the 16-pt arithmetic
mean (208 Hz) is corrupted by a 609 kHz outlier while the true track median
is ~145 Hz. This is a **planner statistic problem**, not a renderer or tracker
problem.

**Implications for residual (b):**
- Flat-probe calibration is VALID for smooth contours (0.15 Hz proves it).
- The median patch is the correct NARROW fix for the spike-corrupted rescale.
- But the patch applies universally, causing the 4 small regressions.
- **Verdict remains DEFERRED** — the mechanism is now precisely measured
  (not a vague "wrong object"), the next step is a spike-selective statistic
  (not a wholesale calibration reshape), but no ship-safe repair is validated.

An independent review of the "honest prediction" line reached a harsher
verdict that applies to this candidate's scope as well:

- **Wrong layer, and worse, wrong object.** Flat-probe calibration is a
  pointwise map (requested → actual per atom); the renderer under a moving
  contour is a *stateful system* — realized F0 depends on phase-accumulator
  history, resonator state, envelope state. It is a functional, not a
  function. Changing the planner's confidence in a mis-shaped model does not
  reshape it.
- **Smoking gun:** t11 was never in the diagnosed mechanism class (t8/t12/t14)
  yet regressed 80 → 588. A mechanism-targeted fix that craters an
  out-of-class fixture is redistributing error, not fixing a mechanism.
- **The entanglement ignored:** "measured probe bias" is measured *through
  YIN* over a rendered WAV, and YIN's period estimate is itself
  contour-dependent — part of the "bias" may be the tracker, not the renderer.
- **Process:** the 425 → 380.5 mean passed a gate while two fixtures cratered —
  a regression gate is required for acceptance (this task's ship bar implements
  exactly that).

Three broad mechanisms proposed, ordered M3 first (weakest assumptions):
- **M1** — contour-conditioned calibration (bias as a smooth operator over
  contour parameters θ; kill if not grid-spannable).
- **M2** — inverse control in renderer-native space (learn "what to request so
  the output is Y"; kill if LSB sweeps show dead zones).
- **M3** — closed-loop replan: render → measure → residual in measured space →
  fixed correction iteration, retiring open-loop calibration as the sole
  mechanism. M3 absorbs tracker bias rather than fighting it.
- **Distinguishing experiment first:** telemetry decomposition — instrument the
  (deterministic, owned) renderer to log internal realized F0 at full
  precision; decompose `e_renderer = f_int − f_req` vs
  `e_instrument = f_yin − f_int`. If the tracker dominates, fix the probe
  before any calibration work.

This candidate implements none of M1/M2/M3 and performs no telemetry
decomposition. Its scope is strictly the §1/§2 statistic repair. Residual (b)
verdict: **DEFERRED** — the mechanism is now precisely named (mis-shaped
calibration object + tracker entanglement), the next experiment is specified
(telemetry decomposition), but no planner-safe repair is validated in this
round.

---

## 4. Residual (c): t17 octave captures — proof verified, unfixable at planner level

Round-2 §3: 17/109 voiced frames of the t17 *reference hearing* are 3rd–9th
harmonic captures; the cross-frame suppressor fired on legitimate rises (t1).

**Independent re-verification (2026-09-27):** from `t17_ref_frames.txt`
(the frozen organ's per-frame F0 on the reference WAV):

- 214 frames total, 109 voiced, voiced median **148.525 Hz** (matches log).
- **17/109** voiced frames at 2.98×–8.25× the median (443.1–1225.0 Hz) —
  3rd–8th harmonic captures. (Round-2 said 3rd–9th; the exact upper bound
  depends on frame set; the count 17/109 reproduces exactly.)

These captures live in the **hearing of the reference**, upstream of every
planner decision. The planner's rescale numerator (`f0h`) and the score
(`err_pm`) are both computed in organ-heard space. No planner-side statistic
can recover the laryngograph truth (~130.3 Hz) from the organ's biased hearing;
fixing it requires changing the frozen organ's harmonic rejection, which is
out of planner scope.

The median patch changes the *render-side* denominator for t17 (the CON's
609 kHz spike no longer corrupts `fcmd`), which is legitimate and may move
t17's score, but it does not and cannot address the 17 harmonic-capture frames.

**Verdict: (c) remains KILL/DEFERRED at planner level — proof verified, no new
angle appeared.** A planner repair is unsafe: any suppression of harmonic
frames risks firing on legitimate rises (round-2's t1 side-effect).

---

## 5. Ship-bar battery results

**Completed 2026-09-27** (`battery_c2.log`, EXIT:0). Full table in EVIDENCE.md
§1.2.

- Mean: **425.10 → 405.30** (improved ✓).
- **KILL:** t5 (+13), t9 (+4), t10 (+1), t13 (+9) regress beyond committed
  baselines. The no-regression prong is absolute.
- Dramatic wins: t12 (172 → 0), t14 (146 → 0) — the median rescale works where
  the mean was spike-corrupted.
- t8: 816 → 814 (R4 veto held the correction, §2).

**Interpretation:** the stage-1 patch is mechanism-correct (median tracks the
organ; t12/t14 prove it) but not ship-safe: it applies the median universally,
perturbing non-spiky contours. This is error redistribution, not a mechanism
fix (z.ai §3.3). The candidate does not ship. Stage-2 (median `fpred2`) was not
attempted — it would need its own full-bar validation.

The old t12-winning/t14-and-t11-regressing repair is not revived.
