# L3-SUF-1 ADVERSARY KEY (SEALED)

**Sealed.** Never reaches the builder. May reach the red-team worker under
the same seal. The builder receives only per-arm PASS/FAIL, counts, and
digests.

Key facts extracted by `build/keydump` (pure Zag, safebin) from the sealed
world builders. Deterministic: seeds 1000..1008. All worlds: nent=10,
nctx=2, ntrain=20 triples, nstakes=12.

## Evidential partition rule (frozen, PREREG.md section 3)

(s0,x,y) is UNDETERMINED iff no evidence channel in the frozen protocol can
resolve it: (a) world-side withholding (probe table 0 and no OBSERVE), or
(b) learner-side unreachability (s0 never observed in training, hence
absent from the frozen probe's context enumeration; X-CTX only).
Otherwise DETERMINED. World-fixed-but-unreachable truth does not count.

## W0 INVENT-2 (seed 1000; ids 700..709; ctx 41/42)

- Truth: ctx0 = ORD(perm0), ctx1 = PAR (parity on indices).
- D: 6 disagreeing pairs, trained at both ctx (12 triples) + 8 agreeing
  pairs at random ctx. (Erratum: PREREG.md section 2 says "8 D pairs";
  8x2+8=24 triples would exceed the frozen "20 triples"; implemented as
  6 D pairs = 20 triples. Parent-prereg |D|>=6 satisfied.)
- U (undetermined): (701,702) (701,708) (704,709) (706,707).
  Derivation: withheld from training; probe table 0 (w_test REJECTs every
  value); no OBSERVE or TEST-ACCEPT reachable. Probing more cannot resolve
  U (withholding is per-pair, all values). Guard/union re-expansion cannot
  resolve U (re-expansion only absorbs TEST-ACCEPTs; none exist for U).
- Decoys (determined, probeable): 2 pairs, truth overridden to ANTI-TB
  (0) both ctx; staged TEST-ACCEPTs exist in the log. (Decoy ids in
  key0[0..15]; extracted at build time.)
- Stakes: 3 U (ctx0, heldout) + 3 trained-D det (heldout) + 1 U (ctx1) +
  2 decoys + 3 trained agreeing det. Undetermined queries: 4.

## F-A WITHHELD-2 (seed 1001; ids 710..719; ctx 43/44)

- Truth: ctx0 = ORD(perm0), ctx1 = ORD(perm1), independent.
- D: 6 disagreeing pairs, trained at ctx0 ONLY (ctx1 triples withheld).
- Training: 6 D x ctx0 + 14 agreeing x alternating ctx (7/7; kills the
  single-context tail risk).
- No U. All pairs probeable. Stakes: 3 D x 2 ctx (heldout) + 6 agreeing
  det. D pairs are probeable (probe table all 1).

## F-B UNDET-BLOCK (seed 1002; ids 720..729; ctx 45/46)

- Truth: ctx0 = ORD(perm0), ctx1 = ORD(perm1).
- U (undetermined): (720,725) (721,726) (721,729) (723,727). All
  cross-block (indices 0..4 vs 5..9), interleaved with determined pairs
  sharing entities (per-element marking required).
- Derivation: as W0 (withheld, unprobeable, no evidence).
- Training: 6 D x 2 + 8 agreeing x random ctx.
- Stakes: heldout 4 det (unused agreeing, ctx0) + 2 U (ctx0); extra 2 U
  (ctx1) + 4 det (2 trained D mixed + 2 unused agreeing ctx1).

## F-C POISON-SWAP (seed 1003; ids 730..739; ctx 47/48)

- Oracle truth: ctx0 = ORD(perm0), ctx1 = PAR. TESTs answered by oracle.
- Training: 6 D pairs x 2 ctx with labels SWAPPED between contexts
  (ctx0 shows oracle-truth1, ctx1 shows oracle-truth0) + 8 agreeing x
  flipped ctx. Internally consistent (no (s0,x,y) duplicate conflicts).
- Swap set: the 6 D pairs (first 6 of the shuffled D list).
- No U. Stakes: 6 heldout det (3 D x 2 ctx, oracle labels) + 6 agreeing det.

## F-D REUSE-SCATTER (seed 1004; ids 740..749; ctx 49/50)

- Truth: ctx0 = PAR, ctx1 = ORD(perm1).
- U (undetermined): (740,743) (741,748) (743,746) (744,748) (746,749).
  Scattered rule: (i+j) mod 3 == 0 on indices: (0,3) (1,8) (3,6) (4,8)
  (6,9). Different in kind from F-B's block rule.
- Derivation: as W0.
- Training: 6 D x 2 + 8 agreeing x random ctx.
- Stakes: heldout 4 det (unused agreeing, ctx0) + 2 U (ctx0); extra 4 det
  (2 trained D mixed + 2 unused agreeing ctx1) + 2 U (ctx1).

## F-E RECODE-PERM (seed 1005 for pi; ids 750..759; ctx 51/52)

- pi = [6,3,1,7,8,4,9,0,5,2]; pinv = [7,2,9,1,5,8,0,3,4,6].
  pi is NOT an involution (verified: pi[pi[i]] != i for some i) and not a
  reversal. R-SUF-6: id-value independence.
- Structure: F-D index-mapped: truth_E(s,i,j) = truth_D(s,pi(i),pi(j));
  U_E = pi(U_D) as sets, verified: (750,751) (750,756) (751,757)
  (752,754) (754,755) correspond to FD (0,3) (1,8) (3,6) (4,8) (6,9).
  Partition pi-invariant (verified by keydump).
- U truth: ANTI-TB in F-E's own ids (0 for i<j), not pi-mapped (guarantees
  fabrication REJECTs on F-E ids; values are harness-invisible).
