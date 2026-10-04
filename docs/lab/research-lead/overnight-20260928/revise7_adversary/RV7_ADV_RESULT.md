# RV7_ADV_RESULT: H-REVISE7 Red Team

**Verdict: H-REVISE7 DOWNGRADED (not killed).** One of six preregistered
attacks succeeds via an undisclosed mechanism interaction; four confirm
disclosed boundaries; regression holds.

**Frozen prereg:** `PREREG_RV7_ADV.md` (commit `ae31ee7aa`), committed alone
before any adversary code, build, or run. Ordering verified with
`git merge-base --is-ancestor` (prereg is a strict ancestor of the result
commit). No amendments.
**Date (UTC):** 2026-09-29
**Raw evidence:** `RV7_ADV_RAW.txt` (md5 `2c9435355dae736ba1979ca479a13ecb`,
3/3 runs byte-identical via cmp, exit 0,
`R7-ADV: ALL ATTACK CHECKS PASS`, 13/13 checks).
**Harness:** `rv7_adv.zag` = `revise7.zag` lines 1-638 byte-verbatim
(cmp-verified against `git show HEAD:`; everything before `fn main`) +
attack-only `main()`. Pure Zag; zero Python at any stage.
**Target:** H-REVISE7 SURVIVES (98/98, result `1d0f82708`).

## X-RV7-3 (multi-slot interference): SUCCEEDS -> DOWNGRADE

Two provisional revisions, both firing on X="zbq", both mispredicting the
trusted label T="qqq":
- slot 1: (0,122), WPROG -> "zzz"
- slot 2: (1,98), WPROG -> "zzz"
- P0-A = [4,0,0] gives P0-A("zbq") = "qqq" = T (sanity CHECK X731 PASS).

`vs3_apply` fires slot 2 (most recent) -> "zzz"; mispredict vs T confirmed
(CHECK X733 PASS). `diagnose_rollback_check(VS, X, T)` returns **0**; both
slots remain PROVISIONAL (CHECK X734 PASS).

Why: the rollback skip-test (`vs3_apply_skip` ignoring slot 2) reveals slot 1,
which also predicts "zzz" =/= T. The "revision overrode a correct prediction"
test therefore fails, and the genuine contradiction is silently absorbed.
Neither revision is rolled back, demoted, or flagged. Every future
contradiction label on X is absorbed the same way: the revisions are
effectively immune to contradiction as long as a fellow wrong revision
fires beneath the most-recent one.

Control (single firing revision): fresh VS2 with only slot 1 = (1,98);
`diagnose_rollback_check` returns **1** and the slot becomes ROLLED_BACK
(CHECK X735 PASS). The interference is load-bearing: without it the bound
holds.

Why this is a downgrade and not a boundary confirmation: the frozen K-RV7-4
bound is "1 contradiction fells a provisional revision, 2 fell a confirmed
one", stated without a single-firing caveat. Multi-slot interference is not
in the frozen disclosed-boundary list (N2, N3, B1, B2). The result doc's
causal interpretation claims `vs3_apply_skip` answers "what would the store
have predicted without this revision" as a "genuine counterfactual". That
reading is sound only when no other firing revision interferes; with
interference the counterfactual is contaminated and the inference "the
revision overrode a correct prediction" is invalid. The failure is the scope
of the guarantee, not the implementation.

Why not killed: all 98/98 frozen builder bars still hold (X-RV7-6); the
rollback/confirm/reactivation machinery does exactly what was preregistered
in the single-revision case; the X-RV5-1 residual treatment is untouched.

Narrowed claim (replaces the K-RV7-4 bound): "1 contradiction fells a
provisional revision and 2 fell a confirmed one, provided no other live
revision fires on the contradicted input. When two or more live revisions
fire on the same input and all mispredict, the rollback skip-test cannot
isolate the most-recent revision and the contradiction is absorbed with no
state change."

## X-RV7-1 (forged-confirmation flooding): boundary confirmed, no verdict change

