# PREREG H-REVISE8: FROZEN

**Date (UTC):** 2026-09-29
**Parent:** H-REVISE7 (SURVIVES 98/98; red team DOWNGRADED by X-RV7-3).
**Target of repair:** X-RV7-3 (multi-slot interference). Two provisional
revisions both firing on X="zbq", both mispredicting T="qqq": the R7
rollback skip-test ignores only the most-recent firing slot, uncovers the
other wrong revision, and the genuine contradiction is silently absorbed.
**This prereg is committed alone, before any implementation edit, build,
or run. No amendments.**

## R6 design (frozen)

Replace `diagnose_rollback_check` with a two-branch protocol:

- Branch A (single-slot semantics, unchanged): compute the firing set F =
  all live (non-tombstoned) slots firing on `inp`, most-recent first. Let
  s = F[0]. If the store without s predicts `true_out`, apply the old rule
  to s only: PROVISIONAL -> ROLLED_BACK (return 1), ACTIVE -> PROVISIONAL
  (return 2).
- Branch B (H-REVISE8 repair): if Branch A did not fire, check whether
  EVERY member of F mispredicts `true_out` (each member's own program run
  directly and compared) AND the store without the WHOLE firing set
  predicts `true_out`. If so, apply the contradiction protocol to EVERY
  member: PROVISIONAL -> ROLLED_BACK, ACTIVE -> PROVISIONAL (first
  contradiction; needs 2 to roll back). Return 1 if any member was rolled
  back, else 2 if any member was demoted, else 0.
- If the uncovered baseline also mispredicts, take no action (return 0).
  The X-RV5-1 underdetermination treatment is untouched.

New helpers (mechanism): `vs3_firing_set` (firing set, most-recent first),
`vs3_apply_skip_set` (apply ignoring a slot set). `vs3_apply_skip`,
`vs3_apply`, `vs3_revise`, `diagnose_confirm_check` unchanged.

Revised claim (replaces the narrowed K-RV7-4 bound): 1 contradiction fells
a provisional revision and 2 fell a confirmed one. When multiple live
revisions fire on the contradicted input, all mispredict, and the store
without them predicts the trusted label, the contradiction protocol
applies to every firing member. If no correct uncovered baseline exists,
no action is taken.

Residuals carried forward (not repaired): X-RV5-1 append-time
underdetermination; forged-label dual-use (X-RV7-1/X-RV7-2); duplicate
append of an ACTIVE revision (X-RV7-4); tombstone capacity (X-RV7-5).

## Frozen kill bars

**K-RV8-1 (X-RV7-3 replay, interference closed):** Fixture: VS init with
P0-A=[4,0,0] (out[k]=inp[2]); X="zbq"; T="qqq". WPROG=[2,0,0]
(out[k]=inp[0]). vs3_revise(VS,0,122,WPROG,1) -> slot1 PROVISIONAL;
vs3_revise(VS,1,98,WPROG,1) -> slot2 PROVISIONAL. Sanity:
vs3_apply(VS,X)->"zzz" (mispredicts). Then
`diagnose_rollback_check(VS,X,T)` MUST return nonzero (frozen expectation:
exactly 1); vs3_status(VS,1)==0 AND vs3_status(VS,2)==0 (both
ROLLED_BACK); vs3_apply(VS,X)->"qqq" exactly (restoration).
KILL if: return==0, either slot not ROLLED_BACK, or restoration not exact.

**K-RV8-2 (X735 control preserved):** VS2 init P0-A;
vs3_revise(VS2,1,98,WPROG,1) -> slot1 PROVISIONAL.
`diagnose_rollback_check(VS2,X,T)` MUST return exactly 1;
vs3_status(VS2,1)==0. KILL if return!=1 or status!=0.

**K-RV8-3 (regression):** All 98 inherited named CHECK lines byte-identical
to the frozen REVISE7 raw (result 1d0f82708, md5
6b783965c82d1b5483808a36ed4f78e7). Full raw diff vs that raw contains ONLY:
(a) banner/verdict rename H-REVISE7->H-REVISE8; (b) R6 mechanism emit lines
(ROLLBACK/DEMOTE with all-firing-revisions wording) emitted from Phase O
only; (c) the Phase O block (19 CHECKs). Expected total 117/117 (98
inherited + 19 Phase O). KILL if any inherited CHECK line differs, the diff
contains other categories, or the total is not 117/117.

**K-RV8-4 (determinism):** 3 consecutive runs byte-identical via cmp,
exit 0. KILL on any byte difference or nonzero exit.

## Phase O fixtures (hand-derived expectations, frozen)

O1 (X-RV7-3 replay): O1 vs3_apply->"zzz" (mispredict). O2 rb==1. O3
st1==0. O4 st2==0. O5 restoration vs3_apply->"qqq".
O2 (control): O6 rb2==1. O7 st==0.
O3 (mixed ACTIVE+PROVISIONAL): slot1 (0,122) WPROG; O8 vs3_apply("zbq")->
"zzz"; O9 diagnose_confirm_check(VS,"zbq","zzz")==1; O10 st1==2 (ACTIVE).
Add slot2 (1,98) WPROG (PROVISIONAL). O11
diagnose_rollback_check(VS,"zbq","qqq")==1. O12 st1==1 (demoted). O13
st2==0 (rolled back).
O4 (underdetermination preserved): P0-B=[0,0,0] identity ("zbq"->"zbq").
Two PROVISIONAL slots as in O1. O14 rb==0. O15 st1==1. O16 st2==1.
O5 (per-member override preserved): slot1 (1,98) with program P0-A
("zbq"->"qqq", correct, fires); slot2 (0,122) WPROG (mispredicts, fires,
most recent). O17 rb==1. O18 st2==0 (slot2 rolled back). O19 st1==1
(slot1 untouched).

## Governance (frozen)

Pure Zag: implementation, fixtures, builds, runs, analysis. Zero Python
at any stage, including verification. No em dashes in loop documentation
(byte-checked before commit). Binaries built in /tmp only, never
committed. Only owned paths staged (revise8.zag, REVISE8_RAW*.txt,
REVISE8_RESULT.md, this prereg). Concurrent workers' files untouched. No
push authorized.
