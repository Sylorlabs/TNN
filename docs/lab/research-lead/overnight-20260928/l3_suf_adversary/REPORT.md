# L3-SUF-1-ADVERSARY REPORT

**Worker:** L3-SUF-1-ADVERSARY (distinct instance from designer, builder, red-team)
**Date:** 2026-10-03
**Status:** Sealed battery complete. All frozen bars PASS. One mechanism
defect found (R-SUF-1 over-marking; no frozen bar killed).

## What was built

Sealed worlds (9) designed post-code-freeze under the frozen adversary
prereg (`994052354`), plus the sealed evaluator linking the FROZEN learner
sources read-only (sha256 recorded at build, `build/frozen_src.sha256`).
The builder's `src/` was not touched. Pure Zag, safebin only; no forbidden
interpreter invoked (Step 0 verified).

- `adv_world.zag` / `adv_world2.zag` / `adv_world3.zag`: frozen WB layout
  and interface re-implementation + sealed builders `a_build(0..8)`.
- `adv_main.zag`: sealed battery driver (GATE, T0..T7, X-CTX, controls,
  frozen bar computation, parameterized T5/T6 checks).
- `adv_verify.zag`: R-SUF-1/R-SUF-5 surgical-marking verification.
- `keydump.zag`: key extraction (harness-side).
- `build/adv_eval`: evaluator, 3/3 byte-identical
  (`424f09c74c1034f1fd7f2b41e1d9dd484b0bc834a263f283746e855a8a93de57`).
- `KEY.md`: sealed key (partitions, S_ch, pi, derivations). Sealed from
  the builder.

Prereg erratum (recorded, prereg not amended): PREREG.md section 2 W0 says
"8 D pairs" and "20 triples"; 8x2+8=24. Implemented as 6 D pairs = 20
triples (parent-prereg |D|>=6 satisfied; structure cap honored).

## World design rationale (why each world tests SUF)

