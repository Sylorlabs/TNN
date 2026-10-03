# MORG result-file format contract (for crew 2)

Fixtures live in `docs/lab/memory_org/`. Result files go in
`results/<arm>/run<R>/` as defined by the frozen prereg. The scorer
(`scorer.py`) parses the formats below; keep to them exactly.

## retrieval.txt / retrieval_holdout.txt

One line per query: `qid|id1,id2,...` — ranked ids, top-20 (fewer OK if the
store holds fewer). Ids must come from the ingested corpus (base corpus for
`retrieval.txt`; base+holdout for `retrieval_holdout.txt`).

## scheme.txt (SELF only)

Chosen scheme + all six candidate scores + one-line rationale. Global form:

```
chosen: S2
S1: 0.8123
S2: 0.8451
S3: 0.7900
S4: 0.8451
S5: 0.8102
S6: 0.8330
rationale: S2 wins argmax on calib mean F1; S4 ties but has more levels
```

Per-domain form (B8: choose runs per domain) — repeat the block under
`domain:` headers:

```
domain: physics
chosen: S2
S1: 0.8100
...
rationale: ...
domain: cooking
chosen: S3
...
```

The scorer re-derives the choice as argmax mean F1 with the frozen tie-break
(fewer levels, then lowest scheme index; levels S1=3 S2=3 S3=2 S4=3 S5=3 S6=1)
and KB-4 requires an exact match. Scores are the mean F1 on the 16
calibration queries (Q01..Q08, Q25..Q28, Q37..Q40).

## scheme_t0.txt / scheme_t1.txt (SELF only)

Same format as scheme.txt. t0 = scheme chosen on the base corpus;
t1 = scheme chosen after ingesting corpus_holdout.txt.

## retrieval_holdout_old.txt (SELF only)

Holdout queries retrieved under the t0 scheme (before re-choose).
`retrieval_holdout.txt` is the same queries under the t1 scheme.

## verify_report.txt (all arms)

One PASS/FAIL line per battery item, e.g.:

```
B3: PASS - revised 10 items, all other items byte-identical
B4: PASS - deletecat CODE hash matches fresh ingest; FACT export/import round-trips
B5: PASS - choose+refile ops: reads=4820 writes=240 moves=240
```

The scorer extracts the PASS/FAIL token per B-item. KB-2 needs B4 PASS on all
arms; KB-3 needs B3 PASS on all arms.

## ops.txt (all arms; SELF required)

Op counts since reset, e.g.:

```
reads=4820
writes=240
moves=240
```
