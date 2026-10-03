# NAMECHECK: L2-ESS-CURRICULUM

Worker: L2-ESS-CURRICULUM-RETRY subagent (depth 2/2), 2026-10-03.
Lane: docs/lab/research-lead/overnight-20260928/l2_ess_curriculum/
Non-ledger task (claim minting paused).

## Step 0: toolchain guard

- Safebin mandatory. Worker runs with `export PATH="$HOME/safebin"`.
- Verification (2026-10-03): `which znc` -> `/home/hatch/safebin/znc`;
  `which python3` -> nothing (does not resolve). 51 tools in safebin.
- All research logic in pure Zag, compiled with the pinned znc.
  Shell only for: invoking znc, running the binary, sha256sum,
  grep/wc text checks on trace output, git ops, file moves.
- If a forbidden executable is invoked, this wave is automatically
  PROCESS-FAIL per the worker toolchain guard.
- No em/en dashes in loop documentation. Commits local with explicit
  pathspecs; never pushed.

## Commit-order self-check

- PREREG.md (+ this NAMECHECK.md) committed alone first; no
  implementation, no kill-bar numbers, no trace text existed at that
  commit. Implementation (learner.zag, world.zag, driver.zag) written
  only after the prereg commit. REPORT.md written last.
