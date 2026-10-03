# NAMECHECK: COGOPS-COSTAWARE

Worker: COGOPS-COSTAWARE. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_costaware/`
Non-ledger task (claim minting paused). Builds on COGOPS-STRATEGY
(`../cogops_strategy/`, BUILD-PASS K1..K12).

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
  clean. The replacement `strat_sel` keeps the exact nesting shape
  of the proven COGOPS-STRATEGY version (only the compared columns
  change: wins/cost instead of wins/uses); if-nesting depth
  unchanged.
- Git writes via `/usr/bin/git` absolute path (safebin git symlink
  EPERM workaround per AGENTS.md), explicit pathspecs, current
  branch (`tnn-native-lab`) only, nothing pushed.

## Step 1: lane isolation

- Lane directory: `docs/lab/research-lead/overnight-20260928/cogops_costaware/`
- Builds on COGOPS-STRATEGY: c11_base.zag is cmp-identical to
  c10_base.zag; c11_learn.zag lines 1..1331 are cmp-identical to
  c10_learn.zag lines 1..1331 (the frozen c8 prefix); the additive
  section differs from c10's in exactly one function (`strat_sel`:
  efficiency instead of win-rate); c11_world.zag is c10_world.zag
  plus one goal constructor (mk_goal824_E2, same structure as
  mk_goal821_E1, fresh tag); c11_main.zag is c10_main.zag plus the
  S13 stage, the S12 lesion retied on efficiency, and the S13
  lesion harness fn. No frozen function modified.
