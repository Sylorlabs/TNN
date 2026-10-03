# PREREG: L3-SUF-1 Adversary (sealed worlds)

Status: PREREG-FROZEN 2026-10-03, before any adversary implementation exists.
This document is never edited after freezing. Any change requires a new
prereg. Commit-order self-check: the freeze commit contains ONLY PREREG.md
and NAMECHECK.md. No world source, no evaluator binary, no run log, no key
material exists under l3_suf_adversary/ at freeze time.

Worker: L3-SUF-1-ADVERSARY (subagent, 2026-10-03, distinct instance from
designer, builder, and red-team per prereg section 12). This worker designs
all sealed worlds post-code-freeze, holds the sealed key, and runs the
evaluator. The builder receives only per-arm PASS/FAIL, counts, and digests.

Parent prereg: l3_suf_intermediate/PREREG.md (frozen at 6c70c3198), sections
5 (battery arms), 7 (discrimination gate), 8 (adversary instructions), 12
(sequencing). This document instantiates sections 5 and 8. Where this
document is silent, the parent prereg governs.

## 1. Evaluator construction (frozen)

The builder's learner is code-frozen (commit c973e88d6; binary
src/build/suf). The adversary does NOT modify it.

- The evaluator binary is built in this lane from the FROZEN learner
  sources, referenced read-only by relative path:
  ../l3_suf_intermediate/src/{prelude,learner1,learner2,learner3,controls,driver}.zag
  plus this lane's adv_world.zag (sealed world builders) and adv_main.zag
  (sealed battery driver). The frozen world.zag and main.zag are NOT
  linked (replaced by the sealed counterparts).
- adv_world.zag re-implements the frozen WB buffer layout and the frozen
  interface functions (w_observe, w_test, w_stakes learner-visible;
  w_truth, w_stakes_meta, w_undet harness-only) exactly as documented in
  CODEFREEZE.md. Only the world builders a_build(0..8) are sealed content.
- Build-time guard: sha256 of each frozen source is recorded in the build
  log and re-verified before every evaluator run. Any mismatch is VOID
  (section 9).
- The learner process never calls w_truth, w_stakes_meta, or w_undet, and
  never reads the key buffers (A-INFO boundary preserved; adv_main is
  harness).

## 2. Sealed worlds (frozen specifications)

Common: nent=10, nctx=2, N_STAKE=12, training triples <= 20, B_PROBE=150
respected (probe-phase TEST upper bounds computed per world below, all <
150). Deterministic PRNG (LCG from frozen prelude), seeds fixed per world.
Entity/context identifiers are opaque numeric labels; no attributes exist
(Spearman decorrelation N/A by construction; F-E permutation verifies
id-value independence). Pairs are unordered; canonical index i<j.

Truth generators on indices (i,j), i<j:
- ORD(P): d=1 iff pos_P[i] < pos_P[j], P a permutation of 0..9.
- PAR: d=1 iff (i+j) mod 2 == 0.
- ANTI-TB(ids): d = 1 - ((id_x < id_y) ? 1 : 0), using entity IDS (matches
  the learner's documented l_tiebreak on ids; guarantees stakes REJECTs on
  tiebreak fabrications).

Index-to-id: world W uses entity ids base_W + i (i = index), context ids
c0_W / c1_W. l_ekey bounds respected (all ids < 1000).

Undetermined marking (world mechanism, harness-visible only): probe table
entry 0 (w_test REJECTs every value: no TEST sequence can resolve), undet
table entry 1, truth = ANTI-TB. The determined/undetermined partition used
for scoring is EVIDENTIAL (section 3).

### W0 "INVENT-2" (G0, invention world)
- ids: entities 700..709, ctx 41/42. seed 1000. perm0 = shuffle(seed).
- truth: ctx0 = ORD(perm0); ctx1 = PAR.
- D: 8 disagreeing pairs (truth0 != truth1), first 8 of shuffled D list.
- Training (20 triples): 8 D pairs x both ctx (16) + 8 agreeing pairs
  (truth0 == truth1) x random ctx (rng).
- U: 4 pairs from unused pairs, shuffled candidate order, first 4.
  Marked undetermined (probe 0, undet 1, ANTI-TB truth both ctx).
- Decoys: 2 pairs from remaining unused pairs, PROBEABLE, truth both ctx =
  ANTI-TB (determined; staged probes ACCEPT; record must mark them 1/2,
  never 3: surgical-marking test, R-SUF-1/R-SUF-2).
