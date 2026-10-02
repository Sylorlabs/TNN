# NAMECHECK: Fragment Record Specifier

## Step 0: Toolchain Guard

- Safebin activated: `$HOME/safebin` created, 16 allowed tools linked
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc,
  cmp, sha256sum).
- `export PATH="$HOME/safebin"` applied.
- `which python3 python` returned nothing. Output: `guard-check-done`.
- Zero forbidden executables invoked. Pure read-only analysis (grep, sed
  over frozen source); no computation required beyond field census.
- Any forbidden executable invocation would have been PROCESS-FAIL.
  None occurred.

## Scope

Specification ONLY. No implementation. No variant built. No code written
beyond these two markdown files.

## Input Provenance

- COMPOSITION_MEMORY_DESIGN.md (`19fa59b6f`): fragment lifecycle,
  F-utility definition, One-System Rule compliance statement.
- AMENDMENT_R1_SETREG_PROVENANCE.md (`bda26cf91`): F-setreg-hist field,
  rebind rule, R2 requirement.
- BUILD_QUESTIONS.md (`97b80383a`): Q3 information gap (this task),
  Q1 splice-trace layout, Q3 ET_FRAGUSE (type 14), Q4 Node 3 interaction.
- Frozen base source: `bootstrap_loop/bl_base.zag` (byte-identical
  verbatim frozen copy, SHA-256 `a29972ca...`). Field census and tag
  census performed read-only against this file. Frozen source unmodified.

## Constraints Honored

- Specification only; no source edits, no variant, no binary.
- Zero em dashes in deliverables (byte-verified before commit).
- Paper untouched (`TNN_RESEARCH_PAPER_20260929.md` not opened).
- No sealed worlds opened.
- Nothing pushed. Commit local only, explicit pathspecs on both
  `git add` and `git commit`.
- Frozen TNN-2 source and frozen preregs read-only, never modified.

## Verdict

FRAGMENT-RECORD-COMPLETE (pending parent review of the specification).
