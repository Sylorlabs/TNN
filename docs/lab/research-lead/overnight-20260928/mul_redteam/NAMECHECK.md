# NAMECHECK.md - MUL Red Team

## Step 0: Toolchain Guard

- Command run: `which python3 python 2>/dev/null; echo "guard-check-done"`
- Result: `/usr/bin/python3` present as unremovable system binary.
- Guard action: documented non-use. Zero invocations of python3/python in this wave.
- This is a read-only attack task (source audit + binary reruns). All computational work via the target binary and shell.

## Ownership

- Owned path: `docs/lab/research-lead/overnight-20260928/mul_redteam/`
- Target (read-only): `docs/lab/research-lead/overnight-20260928/mul_build/` at commit `fbf14f73a`
- This worker does NOT modify the target. Attack only.

## Commit hygiene

- Explicit pathspecs only (owned path).
- No em dashes (byte-verified before commit).
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md` verified zero-diff before and after.
- No sealed FW1-FW9 files accessed.
