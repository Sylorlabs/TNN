# NAMECHECK.md -- H3 Generality Analysis Worker

## Step 0: Toolchain Guard

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

Result: `guard-check-done` with no output from `which python3 python`.
Neither `python3` nor `python` resolves in the safebin PATH.

**Attestation:** Zero forbidden executables invoked during this wave.
All work was file reads (analysis of existing reports) plus git operations.
No Python, no calculators, no text-processing shortcuts beyond grep for
locating report files.

## Scope

This worker performed ANALYSIS ONLY using existing committed results.
No new Zag code was written. No binaries were built. No experiments were run.
The deliverable is ANALYSIS.md with an architecture recommendation.

## Files

- NAMECHECK.md (this file)
- ANALYSIS.md (generality analysis and recommendation)

## Constraints observed

- Pure analysis; no computation beyond file reads.
- Zero em/en dashes (verified by byte scan before commit).
- Paper untouched.
- Nothing pushed (local commits only).
- Explicit pathspecs for git operations.
