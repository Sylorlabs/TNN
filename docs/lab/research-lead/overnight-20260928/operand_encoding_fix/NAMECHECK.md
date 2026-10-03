# NAMECHECK.md -- Operand-encoding fix lane (oe_* workstream)

## Step 0: Toolchain guard (2026-10-02)

Executed at worker start, before any other work:

```
export PATH="$HOME/safebin"
which python3; which python; echo "guard-check-done"
```

Required result: both `which` commands return NOTHING (empty output before
"guard-check-done"). Safebin holds the pinned znc plus coreutils/git.
PATH is $HOME/safebin only for all worker commands.

All scientific computation in pure Zag. Shell only for: invoking znc,
running binaries, git ops, file movement. Any forbidden-executable
invocation -> this wave PROCESS-FAIL, clean re-freeze required.

## Lane scope

Operand-encoding fix only (Micah ruling 2026-10-02). New base revision:
oe_base.zag. The main L2/L3 swarm continues independently; do not block
on it and do not duplicate its work.
