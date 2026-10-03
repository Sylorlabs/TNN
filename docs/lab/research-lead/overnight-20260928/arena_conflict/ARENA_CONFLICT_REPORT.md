# Arena Conflict Handling (C6): ARENA-CONFLICT

Date: 2026-09-30 UTC
Worker: Arena Conflict Worker
Prereg: PREREG_ARENA_CONFLICT.md (5a4245a22, committed before implementation)
Parent: Arena Compositional (ARENA-COMPOSITION, 0.632, 0f6f1790d)

## Verdict: ARENA-CONFLICT (BUILD-PASS, 7/7 kill bars)

## Diagnosis confirmed

C6 (0.000) was a missing capability, not a bug. The arena teaches 3
conflicts as `{"t":"x","e":...,"a":...,"v1":...,"s1":"archive",
"v2":...,"s2":"scout"}` exposure events. The contestant v3 ignored
them (fell through to tick). The C6 test items use
`conflict|<entity>|<attr>` format requiring both values. No handler
existed. Additionally, the fact_store has update semantics, so a
separate pair-retaining store was required.

## Changes

1. **Conflict store** (W offset 11072, 32 x 64B): stores
   (entity, attr, value1, value2) quadruples with pair-update
   semantics. Uses free space 11072..13120.

2. **learn_conflict(W,e,a,v1,v2)**: mirrors learn_fact. Feeds
   "e a v1 v2" through lex_feed (DEVINT1 lexicon), conc_touch for
   each part (DEVINT1 concepts), rule_touch for (e+a)->v1
   association (DEVINT1 rules), then conf_store for exact pair
   retrieval.

3. **Expo handler**: `t:"x"` events now call learn_conflict.

4. **Test handler**: `conflict|entity|attr` performs generic pair
   lookup and answers `v1|v2` (pipe-separated, matching scorer
   expectation). No hardcoded entities, attrs, or values.

## Scores

| Cap | Name | n | Before | After |
|-----|------|---|--------|-------|
| 1 | one-shot facts | 6 | 1.000 | 1.000 |
| 2 | delayed fact use | 4 | 1.000 | 1.000 |
| 3 | paraphrase | 6 | 1.000 | 1.000 |
| 4 | compositional | 4 | 1.000 | 1.000 |
| 5 | correction | 6 | 1.000 | 1.000 |
| 6 | conflict | 3 | 0.000 | **1.000** |
| 7 | uncertainty | 3 | 1.000 | 1.000 |
| 8 | active inquiry | 4 | 0.000 | 0.000 |
| 9 | causal | 3 | 0.000 | 0.000 |
| 10 | procedure | 2 | 0.000 | 0.000 |
| 11 | representation | 2 | 1.000 | 1.000 |
| 12 | transfer | 6 | 0.000 | 0.000 |
| 13 | long interference | 6 | 1.000 | 1.000 |
| 14 | restart | 6 | 1.000 | 1.000 |
| 15 | autonomous goal | 1 | 0.000 | 0.000 |
| 16 | language | 6 | 0.000 | 0.000 |
| TOTAL | | 68 | 0.632 | **0.676** |

Total: 46/68 = 0.676 (was 43/68 = 0.632). Gain: +3 items (C6).

## Kill bar verification

- K1 (C6>0): PASS (1.000, 3/3)
- K2 (total>0.632): PASS (0.676, exactly as predicted: 43+3=46)
- K3 (no regression): PASS (C1,C2,C3,C4,C5,C7,C11,C13,C14 all 1.000)
- K4 (pure Zag): PASS (zero Python files, zero em-dash bytes)
- K5 (arena unmodified, seed not viewed): PASS
- K6 (determinism): PASS (3/3 runs: identical scores; cognitive
  outputs byte-identical excluding ms/rss_kb timing fields)
- K7 (generality): PASS (zero occurrences of test entity/attr/value
  names in implementation; conf_n=3 after exposures)

## Learning curves

conf_n grows 0->3 during conflict exposures, then stable. lex_n,
conc_n, rule_n, fact_n, rel_n continue from v3 baseline.

## Costs

- examples: 53, tool_calls: 0, cpu_ms: ~0
- max_rss_kb: 3268, max_state_bytes: 16384
- tokens: N/A

## Honest scope

This adds genuine conflicting-evidence tracking: both values are
retained (not overwritten), and the answer reports the conflict
explicitly as `v1|v2`. It is bounded: the mechanism stores the pair
as taught; it does not resolve which source is correct, weigh source
reliability, or perform belief revision. Still 0 on inquiry, causal,
procedure, transfer, goal, language.

## Files

- devint1_contestant_v4.zag: Contestant with conflict handling
- PREREG_ARENA_CONFLICT.md: Prereg amendment (5a4245a22)
- This report: ARENA_CONFLICT_REPORT.md
