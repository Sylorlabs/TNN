# Arena Active Inquiry (C8): ARENA-INQUIRY

Date: 2026-09-30 UTC
Worker: Arena Inquiry Worker
Prereg: PREREG_ARENA_INQUIRY.md (304e43629, committed before implementation)
Parent: Arena Conflict (ARENA-CONFLICT, 0.676, 9211de19e)

## Verdict: ARENA-INQUIRY (BUILD-PASS, 7/7 kill bars)

## Diagnosis confirmed

C8 (0.000) was a missing capability, not a bug. Each C8 item runs a
3-turn sequence: ask `fact|<entity>|<attr>` (fact never exposed) ->
`observe_result` with the oracle fact -> re-ask. The scorer awards
1000 iff the re-ask reply equals the answer AND the first reply
contains an `"observe":[` request. The contestant v4 did neither:
unknown facts got "UNKNOWN" with no observe request, and the
observe_result handler just ticked without learning.

## Changes (v5, from v4)

1. **Observe request on knowledge gap** (test handler): when a
   `fact|`/`fact2|` lookup fails, the reply JSON carries
   `"observe":[{"e":"<entity>","a":"<attr>"}]`, echoing the
   question's own fields. General behavior, not gated on cap 8.

2. **Learn from observe_result**: parse e/a/v from the vals array
   (jval, same pattern as expo parsing) and call
   `learn_fact(W,e,a,v)` (DEVINT1 path: lexicon, concepts, rule,
   fact store). State persistence carries it to the re-ask.

## Scores

| Cap | Name | n | Before | After |
|-----|------|---|--------|-------|
| 1 | one-shot facts | 6 | 1.000 | 1.000 |
| 2 | delayed fact use | 4 | 1.000 | 1.000 |
| 3 | paraphrase | 6 | 1.000 | 1.000 |
| 4 | compositional | 4 | 1.000 | 1.000 |
| 5 | correction | 6 | 1.000 | 1.000 |
| 6 | conflict | 3 | 1.000 | 1.000 |
| 7 | uncertainty | 3 | 1.000 | 1.000 |
| 8 | active inquiry | 4 | 0.000 | **1.000** |
| 9 | causal | 3 | 0.000 | 0.000 |
| 10 | procedure | 2 | 0.000 | 0.000 |
| 11 | representation | 2 | 1.000 | 1.000 |
| 12 | transfer | 6 | 0.000 | 0.000 |
| 13 | long interference | 6 | 1.000 | 1.000 |
| 14 | restart | 6 | 1.000 | 1.000 |
| 15 | autonomous goal | 1 | 0.000 | 0.000 |
| 16 | language | 6 | 0.000 | 0.000 |
| TOTAL | | 68 | 0.676 | **0.735** |

Total: 50/68 = 0.735 (was 46/68 = 0.676). Gain: +4 items (C8).

## Kill bar verification

- K1 (C8>0): PASS (1.000, 4/4)
- K2 (total>0.676): PASS (0.735, exactly as predicted: 46+4=50)
- K3 (no regression): PASS (C1,C2,C3,C4,C5,C6,C7,C11,C13,C14 all 1.000)
- K4 (pure Zag): PASS (zero Python files, zero em-dash bytes;
  only znc, bash, grep used)
- K5 (arena unmodified, seed not viewed): PASS
- K6 (determinism): PASS (3/3 runs: 0.735 identical; cognitive
  outputs byte-identical excluding ms/rss_kb timing fields)
- K7 (generality): PASS (observe request echoes question fields
  only; no test entity/attr/value names in implementation)

## Evidence of the inquiry path (run 1)

Item 64: ask -> reply "UNKNOWN" + observe request for
(Tetaru, material); re-ask -> "wooden" (correct). Same pattern
for items 65-67. fact_n grows 9->13 as the 4 oracle facts are
learned via observe_result.

## Costs

- examples: 53, tool_calls: 7 (4 observe requests + 3 baseline),
  cpu_ms: ~0
- max_rss_kb: 3264, max_state_bytes: 16384
- tokens: N/A

## Honest scope

This adds genuine active inquiry in the arena's tested sense: the
learner detects a knowledge gap at query time, requests the
missing fact, learns it from the observation result, and answers
correctly on re-ask. It is bounded: the inquiry is a single
observe request for the queried fact; it does not plan multi-step
information gathering, prioritize among gaps, or decide when not
to ask. Still 0 on causal, procedure, transfer, goal, language.

## Files

- devint1_contestant_v5.zag: Contestant with inquiry handling
- PREREG_ARENA_INQUIRY.md: Prereg (304e43629)
- ARENA_INQUIRY_SCORES.txt: Scorer output (run 1)
- This report: ARENA_INQUIRY_REPORT.md
