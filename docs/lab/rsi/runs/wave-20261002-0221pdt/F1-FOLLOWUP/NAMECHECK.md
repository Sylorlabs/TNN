# NAMECHECK.md - F1-FOLLOWUP lane, wave-20261002-0221pdt

Lane: F1-FOLLOWUP (greedy-trial seed-sensitivity as a separate constructor finding).
Branch: tnn-native-lab. Working copy: ~/workspace/tnn-rsi.
Task: file the RT-EXEC-recommended separate constructor finding as a NEW
candidate (not a verdict change on F1's BUILD-FAIL, which stands untouched).

## Step 0 (toolchain guard)

- 2026-10-02 ~02:45 PDT: ran
  `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`;
  output: SAFEBIN-READY, 36 tools, znc OK
  (src/tools/toolchain/znc_linux_x86_64_abed8aa1).
- `export PATH="$HOME/safebin"` in every shell used by this lane.
- `which python3` prints nothing; `which python` prints nothing.
  Verified again after safebin activation in the same shell.
- PURE ZAG ONLY: implementation, harnesses, verifiers, scorers, fixture
  provisioning, and analysis are pure Zag compiled by the pinned znc, or
  shell invoking znc, running binaries, git ops, cmp/sha256sum, grep, and
  file moves/copies. No Python anywhere in this lane.
- Any forbidden-executable invocation is automatic PROCESS-FAIL and will
  be disclosed immediately. Zero such invocations to date.
- Dash scans via
  docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.
  Zero em/en dashes in loop docs.

## Commit log (this lane only)

- d7164c12b prereg commit: PREREG_F1FOLLOWUP.md + NAMECHECK.md alone.
- 742081f93 methodology commit: dev/ (generator/scorer sources and
  binaries, f1f_analyze.zag and binary, run scripts), METHODOLOGY.md.
  NOTE: this commit inadvertently swept in staged ARENA-lane files
  from another worker; disclosed in REDTEAM_SELF.md Attack 6. ARENA
  working copies intact, match HEAD.
- a920ba752 fixture commit: sealed/ fixtures + FIXTURE_SHA256.txt,
  ncharness/ (NC-HARNESS PASS record). Lane-only (pathspec-limited).
- (pending) sealed eval commit: runs/, analysis/, SEALED_EVAL.md,
  REDTEAM_SELF.md, dev/f1f_diag.zag + binary (post-hoc diagnostic).

## Read-only inputs (never modified)

- docs/lab/rsi/runs/wave-20261001-2321pdt/RT-EXEC/RT-EXEC_REVIEW.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/F1/ (PREREG_TRIG.md,
  JUDGE_BRIEF.md, IMPLEMENTATION.md, SEALED_EVAL.md, impl/f1_learn)
- docs/lab/rsi/runs/wave-20261001-2321pdt/F1-FOLLOWUP/ (PREREG_PART1.md,
  PREREG_PART2.md, JUDGE_BRIEF.md, SEALED_EVAL_PART2.md, dev/, sealed2/)
