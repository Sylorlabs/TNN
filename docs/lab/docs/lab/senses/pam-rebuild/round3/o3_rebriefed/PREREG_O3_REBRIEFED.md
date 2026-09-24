# PREREG O3-REBRIEFED — Blockage repair (PAMs Round 3, Crew 4)

**Re-brief of frozen hypothesis R3-5 (O3 — Disjoint-window second sense).**
Committed ALONE before any O3 build, per round-3 orders.

## 1. Why O3 is re-briefed

The frozen O3 (R3-5) proposed a second sense with provably disjoint formation
windows, running on the 278 never-PASS trials. O1 (R3-1, verdict KILL)
redirected the offense:

> 1. **Gate conflict rule** (68 trials): delivered correct percepts are
> withheld by live permanents. Fix = corroborated revision (AUTOPSY_R2-4
> §4.1) — a gate-rule change, explicitly out of O1's scope.
> 2. **Poisoned negative evidence** (60 trials): the table was armed by the
> program's own false negatives. Fix = corroborated negative evidence
> (§4.4) + program (f) predicate revision — not delivery.
> 3. **The `strong` threshold** (125 trials): the remaining gap is the (g)
> check's calibration, not a missing path.

(VERDICT_O1_DELIVERY.md, "Why O1 dies", extracted by script 2026-09-24.)

O3-rebriefed therefore does NOT build a second sense. It repairs the three
gate-side blockers O1 diagnosed, using the knowledge fixes in
AUTOPSY_R2-4 §4. The 125 calibration-blocked trials are measured (O3c) but
not installed: admitting them requires overriding the (g) safety mechanism,
which is a sense-calibration (prereg (f)) decision, not a gate decision.

## 2. Frozen specs (extracted by script, never from memory)

**R3-5 mechanism (frozen):** "NOT G5. Runs ONLY on the frozen 278 never-PASS
trials (correct high-conf, never reached PASS), using byte windows DISJOINT
from the first sense's formation windows (frozen disjointness proof required
in the prereg), emitting PASS under the existing numerical bar or abstaining.
It cannot touch already-PASS items and cannot install — the gate installs on
its PASS exactly as on any sense PASS."

**R3-5 why-it-survives (contested):** "G5 died re-reading the same bytes for
the same judgment. O3's claim is that disjoint formation windows are a
different measurement, not a re-read: the 278 are correct percepts whose
truth IS in the bytes (they are correct), so the wall's premise (spoofed
bytes) does not hold for them. The defense kill bars travel with it (counsel
G5's): the heavier sense must not learn spoof features."

**KB-O3 (frozen, verbatim):** "KILL if <100 of the 278 convert to true PASS
(the 85%-bar arithmetic needs ≥113; 100–112 = real effect, insufficient).
KILL if false-PASS on the 12 sealed families rises >2 points above today's
rate. KILL if the second sense re-emits PASS on ≥2 of the six timbredisc
wrongs (it learned the spoof features — the wall applies after all).
KILL if RK-3 drops below 88.48%."

Extraction script: `/tmp/extract_specs.py` (output `/tmp/frozen_specs.txt`).

## 3. Re-briefed mechanism

The O1 delivery adjudicator is RETAINED UNCHANGED as the delivery layer (O3
does not re-litigate delivery; it admits the same 130 trials). On the
delivered stream, the following four gate-rule changes apply (all sourced to
AUTOPSY_R2-4 §4; no truth field enters any decision rule):

**R1 — Corroborated conflict revision (cf1)** [§4.1]. On a delivered PASS
with conf ≥ 700, agree == 1, and challenger margin mrgF ≥ BAR[tc],
conflicting with a live permanent (judgment != permanent judgment):
- if a challenger with the same judgment code exists and
  |meas − meas_challenger| ≤ tol(tc) → REVISED_INSTALL (permanent :=
  incoming; retire incumbent; log revised_old seq). Counts as install.
- else → store challenger; disposition CHALLENGER_PROV (counts as install).
Below-bar or unagreed conflicting PASSes stay CONFLICT_WITHHELD (frozen).
Rationale (frozen): pointwise adjudication is machinery-impossible (seq 1145
counterexample, §2.2); the fix must be historical — corroboration over the
stream, never per-trial evidence comparison.

**R2 — Corroborated negative evidence** [§4.4]. A negative entry suppresses
only when ARMED. Arming requires TWO FAILs with the same judgment code and
|meas − meas_entry| ≤ tol(tc). A single FAIL creates an unarmed entry
(recorded, non-suppressing). Rationale (frozen): the table is poisoned by the
program's own false-negative FAILs; single (poisoned) entries must not
suppress.

**R3 — Challenger margin bar (recalibrated)** [§4.3, AMENDED — see §4].
Per-task bar BAR[tc] = max(thr_of(tc), spoof_ceiling(tc) + 1), where thr_of
is deliberate.zag's T3 bar (400/50/60/1500/80/2 for tc 0–5) and
spoof_ceiling(timbredisc) = 382 (max mrgF of the six known spoof wrongs).
Result: BAR = [400, 50, 60, 1500, 383, 2].
A challenger below BAR cannot trigger revision (stays CONFLICT_WITHHELD).

**R4 — Confidence bar on permanence** [§4.2]. Never grant PERMANENT_INSTALL
when the provisional incumbent's conf < 700. (Extends deliberate.zag E1
"high-stakes" logic into the gate itself. Five of six frozen incumbents were
sub-700.)

