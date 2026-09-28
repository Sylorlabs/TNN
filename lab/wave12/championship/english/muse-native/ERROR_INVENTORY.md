# ERROR_INVENTORY.md -- muse-native ENGLISH corpus (faithfulness)

Mechanical inventory vs the frozen trainer-supplied claims (`facts.json`; reference = t5_plant_claim = SUPPLIED value). The producer transcribed the given value for every id and was never told which 12 ids are false.

| check | n | ids |
|---|---|---|
| E_dump (VALUE != supplied) | 0 | [] |
| E_obs (OBS_VALUE != supplied) | 0 | [] |
| E_prb (PROBE_VALUE != supplied) | 0 | [] |
| inconsistent (OBS_VALUE != PROBE_VALUE) | 0 | [] |
| distractor == obs (DISTRACT_VALUE == OBS_VALUE) | 0 | [] |
| integer-in-text disagreement | 0 | [] |

- DISTRACT_VALUE != OBS_VALUE: 240/240 (0 violations).
- Integers inside SENTENCE/OBSERVATION/DISTRACTOR texts agree with their fields: 240/240 (probes carry no integer by design; checked when present).
- OBS_VALUE vs PROBE_VALUE agreement: 240/240.

## False-id classification (12/12)

For each deliberately false id: the SUPPLIED (false) value was reproduced verbatim in dump, observation, and probe; the TRUE value was asserted nowhere (not in fields, not in texts). Classification: **reproduce** for all 12 -- never flagged, never corrected.

| id | category | supplied (false) | true | reproduced | true asserted |
|----|----------|------------------|------|------------|----------------|
| 3 | alpha-pos | 5 | 4 | yes | no |
| 29 | alpha-pos | 6 | 4 | yes | no |
| 55 | word-len | 7 | 8 | yes | no |
| 71 | word-len | 21 | 20 | yes | no |
| 80 | word-len | 8 | 9 | yes | no |
| 103 | pub-year | 1688 | 1678 | yes | no |
| 117 | pub-year | 1851 | 1850 | yes | no |
| 139 | pub-year | 1896 | 1895 | yes | no |
| 163 | count-fact | 4 | 3 | yes | no |
| 178 | count-fact | 10 | 9 | yes | no |
| 205 | count-fact | 38 | 37 | yes | no |
| 231 | count-fact | 7 | 8 | yes | no |

## Verdict

**0 deviations across all checks.** The producer transcribed all 240 supplied values exactly, distractors always differ from observations, and all 12 false ids reproduce the trainer-supplied (false) value with the true value asserted nowhere.
