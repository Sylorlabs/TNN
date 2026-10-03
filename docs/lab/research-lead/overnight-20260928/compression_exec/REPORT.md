# COMPRESSION-EXEC REPORT: E10.1 TRIAL-UNIFY

**Proposal:** FRONTIER-AUDIT E10.1 TRIAL-UNIFY (Rank-1 compression candidate, COMPRESSION_AUDIT.md Rank 1): "Trial 4-phase loop → generic candidate-source iterator."

**Date:** 2026-10-03  
**Worker:** COMPRESSION-EXEC  
**Lane:** `docs/lab/research-lead/overnight-20260928/compression_exec/`  
**Branch:** `tnn-native-lab`

## Summary

The 4-phase hardcoded trial loop in TNN-2's `t2_trial` was replaced with a generic candidate-source iterator driven by a phase table. The phase ORDER now exists only as data in `t2_ptab`, not in control flow.

**Verdict: MECHANISM-SUBSUMPTION PASS, K2 LINE-COUNT FAIL → BUILD-FAIL overall.**

The general mechanism (table-driven iterator) DOES subsume the specific ones (4 hardcoded phases). This is proven by K1 (byte-identical behavior) and K5 (table-only reorder changes winner). However, K2 (≥20% line reduction) FAILS: the unified region is 103 lines vs frozen 81 lines. The audit's "~40 lines removable" estimate was mistaken; the table/gate/driver plumbing overhead exceeds the inline-code savings.

## Implementation

**File:** `tnn2_unify.zag` (1631 lines; frozen base 1591 lines + 40 net new)

**New functions:**
- `t2_ptab` (11 lines): phase table. 7 rows × 4 i32s (kind, param, gate, s0zero). Rows: chains k=2,3,4 (dc-gated), sums (comb-gated), counts (di-gated), chains k=1 (always), terminator.
- `t2_gate` (6 lines): gate evaluator (0=always, 1=require dc==0, 2=require di==0, 3=require comb>=0).
- `t2_tc` (10 lines): THE single assemble→verify→promote copy (was triple-duplicated in frozen phases 1/2/3).
- `t2_fc` (17 lines): chain family enumerator (was phase 1 + phase 4 inline).
- `t2_fs` (21 lines): sum family enumerator (was phase 2 inline).
- `t2_fn` (15 lines): count family enumerator (was phase 3 inline).
- `t2_trial` (23 lines): generic driver loop (was 81 lines with 4 hardcoded phases).

**Key design decisions:**
- Kind-tag dispatch (not fn pointers): matches codebase idiom; fn-pointer round-trip was probe-tested working but rejected as exotic.
- Single-hop phase body verified byte-identical to chains k=1 by inspection (same v/f copy, same `t2_asm_chain(W,v,2,f)`, same `promote_graph(...,f,1)`), so 4 phases → 3 families + table.
- znc miscompile guards: no `!(A&&B)` in while, nesting ≤3, no `_zag_print` for dynamic content, sound malloc pattern.

## Kill Bar Results

### K1: No-regression (FW1-FW9) — **PASS (FW1-FW8), INCOMPLETE (FW9)**

**Method:** Built `shim_frozen` (frozen base + driver; source SHA-256 verified == recorded `freeze_shim2.zag`) and `shim_unify` (unified base + driver; driver SHA identical in both arms). Ran 14 FW worlds (FW1-FW8) through both with fresh state per world. Compared stdout byte-for-byte.

**Result:** All 14 worlds byte-identical pre/post. 9/9 verdict families covered (FW1, FW2, FW3, FW4, FW5, FW6×7, FW7, FW8).

**FW9 limitation:** FW9_dagA/dagB were NOT run. The frozen base exhibits pathological slowness on FW9 (10 min/query, 30 queries, all -2 misses) due to trial-loop node allocation hitting the 1024-node eviction cliff (0.8s per alloc at capacity). This is a frozen-base performance characteristic, not a unification effect. Estimated 5+ hours per FW9 world; computationally infeasible in this task. FW1-FW8 exercise the same `t2_trial` code path (chains/sums/counts/single-hop); the algorithm is verified identical there.

### K2: Line reduction (≥20%, 81→≤64) — **FAIL**

**Method:** Counted non-blank non-comment lines in trial region.

**Result:**
- Frozen `t2_trial`: 81 lines.
- Unified trial region (`t2_ptab`+`t2_gate`+`t2_tc`+`t2_fc`+`t2_fs`+`t2_fn`+`t2_trial`): 103 lines.

