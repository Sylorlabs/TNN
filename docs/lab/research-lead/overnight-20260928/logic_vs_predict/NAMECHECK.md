# NAMECHECK.md -- Logic vs Prediction Worker

## Step 0: Toolchain guard (mandatory)

Executed at worker startup (2026-10-01 23:21 PDT):

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing. Only `guard-check-done` printed.
PATH restricted to `$HOME/safebin` for all build/run commands below.

Pinned compiler: `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`

## Step 1: Pure Zag attestation

- All research logic in `lp_full.zag` (single Zag source, one binary runs both arms).
- Shell used only for: invoking znc, running the binary, git add/commit with explicit pathspecs, sha256sum comparison, file moves.
- Zero Python/C/Rust/JS invocations. No forbidden executables.

## Step 2: Scope

- UNFROZEN variant only. Frozen TNN-2 source read-only (idioms copied, not modified).
- Battery models state-driven process selection (retrieve/derive/predict/inquire) vs prediction-first; it does not claim to be the frozen binary.
- Nothing pushed. Commits local only.

## Step 3: Determinism

- 3 runs of `lp_bin`, sha256sum compared. All byte-identical required before verdict.
