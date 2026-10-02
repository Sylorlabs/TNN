# PREREG H-REVISE7 RED TEAM FROZEN

Date (UTC): 2026-09-29 (preregistered before any adversary code, build, or run)
Branch: tnn-native-lab
Target: H-REVISE7 SURVIVES (98/98, 3/3 deterministic; result 1d0f82708)
Adversary: independent red team. Assume the claim is false.

## Frozen background facts

1. H-REVISE7 implements second-order revision: every revision enters
   PROVISIONAL (status byte 1 at so+60); diagnose_rollback_check rolls back
   (returns 1) or demotes (returns 2) the most-recent firing revision when the
   skip-test shows the store-without-it predicts the trusted label;
   diagnose_confirm_check promotes (returns 1) a PROVISIONAL revision when VS
   is correct and P0 would have mispredicted; vs3_revise reactivates a
   tombstoned slot with identical (cpos,cval) instead of duplicating.
2. Frozen bound under test (K-RV7-4): "1 contradiction fells a provisional
   revision, 2 fell a confirmed one." Stated without qualification.
3. Frozen disclosed non-goals (NOT re-litigated; confirming them changes
   nothing):
   N2. Forged contradiction labels are indistinguishable from genuine ones;
       an adversary holding the label channel can roll back any revision.
   N3. Duplicate append when propose re-derives an ACTIVE revision's
       (cpos,cval) is a known gap.
   B1. Adversarial confirmation-forgery (flooding confirming labels to
       promote a wrong revision) is not defended.
   B2. Tombstones occupy capacity: 4 tombstoned slots refuse appends with
       VS3FULL.
4. X-RV5-1/X-RV6-1 remains a confirmed residual (undetectable at append time).
   Not re-litigated.

## Method (frozen)

- Harness: revise7.zag lines 1-638 (everything before `fn main`), copied
  verbatim and cmp-verified, plus an attack-only main. No mechanism edits.
- Programs are hand-built node triples. P0-A = [4,0,0] (single node type 4
  = constant 2): for a 3-char input, out[k] = inp[2] for all k.
  P0-B = [0,0,0] (identity). WPROG = [2,0,0] (single node type 2 =
  constant 0): out[k] = inp[0] for all k.
- All fixtures hand-derived below. First execution must match or the fixture
  is broken (reported, not tuned).
- Every attack run 3/3; byte-identical required.
- Pure Zag throughout. No Python at any stage.

## X-RV7-1 (forged-confirmation flooding): boundary confirmation expected

Setup: fresh VS, vs3_init(VS, P0-A=[4,0,0], 1). X="zbq", stipulated truth
T="qqq". P0-A(X)="qqq".
vs3_revise(VS, 0, 122, WPROG, 1) -> slot 1 PROVISIONAL. WPROG(X)="zzz" =/= T,
so the revision is WRONG relative to stipulated truth.
Forged confirming label F="zzz". vs3_apply(VS,X) -> "zzz" == F (correct per
forged label; verify).
c = diagnose_confirm_check(VS, X, F).
SUCCESS CRITERION (boundary confirmation of disclosed B1): c==1 AND
vs3_status(VS,1)==2 (ACTIVE). A forged confirming label promotes a wrong
revision, raising its contradiction cost from 1 to 2. This is the disclosed
"not defended" limit; confirming it does not change the verdict.

## X-RV7-2 (rollback/re-admit oscillation): severity note expected

Setup: fresh VS, vs3_init(VS, P0-B=[0,0,0] identity, 1). X="xqw", genuine
truth T="xxx". RPROG=WPROG=[2,0,0]; RPROG(X)="xxx"=T (genuine revision).
vs3_revise(VS, 0, 120, RPROG, 1) -> slot 1 PROVISIONAL ('x'=120).
Forged label F="xqw" (= P0-B output).
Repeat 3 cycles; each cycle:
  (a) vs3_apply(VS,X) -> "xxx" =/= F (mispredict; verify).
  (b) r=diagnose_rollback_check(VS,X,F) -> skip-test falls to P0-B -> "xqw"
      == F, so r==1 and status -> 0 ROLLED_BACK (verify).
  (c) vs3_revise(VS, 0, 120, RPROG, 1) -> R4 REACTIVATE slot 1, status -> 1
      PROVISIONAL, vcount stays 1 (verify).
SUCCESS CRITERION (oscillation demonstration): all 3 cycles complete with
r==1 each time, vcount==1 throughout, status oscillating 1->0->1->0->1->0.
The system never converges under adversarial labels. This is a severity
note on disclosed N2, not a new finding; it does not change the verdict.

## X-RV7-3 (multi-slot interference in the rollback skip-test): DOWNGRADE CANDIDATE

