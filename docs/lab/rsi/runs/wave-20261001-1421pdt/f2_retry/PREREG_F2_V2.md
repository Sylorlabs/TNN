# PREREG_F2_V2: Autonomous Scientist, Harder Sustained Goal on Fresh Sealed Worlds

Date: 2026-10-01. Status: FROZEN. This prereg is written before any
implementation file for this wave exists. No `.zag` for F2 v2 exists at
freeze time. The prereg must be committed alone before implementation;
the commit-order self-check (prereg commit strictly precedes the
implementation commit) applies to the builder wave.

## 1. Objective

Test the F2 autonomous-scientist loop (hypotheses from passive data,
disagreement-driven experiment construction from primitives, elimination,
model-based goal planning) against FRESH sealed worlds with a HARDER
sustained goal than any prior F2 wave. The loop itself is reused
unchanged; only the sealed worlds and the goal predicate change.

## 2. Prior history and why this is v2 (read first)

- F2 v1 (autosci, prereg 2a87efa77, result 4ebde580a, 2026-09-30):
  BUILD-FAIL on K-AS5b. The loop worked in both sealed worlds. World B's
  goal (transient Y=1 within 6 steps) was a weak goal instance: ~5% random
  base rate, and the frozen random control hit 1/20 on the a priori seed
  12345 (the hitting sequence contained the solution pattern as a
  subsequence). Bar failure, not loop failure.
- F2 retry (autosci2, prereg b9ab0acb6, result 2026-09-30): the harder
  World B goal B2 (three consecutive steps with OBS Y=1 AND OBS K=0;
  pre-freeze calibration 0/160 random) achieved BUILD-PASS on all seven
  kill bars, with no architectural changes. The standing order "retry with
  a harder sustained goal" was thereby fulfilled. Later the lane closed
  its memorization control (F2 beats memorization 2-0) and its
  independent reproduction (md5-identical rebuild).

This v2 is therefore NOT a repeat of the B2 retry. It is the next harder
step, and it is harder than B2 in four precise ways:

1. Two independent contextual laws instead of one (9 passive hypotheses,
   not 2).
2. Two delays (2 and 3) managed simultaneously in one plan, not one delay.
3. Two context variables, BOTH actively verified by observation (J=0 and
   K=1). In B2 the K=0 context was self-maintaining via variable decay; in
   v2 the contexts are persistent (see section 4), so the learner must
   actively establish the correct values and they are checked at every
   sustain step.
4. Fresh sealed worlds the F2 loop has never seen (World C below). B2 ran
   on v1's World B physics; a pass there does not show the loop's
   sustained-control achievement transfers to new physics.

## 3. Changes from AUTOSCI2 (explicit, exhaustive)

1. World B (contextual delay, delay 2, single context K) is RETIRED as a
   test world. It is replaced by World C (section 5).
2. World A (confounded chain) is REPLICATED EXACTLY (same physics, goal,
   planner, control) as a regression anchor.
3. New goal predicate C2: three consecutive steps with
   (Y1=1 AND J=0 AND Y2=1 AND K=1), replacing B2's (Y=1 AND K=0).
4. Goal planner alphabet for World C: {SET X, CLR X, SET J, CLR J, SET K,
   CLR K, WAIT} (7 symbols), depths 1..9 (B2 used 5 symbols, depths 1..8).
5. New fixed measurement protocol SUFFIX_C = [OBS Y1, OBS J, OBS Y2, OBS K,
   WAIT] repeated 3 times (15 primitives; disclosed here; contains no
   manipulations).
6. Context variables are persistent across WAIT (section 4). This is a
   disclosed physics property, not a learner change.
7. K-R6 (observation economy) is 28, not 18: World C needs 12 verification
   observations by design (4 per round x 3 rounds) versus 6 in B2, and the
   larger hypothesis space needs more experiments.
