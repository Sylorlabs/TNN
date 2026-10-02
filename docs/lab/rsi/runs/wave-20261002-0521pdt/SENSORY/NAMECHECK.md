# NAMECHECK - SENSORY lane, wave-20261002-0521pdt

## Step 0: Worker toolchain guard (executed 2026-10-02, before any other work)

- Ran `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  -> SAFEBIN-READY: /home/hatch/safebin (36 tools, no python); znc OK (pinned Linux build
  /home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
- Exported `PATH="$HOME/safebin"` in every shell
- `which python3` -> nothing (exit 1); `which python` -> nothing (exit 1)
- VERDICT: guard SATISFIED. All computational work in this lane is pure Zag via the pinned znc
  binary. Shell only for znc invocation, binaries, git ops, file moves. Dash scans via the
  sanctioned check_no_dash.sh snippet only.
- Forbidden-executable invocation rule acknowledged: any python/python3 (or C/C++/JS/Rust
  research-logic) invocation in this lane = automatic PROCESS-FAIL with immediate self-disclosure.
- Pinned-znc miscompile rule observed: no `as *i32` + q[0..n] slice construction anywhere;
  u8-cell loop idiom only (same idiom as the committed desynth_render.zag).

## Step 1: Lane identity

- Lane: SENSORY (audio + image big realism levers), wave-20261002-0521pdt
- Branch: tnn-native-lab; tip db3cc7086 at start
- Working copy: ~/workspace/tnn-rsi
- Task 1: implement frozen PREREG_SA1.md (frozen ALONE at commit 5305d9195; commit-order
  self-check: 5305d9195 strictly precedes all implementation commits in this lane). Sealed
  eval against frozen kill bars B1-B8, 3x byte-identical. Verdict BUILD-PASS/BUILD-FAIL only.
- Task 2: propose ONE big-lever image realism candidate (not grain, not micro-tweak): new
  frozen prereg (alone) naming the new mechanism, then implement and test. If judge-ready,
  sealed blind A/B with full provenance header in JUDGE_BRIEF.md, marked READY-FOR-JUDGE.
  Micah is the sole judge; never adopt on metrics alone.
- Task 3: red-team any artifact/dropout/weirdness as knowledge-vs-architecture.
- Docs: docs/lab/rsi/runs/wave-20261002-0521pdt/SENSORY/
- Red lines observed: no spending, no publishing, no outsiders, no bookings, no irreversible
  commitments, no Google Drive, never weaken a frozen kill bar, never git push (local commits
  only), pathspec-only commits (never git add -A / stash / reset / clean / rebase), no dashes
  in loop docs (check_no_dash.sh before committing), provenance honesty on all candidates.

## Step 2: Commit-order self-check (verified 2026-10-02)

- `git log --oneline` shows 5305d9195 (PREREG_SA1 freeze, committed ALONE, single file)
  as an ancestor of the current tip db3cc7086. All SA1 implementation commits in this lane
  are created after db3cc7086. Prereg strictly precedes implementation. CHECK PASSED.
