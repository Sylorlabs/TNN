# NAMECHECK.md -- Spontaneous Connections Lifetime Worker

## Step 0: Toolchain guard
- Date: 2026-10-01
- `which python3 python` returns nothing (verified: only "guard-check-done" printed).
- `export PATH="$HOME/safebin"` active. safebin/znc symlinks to pinned
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- All computation in pure Zag via pinned znc. Shell only for znc invocation,
  file moves, git ops.
- Zero forbidden executables invoked.

## Step 1: Provenance
- Cognition: byte-identical to rebind treatment variant (`91585087c`).
  Base SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`.
  Only the driver (world stream) is new. No cognition source changes.
- Frozen TNN-2 source read-only, never modified.

## Step 2: Task
- Build a 300+ event continuous lifetime: A learned, 300 unrelated events,
  then B presented with no "use A" hint.
- Measure spontaneous retrieval (verifies on B vs fresh control),
  cross-era edge formation, 3/3 deterministic.

## Step 3: Constraints
- Unfrozen variant (rebind treatment). Driver-only change.
- Pure Zag. Zero em/en dashes in docs. Paper untouched. Nothing pushed.
- Explicit pathspecs on git add and git commit.
