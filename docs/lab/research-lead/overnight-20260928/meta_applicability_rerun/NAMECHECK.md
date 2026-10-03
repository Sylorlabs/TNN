# NAMECHECK.md: Meta-Applicability Rerun Worker (FAIL recovery)

## Step 0: Toolchain Guard (MANDATORY)

Activated: 2026-10-02

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returns nothing (empty output before
`guard-check-done`). Guard check passed.

- Safebin PATH active for all build/run commands in this task.
- All computation in pure Zag via pinned znc
  (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- Shell used only for: invoking znc, running binaries, git ops, file moves.
- Zero forbidden executables invoked. Any invocation would be PROCESS-FAIL.

## Recovery mandate

Prior worker commit 0478b8eaf (branch lane-battery-e5), files in
`docs/lab/research-lead/overnight-20260928/meta_applicability/`:
mechanism behavior correct, verdict FAIL on K7 (TREAT 0/3 byte-identical;
TREAT and NAIVE hang on the 21st problem, C-P5) and C-P5 unmeasured.
Failure is technical (base TNN-2 `t2_trial` scaling), not conceptual.

This worker: diagnose the exact base bug, fix it in the UNFROZEN rerun
copy only, re-freeze the prereg (base change breaks the old prereg), rerun
TREAT 3/3 (and FRESH 3/3 if the fix changes FRESH numbers), deliver
PREREG.md, REPORT.md with bug diagnosis, source, binaries, run outputs.

## Ordering note (prereg discipline)

Diagnosis runs below reproduce the PRIOR worker's failure from its
committed source (commit 0478b8eaf) in /tmp scratch; they are failure
analysis, not the new experiment. The fresh PREREG.md for the rerun is
committed BEFORE the fixed implementation is built or run, so the
prereg's first commit strictly precedes the fixed implementation's first
run (prereg commit-order self-check).

## Base

- `ma_base.zag`: starts as a verbatim copy of the prior worker's
  `ma_base.zag`, itself cmp-verified verbatim against frozen
  `learning_to_learn/l2l_base_trim.zag`. The frozen file is read-only
  and untouched (verified: no modifications in learning_to_learn/).
- The bug fix lands ONLY in the rerun copy `ma_base.zag` (unfrozen
  variant lane). Frozen base never edited.
- `ma_patch.zag`: APPL gate + two-pass rebind, carried over unchanged
  unless the diagnosis implicates it (it does not; the hang is in the
  base trial path with gate=0).
- `ma_driver.zag`: 3-arm driver, carried over unchanged.
- `build.sh`: same 3-arm stamp/compile flow as the prior worker.

## Constraints honored

- Unfrozen variant only. Frozen read-only (verified clean above).
- Pure Zag. Zero em/en dashes in docs (byte-verified before commit).
- Research paper untouched.
- Nothing pushed (local commits only).
- 0 modes/bridges/handlers/semantic cases.
- No researcher domain labels anywhere in cognition (gate sees only the
  8 observable structural features, unchanged from the prior worker).

## Diagnosis (2026-10-02)

Recorded in REPORT.md. Summary: per-candidate node leak in the base
miss policy. Every failed `t2_trial`/`rebind` candidate assembles a
fresh 4-op ISA graph (`t2_asm_chain`: 4 cells per link) plus a frame
node per verify (`t2_exec`); on verification failure none of it is
freed. The node arena is 1024 slots. Cumulative leakage fills the arena
around problem 17-20 of the 21-problem TREAT/NAIVE sequences (FRESH has
only 16 problems and completes just under the limit). Once full, every
`alloc_node` falls through to `evict_node`, whose lowest-bid scan costs
O(1024 nodes x 4096-edge is_prot/bid scans) per eviction; C-P5 performs
dozens of allocs, each triggering a full scan, producing the observed
hang (pathological slowdown, not an infinite loop: `execute` carries a
1000-step budget and all arena scans are bounded).

Fix: free failed candidate graphs (cells + frame + their edges) inside
the miss policy on verification failure. Successful (promoted) graphs
are untouched. This changes no verify outcome and no gate decision; it
only removes arena pressure. FRESH rerun 3/3 compared by SHA-256 against
the prior FRESH hash to confirm zero behavioral delta.
