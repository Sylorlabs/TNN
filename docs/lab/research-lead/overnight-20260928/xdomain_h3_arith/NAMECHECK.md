# NAMECHECK.md -- H3-Arithmetic-Planning Generality Worker

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, 2026-10-02:

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
printed). Safebin PATH active for all subsequent commands.

## Toolchain record

- Pinned compiler: `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
- All research computation in pure Zag via the pinned znc.
- Shell used only for: invoking znc, running binaries, git operations,
  moving/copying files.
- Zero forbidden executables invoked. Any violation would be PROCESS-FAIL.

## Assembly inputs (verbatim, sha256-verified)

- Base: `../../composition_C/cc_base.zag` (frozen TNN-2 base, read-only)
- Mechanism: `../xdomain_dataflow_clean/df_patch.zag` (canonical H3,
  byte-identical to clean reproduction)
- Mechanism (NO-DF control): `../xdomain_dataflow_clean/df_patch_nodf.zag`
- Driver: `h3a_driver.zag` (this worker; behavior implementations only)

## Constraints observed

- Unfrozen work only. Frozen source read-only.
- Paper (`TNN_RESEARCH_PAPER_20260929.md`) untouched.
- Nothing pushed. Local commits only.
- Zero em/en dashes (byte-verified before commit).
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
