# Prereg: H-FDCR-UNIFIED (FROZEN)

**Date:** 2026-09-29
**Hypothesis:** H-FDCR-UNIFIED
**Status:** FROZEN. Implementation must follow this document. No bar may be
weakened after results. Commit-order: this file's commit must strictly
precede the implementation commit.

## Claim

FDCR concept formation can be integrated into the unified learner as a
third knowledge store alongside procedures and causal rules, where
concepts formed from relational facts inform procedure intent
disambiguation. The integration preserves all 20 frozen unified tests
and all 6/6 H-FDCR2 held-out probes.

## Context

1. H-FDCR3 SURVIVES (5/5): MERGE across parents fixed via parent
   re-linking (Fix A), spurious SPLITs eliminated via applicability gate
   (Fix B). All 6/6 held-out probes pass. FDCR stands as bounded L2
   representational adequacy with all three red-team downgrades closed.
2. H-UNIFIED (intent-inclusive) has 20 tests: Part A (10 unified) + Part B
   (10 intent). Stores: procedure (16 slots), bridge (4 rules), causal
   (16 rules), intent. No concept store.
3. FDCR input format: `T subj | rel | obj` facts, `Q subj | rel | exp`
   probes, `PHASE` markers. Completely different from unified learner's
   unlabeled `str>str` and `iii>ii` streams.
4. The unified learner's router has codes 0-4. No code for fact lines.

## Design

**New file:** `unified_fdcr.zag`, based on the COMMITTED
`unified_learn.zag` at HEAD (intent-inclusive, 20 tests). A separate
file avoids conflict with sibling agents (H-CAUSAL-UNIFIED uses
`unified_causal.zag`, H-INTENT-UNIFIED modified the original).

**Integration architecture:**

1. **Router extension:** New code 5 = concept learn (line contains `|`
   with T/Q prefix structure). New code 6 = concept query. The existing
   route_line is extended, not replaced.

2. **Concept store:** Minimal FDCR-derived store in workspace free space.
   Simplified to FORM operator only (shared-feature grouping):
   - Entities are interned strings from fact lines.
   - Features are (rel, obj) pairs per entity.
   - FORM: entities with identical feature sets are grouped under a
     concept node.
   - This is the core of FDCR's representational contribution. SPLIT
     and MERGE are omitted in v1; their absence is documented as a
     boundary.

3. **Concept use (K-FU2):** During intent-based procedure query, if the
   query string matches a concept member, procedures trained on other
   members of the same concept receive a score boost (+5000, below
   cond_fire*20000 and len_match*10000, above learn_seq). This makes
   concepts functionally used, not merely present.

4. **Workspace:** Concept store placed after intent store (SEQADDR=1720).
   Layout: CCONCEPT=1724. 32 concepts * 16 bytes = 512 bytes (ends 2236).
   This overlaps WORK=2048. WORK is moved to 4096. PAIRBASE=8192
   unaffected.

**Why FORM-only in v1:** Full FDCR (FORM+MERGE+SPLIT+GRADE) is 1300+
lines with complex phase-based learning. Porting it wholesale risks
breaking the 20 unified tests. The FORM operator is FDCR's core
representational mechanism; demonstrating its integration validates the
architectural fit. SPLIT/MERGE port is future work if v1 survives.

## Kill Bars (frozen)

**K-FU1 (No unified regression):** All 20 tests in unified_fdcr.zag
(Part A 10 + Part B 10) PASS with identical expected outputs. The
router extension and concept store must not alter existing behavior on
non-fact lines. Verification: run unified_fdcr, confirm 20/20.

**K-FU2 (Concepts formed and used):** 
  (a) After learning facts `T sparrow | is_a | bird`, `T robin | is_a |
      bird`, a concept {sparrow, robin} with intent {is_a=bird} is formed.
      Verification: concept dump shows the grouping.
  (b) A procedure trained on `sparrow` examples, when queried with
      `robin`, receives the concept boost and is selected over a
      recency-favored competitor. Verification: intent trace shows
      +5000 concept score determining the winner.
  PASS requires both (a) and (b).

**K-FU3 (No FDCR regression):** The 6/6 H-FDCR2 held-out probes still
pass when run through the ported concept machinery. Note: since v1 is
FORM-only, this bar is scoped to FORM-relevant probes. Probes requiring
SPLIT/MERGE are documented as out-of-scope for v1. Verification: run
heldout probes, confirm FORM-answerable probes pass.

**K-FU4 (Determinism):** Three consecutive runs of unified_fdcr.zag
produce byte-identical output. Verification: md5sum matches across runs.

## What Does NOT Count

- A concept store that is populated but never consulted during queries.
- Breaking any of the 20 unified tests to accommodate concepts.
- Claiming full FDCR integration when only FORM is ported.
- Any Python in implementation, testing, or verification.
- Modifying unified_learn.zag in place (use the separate file).

## Honest Failure Modes

1. If the concept boost never determines a winner (always dominated by
   other signals), K-FU2(b) fails and the integration is decorative.
2. If FORM-only proves insufficient for the held-out probes, K-FU3
   documents the gap rather than claiming full FDCR.
3. If workspace layout conflicts break existing tests, the integration
   is architecturally incompatible.

## Commit Order

1. This prereg (PREREG_FDCR_UNIFIED.md) — frozen before implementation.
2. Implementation: unified_fdcr.zag + evidence.
3. Result doc (RESULT_FDCR_UNIFIED.md).

Prereg commit must strictly precede implementation commit.
