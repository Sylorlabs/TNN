# Preregistration: H-EXP7 (Transition-Level From/To Evidence + Per-Action Base Rates)

Date: 2026-09-29. Pure Zag. This prereg is frozen BEFORE any
implementation of exp_invent7.zag. No Python at any stage.

## Mission

Close the two H-EXP6 red-team downgrades (EXP6_ADV_RESULT.md):

- X-E6-1: from-blindness. compute_change_to discards the from-value
  os. Fixture G1: the pick requiring temp==2 reports
  "changed-to by action(s) {0,1} (5 eps)" although action 0's
  temp->2 changes are ALL from temp==1 (3 episodes) while only
  action 1 ever effected 0->2 (2 episodes). A setup planner at
  temp==0 cannot tell which action serves its need.
- X-E6-2: hidden per-action base rate. Fixture H1: the pick
  requiring temp==2 reports "{0,1} (2 eps)" although action 0's
  change is 1-in-11 outcomes (1 change + 10 carryovers) while
  action 1's is 1-in-1. Both render identically at the pick level.

H-EXP7 adds a transition-level (from-value, to-value) table and a
per-pick TRANSITION-EVIDENCE annotation that decomposes every
change-to claim into per-action from-value counts and per-action
change/outcome rates.

## Hypothesis H-EXP7

Reporting transitions (from o, to x) per (action,variable) and
annotating each pick with per-action from-value lists and
change/outcome denominators closes X-E6-1 and X-E6-2 without
introducing a new overclaim, provided the legend scopes
transitions as observed change (not caused, not a capability
guarantee) and documents the value-clamping convention.

## Design (frozen)

exp_invent7.zag is built by copying exp_invent6.zag VERBATIM and
making exactly five additions. Nothing else changes: the selection
mechanism, ranking heuristic, reachability FLAG logic,
CONTROLLABILITY computation, the ACHIEVABILITY report, the
CHANGE-TO table, and the CHANGE-EVIDENCE lines are untouched
(all stay byte-identical).

### Addition 1: transition index helpers

trans is 108 i32 cells indexed (((a*3)+v)*3+o)*3+x, a in 0..3,
v in 0..2, o in 0..2 (clamped from-value), x in 0..2 (clamped
to-value). Allocated in main as z_alloc(432), accessed with
trans_idx/trans_get/trans_add (identical structure to the
achv/chgto helpers, separate memory). Buffer 432 bytes = 108
cells * 4; max index 107.

### Addition 2: compute_transitions

New function. For each episode e with ep_st==EP_ACT: for v in
0..2: let ns=ep_ns(W,e,v), os=ep_s(W,e,v); if ns != os (the exact
raw change predicate compute_controllable uses): let x=clamp(ns),
o=clamp(os) (clamp: below 0 -> 0, above 2 -> 2); let a=ep_a(W,e);
if a in 0..3: trans_add(trans,a,v,o,x). Invariant: for every
(a,v,x), sum over o of trans[a][v][o][x] == chgto[a][v][x]
(same episode set, same change predicate).

### Addition 3: emit_trans_table + emit_trans_row

Emitted once per run, immediately after the CHANGE-TO TABLE.
Frozen header line:

TRANSITION TABLE (change episodes per action/variable/from-value/to-value; EP_ACT episodes only):

Row format (only nonzero (from->to) cells, ascending (o,x); empty
variable renders []):

TRANS a0 temp[0->1:1,1->2:1] pressure[] lamp[1->0:1]

(The data line above is the hand-verified F1 action-0 row:
T 0 0 0 | 0 | 1 0 0 gives temp 0->1; T 1 0 0 | 0 | 2 0 0 gives
temp 1->2; T 2 0 0 | 0 | 2 0 0 gives no change;
T 0 0 1 | 0 | 0 0 0 gives lamp 1->0. No other action-0
changes exist in F1.)

### Addition 4: emit_transition_evidence

New function emit_transition_evidence(t,p,l,trans,chgto,achv),
called immediately after EVERY emit_change_evidence call (each
ranked pick with the same 4-space indent, and the top pick without
indent). Frozen format:

    TRANSITION-EVIDENCE: temp==2 transitions: 0: from {1:3} (3/4); 1: from {0:2} (2/2); pressure==0 transitions: none; lamp==1 transitions: none

Per variable v with required value x (clamped to 0..2):
- If total change m = sum over a of chgto_get(a,v,x) is 0:
  segment = "<var>==<x> transitions: none".
- Else, per action a in 0..3 with chgto_get(a,v,x) > 0:
  item = "<a>: from {<o>:<c>,...} (<m_a>/<n_a>)" where
  m_a = chgto_get(a,v,x), n_a = achv_get(a,v,x), and the from
  list enumerates each o in 0..2 with trans_get(trans,a,v,o,x)
  > 0 as "<o>:<c>", comma-separated, ascending o.
  Items joined with "; ".