Setup: fresh VS, vs3_init(VS, P0-A=[4,0,0], 1). X="zbq", trusted label
T="qqq". P0-A(X)="qqq".
vs3_revise(VS, 0, 122, WPROG, 1) -> slot 1 PROVISIONAL (fires on X via
inp[0]=='z'; predicts "zzz" =/= T).
vs3_revise(VS, 1, 98, WPROG, 1) -> slot 2 PROVISIONAL (fires on X via
inp[1]=='b'; predicts "zzz" =/= T).
Verify: vs3_apply(VS,X) -> "zzz" (slot 2, most recent, fires); mispredict
vs T confirmed.
r = diagnose_rollback_check(VS, X, T).
DOWNGRADE CRITERION: r==0 AND vs3_status(VS,1)==1 AND vs3_status(VS,2)==1.
Both firing revisions genuinely mispredict the trusted label, yet the
rollback does not fire: the skip-test's counterfactual is contaminated by
the other firing revision (skipping slot 2 reveals slot 1, also wrong), so
the "revision overrode a correct prediction" test fails and the genuine
contradiction is silently absorbed. This falsifies the frozen K-RV7-4 bound
"1 contradiction fells a provisional revision", which was stated without a
single-firing caveat and is not in the disclosed boundary list.
Control: fresh VS2, vs3_init(VS2, P0-A, 1), only
vs3_revise(VS2, 1, 98, WPROG, 1) -> slot 1.
r2 = diagnose_rollback_check(VS2, X, T).
CONTROL CRITERION: r2==1 AND vs3_status(VS2,1)==0. Proves the interference
is load-bearing: without it the bound holds.

## X-RV7-4 (duplicate append of an ACTIVE revision): boundary confirmation expected

Setup: fresh VS, vs3_init(VS, P0-A=[4,0,0], 1).
vs3_revise(VS, 0, 122, WPROG, 1) -> slot 1 PROVISIONAL.
Genuine confirm: label ("zbq"->"zzz"). vs3_apply -> "zzz" (correct);
P0-A -> "qqq" =/= "zzz" (mispredicts). diagnose_confirm_check -> 1,
status -> 2 ACTIVE (verify).
vs3_revise(VS, 0, 122, WPROG, 1) again (re-derived identical condition).
SUCCESS CRITERION (boundary confirmation of disclosed N3): vcount==2 AND
slot1 (cpos,cval)==(0,122) AND slot2 (cpos,cval)==(0,122) AND
vs3_status(VS,1)==2 AND vs3_status(VS,2)==1. The R4 scan only matches
tombstones, so the ACTIVE duplicate is appended. Disclosed gap; confirming
it does not change the verdict.

## X-RV7-5 (tombstone capacity): boundary confirmation expected

Setup: fresh VS, vs3_init(VS, P0-A=[4,0,0], 1).
Four revisions with mutually exclusive position-0 conditions:
 slot1: vs3_revise(VS, 0, 122, WPROG, 1); input "zbq" -> "zzz"; P0-A -> "qqq";
        forged label "qqq"; diagnose_rollback_check -> 1 (verify).
 slot2: vs3_revise(VS, 0, 121, WPROG, 1); input "ybq" -> "yyy"; P0-A -> "qqq";
        forged label "qqq"; diagnose_rollback_check -> 1 (verify).
 slot3: vs3_revise(VS, 0, 120, WPROG, 1); input "xbq" -> "xxx"; P0-A -> "qqq";
        forged label "qqq"; diagnose_rollback_check -> 1 (verify).
 slot4: vs3_revise(VS, 0, 119, WPROG, 1); input "wbq" -> "www"; P0-A -> "qqq";
        forged label "qqq"; diagnose_rollback_check -> 1 (verify).
Verify: vcount==4 and all four slots status==0.
r5 = vs3_revise(VS, 0, 118, WPROG, 1).
SUCCESS CRITERION (boundary confirmation of disclosed B2): r5==-1 AND
vcount==4 AND all statuses 0. Four tombstones refuse a new append with
VS3FULL even though no live revision exists. Disclosed; confirming it does
not change the verdict.

## X-RV7-6 (regression)

Rebuild revise7.zag from `git show HEAD:...`, run 3x.
HOLDS iff: all 3 runs byte-identical AND md5 ==
6b783965c82d1b5483808a36ed4f78e7 (frozen) AND "98/98" present.

## Verdict rule (frozen)

- If X-RV7-3 DOWNGRADE CRITERION is met (and CONTROL CRITERION holds):
  H-REVISE7 is DOWNGRADED (not killed). One attack succeeds via an
  undisclosed mechanism interaction. All 98/98 frozen bars still hold; the
  failure is the scope of the K-RV7-4 guarantee, not the implementation.
- X-RV7-1, X-RV7-2, X-RV7-4, X-RV7-5 confirm disclosed limits; they do not
  change the verdict under any outcome consistent with the disclosure.
- If X-RV7-3 fails (rollback fires despite interference) and no new
  non-disclosed harm is found: H-REVISE7 SURVIVES this red team.
- Any fixture that does not reproduce its hand-derived expectation on first
  execution is reported as VOID (broken fixture), not tuned.

## Governance

- This prereg is committed alone before any adversary code, build, or run.
- Only adversary-owned paths under revise7_adversary/ will be staged.
- No binaries committed. No em dashes in loop documentation.
- Pure Zag. No Python.
