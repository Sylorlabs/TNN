# PREREG H-FDCR-UNIFIED8 RED TEAM (adversary)

**Date:** 2026-09-29 (UTC 2026-09-30)
**Researcher:** H-FDCR-UNIFIED8 Red Team (independent subagent)
**Target:** H-FDCR-UNIFIED8 SURVIVES (51/51). Prereg `039d6fcaa`,
  result `11918217a`. Repair R8a-R8g: lifetime per-distinct-subject
  overflow counters (NOADD_DROP_OVL=3192, 128 entries; NOADD_DROP_EVL=3704,
  48 entries). Claims B-FU7-1 and B-FU7-2 closed at the mechanism level.
**Mission:** Assume the repair claim is false. Attack it.

## Pre-attack verification (code reading, done before this prereg)

- Diff `unified_fdcr7.zag` vs `unified_fdcr8.zag`: 316 diff lines, ALL
  additions (`>`), zero modifications to pre-existing lines. R8 is
  purely additive.
- Memory map: NOADD_DROP_COUNT=2668, BASE=2672+64*4=2928,
  OVERFLOW=2928, OVN=2932+64*4=3188, OVERFLOW2=3188,
  OVL=3192+128*4=3704, EVL=3704+48*8=4088, WORK=4096 (size constant).
  No address constant or numeric set32/get32 in FU7 collides with
  3192..4087. Region genuinely free.
- Identity is by content (streq) everywhere in R8; offsets are stable
  (append-only string table). No offset-identity confusion in R8 paths.
- ovl_add/evl_add dedup before insert; evl_remove precedes ovl_add in
  the R8d transfer (no transient double-membership, single-threaded).
- The NOTE wording ("distinct subject(s) beyond name capacity" for ov,
  "further drop events beyond overflow naming capacity" for ov2) is
  consistent with R8c/R8d semantics.

## Attack surfaces selected

The builder's PART I fixtures never exercise: (a) a cleared MAIN-named
subject re-dropped while a main slot is free (main-list excursion);
(b) the R8c no-free-OVN-slot branch (ovl-tracked re-admission with OVN
full); (c) multi-subject event transfers with differing event counts
plus a post-transfer re-drop; (d) the documented 128-entry lifetime
boundary empirically; (e) byte-level rebuild verification of the
committed source.

## Frozen attacks and kill bars

**X-FU8-1a (main-list excursion + interleaved ovl restore).**
Fixture (fresh W, fu7_pet40_world):
1. `fu8_teach_many(W,"f",1,64)`, `fu8_teach_many(W,"e",1,64)`.
   Require: total=128, ov=64, ov2=0.
2. `T f1 | is_a | animal` (f1 membered; main slot freed).
   Require: vote_lost("f1")==0, total=128, ov=64, ov2=0.
3. `T e1 | is_a | animal` (e1 membered; OVN slot freed).
   Require: vote_lost("e1")==0, total=128, ov=64, ov2=0.
4. `T e1 | is_a | pet` (extends animal to 2 features).
   Require: con_nfeat(W,1)==2, total=128, ov=64, ov2=0.
5. `T s1 | is_a | animal` (extends pet; merge re-records f1 then e1:
   f1 takes the free main slot; e1 hits the ovl path and its freed
   OVN slot).
   Require: total=130, ov=64, ov2=0, vote_lost("f1")==1,
   vote_lost("e1")==1, vote_lost("s8")==0, raw contains
   "CONCEPT-MERGE 1 into 0".
KILL: ov != 64 at step 5 (recount of a lifetime-tracked subject, or a
lost count). DOWNGRADE: ov==64 but any vote_lost wrong (naming
invariant broken without counter corruption).

**X-FU8-1b (R8c no-free-OVN-slot branch).**
Fixture (fresh W, fu7_pet40_world):
1. `fu8_teach_many(W,"f",1,64)`, `fu8_teach_many(W,"e",1,64)`.
   Require: total=128, ov=64, ov2=0.