8. All else identical to the F2 loop: passive phase, candidate generation,
   cross-product hypotheses, experiment loop (depths 1..6), determinism
   requirements.

## 4. Shared physics (authored substrate, not the discovery target)

Discrete steps t = 0, 1, 2, ... . Each variable has a binary value per
step. History is retained.

- SET v: variable v becomes 1 at the current step.
- CLR v: variable v becomes 0 at the current step.
- WAIT: advance to t+1. New values: for each rule (cause c, effect e,
  delay d, context) in the ACTIVE rule set, e becomes 1 at t+1 iff c was 1
  at (t+1-d) and the context held at (t+1-d). Declared context variables
  are PERSISTENT: they retain their value across WAIT and change only via
  SET/CLR. Every other variable with no applicable rule becomes 0 (decay).
  No rule may have delay 0.
- OBSERVE v: read the current value of v. Costs 1 unit of observation
  budget. State-neutral (does not advance t or change values).
- RESET: laboratory hygiene. Restores all variables to 0 at t=0. Free.
  Used between experiments and before goal execution. Never part of a
  constructed sequence. Disclosed here.

A rule context is one of: ALWAYS, or (V == 0), or (V == 1) for each of the
world's declared context variables, or -1 when the world declares none.
Persistence applies to declared context variables only; it is a generic
property of the declared set, not a per-world special case.

The world advances with its SEALED true rule set. The learner simulates
with hypothesized rule sets. Both use the same generic advance function.
The learner never reads the sealed rule set (structural information
barrier; verified by source audit).

## 5. Sealed worlds (FROZEN; hidden from the learner)

### World A: confounded chain (REPLICATED EXACTLY from F2/AUTOSCI2)

- Variables: X=0, Z=1, Y=2, D=3. Controllable: X, D. Context variable: none.
- TRUE LAWS (sealed): (X -> Z, delay 2, ALWAYS); (Z -> Y, delay 1, ALWAYS);
  (X -> D, delay 1, ALWAYS). D is a confounder.
- Passive schedule (frozen): 12 steps, t = 0..11. Environment SETs X at
  t = 2 and t = 8. Learner OBSERVEs all variables each step (free).
- Goal A (unchanged): reach a step with X = 1 AND Y = 1 AND D = 0
  simultaneously. Goal planner: manipulations + WAIT, depths 1..8.
  Random control: 20 sequences, length plan_length+2, over {SET X, CLR X,
  SET D, CLR D, WAIT}. Bar: 0/20.

### World C: dual contextual delay (FRESH sealed physics)

- Variables: X=0, Y1=1, Y2=2, J=3, K=4. Controllable: X, J, K. Declared
  context variables: J, K (persistent per section 4).
- TRUE LAWS (sealed): (X -> Y1, delay 2, context J == 0);
  (X -> Y2, delay 3, context K == 1). Under J == 1, X does nothing to Y1;
  under K == 0, X does nothing to Y2.
- Passive schedule (frozen): 14 steps, t = 0..13. Environment SETs X at
  t = 2, t = 6, and t = 10. J = 0 and K = 1 throughout. Learner OBSERVEs
  all variables each step (free).
- Predicted passive ambiguity (design calculation, verified at runtime):
  Y1 candidates {(X,2,ALWAYS), (X,2,J=0), (X,2,K=1)}; Y2 candidates
  {(X,3,ALWAYS), (X,3,J=0), (X,3,K=1)}. J=0 and K=1 are constant during the
  passive phase, so they are spuriously sufficient and must be killed by
  constructed experiment. Cross product: 9 hypotheses. K3-R1 requires at
  least 2; the exact count is verified at runtime, not frozen.
