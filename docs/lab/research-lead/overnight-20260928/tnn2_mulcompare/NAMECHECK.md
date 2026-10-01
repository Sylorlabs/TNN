# NAMECHECK.md - TNN-2 vs MUL Rung B Comparator

## Step 0: Toolchain Guard (mandatory)

- Safebin activated: `$HOME/safebin` created and populated with 36 allowed
  tool symlinks (coreutils, git, pinned znc).
- `export PATH="$HOME/safebin"` applied for all worker commands.
- `which python3 python` returns nothing (exit 127 path, verified
  2026-10-01). No forbidden executable resolves in the worker PATH.
- This assignment is analysis only: no binaries were executed, no
  research computation was performed, no code was compiled. All findings
  below come from reading frozen committed reports and sources.
- Zero invocations of python3, python, C/C++, JavaScript, or Rust.
- Guard status: PASS. No PROCESS-FAIL.

## Scope and provenance

- Task: compare TNN-2's `t2_trial` construction with MUL Rung B's
  two-level construction; answer the five frozen questions.
- Owned path: `docs/lab/research-lead/overnight-20260928/tnn2_mulcompare/`
  (this directory only).
- Read-only sources (not modified):
  - MUL Rung B build report and source: `mul_rungb_build/BUILD_REPORT.md`,
    `mul1b.zag` (builder commit `a2223cc11`).
  - MUL Rung B prereg: `mul_rungb_prereg/MUL_RUNGB_PREREG.md`
    (frozen `3ce154801`).
  - TNN-2 build report and source: `tnn2_build/TNN2_BUILD_REPORT.md`,
    `tnn2.zag` (builder commit `f4de7ff46`).
  - TNN-2 prereg: `tnn2_prereg/TNN2_PREREG.md` (frozen `7c1e30522`).
  - Construction red team: `tnn2_redteam_construction/CONSTRUCTION_REDTEAM.md`.
- The contaminated paper (`TNN_RESEARCH_PAPER_20260929.md`) was not
  touched. No em dashes used in worker documentation.

## Verdict

MUL-COMPARISON-COMPLETE. Analysis delivered in MUL_COMPARISON.md.