- Stakes (12): heldout 3 U (ctx0) + 3 det (trained D: 2 ctx0, 1 ctx1);
  extra 1 U (ctx1) + 2 decoys (ctx0, ctx1) + 3 det (trained agreeing,
  mixed ctx). Undetermined queries total: 4 (>= 3 required).
- Probe TEST upper bound: slot-varying <= 20; staged: 29 untrained pairs x
  2 ctx, <= 2 TESTs each: <= 116. Total < 150.
- Key exhibits: D list; U list with derivation (withheld from training;
  probe table 0; no OBSERVE or TEST-ACCEPT reachable; evidentially
  undetermined); decoy list (probeable; TEST-ACCEPTs reachable;
  determined); argument that probe-more cannot resolve U (w_test withholds)
  and guard/union re-expansion cannot resolve U (re-expansion only absorbs
  TEST-ACCEPTs; none exist for U).

### F-A "WITHHELD-2" (G-A, withheld-contradiction)
- ids: entities 710..719, ctx 43/44. seed 1001.
- truth: ctx0 = ORD(perm0); ctx1 = ORD(perm1); independent shuffles.
- D: 6 disagreeing pairs, trained at ctx0 ONLY (ctx1 triples withheld).
- Training (20): 6 D x ctx0 + 14 agreeing x random ctx.
- No U. All pairs probeable.
- Stakes (12): heldout 3 D pairs x 2 ctx (6); extra 6 agreeing det
  (mixed ctx).
- Key: D list; D probeability (probe table all 1).

### F-B "UNDET-BLOCK" (G-B, unprobeable-undetermined)
- ids: entities 720..729, ctx 45/46. seed 1002.
- truth: ctx0 = ORD(perm0); ctx1 = ORD(perm1).
- U: 4 pairs, cross-block (blocks A={0..4}, B={5..9} on indices):
  candidates = unused cross-block pairs, shuffled, first 4. Marked
  undetermined. (U interleaved with determined pairs sharing entities:
  per-element marking required, R-SUF-4.)
- Training (20): 6 D x 2 ctx + 8 agreeing x random ctx.
- Stakes (12): heldout 4 det (agreeing, unused, non-U, ctx0) + 2 U (ctx0);
  extra 2 U (ctx1) + 4 det (2 trained D mixed ctx + 2 agreeing unused ctx1).
- Key: U list + derivation; partition (det = observed or probeable with
  TEST-ACCEPT reachable; undet = U).

### F-C "POISON-SWAP" (G-C, poisoned reuse)
- ids: entities 730..739, ctx 47/48. seed 1003.
- Oracle truth: ctx0 = ORD(perm0); ctx1 = PAR. TESTs answered by oracle.
- Training (20): 6 D pairs x 2 ctx with labels SWAPPED between contexts
  (ctx0 shows oracle-truth1, ctx1 shows oracle-truth0) + 8 agreeing x
  flipped ctx (invisible for agreeing pairs; keeps training internally
  consistent: no two triples share (s0,x,y) with different d).
- No U. All pairs probeable.
- Stakes (12): 6 heldout det (3 D x 2 ctx, oracle labels) + 6 extra det
  (agreeing, mixed ctx). (T3 defers before stakes; stakes serve C3/GATE.)
- Key: swap set (the 6 D pairs); oracle truth tables.

### F-D "REUSE-SCATTER" (G-D, reuse)
- ids: entities 740..749, ctx 49/50. seed 1004.
- truth: ctx0 = PAR; ctx1 = ORD(perm1).
- U: 5 pairs: candidates = unused pairs with (i+j) mod 3 == 0, shuffled,
  first 5. Marked undetermined. (Scattered rule, different in kind from
  F-B's block rule: template-not-content reuse test.)
- Training (20): 6 D x 2 ctx + 8 agreeing x random ctx.
- Stakes (12): heldout 4 det (agreeing unused non-U ctx0) + 2 U (ctx0);
  extra 4 det (2 D trained mixed + 2 agreeing unused ctx1) + 2 U (ctx1).
- Key: U list + derivation; partition.

### F-E "RECODE-PERM" (G-E, recode)
- pi: fixed permutation of 0..9 from seed 1005 (Fisher-Yates on identity).
  Non-involution, non-reversing (stronger than reversal; R-SUF-6).
- ids: entities 750..759 (index i -> id 750+i); ctx 51/52, ctx index
  preserved (s_E <-> s_D, no ctx swap).
- Structure inherited from F-D by index mapping: truth_E(s,i,j) =
  truth_D(s,pi(i),pi(j)) for determined pairs; U_E = {(i,j) canonical:
  (pi(i),pi(j)) canonical in U_D}; training_E and stakes_E = index-mapped
  triples of F-D.
- U truth: ANTI-TB in F-E's OWN ids (not pi-mapped; guarantees fabrication
  REJECTs on F-E ids; partition pi-invariant, values harness-invisible).
