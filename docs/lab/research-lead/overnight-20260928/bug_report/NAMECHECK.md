# NAMECHECK.md

## Step 0: Toolchain Guard (mandatory)

- Activated: `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh` equivalent
  (manual safebin construction, same 36-tool allowlist).
- `export PATH="$HOME/safebin"` active for all commands below.
- `which python3 python` returned NOTHING (no output before `guard-check-done`).
- Zero forbidden executables invoked. All commands were: mkdir, ln, which, grep, sed,
  git, sha256sum, cat (reads only).
- Safebin tools used: git, grep, sed, mkdir, ln, cat, sha256sum.

## Task scope

Bug Reporter: document the revision-corruption bug found by the boundary mapper
(commit `8d763d766`, Surprise 1, probe pE E4). Report only; DO NOT fix the bug.
TNN-2 is frozen; the bug is recorded for TNN-3 to avoid.

## Input provenance

- `docs/lab/research-lead/overnight-20260928/tnn2_boundary/BOUNDARY_MAP.md`
  (commit `8d763d766`), read-only.
- Lines read: 102-132 (probe pE E1-E5 readings), 299-309 (Surprise 1),
  311-315 (Surprise 2), 346-350 (recommendation).
- No TNN-2 source, binary, shim, or sealed FW/GW assets modified or executed.
- No sealed contents inspected.

## Deliverables

- `REVISION_BUG.md`: the bug report.
- This file: `NAMECHECK.md`.

## Constraints honored

- Owned path only: `docs/lab/research-lead/overnight-20260928/bug_report/`.
- Report only; no fix attempted.
- Zero em dashes (byte-verified before commit).
- Paper untouched.
- Nothing pushed.
