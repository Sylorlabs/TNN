# NAMECHECK: Protect-the-How Worker

## Step 0: Toolchain guard (2026-10-01)

Safebin activated:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `which python3 python` returned NOTHING. Guard check passed.
`guard-check-done` printed. Zero forbidden executables invoked.

## Provenance

- Worker: Protect-the-How Worker (subagent of TNN research coordinator).
- Task: Micah Q6 — reverse "preserve answers, kill procedures".
- Base cognition: `ph_base.zag` = lines 1-917 of
  `docs/lab/research-lead/overnight-20260928/interference_experiment/tnn2_interference_variant.zag`
  (cognition byte-identical to frozen TNN-2; interference probes removed).
- Variant: UNFROZEN only. Frozen source never touched.
- Control binary: base cognition + driver (evict_node verbatim).
- Treatment binary: base cognition with ONLY evict_node replaced by 3-tier
  version (derived answers -> other nodes -> generative structure) + driver.
- All computation in pure Zag via pinned znc. Shell used only to invoke znc,
  run binaries, git ops, move files.

## Files

- `ph_base.zag`: base cognition (917 lines, probes stripped)
- `ph_evict_trt.zag`: treatment evict_node (replaces base lines 254-275)
- `ph_driver.zag`: experiment driver (white-box helpers + ph_main)
- `ph_ctl_full.zag` / `ph_trt_full.zag`: assembled sources
- `ph_ctl_bin` / `ph_trt_bin`: binaries
- `ph_ctl_run1/2/3.txt`, `ph_trt_run1/2/3.txt`: 3/3 run outputs per arm
- `ph_diff.txt`: diff of treatment vs control cognition (must show ONLY evict_node)
- `REPORT.md`: results and verdict
