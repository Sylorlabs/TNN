# NAMECHECK: L2-ESS-COMPOSE2 (operator standing x [6,2,4] composition)

Worker: L2-ESS-COMPOSE2 subagent (depth 2/2), 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/l2_ess_compose2/`
Non-ledger task (claim minting paused): wave verdict only, no ledger claim.

## Step 0: Toolchain guard (worker startup)

- Safebin activated: `export PATH="$HOME/safebin"` at startup.
- `~/safebin` contains 51 tools; grep for
  python|perl|ruby|node returns nothing.
- `which python3` under the safebin PATH returns
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
  conditions, De Morgan forms, hoisted flags.

## Scope

Reuse the L2-ESS-COMPOSE standing mechanism
BYTE-IDENTICAL (learner.zag copied from
`l2_ess_compose/`, sha256-verified) on the
L2-COMPOSE-CHAIN3B [6,2,4] world (world_H.zag copied
byte-identical from the `l2_compose_chain3b/` lane,
sha256-verified). Zero learner source changes: the
question is whether the exact standing mechanism
that transferred to [6,5,4] generalizes to the
different [6,2,4] triple (CONCRETIZE -> SUBSTITUTE
-> INVERT Form B) with its de-mismatch middle-link
discriminator.

New file: driver_H2.zag (5 arms: UNGATED /
STANDING / GLOBAL on the H-world FULL sequence;
PROB-UNG / PROB on the ESS probation world, reused
verbatim). The compose, chain3b, ess_compose, and
builder lane directories are never modified.
Commits local with explicit pathspecs; nothing
pushed.

## Key design decisions (frozen before implementation)

1. The standing learner is used BYTE-IDENTICAL to
   l2_ess_compose's learner.zag (sha256
   a7ac8a50848cd8f3ab958d844dd46f79f50eb7d9b33f93d7f127e4e9f11ff6ee,
   verified at copy time). Its base is chain3's
   learner plus the purely additive standing
   integration (diff vs chain3b's learner.zag shows
   only the standing block and gating insertions;
   zero operator-semantic changes).
2. world_H.zag is copied byte-identical from the
   l2_compose_chain3b lane (sha256
   f76b290f8aad163bf16627d792683340cd571cc56e058e4901a93e7cb71d10d0,
   verified at copy time). The l2_compose_chain3b
   lane is not merged into tnn-native-lab, so the
   copy is recorded here.
3. d_teach_maps is byte-identical between the ESS
   driver and driver_H.zag (diff-verified); the new
   driver reuses it verbatim.
4. The probation world (p_teach_initial,
   p_teach_recovery) is reused verbatim from the ESS
   driver: it tests the standing mechanism itself
   (strike -> skip -> probation -> recovery), not
   the composition chain, so it needs no [6,2,4]
   adaptation.

## Branch note

The shared main worktree (~/workspace/tnn-rsi) is
checked out on side branch lane-ma4b-20261003, not
tnn-native-lab. This worker operates in its own
worktree (~/workspace/lane-l2esscompose2-20261003,
branch lane-l2esscompose2-20261003, based on
tnn-native-lab) and lands commits on tnn-native-lab
via git plumbing (write-tree + commit-tree -p HEAD
+ update-ref with old-value check), per the
shared-workspace git discipline. Documented here
per the task's branch-issue instruction.