Forged confirming label ("zbq"->"zzz") on the WRONG revision (stipulated
truth "qqq"): `diagnose_confirm_check` returns 1 and the slot is promoted
PROVISIONAL->ACTIVE (CHECK X712 PASS). A wrong revision now costs 2
contradictions instead of 1. This is the disclosed B1 limit ("not defended;
promotion is evidence-weighting, not authentication"). Confirming it does
not change the verdict.

## X-RV7-2 (rollback/re-admit oscillation): severity note, no verdict change

Three full cycles under the forged label ("xqw"->"xqw" = P0 output):
ROLLBACK (status 1->0) -> REACTIVATE (status 0->1, vcount stable at 1),
repeated 3x with no convergence (CHECK X722 PASS). The protocol cannot
settle under adversarial labels. This is a severity note on disclosed N2
(dual-use); the frozen bars never claimed convergence. No verdict change.

## X-RV7-4 (duplicate append of ACTIVE): boundary confirmed, no verdict change

Re-deriving the ACTIVE revision's (0,122) appends slot 2 as a duplicate
(vcount 2, identical conditions, slot 1 ACTIVE, slot 2 PROVISIONAL; CHECK
X742 PASS). The R4 scan matches tombstones only. This is the disclosed N3
known gap. Confirming it does not change the verdict.

## X-RV7-5 (tombstone capacity): boundary confirmed, no verdict change

Four revisions rolled back (status 0 x4, vcount 4); a fifth `vs3_revise`
returns -1 with VS3FULL (CHECK X752 PASS). Tombstones occupy capacity though
no live revision exists. This is the disclosed B2 limit. Confirming it does
not change the verdict.

## X-RV7-6 (regression): HOLDS

Rebuilt `revise7.zag` from `git show HEAD:` (cmp-verified identical to
worktree): 3/3 runs byte-identical, md5
`6b783965c82d1b5483808a36ed4f78e7` matches the frozen value, "98/98"
present. No silent changes, no nondeterminism.

## Causal interpretation

The rollback protocol's soundness rests on an isolation assumption: that
the store-without-the-firing-revision exhibits the pre-revision behavior.
That assumption holds for a single firing revision (control X735) but fails
when revisions stack on overlapping conditions. The skip-test is a true
counterfactual about the store minus one slot, but the *inference* drawn
from it ("overrode a correct prediction") requires the further premise that
the uncovered behavior is the trustworthy baseline. With interference, the
uncovered behavior is another untrusted revision. A principled repair would
need to iterate the skip-test over all firing revisions, or roll back the
firing *set* when every member mispredicts.

## Classification

Bounded L2+ revision with a self-correction protocol, narrowed. Not L3.

## Governance disclosures

1. Prereg `ae31ee7aa` strictly precedes all adversary code and execution;
   verified with `git merge-base --is-ancestor`. No amendments. First
   execution matched every hand-derived expectation; zero tuning.
2. Pure Zag throughout: implementation, fixtures, builds, runs, analysis.
   Zero Python at any stage. (One `python3 -c` byte-count was used to check
   the prereg file for em-dash bytes before committing; it touched no
   research evidence. Recorded, not hidden.)
3. No em dashes in loop documentation (byte-verified).
4. Binaries built in /tmp/rv7adv only, never committed. Only
   `revise7_adversary/` paths staged. Concurrent workers' files untouched.
5. All commits local; no push authorized or attempted.

## Files (branch `tnn-native-lab`)

- `revise7_adversary/PREREG_RV7_ADV.md` (frozen prereg, commit `ae31ee7aa`)
- `revise7_adversary/rv7_adv.zag` (adversary harness)
- `revise7_adversary/RV7_ADV_RAW.txt` (raw evidence, md5
  `2c9435355dae736ba1979ca479a13ecb`, 3/3 identical)
- `revise7_adversary/RV7_ADV_RESULT.md` (this report)

## Suggested follow-ups (for the parent, not findings)

1. H-REVISE8 repair: iterate the rollback skip-test over the full firing
   set, or roll back all firing revisions when every member mispredicts the
   trusted label. Suggested kill bar: the X-RV7-3 fixture ->
   `diagnose_rollback_check` returns nonzero (both slots addressed) while
   the X735 control still returns exactly 1.
2. The paper's H-REVISE7 line must read DOWNGRADED with the narrowed
   K-RV7-4 claim.
