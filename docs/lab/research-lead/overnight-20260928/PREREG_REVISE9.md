# PREREG H-REVISE9: FROZEN

**Date (UTC):** 2026-09-30
**Parent:** H-REVISE8 (SURVIVES 117/117; red team SURVIVES 10/10 with two
confirmed boundaries: B-RV8-1 forged firing-set amplification,
B-RV8-2 subset/veto gap).
**Target of repair:** B-RV8-2. Three stacked PROVISIONAL revisions on
P0-B (identity; P0 wrong on X="zbq"): slot 1 correct (program [4,0,0]
predicts T="qqq"), slots 2 and 3 wrong (WPROG=[2,0,0] predicts "zzz").
All fire on X. The pair-counterfactual is real (store without {3,2}
predicts T), so slots 3+2 jointly overrode slot 1's correct prediction,
but R6 returns 0: Branch A tests only the singleton most-recent slot,
Branch B tests only the whole firing set, and the correct shadowed
member vetoes Branch B. The two wrong revisions are immune to this
contradiction shape.
**This prereg is committed alone, before any implementation edit, build,
or run. No amendments.**

## R7 design (frozen): peeling protocol

In `diagnose_rollback_check`, keep Branch A (R7 single-slot semantics)
exactly unchanged and keep Branch B (R6 whole-set test) exactly
unchanged. Insert between them the peeling loop:

Let F = firing set (all live slots firing on `inp`), most-recent first,
|F| = nf. For k = 1 .. nf-1, let S_k = {F[0..k-1]} (the k most-recent
firing members). If every member of S_k mispredicts `true_out` (each
member's own program run directly via `vs3_apply_one` and compared over
`inp.len` bytes, exactly as Branch B does) AND the store without S_k
(`vs3_apply_skip_set`) predicts `true_out`, then S_k is the smallest
jointly-implicating prefix: apply the contradiction protocol to every
member of S_k (PROVISIONAL -> ROLLED_BACK; ACTIVE -> PROVISIONAL as a
first contradiction). Return 1 if any member was rolled back, else 2 if
any member was demoted, else continue to the next k. If no prefix fires,
fall through to Branch B unchanged.

Rationale: attribution is most-recent-first and minimal. The store's
wrong answer was produced by F[0]'s program; if removing F[0] alone
restores the trusted label (and F[0] mispredicted), only F[0] is
implicated. If removing F[0] uncovers another wrong member, the pair
jointly overrode the correct prediction, and so on. A correct shadowed
member stops the peel: the prefix containing it cannot satisfy the
all-mispredict condition, so it is never felled by a contradiction it
did not join.

New emit texts (from peeling only):
"PEEL: slot N PROVISIONAL->ROLLED_BACK (smallest firing prefix jointly
overrode a correct prediction)"
"PEEL: slot N ACTIVE->PROVISIONAL (smallest firing prefix jointly
overrode a correct prediction; first contradiction)"

No other mechanism function is touched: `vs3_apply`, `vs3_apply_skip`,
`vs3_apply_skip_set`, `vs3_firing_set`, `vs3_firing_slot`, `vs3_revise`,
`diagnose_confirm_check`, all Phase A-N code unchanged.

Revised claim (replaces the H-REVISE8 claim): 1 contradiction fells a
provisional revision and 2 fell a confirmed one. When the most-recent
prefix of firing revisions jointly overrode a correct prediction (every
prefix member mispredicts and the store without the prefix predicts the
trusted label), the contradiction protocol applies to the smallest such
prefix. If no correct uncovered baseline exists, no action is taken.

B-RV8-1 disposition (disclosure extension, not a mechanism change):
forged labels remain outside every frozen claim; the mechanism does not
authenticate labels (dual-use, as frozen since H-REVISE7). Peeling
bounds the forged blast radius to the smallest implicated prefix: a
forged label implicates only members whose removal restores the forged
label. When F = P0(X) the whole firing set is implicated and the
X-RV8-1 outcome is unchanged (both demoted by one forged label, both
rolled back by a second); a forged label matching an intermediate
uncovered prediction fells only the proper prefix. The set-wide
amplification named in B-RV8-1 is therefore narrowed to the
whole-set-implicated case.

Residuals carried forward (not repaired): X-RV5-1 append-time
underdetermination; forged-label dual-use beyond the prefix bound;
duplicate append of an ACTIVE revision; tombstone capacity.

## Frozen kill bars

