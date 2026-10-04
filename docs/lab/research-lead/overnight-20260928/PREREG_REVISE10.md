# PREREG H-REVISE10: FROZEN

**Date (UTC):** 2026-09-30
**Parent:** H-REVISE9 (SURVIVES 133/133; red team SURVIVES 17/17 with one
confirmed new boundary: B-RV9-3 no-contradiction direct-call misuse,
plus verified forged intermediate-prefix narrowing and B-RV9-1
confirmed at depth 4).
**Target of repair:** B-RV9-3. `diagnose_rollback_check` Branch A is the
only path that does not independently verify fset[0]'s own program
mispredicts true_out. A precondition-violating direct call (no genuine
contradiction; the store already predicts true_out) returns rb=1 and
ROLLS_BACK a correct top member. The documented precondition ("CALL
ONLY after vs3_apply mispredicted true_out") is machine-checkable with
one `vs3_apply` + `streq`, unlike label authenticity (unknowable
in-function, hence the forged-label dual-use disclosure). The lineage
sets a defense-in-depth precedent (R5 nn1<=0 withhold guard in
`diagnose_corroborate_v6`).
**This prereg is committed alone, before any implementation edit, build,
or run. No amendments.**

## R10 design (frozen): in-function contradiction guard

At the very top of `diagnose_rollback_check`, before the firing-set
computation, verify the documented precondition in-function:

```
let pre:[]u8=z_alloc(16);
let preok:i32=vs3_apply(VS, inp, pre);
if(preok==1 && streq(pre[0..inp.len], true_out)==1){
  emit("GUARD: no contradiction (store predicts trusted label); no state change\n");
  return 0;
}
```

If the store's actual prediction on `inp` already matches `true_out`,
no contradiction exists; return 0 with zero state change. This closes
B-RV9-3 at the mechanism level: precondition-violating calls are now
harmless no-ops instead of felling correct members.

No other mechanism function is touched. Branch A, the R7 peeling loop,
Branch B, `vs3_apply`, `vs3_apply_skip`, `vs3_apply_skip_set`,
`vs3_firing_set`, `vs3_revise`, `diagnose_confirm_check`, all Phase A-Q
code unchanged except the new Phase Q block.

Revised claim (extends the H-REVISE9 claim): 1 contradiction fells a
provisional revision and 2 fell a confirmed one. When the most-recent
prefix of firing revisions jointly overrode a correct prediction, the
contradiction protocol applies to the smallest such prefix. Calls
without a genuine contradiction (the store already predicts the trusted
label) are no-ops with zero state change. If no correct uncovered
baseline exists, no action is taken.

On 5-deep peel (considered, deferred): a 5-deep peel requires a
capacity-5 store. The capacity-4 policy is frozen in the regression
suite (Phase K: K1/K2/K3 expect refusal at 4; K-RV9-3 requires all 117
inherited CHECK lines byte-identical). Raising capacity would break the
frozen regression bars. The peel loop itself is generic (k = 1..nf-1)
and proven correct at depth 4 (X-RV9-1a). 5-deep remains future work
requiring a capacity redesign with its own preregistration.

Residuals carried forward (not repaired): X-RV5-1 append-time
underdetermination; forged-label dual-use beyond the prefix bound;
duplicate append of an ACTIVE revision; tombstone capacity; peel k=1
dead code (red-team code observation, harmless redundancy).

## Frozen kill bars

**K-RV10-1 (B-RV9-3 closure):** Replicate the X-RV9-4 adversary fixture
exactly. VS init P0=p0b ([0,0,0] identity). vs3_revise(VS,2,113,p0a,1)
-> slot1 (correct, predicts "qqq" on "zbq"); vs3_revise(VS,1,98,p0a,1)
-> slot2 (correct, predicts "qqq" on "zbq", most recent). Setup sanity
(FATAL if broken): vs3_apply(VS,"zbq") predicts "qqq" exactly (no
contradiction exists). Then `diagnose_rollback_check(VS,"zbq","qqq")`
MUST return exactly 0; vs3_status(VS,1)==1 AND vs3_status(VS,2)==1 (zero
state change); the raw output MUST contain the GUARD emit line (the
guard fired, not a coincidental 0). KILL if: return!=0, either slot
touched, or the GUARD line absent.

**K-RV10-2 (ACTIVE-member peel, 3 stacked wrong):** VS init P0=p0b
(identity; "zbq"->"zbq"). vs3_revise(VS,2,113,p0a,1) -> slot1 (correct,
predicts "qqq"). vs3_revise(VS,1,98,wprog,1) -> slot2 (wrong, predicts
"zzz"); `diagnose_confirm_check(VS,"zbq","zzz")` MUST return 1 (FATAL if
not; slot2 fires, P0 mispredicts); vs3_status(VS,2)==2 (ACTIVE). 
vs3_revise(VS,0,122,wprog,1) -> slot3 (wrong); confirm to ACTIVE the
same way (FATAL if not). vs3_revise(VS,2,113,wprog,1) -> slot4 (wrong,
most recent; duplicate cond of slot1 appends as slot4 since slot1 is
live). Setup sanity (FATAL): vs3_apply(VS,"zbq") predicts "zzz"
(genuine contradiction vs "qqq"). Then
`diagnose_rollback_check(VS,"zbq","qqq")` MUST return exactly 1;
vs3_status(VS,4)==0 (PROVISIONAL rolled back); vs3_status(VS,3)==1 AND
vs3_status(VS,2)==1 (ACTIVE members demoted, NOT rolled back);
vs3_status(VS,1)==1 (correct untouched); vs3_apply(VS,"zbq") predicts
"qqq" exactly (restoration via slot1). KILL on any deviation.

**K-RV10-3 (forged label, mixed ACTIVE/PROVISIONAL stack):** VS init
P0=p0a ([4,0,0]; "zbq"->"qqq"). vs3_revise(VS,0,122,p0b,1) -> slot1
(correct identity, predicts "zbq"); `diagnose_confirm_check(VS,"zbq",
"zbq")` MUST return 1 (FATAL if not); vs3_status(VS,1)==2 (ACTIVE).
vs3_revise(VS,1,98,p0b,1) -> slot2 (correct identity, predicts "zbq",
PROVISIONAL). Setup sanity (FATAL): vs3_apply(VS,"zbq") predicts "zbq".
Forged F="qqq" (=P0("zbq"), differs from store prediction so the R10
guard does not trigger; the mechanism cannot authenticate labels).
`diagnose_rollback_check(VS,"zbq",F)` MUST return exactly 1;
vs3_status(VS,2)==0 (PROVISIONAL rolled back); vs3_status(VS,1)==1
(ACTIVE demoted, NOT rolled back). KILL on any deviation. Dual-use
disclosed (forged labels outside frozen claims, as since H-REVISE7).

**K-RV10-4 (regression):** All 133 inherited named CHECK lines
byte-identical to the frozen REVISE9 raw (result 86e63927b, md5
1388c8e2d151039b2956beb4b86bd81c). Full raw diff vs that raw contains
ONLY: (a) banner/verdict rename H-REVISE9->H-REVISE10; (b) GUARD emit
lines (the new text) emitted only from Phase Q K-RV10-1; (c) the Phase
Q block (new CHECKs); (d) the final RESULT/verdict lines. The R10 guard
MUST NOT fire in any inherited test (all inherited calls satisfy the
documented precondition; verified by the absence of GUARD lines outside
Phase Q). Expected total 133 + Q (Q1..Qn new). KILL if any inherited
CHECK line differs, the diff contains other categories, GUARD fires
outside Phase Q, or the total is not 133+Q.

**K-RV10-5 (determinism):** 3 consecutive runs byte-identical via cmp,
exit 0. KILL on any byte difference or nonzero exit.

## Phase Q fixtures (hand-derived expectations, frozen)

Q1 (guard closure, 4 CHECKs): Q1 rb==0. Q2 st1==1 and st2==1. Q3 GUARD
line present exactly once in the Phase Q1 window. Q4 vs3_apply still
predicts "qqq" (store fully intact).
Q2 (ACTIVE peel, 6 CHECKs): Q5 rb==1. Q6 st4==0. Q7 st3==1. Q8 st2==1.
Q9 st1==1. Q10 restoration "qqq" exact.
Q3 (forged mixed, 3 CHECKs): Q11 rb==1. Q12 st2==0. Q13 st1==1.

Total new: 13 CHECKs. Expected grand total: 146/146 (133 inherited +
13 Phase Q).

## Governance (frozen)

Pure Zag: implementation, fixtures, builds, runs, analysis. Zero Python
at any stage, including verification. No em dashes in loop documentation
(byte-checked before commit). Binaries built in /tmp only, never
committed. Only owned paths staged (PREREG_REVISE10.md, revise10.zag,
REVISE10_RAW*.txt, REVISE10_RESULT.md). Concurrent workers' files
untouched. No push authorized.
