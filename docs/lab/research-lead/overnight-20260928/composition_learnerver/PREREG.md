# PREREG: Learner-Owned Verification for Composition (H-COMPVER-1)

## Identity
- Worker: Learner-Verification Composition Worker (H-COMPVER-1, P0, subagent, 2026-10-02)
- Mission: Replace expected-answer supervision with learner-owned verification in composition.
- Prereg frozen: commit of this file ALONE precedes any implementation commit.
- Unfrozen variant. Frozen sources read only, copied never edited. Pure Zag. Paper untouched.
- Nothing pushed to GitHub. Zero em/en dashes in this document.

## Background
- The composition-compare battery (C208) found T5 FAILED for all three mechanisms:
  all use researcher-supplied expected answers for verification and DFS termination.
  The unified mechanism (C224, composition_unified) inherits this.
- C181 (learner_verification) proved learner reliability can replace researcher
  `expected` for revision acceptance, with honest withholding when evidence is absent.
- H-COMPVER-1: use C181-style learner verification as the composition verifier
  instead of expected answers.

## Design (frozen)

Base: lvcomp_base.zag = composition_C/cc_base.zag + composition_unified/un_patch.zag
(byte-identical to the first 2097 lines of composition_unified/un_full.zag,
verified with cmp before implementation; frozen sources are read, never edited).

Patch: lvcomp_patch.zag (new file, this worker):

1. Prediction machinery ported from C181 (learner_verification/lv_base.zag):
   PRED node recording (tag 31), lv_predict (FACT pred_score basis, then
   MAP-execute basis for the query relation; -999999 if no basis),
   lv_pred_resolve (+1/-1 on source structure), lv_observe (ev_observe with
   prediction resolution appended). Researcher scaffold, honestly labeled:
   PRED layout, +1/-1 rule, threshold value 3. Learner-owned: all score
   values, which predictors are trusted, whether verification succeeds.

2. lv_setup(W,s,r): learner prediction into hg(W,32), reliability into
   hg(W,36); returns prediction or -999999 if no basis. Adapted from C181.

3. lv_dfs(W,s,pred,oseg,ovals,ofids,olen): un_dfs with the expected-answer
   termination replaced by learner-prediction termination (stop when a
   candidate chain end value equals the learner prediction). No expected
   parameter anywhere in this function.

4. lv_verify_chain(W,full,s0,st): execute the assembled chain; accept iff
   output equals hg(W,32) (the learner prediction). Rejection on
   execute failure is genuine.

5. compose_lv(W,s,r,masked,st): the learner-verified composition operation.
   Takes NO expected parameter at all, so expected answers are provably
   unconsulted (grep audit: the token `expected` must not appear in
   lvcomp_patch.zag). Flow: lv_setup; WITHHOLD (-3) if no prediction basis
   or reliability below threshold, before any search; else lv_dfs, assemble
   segment chains, seq_link, lv_verify_chain; on accept promote MAP_Z with
   LINK14 provenance to each segment MAP and type-15 co-use edges between
   consecutive segments (same promotion block as unified compose_try).
   Returns ans (>=0), -2 (rejected/failed after search), -3 (withheld).

Driver: lvcomp_driver.zag (new file). World builders copied verbatim from
un_driver.zag (t1_train, t1_couse, cmp_gap, t1_zfacts, map/edge counters).
compose_lv and the control compose_try are called DIRECTLY, not through
ev_query: after the evidence phase the (101,70,107) FACT would be
activate-shortcut inside ev_query and bypass composition entirely. The
composition operation is the unit under test, so direct calls are the
honest harness. This is documented, not hidden.

Battery (frozen):
- T1-LV: T1 world (3-structure X+Y+W plen-2, rels 1/2/3; co-use episodes;
  gap; Z facts 101..107) + evidence phase: 5 cycles of
  { lv_predict(W,101,70); lv_observe(W,101,70,107); } building the learner
  FACT pred_score to 4. Then compose_lv(W,101,70). Expect PASS ans=107.
  The evidence phase models world experience (C181 V4 precedent); the
  verifier itself never sees a researcher target.
- T-NE (no evidence): T1 world, no evidence phase. compose_lv(W,101,70).
  Expect WITHHOLD (-3), tried=0, MAP count unchanged, no false positive.
  Tests C181 honest withholding in composition.
- T-WE (wrong expected, the critical test): T1 world + evidence phase.
  Treatment: compose_lv(W,101,70) takes no expected; expect PASS ans=107.
  Control: unified compose_try(W,101,70,999,...) with researcher-wrong
  expected=999; expect FAIL (-2, COMP-FAIL). Control sanity:
  compose_try(W,101,70,107,...); expect PASS 107. If the treatment succeeds
  where the wrong-expected control fails, verification is genuinely
  learner-owned. Each arm runs on a fresh workspace.

## Kill bars (frozen)
- K1: T1-LV PASS: ans=107; live MAP count +1 (MAP_Z); LINK14 edges out of
  MAP_Z = 3; new type-15 co-use edges >= 2.
- K2: T-NE returns -3; tried=0; MAP count unchanged; no MAP_Z; no
  hallucinated answer.
- K3: T-WE treatment PASS ans=107 AND control-wrong FAIL (-2) AND
  control-right PASS 107.
- K4: 3/3 runs byte-identical; SHA-256 recorded per run.
- K5: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases; the token
  `expected` appears nowhere in lvcomp_patch.zag (grep audit recorded).
- K6: cognition lines of lvcomp_patch.zag recorded.

Any bar missed: BUILD-FAIL, not COMPLETE.

## Verdict names
- All bars pass: COMPOSITION-LEARNERVER-COMPLETE (report wrong-expected
  test result explicitly).
- Any bar missed: BUILD-FAIL (report which bar).

## Method
- Build: cat lvcomp_base.zag lvcomp_patch.zag lvcomp_driver.zag > lvcomp_full.zag;
  compile with pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1.
- Toolchain guard: safebin PATH, no python3/python, verified in NAMECHECK
  Step 0 before any implementation.
- Commits: this PREREG.md ALONE first; then implementation + results with
  explicit pathspecs. Local only, never pushed.
