# NAMECHECK.md - FORK lane, wave-20261002-1121pdt

Wave: wave-20261002-1121pdt. Lane: FORK. Branch: lane-fork-20261002-1121pdt.
Worktree: ~/workspace/tnn-rsi-work/wave-20261002-1121pdt/fork/ (sparse: src/, docs/lab/rsi/runs/wave-20261002-1121pdt/fork/, wave-20261002-0821pdt dir, safebin_setup, worker_snippets).
Lane branch tip at start: 0296167f0 WATCHDOG: ledger C290 (LW2 bf523af0b/229a6baca, invention regress). Local only, never pushed.
Standing rules read: docs/lab/rsi/runs/wave-20261002-1121pdt/NAMECHECK.md (coordinator level).

## Step 0: toolchain guard (2026-10-02, recorded first)

- Ran: bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
  Output: safebin: /home/hatch/safebin; linked: 36 tools; znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1); verify: python3 absent from safebin PATH (OK); verify: python absent from safebin PATH (OK); SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
- export PATH="$HOME/safebin"
- `which python3` -> (nothing; exit code 1)
- `which python` -> (nothing; exit code 1)
- `which znc` -> /home/hatch/safebin/znc
- GUARD PASS: python3/python do not resolve in PATH; znc resolves to the safebin path. Pure Zag only for all battery work this wave.

## Scope note

This lane runs the frozen test battery against EVERY branch and fork tip (local branches, remote branches, detached-HEAD forktest worktrees). If a fork cannot build under the pinned znc or requires Python, it is reported UNTESTABLE-UNDER-GUARD; no workarounds.

## Red lines acknowledged

No spend, no publish, no contacting outsiders, no purchases/bookings, no irreversible commitments, never git push, never Google Drive. Commits only to lane-fork-20261002-1121pdt with pathspec limited to lane dirs. Never rebase; never git reset --hard. Do not write into scaling_5000_fixed or scaling_10000 dirs; do not disturb worktrees at ~/workspace/tnn-rsi-wave3/forktest/*, ~/workspace/tnn-rsi-wt-exp1, ~/workspace/tnn-rsi-wt-exp2, ~/workspace/tnn-rsi-wt-s5fix, ~/workspace/tnn-rsi-wt-sensory, ~/workspace/wt-e5.
