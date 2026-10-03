# NAMECHECK: COGOPS-HEDGE-FREQUENCY

Worker: COGOPS-HEDGE-FREQUENCY. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_hedge_frequency/`
Non-ledger task (claim minting paused). Builds on
COGOPS-ALTERNATION-WORLD (`../cogops_alternation_world/`,
c18 sources, BUILD-PASS 11/11). Implements the
COGOPS-ALTERNATION-WORLD follow-up: "a natural-tie frequency
study would say how often the hedge's firing condition arises
unengineered" (REPORT.md recommended follow-up #2).

## Step 0: toolchain guard (worker startup)

- `export PATH="$HOME/safebin"` before every command.
- `$HOME/safebin` verified directly (49 tools);
  `which python3` and `which python` return nothing
  (verified 2026-10-03, this session, before any work).
- Pinned znc:
  `$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (2026.07.0-dev), the single compiler for the two builds.
- All computation pure Zag. Shell only for: znc invocation,
  running the binaries, git operations, file assembly
  (head/cat/cp/cmp/grep/wc/sha256sum/diff), and
  byte-verification. Zero forbidden-executable invocations.
- New Zag (1 world-add file with 7-kind goal constructor +
  world augmentation, 1 driver, strat instrumentation of
  exactly 2 det_ev lines) will be scanned for the
  `while.*!(` negated-conjunction pattern: must be clean.
  No new deep nesting (constructor branches are flat w_*
  sequences; driver stages are straight-line calls).
- Git writes via `/usr/bin/git` absolute path (safebin git
  symlink EPERM workaround per AGENTS.md), explicit
  pathspecs, current branch (`tnn-native-lab`) only, nothing
  pushed.

## Step 1: lane isolation

- Lane directory:
  `docs/lab/research-lead/overnight-20260928/cogops_hedge_frequency/`
- Builds on COGOPS-ALTERNATION-WORLD: c19_base.zag will be
  cmp-identical to c18_base.zag; c18_world.zag used verbatim
  (no edits); new world code ONLY in c19_world_add.zag;
  learn prefix lines 1..1331 cmp-identical to
  c12_learn.zag lines 1..1331 (the frozen prefix).
- TWO binaries from one lane, differing ONLY in the
  additive strategy section:
  - c19 (no hedge): c19_strat_additive.zag =
    c18_strat_additive.zag verbatim (hedge deleted, no
    instrumentation). The control.
  - c19h (with hedge): c19h_strat_additive.zag =
    c18h_strat_additive.zag PLUS exactly 2 det_ev lines:
    DET-HGATE (kind 11) at every initial selection,
    DET-HEDGE (kind 10) iff the hedge fires.
  - One driver: c19_main.zag (c18_main.zag helpers +
    new main + kind 10/11 dump branches).
- 26 detection stages over 7 world kinds in 4 contexts
  (tags 840-847, 850-857, 860-865, 870-873), fresh tags
  defeat outcome reuse; plan_drop after every stage keeps
  the 4-slot plan region clear; strategy tables are
  per-context so fresh tags share context history.
- Kill bars K3/K4 are verdict-branching measurement bars
  with explicit numeric branches (fires==0 / 1-2 / >=3;
  net saved >0 / ==0 / <0); K1/K2/K5/K6/K7/K8/K9 are
  pass/fail integrity bars. K4 applies iff fires >= 1.