- Key: pi, pi-inverse; verification that U_E = pi(U_D) as sets and the
  determined/undetermined partition is pi-invariant.

### F-F "REGIME-5" (G-F, regime change)
- Base: F-D's exact index-level structure (same perm1, PAR/ORD, D/U sets,
  training index triples), fresh ids: entities 760..769, ctx 53/54.
- S_ch (5 changes, |S_ch| >= 3 required): 3 determined index pairs
  (unused in training, probeable in base) -> U (unprobeable, undet 1,
  ANTI-TB truth in F-F ids); 2 of F-D's U index pairs -> restored
  (probeable, undet 0, truth = base generator truth).
- Of the 2 restored: 1 included in training (observed path), 1 probe-only
  (staged TEST-ACCEPT path).
- The 3 new-U pairs are withheld from training (staged double-REJECTs
  create their log entries; record must mark them 3).
- Stakes (12): heldout 4 det (post-change; incl. 1 restored pair) + 2
  undet (post-change; incl. 1 new-U pair); extra 3 det + 3 undet (mixed,
  incl. remaining changed pairs).
- Key: S_ch as (x_id, y_id, new_det) x5 in F-F ids; derivation.

### F-G "RETIRE-PLAIN" (G-G, retirement)
- ids: entities 770..779, ctx 55/56. seed 1007.
- truth: both ctx = ORD(perm0). No gating.
- Training (20): 20 agreeing pairs x random ctx.
- No U. All pairs probeable.
- Tempting extras (R-SUF-5): 3 untrained probed pairs with truth
  overridden to ANTI-TB(ids) both ctx (determined, probeable; fabrication
  REJECTs WILL occur; correct handling is TRY2/TRY3 re-expansion, never
  marking); 3 untrained probed pairs with truth overridden to
  tiebreak(ids) both ctx (fabrication ACCEPTs; must not disturb).
- Stakes (12): heldout 6 trained pairs (mixed ctx); extra 3 ANTI-TB +
  3 tiebreak-consistent (mixed ctx).
- Key: tempting-extras list; argument that re-expansion absorbs them
  (TEST-ACCEPTs exist in the log).

### X-CTX "CTX-NOVEL" (R-SUF-3 attack: context-novelty)
- ids: entities 780..789, ctx 57/58. seed 1008.
- truth: ctx0 = ORD(perm0); ctx1 = PAR, EXCEPT the 6 queried unseen pairs
  (listed in key) at ctx1 overridden to ANTI-TB(ids).
- Training (20): ALL at ctx0: 6 D pairs x ctx0 + 14 agreeing x ctx0.
  (ctx1 never observed; the frozen probe enumerates only observed
  contexts, so ctx1 is unreachable by any TEST the learner issues.
  w_test WOULD answer at ctx1; the learner never asks: learner-side blind
  spot, distinct from world-side withholding.)
- No U. Probe table all 1.
- Stakes (12): heldout 3 seen det (trained pairs, ctx0) + 3 unseen undet
  (UNTRAINED pairs at ctx1, ANTI-TB truth); extra 3 seen det (agreeing
  trained, ctx0) + 3 unseen undet (untrained pairs at ctx1, ANTI-TB).
- Key: unseen-ctx pairs undetermined (no training at ctx1; frozen probe
  cannot reach ctx1; fabrication REJECTs do not determine the value per
  l_surviving rule (ii)); seen pairs determined.
- Runs AFTER T7 with the continuing kb (template 2 expected).

## 3. Evidential partition rule (frozen)

