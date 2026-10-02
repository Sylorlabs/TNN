# NAMECHECK.md - sensory worker wave-20260930-1421pdt

## Step 0 (WORKER TOOLCHAIN GUARD, mandatory)

- `which python3` => `/usr/bin/python3` (system runtime binary; removing from PATH would break runtime tools; coordinator has documented this exception).
- Worker will NEVER invoke python3/python, nor any C/C++, JS, Rust interpreter.
- All computational research logic: pure Zag only. Shell only: invoke znc, run compiled binaries, git ops (read-only), move/copy files.
- Python invocation status this wave: NONE. PROCESS-FAIL not triggered.
