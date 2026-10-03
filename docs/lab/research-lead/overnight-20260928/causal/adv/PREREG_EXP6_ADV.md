# Preregistration: H-EXP6 Red Team (EXP6_ADV)

Date: 2026-09-29. Pure Zag. This prereg is frozen BEFORE any
attack fixture, attack code, or adversarial execution. No Python
at any stage. Binary builds in /tmp only, never committed.

## Mission

Independently attack the H-EXP6 claim: "H-EXP6 SURVIVES (4/4).
Both H-EXP5 red-team downgrades are closed by per-(a,v,x)
change-to evidence." Assume the claim is false. Four
preregistered attacks below. Each has explicit kill criteria.

Target: causal/adv/exp_invent6.zag (committed), fixtures in
causal/adv/evidence/exp6_*_raw.txt (committed md5s in
EXP6_RESULT.md).

## Background facts (established by reading committed source,
not by running it)

- compute_change_to counts EP_ACT episodes where ns != os
  (raw values), bucketed by clamped ns into chgto[a][v][x].
  The from-value os is discarded in the aggregation.
- emit_change_evidence prints, per required (v,x): the
  change-to action set with total change count m, and the
  carryover-only set with count c. It does NOT print any
  action's total outcome count for (v,x); an action with
  1 change + 9 carryovers renders identically to an action
  with 1 change + 0 carryovers in the change set.
- chgto does not feed selection/ranking; it is report-only.
- Committed S1 evidence (exp6_s1_raw.txt:30), pick [2]=(2,0,0):
  "temp==2 changed-to by action(s) {0} (1 eps)". Committed
  fixture cum_B.txt shows action 0's temp->2 change was
  T 1 0 0 | 0 | 2 0 0 (from temp==1), while action 0 from
  temp==0 yields T 0 0 0 | 0 | 1 0 0 (temp==1, not 2).

## Attack X-E6-1: change-from blindness (transition specificity)

Hypothesis: the change-to signal discards the from-value, so
it cannot distinguish "action a changed v to x from s0" from
"action a changed v to x from s1". For setup planning (the
signal's stated purpose per the H-EXP5 red-team recommendation)
the from-value is material: a planner at temp==0 needs 0->2,
not 1->2. This is the X-E5-2 "lumping" complaint recurring
along a new axis.

Fixture G1 = S1 (causal/cum_B.txt) plus:
  T 1 0 0 | 0 | 2 0 0   (a0: two more 1->2 changes)
  T 1 0 0 | 0 | 2 0 0
  T 0 0 0 | 1 | 2 0 0   (a1: two 0->2 changes)
  T 0 0 0 | 1 | 2 0 0
  T 0 0 0 | 0 | 0 0 0   (a0 from temp==0: no change)
Expected aggregation for temp==2: chgto[0][0][2]=3 (all from
temp==1), chgto[1][0][2]=2 (from temp==0). Action 0 from
temp==0 never yields 2 (direct episodes in fixture).

KILL CRITERION (downgrade-level): a CHANGE-EVIDENCE line for
required temp==2 lists a non-empty change-to set containing
action 0, while per-episode audit of the run's fixture shows
(a) every one of action 0's temp->2 change episodes started
from temp==1, and (b) the fixture contains action-0 episodes
starting at temp==0 that do not yield temp==2. The line
carries no from-value signal, so the {0,1} (or {0}) listing
lumps the 1->2 evidence with the 0->2 evidence. The base case
is already present in committed S1 evidence (pick [2],
single from-1 change); G1 strengthens it (3 from-1 changes
vs a competing from-0 action).
If the output distinguishes from-values, the attack FAILS.

## Attack X-E6-2: hidden per-action base rate (single-episode
robustness)

Hypothesis: the pick-level CHANGE-EVIDENCE line shows the
change count m but not any action's total outcome count for
(v,x). A single change episode (1-in-10 outcomes) renders
identically to a representative one (1-in-1). The denominator
exists in the ACHV TABLE but is not surfaced in the pick
annotation, which is the "value-level hazard signal" itself.

