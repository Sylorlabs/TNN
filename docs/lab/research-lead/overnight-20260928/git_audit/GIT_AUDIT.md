# Git History Audit: Sweep Collisions and Pathspec Compliance

**Status:** GIT-AUDIT-COMPLETE
**Date:** 2026-10-01
**Scope:** 30 commits from `97b80383a` through `84d91dd9f` (all commits since the explicit-pathspec convention was adopted after collision `bda26cf91`).
**Method:** `git show --stat` for each commit; verify all files belong to the single workstream named in the commit message.

## Verdict: CLEAN. Zero sweep collisions. Zero pathspec violations.

All 30 commits contain only files from the single workstream described in the commit message. The explicit-pathspec convention (`git add -- <paths>` and `git commit -m "msg" -- <paths>`) is working.

## Per-Commit Findings

| Commit | Message (short) | Files | Workstream dirs | Verdict |
|--------|-----------------|-------|-----------------|---------|
| 84d91dd9f | Discount adversary run | 9 | `discount_advrun/` | CLEAN |
| 8ad158352 | DYN-1 on discount pilot | 9 | `dyn1_discount/` | CLEAN |
| 7abc6138b | Protocol QA fixes | 2 | `lifetime_protocol/`, `protocol_qafix/` | CLEAN (both protocol-related) |
| 3708fbd15 | Interference experiment | 8 | `interference_experiment/` | CLEAN |
| dc6b0cfd2 | Wave 20261001-0821pdt record | many | `rsi/runs/wave-20261001-0821pdt/` | CLEAN (all under one wave dir) |
| c040e5fde | WEAK-KLT5-EVAL-COMPLETE | 19 | `weak_klt5_eval/` | CLEAN |
| bc96dd3d8 | BUDGET-PRESSURE-COMPLETE | 10 | `budget_pressure/` | CLEAN |
| 7a3ba6137 | Fossil census | 14 | `fossil_census/` | CLEAN |
| f3e6985d4 | Decline gate pilot | 10 | `decline_gate/` | CLEAN |
| 9f472c725 | NODE1-EFFICACY-COMPLETE | 13 | `node1_efficacy/` | CLEAN |
| b0cd36859 | Discount adversary design | 2 | `discount_adversary/` | CLEAN |
| 3c2dcdec9 | Edge-overflow sketch | 2 | `edge_overflow/` | CLEAN |
| 2a8f4245d | Discount T-sensitivity | 18 | `discount_t/` | CLEAN |
| 2a7e34ffc | Protocol QA dash cleanup | 1 | `protocol_qa/` | CLEAN |
| 557cff134 | Spec errata compile | 2 | `spec_errata/` | CLEAN |
| a125a1984 | Protocol QA check | 2 | `protocol_qa/` | CLEAN |
| 67b700d3f | DYN1-NODE1-COMPLETE | 13 | `dyn1_node1/` | CLEAN |
| 0266321cc | Fragment guard verification | 2 | `fragment_guard/` | CLEAN |
| ff13a411d | Arch audit | 2 | `arch_audit/` | CLEAN |
| 458035b01 | Protocol update (corruption detector) | 2 | `lifetime_protocol/`, `protocol_update/` | CLEAN (both protocol-related) |
| 0daaa2ed4 | Discount pilot impl | 11 | `discount_impl/` | CLEAN |
| 8307a9a9e | Substrate test designs | 2 | `substrate_tests/` | CLEAN |
| ff2d1e1ef | Corruption detector spec | 2 | `corruption_detector/` | CLEAN |
| 8b7b0f12a | Fragment record spec | 2 | `fragment_record/` | CLEAN |
| 003767553 | DYN1-COMPLETE | 9 | `dyn1/` | CLEAN |
| 62fa77192 | Discount spec | 2 | `discount/` | CLEAN |
| 550fa268b | Shared substrate spec | 2 | `shared_substrate/` | CLEAN |
| 94011d705 | Weak K-LT-5 sealed world | 5 | `weak_klt5_world/` | CLEAN |
| 2b81d0692 | Zombie census | 9 | `zombie_census/` | CLEAN |
| 97b80383a | Composition build-questions | 2 | `composition_build/` | CLEAN |

## Notes

1. **Two-file protocol commits are not collisions.** Commits `7abc6138b` and `458035b01` each touch `lifetime_protocol/LIFETIME_PROTOCOL_V2.md` plus a `protocol_*` NAMECHECK.md. Both files serve the same workstream (the protocol update); the NAMECHECK records the worker's toolchain guard for that update. This is the documented pattern, not a sweep-in.

2. **Wave record commit is not a collision.** Commit `dc6b0cfd2` contains many files, but all reside under `rsi/runs/wave-20261001-0821pdt/`. A wave record legitimately aggregates that wave's artifacts. No unrelated workstream files are present.

3. **Prior collisions not re-audited.** Commits `0cab8938f`, `3eeb0d78e`, and `bda26cf91` predate the convention and are documented in parent context. They were not re-examined; the audit covers only post-convention history.

4. **No index.lock interference observed.** All `git show` operations completed without lock contention.

## Standing Metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (audit only)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- All other metrics: 0
- COGNITION LINES: 0 added
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0
