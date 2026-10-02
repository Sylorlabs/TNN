# NAMECHECK.md -- xdomain_value (H2: value-level function composition)

## Step 0: Toolchain guard

Executed at worker startup:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing (only "guard-check-done"
printed). Safebin contains 36 tools including pinned znc
(`znc_linux_x86_64_abed8aa1` via symlink). All subsequent work uses
`export PATH="$HOME/safebin"`.

Pure Zag for all research computation. Shell only for: invoking znc,
running binaries, git operations, moving/copying files.

## Steps 1-6: COMPLETE

- [x] Prereg frozen before implementation (PREREG.md committed as 5b5bb39e8).
- [x] Implementation in pure Zag, unfrozen files only (vc_patch.zag, vc_driver.zag).
- [x] Frozen base (cc_base.zag, cc_patch.zag) used verbatim, read-only.
- [x] 3/3 byte-identical runs per arm (sha256 72f4a805...).
- [x] Zero em/en dashes (byte-verified via grep -P).
- [x] Paper untouched. Nothing pushed.
- [x] K1-K7 all PASS. Verdict: XDOMAIN-VALUE-COMPLETE.