- Goal C2 (FROZEN): SUSTAINED DUAL CONTEXTUAL CONTROL. Goal setup
  (disclosed): environment establishes J = 1; RESET to t=0 (K = 0 by
  reset). The learner executes its full plan (M + SUFFIX_C) for real
  exactly once. GOAL_REAL = 1 iff the real trajectory contains three
  consecutive steps s, s+1, s+2 such that at each step Y1 = 1 AND J = 0
  AND Y2 = 1 AND K = 1. Rationale: the learner must discover both gating
  contexts, flip both (CLR J, SET K), manage delay-2 and delay-3 timing
  simultaneously by re-asserting X at the correct cadence, and hold both
  contexts across three steps. A lucky transient firing cannot satisfy
  three consecutive joint observations.
- Goal planner (C2): iterative deepening over {SET X, CLR X, SET J, CLR J,
  SET K, CLR K, WAIT} (7 symbols), depths 1..9, lexicographic order
  (symbol order 0..6 as listed; most-significant digit first; depths
  ascending). For each M, simulate M followed by 3 WAITs under the first
  surviving hypothesis (pure simulation, zero world calls). The 3 WAITs
  are trajectory-equivalent to the SUFFIX_C observation rounds because
  OBSERVE is state-neutral (disclosed here). Select the first M
  (lexicographic, shortest depth) whose simulated trajectory contains
  three consecutive steps with (Y1=1, J=0, Y2=1, K=1). The full executed
  plan is M + SUFFIX_C.
- SUFFIX_C (fixed measurement protocol, disclosed, not searched):
  [OBS Y1, OBS J, OBS Y2, OBS K, WAIT] repeated 3 times (15 primitives;
  contains no manipulations; not a plan literal for K3-R2 purposes).
- Random control (C2): 20 sequences from a fixed-seed LCG (deterministic,
  a priori seed 12345, disclosed), each of length len(M)+17 over the
  7-symbol manipulation alphabet {SET X, CLR X, SET J, CLR J, SET K, CLR K,
  WAIT}. The 7-symbol alphabet is the generous-to-control choice: every
  symbol acts (no no-op OBS symbols padding the length). Executed for real
  with RESET and goal setup. Count sequences whose real trajectory
  contains three consecutive steps with (Y1=1, J=0, Y2=1, K=1) (semantic
  predicate: the control need not observe, only cause; this is the most
  generous fair reading). Bar: 0/20.

## 6. Learner architecture (generic; identical code for both worlds; UNCHANGED from F2)

1. Passive phase: record the passive trace (12 steps World A, 14 steps
   World C).
2. Candidate generation (generic): for each effect variable e, each cause
   variable c != e, each delay d in 1..4, each context in the world's
   context set: keep the rule if sufficiency holds on the passive trace
   (every c=1 with context at t implies e=1 at t+d) and the rule fired at
   least twice. No other filter.
3. Hypotheses: cross product of one candidate rule per variable that has
   at least one candidate; variables with none are exogenous. Each
   hypothesis is data (a rule set). No per-hypothesis code.
4. Experiment loop:
   a. Iterative deepening over depths 1..6. At each depth, compose EVERY
      sequence from the primitive alphabet (base-B counting; no sequence
      pre-exists). Skip sequences with no OBSERVE.
   b. Simulate each sequence under every live hypothesis (pure simulation;
      zero real-world actions).
   c. Select the FIRST sequence (lexicographic) where the predicted
      observation vectors disagree. Log the sequence and every live
      hypothesis's prediction.
   d. If none found at any depth: stop (search exhaustion).
   e. Check observation budget; RESET; execute the selected sequence
      against the sealed world exactly once; record actual observations.
   f. Eliminate every hypothesis whose prediction disagrees with actual.
      If zero remain: FAIL. If one remains: stop.
   g. Repeat.
5. Goal phase:
   - World A: identical to F2 (manipulations + WAIT, depths 1..8, first
     sequence whose simulated final state satisfies X=1,Y=1,D=0; assert all
     survivors agree; RESET, setup, execute, OBSERVE, verify).
   - World C: C2 protocol as defined in section 5 above.
6. Random-action control: as defined per-world in section 5.

