# NAMECHECK.md -- Cross-Domain Composition H3 (Generic Dataflow)

## Step 0: Toolchain Guard

Executed at worker startup (2026-10-02):

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with NO output from `which python3 python`.
Python is NOT available in the worker PATH. Safebin contains 36 allowed
tools including the pinned `znc` compiler.

All research computation in this wave is pure Zag, compiled with the
pinned toolchain. Shell is used only for: invoking znc, running compiled
binaries, git operations, moving/copying files.

Any forbidden executable invocation would make this wave PROCESS-FAIL.
None occurred.

## Worker

Cross-Domain Composition H3 Worker (generic dataflow hypothesis).
Micah Priority A, Hypothesis 3 of 3 (competing with H1 typed contracts,
H2 value f(g(x))).

## Constraints observed

- Unfrozen layer only. Frozen TNN-2 source read-only.
- Pure Zag. Zero Python invocations.
- Zero em/en dashes in documentation (byte-verified before commit).
- Paper `TNN_RESEARCH_PAPER_20260929.md` untouched.
- Nothing pushed to GitHub. Local commits only.
- 0 modes / 0 bridges / 0 handlers / 0 new semantic cases.
- Explicit pathspecs for all `git add` / `git commit`.
