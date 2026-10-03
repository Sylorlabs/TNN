# NAMECHECK.md: Floor Preserver

## Step 0: Toolchain guard

Safebin activated: `export PATH="$HOME/safebin"`.
`which python3 python 2>/dev/null` returned nothing (empty output, guard-check-done).

Zero forbidden executables invoked. This task performed read-only analysis
(`read`, `exec` with `ls`/`grep`/`git` only) and wrote two markdown files.

## Scope

This worker produced a specification only. No implementation, no code,
no execution of research binaries, no modification of TNN-2 source,
shim, worlds, or any evaluated artifact. Read-only on all inputs.

## Inputs (read-only)

- `docs/lab/research-lead/overnight-20260928/gw_eval/GW_EVAL_REPORT.md` (commit `881fbb3d4`, GW-EVAL-COMPLETE, 2/8)
- `docs/lab/research-lead/overnight-20260928/gw_interpretation/GW_INTERPRETATION.md` (commit `42fa993ab`, section 4 "positive evidence")
- `docs/lab/research-lead/overnight-20260928/reclustering/RECLUSTERING_DRAFT.md` (commit `ed2357141`, freeze pass structure)
- `docs/lab/research-lead/overnight-20260928/core_freeze_tnn1_eval/FREEZE_REPORT.md` (TNN-1 freeze, line 90: passing world descriptions)

## Deliverable

- `FLOOR_SPEC.md`: preservation spec for TNN-3 regression testing.

## Constraints honored

- Owned path only: `docs/lab/research-lead/overnight-20260928/floor_preserve/`
- Spec only, no implementation
- No em dashes (byte-verified zero before commit)
- Paper untouched (`docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`)
- Commit with explicit pathspecs, local only, nothing pushed

## Verdict

FLOOR-SPEC-COMPLETE.
