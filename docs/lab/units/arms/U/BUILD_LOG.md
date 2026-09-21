# BUILD_LOG.md — U: Recompute-on-demand

## Source
- `cl/arm.zag` (pure Zag, zero randomness).
- Substrate: `substrate/R33_NATIVE_SHA256_V2.zag`, `substrate/R33_NATIVE_IO_V1.zag`
  (copied to trial dir per AGENTS.md lesson).
- Toolchain: `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## Build history (2026-09-21)
- Multiple iterations to fix: M2 double-normalization bug, cid_of missing
  t2/t3 corpora, d_recall negative-index bug (missing [a,b) clip), duel_edits
  expected-bytes sync, M9 JSON interleaving.
- Final binary: `/home/hatch/workspace/u_test` (236,018 bytes).
- 77 analyzer warnings (A0102 ignored return values; non-blocking).

## Compliance status
The source COMPILES but is NOT frozen-spec compliant for the BLOCKED items
in AMBIGUITIES.md (A1–A4, A9). Provisional values are used for engineering
only. All runs are reported as provisional, NOT accepted frozen evidence,
until the blocks are resolved.

## Battery
- Workdir: `work/r1-1x/` (under ~/workspace, per rule).
- Runner: `work/run_u_battery.sh` (custom; omits the two memorizer-control
  legs — NOT the official complete battery).
- Harness legs via `run_metric.sh` (double-run, stdout-identical check).
- M8 gate via `m8_gate.sh`: PASS (5 perturbations × 2 reruns, byte-identical).

## Known issues
- Duel heisenbug at E=200+ (see AMBIGUITIES.md A8). E=0..100 clean.
- The custom runner is not the official complete battery (missing memorizer
  controls). Results are provisional.
