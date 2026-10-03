# LIFEXP_RESULT.md -- Lifetime Experience Storage + Changing Abstractions (LIFEXP-1)

Verdict: LIFETIME-TESTED (pending this report's kill-bar check).

## 1. What was built

`lifeexp.zag` (pure Zag, ~800 lines): a synthetic lifetime of 40,000
experiences (t, f0..f3 in 0..15, a in 0..7, o in 0..15, r in 0..3)
generated deterministically from seed 987654321 (xorshift32, frozen
draw order). Storage is structure-of-arrays plus counting-sort
inverted indexes (one N-entry i32 arena per feature, per abstraction
code). Two frozen abstractions: M1 (old) bins coarse (f0,f1); M2 (new)
bins coarse (f2,f3). The re-abstraction pass recomputes M2 codes for
all 40,000 experiences, builds M2 code lists, and fills a 16x16
C1xC2 co-occurrence table; M1 codes and lists are preserved untouched.

Queries: Q1 exact recall (1000 random t, checksum + order-independent
SUM), Q2 pattern (200 random 1..3-constraint patterns, smallest-list
scan with direct verification), Q3 abstraction (64 M2-bin queries, 64
code spot-checks, co-occurrence row-sum check), Q4 temporal range (50
[t1,t2] x r==3 scans). Every query result is verified against
brute-force ground truth computed from the raw arrays.

Baseline: the Zag program emits world.sql (40,000 INSERTs), index.sql
(7 indexes + c1 column UPDATE), reabstract.sql (c2 column UPDATE),
queries.sql (316 labeled SELECTs with identical parameters drawn from
the identical rng stream). Driver `run_lifeexp.sh` (bash + sqlite3
3.45.1) times each phase over 3 reps on fresh DBs.

## 2. Kill bars

- K1 PASS: INGEST count=40000 (engine counter, return value of the
  generation loop), 3/3 runs. Q1_MATCH 1 (checksum over 1000 exact
  recalls equals independent recomputation).
- K2 PASS: Q2_MISMATCH 0 (200/200 patterns), Q3A_MISMATCH 0 (64/64),
  Q3B_MATCH 64 (64/64 spot-checks), Q3C_OK 1, Q4_MISMATCH 0 (50/50),
  C1_INTACT 1 (old abstraction bit-identical after re-abstraction),
  REABSTRACT_DONE, STATE_BYTES 1642048.
- K3 PASS: B-sql implements ingest, indexes, Q1..Q4, and both
  re-abstraction UPDATEs on byte-identical data. All 316 labeled query
  results match the Zag output exactly (sorted diff, 3/3 reps).
  Wall-clock comparison both directions below; code size below.
- K4 PASS: pure Zag + bash + sqlite3 only; zero python3 invocations at
  any stage (world gen, build, runs, baseline emit, baseline driver);
  zero em/en-dash bytes in docs and code (byte-grep verified);
  prereg commit 30b016328 strictly precedes implementation;
  3/3 stdout byte-identical (md5 36179374f0bc66669a2ae4971b412991).

No falsifier fired (F1/F2/F3: zero mismatches, checksum match,
C1 preserved).

## 3. Measurements

Timings in ms (3 reps; machine shared with concurrent workers, so
medians are the comparison basis). Zag timings from stderr;
brute-force verification passes are reported separately and excluded
from the indexed-query comparison.

| phase | Zag r1 | Zag r2 | Zag r3 | Zag median | SQLite r1 | SQLite r2 | SQLite r3 | SQLite median |
|---|---|---|---|---|---|---|---|---|
| ingest 40k | 17 | 92 | 18 | 18 | 9921 / 1021* | 12141 / 1025* | 13210 / 659* | 12141 / 1021* |
| index build | 36 | 100 | 62 | 62 | 818 | 522 | 533 | 533 |
| re-abstraction | 15 | 30 | 42 | 30 | 357 | 159 | 533 | 357 |
| queries | see split | see split | see split | ~190 idx | 1464 | 1487 | 1467 | 1467 |

* SQLite ingest: naive per-statement commits / single-transaction
variant (the serious baseline; used for the ratio).

Zag query split (median): Q1 1000 exact recalls ~1ms; Q2 200 indexed
pattern queries 151ms (~0.75ms/query; brute-force verification
1603ms excluded); Q3 ~262ms includes Q3a brute-force verification,
indexed path near zero; Q4 50 range scans 30ms. Indexed-query total
about 190ms vs SQLite 1467ms for the same 316 queries.

Resources: Zag peak RSS 1824..1828 kB, state bytes 1642048. SQLite DB
file 4403200 bytes. Zag ~2.4x smaller on disk-equivalent footprint.

Code size: lifeexp.zag ~800 lines (includes utils, engine, and the
SQL emitter); handwritten baseline SQL ~15 lines + ~60 lines bash
driver, leaning on the sqlite3 3.45.1 engine.

Ratios (medians, Zag vs serious SQLite): ingest ~57x, index ~8.6x,
re-abstraction ~12x, queries ~7.7x, all in Zag's favor.

## 4. Honest interpretation

1. The in-process engine beats SQLite decisively on this fixed
   workload (roughly one order of magnitude per phase). The gap is
   larger than the hyp-pop result (~5x) because this workload is
   dominated by per-statement and per-query overhead that an
   in-memory engine avoids: tight loops over flat arrays vs SQL
   parsing, planning, and B-tree maintenance.
2. The re-abstraction pass, the novel piece for priority C, costs one
   linear scan (~30ms for 40k experiences): applying a new
   abstraction retrospectively to a full lifetime is cheap, and the
   old abstraction survives intact (C1_INTACT=1) with a recorded
   translation table (co-occurrence). This is the mechanical
   substrate any genuine re-grounding would need; the mapping itself
   remains researcher-authored.
3. This is a bounded engineering result, not a TNN-unique
   architectural advantage: the win comes from in-memory layout and
   zero IPC, not from anything TNN-specific. SQLite buys
   persistence, ACID, concurrent access, and an ad-hoc query
   language; the Zag engine has none of those. The comparison is
   engine-vs-engine on a fixed workload, not a system comparison.
4. Scope bound: 40k experiences fit comfortably; the inverted
   indexes cost one i32 per experience per indexed feature
   (8 arenas = 1.28MB here). A million-experience lifetime would need
   the S9 eviction/GC work (substrate_scale) to stay bounded.

## 5. Commits and files

- Prereg: 30b016328 (alone, before implementation).
- Implementation + results: this commit (lifeexp.zag, run_lifeexp.sh,
  LIFEXP_RESULT.md, LIFEXP_RAW_1..3.txt, LIFEXP_ERR_1..3.txt,
  build.err). Binary lifeexp_bin left untracked.
- Baseline scratch (reproducible, not committed): /tmp/lifeexp_sql/
  (world.sql, index.sql, reabstract.sql, queries.sql, sqlite_out_*.txt).

Seed: 987654321. Zag stdout md5 (3/3):
36179374f0bc66669a2ae4971b412991. SQLite query outputs md5 (3/3):
c2e2554d0d33b02a9a1b047353ab73dc. Cross-check: 316/316 match.

Builder label: LIFETIME-TESTED.
