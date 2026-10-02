# PREREG: H-REVISE8 Red Team (RV8-ADV)

**Date (UTC):** 2026-09-29
**Target:** H-REVISE8 SURVIVES (117/117), result commit `f03295207`.
**Repair under attack (R6):** `diagnose_rollback_check` rewritten as a
two-branch protocol. Branch A: the most-recent firing member gets the
exact old single-slot skip-test (store without it predicts the trusted
label -> PROVISIONAL rolls back returning 1, ACTIVE demotes returning 2).
Branch B: if every firing member's own program mispredicts the trusted
label AND the store without the WHOLE firing set predicts it, the
contradiction protocol applies to every member (PROVISIONAL->ROLLED_BACK,
ACTIVE->PROVISIONAL); returns 1 if any member rolled back, 2 if any
demoted, else 0. If the uncovered baseline also mispredicts, no action.

**Frozen R8 claims under test:**
- C1: Branch A fires iff the store without the most-recent firing member
  predicts the trusted label; it rolls back/demotes only that member.
- C2: Branch B fires iff every firing member's own program mispredicts
  the trusted label AND the store without the whole firing set predicts
  it; then every member is rolled back/demoted per its status.
- C3: If no correct uncovered baseline exists, no action is taken.
- C4: The two branches are mutually exclusive (Branch A fires only when
  the next firing member predicts the trusted label, which falsifies
  Branch B's every-member-mispredicts antecedent).
- C5: 117/117 regression byte-identical; 3/3 deterministic.

**Method:** harness = committed `revise8.zag` lines 1-744 byte-verbatim
(cmp-verified against `git show HEAD:`; everything before `fn main`) +
attack-only `main()`. No mechanism edits. Programs hand-built:
P0-A = [4,0,0] (out[k] = inp[2]); P0-B = [0,0,0] (identity);
WPROG = [2,0,0] (out[k] = inp[0]). X = "zbq" (122,98,113).
T = "qqq". P0-A(X) = "qqq" = T. P0-B(X) = "zbq" != T. WPROG(X) = "zzz".

Conventions: "trusted label" below is stipulated by the fixture.
"Forged" means a label equal to P0's output but unequal to the true
label; the mechanism is disclosed not to authenticate labels.

## X-RV8-1: forged firing-set amplification (BOUNDARY PROBE)

Setup: VS with P0-A. Slot 1: cond (0,122), program identity [0,0,0]
(predicts "zbq"). Slot 2: cond (1,98), program identity (predicts "zbq").
True label for X is "zbq" (identity task). Promote both to ACTIVE via
`diagnose_confirm_check(VS, X, "zbq")` (revision fired; P0-A gives "qqq"
!= "zbq", so each promotes). CHECK A11: both ACTIVE.
Forged label F = "qqq" = P0-A(X) != true label.
Call `diagnose_rollback_check(VS, X, F)`.
- Branch A: skip slot 2 -> slot 1 predicts "zbq" != F -> no fire.
- Branch B (expected): both members' own programs predict "zbq" != F
  (allmiss=1); store without {2,1} = P0-A predicts F -> both ACTIVE
  demoted to PROVISIONAL; return 2.
CHECK A12: return == 2 and both slots PROVISIONAL.
Second forged call `diagnose_rollback_check(VS, X, F)`:
CHECK A13: return == 1 and both slots ROLLED_BACK.
Control note: under R7 semantics this shape returns 0 twice (X-RV7-3
demonstrated the absorption); R8 acts where R7 was silent.

Expected verdict: CONFIRMED NEW BOUNDARY in the disclosed dual-use
class. The frozen disclosure ("does not authenticate labels") covers
single-revision forged rollback; the SET amplification (one forged
label demoting/rolling back N firing revisions at once; two forged
labels destroying two correct confirmed revisions) is new with R6 and
must be named explicitly. Not a kill/downgrade: no frozen claim covers
forged labels.

Kill criterion for X-RV8-1: NONE (boundary probe by design). It becomes
a DOWNGRADE only if the mechanism acts on a forged label in a way the
frozen disclosure does not cover AND the action contradicts C1-C3
(e.g. demoting a member whose own program predicted F, or acting when
the skip-set baseline does not predict F).

## X-RV8-2a: Branch A/B precedence (HOLD PROBE)

Setup: VS with P0-A. Slot 2 (appended second, most recent): cond (1,98),
program [4,0,0] (predicts "qqq" = T on X). Slot 1: cond (0,122),
WPROG (predicts "zzz" != T). Both PROVISIONAL. Both fire on X.
Call `diagnose_rollback_check(VS, X, T)`.
- Branch A expected: skip slot 2 -> slot 1 predicts "zzz" != T... wait,
  slot 2 is most recent. Order: append slot 1 first (cond (0,122),
  WPROG), then slot 2 (cond (1,98), [4,0,0]). Firing set = {2,1}.
  Branch A: skip 2 -> slot 1 predicts "zzz" != T -> no fire.
  Branch B: slot 2's own program predicts T -> allmiss=0 -> no fire.
  Return 0. This is the correct-veto shape; use as 2a-control.
Then the precedence fixture: slot 1: cond (0,122), program [4,0,0]
(predicts T, PROVISIONAL); slot 2: cond (1,98), WPROG (predicts "zzz",
PROVISIONAL, most recent). Firing set = {2,1}.
Call `diagnose_rollback_check(VS, X, T)`.
- Branch A expected: skip 2 -> slot 1 predicts T -> ROLLBACK slot 2
  only, return 1. Branch B must NOT additionally fire (its antecedent
  is falsified: slot 1 predicts T).
CHECK B11: return == 1, slot 2 ROLLED_BACK, slot 1 still PROVISIONAL.

Expected verdict: HOLD (no precedence bug). The branches are mutually
exclusive by construction.

Kill criterion for X-RV8-2a: if both branches fire on one call, or
Branch A fires when the skip-most-recent baseline does not predict T,
or fails to fire when it does, or any member other than the most-recent
is mutated -> KILL.

## X-RV8-2b: subset/veto gap (BOUNDARY PROBE)

Setup: VS with P0-B (identity; P0-B(X) = "zbq" != T, so P0 is a wrong
baseline). Slot 1: cond (2,113), program [4,0,0] (predicts "qqq" = T;
correct but will be shadowed). Slot 2: cond (1,98), WPROG ("zzz",
wrong). Slot 3: cond (0,122), WPROG ("zzz", wrong). All PROVISIONAL.
All three fire on X. vs3_apply -> slot 3 -> "zzz" != T: genuine
contradiction; slots 3+2 jointly overrode slot 1's correct prediction.
Sanity CHECK B21: `vs3_apply_skip_set` skipping {3,2} predicts T
(proves the pair-counterfactual exists).
Call `diagnose_rollback_check(VS, X, T)`.
- Branch A expected: skip 3 -> slot 2 predicts "zzz" != T -> no fire.
- Branch B expected: slot 1's own program predicts T -> allmiss=0 ->
  no fire. Return 0; all three slots remain PROVISIONAL.
CHECK B22: return == 0 and statuses unchanged.

Expected verdict: CONFIRMED NEW BOUNDARY (subset gap). R6 considers only
the singleton most-recent (Branch A) and the whole firing set
(Branch B); intermediate subsets are never tested, so a correct
shadowed member vetoes the protocol even when the effective members
jointly overrode a correct prediction. Not a kill/downgrade: the frozen
claim C2 is explicitly conditional on every firing member mispredicting,
which fails here by construction. Recommended follow-up: a peeling
protocol (test subsets {fset[0..k-1]} for increasing k) for H-REVISE9.

Downgrade criterion for X-RV8-2b: if the frozen claim's natural reading
is judged to promise action here, this would be a DOWNGRADE; the
preregistered judgment is BOUNDARY because C2's antecedent is explicit.
This judgment is recorded, not hedged at verdict time.

## X-RV8-3: tombstone interleaving (HOLD PROBE)

Setup: VS with P0-A. Slot 1: cond (0,122), WPROG -> PROVISIONAL; roll it
back via genuine `diagnose_rollback_check(VS, "zbq", T)` (P0-A predicts T;
single firing member) -> CHECK C11: return == 1, slot 1 ROLLED_BACK.
Slot 2: cond (1,98), WPROG -> PROVISIONAL. Slot 3: cond (2,113),
WPROG -> PROVISIONAL. Slots 2,3 fire on X; slot 1 is tombstoned.
Call `diagnose_rollback_check(VS, X, T)`.
- Firing set must be {3,2} (tombstone excluded). Branch A: skip 3 ->
  slot 2 -> "zzz" != T -> no fire. Branch B: both mispredict; skip {3,2}
  -> slot 1 tombstoned, skipped -> P0-A predicts T -> both rolled back.
CHECK C12: return == 1, slots 2,3 ROLLED_BACK, slot 1 still ROLLED_BACK
(untouched), vcount still 3.

Expected verdict: HOLD.

Kill criterion for X-RV8-3: if a tombstoned slot appears in the firing
set (is mutated or consulted), or the protocol misfires (wrong return,
wrong members), or vcount changes -> KILL.

## X-RV8-4: regression (HOLD PROBE)

Rebuild `revise8.zag` unmodified from `git show HEAD:`, run 3x,
cmp byte-identical to committed `REVISE8_RAW.txt`; expect
`=== RESULT: 117/117 ===`, zero FAIL lines, md5
`631cd08786189b0596c0811f92168032`.

Kill criterion for X-RV8-4: any byte difference, any FAIL line, or count
!= 117/117 -> KILL.

## Verdict aggregation

- SURVIVES if no kill/downgrade criterion fires.
- New confirmed boundaries (X-RV8-1 amplification, X-RV8-2b subset gap)
  are recorded as boundaries with follow-up recommendations.
- Determinism: every attack 3/3 byte-identical via cmp, exit 0.
- Pure Zag throughout; zero Python at any stage. No binaries committed.
- No em dashes in loop documentation.

## Governance

Prereg committed alone before any adversary code, build, or run.
Ordering verified via `git merge-base --is-ancestor` (prereg is a
strict ancestor of the result commit). Only owned
`revise8_adversary/` paths staged. No push.
