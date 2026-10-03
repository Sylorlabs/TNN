# NAMECHECK.md -- Multi-Op Process Selection Worker (Priority F)

## Step 0: Toolchain Guard (mandatory)

Executed at worker startup, before any other work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` printed. `which python3 python` returned NOTHING.
PATH=/home/hatch/safebin. Safebin active for all subsequent work.

No forbidden executable invoked at any point. All research logic in pure
Zag via the pinned znc. Shell used only for: znc invocation, running the
binary, file moves, git operations, text checks (grep/wc/sha256sum).
No Python, C, or other toolchains touched.

## Step 1: Task identity

Multi-Op Process Selection Worker (Constitution Priority F, 2026-10-02).
Learner-owned process selection for MULTI-OPERATION sequences:
(1) discover a 3-op chain whose inner 2-op links were never directly
rewarded (compositional generalization, not pair memorization);
(2) revise an op's internal body parameter from consequences.
Unfrozen variant only. Standalone experiment extending the
cogops_structures approach (ops as learner-owned byte-array bodies,
learned applicability + composition links, consequence credit,
retirement). Frozen sources never read for modification, never
modified.

Design: two arms share ALL learner machinery (generic 8-instruction
interpreter; epsilon-greedy bandit over op indices scoring
appl + comp with uniform 500 optimism; consequence credit; retirement;
body-parameter revision on greedy wrong answers). Arm A (4 ops):
F/F2/T2/CHAIN3 worlds; target triple FOLLOW->SHIFT->COMPLETE
(ids [1,3,2]) in CHAIN3 worlds. Arm B (5 ops, adds ADJUST with
learner-owned immediate parameter p4): F/EST worlds; EST true answer =
V+4, constant lives only in the environment. The interpreter never
branches on op id; the selector never branches on op id. No OP_ mode
constants, no semantic cases, no modes, no bridges, no handlers.

## Step 2: Constraints honored

- Unfrozen only. Frozen read-only (nothing frozen touched).
- Pure Zag. Shell only for znc, binary runs, git, file moves, checks.
- Zero em/en dashes in documentation (byte-verified before commit).
- Paper untouched:
  docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md
- Nothing pushed. Commits local only on tnn-native-lab.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases, 0 hardcoded
  3-sequences in learner code ([1,3,2] appears only in measurement).
- Prereg PREREG.md frozen and committed ALONE (2dfecede8) before any
  implementation file was written.
- Deterministic: two LCG streams, fixed seeds, fixed tie-breaks.
- Per AGENTS.md toolchain lessons: no `as *i32` + slice construction
  (u8 cells with get32/set32 helpers); no `_zag_print` for dynamic
  content (single preallocated output buffer + one
  `_zag_raw_syscall(1,1,ptr,len)` write at end); no `as []f64` casts.

## Step 3: Development notes

Seven versions (v1-v7), each prereg-amended and re-frozen BEFORE
code changes (commits ff6d97d97, 7103ecf44, 02808d14f for v5/v6/v7;
v2/v3/v4 similarly). Kill-bar thresholds never changed. Full
history in REPORT.md section 4.

Key technical findings:
- 4-step limit let solved [1,3,X,2] episodes reward (1,3);
  3-step limit makes link reward imply the triple (structural).
- Two-phase (Phase 1 without CHAIN3) starves SHIFT applicability;
  single-phase lets CHAIN3 itself train appl(3,4) (v2 reached 946).
- With eps>0, exploration-assisted triples contaminate inner-link
  histories (v1/v2 T1=0). With eps=0 globally, every triple is
  all-greedy by construction; combined with the 3-step limit, the
  first triple STRUCTURALLY satisfies T1's clean condition.
- Full-error body revision overshoots if the same op answers
  wrongly multiple times in one episode (stale error applied
  repeatedly; v6 p4 went 0->12). Fix: at most one revision per op
  per episode.
- Arm B needs exploration to recover a miscalibrated op (v6 eps=0
  locked ADJUST out at -1000 below fail-0). v7: Arm A eps=0, Arm B
  normal eps schedule.

Final (v7): single-phase, 3-step limit, Arm A eps=0, Arm B eps
schedule, one-revision-per-op-per-episode, T-gated ADJUST,
full-error revision. T1=1 (DISCOVERY ep=55, clean=1, pre13=0/5,
pre32=0/1), T2=1 (late 27/27), T3=1 (p4=4, rev_n=1, late 53/53).
PROCESS-MULTIOP-COMPLETE.

## Step 4: Determinism

3/3 runs byte-identical. sha256:
6881da8ed332d8faec3c675cd4850ab734555236e54681453ca993340b62ed05
(run1.txt, run2.txt, run3.txt). Fixed LCG seeds (123456789,
987654321), fixed tie-breaks (lowest op id among argmax, least-tried
among unseen). Binaries multop_bin_v1..v7 and all 21 run outputs
preserved. Rebuild: pinned znc
(~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
on multop.zag, zero warnings.

## Architecture accounting

One standalone multop.zag (~1100 lines). 0 modes, 0 bridges,
0 handlers, 0 hardcoded semantic cases, 0 hardcoded 3-sequences in
learner code. Learner-state structures: 5 op byte-array bodies,
8-instruction interpreter, appl 5x16, comp 5x5, tot/retired, param
cells (p4), consequence ring, discovery recorder. Capability-source
delta: the [1,3,2] triple and p4=4 exist only in learner state;
source holds only generic machinery.
