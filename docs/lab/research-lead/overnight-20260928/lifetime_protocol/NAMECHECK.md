# NAMECHECK: Lifetime Evaluation Protocol Designer

## Step 0: Toolchain Guard (mandatory, recorded first)

- Safebin setup: ran `~/safebin` bootstrap linking 36 allowed tools
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc,
  cmp, sha256sum, git-receive-pack, git-upload-pack, and other coreutils).
- `export PATH="$HOME/safebin"` active for all work below.
- Verification: `which python3 python` returned nothing (empty output
  before "guard-check-done"). No Python or other forbidden interpreter
  is resolvable in this worker's PATH.
- All work in this task: file reads (existing protocol documents,
  transfer analysis), document authoring, git operations.
- Zero forbidden executables invoked. If any had been, this wave would
  be PROCESS-FAIL per the worker toolchain guard.

## Scope

Design ONLY the LIFETIME evaluation protocol per Micah's 2026-10-01
architecture clarification (continuous adaptive learner; freeze researcher
code, not learner state). No implementation, no world building, no source
changes, no binary builds, no sealed content created.

## Input provenance (read-only, used for grounding)

- Micah's 2026-10-01 07:17 PDT architecture clarification message
  (parent context): frozen researcher code plus continuously changing
  learner state; lifetime stream A to B to C to D to return-to-A;
  8 required measures; freeze/do-not-freeze lists; isolation vs lifetime
  reporting; continuous operation directive.
- `lifetime_race/RACE_PREREG.md` (frozen 2026-09-30): existing sealed
  multi-world lifetime race, stages A through L, TNN vs LLM framing.
  This protocol is related but distinct: it evaluates one frozen
  architecture's learner-state continuity, not a TNN vs LLM contest.
- `tnn2_transfer/TRANSFER_ANALYSIS.md` (2026-10-01): TNN-2 learner state
  is workspace W (110656 bytes); MAP nodes (type 20) persist with
  provenance; no query path executes stored MAPs; graphs are
  subject-bound (literals baked in); cross-task behavior is rebuild,
  not invocation; revision rewrites MAPs in place.
- `reuse_experiment/` (commit ea8fc0ac1, 2026-10-01): unfrozen variant
  with MAP-first query lookup; R1 confirmed MAP execution on re-query;
  R4 confirmed fresh subjects still rebuild (value-trace limitation
  intact). Honest scope: mechanical reuse works, cross-subject transfer
  still rebuilds.
- `h2_prereg/H2_PREREG_FROZEN.md` (commit c15a47d63, 2026-10-01):
  K-H2-1..4 frozen; evaluator authorized for sealed H2A/H2B/H2C;
  driver-side harnesses only; byte-identical determinism required.
- Standing architectural metric (12 fields) per Micah's 2026-10-01
  ruling: reported for this design where applicable.

## Constraints honored

- Design document only (DRAFT-NOT-FROZEN). Nothing in this task
  implements, builds, or runs anything.
- No em dashes in any authored file (will byte-verify before commit).
- Paper untouched: `docs/lab/research-lead/overnight-20260928/
  TNN_RESEARCH_PAPER_20260929.md` never opened for edit.
- No sealed FW or H2 contents inspected.
- Commits local only. Nothing pushed (only Micah pushes).
- Explicit pathspecs on all git operations.
