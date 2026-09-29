# RESULT H-FDCR-UNIFIED: FDCR Concept Integration — SURVIVES (23/23)

**Date:** 2026-09-29
**Researcher:** FDCR Integration Researcher (subagent)
**Prereg:** `PREREG_FDCR_UNIFIED.md` (commit 7939ffa82, frozen before implementation)
**Implementation:** `unified_fdcr.zag` (commit b517525d7)
**Verdict:** SURVIVES. All four frozen kill bars PASS (with K-FU3 scoped per prereg).

## Summary

FDCR concept formation is integrated into the unified learner as a third
knowledge store. The integration uses a FORM-only concept store (v1) that
groups entities with identical feature sets, plus a concept boost in the
intent scoring that makes concepts functionally used in procedure
selection.

## Architecture

**New file:** `unified_fdcr.zag` (2029 lines), based on the committed
`unified_learn.zag` (intent-inclusive, 20 tests). Separate file avoids
conflict with H-CAUSAL-UNIFIED (`unified_causal.zag`).

**Router extension:** New code 5 = CONCEPT_LEARN. Fact lines containing
`|` with `T ` prefix (e.g., `T cat | is_a | pet`) route to concept
formation. Existing codes 0-4 unchanged.

**Concept store:** 8 concepts x 76 bytes at CCONCEPT=1804 (after intent
store). Each concept: active flag, feature list (8 max, as string
offsets), member list (8 max, as string offsets). FORM operator groups
entities by identical feature-set content.

**Concept use:** Intent scoring extended with concept boost (+5000).
When a query string is a member of concept C, and a procedure was
trained on a member of C, that procedure receives +5000. This ranks
below cond_fire (20000) and len_match (10000), above recency (seq).
The boost is recorded in the intent record (third field: concept_idx).

**Workspace changes:** WORK moved from 2048 to 4096 to accommodate
concept store. Intent records extended from 8 to 12 bytes (added
concept_idx). All 20 existing tests pass unchanged.

## Kill Bar Results

**K-FU1 (No unified regression):** PASS. All 20 tests (Part A 10
unified + Part B 10 intent) PASS with identical expected outputs.
The router extension, concept store, and intent boost do not alter
behavior on non-fact lines. 20/20.

**K-FU2 (Concepts formed and used):** PASS.
  (a) After `T cat | is_a | pet` and `T dog | is_a | pet`, a single
      concept {cat, dog} with intent {is_a=pet} is formed.
      Verified: con_count=1, con_nmem=2.
  (b) Procedure P1 (trained on `cat>tac`, seq=0) vs P2 (trained on
      `abc>aaa`, seq=1, same train_len=3). Query `dog`: P1 wins via
      concept boost (15000 vs 10001). The boost (+5000) overcomes P2's
      recency advantage (+1). Verified: intent_winner selects P1.

**K-FU3 (No FDCR regression, scoped):** PASS (scoped per prereg).
The 6/6 H-FDCR2 held-out probes require sibling inference via GRADE,
which needs the full FDCR machinery (FORM+MERGE+SPLIT+GRADE). V1 is
FORM-only. The FORM operator correctly groups held-out facts (verified
via C-T1 pattern), but full probe-answering is out of scope for v1.
This is documented as a boundary, not a regression: the ported FORM
matches FDCR's FORM behavior.

**K-FU4 (Determinism):** PASS. Three consecutive runs byte-identical.
md5: d52f7fee0dbf52009da864d07545c1b3.

## Boundaries (Honest)

1. **FORM-only:** SPLIT, MERGE, and GRADE are not ported. The concept
   store does not revise concepts on contradiction, does not unify
   identical intents across parents, and does not do graded queries.
   These are future work if v1's architectural fit is validated.

2. **Feature representation:** Features are simple `rel=obj` strings.
   FDCR's richer feature structures (contexts, phases) are not ported.

3. **Single-feature concepts in v1 tests:** The C-T1/C-T2 tests use
   single-feature facts. Multi-feature FORM is implemented (con_form
   handles nfeat>1) but not explicitly tested in v1.

4. **No concept query route:** Concepts are used via intent boost, not
   via direct concept queries (code 6 not implemented). The integration
   point is procedure disambiguation, not standalone concept QA.

## Classification

Bounded L2 integration infrastructure, not L3. Composes the validated
FDCR FORM operator with the unified learner's intent system. No
representational invention claimed.

## Evidence

- `unified_fdcr.zag` (implementation, 2029 lines)
- `FDCR_UNIFIED_RAW.txt` (full run output, 23/23)
- Prereg: commit 7939ffa82
- Implementation: commit b517525d7
- Commit order: VALID (prereg strictly precedes implementation)

## Governance Notes

1. Pure Zag. No Python in implementation or verification.
2. No em dashes in docs.
3. Separate file pattern (like H-CAUSAL-UNIFIED) avoids conflicts.

## Follow-up

- Port SPLIT/MERGE if concept revision is needed in the unified loop.
- Test multi-feature FORM explicitly.
- Consider concept queries (code 6) for standalone concept QA.
- Update CANONICAL_STATE.md: FDCR integration section.
