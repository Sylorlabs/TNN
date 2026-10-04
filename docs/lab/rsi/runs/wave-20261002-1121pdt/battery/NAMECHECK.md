# NAMECHECK.md - lane BATTERY, wave-20261002-1121pdt

Lane branch: lane-battery-20261002-1121pdt. Task: queue item 13, run
T-K5 / T-K9 / T-K11 regression bars against the current
tnn-native-lab tip.

## Step 0 (toolchain guard)

Ran at startup (2026-10-02):
```
bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
```
Setup output: `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`.
Literal verification outputs:
- `which python3` -> NOTHING (resolves to nothing; absent from safebin PATH)
- `which znc` -> /home/hatch/safebin/znc
- `znc --version` -> znc 2026.07.0-dev (edition 2026)

Guard: PASS. All lane work uses PATH=$HOME/safebin only.

## Step 0b (process record, standing rules acknowledged)

- Pure Zag only. No Python anywhere in harness, scoring, or
  analysis. A forbidden-interpreter invocation makes this lane's
  wave PROCESS-FAIL automatically.
- No em-dashes in any loop documentation; verified with
  check_no_dash.sh before each commit.
- Commits pathspec-limited to the lane worktree dirs plus
  docs/lab/rsi/runs/wave-20261002-1121pdt/battery/. Never to
  tnn-native-lab. Never push. Never rebase. No git reset --hard.
- The frozen battery directories
  docs/lab/rsi/runs/wave-20261002-0521pdt/BATTERY and
  docs/lab/rsi/runs/wave-20261002-0221pdt/BATTERY are read-only
  inputs. All run artifacts are written into this lane's run
  directory only. Original driver scripts are copied, not
  modified; the only relocation edit is the DIR= assignment in
  the copies, recorded in REPORT.md.
- Prereg commit-order self-check: this lane has no prereg of its
  own; it re-runs the frozen E10 bars. The frozen prereg
  PREREG_E10.md (SHA-256
  6d7cb92dbfe59a7622196f28bc55ac5c58c7e2c467c268b214df44fa98046952)
  predates all battery artifacts (per 0521pdt SEALED_RESULTS.md
  section 1); bar definitions are taken from its section 7 and
  are not moved.
- Pinned znc defects honored: precompiled scorer binaries
  (e10_score_bin, e10_score_m2w2_bin) are used as committed;
  no _zag_print for dynamic content anywhere in new code;
  no as *i32 + slice construction; u8 cells only; no WAV work.
