# PLANNER_DESIGN — unified planner/vocabulary (Phase B-F1)

Micah order 2026-09-26 ~09:27 PDT: "do the next steps — planner/vocabulary.
TNN is a unified system, not a separated bridging system."

## 1. The failure being answered

B2b §2c closed-loop on real material FAILED (VERDICT.md 2026-09-26):
ERR(3)/ERR(0) = 0.965 (fresh) / 0.944 (deep) vs bar ≤ 0.80; 10/20 and 13/20
improve vs bar ≥ 16/20. White-box bearing: **planner/representation** — the
loop DOES attempt correction, but the 5-action renderer cannot express
high-CV references. Measured ceilings:

- The vibrato depth clamp (baked-in `vib > 0.5 → 0.5`, ANOM-004) caps render
  CV at ≈0.35. Loop refs need CV up to **1.07** (native cv_pm=1066, depth 18).
- Pure sine FM caps at CV ≈ 0.707 no matter the depth (arcsine distribution);
  beyond depth 1.0 the instantaneous frequency goes negative (phase reversal).
- Secondary failures: F0 destabilization (d3: 0.021→0.034, d16: 0.150→0.711 —
  the loop "corrects" already-good plans), sawtooth (6 fresh / 4 deep cases —
  full-step corrections overshoot), low-F0 actuator unreliability (d19/d20
  stuck at ERR 0.500).

## 2. Unification — one system, not a bridge

Micah's load-bearing constraint: NATIVE and UNIFIED. The design:

- **One binary** (`plan`): assembled exactly like the wiring/ctrl binaries
  (frozen organ.zag + low-F0 guard f0low.zag + plan_main.zag, pinned znc).
  No second process, no sidecar, no adapter, no module boundary.
- **One deliberation state**: the planner turn runs INSIDE the same main loop
  as hearing and rendering. It reads the same bytes (reference WAVs through
  the same frozen organ+guard; its own probe WAVs through the same
  organ+guard), journals into the same state (the same journal file; the same
  HEARD/CONSULTED/PLANNED/RENDERED/ITER/DEVIATION tags, extended with
  CAL/DELIBERATED/PREDICT — all byte-compatible with the frozen scorer), and
  renders through the same WAV path.
- **One persistent memory**: the vocabulary table lives in the planner's own
  memory next to the 16-entry history ring. Vocabulary consult is the same
  kind of operation as history consult (both journaled under CONSULTED).
