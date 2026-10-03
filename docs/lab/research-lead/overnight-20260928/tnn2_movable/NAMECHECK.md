# NAMECHECK.md: Movable Decisions Prioritizer

## Step 0: Toolchain Guard

- Date: 2026-10-01
- Safebin activated: `$HOME/safebin` created, 19 tools symlinked (git, znc, sh,
  bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum,
  git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"` applied.
- `which python3 python` returned nothing. Guard check: PASS.
- No forbidden executable invoked during this task.

## Scope

- Analysis only. No implementation, no source edits.
- Owned path: `docs/lab/research-lead/overnight-20260928/tnn2_movable/`
- Read-only inputs:
  - `docs/lab/research-lead/overnight-20260928/tnn2_dof/DEGREE_OF_FREEDOM_MAP.md`
    (commit `d2af26581`)
  - Frozen TNN-2 source `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
    (commit `f4de7ff46`) consulted for line references only; not modified.
- Paper untouched: `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`
  not read, not modified.
- No em dashes used in deliverables (verified by byte check before commit).

## Verdict

MOVABLE-PRIORITIES-COMPLETE
