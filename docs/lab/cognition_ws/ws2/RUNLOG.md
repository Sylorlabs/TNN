# WS2-A RUNLOG — memory-retrieval white-box investigation

## 2026-09-24 ~08:05 PDT — task received
WS2-A dispatched: white-box investigate where TNN memory retrieval fails today.

## 2026-09-24 — machinery survey
Read and mapped:
- `memory_org/arms/lib.zag` (full, 1320 lines): retrieval = per-item
  `is_candidate` predicate (conjunctive exact-hint gating per scheme level)
  + exact-token-overlap scoring + top-k (score desc, id asc tie-break).
  No index: every query full-scans all n items. `filing.txt` is never read
  by retrieval (write-only bookkeeping). `topk` always fills to k — no
  score threshold, so negative queries return junk at score 0.
- `wave2/memoryagency/trial/memory_core.zag`: MA1 slot ops (add/kill/pin/
  promote); retrieval is by slot address, no content query path. Trial
  58/58 (TRIAL_RESULTS_MA1.md + EVIDENCE_20260924T071233Z).
- `wave2/posttable/ctx/ctx_core.zag`: partitions hold regime belief only;
  no cross-partition content retrieval path (by design).
- `knowledge/kb_control/crewA/ROOTCAUSE_A.md`: 1GB blob D1 (post-boundary
  offsets wrong -> recall fail-closed) + D2 (revise clobbers 126 bytes of
  unrelated fact). Cited as clobber-family subsystem; not re-run.

## 2026-09-24 — battery frozen (prereg)
- `cognition_ws/shared/PROBE_BATTERY_SPEC.md` v1 written (51 queries,
  5 classes: P-AGE, P-COLL, P-CTX, P-PARA, P-NEG).
- Fixtures: `ws2/fixtures/probe_corpus.txt` (34 lines / 33 ids incl.
  PD01 duplicate), `ws2/fixtures/probe_queries.txt` (51 queries),
  `ws2/fixtures/validate_battery.py` (build-time invariant checker).
- Validator passes: PARA zero-overlap vs gold, NEG zero-overlap vs all,
  X1 dhint-mismatch, non-NEG queries token-matchable.
- Frozen commit: `df0ea3ecf5c1377762c072f0476eb18abcbd9305`
  (sylorlabs/TNN, tnn-native-lab) — committed BEFORE any probe run.

## 2026-09-24 — battery amendment v1 → v1.1 (BEFORE any valid run)
Defect found at first run: the query-file header comment contained 7 pipes,
so `parse_queries` counted it as a 52nd phantom query. Fix: header comment
rewritten (zero query bytes changed), version bumped to v1.1 in both
fixture headers. Validator re-passed. The v1 run was discarded; all runs
below are v1.1. (This is exactly the pre-declared amendment procedure.)

## 2026-09-24 — harness built
- `ws2/probe.zag`: instrumented driver reusing lib.zag primitives
  (`build_tab`, `build_hay`, `is_candidate`, `tok_count`, `topk`,
  `parse_queries`); per-query TSV trace
  `qid|kind|scheme|installed|candidate|lvl|score|rank|top1|nret|outcome|fail`;
  self-consistency check (trace predicate vs topk predicate).
- `ws2/build.sh`, `ws2/run_battery.sh`, `ws2/analyze.py`,
  `ws2/fixtures/calib.txt` (SELF choose).
- All 4 binaries built clean first try with the pinned znc.

## 2026-09-24 — run1 + run2 (v1.1), byte-identical
Full rebuild + ingest (33 items; PD01 dedup→first) + choose (S6 everywhere)
+ census + 51-query trace × 3 arms, from clean dirs, twice.
- census (all arms, pre+post): `6c257346868b794e8926e4eeb59d64a98c7149233b5d57c9e96765488e5a79f5`
- trace_flat:    `a5ea1fb983ea984bc6edfb5d6d2e89f50832befd288b02bcf6f76a313b36c620`
- trace_imposed: `e1dc6ad44c4e504444da38014cb59375f2fc99880bb9ac8f82355822e020073b`
- trace_self:    `275c09b91468977b0ba48e82ee60c34eb0ccae94bc4d4827f6a3f276a0ddd08e`
- inconsistencies=0 (both runs). run1 vs run2: all 6 files byte-identical.
- Outcomes: FLAT 39 FOUND/6 TOKEN_MISS/6 FALSE_POSITIVE;
  IMPOSED 28/17/6; SELF 39/6/6 (choose picked S6 for all domains+global).
- Interim failure map: `ws2/WS2A_PRELIM.md`.
