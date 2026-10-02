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

## Steps 1-6: (to be filled)

- [ ] Prereg frozen before implementation (PREREG.md committed alone).
- [ ] Implementation in pure Zag, unfrozen files only.
- [ ] Frozen base (cc_base.zag, cc_patch.zag) used verbatim, read-only.
- [ ] 3/3 byte-identical runs per arm.
- [ ] Zero em/en dashes (byte-verified).
- [ ] Paper untouched. Nothing pushed.