Primitive alphabet for experiment search: for each controllable variable
v: SET v, CLR v; plus WAIT; plus OBSERVE v for each variable. Goal
planner alphabet (World A): SET/CLR per controllable plus WAIT. Goal
planner alphabet (World C): SET/CLR per controllable plus WAIT
(7 symbols); SUFFIX_C is the fixed measurement protocol.

## 7. Kill bars (numbered; frozen)

- K3-R1 (passive ambiguity): after the passive phase, the learner holds at
  least 2 hypotheses fully consistent with the passive trace, in EACH
  world. Fewer: FAIL.
- K3-R2 (construction, not enumeration): the source contains no finite
  list of complete experiments or complete goal plans (verified by source
  audit: no experiment/plan sequence literal appears in source;
  construction is exclusively iterative-deepening composition over
  primitives; SUFFIX_C is the preregistered fixed measurement protocol,
  disclosed in this prereg, containing no manipulations). Additionally
  the executed experiments AND the goal plans differ across the two worlds
  in composition. A complete experiment or goal plan found as a literal in
  source (other than the preregistered SUFFIX_C): FAIL.
- K3-R3 (disagreement-driven): every executed experiment is logged with
  the per-hypothesis predicted observation vectors showing disagreement,
  and the world-action counter proves zero real-world actions occurred
  during search (only RESET plus the single selected execution). An
  executed experiment without logged prior disagreement, or any world
  action during search: FAIL.
- K3-R4 (convergence): World A: the true hypothesis
  {Z<-(X,2), Y<-(Z,1), D<-(X,1)} survives, and the loop terminates by
  search exhaustion to depth 6 (survivors form an observational
  equivalence class). World C: the loop terminates with exactly one
  survivor, equal to the true law pair {(X,2,J=0), (X,3,K=1)}. Otherwise:
  FAIL.
- K3-R5 (model to goal): World A: the learner's planned sequence achieves
  Goal A for real, verified by OBSERVE; AND the random-action control
  achieves Goal A 0/20. World C: the learner's full plan (M+SUFFIX_C)
  achieves Goal C2 for real (three consecutive steps with
  (Y1=1,J=0,Y2=1,K=1) on the real trajectory); AND the random-action
  control (7-symbol alphabet, length len(M)+17, a priori seed 12345)
  achieves the predicate 0/20. Otherwise: FAIL.
- K3-R6 (observation economy): total active-phase OBSERVE actions across
  both worlds is at most 28 (passive observations are free given data).
  More: FAIL. (Raised from AUTOSCI2's 18 because Goal C2 requires 12
  verification observations by design versus 6 in B2, and the 9-hypothesis
  space needs more discriminating experiments.)
- K3-R7 (determinism and purity): 3/3 runs byte-identical per world; pure
  Zag (no Python at any stage, including analysis and editing of wave
  artifacts); no em dashes in wave documentation. Otherwise: FAIL.

BUILD-PASS requires all seven bars in both worlds. Any FAIL is BUILD-FAIL.

## 8. Design calculations (pre-freeze calibration; not wave implementation)

A scratch pure-Zag calibration program (/tmp/f2v2_calib.zag, not part of
the wave, never committed) implemented the World C physics and tested,
3/3 byte-identical runs (sha256
16113f7862c6738482691c337f92744aaed4a1a38b889eac4e7b11f36c6711f1):

1. Learner plan achievability: hand-designed
   M = [CLR J, SET K, SET X, WAIT, SET X, WAIT, SET X, WAIT, SET X]
   (9 primitives) achieves the 3-consecutive joint predicate in
   simulation under the true laws. Result: hand_M_achieves=1.
