# NAMECHECK: COGOPS-PESSIMISTIC

Worker: COGOPS-PESSIMISTIC. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_pessimistic/`
Non-ledger task (claim minting paused). Builds on
COGOPS-RESCUEAWARE (`../cogops_rescueaware/`, mechanism bars
K1-K11/K13-K16 PASS, K12 BUILD-FAIL on a transcription slip).
Implements COGOPS-RESCUEAWARE follow-up #2: pessimistic
turn-cost prior (the one untested variant that could actually
price S8's tax).

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
  pattern: must be clean. The change to `strat_sel` is three
  `(c+2)` -> `(c+8)` constants in the N-term computations; the
  proven nesting shape is untouched; no new deep nesting.
- Git writes via `/usr/bin/git` absolute path (safebin git symlink
  EPERM workaround per AGENTS.md), explicit pathspecs, current
  branch (`tnn-native-lab`) only, nothing pushed.

## Step 1: lane isolation

- Lane directory:
  `docs/lab/research-lead/overnight-20260928/cogops_pessimistic/`
- Builds on COGOPS-RESCUEAWARE: c16_base.zag will be cmp-identical
  to c15_base.zag; c16_world.zag cmp-identical to c15_world.zag;
  c16_learn.zag lines 1..1331 will be cmp-identical to
  c12_learn.zag lines 1..1331 (the frozen prefix); the additive
  section is c15's with exactly three `(c+2)` -> `(c+8)`
  constants in `strat_sel`'s N computations (main loop, hedge
  n1, hedge n3) plus header comments; c16_main.zag is
  c15_main.zag with comment updates only; rescue ledger
  machinery, P(fail)/E[rescue], hedge structure, worlds, goals,
  lesions all unchanged. No new goals. No new worlds.
- Apparatus characterization (NOT implementation): a trajectory
  probe (/tmp/probe_traj_bin, ephemeral, built from frozen c15
  sources with main replaced by pass-0..5 snapshot printing)
  measured goal 824 eq(2,0)=0 eq(2,1)=0 eq(3,1)=0 eq(3,2)=0
  eq(3,0)=1 eq(4,1)=1 and goal 825 eq(2,0)=1 eq(2,1)=0
  eq(3,1)=1, reproducing all RA-verified values exactly and
  grounding the two new predictions eq24(2,1)=0, eq25(2,1)=0.
  The probe implements no selection, prior, or rescue logic;
  the worlds are frozen and not under test. Kill bars K4/K9/
  K10/K11/K15/K16 still genuinely discriminate the selection
  hypothesis.
