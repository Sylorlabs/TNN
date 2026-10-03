# NAMECHECK: substrate_selection worker

## Step 0: Toolchain guard
- safebin constructed at worker startup from PATH-resolved tools.
- `export PATH="$HOME/safebin"` active for all build/run commands.
- `which python3 python` returns nothing (verified 2026-10-01, guard-check-done).
- All research computation in pure Zag via pinned znc.
- Shell used only for: invoking znc, running binaries, git ops, file moves.
- No forbidden executable invoked. No Python executed at any point.

## Base
- Fork of prediction_optional/po_full.zag (compact 7-process world, 510 lines).
- Substrate record machinery (tag 61) adapted from
  substrate_expansion/se_machinery.zag (build 02a338dbf).
- Frozen TNN-2 source: read-only, untouched.
- Unfrozen variant only.

## Constraints
- Pure Zag. Zero em/en dashes in docs (byte-verified before commit).
- Research paper untouched. Nothing pushed. Explicit pathspecs for git.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
