# NAMECHECK.md - CLA-2 Red Team

Step 0: Toolchain guard check (mandatory, before any work).

- Guard check command: `which python3 python` returned `/usr/bin/python3`
  (system binary, cannot be removed).
- Mitigation: prepended `~/workspace/tooling_guard/bin` to PATH. That
  directory contains POSIX sh stubs named `python` and `python3` that print
  a BLOCKED message and exit 1. After prepending, `which python3` resolves
  to the stub. Any accidental invocation fails loudly instead of running.
- Commitment: no Python, python3, or other forbidden interpreter will be
  invoked for any purpose in this wave. Shell only: znc, binaries, git ops,
  file moves/copies. Zag only for any computational work.
- If a forbidden executable is invoked despite the stubs, this wave is
  PROCESS-FAIL per the standing governance ruling.

Owned path: `docs/lab/research-lead/overnight-20260928/cla2_redteam/`
Mission: adversarial audit of CLA-2 build (commit e639904f2). Read-only.
