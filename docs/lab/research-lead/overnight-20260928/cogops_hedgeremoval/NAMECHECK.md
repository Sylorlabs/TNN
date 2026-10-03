# NAMECHECK: COGOPS-HEDGEREMOVAL

Worker: COGOPS-HEDGEREMOVAL. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_hedgeremoval/`
Non-ledger task (claim minting paused). Builds on
COGOPS-PESSIMISTIC (`../cogops_pessimistic/`, mechanism bars
K1-K11/K13-K16 PASS, K12 BUILD-FAIL on two worker-side
prediction/assembly errors). Implements COGOPS-PESSIMISTIC
follow-up #2: hedge-removal variant (the one experiment that
could actually price S8's ALT tax; P0 shows the prior alone
cannot).

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
  (head/cat/tail/cmp/grep/wc/sha256sum/diff), and
  byte-verification. Zero forbidden-executable invocations.
- New Zag will be scanned for the `while.*!(` negated-conjunction
  pattern: must be clean. The change to `strat_sel` is
  deletion of the trailing evidence-gated hedge block; the
  proven argmin nesting shape is untouched; no new deep
  nesting.
- Git writes via `/usr/bin/git` absolute path (safebin git symlink
  EPERM workaround per AGENTS.md), explicit pathspecs, current
  branch (`tnn-native-lab`) only, nothing pushed.

## Step 1: lane isolation

- Lane directory:
  `docs/lab/research-lead/overnight-20260928/cogops_hedgeremoval/`
- Builds on COGOPS-PESSIMISTIC: c17_base.zag will be cmp-identical
  to c16_base.zag; c17_world.zag cmp-identical to c16_world.zag;
  c17_learn.zag lines 1..1331 will be cmp-identical to
  c12_learn.zag lines 1..1331 (the frozen prefix); the additive
  section is c16's with the evidence-gated hedge block in
  `strat_sel` DELETED (the `if(tried==0){...}` region that
  re-promotes to ALT=4 on a PW/NEED score tie with in-context
  evidence) plus header comments; the (c+8) pessimistic N-term
  constants stay; c17_main.zag is c16_main.zag with comment
  updates only; rescue ledger machinery, P(fail)/E[rescue],
  worlds, goals, lesions all unchanged. No new goals. No new
  worlds.
- Apparatus characterization (NOT implementation): a trajectory
  probe (/tmp/probe_hr_bin, ephemeral, built from frozen c16
  sources with main replaced by S1A..S7 prefix + pass-0..5
  snapshot printing for goal 823) measured eq(2,0)=0,
  eq(2,1)=0, eq(3,1)=0, eq(3,0)=0, per-need eq(4,2)=[1,1,1,0],
  eq(4,3)=[1,0,0,0], eq(5,3)=[1,1,1], and trajectory phases at
  passes 2,3 identical to S7's, grounding the S8 cascade
  prediction (PW fail / WHOLE fail / NEED wins at pass 4).
  The probe implements no selection, prior, hedge, or rescue
  logic; the worlds are frozen and not under test. Kill bars
  K4/K9/K10/K11/K15/K16 still genuinely discriminate the
  hedge-removal hypothesis.
