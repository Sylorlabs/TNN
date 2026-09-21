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
- Duel heisenbug at E=150+: ROOT-CAUSED 2026-09-21 — silent i32 overflow in
  `duel_edits` edit-position computation `(e*total)/E` (wraps negative at
  r1 corpus sizes for E>=150; mirror write `prose[off]=255` panics). Fixed
  with i64 arithmetic; same latent overflow in `t_m9` fixed. Full duel
  E=0..1000 completes cleanly; both reruns byte-identical stdout, rc=0.
- The custom runner is not the official complete battery (missing memorizer
  controls). Results are provisional.

## Rebuild (2026-09-21, heisenbug fix)
- Fixed `duel_edits` and `t_m9` in `cl/arm.zag` (i64 edit-position
  arithmetic; two-line change + comments).
- New binary: `/home/hatch/workspace/u_test` (rebuilt; 236,105 bytes main).
- Full duel re-run: E=0..1000, both reruns byte-identical, rc=0.
- M9 re-run: e0=175944, e10=175944, e50=203976, e100=727756, e200=727848,
  e500=727204, e1000=727204, rekey=0, hits=0; byte-identical across reruns.
- No commit of binaries, .zagd, .zag-cache/ (workspace build artifacts only).
