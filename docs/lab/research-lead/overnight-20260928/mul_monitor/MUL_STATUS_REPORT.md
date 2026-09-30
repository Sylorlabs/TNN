# MUL Progress Monitor Report

**Date:** 2026-09-30, ~22:26 UTC
**Verdict: MUL-STATUS-REPORTED** (builder making progress, not stuck, not failed)

## Commit status

No commits yet under `docs/lab/research-lead/overnight-20260928/mul_build/`. The directory exists in the working tree as untracked (NAMECHECK.md, mul1.zag, mul1_bin, logs). The builder is mid-wave.

## Working directory state (read-only observation)

| File | Size | mtime (UTC) | Note |
|---|---|---|---|
| NAMECHECK.md | 1.4 KB | 22:21:15 | Step 0 guard recorded |
| mul1.zag | 20 KB | 22:25:12 | Implementation source |
| mul1_bin | 55 KB | 22:25:16 | Compiled, executable |
| build.err | 93 B | 22:25:14 | One benign znc warning (zagd unavailable, foreground compile continued) |
| run1.log | 1.4 KB | 22:24:35 | First test run: 0/6 pass (builder bug) |
| run2.log | 1.4 KB | 22:25:49 | Second test run: 6/6 pass |

## Test trajectory

**run1 (22:24):** 0/6. Phase 3 promoted the 4-step program `[ACCUM_RX STEP_C TEST_CY GOTO(0)]` but the materialized PROC root returned 0 on every probe (execution bug), and transfer width/height were 0.

**run2 (22:25):** 6/6, one minute later. The builder diagnosed and fixed the execution bug:
- P-MUL1: 8/8 held-out probes correct, including the scaling probe (13,17) -> 221
- P-MUL2: Tier2 structural check pass
- P-MUL3: ablation destroys MUL (8/8 wrong-or-unknown) while ADD and facts stay intact
- P-MUL4: transfer via EXECUTE(MUL root) gives rect area 42
- P-MUL5: lookup control 0/8 (under frozen ceiling 2), margin 8 >= 5
- SHUFFLED: same 4-step program promoted on shuffled exemplars, 8/8, scaling 221; ORACLE-AUDIT-3 pass (order not load-bearing)

The promoted program is a repeated-addition loop body: accumulate RX, step counter, test cycle, goto start. 72 genuine rejections were recorded during search, so the search is not trivially accepting.

## Assessment

The builder iterated from a failing run to a full pass within one minute. Logs are still updating (run2 finished ~1 minute before this report). Likely remaining work: Rung B arm, determinism re-runs, BUILD_REPORT.md, then commit. No interference warranted. No replacement spawned.

## Governance

Monitoring only; no builder files touched. No Python invoked. Contaminated paper not touched. No em dashes in this report (byte-checked convention: use none).