- The three segments are joined with "; " and prefixed with
  "TRANSITION-EVIDENCE: ".

The (m_a/n_a) rate is the per-action change/outcome denominator
(X-E6-2 repair). The from list is the transition-level signal
(X-E6-1 repair). Carryover-only is NOT repeated here; it remains
in the CHANGE-EVIDENCE line directly above.

### Addition 5: legend extension

The H-EXP5 legend text and the H-EXP6 legend sentence are kept
byte-identical. One frozen sentence is appended immediately after
them (same emit block):

TRANSITION-EVIDENCE decomposes each change-to claim by from-value and per-action change/outcome rate (an item "0: from {1:3} (3/4)" means action 0 changed the variable to the required value 3 times, all from value 1, in 4 observed outcomes); transitions are observed change, not causal attribution, and from/to values are clamped to 0..2 like outcomes.

## Frozen fixtures

S1 = causal/cum_B.txt, S2 = causal/exp_obs2.txt,
S0 = causal/exp_null.txt, A1 = adv/x_e3_a1.txt,
F1 = adv/f1_e5_adv.txt (the five H-EXP6 frozen fixtures), plus
G1 = adv/g1_e6_adv.txt and H1 = adv/h1_e6_adv.txt (the two
H-EXP6 red-team attack fixtures, now regression tests).
Binary: adv/exp_invent7 (built with znc 2026.07.0-dev), in /tmp
only, not committed.

## Frozen kill bars

- K-E7-1 (X-E6-1 closed): On G1, the ranked pick [2] (2 0 0)
  TRANSITION-EVIDENCE line contains "0: from {1:3} (3/4)" and
  contains "1: from {0:2} (2/2)". Hand-verified from the G1
  fixture and the committed exp6 G1 run: action 0 temp->2
  changes are T 1 0 0 | 0 | 2 0 0 x3 (all from 1), with 4
  temp==2 outcomes (3 changes + 1 carryover T 2 0 0 | 0 |
  2 0 0); action 1 temp->2 changes are T 0 0 0 | 1 | 2 0 0
  x2 (both from 0), with 2 temp==2 outcomes.

- K-E7-2 (X-E6-2 closed): On H1, the ranked pick requiring
  temp==2 TRANSITION-EVIDENCE line contains
  "0: from {1:1} (1/11)" and contains "1: from {0:1} (1/1)".
  Hand-verified from the H1 fixture and the committed exp6 H1
  run: action 0 changes temp 1->2 once (T 1 0 0 | 0 | 2 0 0)
  in 11 temp==2 outcomes (1 change + 10 carryovers
  T 2 0 0 | 0 | 2 0 0); action 1 changes temp 0->2 once
  (T 0 1 0 | 1 | 2 1 0) in 1 temp==2 outcome.

- K-E7-3 (no regression): K-E6-1, K-E6-2, K-E6-3, K-E6-4
  frozen checks pass unchanged on exp7 outputs
  (ACHIEVABILITY/CHANGE-TO tables, CHANGE-EVIDENCE lines, and
  the first two legend sentences byte-identical to exp6). The
  only added lines are the TRANSITION TABLE block (header +
  4 rows), one TRANSITION-EVIDENCE line per pick, and the
  legend sentence. Verified by diff of exp7 vs exp6 raw
  outputs with the added lines excluded.

- K-E7-4 (determinism): 3 consecutive runs per fixture
  (S1, S2, S0, A1, F1, G1, H1) are byte-identical; md5
  recorded in the result doc.

- K-E7-5 (table consistency): On F1, the TRANSITION TABLE
  contains the frozen row
  "TRANS a0 temp[0->1:1,1->2:1] pressure[] lamp[1->0:1]"
  (hand-verified, see Addition 3).

## Honest limits (frozen)

- Transitions are observed change, not causal attribution and
  not a capability guarantee. A single transition episode does
  not prove the action can reproduce the transition on demand.
- From/to values are clamped to 0..2 like outcomes; the change
  predicate uses raw values, so a raw transition like 5->2
  renders as 2->2. The clamp convention is documented, not
  hidden.
- The (m/n) rate is a per-action outcome denominator inside the
  observed episode set; it does not measure robustness,
  stochasticity, or reproducibility.
- No setup planning; no state-as-combination reachability.
- Actions outside 0..3 are not represented (all fixtures use
  actions 0..3 only).
- Classification target: bounded L2 discriminating-state
  selection with honest transition-level reporting.
  Not L3: no new representation is invented; the vocabulary
  (actions, variables, values) is given by the episode format.
