# NAMECHECK.md - F1-REPAIR lane, wave wave-20261001-2321pdt

## Step 0 (toolchain guard)

setup_safebin.sh output:
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)

Verification: `which python3` prints nothing (exit 1).
PATH exported as $HOME/safebin only.
Recorded 2026-10-01 ~23:59 PDT before any computational work.

## Pre-work audit

- Branch: tnn-native-lab, commit 257cd068a46544d27312e411f0aaa246aef02e2f
- Working copy clean at start (no uncommitted changes before new lane files).
- Lane dir: docs/lab/rsi/runs/wave-20261001-2321pdt/F1-REPAIR/
- Frozen F1 binary sha256 recorded from task:
  6f2b155b233a95ad1a8323e8565b71b5be8882847
  (will be re-verified against the extracted copy before runs)
- Tooling discipline: pure Zag for all computational research ops.
  Shell only: invoke znc, run binaries, git ops, move/copy files.
- Commit discipline: commits only under F1-REPAIR/, prereg committed
  alone before any implementation or fixture generation, no em-dashes
  (check_no_dash.sh on every doc before commit), no push, no rebase,
  no git reset --hard.
- Read-only toward F1, F1-FOLLOWUP, F1-BUFFER lane dirs: extract
  committed sources with git show only; never modify.
