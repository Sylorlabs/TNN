# PREREG_AUTOSCI2: Autonomous Scientific Discovery Retry (F2-Retry)

Date: 2026-09-30. Status: FROZEN. This prereg is committed alone before any
implementation. No `.zag` for this wave exists at commit time.

## 1. Objective

Re-run the F2 autonomous scientist (prereg 2a87efa77, result 4ebde580a:
BUILD-FAIL on K-AS5b) with a harder World B goal. F2's loop worked in both
worlds; the frozen bar caught a weak goal instance (transient Y=1, random
base rate ~5%), not a broken mechanism. This wave changes ONLY the World B
goal predicate (transient achievement to sustained contextual control) and
the World B goal-planning protocol. No architectural changes. World A is
replicated exactly.

## 2. Changes from F2 (explicit, exhaustive)

1. World B goal predicate: "reach Y=1 within 6 steps" is REPLACED by
   "sustained contextual control": three consecutive steps at which
   OBSERVE Y reads 1 AND OBSERVE K reads 0. Rationale: transient Y=1 can
   be hit by luck (~5%); sustaining Y=1 for three consecutive steps while
   holding the context requires genuine understanding of the delay-2
   contextual law and its timing. The K=0 observation verifies the context
   was maintained, which is the point of the contextual law.
2. World B goal planner: searches manipulation sequences M over
   {SET X, CLR X, SET K, CLR K, WAIT} (5 symbols), depths 1..8, for the
   first M (lexicographic, shortest) whose simulated execution of
   M + SUFFIX satisfies the triple predicate. SUFFIX = [OBS Y, OBS K, WAIT]
   repeated 3 times (9 primitives; fixed measurement protocol, disclosed
   here, not searched). The full executed plan is M + SUFFIX.
3. World B random control alphabet: {SET X, CLR X, SET K, CLR K, WAIT,
   OBS Y, OBS K} (7 symbols). Length = len(M+SUFFIX)+2. The control must
   have access to observations, otherwise the triple predicate is
   unsatisfiable by construction and the control is vacuous. This is the
   fair, generous-to-control choice.
4. Observation budget: K-AS6 (<=12) is replaced by K2-R6 (<=18), justified
   because the harder goal requires 6 verification observations in World B
   (3x OBS Y + 3x OBS K) versus 1 in F2.
5. All else identical to F2: passive phase, candidate generation,
   hypotheses, experiment loop (depths 1..6), World A (goal, planner,
   control), determinism requirements.

## 3. Shared physics (identical to F2, authored substrate)

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

A rule context is one of: ALWAYS, or (K == 0), or (K == 1), where K is the world's declared context variable, or -1 when the world
declares none.

The world advances with its SEALED true rule set. The learner simulates with
hypothesized rule sets. Both use the same generic advance function. The
learner never reads the sealed rule set (structural information barrier;
verified by source audit).

## 4. Sealed worlds (FROZEN; hidden from the learner; identical to F2 except Goal B)

### World A: confounded chain (UNCHANGED from F2)

- Variables: X=0, Z=1, Y=2, D=3. Controllable: X, D. Context variable: none.
- TRUE LAWS (sealed): (X -> Z, delay 2, ALWAYS); (Z -> Y, delay 1, ALWAYS);
  (X -> D, delay 1, ALWAYS). D is a confounder.
- Passive schedule (frozen): 12 steps, t = 0..11. Environment SETs X at t = 2
  and t = 8. Learner OBSERVEs all variables each step (free).
- Goal A (unchanged): reach a step with X = 1 AND Y = 1 AND D = 0
  simultaneously. Goal planner: manipulations + WAIT, depths 1..8.
  Random control: 20 sequences, length plan_length+2, over {SET X, CLR X,
  SET D, CLR D, WAIT}. Bar: 0/20 (F2 achieved 0/20 on 4 seeds).

### World B: contextual delay (physics UNCHANGED; goal REPLACED)

- Variables: X=0, Y=1, K=2. Controllable: X, K. Context variable: K.
- TRUE LAW (sealed): (X -> Y, delay 2, context K == 0). Under K == 1, X does
  nothing to Y.
