# Preregistration confirmation — strength trial run (Wave 5)

The strength experiment was **APPROVED by Micah** (see MEMORY.md:
"strength trial APPROVED and running (S1 → S10 → S100 per prereg; any
change to rules/schedule/tests/metrics/kill criteria needs Micah's
re-approval)").

This run implements `../wave4/strength-experiment/PREREG.md` and
`TEST_PLAN.md` as written. No change to any of the following:
strength representation or the four legal judgment paths; effort-schedule
constants (25-divisor, stage-50 threshold) or the distinct-citation rule;
justification enum; curriculum closed-form sequences, episode lists, or
variant count; metric definitions; any kill/promotion bound in PREREG §5;
arm semantics; scale-leg sizes; the learner policy rules; the
pressure-demand schedule; the force-PIN contract.

Implementation notes (DESIGN.md) that do NOT require re-registration:
- Audit entry width (16 words incl. op-data d1/d2) and fingerprint format
  — build-system details, explicitly not requiring re-registration
  (PREREG §9).
- The exact trainer id used for force-PIN exercises (id 1) — explicitly
  not requiring re-registration.
- Operationalizations the plan leaves to the builder: the WBS testable
  cohort (right-censoring of horizon-truncated wrong-strong memories),
  stream-level observation of contradiction episodes, earliest-held-first
  citation order, per-(slot,episode) DUPCITE scope, the single-audited-
  abandonment when the held contradiction set is empty, and the
  mid-mimicry corroboration implementing JI entrenchment. All are
  documented in DESIGN.md and flagged in the final report for Micah to
  ratify. If Micah judges any of these to be a material change, the
  affected cells will be re-run under an amended prereg.

First execution of any trial binary is the trial result (no pre-approval
validation runs were performed; the GATE cell runs first per TEST_PLAN
§10 and stops the trial on any mechanism assertion failure).
