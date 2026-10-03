# RV8_ADV_RESULT: H-REVISE8 Red Team

**Verdict: H-REVISE8 SURVIVES.** No kill or downgrade criterion fired.
Two new boundaries confirmed (one amplified dual-use, one functional
gap); two probes hold; regression holds.

**Frozen prereg:** `PREREG_RV8_ADV.md` (commit `3f857df32`), committed
alone before any adversary code, build, or run. Ordering verified with
`git merge-base --is-ancestor` (prereg is a strict ancestor of the
result commit). No amendments.
**Date (UTC):** 2026-09-29
**Raw evidence:** `RV8_ADV_RAW.txt` (md5 `29acc0f3969fc2647be0e72096b22b32`,
3/3 runs byte-identical via cmp, exit 0,
`RV8-ADV: ALL ATTACK CHECKS PASS`, 10/10 checks).
**Harness:** `rv8_adv.zag` = committed `revise8.zag` lines 1-744
byte-verbatim (cmp-verified against `git show HEAD:`; everything before
`fn main`) + attack-only `main()`. Pure Zag; zero Python at any stage.
**Target:** H-REVISE8 SURVIVES (117/117, result `f03295207`).

## X-RV8-1: forged firing-set amplification -> CONFIRMED BOUNDARY

Two correct revisions (identity program), both promoted to ACTIVE via
genuine `diagnose_confirm_check` on the true label "zbq" (CHECKs A10,
A11 PASS). Forged label F = "qqq" = P0-A("zbq"), unequal to the true
label. `diagnose_rollback_check(VS, X, F)`:

- Branch A: skip slot 2 -> slot 1 predicts "zbq" != F -> no fire.
- Branch B: both members' own programs predict "zbq" != F (allmiss=1);
  store without {2,1} = P0-A predicts F -> DEMOTE both slots
  ACTIVE->PROVISIONAL, return 2 (CHECK A12 PASS).
- Second forged call: both PROVISIONAL -> ROLLED_BACK, return 1
  (CHECK A13 PASS).

One forged label demoted two correct confirmed revisions; a second
destroyed both. Under R7 semantics this exact shape returned 0 twice
(X-RV7-3 demonstrated the absorption), so R6 strictly amplifies the
forged-label blast radius from one revision to the whole firing set.

Why a boundary and not a downgrade: the frozen disclosure states the
mechanism does not authenticate labels; forged labels are outside every
frozen claim C1-C5. The AMPLIFICATION (set-wide demotion/rollback per
forged label) is new with R6 and was not named in the frozen disclosure,
so the disclosure must be extended, but no frozen claim is falsified.

## X-RV8-2a: Branch A/B precedence -> HOLD

Precedence fixture (slot 1 correct on X, slot 2 wrong and most recent):
`diagnose_rollback_check` returns 1; only slot 2 ROLLED_BACK; slot 1
untouched PROVISIONAL (CHECK B11 PASS). Branch B did not additionally
fire. Control (correct member in set, direct call): return 0, no state
change (CHECK B10 PASS).

The branches are mutually exclusive by construction, confirmed
empirically: Branch A fires exactly when the next firing member predicts
the trusted label, which falsifies Branch B's every-member-mispredicts
antecedent. No precedence gaming exists.

## X-RV8-2b: subset/veto gap -> CONFIRMED NEW BOUNDARY

Three stacked PROVISIONAL revisions on P0-B (identity; P0 wrong on X):
slot 1 correct (program [4,0,0] predicts T="qqq"), slots 2 and 3 wrong
(WPROG predicts "zzz"). All fire on X. The pair-counterfactual is real:
`vs3_apply_skip_set` skipping {3,2} predicts T (CHECK B21 PASS), so
slots 3+2 jointly overrode slot 1's correct prediction: a genuine
shared contradiction.

`diagnose_rollback_check(VS, X, T)` returns 0; all three slots remain
PROVISIONAL (CHECK B22 PASS). Branch A: skip 3 -> slot 2 wrong -> no
fire. Branch B: slot 1's own program predicts T -> allmiss=0 -> veto.

