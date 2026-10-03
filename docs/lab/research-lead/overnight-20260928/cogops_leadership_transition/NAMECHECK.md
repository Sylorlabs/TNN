# NAMECHECK: COGOPS-LEADERSHIP-TRANSITION

Worker: COGOPS-LEADERSHIP-TRANSITION. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_leadership_transition/`
Non-ledger task (claim minting paused). Builds on
COGOPS-HEDGE-FREQUENCY (`../cogops_hedge_frequency/`, c19/c19h
sources, BUILD-PASS 9/9). Investigates leadership-transition
dynamics: under what world dynamics do strategy-selection
leadership transitions occur, and how often do exact ties
(the hedge's firing precondition) arise at transitions.

## Step 0: toolchain guard (worker startup)

- `export PATH="$HOME/safebin"` before every command.
- `$HOME/safebin` verified directly (49 tools);
  `which python3` and `which python` return nothing
  (verified 2026-10-03, this session, before any work).
- Pinned znc:
  `$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (2026.07.0-dev), the single compiler for all builds.
- All computation pure Zag. Shell only for: znc invocation,
  running the binaries, git operations, file assembly
  (head/cat/cp/cmp/grep/wc/sha256sum/diff), and
  byte-verification. Zero forbidden-executable invocations.
- New Zag (1 world-add file with kind-8 goal constructor,
  1 driver, strat instrumentation of exactly 1 added det_ev
  line for tie-masks) will be scanned for the
  `while.*!(` negated-conjunction pattern: must be clean.
  No new deep nesting (constructor branches are flat w_*
  sequences; driver stages are straight-line calls).
- Git writes via `/usr/bin/git` absolute path (safebin git
  symlink EPERM workaround per AGENTS.md), explicit
  pathspecs, current branch (`tnn-native-lab`) only, nothing
  pushed.

## Step 1: lane isolation

- Lane directory:
  `docs/lab/research-lead/overnight-20260928/cogops_leadership_transition/`
- Builds on COGOPS-HEDGE-FREQUENCY: c20_base.zag will be
  cmp-identical to c19_base.zag; c20_world_add.zag extends
  c19_world_add.zag with kind 8 (unwinnable, context
  (3,613)); c20h_learn.zag = c12_learn.zag head (1331 lines)
  + c20h_strat_additive.zag (c19h strat verbatim + 1
  log-only det_ev line for the argmin tie mask, kind 12).
- One binary only: c20h (hedge-bearing + instrumented).
  No hedge-deleted variant: the transition study measures
  the hedge's precondition, it does not re-price deletion.
- Probe binary (c20probe, throwaway, /tmp outputs only)
  used pre-prereg ONLY to validate the kind-8 trajectory
  model (that kind 8 is genuinely unwinnable by all four
  forms). The probe changes no frozen files and its outputs
  never enter the battery evidence.

## Step 2: determinism contract

- 3/3 byte-identical runs per binary (sha256), stderr empty.
- Frozen predictions file committed with the prereg;
  K-bar verification by byte/grep comparison only.

## Step 3: prereg discipline

- PREREG.md + c20_stages_predicted.txt committed ALONE
  (one commit, explicit pathspec) before any c20
  implementation file exists in the lane.
- Kill bars must discriminate: each bar names a frozen
  prediction that the battery can falsify.
