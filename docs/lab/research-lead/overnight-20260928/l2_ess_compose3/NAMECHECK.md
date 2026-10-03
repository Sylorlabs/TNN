# NAMECHECK: L2-ESS-COMPOSE3 (operator standing x [6,5,4,4] composition)

Worker: L2-ESS-COMPOSE3 subagent (depth 2/2), 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/l2_ess_compose3/`
Non-ledger task (claim minting paused): wave verdict only, no ledger claim.

## Step 0: Toolchain guard (worker startup)

- Safebin activated: `export PATH="$HOME/safebin"` at startup.
- `which python3` and `which python` under the safebin PATH return
  nothing (exit 1). No python3/python available.
- Pinned compiler: `~/safebin/znc`, version
  `znc 2026.07.0-dev (edition 2026)`.
- All computational research operations in this wave
  use Zag compiled with the pinned znc. Shell is used
  only to invoke znc, run binaries, do git ops, and
  move/copy files. No forbidden executable will be
  invoked; if one ever is, this wave is automatically
  PROCESS-FAIL per the worker toolchain guard.
- znc defect workarounds from AGENTS.md honored:
  single-buffer stdout emit, no `!(A && B)` while
  conditions, De Morgan forms, hoisted flags,
  u8-backed cells, no `_zag_print` for dynamic content.

## Scope

Reuse the L2-ESS-COMPOSE standing mechanism
BYTE-IDENTICAL (learner.zag copied from the
`l2_ess_compose2/` lane, sha256-verified) on the
L2-COMPOSE-CHAIN4 [6,5,4,4] world (world_F.zag copied
byte-identical from the `l2_compose_chain4/` lane,
sha256-verified). Zero learner source changes: the
question is whether the exact per-(op,src,sig)
standing mechanism that transferred to [6,5,4] and
[6,2,4] scales to the 4-operator chain
(CONCRETIZE -> ABSTRACT -> INVERT Form A ->
INVERT Form B), where the SAME operator (op4 INVERT)
must fire twice under the same signature on two
different Z sources.

New file: driver_F3.zag (5 arms: UNGATED /
STANDING / GLOBAL on the F-world FULL sequence;
PROB-UNG / PROB on the ESS probation world, reused
verbatim). The compose, chain3b, chain4,
ess_compose, ess_compose2, and builder lane
directories are never modified. Commits local with
explicit pathspecs; nothing pushed.

## Key design decisions (frozen before implementation)

1. The standing learner is used BYTE-IDENTICAL to
   l2_ess_compose2's learner.zag (sha256
   a7ac8a50848cd8f3ab958d844dd46f79f50eb7d9b33f93d7f127e4e9f11ff6ee,
   verified at copy time). That file is itself
   byte-identical to l2_ess_compose's learner.zag:
   chain3's learner plus the purely additive standing
   integration (zero operator-semantic changes).
2. world_F.zag is copied byte-identical from the
   l2_compose_chain4 lane (sha256
   9197c57320515f2a186a9bb752cc74ff7a46b27b4240ac1c4be3b7e5b6be58a2,
   verified at copy time). It is byte-identical to
   chain3's world_E: the 44-fact world on which the
   [6,5,4] standing result was first shown.
3. d_teach_maps is byte-identical between the ESS
   driver, driver_H2.zag, and driver_F.zag
   (diff-verified); the new driver reuses it verbatim.
   d_check_z4/z5/z6/z7 are copied verbatim from
   driver_F.zag.
4. The probation world (p_teach_initial,
   p_teach_recovery) is reused verbatim from the ESS
   driver: it tests the standing mechanism itself
   (strike -> skip -> probation -> recovery), not
   the composition chain, so it needs no [6,5,4,4]
   adaptation.

## Branch note

The shared main worktree (~/workspace/tnn-rsi) is
checked out on side branch lane-ma4b-20261003, not
tnn-native-lab. This worker operates in its own
worktree (~/workspace/lane-l2esscompose2-20261003,
branch lane-l2esscompose2-20261003, based on
tnn-native-lab) and lands commits on tnn-native-lab
via git plumbing (read-tree into a private index,
write-tree, commit-tree -p tnn-native-lab HEAD,
update-ref with old-value check), per the
shared-workspace git discipline. Documented here
per the task's branch-issue instruction.
