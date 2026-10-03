# NAMECHECK.md -- Index Hardening Worker

## Step 0: Toolchain Guard (mandatory)

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

Result: `guard-check-done` with NO python3/python paths printed.
`which python3 python` returns nothing. Guard PASS.

Worker runs with `export PATH="$HOME/safebin"` for all build/test commands.
All research computation in pure Zag via pinned `znc`. Shell used only to
invoke znc, run binaries, and do git/file operations.

Any forbidden executable invocation = PROCESS-FAIL for this wave.

## Build identification

- Base: `../rebinding_hardening/hard_base.zag` (frozen, read-only)
- Vulnerable index: `../scaling_index/si_patch.zag` (frozen, read-only)
- This work: `index_harden/ih_patch.zag` (unfrozen hardened replacement)
- Test driver: `index_harden/ih_driver.zag` (unfrozen)
- Assembly mirrors `../scaling_index/build.sh` line surgery, substituting
  ih_patch.zag for si_patch.zag and ih_driver.zag for si_driver.zag.

## Naming

- `ih_` prefix = index hardening (this worker).
- Binaries: `ih_bin` (corruption tests).
- Run outputs: `ih_run_<corruption>_<n>.txt`.
