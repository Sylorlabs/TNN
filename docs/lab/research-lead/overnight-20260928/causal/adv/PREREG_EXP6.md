# Preregistration: H-EXP6 (Per-(action,variable,value) Change-to Evidence)

Date: 2026-09-29. Pure Zag. This prereg is frozen BEFORE any
implementation of exp_invent6.zag. No Python at any stage.

## Mission

Close the two H-EXP5 red-team downgrades (EXP5_ADV_RESULT.md):

- X-E5-1: flag-silent carryover. lamp==1 in F1 is observed only as
  pure carryover, yet the per-variable flag is silent (lamp changed
  1->0 once via another value) and the achievability line carries
  no per-line carryover signal.
- X-E5-2: lumped change-action and carryover-action. S1 state [2]
  reports "temp==2 demonstrated by action(s) {0,2}" although
  action 0 changed temp to 2 once while action 2 never did.

H-EXP6 adds per-(action,variable,value) CHANGE-TO counts and a
per-pick CHANGE-EVIDENCE annotation: a value-level signal that
distinguishes change-evidence from carryover-evidence. This is the
value-level hazard signal the red team recommended.

## Hypothesis H-EXP6

Annotating each achievability claim with change-to counts, and
flagging carryover-only actions per required (variable,value),
closes the X-E5-1 and X-E5-2 downgrades without introducing a new
overclaim, provided the legend scopes changed-to as observed change
(not caused, not a capability guarantee).

## Design (frozen)

exp_invent6.zag is built by copying exp_invent5.zag VERBATIM and
making exactly four additions. Nothing else changes: the selection
mechanism, ranking heuristic, reachability FLAG logic,
CONTROLLABILITY computation, and the ACHIEVABILITY report are
untouched (ACHIEVABILITY lines stay byte-identical).

### Addition 1: compute_change_to

New function. chgto is 36 i32 cells, indexed ((a*3)+v)*3+x, same
index formula as achv. Allocated in main as z_alloc(144),
accessed with the existing achv_get/achv_add-style helpers on a
separate buffer (chgto_idx/chgto_get/chgto_add, identical
formulas, separate memory). For each episode e with
ep_st==EP_ACT: for v in 0..2: let ns=ep_ns(W,e,v),
os=ep_s(W,e,v); if ns != os: chgto[ep_a(e)][v][clamp(ns)] += 1.
The change predicate is exactly the one compute_controllable
uses (ns != os), so chgto counts change-TO episodes. Always
chgto[a][v][x] <= achv[a][v][x].

### Addition 2: emit_chg_table

Emitted once per run, immediately after the ACHIEVABILITY TABLE.
Frozen header line:

CHANGE-TO TABLE (change episodes per action/variable/value; EP_ACT episodes only):

Rows use the ACHV row format with a CHGTO prefix:

CHGTO a0 temp[0:0,1:1,2:1] pressure[0:0,1:0] lamp[0:1,1:0]

(The data line above is the hand-computed F1 action-0 row:
temp changed 0->1 once and 1->2 once; lamp changed 1->0 once.
Other fixtures render their own counts in the same format.)

### Addition 3: emit_change_evidence

New function emit_change_evidence(t,p,l,chgto,achv), called
immediately after EVERY emit_achievability call (each ranked pick
with the same 4-space indent, and the top pick without indent).
Frozen format:

    CHANGE-EVIDENCE: temp==0 changed-to by action(s) {1,2,3} (5 eps); carryover-only: action(s) {} (0 eps); pressure==0 changed-to by action(s) {0,1,2,3} (10 eps); carryover-only: action(s) {} (0 eps); lamp==1 changed-to by action(s) {} (0 eps); carryover-only: action(s) {2} (1 eps)

Per variable v with required value x (clamped to 0..2):
- change set: actions a in 0..3 with chgto_get(a,v,x) > 0,
  sorted ascending, comma-separated; M = sum of chgto counts.
- carryover-only set: actions a with achv_get(a,v,x) > 0 AND
  chgto_get(a,v,x) == 0; C = sum of achv counts over those
  actions.
