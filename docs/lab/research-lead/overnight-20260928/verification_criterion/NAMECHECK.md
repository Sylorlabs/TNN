# NAMECHECK: Verification Criterion Analyst

## Step 0: Toolchain guard

- Safebin activated: `export PATH="$HOME/safebin"` run at session start.
- `which python3 python` returned nothing (no forbidden executables in PATH).
- Zero forbidden executables invoked during this task.
- All work: file reads (`muse.read`), text search (`grep`, `sed` via safebin shell), git inspection (`git show`, `git log`, `git cat-file`).
- No binaries compiled. No Zag code written. No source modified.

## Scope

- Analysis ONLY. Read-only white-box of frozen TNN-2 (`tnn2_build/tnn2.zag`, build `f4de7ff46`).
- This task analyzes the verification problem space. It does NOT design an implementation.
- No sealed world contents inspected. H2 worlds referenced only via the published H2_EVAL_REPORT.md and hash references.

## Input provenance

- Criterion mechanism inventory: commit `8a2ff4b77` (`criterion_mechanism/CRITERION_MECHANISM.md`), 7 decision points D1-D7.
- Plan constructor analysis: commit `61402fd25` (`plan_constructor/PLAN_CONSTRUCTOR_ANALYSIS.md`), gap G5.
- H2 void report: commit `72173fe11` (`h2_eval/H2_EVAL_REPORT.md`), trial-never-runs finding.
- Frozen source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag` (read-only).
- E-ruling context: `integration_scout/INTEGRATION_SCOUT.md` lines 198-204, 336-341.
- Task context from parent: D4 revision acceptance uses source literal "successful re-execution"; D1 trial acceptance reads harness-supplied `expected`; Micah's invention requirements (SUF AND useful behavior AND learner-internal verification AND revisability AND cognitive reuse).

## Constraints honored

- Analysis only; no implementation, no source edits, no new files outside this directory.
- Zero em dashes in all deliverables (will byte-verify before commit).
- Paper untouched (`docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md` not modified).
- Nothing pushed; commit stays local on `tnn-native-lab`.

## Output

- `VERIFICATION_CRITERION.md`: inventory of all verification/acceptance checks in TNN-2, definition of learner-internal verification, candidate mechanisms with failure modes, gap analysis, H2-void relation.
- This NAMECHECK.md.
