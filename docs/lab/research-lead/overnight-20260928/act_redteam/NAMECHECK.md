# ACT Red Team NAMECHECK

Step 0: Toolchain guard check (executed before any other work).

- Command: `which python3 python 2>/dev/null`
- Result: `/usr/bin/python3` present. No `python` binary.
- `/usr/bin/python3` is a system binary; it cannot be removed from PATH
  without also breaking other tools in /usr/bin (git, sha256sum, grep,
  etc.), so surgical PATH removal is not technically possible here.
- Documented: this worker will NOT invoke python3, python, node, or any
  other forbidden interpreter for any purpose. Shell only: znc, run
  binaries, git ops, move/copy files.
- If a forbidden executable is invoked, this wave is PROCESS-FAIL.

Date: 2026-09-30. HEAD at start: 323f2afaa.
