# NAMECHECK: Composition Three-Level Worker

## Step 0: Toolchain Guard

Executed at worker startup (2026-10-02):

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result:
- `which python3 python` returned NOTHING (empty output before "guard-check-done")
- PATH=/home/hatch/safebin
- Pure Zag for all research computation. Shell used only for: invoking
  znc, running binaries, git ops, moving/copying files.

**Zero forbidden executables invoked during this wave.**

## Worker Identity

- Mission: Micah Priority 3. Measure composition at three levels
  separately using the unified composition mechanism.
- Levels: L1 exact reuse, L2 adaptive reuse, L3 novel composition.
- Do not collapse into one PASS. Report per-level verdicts.
- Branch: tnn-native-lab (local only, nothing pushed).
- Prereg: PREREG.md committed ALONE before any implementation
  (commit-order self-check).

## Build Records

- Base: composition_C/cc_base.zag (1677 lines, frozen, read only)
- Patch: composition_unified/un_patch.zag (420 lines, verbatim copy)
- Driver: composition_levels/lv_driver.zag (this worker)
- Build: cat cc_base.zag un_patch.zag lv_driver.zag > lv_full.zag
- Binary: lv_bin (pinned znc_linux_x86_64_abed8aa1)
- Runs: lv_run1/2/3.txt (3/3 byte-identical required)
