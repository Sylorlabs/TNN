# PREREG_AUTOSCI: Autonomous Scientific Discovery (F2)

Date: 2026-09-30. Status: FROZEN. This prereg is committed alone before any
implementation. No `.zag` for this wave exists at commit time.

## 1. Objective

Push H-CAUSALEXP beyond authored experiment candidates into a true autonomous
scientist. H-CAUSALEXP-CONSTRUCT (BUILD-PASS 7/7) showed a learner can construct
multi-step interventions from primitives, but its hypotheses were authored
rule-sets. This wave: the learner receives ONLY generic primitive actions and
sensors; the environment contains sealed latent laws; several causal models
explain the passive observations equally well. The learner must maintain
multiple explanations, identify disagreement, construct experiments from
primitives (never from an enumerated list), execute, observe, update, build a
predictive model, and use it to accomplish a goal.

## 2. Shared physics (authored substrate, not the discovery target)

Discrete steps t = 0, 1, 2, ... . Each variable has a binary value per step.
History is retained.

- SET v: variable v becomes 1 at the current step.
- CLR v: variable v becomes 0 at the current step.
- WAIT: advance to t+1. New values: for each rule (cause c, effect e, delay d,
  context) in the ACTIVE rule set, e becomes 1 at t+1 iff c was 1 at (t+1-d)
  and the context held at (t+1-d). Variables with no applicable rule become 0
  (decay). No rule may have delay 0.
- OBSERVE v: read the current value of v. Costs 1 unit of observation budget.
- RESET: laboratory hygiene. Restores all variables to 0 at t=0. Free. Used
  between experiments and before goal execution. Never part of a constructed
  sequence. Disclosed here.

A rule context is one of: ALWAYS, or (K == 0), or (K == 1), where K is the
world's declared context variable, or -1 when the world declares none.

The world advances with its SEALED true rule set. The learner simulates with
hypothesized rule sets. Both use the same generic advance function. The learner
never reads the sealed rule set (structural information barrier; verified by
source audit).

## 3. Sealed worlds (FROZEN; hidden from the learner)

### World A: confounded chain

- Variables: X=0, Z=1, Y=2, D=3. Controllable: X, D. Context variable: none.
- TRUE LAWS (sealed): (X -> Z, delay 2, ALWAYS); (Z -> Y, delay 1, ALWAYS);
  (X -> D, delay 1, ALWAYS). D is a confounder: it always follows X and is
  correlated with Y, but causes nothing.
- Passive schedule (frozen): 12 steps, t = 0..11. Environment SETs X at t = 2
  and t = 8. Learner OBSERVEs all variables each step (passive observations are
  free; they are given data, not active experimentation).
- Predicted passive ambiguity (design calculation): candidate rules passing
  sufficiency with at least 2 firings are Z: {(X,2),(D,1)}; Y: {(Z,1),(X,3),
  (D,2)}; D: {(X,1)}; X: none (exogenous). That yields 2*3*1 = 6 hypotheses,
  all consistent with the passive trace. The bar K-AS1 requires at least 2;
  the exact count is verified at runtime, not frozen.
- Goal A (assigned): reach a step with X = 1 AND Y = 1 AND D = 0
  simultaneously. Rationale: D is driven by X, so D = 0 while X = 1 requires
  understanding the confounder's timing. A design-calculated plan is
  [SET X, WAIT, WAIT, WAIT, SET X] (5 primitives, 2 manipulations); the
  learner must find its own plan by searching under its learned model. The
  exact plan the learner finds is NOT frozen.

### World B: contextual delay

- Variables: X=0, Y=1, K=2. Controllable: X, K. Context variable: K.
- TRUE LAW (sealed): (X -> Y, delay 2, context K == 0). Under K == 1, X does
  nothing to Y.
- Passive schedule (frozen): 12 steps. Environment SETs X at t = 2 and t = 8.
  K = 0 throughout. Learner OBSERVEs all variables each step (free).
- Predicted passive ambiguity: Y candidates {(X,2,ALWAYS), (X,2,K=0)}; X and K
  exogenous. That yields 2 hypotheses. K-AS1 requires at least 2.
- Goal B (assigned): the environment establishes K = 1 (goal setup, disclosed),
  then the learner must reach Y = 1 within 6 steps. Rationale: the plan must
  first restore K = 0 (CLR K), which requires the learned contextual knowledge.
  A design-calculated plan is [CLR K, SET X, WAIT, WAIT] (4 primitives,
  2 manipulations); the learner finds its own.

## 4. Learner architecture (generic; identical code for both worlds)

1. Passive phase: record the 12-step trace.
2. Candidate generation (generic): for each effect variable e, each cause
   variable c != e, each delay d in 1..4, each context in the world's context
   set ({ALWAYS} if no context variable, else {ALWAYS, K=0, K=1}): keep the rule
   if sufficiency holds on the passive trace (every c=1 with context at t
   implies e=1 at t+d) and the rule fired at least twice. No other filter.
