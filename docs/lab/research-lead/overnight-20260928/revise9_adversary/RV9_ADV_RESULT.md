# H-REVISE9 RED TEAM: ADVERSARY RESULT

**Red-team verdict: H-REVISE9 SURVIVES the red team.** No kill trigger
fired. No downgrade trigger fired. One new boundary confirmed
(B-RV9-3, no-contradiction direct-call misuse). One frozen "would"
verified empirically (forged intermediate-prefix narrowing). One
disclosed boundary confirmed at depth 4 (B-RV9-1). Classification
remains bounded L2+ revision with firing-set contradiction protocol
plus peeling attribution. Not L3.

## 1. Methodology (exact sequence)

1. Read the builder prereg (`PREREG_REVISE9.md`), builder result
   (`REVISE9_RESULT.md`), and the committed `revise9.zag` mechanism
   (`diagnose_rollback_check` lines 517-640, helpers lines 292-516).
2. Wrote adversary prereg `PREREG_RV9_ADV.md` with five frozen attacks
   (X-RV9-1 through X-RV9-5) and explicit kill / downgrade /
   boundary-confirmation / hold criteria.
3. Committed the prereg ALONE as `045d5981a` before any harness build,
   compile, or run. Verified strict ancestry later via
   `git merge-base --is-ancestor`.
4. Extracted committed `revise9.zag` lines 1-806 (mechanism region;
   `fn main()` starts at line 807) via `git show HEAD:`, cmp-verified
   byte-identical to the worktree copy.
5. Appended the attack-only `main()` (17 named CHECKs, FATAL setup
   guards so a broken fixture cannot silently pass). No mechanism byte
   altered.
6. Compiled with pinned `znc 2026.07.0-dev (edition 2026)` to
   `/tmp/rv9adv/rv9adv_bin` (exit 0; only environmental zagd warning).
   Binary never committed.
7. Ran 3x: exit 0 each, 3/3 byte-identical via cmp, md5
   `d04cfd0b9fea1d819ddbb86b7cc327a7`.
8. Ran X-RV9-5: rebuilt the FULL committed `revise9.zag` (1826 lines,
   from `git show HEAD:`, cmp-verified) 3x: exit 0, 3/3 byte-identical,
   cmp-identical to frozen `REVISE9_RAW.txt` (md5
   `1388c8e2d151039b2956beb4b86bd81c`, the frozen value), 133/133,
   "H-REVISE9 SURVIVES" present, zero failed CHECK lines.
9. Pure Zag throughout: prereg, harness, builds, runs, greps, md5, cmp.
   Zero Python at any stage.

## 2. Attack results (17/17 attack CHECKs pass)

### X-RV9-1a: deep 4-peel (smallest-prefix attribution at depth 4)

Fixture: VS init P0=identity. slot1 (2,113) p0a correct -> "qqq";
slot2 (1,98) wprog -> "zzz"; slot3 (0,122) wprog -> "zzz"; slot4
(2,113) wprog -> "zzz", most recent (duplicate condition of the live
slot1; the R4 reactivation rule matches only tombstoned slots, so this
appends as slot4; store at capacity 4). All four fire on "zbq". Setup
sanity held: vs3_apply -> "zzz" (genuine contradiction vs "qqq").

Result: `diagnose_rollback_check` returned 1. PEEL emits felled slots
4, 3, 2 in most-recent-first order; slot1 untouched. Restoration:
vs3_apply -> "qqq" exact via slot1.

- CHECK A1 rb==1: PASS.
- CHECK A2 st4==0, st3==0, st2==0: PASS.
- CHECK A3 st1==1: PASS.
- CHECK A4 restoration "qqq": PASS.

Verdict: HOLD. The peel correctly identified the smallest
jointly-implicating prefix {4,3,2} at depth 4 (k=3 fired; k=1 and k=2
correctly did not, since removing {4} or {4,3} still left a wrong
predictor). No kill trigger.

### X-RV9-1b: B-RV9-1 boundary confirmation at depth 4

Fixture: slot1 (0,122) wprog -> "zzz" (older, wrong); slot2 (2,113)
p0a -> "qqq" (correct); slot3 (1,98) wprog -> "zzz"; slot4 (2,113)
wprog -> "zzz", most recent. Setup sanity held: vs3_apply -> "zzz".

