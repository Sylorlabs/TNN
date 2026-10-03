# NAMECHECK: Composition Design Amender (R1)

## Step 0: Toolchain guard (mandatory)

- Safebin activated at task start: `mkdir -p $HOME/safebin`, symlinked
  the 19 allowed tools (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat,
  grep, sed, awk, wc, cmp, sha256sum, git-receive-pack, git-upload-pack),
  exported `PATH="$HOME/safebin"`.
- Verification: `which python3 python` printed nothing (only the
  guard-check-done echo). Zero forbidden executables invoked.
- This worker performed: file reads (design + red-team report),
  file writes (amendment document + this NAMECHECK), git operations
  (commit with explicit pathspecs). No computation, no binaries built,
  no evaluators run, no source modified.

## Step 1: Scope

- AMENDMENT ONLY. No implementation. No source edits to any TNN
  variant (frozen or unfrozen). No binaries built. No evaluators run.
  No sealed contents inspected.
- The composition memory design remains DRAFT-NOT-FROZEN. This
  amendment does not freeze it and does not authorize implementation.
- Addresses red-team recommendation R1 (`3eeb0d78e`): specify
  SETREG-provenance through extraction and splice.

## Step 2: Input provenance

- Composition memory design `19fa59b6f`
  (docs/lab/research-lead/overnight-20260928/composition_memory/COMPOSITION_MEMORY_DESIGN.md),
  read-only, unmodified.
- Red-team assessment `3eeb0d78e`
  (docs/lab/research-lead/overnight-20260928/composition_redteam/COMPOSITION_REDTEAM.md),
  verdict VULNERABLE, recommendations R1-R4.
- V2-hole probe `705833a27` (CONFIRMED), via the red-team report's
  summary. No new probing performed by this worker.
- No new empirical claims. All numbered claims referenced are from
  committed prior work.

## Step 3: Decision summary

Adopted the third option beyond the red team's (A)/(B): provenance
rebinding at splice time. Extraction preserves SETREG provenance as
historical metadata (F-setreg-hist, read-only). Splice rebinds each
SETREG's prov edge to the actual data source (live fact f_new) or
nulls it (default-filled constant). R2 criterion fix required as a
build prerequisite. Revision operates on composites, not fragments;
fragment quality via F-utility. Four-part kill bar K-COMP-REV-1
through K-COMP-REV-4 specified for the contrast test's revision leg.

## Step 4: Constraints honored

- Zero em dashes in the amendment document (byte-verified: grep for
  U+2014 returned 0).
- Paper untouched:
  docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md
  not read for editing, not modified.
- Nothing pushed. Local commit only, explicit pathspecs, owned path
  only (composition_memory/ directory).

## Verdict

COMPOSITION-AMENDMENT-COMPLETE.
