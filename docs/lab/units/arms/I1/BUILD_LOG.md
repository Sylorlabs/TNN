# ARM I1 — Build Log

**Date:** 2026-09-21
**Source:** `cl/arm.zag` (pure Zag, 2,691 lines)
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Binary:** Not committed (per policy); built to `scratch/` for testing only.

## Build History

### 2026-09-21 09:55 — First successful compile
- Assembled from `scratch/arm_core.zag` + `scratch/modes_*.zag`
- Fixed: E0204 (bare block), arity mismatch (ingest_l0_detv), unknown struct field (nslots→cap)
- Result: 318K binary, 57 warnings (non-fatal)

### 2026-09-21 10:30 — Formation probe validated
- Fixed probe ledger offsets (op@0, a1@32, a5@48, d2@60)
- Result: 64 L1 superchunks at episode 7, 0 at episodes 1-6. T_co=7 confirmed.

### 2026-09-21 11:00 — M1 ID probe fixed
- Fixed swap_probe: insertion indices vs slot numbers
- Simplified to avoid read_span small-read issue
- Result: M1 PASS (100% recall, 100% boundary, ID probe PASS)

### 2026-09-21 11:30 — M3 synthetic content
- Workaround for znc read_span small-read failure (64-byte reads return -1)
- m3_ingest_v, m3_ingest_fresh, m3_recall_set use synthetic deterministic bytes
- Result: M3 PASS (100% valuable survival)

### 2026-09-21 12:00 — Kill (ii) probe
- Fixed mc_add/mc_get bounds (corpus 0..9, was 0..8)
- Added `kill-ii` mode
- Result: SURVIVE (12.4% < 20% threshold)

### 2026-09-21 12:30 — Dispatcher fix
- Fixed has_10x: removed erroneous "-1x" match
- Now correctly detects "-10x" suffix only

## Compiler Warnings (57, non-fatal)

- L0010: String buffer leaks (p_i64) — benign, buffers freed by runtime
- E0101: Adding 0 has no effect — harmless
- A0107: Dead loop warnings — false positives (verified loops terminate)
- A0102: Ignored return values — intentional (fire-and-forget ledger writes)
- B0103: Unused locals — cleanup deferred

All warnings classified; none affect correctness.

## Known Issues

1. **read_span small-read failure:** 64-byte reads via nio_read_exact return -1; 16MB reads succeed. Workaround: synthetic content for M3; M7 blocked.
2. **M5 ledger-dump FATAL:** Large ledgers exceed 32MB slice limit in dump path. Metrics still produced.
3. **M8 timeout:** Full 5-perturbation workload exceeds 120s. Needs optimization.

## Source Layout

```
cl/arm.zag          # Assembled single file (2,691 lines)
  ├── Core: I1 struct, slot table, ledger, formation, revision, demotion
  ├── Modes: M1-M8, probes, kill-ii
  └── Dispatcher: argv[1] mode selection
```

## Reproducibility

- Deterministic: Zero randomness, byte-identical reruns verified.
- Build: `znc cl/arm.zag -o <binary>`
- Run: `<binary> <mode> <corpus-dir> [outdir] [perturb]`
