# STEP championship English verdict (step-3.7-flash:free, real-English box)

Corpus sha256: `c52e4f52dc15713a5995ff7bc26b9b04298d79df881dca1a90052b76d2ea69ab`
Teacher-state digest (legB == legC): `be5dba8498fffd515f6b9a3b16068300a1d58b00d963338e2b9a0dfad7e9e05d` — MATCH

## Faithfulness (model text vs trainer-supplied claims, 240 ids)

| check | definition | count |
|---|---|---|
| E_dump |  | 1 |
| E_obs |  | 0 |
| E_prb |  | 0 |
| inconsistent |  | 0 |
| sentence_missing_value |  | 12 |

False ids (12): reproduced vs flagged/corrected — see `corpus/ERROR_INVENTORY.md` §2.

## Class 4 — Track 5 (D2 arm, 12 reps; weights 30/25/25/10/10)

| rep | mastery | revisab | integrity | retent | cost | composite |
|---|---|---|---|---|---|---|
| 0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | 0.9911 |
| 1 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | 0.9911 |
| 2 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | 0.9911 |
| 3 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | 0.9911 |
| 4 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | 0.9911 |
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | 0.9911 |
| 6 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | 0.9911 |
| 7 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | 0.9911 |
| 8 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | 0.9911 |
| 9 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | 0.9911 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | 0.9911 |
| 11 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | 0.9911 |
| mean | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | 0.9911 |

Toy comparison: toy step-3.7-flash Zharovia composite mean was 0.9911; English mean is 0.9911.

## Class 4 — §B.7 direct (flaw-only, tid=51; exact hits /12 per slice, bar ≥10/12)

| slice | hits | nears | misses | score_x10 | pass |
|---|---|---|---|---|---|
| 0 | 12 | 0 | 0 | 120 | PASS |
| 1 | 12 | 0 | 0 | 120 | PASS |
| 2 | 12 | 0 | 0 | 120 | PASS |
| 3 | 12 | 0 | 0 | 120 | PASS |
| 4 | 12 | 0 | 0 | 120 | PASS |
| 5 | 12 | 0 | 0 | 120 | PASS |
| 6 | 12 | 0 | 0 | 120 | PASS |
| 7 | 12 | 0 | 0 | 120 | PASS |

Total: 96/96 flaw hits; slices passing strict bar: 8/8. (RUN line: total_hits=96, total_pass=8, fails=0)

## Class 3 — teacher leg (tid=41; flaw-first then clean teaching)

§B.7 per slice (flaw exam administered by the teacher):

| slice | hits | nears | misses | pass |
|---|---|---|---|---|
| 0 | 12 | 0 | 0 | PASS |
| 1 | 12 | 0 | 0 | PASS |
| 2 | 12 | 0 | 0 | PASS |
| 3 | 12 | 0 | 0 | PASS |
| 4 | 12 | 0 | 0 | PASS |
| 5 | 12 | 0 | 0 | PASS |
| 6 | 12 | 0 | 0 | PASS |
| 7 | 12 | 0 | 0 | PASS |

Total: 96/96 flaw hits; slices passing strict bar: 8/8.

Teaching / mastery numbers:

| slice | clean adopts | mastery/24 |
|---|---|---|
| 0 | 20 | 24 |
| 1 | 20 | 24 |
| 2 | 20 | 24 |
| 3 | 20 | 24 |
| 4 | 20 | 24 |
| 5 | 20 | 24 |
| 6 | 20 | 24 |
| 7 | 20 | 24 |

Totals: clean adopted=160, final mastery=192/192, fails=0.

Toy comparison: toy class-3 teach3 composite was 0.9822; the English teacher leg
reaches final mastery 192/192 with 160 clean adoptions and 96/96 flaw hits.

## Verdict

- §B.7 batteries (legs B and C) are value-agnostic: they operate on proposal
  spans, grounding, and confidence only. They received NO content adaptation
  for the English port — identical machinery to the Zharovia run.
- Track-5 D2 battery: two-hop letter→position→wordlen chained lookup, the
  English structural analog of the Zharovia landmark→ruler→year chain.
- All legs ran N=5 byte-identical; pure Zag, zero RNG (static scan PASS).
- Corpus is a frozen artifact of step-3.7-flash:free at temperature 0, seed 42;
  claim reference is the trainer-supplied values in facts.json.
