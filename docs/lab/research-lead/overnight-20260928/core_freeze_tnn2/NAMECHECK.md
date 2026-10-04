# NAMECHECK.md: CORE-FREEZE-TNN2 Preregistration

Date: 2026-09-30. Task: Create frozen preregistration for Core Freeze on TNN-2 (second cycle).

## Step 0: Toolchain guard check

Command run: `which python3 python 2>/dev/null; echo "guard-check-done"`

Result: `/usr/bin/python3` present (unremovable system binary).
Documented non-use. Zero invocations during this task.

This is a documentation-only task (preregistration). No research
computation, scoring, or analysis is performed. No Python is
invoked at any point.

## Scope

Owned path: `docs/lab/research-lead/overnight-20260928/core_freeze_tnn2/`

Contains: CORE_FREEZE_TNN2_PREREG.md (this prereg), NAMECHECK.md (this file).

## Governance

- Preregistration strictly precedes implementation (K-FZ2-1).
- TNN-2 build basis: `f4de7ff46` (TNN2-BUILD-PASS).
- Reproduction basis: `fdf1fa626` (TNN2-REPRO-PASS).
- Root-cause basis: `ed38121d4`.
- Implements Micah's Core Freeze workflow: second FREEZE after NEXT GENERATION build.
- No em dashes (byte-verified before commit).
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md` zero-diff.
- No sealed FW1-FW9 accessed.
- Explicit pathspecs only.
