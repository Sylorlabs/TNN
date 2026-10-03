# LM4 NAMECHECK

## Step 0: Toolchain Guard
- Safebin activated: `export PATH="$HOME/safebin"` ✓
- `which python3`: returns nothing (not in PATH) ✓
- `which python`: returns nothing ✓
- All research logic in pure Zag. Shell only for: znc invocation, binary execution, git ops, file moves.
- No forbidden interpreter invoked.

## Step 1: Lane
- `docs/lab/research-lead/overnight-20260928/lifetime_strategy/`

## Step 2: Prereg
- PREREG.md frozen BEFORE implementation.
- Bars B4,B5a,B5b,B5c,B5d,B5e,B6,B7 defined above.
- Commit order: prereg first, implementation second.

## Step 3: Determinism
- Seed: 20261007 (fixed in gen()).
- 3/3 byte-identical runs required (sha256 of stdout).
