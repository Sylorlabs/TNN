# NAMECHECK: TNN-2 Alternative-Explanation Attack

Date: 2026-09-30 (PDT). Step 6 of the TNN-2 promotion pipeline.

## Step 0: Toolchain guard

- `mkdir -p $HOME/safebin`; symlinked allowed tools
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk,
  wc, cmp, sha256sum, git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"` applied before all work.
- Guard check: `which python3 python` returned nothing.
  Output line `guard-check-done` confirmed.
- Verdict: TOOLCHAIN-GUARD-PASS. No forbidden executable invoked.
  This worker is analysis only; no computation performed.

## Scope

- Owned path: `docs/lab/research-lead/overnight-20260928/tnn2_altexp/`
- Read-only on the three red-team reports (commits `340e94e3e`,
  `4e329c772`, `687ba0219`); no edits to them.
- TNN-2 source, shim, scorer, ISA, worlds, interpretation rules:
  untouched.
- Contaminated paper (`TNN_RESEARCH_PAPER_20260929.md`): untouched.
- This is pipeline step 6 (alternative-explanation attack). It does
  not promote or demote TNN-2, and does not alter any prior verdict.

## Target red-team verdicts under attack

- Construction `340e94e3e`: CONSTRUCTION-ATTACK-SUCCESS
  (finite templates; verifier uses environment-supplied expected).
- Inquiry `4e329c772`: INQUIRY-ATTACK-SUCCESS
  (L3 discriminating need hardcoded as 30/-999; L6 absent).
- Revision `687ba0219`: REVISION-ATTACK-SUCCESS
  (single-schema literal-patch; learner chooses operands only).

## Deliverables

- `NAMECHECK.md` (this file)
- `ALTERNATIVE_EXPLANATIONS.md`

## Commit

- Explicit pathspecs under `tnn2_altexp/` only.
