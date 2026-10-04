# PREREG: F2 Ablation + Adversary

Date: 2026-09-30. Worker: F2 Ablation Worker.
Frozen source under test: AUTOSCI2 learner `1eb66765d` (BUILD-PASS), worlds
`world_a2.zag` (A-confounded-chain) and `world_b2.zag` (B-contextual-delay).

## Question

Which components of F2 are load-bearing, and what breaks F2? F2 is
enumerate-then-select: passive candidates, Cartesian hypothesis product,
disagreement-driven experiments, model-based planning. The memorization
control showed the causal model beats a memorizer. This wave asks: does the
experiment loop matter, does disagreement targeting matter, does the context
machinery matter, and what happens when the truth is outside the hypothesis
family or invisible to passive data?

## Part 1: Ablations (modified learner copies, frozen worlds)

Three learner variants are built by copying the frozen learner verbatim and
applying ONLY the specified edit. All other code is byte-identical to
`1eb66765d:autosci2_learner.zag`. Each variant is run on World A and World B,
3 runs each, byte-identical determinism required.

### ABL1: no experiment loop (passive only)

Edit: in `L_run`, guard the experiment `while(1==1)` loop so it is skipped
entirely when the variant flag is set; set `exhausted=1`; proceed directly to
convergence adjudication and goal planning under h0 (first alive hypothesis,
index 0). No other change.

What it tests: whether passive-data candidates alone suffice for the goal,
or the experiment loop does load-bearing work.

Prediction ABL1-A: GOAL_REAL=0. hyp0 is the lexicographically first candidate
combination, which the frozen run showed is wrong for Y (it selects
(X->Y d3) over the true (Z->Y d1)); with no experiments to kill it, the plan
is built on a false model and fails in reality.

Prediction ABL1-B: GOAL_REAL_B2=0. hyp0 is (X->Y d2 ALWAYS); B2 planning under
a K-blind model cannot satisfy the (Y=1,K=0) triple against a K-sensitive
world.

### ABL2: random experiments instead of disagreement targeting

Edit: replace the `L_find` call with a new `L_find_rand` that generates one
random sequence per round (fixed LCG seed 777, persistent across rounds via a
4-byte seed buffer; random depth 1..6; random digits over the same B-symbol
alphabet; if no OBSERVE digit is drawn the last position is forced to
OBSERVE var 0). Predictions for alive hypotheses are still simulated with
`L_sim` for elimination bookkeeping. The sequence is executed for real
regardless of disagreement. Loop continues until nalive<=1, round cap 40, or
observation budget exceeded. No world calls inside the finder (pure
simulation, same as `L_find`).

What it tests: whether disagreement targeting matters, or any experiments
suffice.

Prediction ABL2-A/B: convergence is slower and noisier than the guided run
(World A guided: 2 experiments; World B guided: 1). Truth may or may not
survive depending on the fixed seed draw. Measured: experiments used,
nalive, truth alive, GOAL_REAL.

### ABL3: no context in the rule language

Edit: in `L_run`, pass `gctx=-1` (instead of `ctxvar`) to `L_gencands` when
the variant flag is set, so only ALWAYS candidates are generated.

What it tests: whether the contextual rule machinery is load-bearing.

Prediction ABL3-A: byte-identical to the frozen World A run (World A already
has ctxvar=-1; this variant is a no-op control verifying the harness).

Prediction ABL3-B: K2-R1 FAIL (nhyp=1; only (X->Y d2 ALWAYS) fits passive
data since K=0 throughout passive), planning proceeds K-blind, GOAL_REAL_B2=0
(the real world is K-sensitive and the goal setup starts at K=1).

## Part 2: Adversary (frozen learner, new sealed worlds)

The learner is used VERBATIM from `1eb66765d` (no modifications). Two new
world files implement the full `w_*` interface. Both worlds are designed and
sealed in this prereg, before any implementation exists.

### ADV1: conjunctive truth (outside the single-cause family)

