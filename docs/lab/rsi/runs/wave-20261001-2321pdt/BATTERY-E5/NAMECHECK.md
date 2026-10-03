# BATTERY-E5 NAMECHECK

## Step 0 (toolchain guard, 2026-10-02)

SAFEBIN-READY output from setup_safebin.sh:
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)

Exact verification:
which python3 -> rc=1 (nothing printed)
which python  -> rc=1 (nothing printed)

Pure Zag rule confirmed. Shell only for this lane.

Working copy note: the shared checkout ~/workspace/tnn-rsi was found
in a conflicted merge state on a detached old HEAD, so this lane
works in an isolated worktree ~/workspace/wt-e5 checked out at the
tnn-native-lab tip (c7f677480) on branch lane-battery-e5. No state
of the shared checkout was modified. Commits are local only, under
docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E5/.
