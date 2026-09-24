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
- Frozen commit: _(pending)_
