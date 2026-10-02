# PREREG: H-CAUSALEXP Experiment CONSTRUCTION (causalexp_construct)

Date: 2026-09-30.
Status: FROZEN. Committed before any implementation, build, or run.
Lane: causal frontier, next step after H-CAUSALEXP1 (BUILD-PASS, bounded L2).

## 1. Objective

H-CAUSALEXP1 selects interventions from 42 researcher-authored candidates.
The alternative-explanation attack downgraded it: the candidate set is
authored and max-split adds nothing to correctness beyond the
discrimination filter. The next architectural frontier is experiment
CONSTRUCTION: the learner must assemble a discriminating multi-step
intervention from generic primitives, not select it from a list.

This prereg defines a sealed world where NO single supplied primitive
action distinguishes the competing hypotheses, and freezes the success
criteria for a learner that constructs the discriminating sequence
because the hypotheses predict different outcomes for it.

## 2. Hypothesis space (authored; the frontier under test is construction, not hypothesis invention)

Hypotheses are delay-rule sets over binary variables X=0, Z=1, Y=2.
A rule (src,dst,delay) means: once src=1, dst becomes 1 when
(t - t_src_set) >= delay, where t advances on wait actions.
Rules are DATA (arrays), interpreted by one generic simulator.
There is no per-hypothesis code branch.

World A hypotheses:
- H1: [(X,Z,2),(Z,Y,0)]. X causes Z after delay 2; Z causes Y immediately.
- H2: [(X,Y,1)]. X causes Y directly after delay 1. Z never changes.

World B hypotheses:
- H3: [(X,Z,3),(Z,Y,0)]. X causes Z after delay 3; Z causes Y immediately.
- H4: [(X,Y,2)]. X causes Y directly after delay 2. Z never changes.

The true world in each run is one of the pair, sealed from the learner.
Four configurations are run: (A,true=H1), (A,true=H2), (B,true=H3),
(B,true=H4).

## 3. Generic primitive actions (the construction substrate)

Four primitives, with fixed generic semantics shared by simulation and
the real world:
- S: set X:=1 (records t_X := t).
- W: t := t+1, then apply all rules once.
- OY: observe Y (returns 0/1; changes nothing).
- OZ: observe Z (returns 0/1; changes nothing).

Initial state: X=Z=Y=0, t=0, t_X=t_Z=t_Y=-1.
A sequence's predicted/actual outcome is the value of its LAST observe
action; sequences with no observe action have outcome NONE and cannot
discriminate.

The learner is NOT given any sequence. It is given the four primitives
and a generic append/compose operation. Sequences are built by the
learner via iterative deepening (depth 1, 2, 3, ...), each depth
generated compositionally from the primitives.

## 4. Proof that no single primitive distinguishes (frozen hand proof; the program re-verifies)

From the initial state, for World A (H1 vs H2):
- S: no observation. Outcomes agree (NONE, NONE).
- W: no observation. Agree.
- OY: H1 predicts Y=0; H2 predicts Y=0. Agree.
- OZ: H1 predicts Z=0; H2 predicts Z=0. Agree.

For World B (H3 vs H4): identical reasoning; OY gives 0/0, OZ gives 0/0.
Therefore no length-1 sequence discriminates in either world.

## 5. Minimal discriminating sequences (frozen hand proof)

World A:
- Every length-2 sequence ending in an observe agrees. Check S,OY:
  H1: t=0 so Y=0. H2: t-t_X=0<1 so Y=0. Agree. S,OZ: Z=0 both.
  W,OY / W,OZ / OY,OY / OY,OZ / OZ,OY / OZ,OZ: all 0/0. Agree.
  Non-observing sequences have outcome NONE.
- Length 3: S,W,OY discriminates. H1: after S (t_X=0) and W (t=1),
  rule (X,Z,2) needs t-t_X>=2: 1<2, so Z=0, Y=0. H2: rule (X,Y,1)
  needs t-t_X>=1: 1>=1, so Y=1. Predictions 0 vs 1. DISAGREE.

World B:
- Lengths 1 and 2 agree (same checks as World A; delays only larger).
- Length 3: S,W,OY agrees. H3: t=1, rule (X,Z,3) needs >=3: Z=0, Y=0.
  H4: rule (X,Y,2) needs t-t_X>=2: 1<2, so Y=0. Agree 0/0.
  All other length-3 observing sequences have t<=1 at observation; agree.
