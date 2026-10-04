# NAMECHECK: formal_richer (TX1 typed arithmetic)

## Step 0: toolchain guard (mandatory)

Executed at worker startup, before any research computation:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing. Only output was
`guard-check-done`. Safebin active for all subsequent commands.
PATH restricted to $HOME/safebin for the whole wave.

Attestation: zero invocations of python3, python, or any other
forbidden executable occurred during this wave. All computation via
the pinned znc (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`)
and compiled Zag binaries. File assembly via shell (cat/awk) only.

## Pre-execution checklist

- [x] Safebin guard executed, python3/python do not resolve.
- [x] PREREG.md frozen and committed BEFORE implementation.
- [x] Base is byte-identical copy of frozen TNN-2 base (sha256
      verified against grammar_induction/gi_base.zag).
- [x] Frozen source read-only; all changes in unfrozen patch/driver.
- [x] Paper (TNN_RESEARCH_PAPER_20260929.md) untouched.
- [x] Nothing pushed; local commits only.
- [x] Explicit pathspecs for all git operations.
- [x] Zero em/en dashes in loop documentation (byte-verified).
- [x] 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
