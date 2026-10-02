# PREREG: H-CAUSALEXP1 (Causal/Experimental Invention Frontier, generation 1)

Date: 2026-09-29. Pure Zag only. No Python at any stage.
Status: FROZEN. Committed alone before any implementation, build, or run.

## Mission

Per the 2026-09-29 directive, the H-CAUSALV6 red-team findings
(R6b weakens positioned-confounder guard, delayed intervener not checked,
floor escalation cost race) are an ARCHITECTURE SIGNAL, not three requests
for three more conditions. This experiment opens a new causal-architecture
frontier: active causal discovery by intervention, replacing passive
observation-only heuristics.

Target loop:
observe -> retain competing causal hypotheses -> identify uncertainty ->
construct discriminating action/experiment -> observe result ->
eliminate/qualify hypotheses -> revise causal structure ->
plan using surviving model.

This is NOT CAUSALV7. No new confirmation rule, floor, or guard is added
to the observation-only learner. If implementation drifts toward "one more
confirmation rule," the run is void.

## Frozen world definitions

Variables: x (v0), y (v1), values in {0,1}.

Actions (frozen ids):
  0 = idle (state persists)
  1 = trigger
  2 = do(x:=0)
  3 = do(x:=1)
  4 = do(y:=0)
  5 = do(y:=1)

A causal hypothesis is a DAG over {x,y}, encoded as an edge mask:
  bit0 = edge x->y, bit1 = edge y->x.
Three candidate hypotheses (frozen enumeration of all DAGs over 2 nodes):
  H0 "X2Y": mask bit0 (x->y)
  H1 "Y2X": mask bit1 (y->x)
  H2 "NONE": mask 0 (no x-y edge)

Intervention semantics, identical for every hypothesis (frozen):
  idle:    (x,y) unchanged.
  trigger: set every root node (no incoming edge) := 1, then propagate
           along edges (child := parent), 2 passes.
  do(x:=c): x := c, then propagate along outgoing edges of x.
  do(y:=c): y := c, then propagate along outgoing edges of y.

True worlds (hidden from the learner; reachable only via the world_step
oracle):
  W1: true mask = bit0 (x->y)
  W2: true mask = bit1 (y->x)

The learner NEVER reads the true mask. Learner functions take
(hypothesis mask, state, action). Only world_step takes wid. A grep audit
must show wid appears only as an argument to world_step.

## Frozen passive phase

Start state (0,0). Fixed action script: [0,1,0,1,1,0].

Frozen predicted outcomes (same in W1 and W2; verified post-implementation
against the raw log):
  (0,0) idle    -> (0,0)
  (0,0) trigger -> (1,1)
  (1,1) idle    -> (1,1)
  (1,1) trigger -> (1,1)
  (1,1) trigger -> (1,1)
  (1,1) idle    -> (1,1)

Frozen per-hypothesis predictions for the passive log:
  X2Y: trigger from (0,0): roots={x}; x:=1; y:=x=1 -> (1,1). All 6 match.
  Y2X: trigger from (0,0): roots={y}; y:=1; x:=y=1 -> (1,1). All 6 match.
  NONE: trigger: roots={x,y}; x:=1,y:=1 -> (1,1). All 6 match.
Passive observation cannot distinguish the three hypotheses: 6/6 each.

## Frozen hypothesis generation

Enumerate masks {bit0, bit1, 0}. For each, simulate all 6 passive episodes
with the frozen predict(). evidence = matches/6. Status LIVE iff 6/6.

## Frozen active loop

Candidate experiments: all action sequences of length 1..2 over
actions {0..5} (42 candidates), evaluated from the current state.

For each candidate seq: predictions p_h = simulate(h, state, seq) for each
LIVE h. split = number of distinct predicted outcomes.

Selection (frozen): maximum split; tie-break shorter sequence, then
lexicographically smallest action sequence. Require split >= 2, else emit
NO-DISCRIMINATING-EXPERIMENT and stop.

Execution: apply seq in the true world via world_step, step by step.
Elimination: for each LIVE h, if simulate(h, old_state, seq) != observed
final state, mark ELIMINATED.

Repeat while LIVE count > 1 (max 4 rounds).

Frozen expected traces:

W1 (true X2Y). Active loop starts at state (1,1).
  Round 1 candidates from (1,1), length-1:
    idle -> all (1,1), split 1
    trigger -> all (1,1), split 1
    do(x:=0): X2Y -> (0,0); Y2X -> (0,1); NONE -> (0,1); split 2
    do(x:=1) -> all (1,1), split 1
    do(y:=0): X2Y -> (1,0); Y2X -> (0,0); NONE -> (1,0); split 2
    do(y:=1) -> all (1,1), split 1
  No length-2 candidate reaches split 3; max split = 2.
  Tie-break: shortest, then lexicographic -> SELECT seq=[2] (do(x:=0)).
  Execute in W1: (1,1) do(x:=0) -> (0,0).
  X2Y predicted (0,0): stays LIVE. Y2X, NONE predicted (0,1): ELIMINATED.
  CONVERGED id=0 (X2Y) after 1 round. End state (0,0).

