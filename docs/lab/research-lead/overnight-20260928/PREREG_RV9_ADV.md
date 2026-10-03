# PREREG H-REVISE9 RED TEAM (ADVERSARY): FROZEN

**Date (UTC):** 2026-09-30
**Target:** H-REVISE9 (builder result `86e63927b`; prereg `e6fbe9f77`).
Builder claim: SURVIVES 133/133. R7 peeling protocol in
`diagnose_rollback_check`: Branch A (single most-recent slot) unchanged,
then peeling loop over proper prefixes S_k = {fset[0..k-1]} for
k = 1 .. nf-1 (smallest prefix whose members all mispredict true_out
and whose removal restores true_out gets the contradiction protocol),
then Branch B (whole firing set) unchanged. Status codes: 0 =
ROLLED_BACK, 1 = PROVISIONAL, 2 = ACTIVE. Revised frozen claim: "1
contradiction fells a provisional revision and 2 fell a confirmed one.
When the most-recent prefix of firing revisions jointly overrode a
correct prediction (every prefix member mispredicts and the store
without the prefix predicts the trusted label), the contradiction
protocol applies to the smallest such prefix. If no correct uncovered
baseline exists, no action is taken."
**Adversary stance:** assume the claim is false. Five frozen attacks.
Kill/downgrade/boundary criteria are frozen below BEFORE any harness
build, compile, or run.
**This prereg is committed alone, before any attack code exists. No
amendments.**

## Shared fixture idioms (copied from the builder's Phase P)

- `p0aP=[4,0,0]` (out[k]=inp[2]); `p0bP=[0,0,0]` (identity);
  `wprogP=[2,0,0]` (out[k]=inp[0]); `identP=[0,0,0]` (identity);
  `midP=[3,0,0]` (out[k]=inp[1]).
- `inX="zbq"`, `T="qqq"`. On "zbq": p0aP -> "qqq", wprogP -> "zzz",
  identP -> "zbq", midP -> "bbb".
- Firing conditions on "zbq": (0,122) [X[0]='z'], (1,98) [X[1]='b'],
  (2,113) [X[2]='q'].
- Store capacity is 4 revisions; each attack uses a fresh VS.

## Verdict taxonomy (frozen)

- KILL: a frozen builder claim (the revised R7 claim above) is
  falsified by the attack. H-REVISE9 does not survive.
- DOWNGRADE: the core mechanism claim holds, but a frozen disclosure
  statement from PREREG_REVISE9.md / REVISE9_RESULT.md is falsified.
- CONFIRMED BOUNDARY: a disclosed limit (or a newly found one) is
  verified empirically. Verdict unchanged.
- HOLD: the attack fails; the mechanism holds.

## X-RV9-1 (peeling-order gaming, 4 stacked revisions)

**X-RV9-1a (deep peel, smallest-prefix attribution at depth 4).**
VS init p0bP. slot1: revise(2,113,p0aP) correct -> "qqq". slot2:
revise(1,98,wprogP) wrong -> "zzz". slot3: revise(0,122,wprogP) wrong
-> "zzz". slot4: revise(2,113,wprogP) wrong -> "zzz", most recent
(duplicate condition of the live slot1; the R4 reactivation rule only
matches tombstoned slots, so this appends). All four fire on "zbq".
Setup sanity (FATAL if broken): vs3_apply -> "zzz" (genuine
contradiction vs T).
Call diagnose_rollback_check(VS,"zbq","qqq").
Expected per the revised claim: Branch A does not fire (skip {4} ->
"zzz"); peel k=1, k=2 do not fire; peel k=3 fires on {4,3,2}; slots
4,3,2 ROLLED_BACK; slot1 untouched; return 1; restoration "qqq".
CHECKs: A1 rb==1. A2 st4==0 && st3==0 && st2==0. A3 st1==1. A4
vs3_apply -> "qqq" exact.
KILL if any of A1-A4 fails (smallest-prefix attribution false at
depth 4).

