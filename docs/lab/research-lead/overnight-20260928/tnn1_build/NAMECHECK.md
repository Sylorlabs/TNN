# TNN-1 Integration Builder: Step 0 Name-Check

Date: 2026-09-30. Worker: Integration Builder (TNN-1).

## Toolchain guard check

Command: `which python3 python 2>/dev/null; echo "guard-check-done"`

Result:
- `/usr/bin/python3` exists (system binary, cannot be removed from PATH)
- `python` not found
- Documented non-use: python3 is NEVER invoked during this wave

## Guard compliance

- All computational research operations use Zag only.
- Shell usage limited to: invoking znc, running binaries, git operations, move/copy files.
- Zero Python invocations. Zero other interpreter invocations.
- If a forbidden executable is invoked, this wave is PROCESS-FAIL.

## K1 verification

Prereg commit `7fc7148ac` verified as ancestor of HEAD via
`git merge-base --is-ancestor 7fc7148ac HEAD` before implementation.
K1 holds.

## Constraints acknowledged

- Owned path: `docs/lab/research-lead/overnight-20260928/tnn1_build/` only.
- No em dashes in documentation (byte-verified).
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md` zero-diff verified.
- No sealed FW1-FW9 files accessed.
- Hard 1200-line ceiling on tnn1.zag (F-INT1).
- Builder reports BUILD-PASS/BUILD-FAIL only. No L3 or SURVIVES claim.
