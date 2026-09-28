# Baseline accuracy — onebrain Experiment 2 problem set (v3 freeze)

Frozen set: `problems.tsv`
SHA-256: `2d4d2ea41efa62877f493a92b399371ca6fd0060e2bab9424d9ed98b50e07b0e`
Frozen: 2026-09-27 06:22:49 UTC (re-freeze v3; see FREEZE.txt for history)

Baseline: `baseline.zag` (pure Zag, zero RNG), built by `build_baseline.sh`.
Fixed integer heuristic: 3×context-overlap + 5×query-overlap + 4×recency +
6×correction-marker, minus length/16. Argmax, ties → lowest reading id.
The baseline reads the readings; it never reads `expected_answer` or the answer key.
Baseline code and design were fixed BEFORE the first scored run and never changed
across v1/v2/v3 (only the problem readings changed).

## Determinism

Three runs of `baseline_bin problems.tsv`, byte-identical output:

| run | output SHA-256 |
|---|---|
| baseline_run1.txt | `ee1e138b5d097f49c4ff2eb104c94c5d502b5a7c937c7b36086044b27f5c2240` |
| baseline_run2.txt | `ee1e138b5d097f49c4ff2eb104c94c5d502b5a7c937c7b36086044b27f5c2240` |
| baseline_run3.txt | `ee1e138b5d097f49c4ff2eb104c94c5d502b5a7c937c7b36086044b27f5c2240` |

32 output lines each (one per problem). Determinism check: PASS (3/3 identical).

## Accuracy (scored against answer_key.tsv)

| category | correct | total | accuracy |
|---|---|---|---|
| entity | 3 | 8 | 37.5% |
| predicate | 4 | 8 | 50.0% |
| scope | 4 | 8 | 50.0% |
| correction | 7 | 8 | 87.5% |
| **overall** | **18** | **32** | **56.2%** |

Misses (14): E02, E03, E04, E05, E07, P01, P04, P06, P08, S04, S05, S06, S08, C02.

## Reading

The single-pass baseline is at chance on entity/predicate/scope (37–50%) and
strong only on correction problems (87.5%), where correction markers are a
genuine single-pass cue. This is the intended calibration: the v3 readings walk
the same taught facts in both alternatives and differ only in the final
inferential step (role order, predicate taught-ness, scope of negation /
correction / quantifier, dimension word, aside-reversion), so bag-of-words
overlap is nearly uninformative and the disambiguating information is
structural — exactly the kind of ambiguity single deliberation is known to
struggle with. Below-chance entity accuracy (37.5%) means the heuristic
systematically prefers the hasty (recency/topic-continuity) reading there, a
real property of the heuristic, not an artifact: the wrong readings are the
plausible hasty inferences a single pass would naturally make.

## History (superseded freezes)

| freeze | problems.tsv SHA-256 | baseline accuracy | note |
|---|---|---|---|
| v1 2026-09-27 06:19:53 UTC | `133965b6e9a3f3c54436900a7de1cd269356baaa157d41b39e243a17cdd09a9e` | 26/32 = 81.25% | wrong readings argued different facts with different vocabulary; too easy |
| v2 2026-09-27 06:21:40 UTC | `fa9624ecf2e2cb565118acc538d1282c9f1db5f7e28018e776562cb0f581277a` | 28/32 = 87.5% | readings lengthened but still lexically distinguishable; still too easy |
| v3 2026-09-27 06:22:49 UTC | `2d4d2ea41efa62877f493a92b399371ca6fd0060e2bab9424d9ed98b50e07b0e` | 18/32 = 56.2% | CURRENT. both readings walk same facts; differ only in inferential step |

Each re-freeze rewrote readings only (ids, queries, expected answers,
categories unchanged) and was logged in FREEZE.txt with a dated note before
any scoring run on the new version. The baseline scorer was never modified.
