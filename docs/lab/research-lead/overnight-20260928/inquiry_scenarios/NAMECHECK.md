# NAMECHECK: Inquiry Scenario Designer

## Step 0: Toolchain guard (mandatory, recorded)

- Safebin setup executed: `~/safebin` populated with 36 allowed tools
  (coreutils, git, pinned znc). `export PATH="$HOME/safebin"`.
- Verification: `which python3 python` returned nothing (empty output
  before `guard-check-done`). No Python or other forbidden executable
  is reachable in this worker's PATH.
- All work in this directory: file reads (`git show`, `grep`, `sed`
  for context recovery), file writes (design documents), git
  operations (add, commit with explicit pathspecs). Zero computation
  performed; this is a design-only task.
- No forbidden executable was invoked. If one had been, this worker's
  output would be PROCESS-FAIL per the governance ruling.

## Scope

Design ONLY. This worker produces a DRAFT-NOT-FROZEN scenario design
document for the TNN-3 inquiry kill bars. It does not freeze any bar,
implement any mechanism, run any evaluation, or modify any source.

## Input provenance

All scenario content is derived from committed repository documents,
read read-only:

- `tnn3_killbars/TNN3_KILLBARS_DRAFT.md`: existing K-T3-INQ-1..4 bar
  text (INQ-3 quoted verbatim in the draft, per Q4).
- `tnn3_killbar_review/KILLBAR_REVIEW.md`: Q1 recommendation (raise
  inquiry to 5+ scenarios), Q2 (topology log format), Q3 (one fixed
  structural signature function), Q4 (retain INQ-3 as drafted),
  Q5 (kill bars, not falsifiers), achievability and non-redundancy
  analysis.
- `tnn2_redteam_inquiry/INQUIRY_REDTEAM.md` (commit `4e329c772`):
  the six-link causal chain; L3 hardcoded (constant 30/-999) and
  L6 absent (no resolution/supersession).
- `tnn2_inquiry_generalization/INQUIRY_GENERALIZATION.md`
  (commit `dedfad368`): derived-question sketch, the
  letter-vs-spirit gap (K-T2-4/K-T2-5 tested chain structure,
  not question content), confirmation-shaped local attractiveness.
- `h2_prereg/H2_PREREG_FROZEN.md` (commit `c15a47d63`): Q1 targets
  inquiry bars not K-H2; `t2_sig` frozen specification and
  calibration properties (i)-(iii); SIG log line format.
- Micah's rulings 2026-10-01: accept Q1-Q6 recommendations; frame
  as kill bars; retain INQ-3 as drafted; retain C0-A regression bar;
  do not freeze full TNN-3 prereg yet.

## Constraints honored

- DRAFT-NOT-FROZEN: the design document is explicitly marked draft.
  Freezing is Micah's decision, not this worker's.
- No implementation, no source edits, no binary built, no evaluation
  run.
- Zero em dashes (to be byte-verified before commit).
- Paper untouched (`TNN_RESEARCH_PAPER_20260929.md` zero-diff).
- No sealed FW1-FW9 or H2 world contents inspected.
- Commits local, explicit pathspecs, owned path only. Nothing pushed.