R6 tests only the singleton most-recent (Branch A) and the whole firing
set (Branch B); intermediate subsets are never tested, so a correct
shadowed firing member vetoes the protocol even when the effective
members jointly overrode a correct prediction. The two wrong revisions
are immune to this contradiction shape.

Why a boundary and not a downgrade: frozen claim C2 is explicitly
conditional on every firing member mispredicting, which fails here by
construction. The R8 authors wrote the condition into the claim (unlike
the R7 bound the RV7 red team downgraded). Recommended follow-up for
H-REVISE9: a peeling protocol that tests subsets {fset[0..k-1]} for
increasing k, rolling back the smallest jointly-implicated prefix.

## X-RV8-3: tombstone interleaving -> HOLD

Slot 1 rolled back via a genuine contradiction (CHECK C11 PASS:
ROLLED_BACK, vcount 1). Slots 2, 3 appended PROVISIONAL with firing
conditions. `diagnose_rollback_check` on X: firing set is {3,2}; the
tombstoned slot 1 is excluded everywhere (firing set, skip-set
baseline, mutation). Branch B rolls back both live members, return 1;
slot 1 untouched; vcount unchanged at 3 (CHECK C12 PASS). Tombstone
handling is consistent across enumeration, dispatch, and protocol.

## X-RV8-4: regression -> HOLD

Committed `revise8.zag` rebuilt from `git show HEAD:`, run 3x:
byte-identical to frozen `REVISE8_RAW.txt` (md5
`631cd08786189b0596c0811f92168032`, the frozen value), exit 0,
`=== RESULT: 117/117 ===`, zero failed CHECK lines (the two raw "FAIL"
strings are expected negative-path EVIDENCE emits inside passing
fixtures, lines 114 and 121).

## Narrowed claim (unchanged, boundaries appended)

H-REVISE8's revised claim stands: 1 contradiction fells a provisional
revision and 2 fell a confirmed one; when multiple live revisions fire,
all mispredict, and the store without them predicts the trusted label,
the protocol applies to every firing member; no correct uncovered
baseline -> no action. Appended boundaries:

- B-RV8-1: one forged label demotes/rolls back the whole firing set;
  forged-label blast radius is set-wide under R6 (disclosure extension
  required).
- B-RV8-2: a correct shadowed firing member vetoes Branch B; the
  protocol never tests intermediate subsets, so jointly-implicating
  prefixes that exclude a correct member are absorbed.

Classification remains bounded L2+ revision with a firing-set
contradiction protocol. Not L3.

## Governance disclosures

1. Pure Zag throughout; zero Python at any stage (prereg, harness,
   builds, runs, hashes, diffs, file edits).
2. No em dashes in loop documentation (byte-checked).
3. Binaries built in /tmp/rv8adv only, never committed.
4. Only owned paths staged: `revise8_adversary/` (prereg was committed
   alone as `3f857df32`; this commit adds `rv8_adv.zag`,
   `RV8_ADV_RAW.txt` (+ `_R2`, `_R3`), `RV8_ADV_RESULT.md`).
   Concurrent workers' files untouched.
5. No push attempted or authorized.
6. The X-RV8-2b preregistration recorded the boundary-vs-downgrade
   judgment explicitly before execution; the verdict applies it
   unchanged.

## Files (branch `tnn-native-lab`)

- `docs/lab/research-lead/overnight-20260928/revise8_adversary/PREREG_RV8_ADV.md`
  (commit `3f857df32`)
- `docs/lab/research-lead/overnight-20260928/revise8_adversary/rv8_adv.zag`
- `docs/lab/research-lead/overnight-20260928/revise8_adversary/RV8_ADV_RAW.txt`
  (+ `_R2`, `_R3`)
- `docs/lab/research-lead/overnight-20260928/revise8_adversary/RV8_ADV_RESULT.md`
  (this report)