- Passive schedule (frozen): 12 steps. Environment SETs X at t = 2 and t = 8.
  K = 0 throughout. Learner OBSERVEs all variables each step (free).
- Predicted passive ambiguity (same as F2): Y candidates {(X,2,ALWAYS),
  (X,2,K=0)}; 2 hypotheses. K2-R1 requires at least 2.
- Goal B2 (REPLACED, frozen): SUSTAINED CONTEXTUAL CONTROL. After goal setup
  (environment establishes K = 1; RESET to t=0), the learner executes its
  full plan (M + SUFFIX). The goal is achieved iff there exist three
  consecutive steps s, s+1, s+2 such that OBSERVE Y reads 1 AND OBSERVE K
  reads 0 at each of the three steps. Rationale: the learner must not only
  discover that K gates the law (CLR K) but must sustain Y=1 across three
  steps by re-establishing X=1 at the correct cadence (delay-2 timing) while
  never disturbing K. A lucky transient firing cannot satisfy three
  consecutive sustained observations.
- Goal planner (B2): iterative deepening over {SET X, CLR X, SET K, CLR K,
  WAIT} (5 symbols), depths 1..8. For each M, simulate M + SUFFIX under the
  first surviving hypothesis (pure simulation, zero world calls). Select the
  first M (lexicographic order, shortest depth) for which the simulated
  observations contain three consecutive steps with (Y=1, K=0).
  SUFFIX = [OBS Y, OBS K, WAIT] x 3 (fixed, preregistered measurement
  protocol; disclosed here; not searched; not a "plan literal" for K2-R3
  purposes because it contains no manipulations).
- Goal verifier (B2): RESET, apply goal setup (K=1), execute M + SUFFIX for
  real exactly once, log all observations. GOAL_REAL=1 iff the triple
  predicate holds on the real observation log.
- Random control (B2): 20 sequences from fixed-seed LCG (deterministic,
  a priori seed 12345, disclosed), each of length len(M+SUFFIX)+2 over the
  7-symbol alphabet {SET X, CLR X, SET K, CLR K, WAIT, OBS Y, OBS K},
  executed for real with RESET and goal setup; count sequences satisfying
  the triple predicate (exists three consecutive steps with (OBS Y=1,
  OBS K=0)). Bar: 0/20.

## 5. Learner architecture (identical to F2 except World B goal phase)

1. Passive phase: record the 12-step trace. (Unchanged.)
2. Candidate generation (generic): for each effect variable e, each cause
   variable c != e, each delay d in 1..4, each context in the world's context
   set: keep the rule if sufficiency holds on the passive trace and the rule
   fired at least twice. No other filter. (Unchanged.)
3. Hypotheses: cross product of one candidate rule per variable that has at
   least one candidate; variables with none are exogenous. Each hypothesis
   is data (a rule set). No per-hypothesis code. (Unchanged.)
4. Experiment loop: (Unchanged from F2.)
   a. Iterative deepening over depths 1..6. At each depth, compose EVERY
      sequence from the primitive alphabet (base-B counting; no sequence
      pre-exists). Skip sequences with no OBSERVE.
   b. Simulate each sequence under every live hypothesis (pure simulation;
      zero real-world actions).
   c. Select the FIRST sequence (lexicographic) where the predicted
      observation vectors disagree. Log the sequence and every live
      hypothesis's prediction.
   d. If none found at any depth: stop (search exhaustion).
   e. Check observation budget; RESET; execute the selected sequence against
      the sealed world exactly once; record actual observations.
   f. Eliminate every hypothesis whose prediction disagrees with actual.
      If zero remain: FAIL. If one remains: stop.
   g. Repeat.
5. Goal phase:
   - World A: identical to F2 (manipulations + WAIT, depths 1..8, first
     sequence whose simulated final state satisfies X=1,Y=1,D=0; assert all
     survivors agree; RESET, setup, execute, OBSERVE, verify). (Unchanged.)
   - World B: B2 protocol as defined in section 4 above. (CHANGED.)
6. Random-action control: as defined per-world in section 4. (B2 changed;
   A unchanged.)