- Length 4: S,W,W,OY discriminates. H3: t=2, 2<3, Z=0, Y=0.
  H4: t-t_X=2>=2, Y=1. Predictions 0 vs 1. DISAGREE.

Consequence: the two worlds require DIFFERENT constructed sequences
(length 3 vs length 4). A learner hardcoded to one length or one
sequence fails one world. The machinery must genuinely compose.

## 6. Learner algorithm (frozen)

Input: hypothesis pair (rule-sets as data). The learner never reads the
true rule-set; only world_step does.

1. For depth d = 1, 2, 3, 4, 5 (MAXD=5):
   a. Generate every sequence of length d over {S,W,OY,OZ} in fixed
      lexicographic order (S<W<OY<OZ), by base-4 counting. Sequences are
      composed by the learner; none pre-exist.
   b. For each sequence with at least one observe action, simulate it
      under EACH live hypothesis with the generic simulator; record the
      predicted outcome per hypothesis.
   c. Emit per-depth summary: sequences checked, discriminating found (0/1).
   d. If any sequence has disagreeing predictions across live
      hypotheses, record the FIRST such sequence (deterministic order),
      emit both predictions, and STOP searching.
2. If no discriminating sequence found by MAXD: emit
   NO-DISCRIMINATING-SEQUENCE and halt (this is a BUILD-FAIL outcome).
3. Execute the recorded sequence ONCE against the real world via
   world_step (the ONLY real-world actions in the run; the search in
   step 1 is pure simulation, zero real actions).
4. For each live hypothesis, re-simulate the executed sequence; eliminate
   every hypothesis whose prediction mismatches the real outcome.
5. Emit survivor(s).

The "BECAUSE" criterion: the executed sequence is the unique output of a
deterministic procedure whose selection rule is predicted disagreement.
The trace shows (i) all shorter depths yielded zero disagreement,
(ii) the executed sequence's per-hypothesis predictions differ,
(iii) no real-world action occurred before the executed sequence.
A random-search learner would execute sequences without predicted
disagreement; this learner cannot, by construction.

## 7. Kill bars (numbered; all must pass for BUILD-PASS)

- K-CX1 (no single primitive discriminates): the program emits, for each
  world, the predicted outcome of each of the 4 primitives under each
  hypothesis; all pairs agree. Verified from the raw output.
- K-CX2 (World A construction): in configs (A,true=H1) and (A,true=H2),
  the learner emits a constructed discriminating sequence of length 3,
  executes exactly one real-world sequence (the constructed one), and
  the survivor is the true hypothesis in both configs.
- K-CX3 (World B construction, different form): in configs (B,true=H3)
  and (B,true=H4), the learner emits a constructed discriminating
  sequence of length 4 (different length from World A), executes exactly
  one real-world sequence, and the survivor is the true hypothesis in
  both configs.
- K-CX4 (because, not chance): the raw trace shows for each config:
  per-depth summaries with 0 discriminating at all depths below the
  found depth; the found sequence with per-hypothesis predictions that
  differ; and exactly one EXEC line (the real-world execution) in the
  config. No real-world action precedes the EXEC line.
- K-CX5 (elimination correctness): in all 4 configs, exactly the true
  hypothesis survives (the other is ELIMINATED) and the real outcome
  equals the true hypothesis's prediction.
- K-CX6 (determinism): 3 runs, byte-identical (cmp), exit 0.
- K-CX7 (purity): pure Zag (build, runs, analysis); no Python anywhere;
  no em dash bytes in committed docs.

BUILD-PASS iff K-CX1 through K-CX7 all pass.
BUILD-FAIL otherwise, with the failing bar named.

## 8. Scope and honest limitations (frozen)

- Hypotheses are authored rule-sets. This wave tests experiment
  CONSTRUCTION, not hypothesis invention. Classification target is
  bounded L2 with learner-constructed experiments, not L3.
- The primitive set {S,W,OY,OZ} is authored. The sequences are not.
- Worlds are synthetic and tiny (3 binary variables, 2 hypotheses).
- Iterative deepening is systematic search over a productive space,
  guided by the semantic criterion of predicted disagreement. It is not
  random search (no real-world trial-and-error) and not selection from an
  authored candidate list (sequences are composed, unbounded in length).
- This is step 2 (implementation) of the promotion pipeline for the
  construction frontier. Steps 3+ (sealed eval is built-in via 4
  configs; independent reproduction; baselines; adversary; OOD;
  ablation; transfer; red team; governance) remain.

## 9. Amendments

None. If an amendment is needed, it will be committed as a separate
file before the result, with the changed section quoted.