**X-RV9-1b (B-RV9-1 boundary confirmation at depth 4).**
VS init p0bP. slot1: revise(0,122,wprogP) wrong -> "zzz" (older).
slot2: revise(2,113,p0aP) correct -> "qqq". slot3:
revise(1,98,wprogP) wrong -> "zzz". slot4: revise(2,113,wprogP) wrong
-> "zzz", most recent. Setup sanity (FATAL if broken): vs3_apply ->
"zzz".
Call diagnose_rollback_check(VS,"zbq","qqq").
Expected per disclosed B-RV9-1 ("an older wrong member below a correct
member can survive a contradiction it did not join"): peel k=2 fires
on {4,3}; slots 4,3 ROLLED_BACK; return 1; slot2 (correct) untouched;
slot1 (older wrong, not in the implicated prefix) survives.
CHECKs: A5 rb==1. A6 st4==0 && st3==0. A7 st2==1. A8 st1==1.
CONFIRMED BOUNDARY (B-RV9-1 holds at depth 4) if all of A5-A8 hold.
KILL if A5, A6, or A7 fails, or if st1==0 (a non-implicated member
was felled).

## X-RV9-2 (forged-label prefix shapes; the "would" in B-RV8-1)

PREREG_REVISE9.md disposes B-RV8-1 with: "a forged label matching an
intermediate uncovered prediction would fell only the proper prefix."
The word "would" marks this as predicted, never executed. This attack
executes it.
VS init p0aP. slot1: revise(0,122,midP) -> "bbb" (wrong vs the true
label "qqq", but its prediction will match the forged label). slot2:
revise(1,98,wprogP) -> "zzz". slot3: revise(2,113,wprogP) -> "zzz",
most recent. Setup sanity (FATAL if broken): vs3_apply -> "zzz".
Forged F = "bbb" (equals slot1's prediction; slot1 is uncovered once
{3,2} are removed).
Call diagnose_rollback_check(VS,"zbq","bbb").
Expected per the frozen disposition: Branch A does not fire (skip {3}
-> "zzz"); peel k=1 does not fire (skip {3} -> "zzz"); peel k=2 fires
on {3,2} (both mispredict "bbb"; store without {3,2} -> slot1 ->
"bbb"); slots 3,2 ROLLED_BACK; return 1; slot1 untouched.
CHECKs: B1 rb==1. B2 st3==0 && st2==0. B3 st1==1.
CONFIRMED (the narrowing is real; the "would" becomes verified) if
B1-B3 hold. DOWNGRADE if violated (e.g. the whole set is felled
including slot1, or rb==0): the frozen B-RV8-1 disposition text is
false. The core R7 claim is not implicated either way (forged labels
are outside it).

## X-RV9-3 (ACTIVE-member peeling interactions; "2 fell a confirmed one")

VS init p0aP. slot1: revise(2,113,p0aP) correct -> "qqq" PROVISIONAL.
slot2: revise(1,98,identP) -> "zbq" PROVISIONAL. Setup sanity (FATAL
if broken): vs3_apply -> "zbq". Confirm slot2 to ACTIVE with a genuine
confirmation: diagnose_confirm_check(VS,"zbq","zbq") must return 1
(firing slot is slot2; P0=p0aP predicts "qqq" != "zbq", so promotion
is legitimate). FATAL if confirm != 1 or vs3_status(slot2) != 2.
slot3: revise(0,122,wprogP) -> "zzz" wrong PROVISIONAL, most recent.
First contradiction: diagnose_rollback_check(VS,"zbq","qqq").
Expected: Branch A does not fire (skip {3} -> slot2 "zbq" != "qqq");
peel k=1 does not fire (skip {3} -> "zbq"); peel k=2 fires on {3,2}
(both mispredict "qqq"; skip {3,2} -> slot1 "qqq"); slot3
PROVISIONAL->ROLLED_BACK; slot2 ACTIVE->PROVISIONAL (demoted, NOT
rolled back: one contradiction demotes a confirmed revision); return
1 (a rollback occurred).
CHECKs: C1 rb1==1. C2 st3==0 && st2==1 && st1==1.
Second contradiction (accounting end-to-end):
diagnose_rollback_check(VS,"zbq","qqq") again. Expected: firing set is
now {2,1} (slot3 tombstoned, excluded); Branch A fires on slot2
(skip {2} -> slot1 "qqq"); slot2 ROLLED_BACK; return 1.
CHECKs: C3 rb2==1. C4 st2==0 && st1==1.
KILL if any of C1-C4 fails. In particular, st2==0 after the FIRST
contradiction KILLs ("2 fell a confirmed one" violated through the
peel path).

## X-RV9-4 (no-contradiction direct-call misuse; Branch A asymmetry)

Code inspection (frozen observation, verified against lines 517-541):
Branch A fells fset[0] when st in {1,2} and the store without fset[0]
predicts true_out. It does NOT check that fset[0]'s own program
mispredicts true_out. The peeling loop and Branch B both require
all-mispredict; Branch A is the only path without it. Under the
documented precondition ("CALL ONLY after vs3_apply mispredicted
true_out", also enforced by the builder's own harness, which verifies
misprediction before every call), fset[0] necessarily mispredicts, so
the missing check is harmless. This attack violates the precondition
deliberately to test misuse robustness.
VS init p0bP. slot1: revise(2,113,p0aP) -> "qqq" PROVISIONAL, correct.
slot2: revise(1,98,p0aP) -> "qqq" PROVISIONAL, correct, most recent.
Setup sanity (FATAL if broken): vs3_apply(VS,"zbq") -> "qqq": NO
contradiction exists.
Misuse call: diagnose_rollback_check(VS,"zbq","qqq").
Predicted: Branch A fires (skip {slot2} -> slot1 -> "qqq"): rb==1,
st2==0 (a CORRECT member felled with zero contradiction), st1==1.
CHECKs: D1 setup sanity (FATAL). D2 outcome recorded.
CONFIRMED NEW BOUNDARY B-RV9-3 if the prediction holds: direct calls
without a genuine contradiction can fell a correct top member via
Branch A. Not a KILL/DOWNGRADE: the frozen revised claim is
conditional on a contradiction existing, and no frozen bar covers
precondition-violating calls. It is a genuine robustness gap: unlike
label authenticity (unknowable in-function), the contradiction
precondition is machine-checkable (one vs3_apply + streq), and the
lineage already sets a defense-in-depth precedent (the R5 nn1<=0
guard in diagnose_corroborate_v6). The paper must disclose B-RV9-3.
HOLD if rb==0 with no state change (defense-in-depth present).

## X-RV9-5 (regression)

Rebuild the committed revise9.zag main (from `git show HEAD:`) and run
3x. CHECKs: E1 3/3 byte-identical via cmp, exit 0. E2 cmp-identical to
the frozen REVISE9_RAW.txt (md5
1388c8e2d151039b2956beb4b86bd81c). E3 output contains "133/133" and
"H-REVISE9 SURVIVES".
KILL on any deviation.

## Governance (frozen)

Pure Zag: prereg, harness, builds, runs, hashes, diffs, analysis. Zero
Python at any stage, including verification. Harness = committed
revise9.zag mechanism lines (1-806; main starts at line 807)
byte-verbatim, cmp-verified against `git show HEAD:`, + attack-only
main(). Binaries in /tmp/rv9adv only, never committed. Only owned
adversary paths staged (PREREG_RV9_ADV.md, rv9_adv.zag,
RV9_ADV_RAW*.txt, RV9_ADV_RESULT.md). Concurrent workers' files
untouched. No em dashes in adversary documentation (byte-checked).
No push authorized.
