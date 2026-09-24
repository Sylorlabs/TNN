# MORG SCORES

Fixtures (sha256): corpus.txt=908d7ca2d853, corpus_holdout.txt=dd4a0ed71873, queries.txt=5f94658caea4, queries_holdout.txt=4636d34f9c6c

Test queries: 32 (PURE 16, SUBJ 8, AMBIG 8). Holdout queries: 12.

## B1 retrieval macro F1 (test queries, top-20)

| arm | PURE | SUBJ | AMBIG | overall |
|---|---|---|---|---|
| SELF | 0.6104 | 1.0000 | 0.5125 | 0.6833 |
| IMPOSED | 0.8333 | 0.6667 | 0.1250 | 0.6146 |
| FLAT | 0.4750 | 0.6667 | 0.8313 | 0.6120 |

## B2 interference (test PURE queries, top-10)

| arm | type-pure: frac wrong type | domain-pure: frac wrong domain | n |
|---|---|---|---|
| SELF | 0.0000 | 0.4250 | 8/8 |
| IMPOSED | 0.0000 | 0.0000 | 8/8 |
| FLAT | 0.1375 | 0.4875 | 8/8 |

## B7 holdout F1 (astronomy queries, top-20)

| arm | PURE | SUBJ | AMBIG | overall |
|---|---|---|---|---|
| SELF | 0.6917 | 0.9167 | 0.6667 | 0.7583 |
| IMPOSED | 0.9167 | 0.3333 | 0.3333 | 0.5278 |
| FLAT | 0.5250 | 0.3333 | 0.6667 | 0.5083 |

## B6 drift (scheme t0 vs t1; holdout F1 under old vs new scheme)

| arm | scheme t0 | scheme t1 | changed | F1 old | F1 new | delta | outcome |
|---|---|---|---|---|---|---|---|
| SELF | {coding:S1, cooking:S3, gardening:S3, history:S6, music:S6, physics:S6} | {astronomy:S6, coding:S1, cooking:S3, gardening:S3, history:S6, music:S6, physics:S6} | y | 0.0000 | 0.7583 | +0.7583 | helped |
| IMPOSED | MISSING | MISSING | n/a | 0.0000 | 0.5278 | +0.5278 | helped |
| FLAT | MISSING | MISSING | n/a | 0.0000 | 0.5083 | +0.5083 | helped |

## B3/B4/B5 evidence (from verify_report.txt)

| arm | B3 revision locality | B4 separability | B5 reorg cost |
|---|---|---|---|
| SELF | PASS | PASS | PASS |
| IMPOSED | PASS | PASS | PASS |
| FLAT | PASS | PASS | PASS |

ops.txt [SELF]:
```
reads=480
writes=240
moves=240
```

ops.txt [IMPOSED]:
```
reads=0
writes=480
moves=0
```

ops.txt [FLAT]:
```
reads=0
writes=480
moves=0
```

## Kill bars

- KB-1 non-inferiority: SELF 0.6833 >= IMPOSED 0.6146 - 0.02 -> PASS
- KB-5 deltas SELF-IMPOSED: PURE -0.2229, SUBJ +0.3333, AMBIG +0.3875, overall +0.0688
- KB-5: SELF wins>=0.03: ['SUBJ', 'AMBIG']; loses>=0.03: ['PURE'] (REPORTED, not a kill)
- KB-2 separability (ALL arms B4 PASS): PASS
- KB-3 revision locality (ALL arms B3 zero collateral): PASS
- KB-4 consciousness (scorer re-derives SELF argmax under frozen tie-break): PASS
  - coding: recorded=S1 re-derived=S1 scores=S1:1.0000 S2:1.0000 S3:0.8333 S4:1.0000 S5:1.0000 S6:0.8333 -> MATCH
  -   rationale: coding: S1 wins argmax on calib mean F1 (n=2); ties S1,S2,S4,S5 at 1.000000000000; frozen tie-break fewest-levels-then-lowest-index
  - cooking: recorded=S3 re-derived=S3 scores=S1:1.0000 S2:1.0000 S3:1.0000 S4:1.0000 S5:1.0000 S6:0.6667 -> MATCH
  -   rationale: cooking: S3 wins argmax on calib mean F1 (n=1); ties S1,S2,S3,S4,S5 at 1.000000000000; frozen tie-break fewest-levels-then-lowest-index
  - gardening: recorded=S3 re-derived=S3 scores=S1:1.0000 S2:1.0000 S3:1.0000 S4:1.0000 S5:1.0000 S6:0.6667 -> MATCH
  -   rationale: gardening: S3 wins argmax on calib mean F1 (n=1); ties S1,S2,S3,S4,S5 at 1.000000000000; frozen tie-break fewest-levels-then-lowest-index
  - history: recorded=S6 re-derived=S6 scores=S1:1.0000 S2:1.0000 S3:1.0000 S4:1.0000 S5:1.0000 S6:1.0000 -> MATCH
  -   rationale: history: S6 wins argmax on calib mean F1 (n=1); ties S1,S2,S3,S4,S5,S6 at 1.000000000000; frozen tie-break fewest-levels-then-lowest-index
  - music: recorded=S6 re-derived=S6 scores=S1:1.0000 S2:1.0000 S3:1.0000 S4:1.0000 S5:1.0000 S6:1.0000 -> MATCH
  -   rationale: music: S6 wins argmax on calib mean F1 (n=1); ties S1,S2,S3,S4,S5,S6 at 1.000000000000; frozen tie-break fewest-levels-then-lowest-index
  - physics: recorded=S6 re-derived=S6 scores=S1:1.0000 S2:1.0000 S3:1.0000 S4:1.0000 S5:1.0000 S6:1.0000 -> MATCH
  -   rationale: physics: S6 wins argmax on calib mean F1 (n=2); ties S1,S2,S3,S4,S5,S6 at 1.000000000000; frozen tie-break fewest-levels-then-lowest-index

## Cross-arm deltas

- SELF - IMPOSED overall: +0.0688
- SELF - FLAT overall: +0.0714
- IMPOSED - FLAT overall: +0.0026

## SELF per-domain scheme choices

- coding: S1
- cooking: S3
- gardening: S3
- history: S6
- music: S6
- physics: S6

## Failure-mode pointers (sol's list, checked against evidence; pointers, not verdicts)

- self-reinforcing misorganization: see B6 drift outcome + SELF scheme rationale above.
- popularity bias: see B2 interference (wrong-type/wrong-domain leakage into top-10).
- misleading cross-domain links: see B1 AMBIG vs PURE F1 gap per arm.

