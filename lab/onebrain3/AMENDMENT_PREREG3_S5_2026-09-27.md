# Amendment to frozen PREREG3 §5 (reintegration inputs)

**Date:** 2026-09-27
**Signed:** Micah — "easy fix it" (recorded in `~/workspace/governance_bundle/SIGNATURE_SHEET.md`, item 6, "One stale line in the one-brain plan")
**Status:** ENACTED. This amendment supersedes the named line of the frozen text.
The frozen `PREREG3.md` is **not** edited in place; its original wording stands as
historical record.

## The change

PREREG3 §5, line 235, reintegration stage "Inputs (ledger only)":

- **Before (frozen text, unchanged):** "...sub-deliberation agreement (branch winners, margins)."
- **After (amended):** "...sub-deliberation agreement (branch winners)."

## Why

The branch-margin fields (ledger row 0 offsets @56/@64) were deleted from the
implementation by fix-or-kill commit `a7f77b25b` (2026-09-27) after an exhaustive
audit proved **zero reads anywhere** — no code ever consumed them. Wiring margins
in would have changed the frozen round-3 rules, so the auditor deleted rather
than wired.

## No behavior change

The code deletion predates this amendment and was proven decision-neutral:
Crew M Gate 1 (2026-09-27) showed the post-fix binary's outputs byte-identical
to the measured R3 binary on all 9 modes, with 396/396 per-problem table cells
matching `MEASUREMENT3.md`. This amendment only stops the frozen document from
describing a ledger layout that no longer exists.

## Effect on round-3 evidence

None. The R3 scores, the red-team report, and the frozen verdicts are unaffected:
they were produced by the code as it ran, which never read the margin fields.