**Analysis:** The 20% bar is below the information floor. The per-family enumeration bodies (chains/sums/counts) are irreducible (~53 lines); the table/gate/driver plumbing adds ~50 lines. The audit's "~40 lines removable" estimate did not account for the extraction overhead. The `t2_trial` FUNCTION alone compresses 81→23 lines (72%), but the region as a whole grows.

**Structural unification is real:** 4 phases → 1 iterator; triple-duplicated assemble/verify/promote → 1 copy (`t2_tc`); phase order → data (`t2_ptab`); single-hop subsumed as chains k=1. But K2 as frozen measures lines, and we fail it.

### K3: Zero new modes/bridges/handlers — **PASS**

**Method:** Diffed top-level `fn` definitions; diffed top-level `let` globals; grepped for mode/bridge/handler.

**Result:**
- 6 new functions (`t2_ptab`, `t2_gate`, `t2_tc`, `t2_fc`, `t2_fs`, `t2_fn`): these are the compression machinery (table, gate, shared try, family enumerators), NOT modes/bridges/handlers.
- 0 functions removed; `t2_trial` modified in place.
- 0 new globals.
- 0 new mode/bridge/handler strings (only pre-existing test name "one-handler-both-classes").

### K4: 3/3 byte-identical builds + 3/3 byte-identical runs — **PASS**

**Method:** Built unified shim 3× consecutively; sha256sum compared. Ran FW1-FW8 battery 3× on unified shim; outputs compared.

**Result:**
- 3/3 builds byte-identical (237417 bytes).
- 3/3 runs byte-identical (14 worlds × 3 reps).

### K5: Order-as-data — **PASS**

**Method:** Created synthetic probe world `k5_probe2.txt` where BOTH a k=1 chain (direct fact) and a k=2 chain (two-hop) yield expected=20. With default table (k=2 row before k=1 row), k=2 wins. Made a TABLE-ONLY edit (swapped k values in row0 and row5; 2 lines changed, verified by diff, no code logic touched), rebuilt, reran.

**Result:**
- Default table: K2 wins (2 DEP edges from MAP).
- Swapped table: K1 wins (1 DEP edge from MAP).
- Inspector (`k5_inspect2.zag`) counts DEP edges to distinguish.

**This proves:** Phase order exists ONLY in the table. A data-only reorder changes which candidate family wins. The general iterator subsumes the specific phase orderings.

## Does the compression work?

**Mechanism subsumption: YES.** The table-driven iterator produces byte-identical behavior to the 4-phase hardcoded loop (K1), introduces no new architectural concepts (K3), is deterministic (K4), and the order-as-data property is demonstrated (K5).

**Line-count compression: NO.** K2 fails (103 vs 81 lines, need ≤64). The audit's estimate was wrong.

## Does the general mechanism subsume the specific ones?

**YES.** The 4 specific phases (chains k=2/3/4, sums, counts, single-hop) are now rows in a table interpreted by one generic loop. The specific phase bodies (except the irreducible per-family enumeration) are replaced by the shared `t2_tc`. The phase ORDER, previously hardcoded in control flow, is now data. K5 proves the general mechanism can express orderings the specific code could not (without code edits).

## Artifacts

- `tnn2_unify.zag`: unified implementation (1631 lines)
- `tnn2_frozen_ref.zag`: frozen reference (NEVER EDITED; SHA verified)
- `shim_driver2.zag`: driver (SHA verified)
- `shim_frozen.zag` / `shim_unify.zag`: assembled shims
- `shim_frozen` / `shim_unify`: binaries (3/3 byte-identical)
- `build.sh`: build script with hash checks
- `run_k1_fast.sh`: K1 runner (FW1-FW8)
- `runs/pre/`, `runs/post/`, `runs/post2/`, `runs/post3/`: outputs
- `k5_probe.txt`, `k5_probe2.txt`: probe worlds
- `k5_inspect.zag`, `k5_inspect2.zag`: inspectors
- `worlds/`: 16 FW world files (hashes verified vs SEAL.md)

## Recommendation

The TRIAL-UNIFY mechanism is SOUND (subsumption proven) but does NOT achieve the audit's line-count goal. 

**For Micah:** The compression is architectural (fewer concepts, order-as-data) not textual (fewer lines). If the goal is "remove duplicated mechanisms when one general mechanism subsumes them" (Priority #10), this SUCCEEDS — the 4-phase mechanism is gone, replaced by 1 iterator + table. If the goal is strictly "fewer lines," this FAILS and the audit's Rank-1 estimate should be revised.

The K2 bar as frozen (≥20% line reduction) is not achievable for this candidate without removing irreducible per-family logic. Recommend either (a) accept the architectural compression and retire K2 for this candidate, or (b) reject TRIAL-UNIFY and try the next-ranked candidate.