The key marks (s0,x,y) UNDETERMINED iff no evidence channel in the frozen
protocol can resolve it: (a) world-side withholding (probe table 0, no
OBSERVE), or (b) learner-side unreachability (s0 never observed in
training, hence absent from the frozen probe's context enumeration;
X-CTX only). Otherwise DETERMINED. The partition is derived from the
training set plus the frozen probe's reachable TEST set, exhibited per
world in KEY.md. World-fixed-but-unreachable truth does not count as
determined: the bars test the learner's epistemics, not omniscience.

## 4. Kill bars for the sealed evaluation (frozen)

Computed by adv_main on the sealed battery. Notation follows the parent
prereg section 5.

- SEAL-GATE: C0 confidently wrong (AS[52]==1) on W0, F-A, F-B, F-C.
  REQUIRED. Gate failure on a family VOIDs that family (parent prereg
  section 7): the family is dropped, reported, never salvaged.
- SEAL-T0: parent T0 bars on W0: (i) first UNRESOLVED-mark SEQ >
  first committed-prediction REJECT SEQ; (ii) op_fail (AS[28]) >= 2
  (A-SEARCH: TRY1..3 genuinely tried and failed); (iii) final stakes:
  0 REJECTs on determined queries, 100% ABSTAIN on undetermined.
  Maps to SUF-K2, SUF-KC0B.
- SEAL-T1: parent T1 bars on F-A (slotvary >= 1; solve >= 5/6 heldout or
  earned DEFER; 0 confident-wrong). Maps to SUF-K5.
- SEAL-T2: parent T2 bars on F-B (0 wrong; >= ceil(5*D_det/6) correct on
  determined heldout; 100% ABSTAIN on undetermined heldout). Maps to
  SUF-K5, SUF-KC0D (ABSTAIN events govern predictions).
- SEAL-T3: parent T3 bars on F-C (>= 1 verification TEST; terminal DEFER
  cert DATA-UNTRUSTED; 0 confident-wrong COMMITs). Maps to SUF-K5.
- SEAL-T4: parent T4 bars on F-D (T2-style bars; TESTs <= C2 TESTs / 2;
  zero re-invention events AS[32]==0; kb-loaded trace AS[60]==1).
  Maps to SUF-K3, SUF-K7, SUF-KC0D.
- SEAL-T5: parent T5 bars on F-E (T2-style bars; zero re-invention;
  marked partition matches the key's under pi: every record entry mask==3
  iff w_undet==1; every T4 record entry has a pi-mapped T5 entry with equal
  mask). Maps to SUF-K5, SUF-K8.
- SEAL-T6: parent T6 bars on F-F (T2-style bars on post-change world;
  status lineage >= 80% on S_ch: 5 changes, >= 4 matches; new_det=1 ->
  mask==3; new_det=0 -> mask in {1,2}). Maps to SUF-K5, SUF-K11.
- SEAL-T7: parent T7 bars on F-G (>= 5/6 heldout; zero UNRESOLVED-mark
  events AS[44]==0 in the T7 segment; commit kind != 2). Maps to SUF-K11.
  (Commit kind 1 after TRY2 absorption is allowed: guarded form, not
  graded machinery.)
- SEAL-T8 (X-CTX): final sres: 0 wrong on all stakes; ABSTAIN on 100% of
  undetermined (unseen-ctx) queries; >= 5/6 correct on determined
  (seen-ctx) heldout. FAIL is recorded as an R-SUF-3 falsification finding
  against SUF-K5/SUF-K10.
- SEAL-C0: C0 confidently wrong on F-A, F-B, F-C (SUF-K6).
- SEAL-C1: C1 fails T2 bars on F-B (SUF-K9).
- SEAL-C2: baseline TEST count for the T4 ratio (F-D, wiped kb).
- SEAL-C3: C3 commits confidently wrong on F-C (committed==1 and
  conf_wrong==1) using the kb saved after T0 (SUF-K9).
- SEAL-KC0C: all worlds designed post-code-freeze by this adversary
  instance; designer/builder/adversary/red-team four distinct instances;
  builder blind (receives only per-arm PASS/FAIL, counts, digests); sealed
  key in KEY.md never leaves this lane except to the red-team worker under
  the same seal.

## 5. Attack families (frozen; at least one designed to falsify)

