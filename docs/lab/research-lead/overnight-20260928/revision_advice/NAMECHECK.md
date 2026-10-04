# NAMECHECK: Architecture Advisor (revision)

Date: 2026-10-01 (UTC). Session: Architecture Advisor.
Verdict on completion: REVISION-ADVICE-COMPLETE.

## Step 0: Toolchain guard (mandatory, completed first)

- Ran the safebin setup: `mkdir -p $HOME/safebin`, linked the 17 allowed
  tools (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk,
  wc, cmp, sha256sum, git-receive-pack, git-upload-pack), exported
  `PATH="$HOME/safebin"`.
- `which python3 python` returned nothing. Zero forbidden executables
  invoked during this task.
- All work below is advisory text. No source was modified, no binary was
  built, no Zag was compiled, no experiment was run, no sealed asset was
  inspected.

## Scope

Advise on TNN-3 revision architecture given:
- the revision-corruption bug report (`bug_report/REVISION_BUG.md`,
  commit `8b58c4104`, from boundary map `8d763d766` Surprise 1), and
- the one-shot-per-fact-lineage limit (boundary map Surprise 2,
  probe pE E2/E3).

Advise only. This document changes no design, implements nothing, and
authorizes nothing. Any TNN-3 revision work must go through its own
preregistration with frozen kill bars.

## Input provenance (all read-only)

- `bug_report/REVISION_BUG.md` (commit `8b58c4104`)
- `tnn2_boundary/BOUNDARY_MAP.md` (commit `8d763d766`), probes pE, pY, pZ
- `tnn2_reusepath/REUSE_PATH_DESIGN.md` (commit `5f15b9309`), sections 4, 6
- `tnn2_revision_generalization/REVISION_GENERALIZATION.md`, sections 1-2
- `tnn2_h3lite/H3LITE_DESIGN.md` (commit `22197da2c`), repair dispatcher
- `property_name/PROPERTY_DEFINITION.md` (commit `64eec921f`), SUF
- `reclustering/RECLUSTERING_DRAFT.md` (commit `ed2357141`), R3
- `protected_core_decision/PROTECTED_CORE_BRIEF.md` (commit `092566072`)

## Constraints honored

- Owned path only: `docs/lab/research-lead/overnight-20260928/revision_advice/`.
- Advice only; no design changes, no implementation, no evaluation.
- No em dashes (byte-verified before commit).
- Paper (`TNN_RESEARCH_PAPER_20260929.md`) untouched.
- Nothing pushed. Commits stay local on `tnn-native-lab`.