3. Hypotheses: cross product of one candidate rule per variable that has at
   least one candidate; variables with none are exogenous (no rule). Each
   hypothesis is data (a rule set). There is no per-hypothesis code.
4. Experiment loop:
   a. Iterative deepening over depths 1..6. At each depth, compose EVERY
      sequence from the primitive alphabet (base-B counting, B = 2*nctrl + 1 +
      nvars; no sequence pre-exists). Skip sequences with no OBSERVE.
   b. Simulate each sequence under every live hypothesis with the generic
      delay-rule simulator (pure simulation; zero real-world actions).
   c. Select the FIRST sequence (lexicographic) where the predicted
      observation vectors disagree across live hypotheses. Log the sequence
      and every live hypothesis's prediction (the "because" evidence).
   d. If none found at any depth: stop (search exhaustion).
   e. Check observation budget; RESET; execute the selected sequence against
      the sealed world exactly once; record actual observations.
   f. Eliminate every hypothesis whose prediction disagrees with actual.
      If zero remain: FAIL (truth lost). If one remains: stop.
   g. Repeat.
5. Goal phase: search primitive sequences (manipulations + WAIT only, no
   OBSERVE) at depths 1..8 (World A) or 1..6 (World B), simulating under the
   first surviving hypothesis, for the first sequence whose simulated final
   state satisfies the assigned goal. Assert all survivors agree on the
   plan's predicted goal-variable values. RESET, apply goal setup, execute
   the plan for real, OBSERVE the goal variables, verify.
6. Random-action control: 20 sequences from a fixed-seed LCG (deterministic),
   each of length plan_length + 2 over the planner alphabet, executed for
   real with RESET and goal setup; count goal achievements.

Primitive alphabet for search: for each controllable variable v: SET v, CLR v;
plus WAIT; plus OBSERVE v for each variable. Planner alphabet: SET/CLR per
controllable variable plus WAIT (no OBSERVE inside plans; verification
observes after).

## 5. Kill bars (numbered; frozen)

- K-AS1 (passive ambiguity): after the passive phase, the learner holds at
  least 2 hypotheses fully consistent with the passive trace, in EACH world.
  Fewer: FAIL.
- K-AS2 (construction, not enumeration): the source contains no finite list
  of complete experiments (verified by source audit: no experiment sequence
  literal appears in source; construction is exclusively iterative-deepening
  composition over primitives). Additionally the executed experiments differ
  across the two worlds in composition. A complete experiment found as a
  literal in source: FAIL (downgrade to L2).
- K-AS3 (disagreement-driven): every executed experiment is logged with the
  per-hypothesis predicted observation vectors showing disagreement, and the
  world-action counter proves zero real-world actions occurred during search
  (only RESET plus the single selected execution). An executed experiment
  without logged prior disagreement, or any world action during search: FAIL.
- K-AS4 (convergence): World A: the true hypothesis
  {Z<-(X,2), Y<-(Z,1), D<-(X,1)} survives, and the loop terminates by search
  exhaustion to depth 6 (the survivors form an observational equivalence
  class; no sequence to depth 6 distinguishes them). World B: the loop
  terminates with exactly one survivor, equal to the true law {(X,2,K=0)}.
  Otherwise: FAIL.
- K-AS5 (model to goal): the learner's planned sequence achieves the assigned
  goal for real, verified by OBSERVE, in EACH world; AND the random-action
  control achieves the goal 0/20 in EACH world. Otherwise: FAIL.
- K-AS6 (observation economy): total active-phase OBSERVE actions across both
  worlds is at most 12 (passive observations are free given data). More: FAIL.
- K-AS7 (determinism and purity): 3/3 runs byte-identical; pure Zag (no Python
  at any stage, including analysis and editing of wave artifacts); no em
  dashes in wave documentation. Otherwise: FAIL.

BUILD-PASS requires all seven bars in both worlds. Any FAIL is BUILD-FAIL.

## 6. Harder-case coverage (design map; verified at runtime)

- Interventions requiring 2 manipulations: World B experiment (context + cause)
  and World A goal plan.
- Interventions of 4+ total primitives: World B experiment (5 primitives),
  World A goal plan (5 primitives). Counting convention: primitives.
- Confounder: D in World A.
- Delayed effects: delays 1, 2, 3 in World A; delay 2 in World B.
- Contextual law: K-gated rule in World B.
- Observation cost: hard budget of 12 with full accounting.

## 7. Governance

Pure Zag only. No Python anywhere in this wave. Prereg committed alone before
any implementation file exists. Commits local on tnn-native-lab, owned path
only: docs/lab/research-lead/overnight-20260928/autosci/. Builder reports
BUILD-PASS or BUILD-FAIL only; no SURVIVES claim (promotion pipeline steps
4-11 remain for the parent to schedule).
