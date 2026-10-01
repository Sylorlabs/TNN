# NAMECHECK.md: TNN-2 Architecture Compression Analysis

Date: 2026-09-30. Task: Investigate which researcher-authored machinery
in TNN-2 can be deleted while preserving the new general capability.
Investigation only; no source edits.

## Step 0: Toolchain guard check

Command run: `which python3 python 2>/dev/null; echo "guard-check-done"`

Result: empty output before "guard-check-done". Neither `python3`
nor `python` resolves in the safebin PATH (40 allowed tools:
coreutils, git, pinned znc).

This is an analysis-only task (reading source, reasoning, writing
this report). No research computation is performed. No Python is
invoked at any point.

## Scope

Owned path: `docs/lab/research-lead/overnight-20260928/tnn2_compression/`

Contains: NAMECHECK.md (this file), COMPRESSION_ANALYSIS.md.

Target (read-only, never modified):
`docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
(1591 lines, frozen, commit `f4de7ff46`).

## Governance

- Investigation only. Zero source edits to `tnn2_build/`.
- Per Micah's directive: do NOT compress before frozen evidence is
  collected (the TNN-2 freeze is still running). This produces a
  deletion plan, not a compression implementation.
- No em dashes (byte-verified before commit).
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md` zero-diff.
- No sealed FW1-FW9 accessed.
- Explicit pathspecs only.
