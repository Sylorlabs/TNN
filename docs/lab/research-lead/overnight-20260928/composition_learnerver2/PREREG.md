# PREREG: H-COMPVER-2 Learner-Verified Composition Extension

Frozen: 2026-10-02 ~08:00 PDT. Worker: H-COMPVER-2 (Learner-Verified
Composition Extension Worker). Branch: tnn-native-lab, local only.

## Question

H-COMPVER-1 (prereg 3e692a037) built compose_lv: learner-verified
composition with no researcher answer parameter, verification against
the learner's own prediction gated by earned reliability (threshold 3).
T1-LV PASS (107), T-NE withhold PASS, T-WE PASS (researcher error 999 no
longer fails). Honest caveats recorded: only the 3-structure world
tested; T2A/T2B/T3/T4 analogues and the ev_query hookup are future work;
compose_lv was called directly because the post-evidence FACT would
activate-shortcut through ev_query.

H-COMPVER-2 extends: (a) compose_lv to T2A (4-structure), T2B
(5-structure), T3 (cross-domain), T4 (partial applicability); (b) a
principled resolution of the ev_query hookup problem; (c) the
unreliable-evidence boundary (reliability 1-2): withhold or gamble?

## Mechanism (unfrozen variant only)

- Base: lv2_base.zag = byte-identical copy of
  composition_learnerver/lvcomp_base.zag (itself cc_base.zag +
  un_patch.zag, verified first-2097-lines identical to
  composition_unified/un_full.zag). Copied, never edited.
- lv2_patch.zag = verbatim copy of composition_learnerver/lvcomp_patch.zag
  (compose_lv, lv_dfs, lv_setup, lv_predict, lv_pred_resolve, lv_observe,
  lv_verify_chain; 320 lines) PLUS one addition: ev_cquery, the
  CONSTRUCT-goal query entry point.
- ev_cquery design (principled resolution, no flag): RETRIEVE and
  CONSTRUCT are distinct query goals served by distinct operations.
  ev_query keeps its frozen activate-first RETRIEVE pipeline untouched.
  ev_cquery(W,s,r,masked,st) is the CONSTRUCT-goal entry: derive the
  answer from learned MAP structures and verify it against the learner's
  own prediction; direct FACT recall is not an answer source under this
  contract (the evidence FACT serves only as prediction basis). It
  delegates to compose_lv. No flag parameter alters ev_query's behavior;
  the two operations have different documented contracts, as
  rebind_try/compose_try/mp_run already do inside the pipeline.
- Driver: lv2_driver.zag. World builders ported verbatim from
  composition_unified/un_driver.zag (T1/T2A/T2B/T3/T4 train, couse,
  zfacts, gap). Evidence helper: N predict/observe cycles via
  lv_predict/lv_observe for (101,70) with the true world outcome o
  (C181 V4 precedent). After N cycles the evidence FACT pred_score = N-1.

## Battery (8 tests, fresh workspace each)

1. T2A-LV: 4-structure world (X+Y+W+V), evidence 5 cycles o=109.
   compose_lv(W,101,70,0,st). Expect PASS: ans=109, live MAPs +1, LINK14
   out of MAP_Z = 4, type-15 co-use edges >= +3, tried >= 1.
2. T2B-LV: 5-structure world (X+Y+W+V+U), evidence 5 cycles o=111.
   Expect PASS: ans=111, live MAPs +1, LINK14 = 5, type-15 >= +4.
3. T3-LV: cross-domain (plen-3 chain X + single-hop Y), evidence 5
   cycles o=105. Expect PASS: ans=105, live MAPs +1, LINK14 = 2,
   type-15 >= +1.
4. T4-LV: partial applicability, evidence 5 cycles o=106 (reliability
   reaches 4, the gate passes). Expect ans = -2 (LV-COMP-FAIL), live
   MAPs unchanged, no MAP_Z promoted. Rationale: the DFS search space
   is identical to unified compose_try, which cannot reach 106 (atomic
   MAP assumption); learner verification must not hallucinate a partial
   composition. No false positive.
5. T-THR-LO: T1 world, 3 evidence cycles o=107, so reliability = 2 < 3.
   Expect -3 (LV-WITHHOLD unreliable), tried = 0, MAPs unchanged.
   Withholding is the honest consequence of the preregistered gate:
   sub-threshold evidence must not drive structural promotion.
6. T-THR-HI: T1 world, 4 evidence cycles o=107, so reliability = 3 >= 3.
   Expect PASS: ans = 107, live MAPs +1. Boundary exactness: the gate
   opens at exactly the threshold value.
7. T-HOOK: T1 world, 5-cycle evidence o=107, ev_cquery(W,101,70,0,st).
   Expect ans = 107, tried >= 1, live MAPs +1, LINK14 = 3. The
   CONSTRUCT-goal entry point composes through the query API;
   composition genuinely ran (tried >= 1, MAP_Z promoted), not FACT
   recall, which compose_lv never consults.
8. T-HOOK-NE: T1 world, no evidence, ev_cquery(W,101,70,0,st).
   Expect -3 withhold, tried = 0, MAPs unchanged. Entry-point parity
   with compose_lv.

(H1's T-NE and T-WE are not rerun; they stand from faf1b2547.)

## Kill bars

- K1: T2A-LV PASS per metrics in test 1.
- K2: T2B-LV PASS per metrics in test 2.
- K3: T3-LV PASS per metrics in test 3.
- K4: T4-LV ans = -2, MAPs unchanged, no promotion. Any ans >= 0 or any
  promotion = FAIL (false positive).
- K5: threshold boundary. T-THR-LO = -3 with tried = 0 and no promotion;
  T-THR-HI = PASS 107 with +1 MAP. If T-THR-LO gambles (ans >= 0 or
  tried > 0) = FAIL.
- K6: hookup. T-HOOK = 107 with tried >= 1 and promotion; T-HOOK-NE = -3
  with tried = 0. If T-HOOK answers without composing (tried = 0) =
  FAIL.
- K7: 3/3 byte-identical runs, SHA-256 recorded.
- K8: 0 modes, 0 bridges, 0 handlers, 0 semantic cases; the token
  `expected` occurs 0 times in lv2_patch.zag outside audit comments;
  compose_lv, lv_dfs, ev_cquery take no researcher-target parameter;
  ev_query untouched (frozen base, copied).
- K9: cognition lines recorded (patch line count).

## Verdict on completion

COMPOSITION-LEARNERVER2-COMPLETE iff K1 through K9 all pass.

## Constraints

Unfrozen variant only. Frozen sources read-only (copies). Pure Zag via
the pinned znc binary. Safebin toolchain guard active. Zero em/en dashes
in all documentation. Research paper untouched. Nothing pushed to GitHub.
Git add and git commit use EXPLICIT pathspecs only.
