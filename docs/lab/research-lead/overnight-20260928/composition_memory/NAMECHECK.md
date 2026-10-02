# NAMECHECK: Composition Memory Designer

## Step 0: Toolchain guard (mandatory)

- Safebin activated at task start: `mkdir -p $HOME/safebin`, symlinked
  the 15 allowed tools (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat,
  grep, sed, awk, wc, cmp, sha256sum, git-receive-pack, git-upload-pack),
  exported `PATH="$HOME/safebin"`.
- Verification: `which python3 python` printed nothing (only the
  guard-check-done echo). Zero forbidden executables invoked.
- This worker performed: file reads (background research), directory
  creation, file writes (design documents), git operations (commit).
  No computation, no binaries built, no evaluators run.

## Step 1: Scope

- DESIGN ONLY. No implementation. No source edits to any TNN variant.
  No binaries built. No evaluators run. No sealed contents inspected.
- H1 deferral respected: Micah's 2026-10-01 ruling defers H1 / open
  construction until H2 evidence lands ("Do not expand from 3 templates
  to 30 templates"). This design is preparation for the
  entrance-criterion-satisfying direction, not construction work. It
  does not begin H1 implementation and does not request H1 resources.

## Step 2: Input provenance

- SUF formalization `7dddf3933` (section 6 hypothetical PASS example:
  composition memory; section 3 testable criterion; section 7 evidence
  bar; section 8 continuous-learner reading).
- Micah's 2026-10-01 rulings: H1 deferred with SUF as entrance
  criterion; protected-core Alternative C; continuous-learner
  clarification (freeze researcher code, not learner state); standing
  architectural metric (12 fields); H2-before-H1 ordering.
- H3-lite prereg draft `dab50dd68` (policy nodes do NOT establish SUF;
  the menu-size distinction).
- Reuse-path experiment `ea8fc0ac1` (MAP-first query; shadow-fact
  deletion; value-trace limitation persists).
- No new empirical claims. All numbered claims referenced are from
  committed prior work, not from this worker.

## Step 3: Constraints honored

- Zero em dashes in both deliverable files (will byte-verify before
  commit).
- Paper untouched:
  docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md
  not read for editing, not modified.
- Nothing pushed. Local commits only, explicit pathspecs, owned path
  only.

## Verdict

COMPOSITION-MEMORY-DESIGN-COMPLETE (pending commit).
