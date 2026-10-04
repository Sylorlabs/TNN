# NAMECHECK: Cross-Domain Grammar to Construction Worker

## Step 0: Toolchain guard (mandatory)

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

Result: `which python3 python` returned nothing. `guard-check-done` printed.
Safebin PATH active for the entire session. All research computation in
pure Zag via the pinned znc. Shell used only for: invoking znc, running
compiled binaries, git operations, moving/copying files.

Zero forbidden executables invoked. Any violation would be PROCESS-FAIL.

## Worker identity

Cross-Domain Grammar to Construction Worker (fourth domain pair,
Micah Battery D). Tests H1 (learned typed contracts) and H2
(value-level function composition) with UNMODIFIED mechanism logic on
the grammar -> construction pair.

## Constraints observed

- Unfrozen experiment only. Frozen source read-only (never read for code).
- Pure Zag. Zero em/en dashes (byte-verified before commit).
- Paper untouched (`docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`).
- Nothing pushed. Commits local only.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
- Explicit pathspecs for all git operations.
