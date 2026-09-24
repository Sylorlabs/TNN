# W11 runlog — 2026-09-24

## Fixtures (frozen, inherited; byte-identical re-verified before build)
- `wild/w11/w11_chains.txt`: 370 chains
  (VALID 200, BROKEN_MAC 30, UNLISTED 20, OVERLONG 20, REPLAY 15,
  MID_TRUNCATE 15, FORGE_NOKEY 30, CALIB_DRIFT 40)
- Generator `wild/w11/gen_chain.py` rerun -> byte-identical (recorded in
  `wild/RESUME_WILDB3.md`).
- C3 construction audit: `wild/w11/C3_AUDIT.md` (single anchor()+extend()
  path; recorded in the fixture commit).

## Build
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (pinned build; `--no-zagd`).
- Substrate copies beside the source (sha256 module imports IO relatively):
  `R33_NATIVE_SHA256_V2.zag` (from `tnn-lab/toolchain/`),
  `R33_NATIVE_IO_V1.zag`.
- Command (cwd `pam/round4/wild/w11`):
  `znc w11_chain.zag -o ~/workspace/scratch_wildb3/w11_chain --no-zagd`
- Result: success; only the known benign A0101/A0102 warnings.
- Binary is scratch-only (NOT committed):
  `~/workspace/scratch_wildb3/w11_chain`

## Battery (2x determinism)
- `./w11_chain w11_chains.txt > w11_run1.txt`
- `./w11_chain w11_chains.txt > w11_run2.txt`
- `cmp w11_run1.txt w11_run2.txt` -> identical (no output).
- SHA-256 (both runs, and evidence copy):
  `690543d07c4ccdee2fae34e03c8e4dd8599eb399dcc436007a10416447dbb789`

## Score
- `python3 wild/w11/score_w11.py ~/workspace/scratch_wildb3/w11_run1.txt`
  -> exit 0. All 370 dispositions match independent Python hmac/sha256
  recomputation in the frozen check order.

## Build note (fixed during build, not a prereg change)
- First build hardcoded CALIB_REG as 3235823633 (wrong); corrected to
  0xC0FFEE11 = 3237998097. The error was caught by the scorer mirror
  (200 VALID chains mis-rejected) before any evidence was taken; no
  battery output from the buggy build was kept.
