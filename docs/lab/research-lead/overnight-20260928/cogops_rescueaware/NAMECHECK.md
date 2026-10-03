# NAMECHECK: COGOPS-RESCUEAWARE

Worker: COGOPS-RESCUEAWARE. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_rescueaware/`
Non-ledger task (claim minting paused). Builds on
COGOPS-EXPECTEDCOST (`../cogops_expectedcost/`, BUILD-PASS
K1..K14). Implements COGOPS-EXPECTEDCOST follow-up #1:
rescue-aware expected-cost strategy selection
(E[turn] + P(fail)*E[rescue], P(success) does NOT cancel).

## Step 0: toolchain guard (worker startup)

- `export PATH="$HOME/safebin"` before every command.
- `$HOME/safebin` verified directly; `which python3` and
  `which python` return nothing (verified 2026-10-03, this
  session, before any work).
- Pinned znc:
  `$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (2026.07.0-dev), the single compiler for the one build.
- All computation pure Zag. Shell only for: znc invocation,
  running the binary, git operations, file assembly
  (head/cat/tail/cmp/grep/wc/sha256sum), and byte-verification.
  Zero forbidden-executable invocations.
- New Zag will be scanned for the `while.*!(` negated-conjunction
  pattern: must be clean. The new `strat_sel` keeps the proven
  nesting shape of the COGOPS-EXPECTEDCOST version (no function
  calls inside nested conditions; exact integer
  cross-multiplication on hoisted locals); only the score terms
  change (N_s/(u_s+2) with N_s=(c+2)(rc+2)+(f+1)(rt+2) instead
  of (c+2)/(u+2)). Rescue hooks (`rescue_finalize`,
  `slog_*` counting, `det_handle` open/finalize) use the same
  flat flag pattern; no new deep nesting.
- Git writes via `/usr/bin/git` absolute path (safebin git symlink
  EPERM workaround per AGENTS.md), explicit pathspecs, current
  branch (`tnn-native-lab`) only, nothing pushed.

## Step 1: lane isolation

- Lane directory:
  `docs/lab/research-lead/overnight-20260928/cogops_rescueaware/`
- Builds on COGOPS-EXPECTEDCOST: c15_base.zag will be cmp-identical
  to c14_base.zag; c15_world.zag cmp-identical to c14_world.zag;
  c15_learn.zag lines 1..1331 will be cmp-identical to
  c12_learn.zag lines 1..1331 (the frozen prefix); the additive
  section is c14's with the selection rule replaced by the
  rescue-aware score plus the rescue-ledger machinery (global
  cells 16680/16684, transient 16688/16692, `rescue_finalize`,
  `slog_cmp`/`slog_ncmp` rescue counting, `det_handle`
  open/finalize hooks); c15_main.zag is c14_main.zag with
  comment updates plus one added `RESCUE total=<rt> count=<rc>`
  summary line (verified by diffing non-comment lines); every
  other additive function is untouched. No new goals. No new
  worlds. Lesion cell values unchanged.
- Apparatus characterization (NOT implementation): a trajectory
  probe (/tmp/probe823, built from frozen c14 sources with the
  S12 stage replaced by pass-0/1/2 snapshot printing) measured
  goal 823's frozen pass-0 snapshots to ground the preregistered
  S12 NCMP eq values. The probe implements no selection or
  rescue logic; the world is frozen and not under test. Kill
  bars K4/K9/K15/K16 still genuinely discriminate the
  selection hypothesis.