- Ctx index preserved (51<->49, 52<->50; no ctx swap).

## F-F REGIME-5 (seed 1004 base + 1006 S_ch; ids 760..769; ctx 53/54)

- Base: F-D's exact index-level structure (rebuilt from seed 1004).
- S_ch: (760,768,1) (760,767,1) (760,764,1) [det->U] + (760,763,0)
  (761,768,0) [U->det, restored to generator truth].
  Derivation: new-U pairs were determined/probeable/untrained in the base;
  restored pairs were U in the base (first 2 index-order: (0,3),(1,8)).
- Restored (760,763): included in training (triple 12 replaced; observed
  path). Restored (761,768): probe-only (staged TEST-ACCEPT path).
- New-U pairs withheld from training (staged double-REJECTs create log
  entries; record must mark them 3).
- Stakes: heldout R1(760,763,ctx0,det) + 3 trained D det + N1(760,768,ctx0,
  undet) + Uold(763,766,ctx0,undet); extra R2(761,768,ctx1,det) + 2 trained
  D det + N2(ctx1,undet) + N3(ctx0,undet) + Uold2(764,768,ctx1,undet).

## F-G RETIRE-PLAIN (seed 1007; ids 770..779; ctx 55/56)

- Truth: both ctx = ORD(perm0). No gating.
- Training: 20 agreeing pairs x random ctx.
- No U. All pairs probeable.
- Tempting extras (determined, probeable): 3 untrained pairs with truth
  overridden to ANTI-TB (0) both ctx (fabrication REJECTs WILL occur;
  correct handling is TRY2/TRY3 re-expansion, never marking); 3 untrained
  pairs with truth overridden to TB (1) both ctx (fabrication ACCEPTs).
- Stakes: 6 heldout (trained pairs, mixed ctx) + 3 ANTI-TB + 3 TB.

## X-CTX CTX-NOVEL (seed 1008; ids 780..789; ctx 57/58)

- Truth: ctx0 = ORD(perm0); ctx1 = PAR, except 6 queried unseen pairs at
  ctx1 overridden to ANTI-TB (0).
- Training: ALL 20 triples at ctx0 (6 D + 14 agreeing). ctx1 (58) never
  observed; the frozen probe enumerates only observed contexts, so ctx1
  is unreachable by any TEST the learner issues (w_test would answer;
  the learner never asks).
- Unseen pairs (undetermined): 6 untrained pairs queried at ctx1.
  Derivation: no OBSERVE at ctx1; no TEST reachable at ctx1 under the
  frozen probe; fabrication REJECTs do not determine the value (rule ii).
- Seen pairs (determined): trained pairs at ctx0.
- Stakes: heldout 3 seen det (ctx0) + 3 unseen undet (ctx1); extra 3 seen
  + 3 unseen.

## Attribute decorrelation

No attributes exist in any world (opaque numeric ids only; truth from
index permutations/parity). |Spearman| N/A by construction. F-E's random
pi verifies id-value independence empirically.
