# PREREG_LIFETIME_EXP.md -- Lifetime Experience Storage + Changing Abstractions (LIFEXP-1)

Frozen: 2026-09-30. Committed alone before any implementation, world
generation, or measurement. Any implementation commit must strictly follow
this commit.

## 1. Claim under test

Directive priority C (machine-native): exact lifetime experience plus
changing abstractions. Can TNN store its complete experiential history
efficiently and retrieve from it under exact recall, pattern matching,
and a CHANGED abstraction (re-grounded vocabulary applied
retrospectively to all past experience)?

This is a MACHINE-NATIVE claim (storage/retrieval efficiency), NOT an
L3 representational-invention claim. The experience SCHEMA, the two
abstraction mappings, and the index structures are researcher-designed.
What is tested is: exact storage of a full lifetime, retrieval
correctness and cost, the cost/correctness of re-grounding the entire
history under a new abstraction, and honest comparison against a
conventional baseline (SQLite) doing the same logical work.

## 2. Synthetic lifetime (deterministic from sealed seed)

Generated entirely inside the Zag program from a fixed seed constant
(sealed at implementation; recorded in the result report). LCG with
frozen multiplier/increment.

- N = 40,000 experiences. Experience e: t = e (0..N-1, also the id),
  obs features f0..f3 each in 0..15, action a in 0..7, outcome o in
  0..15, reward r in 0..3.
- Generative process: f_i(t) = hash-mix of (seed, t, i) mod 16;
  a(t) = mix mod 8; o(t) = (f0 + 2*f1 + a) mod 16 (a fixed causal
  regularity, disclosed); r(t) = 1 if o in {0,1,2,3} else (mix mod 3).
  All deterministic; the program stores the ground truth.

## 3. Contestant: lifetime store engine (pure Zag)

Storage (structure-of-arrays, exact counts verified by engine
counter): arrays T (implicit, = index), F0..F3, A, O, R as u8/i32;
plus per-experience abstraction codes C1 (u8, under M1) and C2 (u8,
under M2, filled by the re-abstraction pass).

Indexes (built once after ingest):
- Exact: direct array index by t (O(1)).
- Pattern: inverted lists. For f0..f3: 16 lists each; a: 8 lists;
  o: 16 lists. Each list holds experience ids (sorted by insertion).
  Pattern query = intersect the relevant lists (two-pointer merge).
- Abstraction: after re-abstraction, inverted lists per C1 bin and per
  C2 bin (16 each), plus a 16x16 co-occurrence table (C1 bin x C2 bin
  counts) as the translation record.

Abstractions (frozen here):
- M1 (old): code = (f0/4)*4 + (f1/4). 16 bins over coarse (f0,f1).
- M2 (new): code = (f2/4)*4 + (f3/4). 16 bins over coarse (f2,f3).
- Re-abstraction pass: for every experience, compute C2 from raw
  (f2,f3) and build the C2 inverted lists and the C1xC2 co-occurrence
  table. C1 codes and lists are preserved untouched (no forgetting of
  the old abstraction).

Queries (frozen; counts verified against brute-force ground truth
computed from raw arrays):
- Q1 exact recall: 1000 pseudo-random t values; return full record;
  checksum over returned fields must equal the precomputed checksum.
- Q2 pattern: 200 patterns, each 1..3 constraints on
  {f0..f3, a, o}; return match count; must equal brute-force count.
- Q3 abstraction: (a) 64 queries "C2 == c" for random c; counts must
  equal brute-force over raw (f2,f3); (b) translation spot-check: 64
  random experiences, C1 and C2 codes must equal direct recomputation
  from raw features; (c) co-occurrence row sums must equal C1 bin
  totals.
- Q4 temporal range: 50 queries [t1,t2] x (r == 3); counts must equal
  brute-force.

Metrics per run (timings/RSS to stderr; stdout deterministic):
ingest ms, index-build ms, re-abstraction ms, per-query-type total ms
and mean latency, peak RSS kB (verbatim mnstress1.zag reader),
state bytes (arrays + lists + tables).

