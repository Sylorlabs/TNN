# REPORT: H-CONTLIFE-5 -- Learner-Owned Evaluation

Worker: H-CONTLIFE-5 (subagent, 2026-10-02). Replacement for a completed worker.
Prereg: `hcontlife5/PREREG.md`, frozen and committed alone at 7c1062dd6
before any implementation existed. Implementation: `src/selfjudge.zag`
(pure Zag), built with the pinned compiler
`src/tools/toolchain/znc_linux_x86_64_abed8aa1` to `bin/selfjudge`.
Toolchain guard: Step 0 safebin active whole session; `which python3` and
`which python` returned nothing; no forbidden executable invoked.

## What was built

One pure-Zag binary with three roles separated by function boundaries:

- LEARNER: `learner_commit` (affine fit on three training pairs, seals
  prediction p, tolerance t = rmax + 1, residual max rmax), `learner_judge`
  (self = 1 iff |observed y* - p| <= t), `learner_control_judge`
  (self_c = 1 iff rmax == 0, no consequence access). These take values
  only, never a case id, never call the world rule table.
- WORLD: `world_y`, called only from the P2 path in main.
- HARNESS: post-hoc hidden judgments (hidden = 1 iff |y* - p| == 0),
  agreement counts, bar checks. Reads sealed records only.

Phase order, enforced structurally: P1 commit all 24 cases (epoch 1),
P2 world reveals consequences (epoch 2, main arm only), P3 judge
(epoch 3). The control arm runs P1 then P3-CTRL with the consequence
field holding sentinel -999, which its judge never reads.

Frozen 24-case set: 8 AFFINE, 4 QUAD, 8 SHIFT (rule changes after the
training window), 2 WOBBLE-G (training noise at x=2, prediction exact),
2 WOBBLE-B (training noise at x=1 corrupts the fit).

## Results (3/3 runs byte-identical, sha256 8d4fe54446ac2f261269e0ef342cb1c828ad2c7ec4f61b2d5a019630f55b5563)

Main arm agreement: 24/24 (1.00). Every self-judgment matched the hidden
harness judgment: AFFINE 8/8 self=1, QUAD 4/4 self=0, SHIFT 8/8 self=0,
WOBBLE-G 2/2 self=1, WOBBLE-B 2/2 self=0.

Control arm (no consequence access) agreement: 14/24 (0.583). It agreed
on AFFINE (8), QUAD (4), WOBBLE-B (2) and failed exactly where the
prereg predicted: all 8 SHIFT cases (perfect training fit, so it trusted
a commitment the world had invalidated) and both WOBBLE-G cases
(imperfect fit, so it distrusted a commitment that was in fact exact).

In-program bars: k1=1, k3=1, k5=1, "IN-PROGRAM-BARS 3/3".

## Kill bar verdicts

- K1 TEMPORAL ORDER: PASS (in-program). All main-arm cases show commit
  epoch 1 < consequence epoch 2 < judge epoch 3; commits identical across
  arms; control arm shows epoch 1 < 3 with the consequence sentinel -999
  intact in every record.
- K2 LEARNER-STATE-ONLY JUDGMENT: PASS (shell grep audit). Learner
  function bodies contain no reference to world_y, hidden values, or
  case ids; world_y is called only from the P2 path in main.
- K3 CALIBRATION: PASS. 24/24 >= 20/24 (rate 1.00 >= 0.80).
- K4 DETERMINISM: PASS. 3/3 runs byte-identical.
- K5 CONTROL DEGRADATION: PASS. 14/24 <= 18/24 (0.583 < 0.80). The
  no-consequence control is far below the main bar, so the consequence
  carries the information.
- K6 NO EXPECTED-ANSWER LEAKAGE: PASS (shell grep audit). Hidden
  judgments are computed in the harness section after P3 and never fed
  back into any learner function; the learner never receives rule
  parameters, the hidden standard (eps = 0), or hidden judgments.

Verdict: BUILD-PASS (K1..K6 all pass).

## Honest interpretation

What this shows: the minimal closed loop works. A learner can commit to
a prediction plus a self-derived tolerance before consequences arrive,
then judge its own commitment from its sealed state plus the observed
consequence, with judgments that agree with hidden ground truth on a
frozen set. The SHIFT cases are the informative ones: training fit was
perfect, so the control trusted its commitment and was wrong 8/8, while
the consequence-informed self-judgment caught all 8 failures. The
consequence did real work that training-fit alone could not do.

What this does NOT show (pre-registered limits, restated): the predictor
is a fixed affine primitive, so this is not predictor invention; the
claim is the self-judgment loop. Consequences are exact, no noise. The
case set is small and the mechanism simple; a pass here bounds the
floor of self-evaluation capability, not its ceiling. The 24/24 was
expected by hand analysis before implementation, so the information gain
is in the machinery working as specified plus the control contrast, not
in a surprising outcome.

## Recommended follow-ups

1. Noisy consequences: y* with noise; does the residual-derived tolerance
   still calibrate, and where does it break?
2. Learner-set tolerance under genuine uncertainty: cases where the right
   t is not rmax + 1 by construction.
3. Revision: after a self-judged failure (self=0), the learner revises the
   commitment or the tolerance and is re-tested; does self-judgment drive
   improvement?
4. Cross-domain transfer of the judgment mechanism: same commit/judge
   loop on a non-sequence task with no mechanism changes.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/hcontlife5
~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1 src/selfjudge.zag -o bin/selfjudge
./bin/selfjudge | sha256sum   # expect 8d4fe54446ac2f261269e0ef342cb1c828ad2c7ec4f61b2d5a019630f55b5563
```

K2/K6 audit: `grep -n "world_y" src/selfjudge.zag` (only definition and
the P2 call site in main); `sed -n '134,174p' src/selfjudge.zag | grep
-n "world_y\|hidden\|HIDDEN\|cid"` (empty).
