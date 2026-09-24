# W7 runlog — 2026-09-24

## Fixtures (frozen, verified before build)
- `wild/w7/launder_signals.txt`
  SHA-256 `9024f08ebfaea55b3ace6689ada04697e998b550d4367b65d30fb04c3310ce2b`
- `wild/w7/launder_truth.txt`
  SHA-256 `5adc617c3e667d928c925b5b0c4468ec6338cf1eb799ab29241b1dcdcf43a34a`
- Both match `wild/tape/TAPE_W7_ADDENDUM.md`. Instrument never reads the
  truth file (not taken as an argument; KB-W7-L audit in scorer).

## Build
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (pinned build; `--no-zagd`).
- Command (cwd `pam/round4/wild/w7`, IO module copied beside source):
  `znc w7_hunter.zag -o ~/workspace/scratch_wildb3/w7_hunter --no-zagd`
- Result: success; only the known benign A0101/A0102 warnings.
- Binary is scratch-only (NOT committed):
  `~/workspace/scratch_wildb3/w7_hunter`

## Battery (2x determinism)
- `./w7_hunter launder_signals.txt > w7_run1.txt`
- `./w7_hunter launder_signals.txt > w7_run2.txt`
- `cmp w7_run1.txt w7_run2.txt` -> identical (no output).
- SHA-256 (both runs, and evidence copy):
  `fa92249940f79b60cdc38f545012bf95baa6d99c0975163f25f724d62401ca76`

## Score
- `python3 wild/w7/score_w7.py ~/workspace/scratch_wildb3/w7_run1.txt` -> exit 0.
- Recomputes all 200 suspicions from the signals file (200/200 match),
  joins truth, evaluates bars, runs the KB-W7-L source audit, D-W7-1..3.