Primitive alphabet for experiment search: for each controllable variable v:
SET v, CLR v; plus WAIT; plus OBSERVE v for each variable. (Unchanged.)
Goal planner alphabet (World A): SET/CLR per controllable plus WAIT.
(Undisputed; unchanged.)
Goal planner alphabet (World B): SET/CLR per controllable plus WAIT
(5 symbols); SUFFIX is fixed measurement protocol. (Changed as described.)

## 6. Kill bars (numbered; frozen)

- K2-R1 (passive ambiguity): after the passive phase, the learner holds at
  least 2 hypotheses fully consistent with the passive trace, in EACH world.
  Fewer: FAIL.
- K2-R2 (construction, not enumeration): the source contains no finite list
  of complete experiments or complete goal plans (verified by source audit:
  no experiment/plan sequence literal appears in source; construction is
  exclusively iterative-deepening composition over primitives; the SUFFIX is
  a fixed measurement protocol, disclosed in this prereg, containing no
  manipulations). Additionally the executed experiments AND the goal plans
  differ across the two worlds in composition. A complete experiment or goal
  plan found as a literal in source (other than the preregistered SUFFIX):
  FAIL.
- K2-R3 (disagreement-driven): every executed experiment is logged with the
  per-hypothesis predicted observation vectors showing disagreement, and the
  world-action counter proves zero real-world actions occurred during search
  (only RESET plus the single selected execution). An executed experiment
  without logged prior disagreement, or any world action during search: FAIL.
- K2-R4 (convergence): World A: the true hypothesis
  {Z<-(X,2), Y<-(Z,1), D<-(X,1)} survives, and the loop terminates by search
  exhaustion to depth 6 (survivors form an observational equivalence class).
  World B: the loop terminates with exactly one survivor, equal to the true
  law {(X,2,K=0)}. Otherwise: FAIL.
- K2-R5 (model to goal): World A: the learner's planned sequence achieves
  Goal A for real, verified by OBSERVE; AND the random-action control
  achieves Goal A 0/20. World B: the learner's full plan (M+SUFFIX) achieves
  Goal B2 for real (triple predicate on the real observation log); AND the
  random-action control (7-symbol alphabet, length plan_length+2) achieves
  the triple predicate 0/20. Otherwise: FAIL.
- K2-R6 (observation economy): total active-phase OBSERVE actions across
  both worlds is at most 18 (passive observations are free given data).
  More: FAIL. (Raised from F2's 12 because Goal B2 requires 6 verification
  observations by design.)
- K2-R7 (determinism and purity): 3/3 runs byte-identical per world; pure
  Zag (no Python at any stage, including analysis and editing of wave
  artifacts); no em dashes in wave documentation. Otherwise: FAIL.

BUILD-PASS requires all seven bars in both worlds. Any FAIL is BUILD-FAIL.

## 7. Design calculations (pre-freeze calibration; not wave implementation)

A scratch pure-Zag calibration program (/tmp/calib2.zag, not part of the
wave, never committed) implemented the World B physics and tested:

1. Learner plan achievability: M = [CLR K, SET X, WAIT, SET X, WAIT, SET X]
   (6 primitives) + SUFFIX [OBS Y, OBS K, WAIT]x3 achieves the triple
   predicate in simulation under the true law. Result: TRIPLE ACHIEVED (1).
   The planner (depths 1..8, 5 symbols = 488K sequences max) will find an
   M of length <= 8; a length-6 M is known to exist, so the search succeeds.
2. Random base rate: 20 random sequences (length 17, 7-symbol alphabet) per
   seed, 8 seeds (12345, 20264, ..., 67778), 160 sequences total. Triple
   predicate hits: 0/160. The sustained triple goal has a far larger safety
   margin than F2's transient goal (~5% base rate, 1/20 on the a priori
   seed).

These are design calculations informing the prereg, not wave results. The
wave implementation is independent.

## 8. Governance

Pure Zag only. No Python anywhere in this wave. Prereg committed alone before
any implementation file exists. Commits local on tnn-native-lab, owned path
only: docs/lab/research-lead/overnight-20260928/autosci2/. Builder reports
BUILD-PASS or BUILD-FAIL only; no SURVIVES claim (promotion pipeline steps
4-11 remain for the parent to schedule).
