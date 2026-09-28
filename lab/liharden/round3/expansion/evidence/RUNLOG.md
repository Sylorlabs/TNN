# RUNLOG — candidate-set expansion demo

## Build

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (pinned znc per AGENTS.md).
- Source: `expansion.zag` (+ `R33_NATIVE_IO_V1.zag` import, copied from
  `liharden/glue/`).
- Command (cwd = expansion_work/):
  `znc_linux_x86_64_abed8aa1 expansion.zag -o expansion_bin`
- Build result: success, analyzer warnings only (A0102 nio_close discards,
  A0101 off-by-one idiom — same idioms as the measured wallsel.zag probe).
- Binary NOT committed (per standing rule: no build binaries in the repo).

## Battery

For d in 0 1 2; for each fixtures/*.flat.txt; for r in 1 2:
`./expansion_bin <fixture> <d> > evidence/run_<case>_d<d>_r<r>.log`

54 runs total (9 fixtures × 3 depths × 2 reps).

## Determinism check

`cmp` per rep-pair: 27/27 byte-identical (0 fails).

## Depth sweep (measured)

| depth | attack fixtures (4) | honest+S3 (5) | C_SPLIT |
|---|---|---|---|
| 0 | INSTALL 4/4 (baseline failure) | INSTALL | WITHHOLD\|CONTRADICTION |
| 1 | WITHHOLD\|HIDDEN-DISSENT 4/4 | INSTALL (unchanged) | unchanged |
| 2 | WITHHOLD\|HIDDEN-DISSENT 4/4 (no new kills) | INSTALL (unchanged) | unchanged |

Opened-page cost, W_R3: depth 1 → 5 pages, depth 2 → 7 pages (noise n1/n2
opened, no verdict change). Depth 1 is the cost-minimal sufficient default.
