# W4 runlog — 2026-09-24

## Build
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (pinned build; `--no-zagd`).
- Command (cwd `pam/round4/wild/w4`, IO module copied beside source):
  `znc w4_selftrain.zag -o ~/workspace/scratch_wildb3/w4_selftrain --no-zagd`
- Result: success. Only known benign warnings: A0101 (guarded `field()`
  sentinel loop), A0102 (ignored `nio_close` result).
- Binary is scratch-only (NOT committed):
  `~/workspace/scratch_wildb3/w4_selftrain`

## Battery (2x determinism)
- `./w4_selftrain <tape> > w4_run1.txt`
- `./w4_selftrain <tape> > w4_run2.txt`
- `cmp w4_run1.txt w4_run2.txt` -> identical (no output).
- SHA-256 (both runs, and evidence copy):
  `8928815c5d6fa2e9b57e4ec640d3950294a9e001a619ee299a7b901e47d21860`

## Score
- `python3 wild/w4/score_w4.py ~/workspace/scratch_wildb3/w4_run1.txt` -> exit 0.
- Independent mirror agrees on every number (FINAL_CT, convergence,
  admits, revision trace, D-W4-1, instruments).

## Tape
- `pam/round3/m1/m1_cases.txt`
  SHA-256 `5d4160d1e1a06c8250376bc85367981722fe0002296ae168c581c8353322c611`
  (canonical frozen tape; verified before build).
