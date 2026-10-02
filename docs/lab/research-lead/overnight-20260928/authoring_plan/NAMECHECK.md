# NAMECHECK.md - Authoring Planner

## Step 0: Toolchain guard (mandatory)

- Safebin activated: `$HOME/safebin` created, 36 allowed tools linked.
- `export PATH="$HOME/safebin"` applied.
- `which python3 python` returned nothing (verified: only "guard-check-done" printed, no paths).
- Zero forbidden executables invoked in this session.
- This worker performed planning and documentation only: no Zag compiled,
  no binaries built, no experiments run, no sealed contents inspected.

## Scope

Plan only. This worker drafts the authoring plan for TNN-3 preregistration
items A-G. It does NOT write any preregistration text, freeze any bar,
implement the signature function, or make any banked decision.

## Input provenance

- Prereg readiness checklist: `docs/lab/research-lead/overnight-20260928/prereg_check/PREREG_READINESS.md`
  (committed in `5a009ff87`; verdict PREREG-CHECK-COMPLETE, NOT ready to freeze).
- 10-section outline: `tnn3_prereg_struct/PREREG_STRUCTURE.md` (`206499c03`), section 6.
- Banked decisions compilation: `banked_decisions/BANKED_DECISIONS.md` (`f4f8fa532`).
- Morning schedule: `morning_coord/MORNING_SCHEDULE.md` (`081c9c3a9`).

## Constraints honored

- Owned path only: `docs/lab/research-lead/overnight-20260928/authoring_plan/`.
- Plan only; no prereg text authored.
- Zero em dashes (byte-verified before commit).
- Paper untouched: `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md` not modified.
- No sealed FW/GW/H2 contents inspected.
- Nothing pushed; commit local on `tnn-native-lab`.
