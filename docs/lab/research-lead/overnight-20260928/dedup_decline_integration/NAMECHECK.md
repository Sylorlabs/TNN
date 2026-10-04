# NAMECHECK.md -- Dedup-Decline Integration Worker

## Step 0: Toolchain Guard (MANDATORY)

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

Result: `guard-check-done` with NO output from `which python3 python`.
- `which python3` returns nothing.
- `which python` returns nothing.
- Safebin active: `$HOME/safebin` first in PATH.
- Zero forbidden executables invoked.

## Scope

INTEGRATION BUILD AND MEASUREMENT ONLY. Unfrozen variant only.
Frozen TNN-2 source is read-only (never opened for edit).
No sealed worlds. Nothing pushed.

## Input Provenance

- Dedup mechanism: commit `296fd79cb` (DEDUP-COMPLETE: BENT, 201 nodes).
  Base source: `dedup_full.zag` (verbatim, 1728 lines).
  Mechanism: 15-line content-addressed reuse pre-scan at top of `miss_inquire`.
- Decline mechanism: commit `f3e6985d4` (DECLINE-GATE-COMPLETE: BENDS, 241 nodes).
  Patch source: `dg_gate.zag` (61 lines).
  Mechanism: `dg_uncert_count` + `dg_n()=3` + WITHHOLD (-3) spliced into `ev_query`.
- DYN-1 driver: verbatim from dedup build (itself verbatim from `003767553`).

## Constraints Honored

- Unfrozen variant only. Frozen source read-only.
- Pure Zag via pinned znc (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- Shell only: znc invocation, binary runs, git ops, file moves.
- Zero em/en dashes in all documentation (byte-verified).
- Paper (`TNN_RESEARCH_PAPER_20260929.md`) untouched.
- Nothing pushed to GitHub (local commits only).
- Explicit pathspecs on both `git add` and `git commit`.