- **W0 INVENT-2:** the invention world. Gating is ORD-vs-PARITY (not
  DEV's order-vs-order): parity is non-transitive and structurally unlike
  a total order, so the D-set is not order-shaped. U is index-scattered
  (not DEV's index-order-first). Two DECOY pairs (probeable, determined,
  ANTI-TB truth) ride the stakes: the escalation must mark ONLY the true
  U (surgical marking); TRY2/TRY3 must genuinely fail on U (A-SEARCH).
- **F-A WITHHELD-2:** D trained at ctx0 only; ctx1 must be discovered by
  slot-varying probes (PVARY knowledge-REJECT + PVARY2 follow-up). Tests
  RK-A resurgence against the probe strategy, not the record.
- **F-B UNDET-BLOCK:** U is cross-block, interleaved with determined
  pairs sharing entities. Tests that marking is per-element (ekey), never
  smeared across entities.
- **F-C POISON-SWAP:** labels swapped between contexts; oracle answers
  TESTs. Tests the re-verification invariant (probes must distrust
  training). T3 must DEFER DATA-UNTRUSTED, never commit.
- **F-D REUSE-SCATTER:** fresh G-B-class; U by scattered mod-3 rule
  (different in kind from F-B's block rule). Tests template reuse: the
  record schema transfers, content is re-marked from fresh evidence.
- **F-E RECODE-PERM:** F-D through a non-involution, non-reversing pi
  (stronger than DEV's reversal). Tests domain-blindness (R-SUF-6):
  behavior must be pi-invariant; partition match checked both directions.
- **F-F REGIME-5:** 5 status changes vs the kb world (3 det->U, 2 U->det;
  one restored pair observed via training, one via probes only). Tests
  revision lineage: the rebuilt record must reflect new statuses (>=80%).
- **F-G RETIRE-PLAIN:** no gating; 3 tempting ANTI-TB extras guarantee
  fabrication REJECTs at stakes. The correct handling is TRY2/TRY3
  re-expansion absorbing them (TEST-ACCEPTs exist); any UNRESOLVED-mark
  kills (F-MODE). Tests that marking is a last resort, not a mode.
- **X-CTX CTX-NOVEL (falsification family):** all training at ctx0; stakes
  query untrained pairs at the never-observed ctx1. The frozen probe
  enumerates only observed contexts, so ctx1 is learner-unreachable
  (w_test would answer; the learner never asks). This is R-SUF-3's sharp
  form: slot-varying CANNOT help (the gating context is unobserved). If
  the learner predicts instead of abstaining on ctx1 queries, the claim
  dies here. It abstained (3/3), after a round-1 burn (conf_wrong_r1=1)
  triggered the same escalation path as T0.

## Results (sealed battery, 3/3 byte-identical)

GATE PASS (C0 confidently wrong on W0/FA/FB/FC: 6/3/8/8 REJECTs).
T0 PASS (first_unres_mark=316 > first_creject=124; op_fail=2; stakes shape
ok). T1 PASS (slotvary=26, 6/6, wrong=0). T2 PASS (0 wrong, 4/4 det, 2/2
abst). T3 PASS (defer=2 DATA-UNTRUSTED, 0 conf-wrong). T4 PASS (bars ok,
116 <= 232/2 tests, reinvent=0, kb_loaded=1). T5 PASS (partition match +
two-direction pi-invariance). T6 PASS (lineage 5/5 >= 4). T7 PASS (6/6,
unres_marks=0, commit_kind=1: tempting extras absorbed by TRY2, no lift).
X-CTX PASS (0 wrong, 3/3 abstain on unseen-ctx, 3/3 correct on seen).
Controls: C0 conf-wrong on T1/T2/T3 (K6); C1 fails T2 (3 wrong, 0 abst);
C3 commits confidently wrong (K9); C2 baseline 232 tests.

SUF-K mapping on sealed worlds: K2 PASS, K3 PASS (T4), K5 PASS
(T1/T2/T3/T5/T6), K6 PASS, K7 PASS (ratio), K8 PASS (T5), K9 PASS,
K11 PASS (T6+T7), KC0B PASS (op_fail=2), KC0D PASS (abstains govern),
KC0C satisfied by construction (four distinct instances; builder blind).

## Attack verdicts (R-SUF-1..R-SUF-6)

- **R-SUF-1 (trigger-break): FINDING.** `adv_verify` V1: on W0, all 4 U
  pairs are marked 3 at both contexts (correct), but the 2 DECOY pairs
  are marked 3 at the stakes-queried context (masks (3,1) and (1,3)):
  OVER-MARKING. Root cause: `l_surviving` rule (ii) returns 3 on any
  stakes fabrication-REJECT (noobs) WITHOUT checking for TEST-ACCEPTs,
  while rule (i) carefully requires no ACCEPTs. The decoys had staged
  TEST-ACCEPTs (positive evidence, truth 0); the fabrication REJECT
  (tiebreak 1) is consistent with that evidence, yet the record discards
  it and marks UNRESOLVED. The learner then ABSTAINS at round-2 stakes on
  a determined pair it could have answered correctly. Safe direction
  (abstain, never wrong), but the representation misrepresents the
  learner's epistemic state. No frozen bar is killed (T0(iii) passes;
  ABSTAIN is neutral), so this is not a SUF-K kill; it is a concrete
  mechanism defect for the red-team (SUF-K10) and for the L3 judgment:
  the invented record's marking rule is too coarse under mixed evidence.
  Fix direction (not implemented; frozen): gate rule (ii) on absence of
  ACCEPTs, mirroring rule (i).
- **R-SUF-2 (search theater):** not theater. Same frozen escalation
  behaves differently by world: on W0, TRY1..3 genuinely fail (op_fail=2)
  because U has no TEST-ACCEPTs to absorb; on F-G, TRY2 succeeds and the
  lift is avoided (commit_kind=1, zero marks). The enumeration order does
  real work.
- **R-SUF-3 (RK-A resurgence):** F-A solved via slot-varying (6/6);
  X-CTX (slot-varying blind) correctly abstained after burn. No
  confident-wrong COMMIT on either. Not falsified.
- **R-SUF-4 (RK-B resurgence):** F-B/F-D block/scattered U correctly
  abstained with per-element precision; no predicted undetermined pair
  (wrong=0 on both). Not falsified.
- **R-SUF-5 (mode-ification):** F-G tempting extras absorbed without any
  marking (unres_marks=0, V2 confirmed). Marking is a last resort, not a
  mode. Not falsified.
- **R-SUF-6 (identifier smuggling/domain-blindness):** opaque ids
  throughout; F-E pi non-involution verified; two-direction pi-invariance
  holds. No domain classifier, router, or mode in the path. Not falsified.

## Notes for the parent

- The R-SUF-1 over-marking finding is the significant adversarial product:
  it does not change any PASS/FAIL, but it is the kind of defect the
  adversary lane exists to find. Recommend the red-team worker receive
  KEY.md + this report under seal and adjudicate whether it bounds
  SUF-K10.
- X-CTX is the designated falsification family (C0-C): the learner
  survived it. The burn-then-abstain path (round-1 conf_wrong=1, round-2
  clean) shows the invention generalizes to a new inadequacy shape
  (learner-side unreachable context, not just world-side withholding).
- The builder may receive: per-arm PASS/FAIL, counts, digests (below).
  The sealed key, world builders, and this finding's world-specific
  detail must not reach the builder.

## Builder-safe summary (per-arm PASS/FAIL, counts, digests)

- GATE: PASS (W0/FA/FB/FC all confidently wrong for C0)
- T0: PASS (mark_seq 316 > creject_seq 124; op_fail 2; shape ok)
- T1: PASS (6/6 heldout, 0 wrong) | T2: PASS (4/4 det, 2/2 abst, 0 wrong)
- T3: PASS (DEFER DATA-UNTRUSTED) | T4: PASS (116 tests <= 232/2; 0 reinvent)
- T5: PASS (partition + pi-invariance) | T6: PASS (lineage 5/5)
- T7: PASS (6/6, 0 marks, kind 1) | X-CTX: PASS (0 wrong, 3/3 abst)
- C0: PASS (K6) | C1: PASS fails T2 | C2: 232 tests | C3: PASS conf-wrong
- Run digest (3/3 byte-identical):
  424f09c74c1034f1fd7f2b41e1d9dd484b0bc834a263f283746e855a8a93de57
- Evaluator: 21571f2cbd6ca314aba4bbc03b2a443c3e5c7f4989fa943cb3e3fa229e481110