Variables: X(0,ctrl), Z(1,ctrl), Y(2), W(3,dummy). nctrl=2, ctxvar=-1,
goal_mode=0, w_plan_maxd=8.

Sealed truth: Y(t) = X(t-2) AND Z(t-1). X and Z are pulsed (SET writes only
the current step; no persistence). W is always 0.

Passive schedule: env SETs X at t=2 and t=8; env SETs Z at t=3 and t=9.

Derivation (sealed): Y=1 at t=4 (X(2)&Z(3)) and t=10 (X(8)&Z(9)), else 0.
Candidates for Y: (X->Y d2) fits (X=1 at 2,8 gives Y=1 at 4,10); (Z->Y d1)
fits (Z=1 at 3,9 gives Y=1 at 4,10); no other delay fits. Z gets the spurious
but fitting candidate (X->Z d1). NHYP=4 over evars [Z,Y].

Predicted mechanism: the experiment loop kills hypotheses until one survivor
remains; the survivor is a wrong single-cause rule; the loop stops at
nalive==1 (it never considers that the family itself is wrong); the planner
builds a plan under the wrong model; the plan fails in reality.

Predicted outcome: FOOLED=1, i.e. SURVIVORS has 1 entry, PLAN is found,
GOAL_REAL=0. (If instead all hypotheses die, the learner reaches the
TRUTH_LOST path; that outcome is also recorded as informative.)

Goal: final-state Y=1 (w_goal_met: vals[2]==1). w_goal_setup: no-op.

### ADV2: silent cause (invisible to passive data)

Variables: X(0,ctrl), Z(1,ctrl), Y(2). nctrl=2, ctxvar=-1, goal_mode=0,
w_plan_maxd=8.

Sealed truth: Y(t) = X(t-2) AND Z(t-1), same as ADV1.

Passive schedule: env SETs X at t=2 and t=8. Z is NEVER set in passive
(stays 0). Y is always 0 in passive.

Derivation (sealed): no candidate for Y is generated (X=1 never coincides
with Y=1; Z never 1), so ne=0, nhyp=1, the experiment loop exhausts
immediately, and no plan is found. Yet the goal IS achievable: the real plan
[SX,W,SZ,W] gives Y(2)=X(0)&Z(1)=1.

Predicted outcome: MISSED=1, i.e. "PLAN none found", GOAL_REAL never
attempted, although a real achieving plan exists. This tests whether F2 can
discover a cause that passive data never implicates (it cannot: hypotheses
come only from passive correlations; the experiment loop never proposes
manipulating an unvaried variable).

Goal: final-state Y=1. w_goal_setup: no-op.

## Kill bars

- K1 PASS if: all three ablation variants are implemented with ONLY the
  specified edits (verified by diff against frozen source), and run on both
  frozen worlds.
- K2 PASS if: ADV1 and ADV2 are implemented exactly as sealed above (world
  parameters, truth, passive schedules, goals) with the learner used verbatim
  from `1eb66765d`.
- K3 PASS if: every run is pure Zag (no Python in source, build, execution,
  or analysis), wave docs contain zero em-dash bytes, and each configuration
  is 3/3 byte-identical with md5 recorded.

## Verdict rule

Report ABLATION-TESTED. For each ablation and adversary world, report the
observed mask, NHYP, nalive, exhausted, GOAL_REAL, OBS_USED, and md5, plus
whether the preregistered prediction was confirmed or refuted. Conclude which
components are load-bearing: the experiment loop (ABL1), disagreement
targeting (ABL2), context machinery (ABL3), and state the adversary findings
for out-of-family truth (ADV1) and silent causes (ADV2). No SURVIVES claim is
made; this wave feeds promotion steps 6 (alternative-explanation attack) and
7 (OOD test).

## Purity and determinism

- Pure Zag only. No Python anywhere including analysis and /tmp scratch.
- No em dashes in wave documentation.
- 3/3 byte-identical per configuration; exit 0; zero stderr.
- Commits local on tnn-native-lab, owned path only:
  docs/lab/research-lead/overnight-20260928/f2_ablation/
