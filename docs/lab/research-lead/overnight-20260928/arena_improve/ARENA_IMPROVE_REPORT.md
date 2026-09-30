# Arena Contestant Improvement: ARENA-IMPROVED

Date: 2026-09-30 UTC
Worker: Arena Contestant Improvement Worker
Prereg: PREREG_ARENA_IMPROVE.md (568cba875, committed alone before implementation)
Parent: I1 (ARENA-RUN-COMPLETE, 0.352, 8b0f01a9f)

## Verdict: ARENA-IMPROVED (BUILD-PASS, 8/8 kill bars)

## Diagnosis confirmed

C14 (0.500) was NOT a serialization bug. The 3 failing items were the
"corrected" facts. The contestant ignored correction events (`t:"k"`).
State persisted correctly. The gap was C5 (correction handling), not I/O.

## Changes (2 lines of logic)

1. **Correction handling:** In expo handler, `t:"k"` events now call
   `learn_fact(W,e,a,new)`. Uses DEVINT1's actual mechanisms
   (lex_feed, conc_touch, rule_touch, fact_store). `fact_store`
   already updates existing entity+attr entries.

2. **Paraphrase format:** In test handler, head `"fact2"` accepted as
   alias for `"fact"`. Same `fact_get` lookup. Format robustness,
   not new reasoning.

## Scores

| Cap | Name | n | Before | After |
|-----|------|---|--------|-------|
| 1 | one-shot facts | 6 | 1.000 | 1.000 |
| 2 | delayed fact use | 4 | 1.000 | 1.000 |
| 3 | paraphrase | 6 | 0.000 | 1.000 |
| 4 | compositional | 4 | 0.000 | 0.000 |
| 5 | correction | 6 | 0.000 | 1.000 |
| 6 | conflict | 3 | 0.000 | 0.000 |
| 7 | uncertainty | 3 | 1.000 | 1.000 |
| 8 | active inquiry | 4 | 0.000 | 0.000 |
| 9 | causal | 3 | 0.000 | 0.000 |
| 10 | procedure | 2 | 0.000 | 0.000 |
| 11 | representation | 2 | 1.000 | 1.000 |
| 12 | transfer | 6 | 0.000 | 0.000 |
| 13 | long interference | 6 | 1.000 | 1.000 |
| 14 | restart | 6 | 0.500 | 1.000 |
| 15 | autonomous goal | 1 | 0.000 | 0.000 |
| 16 | language | 6 | 0.000 | 0.000 |
| TOTAL | | 68 | 0.352 | 0.573 |

Total: 39/68 = 0.573 (was 24/68 = 0.352). Gain: +15 items.

## Kill bar verification

- K1 (C14=6/6): PASS (1.000)
- K2 (C5=6/6): PASS (1.000)
- K3 (C3=6/6): PASS (1.000)
- K4 (no regression): PASS (C1,C2,C7,C11,C13 all 1.000)
- K5 (total>0.352): PASS (0.573)
- K6 (pure Zag): PASS (zero Python, zero em dashes)
- K7 (arena unmodified): PASS (world_gen.zag, arena.zag untouched)
- K8 (seed not viewed): PASS

## Determinism

3/3 runs: scores identical (0.573). Cognitive outputs byte-identical
(md5 63a4c20c69a8126e3f21553e35ae6221 after stripping rss_kb/ms).
Only system RSS and timing vary (environmental, not cognitive).

## Costs

- examples: 53, tool_calls: 0, cpu_ms: ~0
- max_rss_kb: 3224, max_state_bytes: 16384
- tokens: N/A

## Honest scope

This is a bugfix + format robustness, not new cognition. The contestant
still scores 0 on composition, conflict, inquiry, causal, procedure,
transfer, goal, language. Those require new mechanisms.

The improvement from 0.352 to 0.573 comes from:
- Fixing an ignored event type (corrections)
- Accepting a question format variant (fact2)

Both use existing DEVINT1 mechanisms. No hand-authored capability-specific
code was added.

## Files

- devint1_contestant_v2.zag: Improved contestant
- PREREG_ARENA_IMPROVE.md: Prereg amendment
- This report: ARENA_IMPROVE_REPORT.md