- Segment: "<var>==<x> changed-to by action(s) {<change set>}
  (<M> eps); carryover-only: action(s) {<co set>} (<C> eps)".
- Empty sets render as {}.
- If total outcome eps == 0 (NEVER OBSERVED case), both sets are
  empty and both counts are 0.
- The three segments are joined with "; " and prefixed with
  "CHANGE-EVIDENCE: ".

This is the value-level hazard signal: a non-empty
carryover-only set means no observed change evidence for that
required value; an empty change set with non-empty outcome set
is the X-E5-1 case made machine-readable.

### Addition 4: legend extension

The H-EXP5 legend text is kept byte-identical. One frozen
sentence is appended immediately after it (same emit block):

CHANGE-EVIDENCE annotates each pick with change-to counts: an action listed carryover-only never changed the variable to the required value (its outcomes were pure carryover). Changed-to is observed change, not proven capability.

## Frozen fixtures

S1 = causal/cum_B.txt, S2 = causal/exp_obs2.txt,
S0 = causal/exp_null.txt, A1 = adv/x_e3_a1.txt (the four H-EXP5
frozen fixtures), plus F1 = adv/f1_e5_adv.txt (the X-E5-1
adversarial fixture, the regression test for this repair).
Binary: adv/exp_invent6 (built with znc 2026.07.0-dev), in /tmp
only, not committed.

## Frozen kill bars

- K-E6-1 (X-E5-1 closed): On F1, the top-pick CHANGE-EVIDENCE
  line contains "lamp==1 changed-to by action(s) {} (0 eps)"
  and contains "carryover-only: action(s) {2} (1 eps)".
  Hand-verified: lamp==1 is observed once (S1 phase-B ep
  T 2 0 1 | 2 | 2 0 1, start lamp==1, no change), so
  achv[2][2][1]=1 and chgto[*][2][1]=0.

- K-E6-2 (X-E5-2 closed): On S1, ranked pick [2] (2 0 0) the
  CHANGE-EVIDENCE line contains "temp==2 changed-to by
  action(s) {0} (1 eps)" and contains "carryover-only:
  action(s) {2} (2 eps)". Hand-verified from the red-team
  per-episode analysis: action 0 yields temp==2 twice
  (T 1 0 0 | 0 | 2 0 0 changes 1->2 once; T 2 0 0 | 0 | 2 0 0
  carryover once); action 2 yields temp==2 twice, both
  carryover (T 2 1 0 | 2 | 2 1 0, T 2 0 1 | 2 | 2 0 1).

- K-E6-3 (no regression): K-E5-1, K-E5-2, K-E5-3, K-E5-5,
  K-E5-6 frozen checks pass unchanged on exp6 outputs
  (ACHIEVABILITY lines byte-identical to exp5). K-E5-4 is
  amended transparently here: RANKED/TRACE/CONTROLLABILITY/
  SELECTION-FILTER/REACHABILITY/ACHIEVABILITY lines are
  byte-identical to the committed exp5 raw evidence; the only
  added lines are the CHANGE-TO TABLE block (header + 4 rows)
  and one CHANGE-EVIDENCE line per achievability pick. Verified
  by diff of exp6 vs exp5 raw outputs with the added lines
  excluded.

- K-E6-4 (determinism): 3 consecutive runs per fixture
  (S1, S2, S0, A1, F1) are byte-identical; md5 recorded in the
  result doc.

## Honest limits (frozen)

- Changed-to is observed change, not causal attribution and not
  a capability guarantee. A single change-to episode does not
  prove the action can reproduce the change on demand.
- The counts do not capture why the change occurred; a change
  may be coincidental to the action.
- Carryover-only is a hazard signal at the required-value
  level; it does not say the value is unreachable, only that
  no change evidence was observed.
- No setup planning; no state-as-combination reachability.
- Actions outside 0..3 are not represented (all fixtures use
  actions 0..3 only).
- Classification target: bounded L2 discriminating-state
  selection with honest per-(a,v,x) change-to reporting.
  Not L3: no new representation is invented; the vocabulary
  (actions, variables, values) is given by the episode format.