Fixture H1 = S1 plus 9 carryover episodes giving action 0
temp==2 outcomes without change:
  T 2 0 0 | 0 | 2 0 0   (x9)
plus one action-1 change episode with no carryover:
  T 0 1 0 | 1 | 2 1 0   (a1: temp 0->2; pressure carryover 1)
  (pressure==1 carryover keeps the episode otherwise inert;
  verify by audit it does not disturb the temp==2 pick.)
Expected: for temp==2, action 0 has achv=1+1+9=11 outcomes
(1 change + 10 carryover incl. S1's), chgto=1; action 1 has
achv=1, chgto=1.

KILL CRITERION (downgrade-level): a CHANGE-EVIDENCE line for
required temp==2 shows "changed-to by action(s) {0,1}" (or
{0} and {1} across lines) with no per-action outcome
denominator, although per-episode audit shows action 0's
change was 1-in-11 outcomes while action 1's was 1-in-1.
The ACHV TABLE may contain the denominators; the criterion
is about the pick-level signal. Base case already in
committed S1 evidence: pick [2] shows {0} (1 eps) while
action 0 had 2 temp==2 outcomes (1 change + 1 carryover).
If the pick line surfaces per-action denominators, FAILS.

## Attack X-E6-3: regression / evidence integrity

Rebuild exp_invent6.zag from the committed source with
znc 2026.07.0-dev, run the five frozen fixtures
(S1=causal/cum_B.txt, S2=causal/exp_obs2.txt,
S0=causal/exp_null.txt, A1=adv/x_e3_a1.txt,
F1=adv/f1_e5_adv.txt), 3 runs each, compare md5 against the
committed evidence files. Re-verify the K-E6-1 and K-E6-2
frozen strings in fresh output. Diff fresh exp6 output vs
committed exp5 output with added lines excluded.

KILL CRITERION (integrity-level): any md5 mismatch vs
committed evidence, any K-E6-1..K-E6-4 bar failing to
reproduce, or any non-additive diff vs exp5 (a changed or
removed pre-existing line). Any of these is reported as a
kill-grade integrity failure. If everything reproduces,
the attack FAILS.

## Attack X-E6-4: source audit of the four additions

By reading (no execution): (a) chgto_idx formula identical
to achv_idx; (b) EP_ACT filter and a-in-0..3 guard in
compute_change_to match compute_achievability; (c) change
predicate (ns != os, raw) matches compute_controllable;
(d) emit_change_evidence is called after EVERY
emit_achievability call site in main; (e) no test-answer
literals (fixture-specific values) in the four added
functions; (f) diff exp_invent5.zag vs exp_invent6.zag shows
only the four preregistered additions.

KILL CRITERION: any deviation from the PREREG_EXP6 spec, any
test literal in mechanism code, any missing call site, any
index/filter/predicate mismatch. If the audit is clean,
the attack FAILS.

## Verdict rules

- X-E6-1 or X-E6-2 succeeding: H-EXP6 DOWNGRADED
  (claim-narrowing; the frozen 4/4 bars are not re-litigated).
- X-E6-3 or X-E6-4 succeeding: reported at kill-grade
  (integrity failure), verdict at least DOWNGRADED and
  flagged for re-freeze.
- All four failing: H-EXP6 SURVIVES this red team.

## Governance

- Only adversary-owned files staged/committed:
  PREREG_EXP6_ADV.md, exp6_adv.zag (if a harness is needed),
  g1_e6_adv.txt, h1_e6_adv.txt, EXP6_ADV_RAW*.txt,
  EXP6_ADV_RESULT.md. Fixture files live in causal/adv/.
- Concurrent workers' files untouched; only-owned-paths
  staging. No binaries committed. No em dashes in loop docs.
