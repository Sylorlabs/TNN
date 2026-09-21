# Q2-SWE faithfulness inventory

Source model: swe-1-6-slow:free (frozen corpus, seed unsupported).
corpus.json sha256: 45e53784dc914fab4addbac11990719df3bde6e13ae515f8a057725cfef1e9c6

All comparisons are mechanical against the frozen prompt set and the
frozen Zharovia domain spec. No retries were made for wrong values.

## §7 E_dump (240/240)
items deviating from the planted claim: 0/240

## §7 E_obs (240/240)
items where the LLM's observed value != world observation: 12/240
deviating ids: [3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231]

## §7 E_prb (240/240)
items where the LLM's probe value != world observation: 12/240
deviating ids: [3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231]

## inconsistencies (dump vs obs vs probe)
ids where dump/obs/probe are not all equal: 0/240
Note: for false ids the planted claim differs from the world value
by design, so dump != obs == probe is the EXPECTED pattern there.

## sentence-value checks
text/value mismatches: 0

## per-ID table: the 12 false ids

claim_in = planted claim shown in the dump prompt (the distractor,
INTENTIONAL deviation from world truth); truth = world observation;
obs/distract/probe = values asserted by the model in the teach item.
A teach deviation is UNINTENDED iff it differs from the intended
witness pattern (obs == truth, probe == truth, distract == claim_in).

| id | claim_in | truth | obs | distract | probe | intended | unintended |
|---:|---:|---:|---:|---:|---:|---|---|
| 3 | 1 | 0 | 1 | 2 | 1 | NO | obs,probe,distract |
| 29 | 3 | 2 | 3 | 2 | 3 | NO | obs,probe,distract |
| 55 | 5 | 4 | 5 | 4 | 5 | NO | obs,probe,distract |
| 71 | 5 | 4 | 5 | 6 | 5 | NO | obs,probe,distract |
| 80 | 1896 | 1895 | 1896 | 1897 | 1896 | NO | obs,probe,distract |
| 103 | 1849 | 1848 | 1849 | 1850 | 1849 | NO | obs,probe,distract |
| 117 | 1820 | 1819 | 1820 | 1806 | 1820 | NO | obs,probe,distract |
| 139 | 1706 | 1705 | 1706 | 1707 | 1706 | NO | obs,probe,distract |
| 163 | 21 | 20 | 21 | 22 | 21 | NO | obs,probe,distract |
| 178 | 12 | 11 | 12 | 11 | 12 | NO | obs,probe,distract |
| 205 | 10 | 9 | 10 | 11 | 10 | NO | obs,probe,distract |
| 231 | 20 | 19 | 20 | 19 | 20 | NO | obs,probe,distract |

Range check: every asserted numeric value lies within the fact's
  OUT OF RANGE: id 8 field distract_value value 12
  OUT OF RANGE: id 20 field distract_value value 12
  OUT OF RANGE: id 32 field distract_value value 12
  OUT OF RANGE: id 44 field distract_value value 12
  OUT OF RANGE: id 70 field distract_value value 8
  OUT OF RANGE: id 108 field distract_value value 1695
  OUT OF RANGE: id 154 field distract_value value 1699
  OUT OF RANGE: id 166 field distract_value value 48
  OUT OF RANGE: id 182 field distract_value value 48
out-of-range assertions: 9
