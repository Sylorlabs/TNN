# Y5 Build Log

## Source
- `units/arms/Y5/cl/arm.zag` (single-file Zag implementation, pure Zag cognition)
- Substrate: `R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag`
- Compiler (frozen): `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Binary: `units/arms/Y5/.work/y5_arm` (NOT committed)

## Compile
- First successful compile: 2026-09-21 (after fixing `y_free`, `jf_int`, `probe_reg`,
  `main()` dispatch to exact harness mode names).
- Warnings only (unused returns, string buffer lints); zero errors.

## Bugs found and fixed during bring-up
1. **M3 valuable mapping.** Survival check derived (corpus, offset) from `v*58`,
   but code valuable are indexed `(v-365)*58`. Only 365/1000 checked correctly
   (36.6% survival). Fixed by storing (cid, off) per valuable at record time.
   Result: 100.0% survival.
2. **y_recall on absorbed members.** `y_recall` consulted `R_REMAP` directly, but
   tombstoned members are not live → returned -1. M7 hit rate was 76.7%.
   Fixed: `y_recall` now resolves through link-absorption (`y_resolve`) first,
   then the ID remap layer. Result: 100.0% hit. M1 swap probe still PASS.

## 1x battery (r1 corpus)
- All 16 legs: rc=0, stdout byte-identical across double runs.
- M8 gate: 5 perturbations × 2 runs, `M8GATE PASS` (byte-identical artifacts).
- Scorecard: `units/arms/Y5/.work/scorecard_y5_1x.json`
- M5 memory: 1.498× (bar ≤1.5) — PASS, but close. Audit: 5.015/KB (bar ≤10).
- Binding kill: degradation 0.0%, atomicity violations 0 — kill does NOT fire.

## 10x battery (r10 corpus)
- Started 2026-09-21; see `battery10.log`.

## Determinism
- Zero RNG in AI decision paths (verified by source scan: no random, no clock,
  no address/PID in decision logic).
- Byte-identical reruns confirmed by harness double-run diffs (all legs) and
  the M8 external gate (10 runs).

## Provisional items (logged, not reinterpreted)
- M1 ID-swap probe: PROVISIONAL-PENDING-FREEZE (A15). Implemented literally.
- M7 schedule: provisional A7/A8 (C, C, C′ every-100th-XOR, 5,000 lookups).
- M8: B-64 combined-instance reading (A17).