- **The long-memory engine, natively**: rb_longmem.zag's walk is model-file
  driven (its analysis lives in Python) and is NOT linked — that would be a
  bridge. What IS reused, reimplemented natively inside the unified renderer,
  is the v5 long-memory *mechanism*: per-period deterministic jitter redraw
  via fmix32, zero RNG (commit 3bcd2dcdb95f: "jitter PMF from matched-filter
  period measurement redrawn every cycle via deterministic fmix32"). It is a
  grown action candidate (H3), measured and selected like the rest — not a
  bolted-on module.

## 3. What is fixed vs what is grown

FIXED (the deliberative method — the substrate, like the organ itself; these
are inference rules, not action limits):
- R1 SELF-CALIBRATION. Before planning, the planner measures its own
  actuators natively: renders probe tones through its own renderer, hears
  them through its own organ+guard, records (param → heard quantity) curves.
  No frozen gain constant. No clamp constant anywhere in code.
- R2 COVERAGE CONSULT. For a case's measured need, consult the vocabulary:
  actions whose MEASURED probe range covers the need; select by argmin
  PREDICTED native ERR computed from each action's measured curves.
- R3 GROWTH ON COVERAGE FAILURE. If no known action's measured range covers
  the need, grow: render candidate probes (hypotheses about how to express
  the need), hear them, measure yield/bias, install the argmin-predicted-ERR
  candidate as a new action, journal DELIBERATED with every candidate's
  numbers and the reason. If no candidate covers the need, journal the
  unexpressible FINDING and use the best available.
- R4 PREDICT-BEFORE-CORRECT. Each loop iteration predicts the next render's
  heard quantities and native ERR from the action's measured curves
  (including the measured F0-hearing bias). A correction is applied ONLY if
  predicted ERR < measured ERR (strict). Otherwise the component is held,
  with the reason journaled. This replaces both the blind full-step
  correction (sawtooth source) and the correct-when-already-good behavior
  (d3/d16 destabilization).
- R5 DAMP ON MEASURED OVERSHOOT. If iteration k's deviation reverses
  iteration k−1's on a component (a measured sign flip = overshoot), halve
  that component's correction multiplier, journaled. No floor; repeated
  halving converges to holding.
- R6 EXTRAPOLATION DISTRUST. The planner trusts interpolation within its
  measured probe range. A need beyond the largest probed parameter is a
  guess → triggers R3 growth (probe, don't guess). The measured FM tracking
  frontier (CALIB@56) gates BOTH initial plans (depth capped at the frontier,
  journaled `depth_capped_at_tracking_frontier`) and corrections (held with
  `correction-beyond-tracking-frontier`). The frontier is a measurement of
  the planner's own hearing, not a programmed clamp.
- R7 CONTOUR-MEAN CORRECTION. The contour action determines F0 through its
  shape, but its mean is a free parameter: the planner rescales the contour
  mean by the measured heard ratio (f0h/f0dr) through the same damped
  multiplier (R5) as every other correction, gated by the same R4
  predicted-strict-improvement rule. (Found 2026-09-26: contour renders came
  out +10% high with the planner holding — the mean was correctable and the
  hold rule was wrong to freeze it.)
- R8 NO-PROGRESS HOLD. If the previous iteration applied a correction and the
  measured ERR did not strictly improve, the correction model is wrong for
  this case — hold instead of drifting. (Found 2026-09-26: the amode-3 mean
  predictor is overconfident (predicts 0); the organ's F0 estimator stops
  responding to contour-mean rescaling after the first pull (+17.7% mean →
  +8.6% heard, then +8.3% mean → −0.1% heard). Without R8 the planner would
  keep rescaling toward a prediction it never reaches. Implemented in the
  loop as `corrected_last`/`prev_meas`/`force_hold`: a correction applied at
  iter k with meas(k+1) >= meas(k) forces a hold at iter k+1 with reason
  `no-progress-hold`, journaled like every other decision.)

GROWN (the vocabulary content — 100% from the planner's own measurements):
every action's form, parameters, proven range, and gain; recorded in
DELIBERATED journal lines with measured evidence and reasons.

## 4. The action substrate (fixed mechanisms; actions are grown compositions)

The renderer implements modulation PRIMITIVES (the substrate):
- sine-FM components: (rate_mhz, depth_pm), up to 2
- per-period deterministic jitter: fmix32 redraw of the period multiplier
  (triangular z from two fmix32 draws; mult = 1 + width·z), zero RNG
- piecewise-linear contour following: 16-pt median-3 guarded F0 contour
- envelope shaping: flat/rise/decay with slope_db (inherited)

An ACTION = a grown composition of primitives + measured curves. The initial
vocabulary holds ONE action, A1 = single sine FM at 5 Hz — the previous
vocabulary's form, kept explicitly as the null hypothesis ("inherited form"),
journaled as such. Everything else is grown by R3.

## 5. Growth hypotheses (the space TNN searches; SELECTION is measured)

On coverage failure the planner probes ALL of these (Micah's standing
"test both" rule — never pick by fiat):
- H1 deeper single FM at the reference's natively-measured modulation rate
  (zero-crossings of the demeaned voiced contour; 5 Hz fallback)
- H2 dual FM: a second, slower component (equal-split depth hypothesis)
- H3 per-period jitter (longmem v5 mechanism, native reimplementation)
- H4 contour following: the reference's own 16-pt median-3 guarded contour
  (offered only if ≥8/16 contour points are voiced)

Each probe is rendered at the case's f0/env, heard natively, measured
(cv_yield_pm, f0_bias_ppm, env_ok). Predicted native ERR is computed per
candidate; the argmin is installed as a new action with a DELIBERATED reason
carrying all four candidates' numbers. The winning probe's params become the
case's iter0 plan (the deliberation's test becomes the action).

## 6. Correction deliberation (per loop iteration)

From DEVIATION (df0_mhz, env_ok, dcv_pm) plus the action's measured curves:
- f0: candidate render_f0 = fcur + df0·m (m = damped multiplier); predicted
  heard f0 uses the self-cal bias table (bias_ppm vs f0 at 3 probe f0s,
  linear in depth). Correct only if predicted ERR improves (R4).
- cv: candidate param step from the action's measured gain (vib1: Δdepth;
  vib2: proportional scale of both depths; jitter: Δwidth; contour:
  mean + (contour−mean)·need/heard). Correct only if predicted ERR improves.
- env: slope from the self-cal env curve (minimum probed slope reaching the
  needed class) — no blind stepping.
- native ERR (computed natively each iteration from organ-heard quantities):
  |f0−f0ref|/f0ref [f0ref≥125] + 0.5·[env≠] + 0.5·[cv outside ±25%].
  The planner optimizes what its own senses measure; the frozen scorer judges
  independently. Any organ/scorer gap (cf. ANOM-005) shows up honestly as
  PREDICT-vs-measured divergence.

## 7. Journal (scorer-compatible extensions)

Kept byte-compatible: TARGET / HEARD / CONSULTED / PLANNED / RENDERED /
ITER n PLANNED / ITER n RENDERED / ITER n DEVIATION (adds native `err=` key;
the frozen scorer's parser tolerates extra keys).
New: CAL / CALHEARD (self-calibration probes), DELIBERATED (growth reasons +
evidence numbers + damp/hold notes), PREDICT (predicted next-render
quantities + ERR). HEARD gains `crate_mhz` (measured modulation rate) and
the 16-pt contour lives in the D arena (not journaled per-point; the
contour-following renders are the evidence).

## 8. What "grown" must show in the verdict

- The vocabulary table as grown (VOCAB.md): each action, its measured
  curves, and the DELIBERATED reason for its addition.
- Closed-loop numbers on the same 20 real refs (fresh + deep state):
  ERR(3)/ERR(0) vs ≤0.80, ≥16/20 improve, Wilcoxon p<0.01, sign agreement.
- Honest accounting: if the loop still fails, the white-box reason from the
  deliberation (what it concluded it still can't express) — brief §4.
- 2× byte-identical reruns (canonical journals + WAV SHAs), zero RNG.