## 4. Baseline (same lifetime, same queries)

B-sql: SQLite implementation of the same logical work:
- table exp(t INTEGER PRIMARY KEY, f0,f1,f2,f3,a,o,r);
- indexes: on (f0),(f1),(f2),(f3),(a),(o),(r) to mirror the inverted
  lists; pattern queries use WHERE with AND.
- Q1: SELECT by t. Q2: SELECT COUNT(*) WHERE .... Q4: SELECT COUNT(*)
  WHERE t BETWEEN ? AND ? AND r=3.
- Abstraction: ALTER TABLE ADD COLUMN c1, c2; UPDATE exp SET c1 = ...,
  c2 = ... (mirrors the re-abstraction pass); Q3a: SELECT COUNT(*)
  WHERE c2=?; Q3b spot-check via recomputation in SQL.
- The lifetime data for the baseline is emitted by the Zag program
  itself (world.sql: 40,000 INSERTs), guaranteeing identical data.
  Driver is bash + sqlite3; timing via shell nanosecond clock around
  sqlite3 invocations. Same hardware.

## 5. Kill bars (numbered; ALL must pass for LIFETIME-TESTED)

- K1 (lifetime stored): experiences stored = 40,000 exactly, verified
  by engine counter; Q1 checksum over 1000 exact recalls matches the
  precomputed ground-truth checksum.
- K2 (retrieval tested): Q2 (200 patterns), Q3a/Q3b/Q3c
  (abstraction), Q4 (50 ranges) all executed; every returned count /
  code equals the brute-force ground truth computed from raw arrays.
  Re-abstraction pass completes; C1 codes/lists intact afterward.
- K3 (baseline comparison): B-sql implements ingest + indexes +
  Q1..Q4 + re-abstraction UPDATEs on identical data; wall-clock
  comparison reported for both directions (Zag vs SQLite); code size
  (Zag lines vs SQL+driver lines) reported. No superiority claim
  unless measured.
- K4 (purity/governance): pure Zag plus bash plus sqlite3 only (no .py
  files, no python3 invocation at any stage); zero em/en-dash bytes in
  committed docs and code comments; prereg commit strictly precedes
  implementation; 3/3 full runs byte-identical on normalized stdout.

## 6. Honest scope and anti-spoof notes

- The schema, both abstraction mappings, and all index structures are
  authored; the test measures storage/retrieval, not invention. The
  re-abstraction pass is a bulk recompute, not a learned re-grounding;
  the honest claim is about the COST and CORRECTNESS of applying a new
  abstraction to a full history, which is the mechanical substrate any
  re-grounding would need.
- SQLite is expected to be competitive or faster on pure bookkeeping;
  the honest question is WHERE (if anywhere) the Zag in-process engine
  differs: ingest/index latency profile, flat resource footprint,
  re-abstraction pass cost, integration with learner-owned state.
  Name the measured differences; do not claim unmeasured advantages.
- The causal regularity o = (f0 + 2*f1 + a) mod 16 is disclosed and is
  not used by any query; it exists so the lifetime is not pure noise.

## 7. Pre-stated expectations (not kill bars)

Exact recall should be near-free in both systems (array index vs PK
lookup). Pattern queries are the discriminating case: inverted-list
intersection vs indexed WHERE. Re-abstraction is a full scan in both;
the question is the constant factor. Any large gap either way is a
finding, not a failure.

## 8. Falsifiers

- F1: any query count/code disagrees with brute-force ground truth
  (wrong implementation; void, fix, re-run 3x).
- F2: Q1 checksum mismatch (storage corruption; void, fix).
- F3: re-abstraction alters any C1 code or C1 list (old abstraction
  not preserved; void, fix).

No bar may be altered after results. Timing methodology is frozen here.

## 9. Verdict rule

LIFETIME-TESTED iff K1..K4 all pass as numbered above. Any single
failure -> LIFETIME-FAIL with the failing bar named. Builder reports
LIFETIME-TESTED or LIFETIME-FAIL only; no SURVIVES claim (promotion
pipeline steps are for the parent to schedule).
