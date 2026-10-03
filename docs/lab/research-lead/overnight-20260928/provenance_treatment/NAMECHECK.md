# NAMECHECK.md: Provenance Treatment Worker

## Step 0: Toolchain Guard

Activated safebin at startup per worker toolchain guard.

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with no python3/python paths printed.
`which python3` and `which python` return nothing in safebin PATH.

All research computation in pure Zag via pinned znc:
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`.

Shell used only for: invoking znc, running binaries, git ops, file moves/copies.

## Scope

Unfrozen variant only. Frozen TNN-2 source never touched.
Frozen source read-only reference. Paper untouched. Nothing pushed.

## Input Provenance

- Base: verbatim copy of prior provenance experiment files from
  `docs/lab/research-lead/overnight-20260928/provenance_exp/`
  (commit `8c352e5bf`, PROVENANCE-COMPLETE: FIXES).
- `pv_nomain.zag`: frozen base + 6 source-tag writes, truncated before run_all.
- `pt_boot_ctl.zag`: control bootstrap_miss (source-blind, verbatim discount pilot).
- `pt_boot_trt.zag`: treatment bootstrap_miss (source-aware, EXTERNAL-only voting).
- New driver `pt_driver.zag`: three batteries (A/B/C) written by this worker.

## Output

All deliverables in `docs/lab/research-lead/overnight-20260928/provenance_treatment/`:
- `NAMECHECK.md` (this file)
- `REPORT.md` (results, tradeoff analysis, standing metrics)
- `pt_driver.zag` (three-battery driver)
- `pt_full_ctl.zag`, `pt_full_trt.zag` (assembled units)
- `pt_bin_ctl`, `pt_bin_trt` (pinned-znc binaries)
- `pt_ctl_run1/2/3.txt`, `pt_trt_run1/2/3.txt` (3/3 per arm)
