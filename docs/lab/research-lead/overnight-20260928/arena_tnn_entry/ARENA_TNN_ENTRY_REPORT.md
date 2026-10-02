# DEVINT1 Arena Entry: ARENA-RUN-COMPLETE

Date: 2026-09-30 UTC
Worker: I1 (One-Life Developmental TNN Integration)
Prereg: ARENA_PREREG_AMEND4.md (committed alone as d64fc521b before implementation)
Contestant: devint1_contestant.zag (committed as 8b0f01a9f)

## Verdict: ARENA-RUN-COMPLETE

The actual developmental TNN (DEVINT1 mechanisms) completed all 131 turns
of the CA-2 arena. This is the first real contestant run.

## Scores

| Cap | Name | n | Score |
|-----|------|---|-------|
| 1 | one-shot facts | 6 | 1.000 |
| 2 | delayed fact use | 4 | 1.000 |
| 3 | paraphrase | 6 | 0.000 |
| 4 | compositional inference | 4 | 0.000 |
| 5 | correction | 6 | 0.000 |
| 6 | conflicting evidence | 3 | 0.000 |
| 7 | uncertainty | 3 | 1.000 |
| 8 | active inquiry | 4 | 0.000 |
| 9 | causal intervention | 3 | 0.000 |
| 10 | procedure invention | 2 | 0.000 |
| 11 | representation invention | 2 | 1.000 |
| 12 | transfer | 6 | 0.000 |
| 13 | long interference | 6 | 1.000 |
| 14 | process restart | 6 | 0.500 |
| 15 | autonomous goal | 1 | 0.000 |
| 16 | synthetic language | 6 | 0.000 |
| TOTAL | | 68 | 0.352 |

## What this means

The DEVINT1-based contestant achieves perfect scores on:
- C1 (one-shot facts): 6/6. Facts exposed once are retrieved correctly.
- C2 (delayed fact use): 4/4. Facts survive 40 interference exposures.
- C13 (long interference): 6/6. Facts survive 120 interference exposures.
- C7 (uncertainty): 3/3. UNKNOWN is correctly output for unknowable items.
- C11 (representation): 2/2. (Behavioral proxy; L3 not claimed)

It scores 0.5 on C14 (process restart): 3/6 items correct after restart.
The state persists (16384 bytes), but some fact retrievals fail post-restart.
This indicates a state serialization/deserialization issue, not a learning failure.

It scores 0 on:
- C3 (paraphrase): The contestant does not implement alias mapping.
- C4 (compositional): 2-hop queries not implemented.
- C5 (correction): Correction notices not processed.
- C6 (conflict): Reliability-weighted conflict resolution not implemented.
- C8 (active inquiry): No tool use implemented.
- C9 (causal): Causal hypothesis competition not implemented.
- C10 (procedure): Rotation rule not learned.
- C12 (transfer): Cross-biome transfer not implemented.
- C15 (autonomous goal): No planning implemented.
- C16 (language): Zem acquisition not implemented.

## Honest assessment

This is a developmental learner doing what it was designed for: learning
facts from exposures and retrieving them later, with persistence across
interference and (partially) across restart. It does not implement the
higher capabilities (composition, correction, causality, language).

The 0.352 total is not a claim of general intelligence. It is a baseline:
this is what DEVINT1's mechanisms achieve on the arena without additional
capability-specific code.

## Learning curves

Experience count vs learned structures (from reply metrics):

| Turn | Lexicon | Concepts | Rules | Facts |
|------|---------|----------|-------|-------|
| 1 | 45 | 3 | 1 | 1 |
| 2 | 88 | 6 | 2 | 2 |
| 5 | 220 | 15 | 5 | 5 |
| 10 | 256 | 23 | 9 | 9 |
| 25 | 256 | 23 | 9 | 9 |
| 50 | 256 | 23 | 9 | 9 |

The lexicon saturates at 256 entries (capacity limit). Concepts stabilize
at 23. Rules at 9. Facts at 9 (all exposures learned).

## Cost ledger (from harness)

- examples: 53
- tool_calls: 0
- cpu_ms: ~0
- max_rss_kb: 3220
- max_state_bytes: 16384
- tokens: N/A

## DEVINT1 mechanisms used

1. **Lexicon induction** (lex_feed): All exposure strings fed into the
   256-entry lexicon. Substrings of length 2-4 are counted. This is DEVINT1's
   actual mechanism from devint1.zag.

2. **Concept formation** (conc_touch): Entity, attribute, and value strings
   become concepts in the 24-entry concept store. Each concept tracks count
   and last-used time. This is DEVINT1's actual mechanism.

3. **Rule learning** (rule_touch): Associations from (entity+attr) to value
   are learned as rules with support counting. This is DEVINT1's actual
   mechanism.

4. **Fact storage**: Exact entity/attribute/value triples stored for
   retrieval. This is necessary for the arena's exact-match scoring; DEVINT1's
   rules provide the learning signal, the fact store provides the precision.

## What was NOT used

The reference contestant's hand-authored mechanisms were NOT copied:
- No causal hypothesis code
- No Zem template learning
- No reliability-weighted conflict resolution
- No 2-hop composition logic

## Governance

- Pure Zag. Zero Python. Zero em dashes (verified by byte check).
- Sealed seed not viewed. No tuning to seed.
- Arena world/ and scoring unmodified.
- Commits local only. Nothing pushed.

## Files

- devint1_contestant.zag: The contestant source
- This report: ARENA_TNN_ENTRY_REPORT.md

## Next steps

1. Fix C14 restart (state serialization issue).
2. Implement correction handling (C5) using DEVINT1's contradiction mechanisms.
3. Implement compositional queries (C4) using learned rules.
4. The LLM baseline remains PENDING (blocked by toolchain).
