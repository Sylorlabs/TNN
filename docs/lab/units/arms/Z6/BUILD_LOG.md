# Z6 — BUILD_LOG

## 2026-09-21 — rebuild from scratch (ARM CREW Z6)

The pre-existing draft (`Z6/.work/ref_arm_draft_broken.zag`, from an
interrupted earlier crew) was unrecoverable: miswired `_zag_arg` handling,
uninitialized sentinels, and a broken scar-sort. It was kept for reference
only; `cl/arm.zag` was written fresh.

Build discipline: minimal compiling skeleton first, then ~100-line
increments, compiling after each. Final source is ~1,700 lines of pure Zag.

### Compiler/workstation issues hit and worked around

- `nio_alloc(N) as []i32` miscompiles consecutive same-size indexed tables
  (ZNC-2026-09-21-007): all tables are `[]u8` arenas with explicit
  little-endian `w32`/`ws32` accessors.
- No slice > 2^25 bytes: the 4-shard audit ledger keeps each shard under the
  limit (code corpus needs ~165k entries × 64 B ≈ 10.6 MB → 4 shards).
- `_zag_arg(n)` is non-owned (never free); `argc` is always 0 (read args
  unconditionally); `_zag_strcmp` returns 1 on equality.
- `ns_sha256(input, out)` is the hash API (`out` = 32 bytes); wrapped for
  the M8 determinism battery.

### Correctness bugs found by testing (not by reasoning)

1. Scar proposal sort was an insertion sort over 148k cuts — replaced with a
   sound sort; `rctrl_rate` kept O(L+S) via sort + two-pointer merge.
2. `gt_match` negative-index sentinel — fixed.
3. Headline scar scoring first counted every 64-byte grid cut; corrected to
   scar-born/displaced boundaries only (birth-seq `cborn` tracking).
4. M3 fresh-recall double-counted reused slots — per-slot fresh-index tags.
5. M4 repair-entry count reported 0 — shard-aware `led_op` reader fixed it
   (200 entries verified).
6. A15 first compared a span to itself (vacuous). Rewrote as a genuine
   remap→re-resolve→restore probe against independent reference buffers;
   64/64 pass.

### Battery (final)

- Binary: `Z6/.work/z6_1x` (build artifact, not committed).
- `Z6/.work/run_battery_1x.sh`: all 19 legs × 2 runs, byte-identical stdout
  required, `cmp` enforced. Result: BATTERY PASS.
- Evidence: `Z6/.work/evidence/1x/` (per-leg run logs + `metrics_1x.jsonl`).
- Scorecard: `Z6/.work/scorecard_z6_1x.json` via `z6_assemble.py`.

### Determinism (M8)

Five environmental perturbations (heap pre-dirty, fragmentation, image
pre-fill, stdout junk, layout jitter) × 2 runs: sha256 over memory image,
audit bytes (used, in entry order), canonical state, and allocation trace
are byte-identical across all 10 runs. Zero RNG in any decision path;
SplitMix64 appears only as the frozen offline schedule/control reference.

### Provisional items

- M5 storage accounting and A15 ID-remap probe are labeled
  `PROVISIONAL-PENDING-FREEZE` pending Micah's freeze-vs-retention ruling.
- `GT_WIN=64` positional tolerance is the crew's preregistered reading of
  "match"; the frozen row states no tolerance (ARM_SPEC §8).
