# NAMECHECK.md: Core Freeze Re-run Preparer

## Step 0: Toolchain Guard

- Command: `which python3 python 2>/dev/null; echo "guard-check-done"`
- Result: `/usr/bin/python3` present (system binary, cannot be removed from PATH)
- Action: Documented non-use. Zero invocations of python3 or python in this task.
- Task type: Analysis and planning only. No computational research operations performed.
- If computation were needed, Zag would be used. Shell used only for git reads and file operations.

## Contamination Check

- Contaminated paper `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`: will verify zero-diff before and after commit.
- Sealed FW1-FW9 files: NOT accessed. Planning only; world designs read from the design document (commit `200387b42`), which is design-only markdown, not the sealed world files.
- No em dashes in documentation (verified via byte grep before commit).

## Scope

This worker prepares the Core Freeze re-run plan. It does NOT run the freeze, does NOT modify TNN-1 source, does NOT access sealed evaluator files.
