# NAMECHECK.md -- Sealed Strong Composition Worker

## Step 0: Toolchain guard (mandatory)

Executed at startup:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing. `guard-check-done` printed.
Safebin active for every subsequent command. Zero forbidden executables
invoked. Toolchain note: the pinned znc
(`src/tools/toolchain/znc_linux_x86_64_abed8aa1`) exposes `emit`/`e64`/
`z_alloc` only through user-defined prelude functions on the `_zag_print`,
`_zag_i64_to_str`, `_zag_malloc` intrinsics; `sc_full.zag` carries that
prelude (same pattern as prior workers). Plain `znc` compile used, exit 0.

## Step 1: Identity

Worker: Sealed Strong Composition (Micah Priority 4).
Task: sealed test of X+Y->Z with X = independently taught scalar skill,
Y = independently taught sequence domain, Z = sealed novel goal requiring
both. No paired X+Y examples (machine-checked), no hint, no task label.

## Step 2: Base

Unfrozen only. Standalone experiment binary; no frozen source touched,
frozen read-only. Preregistration committed first as `a9fa821f3`
(PREREG_SEALED.md), strictly before implementation.

## Step 3: Outputs

- `PREREG_SEALED.md`: frozen kill bars (committed `a9fa821f3`).
- `sc_full.zag`: full experiment (309 lines, pure Zag).
- `sc_bin`: compiled binary (pinned znc, 38400 bytes).
- `sc_compile.txt`: compiler transcript (exit 0).
- `sc_run1/2/3.txt`: 3/3 byte-identical transcripts
  (SHA-256 `bc4cf4bc1ff14070bbb62e169a63129feb43ccd0da7297613f96982370e4c28d`).
- `REPORT.md`: full analysis.

Pure Zag. Paper untouched. Nothing pushed. 0 modes/bridges/handlers.
Zero em/en dashes (byte-verified).
