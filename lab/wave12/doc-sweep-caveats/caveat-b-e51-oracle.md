# Caveat (b): the E51 oracle caveat on expressivity readings

**Date:** 2026-09-20
**Verdict: RESOLVED — the caveat is stated in the corpus in its own words (program
charter, arc report, E51AH result, and the oracle reports themselves).**

## What the oracle caveat is

In E51AE and E51AG, an evaluator-only oracle **assigned `success=1` by construction**:
the evaluator computed the correct action itself rather than scoring the learner's
actually-selected action through grounded consequences. The September 4 qualification
(recorded in the program charter and repeated in the arc report and E51AH result)
states that these oracle counters **do not independently establish expressivity**.

Exact corpus language:

`docs_local/0482_R32_E51_PROGRAM_CHARTER.md`, "Current frontier at charter creation":

> "September 4 qualification: historical E51AE/E51AG oracle counts were assigned
> success by construction. They do not independently establish expressivity."

`docs_local/0501_R32_E51AC_AH_ARC_REPORT.md`, "An additional evidence boundary matters":

> "Historical E51AE/E51AG oracle counters assigned success by construction. Their
> learned/control comparisons remain usable, but the oracle counters are not
> independent proof of action expressivity."

`docs_local/0060_R32_E51AH_RESULT.md`, "Causal closure and limitations":

> "Historical E51AE/E51AG oracle counters were assigned success by construction.
> Their measured learned/control comparisons remain evidence, but the counters
> do not independently establish candidate expressivity. E51AH corrected its own
> oracle before execution, but the sealed branch did not execute and supplies
> no new expressivity evidence."

The oracle reports self-qualify: `docs_local/0056_R32_E51AG_RESULT.md`, line 25:
"an independent expressivity test. This qualification supersedes oracle-based
expressivity inferences in this report, not the observed learned/control [comparisons]."

## What it qualifies

- **Qualified:** expressivity inferences drawn from the E51AE/E51AG oracle counters
  (and, by extension, any reading that cites them as proof the learner can express
  good solutions). E51AH adds no expressivity evidence of its own — its oracle was
  corrected but the sealed branch never executed (E51AH never passed development
  eligibility; validation/confirmation stayed at 0/5400 and 0/10800).
- **NOT qualified by this caveat:** the measured learned-arm vs control comparisons in
  E51AE/E51AG ("Their learned/control comparisons remain usable"), and E51X's exact
  terminal reachability (5,400/5,400 untouched validation; 8,400/8,400 known +
  2,400/2,400 no-unique sealed confirmation) — E51X scored the learner's selected
  actions, so it is actually-measured behavior, not an oracle assignment.
  (E51T is an optimization-dose comparison, also actually measured.)
- **Related direction:** E51Z (the stopping-state oracle audit, `docs_local/0104_R32_E51Z_RESULT.md`)
  is a separate evaluator-only oracle exercise; the arc report's prescription is
  "Score evaluator-only candidate choices through their actual grounded consequences;
  do not manufacture an exact oracle counter."

## Quotable qualification paragraph

> **E51 expressivity qualification (R32 program charter, Sept 4 qualification):** The
> historical E51AE/E51AG oracle counters were *assigned success by construction* — an
> evaluator-only oracle computed the correct action itself rather than scoring the
> learner's selected action through grounded consequences. The oracle is exact, so it
> establishes that the candidate-action interface **is capable of expressing** a perfect
> solution on the tested partitions — but it does **not** establish that the learner can
> reach or select that solution, and it is not independent proof of action
> expressivity. The measured learned-arm vs control comparisons in E51AE/E51AG remain
> usable evidence; only expressivity inferences from the oracle counters are
> superseded. E51AH corrected its own oracle before execution but its sealed branch
> did not execute, so E51AH supplies no expressivity evidence. E51X's exact terminal
> reachability (5,400/5,400 untouched validation; 8,400/8,400 known + 2,400/2,400
> no-unique sealed confirmation) is actually-scored selected-action measurement and
> is unaffected by this caveat.

## What the failure actually was (for context)

Per the charter: "The candidate-action oracle is exact, so the next causal branch
concerns **evaluator-blind discrimination and preservation, not candidate
expressivity**" — i.e., the tested additive candidate residual failed because the
evaluator-blind learner could not reliably distinguish when candidate correction was
beneficial from when the mature union should be left unchanged, especially on
no-unique cases.
