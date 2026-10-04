# PREREG: H-CONTLIFE-5 -- Learner-Owned Evaluation: Commitment, Consequence, Self-Judgment

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/hcontlife5/` only.
Worker: H-CONTLIFE-5 (subagent, 2026-10-02). Replacement for a completed worker.
Parent mandate: Micah priority, internal verification. Reduce dependence on
harness-supplied expected answers in composition and evaluation. Prefer:
learner commitment, later world consequence, learner-owned evaluation.

## 1. What is being tested

The DELAYED-CONSEQUENCE work (C306, C316/DCE-V2) built temporal credit
assignment machinery: act, later observe consequences, attribute them. This
wave closes the loop: the learner COMMITS to an answer BEFORE seeing
consequences, the world later provides consequences, and the LEARNER ITSELF
judges whether its commitment was good, with no harness expected answer
anywhere in the learner's path.

Concretely: the learner sees three training pairs of an integer sequence,
commits to a predicted value p for a query point x* AND to a tolerance t
derived from its own training residuals, before the true outcome is
revealed. The world later reveals the true outcome y*. The learner then
computes its own verdict: self = 1 iff |y* - p| <= t, else 0. The tolerance
t is the learner's own committed standard, built from its own experience;
the learner is never told the harness acceptance standard.

Calibration bar: the harness holds hidden judgments on a frozen 24-case
set. Hidden judgment for a case: hidden = 1 iff the committed prediction
was exactly right (|y* - p| == 0), else 0. The harness knows the frozen
rules; the learner never sees the rules, the hidden standard (eps = 0), or
the hidden judgments. Agreement between self and hidden is measured
post-hoc by the harness. It is not trained, not fed back, not visible to
the learner.

The claim under test is the self-judgment loop, not the predictor. The
predictor (affine fit) is a generic function-approximation primitive. The
evaluation mechanism (residual-derived tolerance, post-consequence
threshold check) is fully generic and task independent.

## 2. Frozen task: sequence prediction with committed tolerance

Each case: training pairs (x, y) for x = 0, 1, 2, plus a query x*.
The learner must output, BEFORE the consequence phase, for every case:
  p = committed prediction for y at x*
  t = committed tolerance, t = rmax + 1, where rmax is the max absolute
      training residual of the learner's own affine fit.

The affine fit (frozen learner primitive): a_hat = y1 - y0 (unit x
spacing), b_hat = y0, prediction p = a_hat * x* + b_hat,
residuals r_i = |a_hat * x_i + b_hat - y_i|, rmax = max(r_0, r_1, r_2).

## 3. Frozen world and delayed consequence mechanism

World rule family (frozen, hidden from the learner). 24 cases, 5 flavors.
Training x is always 0, 1, 2. Listed as: id, flavor, train y0 y1 y2,
query x*, true outcome y* (world computed, learner never sees the rule).

AFFINE (flavor 0), y = a*x + b, x* = 5:
 1: (1,0): 0 1 2, y* 5
 2: (2,3): 3 5 7, y* 13
 3: (3,7): 7 10 13, y* 22
 4: (1,9): 9 10 11, y* 14
 5: (2,0): 0 2 4, y* 10
 6: (3,2): 2 5 8, y* 17
 7: (1,5): 5 6 7, y* 10
 8: (2,8): 8 10 12, y* 18

QUAD (flavor 1), y = x^2 + c, x* = 4:
 9: c=0: 0 1 4, y* 16
 10: c=1: 1 2 5, y* 17
 11: c=2: 2 3 6, y* 18
 12: c=3: 3 4 7, y* 19

SHIFT (flavor 2), y = a*x + b for x <= 2, y = a*x + b + d for x >= 3,
x* = 4 (rule changes after the training window; undetectable at commit):
 13: (1,0,d=3): 0 1 2, y* 7
 14: (2,1,d=4): 1 3 5, y* 13
 15: (3,0,d=5): 0 3 6, y* 17
 16: (1,4,d=3): 4 5 6, y* 11
 17: (2,2,d=5): 2 4 6, y* 15
 18: (3,1,d=4): 1 4 7, y* 17
 19: (1,7,d=5): 7 8 9, y* 16
 20: (2,5,d=3): 5 7 9, y* 16

WOBBLE-G (flavor 3), true affine rule, one training point off by +1 at
x = 2 (fit uses x = 0, 1 so the prediction stays exact), x* = 5:
 21: true 2x+1: 1 3 6, y* 11
 22: true 3x+2: 2 5 9, y* 17

WOBBLE-B (flavor 4), true affine rule, training point at x = 1 off by +1
(corrupts a_hat; prediction misses by more than the tolerance), x* = 4:
 23: true 2x: 0 3 4, y* 8
 24: true 2x+1: 1 4 5, y* 9

Consequence timing (frozen): three strict phases with a state barrier.
P1 COMMIT: the learner computes (p, t, rmax) for ALL 24 cases and seals
the commitment records. No consequence value exists in the learner's data
flow during P1. P2 WORLD: the world reveals y* for all cases (epoch 2).
P3 JUDGE: the learner computes self from its sealed (p, t) and the
observed y* (epoch 3). The delay is structural: every commitment epoch
strictly precedes every consequence epoch. The consequence is the observed
true outcome itself, delivered after commitment, never before.

Control arm (frozen): identical P1, then P3-CTRL with NO P2. The control
learner's judgment is computed with the consequence field holding a
sentinel (-999) that its judge function never reads. Frozen control
policy: self_c = 1 iff rmax == 0 (judge from training fit alone:
"I trust my commitment iff my training fit was perfect"). This is the
natural no-consequence baseline.

## 4. The learner-owned evaluation: exact computation

Main arm, per case, from learner state only:
  self = 1 iff |y*_observed - p_committed| <= t_committed, else 0.
Inputs to the judge function: (p, t, y*) as values only. No case id, no
rule parameters, no hidden standard, no expected answer.

Control arm, per case, from learner state only:
  self_c = 1 iff rmax == 0, else 0.
Inputs to the control judge function: (rmax) as a value only. The
consequence is structurally absent.

Hidden harness judgment (never visible to the learner), per case:
  hidden = 1 iff |y* - p| == 0, else 0.
The harness standard eps = 0 is frozen here and never passed to any
learner function. Agreement = (self == hidden), counted per arm.

## 5. Calibration bar and frozen kill bars

Expected values by hand analysis of the frozen mechanism on the frozen
cases (recorded before implementation; the run must reproduce them):

Main arm: AFFINE err 0 <= t 1 -> self 1 = hidden 1 (8/8). QUAD err 12 >
t 3 -> self 0 = hidden 0 (4/4). SHIFT err d in {3,4,5} > t 1 -> self 0 =
hidden 0 (8/8). WOBBLE-G err 0 <= t 2 -> 1 = 1 (2/2). WOBBLE-B err 4 >
t 3 -> 0 = 0 (2/2). Expected agreement 24/24.

Control arm: AFFINE rmax 0 -> self_c 1 = hidden (8 agree). QUAD rmax 2 ->
self_c 0 = hidden (4 agree). SHIFT rmax 0 -> self_c 1 != hidden 0
(8 disagree). WOBBLE-G rmax 1 -> self_c 0 != hidden 1 (2 disagree).
WOBBLE-B rmax 2 -> self_c 0 = hidden (2 agree). Expected 14/24 = 0.583.

Frozen kill bars:
K1 TEMPORAL ORDER: for every main-arm case, commit epoch < consequence
epoch < judge epoch, checked in-program from the sealed records. Control
arm: consequence field is the sentinel and the control judge never reads
it. FAIL if any epoch ordering is violated.
K2 LEARNER-STATE-ONLY JUDGMENT: shell grep audit. Learner functions
(learner_commit, learner_judge, learner_control_judge) must not reference
the world rule table (world_y), the hidden standard, or hidden judgments.
They receive only values (training y's, x*, p, t, rmax, observed y*).
FAIL on any reference.
K3 CALIBRATION: main-arm agreement >= 20/24 (rate >= 0.80). FAIL below.
K4 DETERMINISM: 3/3 runs byte-identical (sha256 of full stdout).
FAIL on any divergence.
K5 CONTROL DEGRADATION: control-arm agreement <= 18/24 (strictly below
0.80; expected 14/24). FAIL if the no-consequence control reaches the
main bar, which would mean consequences carry no information.
K6 NO EXPECTED-ANSWER LEAKAGE: the learner's data flow contains no rule
parameters, no hidden standard, no hidden judgments. The harness
agreement section is a separate function that never feeds values back
into any learner function. Verified by the K2 grep audit plus code
inspection. FAIL on any leakage path.

Verdict rule: BUILD-PASS iff K1..K6 all pass. Any single FAIL -> BUILD-FAIL
with the failing bar named. VOID is terminal (prereg violation).

## 6. Information-flow architecture (one binary, three roles)

Single pure-Zag program, three roles separated by function boundaries:
- LEARNER role: learner_commit(y0, y1, y2, xstar) -> (p, t, rmax);
  learner_judge(p, t, ystar) -> self; learner_control_judge(rmax) -> self_c.
  These functions never receive a case id and never call world_y.
- WORLD role: world_y(cid) -> y*, called only in P2, only by main.
- HARNESS role: agreement counting and bar checks, reading sealed
  records only, never writing into learner state.
The case table (training values) is readable by main for P1 input
assembly; the rule table (world_y) is callable only from the P2 path.
K2/K6 audits enforce this.

## 7. Determinism and build plan

Pure Zag, pinned compiler src/tools/toolchain/znc_linux_x86_64_abed8aa1.
No randomness, no clocks, no environment reads in the program. Output via
one preallocated buffer and a single raw-syscall flush (the established
emit idiom: cursor-returning e1 helpers, no _zag_print for dynamic
content). Build: `znc src/selfjudge.zag -o bin/selfjudge`. Run three
times, sha256 each stdout, require identical. All scientific computation
in Zag; shell only for znc invocation, runs, sha256sum, greps, git.

## 8. Honest limitations (pre-registered)

- The predictor is a fixed affine primitive; the experiment tests the
  self-judgment loop, not predictor invention. A pass does not show the
  learner can invent evaluation standards for arbitrary tasks.
- Consequences are exact (no noise). Noisy consequences are follow-up work.
- The hidden standard (exact match) is lenient to state but strict in
  value; the learner's t is its own construction. Agreement measures
  calibration of the learner's self-derived standard, not access to truth.
- If the main arm scores at chance, the report will say so; that bounds
  the current architecture's self-evaluation capacity.
- Follow-ups if PASS: noisy consequences, learner-set t under genuine
  uncertainty, revision after self-judged failure, cross-domain transfer
  of the judgment mechanism.
