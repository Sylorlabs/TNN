# PREREG — W4 SELF-TRAINING PAM (wild track, WILD-B)

**Date:** 2026-09-24. **Crew:** WILD-B. **Status:** FROZEN — committed before
any W4 fixture, build, or run. Parent: `pam/round4/prereg/PREREG_ROUND4.md`
(§4 seed design W4). Shared tape: `wild/tape/TAPE.md` (frozen).

## 1. Falsifiable claim

W4 is an ONLINE, tighten-only, deterministic threshold learner. Starting from
the frozen baseline bar (CT=700, MT=0, ST=1, AT=1 — PREREG_M1_BAR §7, used
as-is, NOT recalibrated), W4 processes the frozen wrong stream and revises
its confidence threshold CT from a miss log by a frozen rule. Claims:

- **F1 (mechanism):** W4's online revision converges to EXACTLY CT=841, the
  value of the offline M1 exact rule restricted to the frozen arm set
  (MT=0, ST=AT=1): CT*(0) = max({conf(w)+1 : w∈W} ∪ {minconf(pair)+1}) =
  max(833, 841) = 841 (script-extracted from the frozen tape: W confs
  764,774,788,798,798,799,800,806,806,819,830,832; P weaker-member confs
  704×8, 840). Online ≡ offline under the same arms.
- **F2 (safety):** the converged bar (841, 0, 1, 1) admits ZERO frozen wrongs
  (12 W + 9 P pairs) — K1 satisfied post-training.
- **F3 (discipline):** every revision is triggered by a logged confirmed miss,
  magnitude ≤ CAP=64 CT-points per miss, thresholds never decrease.
- **F4 (hygiene):** byte-identical reruns (≥2×), O(1) work per decision,
  terminates (epochs bounded).

## 2. Frozen mechanism

State: CT (i64, init 700). MT=0, ST=1, AT=1 FROZEN — W4 moves CT only
(hands-off §5(a): no recalibration of strong/agree; the margin arm is not
touched either — the CT-only restriction is itself part of the design).

Admission predicate (frozen): PASS(t) ⟺ conf≥CT ∧ mrgF≥0 ∧ strong≥1 ∧ agree≥1.

Training stream (preregistered deterministic order): the 12 W rows in tape
order (seq 24..35), then the 9 P pairs in pairid 0..8 order. A P pair is a
"miss" iff BOTH members pass (pair installs ⟺ both pass); the revision uses
the pair's weaker member conf.

Revision rule (frozen, on confirmed miss m with conf c_m):
`CT := min(c_m + 1, CT + 64)` — i.e., raise CT to block this miss, but never
more than CAP=64 points per miss. If the miss is already blocked
(c_m + 1 ≤ CT), no revision (not a miss — cannot happen by construction;
asserted in the log).

Epochs: repeat the stream until a full epoch produces zero revisions;
max 3 epochs (then HALT — non-convergence is a finding, not a loop).

Miss-log discipline (auditable): the instrument logs every miss as
`MISS|kind|id|conf` immediately followed by `REV|oldCT|newCT|delta|cap_hit`.
A revision line without a preceding miss line is a protocol violation.

Predicted trace (from frozen numbers): epoch 1 ends at CT=841 (W max 832 →
833; P-V4 weaker 840 → 841; max inter-miss conf gap is 14 < 64 so the cap
never binds except possibly the first miss); epoch 2: zero revisions →
converged. Correct-admit at convergence: |{t∈C : conf≥841}|/1102 =
433/1102 = 39.29% (script-computed from the frozen tape).

## 3. Kill bars (program §4 K1–K5 verbatim + W4 additions, add-only)

- **K1:** any false-admit on the frozen wrong set → KILL. Applies to the
  CONVERGED bar (post-final-revision). During training, wrongs passing the
  bar are the intended learning signal, not K1 violations.
- **KB-W4-T (training safety, added):** any confirmed miss in the stream that
  is NOT followed by a revision before the next admission decision (a silent
  miss) → KILL. Verified from the log: #REV == #MISS, alternating order.
- **KB-W4-MONO (added):** any revision with newCT < oldCT (loosening), or any
  revision with delta > 64, or any revision not immediately preceded by a
  miss log line → KILL (tighten-only, bounded, state-driven-only).
- **KB-W4-CONV (added):** final CT ≠ 841 (the offline exact value) →
  KILL (online failed to reproduce offline optimum). Correct-admit ≠ 433/1102
  → KILL (count mismatch = implementation defect).
- **K2:** the two battery runs' stdout differ by even one byte → KILL.
- **K3:** correct-admit 39.29% is >5 pts below the C3-repair baseline
  (71.78%). Per schema this is HOLD (redesign), not KILL — UNLESS the
  D-W4-1 diagnostic below demonstrates a compensating safety gain, in which
  case the verdict records SURVIVE-with-documented-tradeoff and the HOLD
  converts to a redesign direction (hybrid arms). The verdict will state
  which reading was applied and why.
- **K4:** per-decision work superlinear in stream length → KILL (assert O(1):
  the instrument logs decisions-per-epoch; epochs ≤ 3 by construction).
- **K5:** non-termination on any input → KILL (epoch cap = 3; asserted).

## 4. Diagnostics (reported, never kill — frozen list)

- **D-W4-1 (margin-adversary invariance):** re-evaluate the CONVERGED W4 bar
  and the frozen M1 bar (705, 3588, 1, 1) over the wrong set with every
  wrong's mrgF deterministically inflated ×10 (simulating margin-sensor
  corruption; conf/strong/agree untouched). Report wrongs admitted under each
  bar. Predicted: W4 (MT=0, margin arm vacuous) still blocks 30/30; M1's
  margin arm passes the inflated wrongs (W mrgF 1888–2373 → 18880–23730 ≥
  3588; conf 764–832 ≥ 705) → M1 admits 12/12 W. This is the candidate
  compensating safety gain for the K3 reading.
- **D-W4-2:** revision count, per-revision deltas, cap-hit count (predicted 0
  hits after the first miss — max gap 14 < 64 — recorded, not asserted).
- **D-W4-3:** epoch-1 intermediate CT values (learning curve).

## 5. Battery

Instrument: pure-Zag `w4_selftrain.zag`. CLI: `w4_selftrain <tape>`.
Reads the canonical tape (sha asserted in-output), runs the training stream,
emits the miss/revision log + final metrics (`FINAL_CT`, `correct_admit`,
`wrong_admit`, `kb_*` lines). Runs: 2×; sha256(stdout) must match.
Scorer: `score_w4.py` (Python mirror — independently recomputes CT trace,
final CT, correct-admit, K1/KB checks, D-W4-1 — never the instrument).

## 6. Hands-off / laws compliance

- Uses frozen Round-3 bars as-is (baseline bar as start; M1 bar only as a
  diagnostic comparator in D-W4-1). No recalibration of strong/agree/MT.
- Fable's 4 kill-bar repairs: not applied. 3 HELD items: not run.
- Zero RNG; no wall-clock; deterministic given (tape, rule).
- []u8 arenas + LE accessors; no `as []i32/u32/u16` indexed casts.
- znc gotchas honored (see build notes in the runlog).

## 7. Standing-law cap note (for verdict-time classification)

Frozen numeric caps in this design: CAP=64 (per-miss revision bound),
epoch cap 3. Classified at verdict time as load-bearing vs arbitrary per
Micah's 2026-09-24 standing law. (Design note: CAP's VALUE 64 is
calibration; the EXISTENCE of a per-miss bound is the stability mechanism.)
