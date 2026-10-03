# NAMECHECK.md -- Scaling 5000 Worker

## Step 0: Toolchain guard (2026-10-02)

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
"guard-check-done"). Safebin contains 42 tools including pinned znc.
Pure Zag for all computation. Shell only for: invoking znc, running
binaries, git operations, moving/copying files.

No forbidden executable invoked in this wave. PROCESS-PASS on toolchain.

## Reuse verification

- `base_nohook.zag`: 7-slice extraction of
  `../scaling_clean/sc_base_expanded.zag` (regions 1-296, 315-418,
  427-441, 473-532, 544-812, 836-1356, 1358-1591). Assembly
  base_nohook + sc_patch + sc_driver reproduces
  `../scaling_clean/sc_full.zag` BYTE-IDENTICALLY (cmp clean).
- `ih_patch_used.zag`: cmp-verified identical to
  `../index_harden/ih_patch.zag` (sha256 2a057061...fea06a2b).
- `idx_walk_bucket` logic reused verbatim from the hardened patch;
  I1-I4 invariants unchanged; only the I5 buffer capacity constant was
  adapted 512 -> 8192 (documented in REPORT.md; forced by scale, the
  plen-2 bucket alone holds ~4995 MAPs).
- Workspace expansion 8192/16384 -> 65536/65536 and frame-slot
  threshold 10000 -> 100000 applied by line-addressed sed to the
  extracted base only, documented in REPORT.md. No mechanism logic
  changed.

## Determinism

3/3 runs byte-identical. Binary stdout sha256:
382e913a1ada196ac858de10644f1a3d2060f734c6b9dfa34be974c334fdc4d6
for s5000_run1.txt, s5000_run2.txt, s5000_run3.txt (wrapper
exit-echo lines stripped before hashing; the binary outputs are
identical).
