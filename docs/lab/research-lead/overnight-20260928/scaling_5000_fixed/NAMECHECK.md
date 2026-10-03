# NAMECHECK.md -- Scaling 5000 Rerun Worker (s6_* workstream)

## Step 0: Toolchain guard (2026-10-02)

Executed at worker start, before any other work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING (empty output before
"guard-check-done"). Safebin holds the pinned znc plus coreutils/git.
PATH is $HOME/safebin only for all worker commands.

No forbidden executable invoked in this wave. PROCESS-PASS on toolchain.

## Reuse verification

- `s6_base.zag`: byte extracted lines 1..1495 of the committed
  `../scaling_5000/s5_full.zag` (the exact base region that produced
  the s5 5000-MAP runs, including the high-water alloc_node). Verified
  with cmp after extraction.
- `s6_patch.zag`: `../scaling_5000/s5_patch.zag` with the three FACT
  index functions (`fidx_add`, `t2_lu_first_idx`, `t2_gather_idx`)
  renamed to `*_orig` (kept, dead code, provenance) and the hardened
  FI1-FI5 replacements from committed `../fact_index_fix/fi_fix.zag`
  (commit 11622ae25, sha256 verified identical to working tree)
  appended under the canonical names. The redundant `t2_lu_first_h`
  dispatch override was dropped: the existing `t2_lu_first` dispatch
  already routes to the hardened `t2_lu_first_idx` when mode bit2 is set.
- `s6_driver.zag`: new driver written for this prereg (three build
  orders, chain integrity checks, mode 0/1/3/5 query measurements).
  Build helpers `s6_mkchain`/`s6_mkbroken` are logic identical to the
  s5 driver versions (renamed only).
- `s6_full.zag`: assembled as s6_base + s6_patch + s6_driver by
  concatenation; no overlapping definitions (verified: each `fn`
  defined exactly once).
- Frozen TNN-2 base used read-only as library. Nothing in the frozen
  tree modified.

## Determinism

3/3 runs byte-identical per build order (sha256 recorded in REPORT.md).