2. `T e1 | is_a | animal`. Require: vote_lost("e1")==0.
3. `T e1 | is_a | pet`. Require: con_nfeat(W,1)==2, total=128, ov=64.
4. `T q1 | is_a | pet` (new subject fills e1's freed OVN slot).
   Require: total=129, ov=65, ov2=0, vote_lost("q1")==1.
5. `T s1 | is_a | animal` (merge re-records e1; OVN is full so the R8c
   no-slot branch must touch neither tier).
   Require: total=130, ov=65, ov2=0, vote_lost("e1")==0,
   vote_lost("q1")==1.
KILL: ov != 65 at step 5 (65->66 means the no-slot branch recounted;
65->64 means q1's count was lost). DOWNGRADE: vote_lost wrong with
ov==65.

**X-FU8-2 (multi-subject transfer, differing event counts, re-drop).**
Fixture (fresh W, fu7_pet40_world):
1. `fu8_teach_many(W,"g",1,128)`.
   Require: total=128, ov=64, ov2=0.
2. `T h1 | is_a | pet` x3. Require: total=131, ov=64, ov2=3.
3. `T h2 | is_a | pet` x2. Require: total=133, ov=64, ov2=5.
4. `T g65 | is_a | animal`. Require: vote_lost("g65")==0.
5. `T h1 | is_a | pet` (transfer, ec=3).
   Require: total=134, ov=65, ov2=2, vote_lost("h1")==1.
6. `T g66 | is_a | animal`. Require: vote_lost("g66")==0.
7. `T h2 | is_a | pet` (transfer, ec=2).
   Require: total=135, ov=66, ov2=0, vote_lost("h2")==1.
8. `T h1 | is_a | pet` (OVN dedup; must not touch any tier).
   Require: total=136, ov=66, ov2=0.
KILL: any deviation in ov/ov2/total at steps 5, 7, or 8. Step 8 is
the sharpest: a transferred subject re-dropped must be a pure no-op
on both tiers.

**X-FU8-3 (regression / lineage / determinism).**
1. Extract the mechanism region (lines 1..2304) of the COMMITTED
   `unified_fdcr8.zag` (result `11918217a`), cmp-verify the extraction,
   append the adversary main only. Rebuild with the frozen toolchain
   (`znc 2026.07.0-dev`), run 3x.
   Require: 3/3 byte-identical and md5 equal to the builder's
   `6ae1d1e5716e09d0a07beb3dee420d68`.
2. Reconfirm the FU7-vs-FU8 diff is purely additive and the 3192..4087
   region is free in FU7 (code-reading results above, re-verified at
   run time).
KILL: md5 mismatch, non-additive diff, or a memory-region collision.

**X-FU8-4 (the 128-entry lifetime boundary, empirical).**
Fixture (fresh W, fu7_pet40_world):
1. `fu8_teach_many(W,"f",1,64)`, `fu8_teach_many(W,"e",1,64)`.
   Require: total=128, ov=64, ov2=0 (ovl holds e1..e64).
2. Member e1..e64 into 8 concepts a1..a8 (8 members each; stays under
   the 8-member cap): for j in 1..8, for k in 1..8,
   `T e{(j-1)*8+k} | is_a | a{j}`.
   Require: total=128, ov=64, ov2=0 (membering clears OVN, touches no
   counter).
3. `fu8_teach_many(W,"g",1,64)`.
   Require: total=192, ov=128, ov2=0 (ovl now holds 128 entries: FULL).
4. `T g1 | is_a | a9` (clears g1 from OVN).
   `T h1 | is_a | pet` (new subject; ovl_add is a no-op: list full).
   Require: total=193, ov=129, ov2=0, vote_lost("h1")==1.
5. `T h1 | is_a | a9` (members h1; clears OVN).
   `T h1 | is_a | pet` (extends a9 to 2 features; no drop).
   Require: total=193, ov=129, ov2=0.
   `T s1 | is_a | a9` (extends pet; merge re-records g1 then h1: g1
   restores via ovl without recount; h1 was never tracked so the
   documented old behavior recounts).
   Require: total=195, ov=130, ov2=0, vote_lost("h1")==1,
   vote_lost("g1")==1.
KILL: ov recounts BEFORE the boundary is reached (ov != 128 after
step 3, or ov jumps by more than 1 on any single teach), ov2 != 0 at
any point, or final ov != 130. If the boundary holds at exactly 128
as documented, X-FU8-4 PASSES; the residual is confirmed documented,
not silent-but-undisclosed.
Disclosure check (non-kill): grep the implementation for any emit on
the ovl-full / evl-full paths. The RESULT.md claims the bounds "fail
loudly by construction". Code reading shows no emit on either full
path. If confirmed at run time, this is a disclosure-precision defect
("documented but silent", not "loud") to flag for correction; it does
not change the verdict because the prereg documents the boundary.

## Verdict rule

Any KILL trigger fires -> H-FDCR-UNIFIED8 is KILLED (the repair claims
to close the findings, so a counter failure is a kill, not a
downgrade). Any DOWNGRADE trigger fires without a kill ->
DOWNGRADED. All attacks pass -> SURVIVES the red team.

## Governance

- Prereg committed ALONE before any harness build or run.
- Pure Zag throughout: fixtures, harness, builds, runs, greps, md5,
  cmp, diff. Zero Python at any stage.
- Harness = committed mechanism region (lines 1..2304 of
  `unified_fdcr8.zag` at `11918217a`, cmp-verified) + new adversary
  main. No mechanism byte altered.
- Only owned paths staged/committed (pathspec-restricted).
- No binaries committed (builds in /tmp/fu8adv only).
- No em dashes in loop documentation (byte-verified).
