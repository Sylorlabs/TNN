# NAMECHECK: CLA-2 Binary Rebuild

Step 0: Toolchain guard check.

- `which python3 python` returned: `/usr/bin/python3`
- `/usr/bin` also holds git, sha256sum, and other essential tools.
  Surgical PATH removal is not possible without breaking git operations.
- Documented: python3 will NOT be invoked for any purpose during this wave.
- Allowed: znc (pinned compiler), shell builtins, git, sha256sum, file moves.
- If a forbidden executable is invoked, this wave is PROCESS-FAIL.

Task: Rebuild cla2_bin from committed source (Finding F1 from red team).
Source is frozen. Binary only. No source modifications.

## Rebuild verification

- Source: docs/lab/research-lead/overnight-20260928/cla2_build/cla2.zag (unmodified)
- Compiler: src/tools/toolchain/znc_linux_x86_64_abed8aa1 (pinned)
- Fresh binary: 116799 bytes (matches red team expectation)
- SHA-256: 74c125c7356cdb5285f4f67a94530e70a7d5cc38948d03b6e47542fdb371f26d
- Tests: SELF-TESTS PASSED: 15/15 (all 8 original + 7 amendment tests)
- Stale binary replaced. Source untouched.

Verdict: CLA2-BINARY-REBUILT.
