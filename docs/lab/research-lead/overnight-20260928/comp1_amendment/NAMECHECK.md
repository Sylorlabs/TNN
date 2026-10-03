# NAMECHECK.md: COMP-1 Prereg Amendment Worker

## Step 0: Toolchain guard check

- Ran `which python3 python 2>/dev/null` at wave start.
- Result: `/usr/bin/python3` is present in the default PATH. It is
  an unremovable system binary; I did not invoke it for any purpose
  in this wave.
- Zero forbidden executable invocations this wave.
- All computational checks in this wave used shell only
  (`grep`, `sed`, `wc` on committed files). No Python, C/C++,
  JavaScript, or Rust executed.

## Step 1: Identity

I am the COMP-1 Prereg Amendment Worker. My mission is to draft a
dated prereg amendment documenting the COMP-1 bootstrap's 157-line
actual vs the prereg's 150-line bound, per the red team
recommendation (commit `7ffc2dae4`).

## Step 2: Inputs read

- Frozen prereg: commit `4f6f0c5c8`,
  `composition_prereg/PREREG_COMP1.md` (bound language at the
  One-System accounting section; K1 references the accounting bound).
- Build report: commit `170e39424`,
  `comp1_build/BUILD_REPORT.md` (builder's "+7 variance" framing).
- Red team report: commit `7ffc2dae4`,
  `comp1_redteam/COMP1_REDTEAM_REPORT.md` (Vector 4, process-level
  ATTACK-SUCCESS).
- Committed source: `comp1_build/comp1.zag`, fenced bootstrap
  section lines 459-632; independent shell count = 157 non-blank,
  non-comment lines, matching the red team measurement.

## Step 3: Output

- `COMP1_PREREG_AMENDMENT.md` in this directory (new file).
- This amendment does NOT modify the original prereg. The frozen
  bound stands as written.
- Dash check: byte-verified, zero em dashes in both wave files.
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md`: zero diff
  verified before and after commit.
- Commit uses explicit pathspecs under the owned path only.
