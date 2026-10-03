# NAMECHECK: COGOPS-OPTIMISTIC

Worker: COGOPS-OPTIMISTIC. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_optimistic/`
Non-ledger task (claim minting paused). Builds on COGOPS-COSTAWARE
(`../cogops_costaware/`, BUILD-PASS K1..K13). Implements
COGOPS-COSTAWARE follow-up #1: optimistic efficiency
((w+1)/(c+1)).

## Step 0: toolchain guard (worker startup)

- Ran `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`:
  NOT FOUND in this checkout (same finding as the predecessor
  workers). Fallback: `$HOME/safebin` exists directly.
- `export PATH="$HOME/safebin"` before every command.
- `$HOME/safebin` verified directly: 49 entries, no `python3`, no
  `python`. `which python3` and `which python` return nothing before
  and after every build/run.
- Pinned znc: `$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (2026.07.0-dev), the single compiler for the one build.
- All computation pure Zag. Shell only for: znc invocation, running
  the binary, git operations, file assembly (head/cat/cmp/grep),
  and byte-verification (sha256sum, cmp). Zero forbidden-executable
  invocations.
- New Zag scanned for the `while.*!(` negated-conjunction pattern:
  clean (the new `strat_sel` contains no `!` at all). The
  replacement keeps the exact nesting shape of the proven
  COGOPS-COSTAWARE version (tried==0 / best!=0 / c1>0 / c3>0 /
  == on hoisted locals; no function calls inside nested
  conditions); only the compared terms change
  ((w+1)*(c2+1) vs (w2+1)*(c1+1)).
- Git writes via `/usr/bin/git` absolute path (safebin git symlink
  EPERM workaround per AGENTS.md), explicit pathspecs, current
  branch (`tnn-native-lab`) only, nothing pushed.

## Step 1: lane isolation

- Lane directory: `docs/lab/research-lead/overnight-20260928/cogops_optimistic/`
- Builds on COGOPS-COSTAWARE: c12_base.zag will be cmp-identical
  to c11_base.zag; c12_learn.zag lines 1..1331 will be
  cmp-identical to c11_learn.zag lines 1..1331 (the frozen
  prefix); the additive section differs from c11's in exactly
  one function (`strat_sel`: optimistic efficiency instead of
  pure efficiency); c12_world.zag is c11_world.zag plus one goal
  constructor (mk_goal825_E3, same structure as mk_goal820_E0,
  fresh tag); c12_main.zag is c11_main.zag plus the S14 stage,
  the S12 lesion retied on optimistic efficiency, the S13
  lesion harness fn kept with updated comments, and a new S14
  lesion harness fn. No frozen function modified.
