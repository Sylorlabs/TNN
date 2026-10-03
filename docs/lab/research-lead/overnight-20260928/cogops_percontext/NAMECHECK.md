# NAMECHECK: COGOPS-PERCONTEXT

Worker: COGOPS-PERCONTEXT. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_percontext/`
Non-ledger task (claim minting paused). Builds on COGOPS-OPTIMISTIC
(`../cogops_optimistic/`, BUILD-PASS K1..K14). Implements
COGOPS-OPTIMISTIC follow-up #1 / COGOPS-COSTAWARE follow-up #2:
per-context strategy tables.

## Step 0: toolchain guard (worker startup)

- `export PATH="$HOME/safebin"` before every command.
- `$HOME/safebin` verified directly; `which python3` and
  `which python` return nothing (verified 2026-10-03, this
  session, before any work).
- Pinned znc:
  `$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (2026.07.0-dev), the single compiler for the one build.
- All computation pure Zag. Shell only for: znc invocation,
  running the binary, git operations, file assembly
  (head/cat/cmp/grep), and byte-verification (sha256sum, cmp).
  Zero forbidden-executable invocations.
- New Zag will be scanned for the `while.*!(` negated-conjunction
  pattern: must be clean. The new `strat_sel` keeps the proven
  nesting shape of the COGOPS-OPTIMISTIC version (no function
  calls inside nested conditions; cross-multiplication on hoisted
  locals); only the table address computation changes (slot base
  instead of the fixed 16600).
- Git writes via `/usr/bin/git` absolute path (safebin git symlink
  EPERM workaround per AGENTS.md), explicit pathspecs, current
  branch (`tnn-native-lab`) only, nothing pushed.

## Step 1: lane isolation

- Lane directory:
  `docs/lab/research-lead/overnight-20260928/cogops_percontext/`
- Builds on COGOPS-OPTIMISTIC: c13_base.zag will be cmp-identical
  to c12_base.zag; c13_world.zag cmp-identical to c12_world.zag;
  c13_learn.zag lines 1..1331 will be cmp-identical to
  c12_learn.zag lines 1..1331 (the frozen prefix); the additive
  section replaces the global STRATT table with a per-context
  table pool and re-wires `strat_sel`/`st_rec` through a
  learner-computed context slot; every other additive function is
  untouched. c13_main.zag is c12_main.zag with the lesion harness
  fns retargeted at context slots and the summary dump replaced by
  the per-context dump. No frozen function modified. No new goals.
  No new worlds.