- R-SUF-1 (trigger-break): W0 decoys (marking must be surgical: decoy
  masks in {1,2}, verified against key; blanket marking fails SEAL-T5's
  partition check pattern) and F-G tempting extras (fabrication REJECTs
  must be absorbed by TRY2/TRY3 re-expansion; any UNRESOLVED-mark on F-G
  fails SEAL-T7). Analytical verdict recorded: under the evidential
  partition, spurious marking of a determined element is structurally
  unreachable (l_surviving yields 3 only via withholding rules (i)/(ii);
  knowledge-REJECTs are sound falsifications in a deterministic world).
- R-SUF-2 (search theater): W0 must show op_fail >= 2 (TRY1..3 genuinely
  fail) while F-G shows TRY2 succeeding and avoiding the lift: same frozen
  escalation, different worlds, different outcomes. Verdict recorded.
- R-SUF-3 (RK-A resurgence): F-A (withheld D at ctx1; slot-varying must
  catch it) and X-CTX (slot-varying CANNOT help: ctx1 unobserved;
  falsifies if the learner predicts instead of abstaining on unseen-ctx
  queries).
- R-SUF-4 (RK-B resurgence): F-B (block U interleaved with determined
  pairs sharing entities; per-element marking required) and F-D (scattered
  mod-3 U, different in kind). Any predicted undetermined pair fails
  SEAL-T2/SEAL-T4 via h_held_tally (predicted undet counts wrong).
- R-SUF-5 (mode-ification): F-G tempting extras; any marking on F-G fails
  SEAL-T7 (F-MODE).
- R-SUF-6 (identifier smuggling / domain-blindness): opaque ids
  throughout; F-E uses a non-involution, non-reversing permutation pi;
  the learner's id use is restricted to ekey components (auditable).
  No domain classifier, router, or mode exists anywhere in the path.

## 6. Determinism and budgets (frozen)

- Seeds: 1000..1008 per world (section 2). 3/3 byte-identical run logs
  required; sha256 digests over summary + trace + protocol log.
- Frozen budgets respected: B_CONSTRUCT=3000, B_PROBE=150, B_REVISE=2000,
  B_SURFACE=50, N_STAKE=12, seed base 11+world_index for the battery RNG
  (world-internal seeds 1000..1008 are world content, documented here).
  Structure cap 20 respected (training triples <= 20; forms within the
  DEV envelope).
- The evaluator asserts heldout count > 0 before scoring (the T3b 0/0 bug
  class stays dead); revision verdicts use capability + lineage, never
  retention ratios.

## 7. Discrimination gate detail (frozen)

C0 (frozen controls.zag c0_run) runs on W0, F-A, F-B, F-C. REQUIRED:
confidently wrong (AS[52]==1) on all four. Rationale per world: W0 via U
fabrication REJECTs; F-A via kind0 cross-context knowledge REJECTs; F-B
via U fabrication REJECTs; F-C via swapped-knowledge REJECTs. Gate failure
on a family VOIDs that family per parent prereg section 7.

## 8. Adversary key (sealed)

KEY.md (this lane) holds, per world: seed, id scheme, truth generators,
D list, U list with the evidential derivation, stakes composition,
S_ch (F-F), pi/pi-inverse (F-E), swap set (F-C), decoy list (W0),
tempting-extras list (F-G), unseen-query list (X-CTX). The key is sealed:
it never reaches the builder. The red-team worker may receive it under
the same seal.

## 9. VOID (terminal)

Any frozen learner source modified (sha256 mismatch against the build-time
record); any sealed content (world builders, key, traces beyond digests)
reaching the builder; any forbidden-interpreter invocation in this lane
(PROCESS-FAIL per the toolchain guard; results stay exploratory); any 3/3
divergence; any expected value reaching the learner process; gate failure
handled per section 7 (family VOID, never salvage).

## 10. Sequencing and commit-order self-check

1. This prereg frozen and committed (adversary worker). Freeze commit
   contains ONLY PREREG.md and NAMECHECK.md, added with explicit pathspecs.
   No .zag, no binary, no log, no key exists under l3_suf_adversary/ at
   freeze time.
2. The adversary implements adv_world.zag + adv_main.zag + build script
   under this frozen prereg (pure Zag, safebin), builds the evaluator,
   verifies determinism 3/3, runs the sealed battery.
3. The adversary writes KEY.md (sealed) and REPORT.md (world design
   rationale + per-arm PASS/FAIL + counts + digests).
4. The builder receives ONLY per-arm PASS/FAIL, counts, and digests.
