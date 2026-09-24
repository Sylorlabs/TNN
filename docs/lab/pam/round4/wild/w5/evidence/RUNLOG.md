# W5 runlog — 2026-09-24

## Build
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (pinned build; `--no-zagd`).
- Command (cwd `pam/round4/wild/w5`, IO module copied beside source):
  `znc w5_memory.zag -o ~/workspace/scratch_wildb3/w5_memory --no-zagd`
- Result: success; no new warnings beyond the known benign A0101/A0102 set.
- Binary is scratch-only (NOT committed):
  `~/workspace/scratch_wildb3/w5_memory`

## Battery (2x determinism)
- `./w5_memory <tape> > w5_run1.txt`
- `./w5_memory <tape> > w5_run2.txt`
- `cmp w5_run1.txt w5_run2.txt` -> identical (no output).
- SHA-256 (both runs, and evidence copy):
  `0e630c0cd85cb53883e2fae1aeee5a577215d89af3b3e30326522110fcd1a4ee`

## Score
- `python3 wild/w5/score_w5.py ~/workspace/scratch_wildb3/w5_run1.txt` -> exit 0.
- Independent Python mirror re-simulates all three phases from the tape and
  agrees with the instrument on every printed number.

## Tape
- `pam/round3/m1/m1_cases.txt`
  SHA-256 `5d4160d1e1a06c8250376bc85367981722fe0002296ae168c581c8353322c611`
  (canonical frozen tape; verified before build).
