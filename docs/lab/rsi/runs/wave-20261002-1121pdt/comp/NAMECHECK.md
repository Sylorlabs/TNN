# NAMECHECK.md - lane COMP, wave-20261002-1121pdt

Worker: lane-comp-20261002-1121pdt. Worktree: ~/workspace/tnn-rsi-work/wave-20261002-1121pdt/comp/

## Step 0: toolchain guard (recorded first, 2026-10-02)

Setup command run:
  bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
Literal tail output:
  linked: 36 tools
  znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
  verify: python3 absent from safebin PATH (OK)
  verify: python absent from safebin PATH (OK)
  SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)

With PATH="$HOME/safebin":
  `which python3` -> (nothing; exit code 1). RESOLVES TO NOTHING: PASS.
  `which python`  -> (nothing; exit code 1). RESOLVES TO NOTHING: PASS.
  `which znc`    -> /home/hatch/safebin/znc (exit code 0). SAFEBIN PATH: PASS.

Conclusion: guard ok with literal evidence recorded above. All research logic in this lane is pure Zag; shell used only for toolchain invocation, git ops, file moves.

## Provenance notes

- The prior 0821pdt lane branch (lane-comp-20261002-0821pdt) was consulted for provenance only; this wave's state is built fresh under a frozen prereg committed before any implementation.
- 0521pdt COMP record (docs/lab/rsi/runs/wave-20261002-0521pdt/COMP/) supplies the frozen prereg, implementation, sealed-eval record, and run_a1.txt for the unified `satisfy` composition operation; verdict BUILD-PASS with KB6 PARTIAL on the trial-path confound, no L3 claims permitted.
- 0821pdt queue item 1 (F1 re-freeze and re-run, FINDING CONFIRMED at 655c8d7d6 on lane-f1-20261002-0821pdt) is read-only reference only.
