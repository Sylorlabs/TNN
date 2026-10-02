# SWE-ENGLISH error inventory (source faithfulness)

Source model: swe-1-6-slow:free ONLY (frozen corpus english-championship-v1).
Claim reference: the trainer-SUPPLIED values from the frozen `facts.json`
(228 true + 12 deliberately false; the model's job was to state the given
value and never correct from prior knowledge). Batches are never retried
because values are wrong — wrong values are the experiment.

## Mechanical inventory (vs supplied claims)

| check | n | ids |
|---|---|---|
| E_dump | 0 | — |
| E_obs | 0 | — |
| E_prb | 0 | — |
| inconsistent | 0 | — |
| sentence_missing_value | 0 | — |
| obs_missing_value | 0 | — |
| distractor_eq_obs | 0 | — |

## The 12 false ids: transcription direction per channel

FOOLED = model reports the SUPPLIED (false) value (faithful transcription,
world-wrong). CORRECTED = model reports the TRUE value despite the no-correction
instruction (prior-knowledge override; world-right, transcription-unfaithful).
OTHER = neither supplied nor true.

| id | supplied (false) | true | dump | obs | probe |
|---:|---:|---:|:---|:---|:---|
| 3 | 5 | 4 | FOOLED | FOOLED | FOOLED |
| 29 | 6 | 4 | FOOLED | FOOLED | FOOLED |
| 55 | 7 | 8 | FOOLED | FOOLED | FOOLED |
| 71 | 21 | 20 | FOOLED | FOOLED | FOOLED |
| 80 | 8 | 9 | FOOLED | FOOLED | FOOLED |
| 103 | 1688 | 1678 | FOOLED | FOOLED | FOOLED |
| 117 | 1851 | 1850 | FOOLED | FOOLED | FOOLED |
| 139 | 1896 | 1895 | FOOLED | FOOLED | FOOLED |
| 163 | 4 | 3 | FOOLED | FOOLED | FOOLED |
| 178 | 10 | 9 | FOOLED | FOOLED | FOOLED |
| 205 | 38 | 37 | FOOLED | FOOLED | FOOLED |
| 231 | 7 | 8 | FOOLED | FOOLED | FOOLED |

Direction totals over 36 false-id channel outputs: FOOLED=36, CORRECTED=0, OTHER=0.

## Integer/text agreement (mechanical categories)

For alpha-pos (`value == ord(letter)-ord('A')+1`) and word-len (`value == len(word)`),
does the model's own integer agree with its own claim text?

| id | category | claim | model value | text-derived |
|---|---|---|---|---|
| 3 | alpha-pos | D | 5 | 4 |
| 29 | alpha-pos | D | 6 | 4 |
| 55 | word-len | saturday | 7 | 8 |
| 71 | word-len | incontrovertibleness | 21 | 20 |
| 80 | word-len | knowledge | 8 | 9 |

