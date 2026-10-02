# NAMECHECK.md (redteam wave-20260930-1421pdt)

## Step 0 (WORKER TOOLCHAIN GUARD, mandatory)

Ran `which python3` before any research work.

- Result: `/usr/bin/python3`
- Classification: system runtime binary. The task instructions from the parent (wave coordinator) state this cannot be safely removed from PATH without breaking runtime tools, and that the coordinator has documented this. I did not attempt to remove it from PATH.
- Commitment: NEVER invoke python/python3 (or any C/C++, JS, Rust interpreter) during this wave. Shell used only for: `znc` invocations, running compiled binaries, read-only git ops (log/show/status/diff), and move/copy of files.
- Incidents so far: none.
