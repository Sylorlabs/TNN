# NAMECHECK: COGOPS-EXPECTEDCOST

Worker: COGOPS-EXPECTEDCOST. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_expectedcost/`
Non-ledger task (claim minting paused). Builds on COGOPS-PERCONTEXT
(`../cogops_percontext/`, BUILD-PASS K1..K14). Implements
COGOPS-PERCONTEXT follow-up #3: expected-cost strategy selection
(replacing optimistic efficiency (w+1)/(c+1) argmax with expected
cost (c+2)/(u+2) argmin within the current context's table).

## Step 0: toolchain guard (worker startup)

- `export PATH="$HOME/safebin"` before every command.
- `$HOME/safebin` verified directly; `which python3` and
  `which python` return nothing (verified 2026-10-03, this
  session, before any work).
- Pinned znc:
  `$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (2026.07.0-dev), the single compiler for the one build
  (byte-identical to the tnn-rsi copy per `cmp`, 8337204 bytes).
- All computation pure Zag. Shell only for: znc invocation,
  running the binary, git operations, file assembly
  (head/cat/tail/cmp/grep/wc/sha256sum), and byte-verification.
  Zero forbidden-executable invocations.
- New Zag will be scanned for the `while.*!(` negated-conjunction
  pattern: must be clean. The new `strat_sel` keeps the proven
  nesting shape of the COGOPS-PERCONTEXT version (no function
  calls inside nested conditions; exact integer
  cross-multiplication on hoisted locals); only the score terms
  change ((c+2)/(u+2) argmin instead of (w+1)/(c+1) argmax).
- Git writes via `/usr/bin/git` absolute path (safebin git symlink
  EPERM workaround per AGENTS.md), explicit pathspecs, current
  branch (`tnn-native-lab`) only, nothing pushed.

## Step 1: lane isolation

- Lane directory:
  `docs/lab/research-lead/overnight-20260928/cogops_expectedcost/`
- Builds on COGOPS-PERCONTEXT: c14_base.zag will be cmp-identical
  to c13_base.zag; c14_world.zag cmp-identical to c13_world.zag;
  c14_learn.zag lines 1..1331 will be cmp-identical to
  c12_learn.zag lines 1..1331 (the frozen prefix); the additive
  section is c13's with ONLY `strat_sel` (and its header comment)
  replaced by the expected-cost rule; c14_main.zag is c13_main.zag
  with comment-only updates (verified by comparing non-comment
  lines); every other additive function is untouched. No new
  goals. No new worlds. The only frozen-additive function whose
  behavior changes is `strat_sel` itself (the selection rule under
  test).
