# M2 — Build Log

## Source
- `units/arms/M2/cl/arm.zag` (M2 implementation, pure Zag)
- `units/arms/M2/R33_NATIVE_SHA256_V2.zag` + `R33_NATIVE_IO_V1.zag` (root-level
  copies; `cl/arm.zag` imports `../R33_NATIVE_SHA256_V2.zag`)
- `units/arms/M2/substrate/` (copies, as in ARM M)

Built with: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Command: `znc_linux_x86_64_abed8aa1 cl/arm.zag -o <out>` (run from `units/arms/M2/`)
- Warnings: A0102 (ignored return values) for `ns_sha256`, `m2_comp_add`,
  `nio_close` — non-fatal, results checked where load-bearing.

## Design lineage
- Started from ARM M (`units/arms/M/cl/arm.zag`), renamed M→M2.
- The unmodified renamed base compiled successfully 2026-09-21 ~02:58.
- M2 compositional layer added: `M2` struct extended with composition arrays
  (`comp_id`, `comp_sa/sb`, `comp_qa/qb`, `comp_depth`, `comp_off/len/corpus`,
  `comp_map`), `m2_build_compositions`, `m2_parent_id` (SHA-256),
  `m2_comp_verify`, `m2_recall_composed`, K1 probe, K2 benchmark.
- ARM M's `t_merge` / `merge-1x` removed (unrelated to M2).

## Bug fixes during build
1. `m2_add` undefined (K1 probe) → replaced with in-place byte flip +
   `m2_kill` + `m2_ingest` (new counter ID, M2 revision semantics).
2. JSON `arm` tag `"m"` → `"m2"`.
3. `ns_sha256` return value now checked in `m2_parent_id`.
4. t_m6 capacity: `nt+ny+64` → `4*nt+ny+1024` (matched ARM M; fixed
   "slice index out of bounds" panic).
5. t_m3 capacity: `M2_M3_CAP` (4000) → `9000` (matched ARM M).
6. Added `m8-1x` dispatch mode (for `harness/m8_gate.sh`; perturbation name
   in argv[4]).
7. Added `m2-k2-10x` / `m2-k2-code-10x` modes (10x ID scale via 10x ingest
   of r1 corpus; see ARM_SPEC.md §4).

## Battery
- 1x M1–M9 via `~/workspace/m2scratch/run_m2_battery.sh` (custom; M2 mode
  names differ from `harness/run_battery.sh`).
- Each leg: `harness/run_metric.sh` (2 runs, stdout diffed, byte-identical).
- M8: `harness/m8_gate.sh` (5 perturbations × 2 runs, byte-identical).
- Workdir: `/home/hatch/workspace/m2scratch/battery_1x/` (not `/tmp`).

## K2 (binding)
- Mode `m2-k2-10x`: 10x ingest of r1 prose (847k leaves, ~635k compositions).
- Measures T_recompute (parent-ID SHA-256 + map lookup) vs T_recall
  (leaf + composed recall with verify). Kill if >10%.
- Note: r10 corpus (54MB) exceeds the 2^25 single-slice limit; 10x ID scale
  achieved via 10x ingest (byte content reused; K2 is byte-independent).
