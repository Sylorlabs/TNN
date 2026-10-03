# PREREG-REVISE: H-CONTLIFE-5 follow-up -- Revision After Self-Judged Failure

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/hcontlife5/` only. New
files: PREREG-REVISE.md (this file), src/revise.zag, bin/revise,
runs/revise-run{1,2,3}.txt, REPORT-REVISE.md. The frozen C337 files
(PREREG.md, REPORT.md, src/selfjudge.zag) are not modified.
Worker: H-CONTLIFE-5-REVISE (subagent, 2026-10-02). Replacement for a
completed worker (learner-owned evaluation).
Parent mandate: close the evaluation to action loop. C337 (BUILD-PASS)
showed the learner can commit, observe consequences, and judge itself
(24/24 agreement; no-consequence control 14/24). This wave asks: when the
learner judges its own commitment BAD, what does it do, and does the
revision help on fresh cases?

## 1. What is being tested

The revision step of the commit to consequence to judge loop. After a
self-judgment of failure (self=0), the learner runs a failure analysis
built only from its own state (training values, committed prediction,
observed consequence), and may adopt a revised commitment procedure as
persistent learner state. It is then tested on 24 FRESH cases (frozen
set below, same 5 flavor families with new parameters, including fresh
SHIFT-type rule changes). A no-revision control arm (judges but never
revises) runs the same fresh set for comparison.

The claim under test is self-judgment GATED revision: the trigger, the
failure attribution, and the adoption decision are the learner's own.
The revision PROCEDURE itself (leave-one-out analysis plus median, see
section 2) is researcher specified in this prereg. This wave does not
claim learner invented revision, only that self-judgment can gate a
revision that improves later commitments.

## 2. The revision mechanism: exact specification

Chosen mechanism: SWITCH PREDICTOR (parent task option 3), with the
switch licensed by a learner owned failure attribution (a precise,
implementable form of option 4, mark the failing pattern unreliable).

Definitions (all quantities are learner observable values; no case id,
no flavor label, no hidden standard, no hidden judgment anywhere):

- Training values per case: (y0, y1, y2) at x = 0, 1, 2; query x*.
- Committed (p, t): p from the frozen affine fit, t = rmax + 1.
- Observed consequence: y*.
- Self-judgment: self = 1 iff |y* - p| <= t, else 0.
- LOO prediction excluding point k in {0,1,2}: affine fit on the other
  two training points, evaluated at x*. Pure function of values.
- LOO license: some k with loo_pred(k) == y* exactly. Meaning, from the
  learner's own data: "excluding one training point would have made my
  prediction match the observed consequence exactly," i.e. the failure
  is attributable to single point training corruption.

Revision protocol (frozen):

1. TRIGGER: after round-1 judging, for each case with self=0 and only
   such cases, the learner runs the failure analysis. Cases with self=1
   are never analyzed.
2. ATTRIBUTION: the analysis computes the three LOO predictions from
   the training values and checks the LOO license against the observed
   y*. No other input.
3. ADOPTION: if at least one self-judged failure is LOO licensed, the
   learner sets a persistent flag in its own state: for all FUTURE
   commitments whose training fit is imperfect (rmax > 0), commit
   p = median of the three LOO predictions instead of the full fit
   prediction. The tolerance rule is UNCHANGED (t = rmax + 1 from the
   standard fit). If no failure is licensed, nothing is adopted.
4. Round 2 uses the adopted procedure (revision arm) or the frozen
   procedure (control arm).

Why this mechanism, and not the other options:

- WIDEN TOLERANCE (rejected as the primary mechanism). Preregistered
  lemma: self judgment agreement with the hidden exact match standard
  holds iff (err <= t) == (err == 0). Widening t cannot change any err=0
  verdict (already accepted) and can only flip err != 0 verdicts from
  correct reject to incorrect accept. Therefore no tolerance widening
  revision can raise agreement; it is agreement monotone nonincreasing.
  Bar R5 guards against degenerate always pass widening.
- REQUEST MORE TRAINING DATA (rejected). Not implementable: the
  protocol delivers exactly three training pairs per case and the
  learner has no channel to request more.
- PURE TOLERANCE RE TUNING / mark unreliable as a tolerance ledger
  (rejected as primary). Any revision preserving the observed round-1
  verdicts must keep t=1 on the rmax=0 signature (passes at miss 0,
  failures at miss >= 3) and t=3 on the rmax=2 signature (failures at
  miss >= 4, frozen already at the boundary). The learner's failure
  experience licenses no verdict changing tolerance move. The
  actionable signal is in the predictor, not the tolerance.
- SWITCH PREDICTOR (chosen). The WOBBLE-B failures carry a learner
  detectable signature (LOO exact licensing). The response,
  median of leave one out fits, is a generic robust fitting procedure,
  not a task specific handler: it knows nothing about flavors, shifts,
  or quadratics. SHIFT failures (rule changes after the training
  window) cannot be LOO licensed, so the irreducible class is correctly
  left alone. QUAD failures (needs a non affine primitive) cannot be
  LOO licensed either, so the primitive limited class is left alone.

Preregistered honest limitation: the LOO plus median procedure is
researcher specified here. The learner owns the trigger (self judged
failures only), the attribution (computed from its own values plus the
observed consequence), and the adoption (persistent learner state).
A pass shows self judgment can gate useful revision, not that the
learner invented robust statistics.

## 3. Round-2 frozen set: 24 fresh cases, same 5 flavors

Training x is always 0, 1, 2. Format: cid, train y0 y1 y2, x*, y*.

AFFINE (flavor 0), x* = 5:
 0: 1 3 5, y* 11        (2x+1)
 1: 2 3 4, y* 7         (x+2)
 2: 0 3 6, y* 15        (3x)
 3: 4 6 8, y* 14        (2x+4)
 4: 1 2 3, y* 6         (x+1)
 5: 3 6 9, y* 18        (3x+3)
 6: 2 4 6, y* 12        (2x+2)
 7: 6 7 8, y* 11        (x+6)

QUAD (flavor 1), y = x^2 + c, x* = 4:
 8: c=4: 4 5 8, y* 20
 9: c=5: 5 6 9, y* 21
 10: c=6: 6 7 10, y* 22
 11: c=7: 7 8 11, y* 23

SHIFT (flavor 2), y = a*x + b for x <= 2, y = a*x + b + d for x >= 3,
x* = 4 (fresh rule changes, new a, b, d):
 12: (2,0,d=3): 0 2 4, y* 11
 13: (1,1,d=4): 1 2 3, y* 9
 14: (3,2,d=5): 2 5 8, y* 19
 15: (2,3,d=3): 3 5 7, y* 14
 16: (1,3,d=5): 3 4 5, y* 12
 17: (3,1,d=4): 1 4 7, y* 17
 18: (2,6,d=5): 6 8 10, y* 19
 19: (1,0,d=3): 0 1 2, y* 7

WOBBLE-G (flavor 3), true affine rule, training point at x = 2 off by
+1 (fit uses x = 0, 1 so the prediction stays exact), x* = 5:
 20: true 2x+3: 3 5 8, y* 13
 21: true 4x+1: 1 5 10, y* 21

WOBBLE-B (flavor 4), true affine rule, training point at x = 1 off by
+1 (corrupts the full fit), x* = 4:
 22: true 3x: 2 6 8 wait, train is (0,4,6): y0=0, y1=4, y2=6, y* 12
 23: true 3x+2: train (2,6,8), y* 14

(Case 22: true 3x gives (0,3,6); x=1 point off by +1 gives train
(0,4,6), y* = 12. Case 23: true 3x+2 gives (2,5,8); train (2,6,8),
y* = 14.)

## 4. Protocol: two rounds, seven phases, epoch barrier

Round 1 runs on the frozen C337 24-case set (same cases, same world).
Round 2 runs on the fresh set of section 3.

- R1-P1 COMMIT (epoch 1): both arms commit (p, t, rmax) on all 24
  round-1 cases with the frozen procedure. No consequence exists yet.
- R1-P2 WORLD (epoch 2): world reveals y* for round 1 (both arms; the
  control arm here DOES receive consequences, unlike the C337
  no-consequence control).
- R1-P3 JUDGE (epoch 3): both arms compute self from sealed (p, t)
  plus observed y*.
- R1-P4 REVISE (epoch 4, revision arm ONLY): for each case with
  self=0, run the learner failure analysis (section 2); adopt the
  persistent flag iff at least one case is LOO licensed. The control
  arm has no P4: it judges but does not revise. This isolates the
  revision effect.
- R2-P5 COMMIT (epoch 5): both arms commit on the 24 fresh cases.
  Revision arm uses learner_commit2 (median of LOO predictions when
  the flag is set and rmax > 0, else the frozen fit). Control arm uses
  the frozen fit.
- R2-P6 WORLD (epoch 6): world reveals fresh y*.
- R2-P7 JUDGE (epoch 7): both arms compute self on the fresh cases.

## 5. Expected values (hand analysis, recorded before implementation)

Round 1 (both arms): agreement 24/24, same as C337 main. Self judged
failures: 4 QUAD + 8 SHIFT + 2 WOBBLE-B = 14. Revision triggers on all
14. LOO license check: WOBBLE-B cid 22: LOO preds {6, 8, 12}, y* = 8,
  exclusion of x=1 predicts exactly: LICENSED. cid 23: LOO {12, 14,
  18}, y* = 14: LICENSED. QUAD: LOO {10+c, 8+c, 4+c} vs y* = 16+c:
  none exact, 0 licenses. SHIFT: training is clean affine, all LOO
  preds equal the full fit pred, none equals y*: 0 licenses. Expected:
  trg_count = 14, lic_count = 2, persistent flag adopted = 1.

Round 2 revision arm: AFFINE 8/8 self=1 (err 0). QUAD 4/4 self=0
  (median pred 8+c, err 8 > t 3). SHIFT 8/8 self=0 (err d in
  {3,4,5} > t 1). WOBBLE-G 2/2 self=1 (median exact, err 0 <= t 2).
  WOBBLE-B 2/2 self=1 (median pred exact: 12 and 14; err 0 <= t 3;
  verified in general: for true ax+b with x=1 corrupted by +1, the
  three LOO preds are {4a+b-2, 4a+b, 4a+b+4}, median 4a+b exact).
  Expected agreement 24/24.
Round 2 control arm: identical except WOBBLE-B self=0 (full fit pred
  16/18, err 4 > t 3, hidden 0): expected agreement 24/24.
Commitment quality on the WOBBLE-B class, round 2 total |err|:
  revision arm 0 vs control arm 8.

Note the honest expectation: agreement is at ceiling (24/24) in both
arms because the C337 loop was already calibrated; the measurable
revision effect is commitment quality on the correctable class (bar
R7). If R7 fails while agreement bars pass, the verdict follows the
bars and the report states revision did not improve predictions.

## 6. Frozen kill bars R0..R7

- R0 TEMPORAL ORDER: per case records show strict epoch order:
  revision arm round 1: 1 < 2 < 3 < 4; control round 1: 1 < 2 < 3;
  both arms round 2: 5 < 6 < 7. Checked in program. FAIL on any
  violation.
- R1 TRIGGER EXACTNESS: revision analysis ran on all and only self
  judged failures. In program: revision arm trg_count == 14, per case
  TRG == (SELF == 0); control arm TRG == 0 on all cases. FAIL otherwise.
- R2 SELECTIVITY: LOO licensing fired exactly twice (the WOBBLE-B
  cases), zero on QUAD and SHIFT: lic_count == 2. FAIL otherwise.
- R3 ROUND-2 AGREEMENT: revision arm agreement on the fresh 24 >=
  14/24. (Floor mandated by the parent task: first round no-consequence
  control scored 14/24. Expected 24/24.) FAIL below.
- R4 NO HARM VS CONTROL: revision arm round-2 agreement >= control
  arm round-2 agreement. Expected 24/24 = 24/24. FAIL if revision
  scores strictly below the no-revision control.
- R5 STILL REJECTS BAD: on the 12 round-2 genuinely bad commitments
  (hidden = 0: 4 QUAD + 8 SHIFT), revision arm self = 0 on all 12.
  Guards against always pass tolerance degeneration. FAIL below 12/12.
- R6 DETERMINISM: 3/3 runs byte identical (sha256 of full stdout).
  FAIL on any divergence.
- R7 COMMITMENT GAIN: round-2 WOBBLE-B class total |err|, revision
  arm < control arm. Expected 0 < 8. FAIL otherwise.

Shell audits (reported alongside R0): learner functions
(learner_commit, learner_judge, learner_revise, learner_commit2,
loo_pred, med3) never reference world_y, world_y2, hidden values, the
hidden standard, or case ids; the harness agreement section never feeds
values back into learner state (K2/K6 style grep audit).

Verdict rule: REVISION-PASS iff R0..R7 all pass. Any single FAIL gives
REVISION-FAIL with the failing bar named. VOID is terminal (prereg
violation: e.g. implementation committed before this prereg, or a bar
weakened after results).

## 7. Information flow architecture

Single pure Zag binary, three roles separated by function boundaries:
- LEARNER: learner_commit, learner_judge, learner_revise (takes values
  plus a learner owned flag cell; sets the flag only on LOO license),
  learner_commit2 (takes the flag value), loo_pred, med3. Values only,
  never a case id, never calls world_y / world_y2.
- WORLD: world_y (round 1), world_y2 (round 2), called only from the
  P2/P6 paths in main.
- HARNESS: agreement counting and bar checks, reading sealed records
  only, never writing into learner state. The persistent revision flag
  is written only by learner_revise.
Round-1 case tables are readable by main for P1 input assembly; round-2
tables likewise for P5. Rule tables are callable only from the P2/P6
paths. Audits enforce this.

## 8. Determinism and build plan

Pure Zag, pinned compiler src/tools/toolchain/znc_linux_x86_64_abed8aa1.
No randomness, no clocks, no environment reads. Output via one
preallocated buffer and a single raw syscall flush (established emit
idiom). Build: `znc src/revise.zag -o bin/revise` (run from the lane
dir). Run three times, sha256 each stdout, require identical. All
scientific computation in Zag; shell only for znc invocation, runs,
sha256sum, greps, git.

## 9. Honest limitations (pre-registered)

- The revision procedure (LOO plus median) is researcher specified in
  this prereg; the experiment tests self judgment gated revision, not
  learner invented revision. A pass does not show the learner can
  invent revision procedures.
- Agreement is expected at ceiling in both arms; the discriminating
  bar is R7 (commitment quality on the correctable class).
- Consequences are exact (no noise). Case sets are small (24 + 24).
- The WOBBLE-B correctability depends on single point corruption at
  x=1; the prereg does not claim generalization to other corruption
  patterns.
- If revision makes round-2 agreement worse than control (R4 FAIL) or
  fails to improve predictions (R7 FAIL), the report will say exactly
  why, per the observed mechanism, with no salvage.