2. Planner search (the exact procedure the wave planner will use:
   depths 1..9, 7 symbols, lexicographic, first success): found
   M = [SET X, CLR J, SET K, WAIT, SET X, WAIT, SET X, WAIT, SET X]
   (9 primitives; lexicographically first valid M; differs from the hand
   M but equally valid) after 9,769,768 simulations. Depths 1..8 exhaust
   with no success, confirming depth 9 is minimal for this goal (2
   context ops + 4 X-assertions + 3 WAITs). Full calibration run wall
   time ~55 s.
3. Random base rate: 20 random sequences per seed (length 26 = 9+15+2,
   7-symbol alphabet, continuing LCG stream), 8 seeds
   (12345, 20264, 30311, 42424, 55555, 66666, 77777, 88888), 160 sequences
   total, semantic trajectory predicate (generous: cause, not observe).
   Triple joint-predicate hits: 0/160. The v1 failure mode (lucky
   transient achievement, ~5% base rate) cannot satisfy the sustained
   dual predicate.

These are design calculations informing the prereg, not wave results. The
wave implementation is independent.

## 9. Honest boundaries (what BUILD-PASS would and would not establish)

A BUILD-PASS on all seven bars would establish: the unchanged F2 loop
achieves sustained dual contextual control (two gating variables, two
delays, three consecutive joint observations) in fresh sealed worlds it
has never seen, via hypotheses from passive data, disagreement-driven
experiment construction, and model-based planning. That is bounded L2
structural learning.

It would NOT establish, and no claim to the contrary may be made:

- L3 representational invention. Against Criterion 0: (C0-A) FAILS, the
  rule semantics (cause/effect/delay/context) are researcher-authored and
  the learner fills in edges, delays, and contexts; (C0-B) FAILS, the
  solution space (rule sets over a researcher-fixed alphabet) is
  researcher-enumerated and the loop is enumerate-then-select, the same
  family H-CAUSALEXP-CONSTRUCT was L3-killed under; (C0-C) is NOT TESTED
  (two worlds, one law family, mechanism frozen throughout); (C0-D) is
  only partially met (the learned model is reused for goal planning
  within the wave, not across unforeseen forms).
- Generality beyond the tested worlds. Even a full pass is a targeted
  result on two sealed worlds, not a broad capability claim (the same
  discipline as the FW1-FW9 regression-battery ruling: a pass on a fixed
  battery establishes no broad generality).
- Escape from the enumerate-then-select family. DDES remains the lane
  that escapes it; F2 does not.

## 10. Governance

Pure Zag only. No Python anywhere in this wave (implementation, build,
execution, analysis, artifact editing). This prereg is frozen before any
implementation file exists; the builder wave must commit this prereg
alone first (commit-order self-check: prereg commit strictly precedes the
implementation commit). Commits local on tnn-native-lab; nothing pushed.
Builder reports BUILD-PASS or BUILD-FAIL only; no SURVIVES claim
(promotion pipeline steps 4-11 remain for the parent to schedule).

## 11. Architecture accounting (prereg step)

- Cognition source lines added: 0 (writing-only step; no implementation).
- New hardcoded semantic cases: 0.
- New modes / bridges / routers: 0.
- New task-specific handlers: 0.
- New learner-state structures: 0.
- The F2 learner loop is reused unchanged. The sealed worlds are authored
  test substrate, not cognition. Context-variable persistence (section 4)
  is a generic property of the declared context-variable set, not a
  dedicated semantic case: no world-specific rule, mode, or handler is
  introduced.

## 12. Harder-case coverage (design map; verified at runtime)

- Interventions requiring 2+ manipulations: World C goal plan (3: CLR J,
  SET K, plus X cadence).
- Interventions of 4+ total primitives: World C goal plan (9 primitives).
- Confounder: D in World A (replication).
- Delayed effects: delays 1, 2, 3 in World A; delays 2 and 3
  simultaneously in World C.
- Contextual laws: two independent single-variable gates in World C
  (J==0, K==1), with spurious always-on and wrong-variable candidates
  that passive data cannot exclude.
- Observation cost: hard budget of 28 with full accounting.
