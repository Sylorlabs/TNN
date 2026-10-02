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

## This worker: rebuild and independent rerun (2026-10-02)

### Step 0 (this worker): Toolchain Guard

Executed at this worker's startup, same script as above. `which python3
python` returned NOTHING (empty output before "guard-check-done").
PATH=/home/hatch/safebin. Pure Zag for all research computation.
**Zero forbidden executables invoked.**

### Commit-order self-check

- PREREG.md committed ALONE as 4c15fe32d (2026-10-02 15:47:04 UTC).
- lv_driver.zag first written 15:47:47 UTC, after the prereg commit.
- lv_run1.txt first written 15:48:43 UTC, after implementation.
- PREREG_AMENDMENT1.md write-up finalized 15:49:19 UTC, after the
  first run file's mtime. The amendment STRENGTHENS the battery
  (plen-4 to plen-6 Z; no bar weakened), and this worker rebuilt and
  reran the amended battery from scratch, evaluating all bars against
  the amended design only. Recorded transparently per governance.

### Driver verification (this worker, against frozen PREREG + Amendment 1)

- X taught as (11,1,12),(12,1,13),(13,1,14), query (11,71,14) ans=14:
  matches amended plen-3 design.
- Y taught as (21,2,22),(22,2,23),(23,2,24), query (21,72,24) ans=24:
  matches amended plen-3 design.
- L1 Z facts plen-6 (101..107), query (101,70,107): matches amendment.
- L2 Z facts: four r1 links (101..105) + three r2 links, query
  (101,70,108): X ([1,1,1]) must be extended; the adaptation
  requirement survives the amendment correctly.
- L3 Z facts: three r1 links + r9 bridge (104,9,105) + three r2
  links, query (101,70,108): matches design.
- 30-distractor gap (subjects 5000+, relations 60-69) in every
  treatment arm. Fresh tnn2_init workspace per arm.
- un_patch.zag sha256 3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2
  identical to composition_unified/un_patch.zag: verbatim copy.
- lv_has14 edge check verified against link_edge layout
  (offsets 0=from, 4=rel, 8=to); patch writes
  link_edge(W,zm,14,segmap,0), so the provenance direction matches.
- lv_kill (ns(W,m,36,0)) disables the MAP: activate requires
  ng(W,n,36)==1.

### Build records (this worker)

- Build: cat ../composition_C/cc_base.zag un_patch.zag lv_driver.zag
  > lv_full.zag (2298 lines)
- Compile: src/tools/toolchain/znc_linux_x86_64_abed8aa1
  lv_full.zag -o lv_bin > lv_compile.txt 2>&1; exit 0; benign A0102
  warnings only (same class as prior builds).
- Binary: lv_bin, 281033 bytes.
- Runs: lv_run1/2/3.txt, exit 0 each.
- SHA-256: d7cded3a3a26ccd9ea15dafe001d3aa64b824de8c397f2946b19c4d362272e51
  for all three runs (byte-identical), matching the prior wave's
  digest exactly: independent reproduction confirmed.
- Kill bars: K1-K8 all PASS (see REPORT.md).
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
- Em/en dash byte-verification: no E2 80 93/94 sequences in any
  deliverable (PREREG.md, PREREG_AMENDMENT1.md, NAMECHECK.md,
  REPORT.md, lv_driver.zag).
