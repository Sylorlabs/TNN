# NAMECHECK: H-DECOMP-1 Fragment-Addressable Storage Worker

Worker: Fragment-Addressable Storage (H-DECOMP-1, P0).
Date: 2026-10-02. Session 17a2086f-b685-4ac2-b6c7-cfdffc284438.

## Step 0: Toolchain Guard (mandatory, recorded before any build)

Safebin setup executed 2026-10-02 07:18 PDT:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum \
         git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` printed NOTHING (no forbidden executable
resolves in PATH). Guard line printed `guard-check-done`. Safebin holds 36
symlinks including pinned `znc 2026.07.0-dev (edition 2026)`.

All subsequent work in this lane runs with `export PATH="$HOME/safebin"`.
Any invocation of a forbidden executable (python3, python, or any other
interpreter outside the safebin allowlist) is automatic PROCESS-FAIL for the
current scientific wave.

## Step 1: Prereg commit order

PREREG.md is committed BEFORE any implementation file exists. The prereg
commit must strictly precede the implementation commit (commit-order
self-check). Verified via `git log` ordering before the build begins.

## Step 2: Pure Zag verification

- Implementation file `frag_store.zag` contains only Zag source.
- Build command is `znc` only. No python, no cc, no other compiler.
- Runtime output inspected for toolchain leakage (no python tracebacks,
  no non-Zag artifacts).

## Step 3: Frozen read-only

No file outside `frag_storage/` is modified. The frozen TNN-2 core, the
composition_compare battery, and invention_recombine sources are read but
never edited.

## Step 4: No-push, local commits only

Commits stay on branch `tnn-native-lab` in `~/workspace/tnn-rsi`.
Explicit pathspecs only; other workers' uncommitted changes are never
staged. Nothing is pushed to GitHub.

## Step 5: Output determinism check

`run1.txt`, `run2.txt`, `run3.txt` are byte-compared with `cmp` and
`sha256sum`. 3/3 identical required by kill bar KB1.

## Step 6: Dash audit

All docs and code comments scanned for em dashes and en dashes before each
commit. None permitted.
