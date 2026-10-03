# H-EXP6 RESULT: H-EXP6 SURVIVES (4/4)

**Date:** 2026-09-29
**Prereg:** causal/adv/PREREG_EXP6.md (commit 1b7a17201, frozen
before any implementation; strict ancestor of this result commit,
verified via git merge-base --is-ancestor)
**Implementation:** causal/adv/exp_invent6.zag
(= exp_invent5.zag verbatim + the four preregistered additions;
diff-verified, only additive changes)
**Raw evidence:** causal/adv/evidence/exp6_s1_raw.txt,
exp6_s2_raw.txt, exp6_s0_raw.txt, exp6_a1_raw.txt,
exp6_f1_raw.txt (3/3 byte-identical each)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python anywhere (no generators,
verifiers, analysis, or scratch). Binary built in /tmp only,
not committed.

## Verdict: H-EXP6 SURVIVES (4/4)

Both H-EXP5 red-team downgrades are closed:

- X-E5-1 (flag-silent carryover): every ranked pick now carries
  a CHANGE-EVIDENCE line. The F1 top pick reports "lamp==1
  changed-to by action(s) {} (0 eps); carryover-only:
  action(s) {2} (1 eps)": the carryover-only demonstration is
  now machine-readable at the required-value level, even when
  the per-variable hazard flag is silent.
- X-E5-2 (lumped change/carryover): the S1 pick [2] reports
  "temp==2 changed-to by action(s) {0} (1 eps);
  carryover-only: action(s) {2} (2 eps)": action 2's
  carryover-only evidence is distinguished from action 0's
  genuine change evidence.

## What was built

Four additions to exp_invent5.zag, exactly as preregistered:

1. **compute_change_to**: chgto is 36 i32 cells, indexed
   ((a*3)+v)*3+x like achv. Counts EP_ACT episodes where the
   action changed variable v TO value x (ep_ns != ep_s, the
   same change predicate compute_controllable uses). Observed
   change only, not causal attribution. Structurally
   chgto[a][v][x] <= achv[a][v][x] in every cell.
2. **emit_chg_table**: CHANGE-TO TABLE emitted once per run
   after the ACHIEVABILITY TABLE, same row layout (CHGTO aN
   temp[...] pressure[...] lamp[...] prefixes).
3. **emit_change_evidence**: one CHANGE-EVIDENCE line after
   every ACHIEVABILITY line (ranked picks and top pick).
   Per required (variable,value): the change-evidence action
   set with change counts, and the carryover-only set (actions
   with outcome evidence but zero change evidence) with its
   counts. Empty sets render as {}. This is the value-level
   hazard signal the red team recommended.
4. **Legend extension**: one frozen sentence appended after
   the byte-identical H-EXP5 legend text.

Nothing else changed: selection, ranking, flags,
CONTROLLABILITY, and the ACHIEVABILITY report are untouched;
ACHIEVABILITY lines are byte-identical to exp5.

## Frozen bar results

- **K-E6-1 PASS:** F1 top-pick CHANGE-EVIDENCE line contains
  "lamp==1 changed-to by action(s) {} (0 eps)" and contains
  "carryover-only: action(s) {2} (1 eps)". Matches the frozen
  hand verification (lamp==1 observed once, pure carryover,
  in the S1 phase-B episode).
- **K-E6-2 PASS:** S1 ranked pick [2] (2 0 0)
  CHANGE-EVIDENCE line contains "temp==2 changed-to by
  action(s) {0} (1 eps)" and contains "carryover-only:
  action(s) {2} (2 eps)". Matches the red-team per-episode
  analysis (a0: 1 change + 1 carryover; a2: 2 carryover).
- **K-E6-3 PASS:** K-E5-1, K-E5-2, K-E5-3, K-E5-5, K-E5-6
  frozen checks pass unchanged on exp6 outputs. K-E5-4 as
  transparently amended in the prereg: all
  RANKED/TRACE/CONTROLLABILITY/SELECTION-FILTER/REACHABILITY/
  ACHIEVABILITY lines are byte-identical to the committed
  exp5 raw evidence on S1, S2, S0, A1 (verified by diff with
  the added lines excluded); the only added lines are the
  CHANGE-TO TABLE block (header + 4 rows) and one
  CHANGE-EVIDENCE line per achievability pick.
- **K-E6-4 PASS:** 3/3 runs byte-identical per fixture:
  S1 md5 3c8ad4a2a507, S2 md5 521fb312f409,
  S0 md5 4ae8ecfabf44, A1 md5 71c971adf7fa,
  F1 md5 d11ad7f3f47d (first 12 hex chars; full files in
  evidence/).

## Hand-verified spot checks

- F1 CHGTO a0 row "temp[0:0,1:1,2:1] pressure[0:0,1:0]
  lamp[0:1,1:0]" matches the frozen prereg prediction
  (temp 0->1, temp 1->2, lamp 1->0).
- F1 CHGTO a1 temp[0:1,1:1,2:0] (T 2 0 0 | 1 | 1 0 0 and
  T 1 0 0 | 1 | 0 0 0); a2 pressure[0:0,1:2] (two 0->1
  changes); a3 pressure[0:1,1:0] (one 1->0 change).
- chgto <= achv in every cell of every fixture table
  (structural, plus visually confirmed on F1).

## Honest limits (from prereg)

- Changed-to is observed change, not causal attribution and
  not a capability guarantee. A single change-to episode does
  not prove the action can reproduce the change on demand.
- The counts do not capture why the change occurred; a change
  may be coincidental to the action.
- Carryover-only is a hazard signal at the required-value
  level; it does not say the value is unreachable, only that
  no change evidence was observed.
- No setup planning; no state-as-combination reachability.
- Classification: bounded L2 discriminating-state selection
  with honest per-(a,v,x) change-to reporting. Not L3.

## Commit lineage (branch tnn-native-lab, local only)

- 1b7a17201: PREREG H-EXP6 FROZEN (alone; before any
  implementation)
- this commit: exp_invent6.zag, EXP6_RESULT.md (this file),
  evidence/exp6_s1_raw.txt, exp6_s2_raw.txt, exp6_s0_raw.txt,
  exp6_a1_raw.txt, exp6_f1_raw.txt (only owned files staged)

## Suggested follow-up for parent

Independent red team on H-EXP6 (natural attacks: X-E6-1 a
fixture where change-to counts mislead about reproducibility,
e.g. coincidental change; X-E6-2 probing whether a single
change-to episode is over-weighted by consumers of the
signal). The F1 fixture remains the regression test.