**K-RV9-1 (B-RV8-2 closure):** Fixture replicated exactly from the
X-RV8-2b adversary: VSv init with P0-B=[0,0,0] identity; X="zbq";
T="qqq". vs3_revise(VSv,2,113,P0A,1) -> slot1 (correct, fires);
vs3_revise(VSv,1,98,WPROG,1) -> slot2 (wrong, fires);
vs3_revise(VSv,0,122,WPROG,1) -> slot3 (wrong, fires, most recent).
Setup sanity (FATAL if broken): pair-counterfactual
vs3_apply_skip_set(VSv,X,{3,2}) predicts T. Then
`diagnose_rollback_check(VSv,X,T)` MUST return exactly 1;
vs3_status(VSv,3)==0 AND vs3_status(VSv,2)==0 (both wrong revisions
ROLLED_BACK); vs3_status(VSv,1)==1 (correct revision untouched);
vs3_apply(VSv,X)->"qqq" exactly (restoration via slot 1).
KILL if: return==0, either wrong slot not rolled back, the correct slot
touched, or restoration not exact.

**K-RV9-2 (forged boundary unchanged):** X-RV8-1 adversary fixture:
VS init P0-A=[4,0,0]; two correct identity revisions, both confirmed to
ACTIVE on the true label "zbq". Forged F="qqq"=P0-A(X). First
`diagnose_rollback_check(VS,X,F)` MUST return exactly 2 with both slots
demoted (st1==1, st2==1); second call MUST return exactly 1 with both
slots rolled back (st1==0, st2==0). Dual-use disclosed. KILL if any
value differs.

**K-RV9-3 (regression):** All 117 inherited named CHECK lines
byte-identical to the frozen REVISE8 raw (result f03295207, md5
631cd08786189b0596c0811f92168032). Full raw diff vs that raw contains
ONLY: (a) banner/verdict rename H-REVISE8->H-REVISE9; (b) PEEL emit
lines (the two new texts) emitted from Phase P only; (c) the Phase P
block (16 CHECKs); (d) the final RESULT/ verdict lines. Expected total
133/133 (117 inherited + 16 Phase P). KILL if any inherited CHECK line
differs, the diff contains other categories, or the total is not
133/133.

**K-RV9-4 (determinism):** 3 consecutive runs byte-identical via cmp,
exit 0. KILL on any byte difference or nonzero exit.

**K-RV9-5 (minimality and veto preserved):** P3a: VS init P0-A;
vs3_revise(VS,1,98,P0A,1) -> slot1 correct PROVISIONAL (fires, predicts
T); vs3_revise(VS,0,122,WPROG,1) -> slot2 wrong PROVISIONAL (fires,
most recent). `diagnose_rollback_check(VS,X,T)` MUST return exactly 1;
st2==0 (wrong felled); st1==1 (correct fellow untouched). P3b: VS init
P0-A; vs3_revise(VS,0,122,WPROG,1) -> slot1 wrong PROVISIONAL;
vs3_revise(VS,1,98,P0A,1) -> slot2 correct PROVISIONAL (most recent).
`diagnose_rollback_check(VS,X,T)` MUST return exactly 0; st1==1 AND
st2==1 (veto preserved, no state change). KILL on any deviation.

**K-RV9-6 (tombstone interleave preserved):** X-RV8-3 adversary fixture:
VSt init P0-A; vs3_revise(VSt,0,122,WPROG,1) -> slot1; first
`diagnose_rollback_check(VSt,X,T)`==1 (slot1 ROLLED_BACK; FATAL if not);
vs3_revise(VSt,1,98,WPROG,1) -> slot2; vs3_revise(VSt,2,113,WPROG,1) ->
slot3. Second `diagnose_rollback_check(VSt,X,T)` MUST return exactly 1;
st3==0 AND st2==0 (both live wrong rolled back); st1==0 (tombstone
untouched); get32(VSt,0)==3 (vcount unchanged). KILL on any deviation.

## Phase P fixtures (hand-derived expectations, frozen)

P1 (subset closure, 5 CHECKs): P1 rb==1. P2 st3==0. P3 st2==0. P4
st1==1. P5 vs3_apply->"qqq" exact.
P2 (forged boundary, 2 CHECKs): P6 first forged call rb==2, st1==1,
st2==1. P7 second forged call rb==1, st1==0, st2==0.
P3a (minimality, 3 CHECKs): P8 rb==1. P9 st2==0. P10 st1==1.
P3b (veto, 2 CHECKs): P11 rb==0. P12 st1==1 and st2==1.
P4 (tombstone, 4 CHECKs): P13 rb==1. P14 st3==0 and st2==0. P15
st1==0. P16 vcount==3.

## Governance (frozen)

Pure Zag: implementation, fixtures, builds, runs, analysis. Zero Python
at any stage, including verification. No em dashes in loop documentation
(byte-checked before commit). Binaries built in /tmp only, never
committed. Only owned paths staged (PREREG_REVISE9.md, revise9.zag,
REVISE9_RAW*.txt, REVISE9_RESULT.md). Concurrent workers' files
untouched. No push authorized.
