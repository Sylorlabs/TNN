# Preregistration: H-EXP5 (Per-(action,variable,value) Achievability)

Date: 2026-09-29. Pure Zag. This prereg is frozen BEFORE any
implementation of exp_invent5.zag. No Python at any stage.

## Mission

Close the exact gap the H-EXP4 legend admits: "(which action sets
which value, and state-level reachability, are not computed)".
H-EXP5 computes the first half honestly: per-(action,variable,value)
observed-outcome achievability. State-as-combination reachability
remains uncomputed and stays documented as such.

## Hypothesis H-EXP5

Adding an evidence-based achievability report, which actions were
observed to yield which values as outcomes, strictly increases the
honesty and usefulness of the reachability flag without introducing
a new overclaim, provided the legend scopes "demonstrated" as
observed-outcome (not caused, not guaranteed).

## Design (frozen)

exp_invent5.zag is built by copying exp_invent4.zag VERBATIM and
making exactly four additions. Nothing else changes: the selection
mechanism, ranking heuristic, reachability FLAG logic, and the
CONTROLLABILITY computation are untouched.

### Addition 1: compute_achievability

New function. achv is 36 i32 cells, indexed ((a*3)+v)*3+x, for
action a in 0..3, variable v in 0..2, value x in 0..2. Allocated
in main as z_alloc(144), accessed with get32/set32, zeroed by
z_alloc. For each episode e with ep_st==EP_ACT: for v in 0..2,
achv[ep_a(e)][v][ep_ns(e,v)] += 1.

This records which action was OBSERVED to yield which value as an
outcome. It is not causal attribution: the value may have been
unchanged by the action.

### Addition 2: emit_achv_table

Emitted once per run, immediately after the CONTROLLABILITY line
and before the legend. Frozen format:

ACHIEVABILITY TABLE (observed outcome counts per action/variable/value; EP_ACT episodes only):
ACHV a0 temp[0:0,1:1,2:2] pressure[0:3,1:0] lamp[0:3,1:0]
ACHV a1 temp[0:2,1:1,2:0] pressure[0:3,1:0] lamp[0:3,1:0]
ACHV a2 temp[0:1,1:1,2:2] pressure[0:1,1:3] lamp[0:3,1:1]
ACHV a3 temp[0:3,1:0,2:0] pressure[0:3,1:0] lamp[0:2,1:1]

(The four data lines above show the A1 fixture values, hand
computed from the 13 episodes; other fixtures render their own
counts in the same format. Order is a0..a3. temp shows values
0..2, pressure 0..1, lamp 0..1.)

### Addition 3: emit_achievability

New function emit_achievability(t,p,l,achv), called immediately
after EVERY emit_reachability call (each ranked pick with the same
4-space indent, and the top pick without indent). Frozen format:

    ACHIEVABILITY: temp==0 demonstrated by action(s) {1,2,3} (6 eps); pressure==0 demonstrated by action(s) {0,1,2,3} (10 eps); lamp==1 demonstrated by action(s) {2,3} (2 eps)

Rules: for each variable v with required value x, total =
sum over a of achv[a][v][x]. If total>0: "<var>==<x>
demonstrated by action(s) {<a sorted asc, comma-separated>} (<total>
eps)". If total==0: "<var>==<x> NEVER OBSERVED as outcome
(undemonstrated)". Variables joined with "; ". Counts are outcome
counts, not change counts.

### Addition 4: legend replacement

The H-EXP4 legend line is replaced with this frozen text:

REACHABILITY LEGEND: NEEDS-EXTERNAL-SETUP is a conservative hazard flag (variable never changed by any action). NO-UNCONTROLLABLE-VARS means no hazard detected but setup is NOT verified. ACHIEVABILITY reports observed outcomes per (action,variable,value): "demonstrated by action(s)" means that value was seen as an outcome of those actions, not necessarily caused by them; a value NEVER OBSERVED was never seen as any action's outcome. Demonstrated-as-outcome is weaker than demonstrated-as-change; state-as-combination reachability is not computed.

## Frozen fixtures

S1 = causal/cum_B.txt, S2 = causal/exp_obs2.txt,
S0 = causal/exp_null.txt, A1 = adv/x_e3_a1.txt. Same four as
H-EXP4. Binary: adv/exp_invent5 (built with znc 2026.07.0-dev).

## Frozen kill bars

- K-E5-1 (positive achievability): On A1, the top-pick
  ACHIEVABILITY line contains "lamp==1 demonstrated by
  action(s) {2,3}" and contains "temp==0 demonstrated by
  action(s) {1,2,3}". Hand-verified from the 13-episode fixture:
  lamp==1 outcomes occur only in ep11 (a2) and ep12 (a3);
  temp==0 outcomes occur in ep5,ep10 (a1), ep6 (a2),
  ep8,ep12,ep13 (a3); a0 never yields temp==0.

- K-E5-2 (outcome-without-change nuance): On S1, the top-pick
  ACHIEVABILITY line contains "lamp==1 demonstrated by
  action(s) {2}" (single outcome in ep11, never a change) AND
  the top-pick REACHABILITY line is still "FLAG:
  NEEDS-EXTERNAL-SETUP" naming lamp==1. The conservative flag is
  preserved while the achievability line honestly reports the
  observed outcome. This distinction is documented in the legend.

- K-E5-3 (table present, zero row): On S0, the ACHV table
  contains the all-zero action-0 row "ACHV a0
  temp[0:0,1:0,2:0] pressure[0:0,1:0] lamp[0:0,1:0]" (S0 has only
  a2 episodes); S0 still emits "NO AMBIGUITY: no competing
  hypotheses, nothing to invent."

- K-E5-4 (no regression): On S1, S2, A1, the RANKED EXPERIMENTS
  state lines, the CONTROLLABILITY line, the SELECTION FILTER
  line, the TRACE lines, and the REACHABILITY flag lines are
  byte-identical to the exp_invent4 outputs. Only added lines
  are the ACHV table, the ACHIEVABILITY lines, and the replaced
  legend. Verified by diffing exp5 raw output against exp4 raw
  output with the added/replaced lines excluded.

- K-E5-5 (determinism): 3 consecutive runs per fixture
  (S1, S2, S0, A1) are byte-identical; md5 recorded in the
  result doc.

- K-E5-6 (legend honesty): the legend line contains "not
  necessarily caused by them" and contains "state-as-combination
  reachability is not computed". The H-EXP4 parenthetical
  "(which action sets which value, and state-level reachability,
  are not computed)" appears 0 times in source and outputs.

## Honest limits (frozen)

- Achievability is observed-outcome, not causal attribution and
  not a capability guarantee. An action observed to yield a
  value may not be able to reproduce it on demand.
- Demonstrated-as-outcome is weaker than demonstrated-as-change;
  change-to counts are future work.
- No setup planning; no state-as-combination reachability.
- Actions outside 0..3 are not represented (all four fixtures
  use actions 0..3 only).
- Classification target: bounded L2 discriminating-state
  selection with honest per-(a,v,x) achievability reporting.
  Not L3: no new representation is invented; the vocabulary
  (actions, variables, values) is given by the episode format.
