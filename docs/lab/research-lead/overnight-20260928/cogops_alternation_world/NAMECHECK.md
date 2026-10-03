# NAMECHECK: COGOPS-ALTERNATION-WORLD

Worker: COGOPS-ALTERNATION-WORLD. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_alternation_world/`
Non-ledger task (claim minting paused). Builds on
COGOPS-HEDGEREMOVAL (`../cogops_hedgeremoval/`, c17 sources,
BUILD-PASS 16/16). Implements the COGOPS-HEDGEREMOVAL
follow-up: "A world genuinely rewarding alternation (PW and
NEED each half-right, ALT strictly best) would test if the
hedge is ever beneficial; none exists in this battery."

## Step 0: toolchain guard (worker startup)

- `export PATH="$HOME/safebin"` before every command.
- `$HOME/safebin` verified directly; `which python3` and
  `which python` return nothing (verified 2026-10-03, this
  session, before any work).
- Pinned znc:
  `$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (2026.07.0-dev), the single compiler for the two builds.
- All computation pure Zag. Shell only for: znc invocation,
  running the binaries, git operations, file assembly
  (head/cat/tail/cmp/grep/wc/sha256sum/diff), and
  byte-verification. Zero forbidden-executable invocations.
- New Zag (3 goal constructors + driver stages) will be
  scanned for the `while.*!(` negated-conjunction pattern:
  must be clean. No new deep nesting (constructors are flat
  w_* call sequences; driver stages mirror c17's).
- Git writes via `/usr/bin/git` absolute path (safebin git
  symlink EPERM workaround per AGENTS.md), explicit
  pathspecs, current branch (`tnn-native-lab`) only, nothing
  pushed.

## Step 1: lane isolation

- Lane directory:
  `docs/lab/research-lead/overnight-20260928/cogops_alternation_world/`
- Builds on COGOPS-HEDGEREMOVAL: c18_base.zag will be
  cmp-identical to c17_base.zag; c18_world.zag will be
  c17_world.zag PLUS three appended goal constructors
  (lines 1..594 cmp-identical); c18_learn.zag /
  c18h_learn.zag lines 1..1331 will be cmp-identical to
  c12_learn.zag lines 1..1331 (the frozen prefix).
- TWO binaries from one lane, differing ONLY in the
  additive strategy section:
  - c18 (no hedge): c18_strat_additive.zag =
    c17_strat_additive.zag (evidence-gated hedge DELETED).
  - c18h (with hedge): c18h_strat_additive.zag =
    c16_strat_additive.zag (evidence-gated hedge PRESENT).
  - One driver: c18_main.zag, used for both builds.
- New worlds/goals (all in world F, 613-oscillator):
  - Goal 830 (PW-world): 3 needs [carrier, 613-osc,
    614-verify], whole-state lag-2 oscillation, context
    (3,613). PW wins efficiently.
  - Goal 831 (NEED-world): 4 needs [carrier, 613-osc,
    614-verify, 604-drifter], partial oscillation, context
    (4,613). PW fails, WHOLE fails, NEED wins.
  - Goal 832 (TEST-world): same structure as 831, fresh
    tag, context (4,613). PW/NEED tie -> hedge
    discriminates.
- Setup stages S1A/S1B/S2/S4/S6L/S6B copied verbatim from
  c17_main.zag (detection stages S3/S5/S7..S14 dropped).
  Code inspection (this session): detection (det_handle)
  never writes ret/vfy coverage (L[0..67], L[4248..]),
  buckets, or specialization state; ret_log_rel /
  vfy_log_rel are called only by ret_episode / vfy_episode.
  Hence the setup-stage output blocks are byte-identical to
  c17_run1.txt's (K11 checks this).
- Kill bars K4/K5/K6 genuinely discriminate the hedge:
  with-hedge S_TEST must show chosen=4 / 6 events /
  ledger (6,2); no-hedge S_TEST must show chosen=1 /
  8 events / ledger (12,4).