Result: return 1; slots 4 and 3 ROLLED_BACK (peel k=2 fired on {4,3});
slot2 correct untouched; slot1 (older wrong member below the correct
member) survived with status 1.

- CHECK A5 rb==1: PASS.
- CHECK A6 st4==0, st3==0: PASS.
- CHECK A7 st2==1: PASS.
- CHECK A8 st1==1: PASS.

Verdict: CONFIRMED BOUNDARY. B-RV9-1 ("an older wrong member below a
correct member can survive a contradiction it did not join") holds at
depth 4. The peel stopped at the correct member exactly as disclosed;
the surviving wrong member is felled only when a later failure
implicates it. Not a kill (this is the disclosed behavior).

### X-RV9-2: forged intermediate-prefix narrowing (the "would" in B-RV8-1)

`PREREG_REVISE9.md` disposed B-RV8-1 with the prediction: "a forged
label matching an intermediate uncovered prediction would fell only
the proper prefix." This attack executed that prediction.

Fixture: VS init P0=p0a. slot1 (0,122) mid=[3,0,0] -> "bbb" (wrong vs
the true label "qqq", but its prediction matches the forged label);
slot2 (1,98) wprog -> "zzz"; slot3 (2,113) wprog -> "zzz", most
recent. Setup sanity held: vs3_apply -> "zzz". Forged F = "bbb".

Result: Branch A did not fire (skip {3} -> "zzz" != "bbb"); peel k=1
did not fire (skip {3} -> "zzz"); peel k=2 fired on {3,2} (both
mispredict "bbb"; store without {3,2} -> slot1 -> "bbb"); slots 3 and
2 ROLLED_BACK; return 1; slot1 untouched.

- CHECK B1 rb==1: PASS.
- CHECK B2 st3==0, st2==0: PASS.
- CHECK B3 st1==1: PASS.

Verdict: CONFIRMED (narrowing verified). The frozen "would" is now an
empirically verified "does": a forged label matching an intermediate
uncovered prediction fells only the proper prefix {3,2}, not the
whole firing set. Contrast with the X-RV8-1 shape (F = P0(X), whole
set implicated) where both members are felled. The B-RV8-1 disposition
stands as written; no downgrade trigger fired. Forged labels remain
outside every frozen claim (dual-use, as frozen since H-REVISE7).

### X-RV9-3: ACTIVE-member peeling interactions ("2 fell a confirmed one")

Fixture: VS init P0=p0a. slot1 (2,113) p0a -> "qqq" PROVISIONAL.
slot2 (1,98) ident -> "zbq" PROVISIONAL; setup sanity held
(vs3_apply -> "zbq"); genuine confirmation
`diagnose_confirm_check(VS,"zbq","zbq")` returned 1 (firing slot was
slot2; P0=p0a predicts "qqq" != "zbq", so promotion legitimate);
slot2 verified ACTIVE (status 2). slot3 (0,122) wprog -> "zzz" wrong
PROVISIONAL, most recent.

First contradiction `diagnose_rollback_check(VS,"zbq","qqq")`:
Branch A did not fire (skip {3} -> slot2 "zbq" != "qqq"); peel k=1
did not fire (skip {3} -> "zbq"); peel k=2 fired on {3,2} (both
mispredict "qqq"; skip {3,2} -> slot1 "qqq"). Protocol: slot3
PROVISIONAL->ROLLED_BACK; slot2 ACTIVE->PROVISIONAL (demoted, NOT
rolled back); return 1 (a rollback occurred, so return 1 per the
frozen "return 1 if any rolled back, else 2 if any demoted" rule).

- CHECK C1 rb1==1: PASS.
- CHECK C2 st3==0, st2==1, st1==1: PASS.

Second contradiction (same call again): firing set is now {2,1}
(slot3 tombstoned, excluded from the firing set). Branch A fired on
slot2 (skip {2} -> slot1 "qqq"); slot2 ROLLED_BACK; return 1.

- CHECK C3 rb2==1: PASS.
- CHECK C4 st2==0, st1==1: PASS.

Verdict: HOLD. "2 fell a confirmed one" holds end-to-end through the
peel path: first contradiction demotes (ACTIVE->PROVISIONAL), second
fells (PROVISIONAL->ROLLED_BACK). The mixed-prefix return-code
precedence (rollback beats demotion) behaved as frozen. No kill
trigger. In particular, the ACTIVE member was NOT rolled back on the
first contradiction; had it been (st2==0 after call 1), that would
have KILLED.

### X-RV9-4: no-contradiction direct-call misuse (Branch A asymmetry)

Code inspection (frozen observation, verified against source lines
517-541): Branch A fells fset[0] when its status is 1 or 2 and the
store without fset[0] predicts true_out. It does NOT check that
fset[0]'s own program mispredicts true_out. The peeling loop and
Branch B both require every implicated member to mispredict;
Branch A is the only path without that check. Under the documented
precondition ("CALL ONLY after vs3_apply mispredicted true_out",
which the builder's own harness enforces by verifying misprediction
before every call), fset[0] necessarily mispredicts, so the missing
check is harmless in protocol-conformant use.

Fixture: VS init P0=identity. slot1 (2,113) p0a -> "qqq" correct
PROVISIONAL; slot2 (1,98) p0a -> "qqq" correct PROVISIONAL, most
recent. Setup sanity held (CHECK D1 PASS): vs3_apply -> "qqq". NO
contradiction exists.

Misuse call `diagnose_rollback_check(VS,"zbq","qqq")`: Branch A fired
(skip {slot2} -> slot1 -> "qqq" == T). MISUSE-OUTCOME: rb=1, st1=1,
st2=0. A CORRECT top member was ROLLED_BACK with zero contradiction.

- CHECK D1 no contradiction exists: PASS.
- CHECK D2: BOUNDARY B-RV9-3 CONFIRMED.

Verdict: CONFIRMED NEW BOUNDARY B-RV9-3 (no-contradiction
direct-call misuse). Not a KILL and not a DOWNGRADE: the frozen
revised claim is conditional on a contradiction existing ("When the
most-recent prefix of firing revisions jointly overrode a correct
prediction..."), and no frozen bar covers precondition-violating
calls. But it is a genuine robustness gap, and a cheaply closable
one: unlike label authenticity (unknowable in-function, hence the
forged-label dual-use disclosure), the contradiction precondition is
machine-checkable with one `vs3_apply` + `streq`. The lineage already
sets a defense-in-depth precedent (the R5 nn1<=0 withhold guard in
`diagnose_corroborate_v6`). Recommended: a future repair adds an
in-function "no contradiction -> return 0, no state change" guard.
The paper must disclose B-RV9-3. All protocol-conformant callers
(including the builder's harness) are unaffected.

### X-RV9-5: regression

Rebuilt the full committed `revise9.zag` (1826 lines, extracted via
`git show HEAD:`, cmp-verified byte-identical to worktree), ran 3x.

- E1: 3/3 byte-identical via cmp, exit 0: PASS.
- E2: cmp-identical to frozen `REVISE9_RAW.txt` (md5
  `1388c8e2d151039b2956beb4b86bd81c`, the frozen value): PASS.
- E3: output contains "133/133" and "H-REVISE9 SURVIVES"; zero failed
  CHECK lines (the two "CORROBORATE FAIL" emits are the builder's own
  expected negative-path fixture outputs, not CHECK failures): PASS.

Verdict: HOLD. No regression.

## 3. Code observation (not an attack; no verdict attached)

Peel iteration k=1 is unreachable dead code, shadowed by Branch A.
Proof from the source: Branch A fires iff st(fset[0]) in {1,2} and
`vs3_apply_skip` without fset[0] predicts true_out. Peel k=1 fires
iff fset[0]'s own program mispredicts true_out and
`vs3_apply_skip_set` without {fset[0]} predicts true_out. The two
skip calls are semantically identical (skip exactly one slot), and
every firing-set member has status 1 or 2 (the firing set excludes
tombstoned slots; statuses are only 0/1/2). Hence peel k=1's
condition implies Branch A's condition, and Branch A runs first.
The loop `while(k<nf)` starting at k=1 therefore never fires its
first iteration. Harmless redundancy; matches the frozen spec text
("for k = 1 .. nf-1"). The one behavioral case where Branch A fires
but peel k=1 could not (fset[0]'s own program PREDICTS true_out) is
exactly the X-RV9-4 misuse shape. Noted for a future cleanup pass;
no claim is affected.

## 4. Boundaries after this red team

- B-RV8-1: forged firing-set amplification, now NARROWED and
  VERIFIED: whole-set implication only when the forged label equals
  the store-without-whole-set prediction (X-RV8-1 shape, unchanged);
  a forged label matching an intermediate uncovered prediction fells
  only the proper prefix (X-RV9-2, verified this round). Dual-use
  disclosure stands.
- B-RV8-2: closed by R7 (builder); the 4-deep generalization holds
  (X-RV9-1a).
- B-RV9-1: older wrong member below a correct member survives a
  contradiction it did not join; confirmed at depth 4 (X-RV9-1b).
- B-RV9-2: append-time X-RV5-1 underdetermination unchanged (not
  probed this round; carried forward).
- B-RV9-3 (NEW, this round): direct calls to
  `diagnose_rollback_check` without a genuine contradiction can fell
  a correct top member via Branch A, the only path lacking the
  all-mispredict check. Protocol-conformant callers unaffected. Fix
  proposed: in-function contradiction guard (defense in depth).

Classification remains bounded L2+ revision with a firing-set
contradiction protocol plus peeling attribution. Not L3.

## 5. Governance disclosures

1. Adversary prereg `PREREG_RV9_ADV.md` committed alone as
   `045d5981a` before any harness build, compile, or run. Strict
   ancestry verified with `git merge-base --is-ancestor`. No
   amendments.
2. Pure Zag throughout: prereg, harness, builds, runs, hashes, diffs,
   analysis. Zero Python at any stage, including verification.
3. Harness = committed `revise9.zag` lines 1-806 byte-verbatim
   (cmp-verified against `git show HEAD:`) + attack-only `main()`.
   No mechanism byte altered.
4. Binaries built in `/tmp/rv9adv` only, never committed. No
   `.zag-cache` committed.
5. Pathspec-restricted staging: only the five owned adversary paths
   in `revise9_adversary/` (+ the already-committed prereg).
   Concurrent workers' files untouched.
6. Zero em dashes in all adversary-authored documentation
   (byte-checked with grep for U+2014).
7. No fixture was redesigned or rerun post-hoc. X-RV9-4's D2 outcome
   was recorded exactly as the frozen criteria directed
   (boundary-confirm vs hold); the observed outcome matched the
   boundary-confirm branch.
8. No push attempted or authorized. Local branch `tnn-native-lab`
   only.

## 6. Files (branch `tnn-native-lab`)

- `docs/lab/research-lead/overnight-20260928/revise9_adversary/PREREG_RV9_ADV.md`
  (copy of the frozen prereg; canonical commit `045d5981a`)
- `docs/lab/research-lead/overnight-20260928/revise9_adversary/rv9_adv.zag`
  (adversary harness)
- `docs/lab/research-lead/overnight-20260928/revise9_adversary/RV9_ADV_RAW.txt`
  (+ `_R2`, `_R3`; md5 `d04cfd0b9fea1d819ddbb86b7cc327a7`, 3/3
  byte-identical, exit 0, 17/17 CHECKs pass)
- `docs/lab/research-lead/overnight-20260928/revise9_adversary/RV9_ADV_RESULT.md`
  (this report)

## 7. Recommended follow-ups for the parent

1. Record B-RV9-3 in the paper/CANONICAL_STATE as a disclosed
   boundary with the proposed in-function contradiction guard as
   future repair work.
2. Record the X-RV9-2 verification: the B-RV8-1 disposition's
   "would" is now verified; the forged blast radius is the smallest
   implicated prefix.
3. Consider a characterization of the peel k=1 dead code in a
   cleanup pass (no behavior change).
4. H-REVISE10 frontier (if pursued): the in-function contradiction
   guard for B-RV9-3; 5-deep peel; ACTIVE-member peel with 3+
   stacked wrong members; forged labels against mixed
   ACTIVE/PROVISIONAL stacks.
