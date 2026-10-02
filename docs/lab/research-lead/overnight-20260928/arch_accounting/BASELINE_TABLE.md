# Architecture Accounting: Baseline Table

Date: 2026-09-30. Worker: Architecture Accounting Auditor.
Status: ARCH-ACCOUNTING-BASELINE-COMPLETE.
Method: MEASUREMENT_PROCEDURE.md, applied to frozen sources.

## Headline table

| Generation | Capabilities passed | Cognition source lines | Semantic cases | Modes | Bridges | Handlers | Learner-state bytes | New learned structures |
|---|---|---|---|---|---|---|---|---|
| Frozen core (87ac95d08 / run 97b28e6a6) | 1/9 freeze worlds | 586 | 0 | 0 | 0 | 0 | 32768 | 0 |
| contlearn2 (179b4a950) | LEARNER-EXTENDED | 136 | 0 | 0 | 0 | 0 | 1024 | 0 |
| CLA-2 (e639904f2) | 15/15 self-tests (sealed FW pending) | 685 | 0 | 0 | 0 | 0 | 16384 | 3 (GROUP, MAP, edge-standing) |
| CAM-1 (371d20743) | 6/6 synthetic (sealed FW pending) | 408 | 0 | 0 | 0 | 0 | 344080 | 1 (MAP nodes) |
| ACT (f7d87938f) | 24/24 tests (sealed FW pending) | 162 | 0 | 0 | 0 | 0 | 33816 | 2 (POLICY_ROOT, GUIDEs) |

Desired trajectory: capabilities up, learner-created state up,
specialized source down, modes/bridges/handlers at zero.

## Frozen core baseline detail

Source: docs/lab/research-lead/overnight-20260928/core_freeze/stage0/world_learn.zag
at commit e129b2fbd (frozen at 87ac95d08).
Total lines: 1424. Comment-only lines: 113. Functions: 75.

| Category | Lines | Functions |
|---|---|---|
| INFRA (io, alloc, string, byte helpers) | 33 | 9 |
| ACCESSOR (slot/field read/write) | 33 | 14 |
| COGNITION: associative store (find_key, learn, query, evict_c, importance_c, twohop, store_count, signof) | 105 | 8 |
| COGNITION: DDES/causal derivation (verbatim frozen: compute_arrivals, compute_frontier, eff_waits, synthesize_plan_gen, predict_gen, world_step_gen) | 137 | 6 |
| COGNITION: episode/candidate machinery (frontier_surv, feed_ep, oneshot_ep, adapt_ep, exec_plan_ep, pred_cand, dquery, zero_ledger, earn_guarded) | 344 | 9 |
| DIAG (hashing, junk count, collision record) | 84 | 6 |
| FIXTURE (load_e0..load_r3 frozen case loaders) | 120 | 9 |
| EMIT helpers (emit_plan, emit_survivors) | 30 | 2 |
| LEGACY (legacy_p1_p11, retained for provenance) | 356 | 1 |
| PARSE/DRIVER (event parsing, process_line, drive_world, main) | 174 | 11 |

Cognition source lines: 105 + 137 + 344 = 586.

Semantic cases: 0 (no switch/match; no hardcoded domain-id branches;
event dispatch is on generic OBSERVE/QUERY/ACT only).
Modes: 0 (no _MODE identifiers).
Bridges: 0 (no bridge functions).
Handlers: 0 (no handle_ functions).
Learner-state bytes: 32768 (single W, per FREEZE_RECORD.md and REGIONS.md).
New learned structures: 0 (fixed slots; learner fills values, creates no structure).

Capabilities: 1/9 WORLD-PASS (W1 10/12; W2-W9 fail), per RUN_RESULTS.md
at 97b28e6a6 and confirmed by pure-Zag rescore at 5325ffed8.

## contlearn2 baseline detail

Source: docs/lab/research-lead/overnight-20260928/continuing_learner/contlearn2.zag
at commit 179b4a950.
Total lines: 363. Comment-only lines: 25. Functions: 26.

| Category | Lines | Functions |
|---|---|---|
| INFRA (emit, i64s, e64, z_alloc, get32, set32) | 25 | 6 |
| ACCESSOR (true_obj, subj_of, sbase, sf, sw, sch, schw, ctr, ctrw, ctradd) | 35 | 10 |
| COGNITION (free_slot, learn, query, iobj, discover, discover2, gate1_pass, queries_correct, retire_ledger, retire_consec) | 136 | 10 |
| DRIVER (main, includes test harness) | 159 | 1 |

Cognition source lines: 136.

Semantic cases: 0. Modes: 0. Bridges: 0. Handlers: 0.
Learner-state bytes: 1024 (z_alloc(1024) in main).
New learned structures: 0 (fixed 20-byte slots, schema at 640,
counters at 664; learner fills values, creates no structure).

Capabilities: LEARNER-EXTENDED, per CL2_RESULT.md at 179b4a950.

## Re-measurement note (2026-09-30)

The CLA-2 projection ("40-60 retention lines, net-negative vs mechanism
sum") did not hold for the separate implementations. Measured:
CLA-2 685 + CAM-1 408 + ACT 162 = 1255 cognition lines vs 586 for the
frozen core. The three builders each wrote a full stack with duplicated
workspace machinery (roughly 404 lines of duplicated INFRA/ACCESSOR).

Modes, bridges, handlers, and semantic cases hold at zero across all
three. Learned structures are now nonzero (3/1/2) where the baselines
were zero.

The honest comparison awaits the integrated one-system implementation
measured on sealed FW1-FW9. See REMEASURE_REPORT.md in arch_remeasure/
for the full analysis.

## Reading the baselines

The frozen core carries 586 cognition lines for 1/9 worlds. The bulk
sits in episode/candidate machinery (344) and verbatim DDES derivation
(137); the associative store itself is 105. contlearn2 is leaner (136)
but also narrower in capability. Neither creates learner structures;
both use fixed slots.

The CLA-2 projection (40-60 retention lines, net-negative vs mechanism
sum) will be tested when the builder lands: the honest comparison is
CLA-2 + CAM-1 + ACT cognition lines against the 586-line frozen core,
with capabilities measured on fresh adversarial worlds.

## Re-measurement log

| Date | Generation | Trigger | Result |
|---|---|---|---|
| 2026-09-30 | frozen core, contlearn2 | initial baseline | this document |
| 2026-09-30 | CLA-2 (e639904f2), CAM-1 (371d20743), ACT (f7d87938f) | builder landings | REMEASURE_REPORT.md in arch_remeasure/; sum 1255 vs 586; details in report |

Append rows here on every re-measurement. Never edit historical rows.