W2 (true Y2X). Active loop starts at state (1,1).
  Round 1: identical candidate table -> SELECT seq=[2] (do(x:=0)).
  Execute in W2: (1,1) do(x:=0) -> (0,1).
  X2Y predicted (0,0): ELIMINATED. Y2X, NONE predicted (0,1): stay LIVE.
  Round 2 from (0,1), length-1:
    do(x:=0): Y2X -> (0,1); NONE -> (0,1); split 1
    do(x:=1): Y2X -> (1,1); NONE -> (1,1); split 1
    do(y:=0): Y2X -> (0,0); NONE -> (0,0); split 1
    do(y:=1): Y2X -> (1,1); NONE -> (0,1); split 2
    idle/trigger: split 1
  SELECT seq=[5] (do(y:=1)).
  Execute in W2: (0,1) do(y:=1) -> (1,1).
  Y2X predicted (1,1): stays LIVE. NONE predicted (0,1): ELIMINATED.
  CONVERGED id=1 (Y2X) after 2 rounds. End state (1,1).

## Frozen planning phase

Setup (frozen): if state != (1,1), execute trigger once; assert state is
(1,1). (W1 ends discovery at (0,0): trigger -> (1,1). W2 ends at (1,1).)

Goal (frozen, both worlds): (0,0).

Planner (frozen): BFS over action sequences of length 1..3 (258
candidates), simulated under the single surviving hypothesis from (1,1);
pick shortest achieving (0,0), tie-break lexicographic.

Frozen expected plans:
  W1 under X2Y: [0]->(1,1) no; [1]->(1,1) no; [2] do(x:=0) -> (0,0) yes.
    PLAN seq=[2].
  W2 under Y2X: [0] no; [1] no; [2] -> (0,1) no; [3] -> (1,1) no;
    [4] do(y:=0) -> (0,0) yes. PLAN seq=[4].

Execute the plan in the true world from (1,1); require final == (0,0)
(PLAN-OK). The plans differ ([2] vs [4]) for the same goal, proving the
planner uses the surviving causal model rather than a fixed policy.

## Frozen kill bars

K-CX-1 (passive indistinguishability): in each world, PASSIVE-CHECK shows
all three hypotheses 6/6 consistent and all three enter the active loop
LIVE. Any hypothesis eliminated during the passive phase = FAIL.

K-CX-2 (explicit representation): raw output contains HYPO lines for all
three edge codes (X2Y, Y2X, NONE) with evidence 6/6 and status LIVE in each
world, plus PRED lines giving each live hypothesis's predicted outcome for
every selected experiment.

K-CX-3 (discriminating selection): every SELECTed experiment has split >= 2
distinct predicted outcomes across the live hypotheses (emitted SPLIT
count). No round selects a non-discriminating experiment.

K-CX-4 (elimination correctness): after each intervention, exactly the
hypotheses whose predictions mismatch the observed outcome are ELIMINATED
(emitted ELIM lines name them with predicted vs observed). Final
CONVERGED hypothesis is the true one: W1 -> X2Y, W2 -> Y2X.

K-CX-5 (planning from surviving model): W1 PLAN seq=[2], W2 PLAN seq=[4];
both execute in the true world reaching (0,0) (PLAN-OK lines).

K-CX-6 (transfer, one binary): K-CX-1..K-CX-5 hold for both W1 and W2 in a
single program run. Grep audit: the token wid occurs in learner code only
as an argument passed to world_step (no world-conditional learner logic).

K-CX-7 (determinism): 3 consecutive runs byte-identical, exit code 0.

Verdict rule: BUILD-PASS iff K-CX-1..K-CX-7 all hold. Otherwise BUILD-FAIL.
The builder does NOT promote to SURVIVES.

## Honest scope (frozen)

Authored machinery: the hypothesis vocabulary (all DAGs over 2 variables),
the experiment vocabulary (do-operations, sequences up to length 2), the
trigger/root semantics, the selection tie-breaks. The learner contributes:
representing competing hypotheses with evidence and intervention
predictions, selecting discriminating experiments from its own uncertainty,
eliminating via intervention outcomes, and planning with the survivor.

Classification: bounded L2 architecture-signal response. NOT L3: the causal
graph vocabulary is fixed and researcher-enumerated; no representational
expansion occurs. The architectural advance over CAUSALV6 is the closed
intervention loop (act -> eliminate -> plan), not another passive
confirmation rule.

## Output line formats (frozen, for audit)

WORLD <wid>
PASSIVE (<x>,<y>)|<a> -> (<x>,<y>)
PASSIVE-CHECK hypo=<id> edges=<X2Y|Y2X|NONE> ev=<ok>/<total>
HYPO id=<id> edges=<code> status=<LIVE|ELIMINATED> ev=<ok>/<total>
ROUND <n> state=(<x>,<y>) live=<k>
CAND seq=[<a>,...] split=<n>
PRED id=<id> seq=[<a>,...] -> (<x>,<y>)
SELECT seq=[<a>,...] split=<n>
EXEC seq=[<a>,...] -> (<x>,<y>)
ELIM id=<id> predicted=(<x>,<y>) observed=(<x>,<y>)
CONVERGED id=<id> edges=<code>
SETUP state=(<x>,<y>)
PLANCAND seq=[<a>,...] -> (<x>,<y>)
PLAN seq=[<a>,...]
PLAN-SIM id=<id> seq=[<a>,...] -> (<x>,<y>)
PLAN-EXEC -> (<x>,<y>)
PLAN-OK goal=(<x>,<y>)
NO-DISCRIMINATING-EXPERIMENT
WORLD-DONE <wid>