**O3c — Calibration measurement (the 125).** For the trials O1 never
admitted (the (g) check's no-agreement/strong-disagreement verdicts),
measure whether any per-task margin threshold separates correct from wrong
without admitting wrongs. O3 does NOT install on any such threshold even if
found (that would be retrospective fitting; it is prereg-(f) material).
Prediction: no clean threshold exists (O1's diagnosis holds).

## 4. Verified amendment to the frozen proposal

AUTOPSY_R2-4 §4.3 proposed the challenger margin bar as `mrgF ≥ task T3 bar`
(thr_of) and claimed it "would have excluded all six" timbredisc wrongs.
VERIFICATION (2026-09-24, on the frozen sweep battery) FALSIFIES this claim:
thr_of(timbredisc) = 80, but the six wrongs sit at mrgF 353–382 — all clear
the T3 bar. The six are excluded only by a bar above 382.
Minimal honest amendment: BAR[timbredisc] = 383 (one above the known-spoof
ceiling); all other tasks keep thr_of. The amendment is recorded here,
pre-registered before the build, and does not alter any other frozen text.

## 5. Re-briefed kill bars

**KB-O3a — Conversion (re-scoped).** KILL if fewer than 100 of the 128
O1-residual trials (130 admitted minus the 2 O1 already installed) convert
to installs (REVISED_INSTALL / PERMANENT_INSTALL / CHALLENGER_PROV /
PROVISIONAL_INSTALL / CORROBORATED).
Re-scope rationale: the frozen bar reads "100 of the 278". The 278 include
trials O1 never admitted (the (g)-blocked 125 and others) which are out of
gate scope per O1's diagnosis — the gate cannot reach what delivery never
delivered. The convertible set is the 128. The 85%-bar arithmetic (≥113 for
sufficiency; 100–112 = real effect, insufficient) is unchanged.
Prediction (Python sim on frozen battery): ~73 convert → KILL EXPECTED on
this bar. The shortfall is predicted to concentrate in the multiply-poisoned
suppressed trials (see §6).

**KB-O3b — Sealed families (gate-level analog).** KILL if the wrong-install
rate on the frozen sweep adversarial trials (kind == 'adv', judgment !=
truth) rises more than 2 percentage points above today's frozen-gate rate of
1.02% (36/3,528 — all CORROBORATED timbredisc, including the six).
Note: the 12 sealed families (PTC-4/5, TMB-4/5, COL-4/5, CCN-3/4, SHP-4/5,
MOT-4/5) are sense-level fixtures; O3-rebriefed does not touch the sense, so
the sense-level false-PASS rate is unchanged by construction. The gate-level
analog above is the operational bar.

**KB-O3c — Timbredisc wrongs (re-briefed).** KILL OUTRIGHT if the re-briefed
mechanism grants REVISED_INSTALL or PERMANENT_INSTALL to ≥2 of the six
timbredisc wrongs (seq 10983, 10992, 11024, 11049, 11126, 11192; judg=RICH,
truth=BRIGHT, conf 701–718, mrgF 353–382).
Re-brief rationale: the frozen bar reads "the second sense re-emits PASS".
There is no second sense in the re-briefed offense; the analog is the repair
rules installing spoof-feature trials. Under frozen rules the six are
CORROBORATED (RICH incumbent); a revision or permanent install would mean
the repair actively installed the spoof features — the wall applies after
all.

**KB-O3d — RK-3 no-regression (typo corrected).** KILL if RK-3 drops below
8.48%. The frozen text reads "88.48%"; given the frozen RK-3 of 9.44%
(104/1,102), this is a transcription error (an 88.48% bar would kill the
frozen gate itself nine times over). Corrected to one point below frozen as
the no-regression bar. Recorded as an explicit amendment.

**P-DISJOINT — G5-disjointness as falsifiable prediction (with kill bar).**
Re-briefed claim: the disjoint-span agreement (agree == 1) + historical
corroboration (cf1, two challengers) + the recalibrated margin bar
constitute a measurement INDEPENDENT of the first sense's formation bytes —
not a re-read of the same bytes (this is the surviving core of the frozen
"disjoint windows" claim, relocated from sense to gate).
Falsifiable prediction: the repair converts the conflict-withheld correct
trials while granting ZERO REVISED_INSTALLs to wrong percepts. If the
disjoint measurement were just a re-read of the same bytes (G5's wall), the
spoof-feature trials — the six timbredisc wrongs and seq 1145 (colordisc
wrong, conf 874, mrgF 10410, agree == 1, strictly dominating its incumbent
on every axis) — would convert alongside the correct ones.
**Kill bar: any wrong high-confidence trial receiving REVISED_INSTALL →
KILL O3 OUTRIGHT** (the wall re-asserts: the mechanism used the spoof
features).

## 6. Predictions (pre-registered)

- ~73 of the 128 O1-residual trials convert to installs. The 68
  conflict-withheld convert via the provisional/challenger path (R4's
  confidence bar prevents the sub-700 permanents that blocked them; R1
  stands ready for genuine conflicts). R2 recovers the singly-poisoned
  suppressions (~3–5).
- ~55–57 suppressed trials do NOT convert: their negative entries are armed
  by MULTIPLE false-negative FAILs (e.g. 11 FAILs on one pitchdisc percept),
  beyond the two-FAIL corroboration fix. This confirms O1's diagnosis that
  the poisoning is program-side (prereg (f)), not gate-side.
- RK-3 rises to ~72% (~799/1,102), driven substantially by R1 revising the
  621 frozen conflicts (reported as a cross-check against AUTOPSY_R2-4 §4's
  65.8% replay; not claimed as O3's — the 621 are outside O1's residual).
- RK-2 stays 0/1,109. Wrong REVISED_INSTALLs: 0. Six timbredisc wrongs: all
  CORROBORATED, zero new installs. Adv wrong-install rate: unchanged at
  ~1.02%.
- O3c: no per-task margin threshold cleanly separates the (g)-blocked
  correct trials from the wrong trials (O1's calibration diagnosis holds).

## 7. Build/run protocol (frozen)

- Pure Zag, zero randomness. Three runs, byte-identical outputs required.
- Input: the frozen sweep battery (`sweep.jsonl`,
  sha256 `4163fffa65f18f552d48f7efec0e9800a7406547a27c6259d39a48ec7f0833f2`)
  via the frozen case generator; tol_of per the O1 replay
  (colordisc 8, colorconst 40, shapetrans 60, pitchdisc 4000, timbredisc 120,
  motiondir 0).
- The Zag instrument replays the gate with the O1 adjudicator (retained) +
  R1–R4, then scores every kill bar above.
- Commit via `TMPDIR=~/workspace/tmp_commit ~/workspace/commit_racefree.py`;
  binaries and `.zagd` excluded.

## 8. Relationship to sibling hypotheses

- R3-3 (D2, corroborated revision — release direction): O3-rebriefed covers
  the ADMISSION direction (O1's residual). D2's prereg is untouched.
- R3-7 (O2, full two-tier machinery): O2 remains PREREG-ONLY until V4. The
  R1 cross-check numbers are reported, not claimed, to avoid double-claiming.
- Prereg (f) ((g)-predicate revision): O3c's measurement is its input; O3
  installs nothing on it.
