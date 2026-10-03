# NAMECHECK: H-FALLBACKFIX-1 Scaling Analysis Worker (competing sublinear alternatives)

## Step 0: Toolchain Guard

Executed at worker startup (2026-10-02, first action of this session):

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null); [ -n "$p" ] && ln -sf "$p" $HOME/safebin/$t 2>/dev/null
done
export PATH="$HOME/safebin"
which python3; echo "python3 rc=$?"
which python; echo "python rc=$?"
```

Result:
- `which python3` returned NOTHING (rc=1). `which python` returned
  NOTHING (rc=1).
- PATH=/home/hatch/safebin (allowed tools only; python3/python do not
  resolve).
- safebin/znc symlinks to the pinned compiler
  src/tools/toolchain/znc_linux_x86_64_abed8aa1 (verified via ls -la).
- Pure Zag for all research computation. Shell used only for: invoking
  znc, running binaries, git ops, moving/copying files.

**Zero forbidden executables invoked during this wave.**

## Worker Identity

- Mission: H-FALLBACKFIX-1 scaling analysis. Generate, implement, and
  measure three structurally different sublinear alternatives to the
  O(4096) edge-scan pattern (D1 substrate edge-and-fact index, D2 lazy
  per-query memoization, D3 mechanism-maintained fragment summary),
  per Micah's ruling to treat the K4/K5 miss as scaling evidence.
- Worktree: ~/workspace/tnn-rsi, branch lane-tnn3-20261002-1421pdt
  (task named tnn-native-lab; that branch is checked out and locked in
  worktree ~/workspace/tnn-rsi-gpi3, so work proceeds here; deviation
  recorded, parent notified in final report).
- Prereg: PREREG.md in this directory, committed ALONE with this file
  strictly before any implementation file (commit-order self-check).
- Frozen inputs (read only, never modified):
  - composition_C/cc_base.zag (1677 lines)
  - composition_fallbackfix/ff_patch.zag (the repaired patch; copied
    to this lane as ff_patch_base.zag, cmp-verified, as the frozen
    baseline reference)
  - composition_fallbackfix/ff_driver_nomain.zag (test functions)
  - composition_collapse/cl_driver.zag (C234 battery protocol)

## Build Records

(to be filled after the prereg commit; implementation follows)

- Baseline patch: scaling_fallbackfix/ff_patch_base.zag (frozen copy)
- D1 patch: scaling_fallbackfix/ff_patch_D1.zag (to be written)
- D2 patch: scaling_fallbackfix/ff_patch_D2.zag (to be written)
- D3 patch: scaling_fallbackfix/ff_patch_D3.zag (to be written)
- Timed driver: scaling_fallbackfix/ff_scal_timed.zag (to be written)
- Mains: main_corr.zag, main_r4b.zag, main_r4c.zag, main_d3sess.zag
  (to be written)
- Pinned compiler: src/tools/toolchain/znc_linux_x86_64_abed8aa1

## Constraints Observed

- Prereg committed alone before any implementation file exists.
- Pure Zag for all research logic (Step 0 guard above).
- Zero em/en dashes in PREREG.md, NAMECHECK.md, REPORT.md
  (byte-verified before commit).
- Local commits only with explicit pathspecs. Nothing pushed.
- No new edge types, node tags, semantic cases, modes, bridges,
  handlers, or routers in any design (A0 audit at report time).
