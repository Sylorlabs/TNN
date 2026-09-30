# CHURN-REVISION RESULT

Worker: Newcomer-Churn Revision Worker
Date: 2026-09-30 PDT
Prereg: PREREG_CHURN.md (18fb10434), frozen before implementation.
Status: COMPLETE

## Verdict

**CHURN-REVISION-PASS**

All three kill bars pass. The experiment answered the frozen question, and
the answer is the falsifier branch: the churn hypothesis is REJECTED for
this regime. The current policy is fine; no variant adoption is recommended.

## What was tested

Whether useful-but-not-yet-queried knowledge is churned before its first
query under the consequence eviction policy. Design: 12 foundation rules
(queried, earned), 10 Group A newcomers (queried 2x, earned), 10 never-
queried sleeper newcomers, then a 30-item pressure wave, then a delayed
first-use probe of the sleepers plus 4 two-hop compositions routing through
sleeper premises, then a recovery phase, then a final probe. Two arms with
identical trajectories: control (FIFO tie-break, the current policy) and a
LIFO-tie variant (among minimum-importance slots, evict the highest slot
index).

## Measurements (3/3 byte-identical runs per arm, exit 0, zero stderr)

Control arm (POLICY=0):
- C1 foundation recall: 12/12
- C2: sleepers 10/10 present, Group A 10/10 present
- C3 after 30-item pressure wave: sleepers 9/10, Group A 10/10,
  foundation intact, flood retained 5/30
- C4 delayed first-use probe: SURV_SLEEP 9/10, COMP_FIRST 3/4
  (the one failed composition routed through the single churned sleeper)
- C5 recovery: RELEARN_OPS 1, flood victims 1, earned victims 0,
  foundation victims 0, COMP_RECOV 4/4
- C6 final: foundation 12/12, Group A 10/10, FOUND_EVICT 0

LIFO-tie variant (POLICY=1):
- C3: sleepers 10/10, Group A 10/10, flood retained 4/30
- C4: SURV_SLEEP 10/10, COMP_FIRST 4/4
- C5: RELEARN_OPS 0, COMP_RECOV 4/4
- C6: foundation 12/12, Group A 10/10, FOUND_EVICT 0

## The prediction miss and what it revealed

The prereg predicted control sleepers 0/10 (FIFO tie-break churning the 10
oldest importance-1 slots). Observed: 9/10. The EVICT log shows why. The
first eviction took sleeper (40,20), the lowest-index importance-1 slot.
Every subsequent eviction then hit that same slot index again, because the
replacement flood item sitting there was again the lowest-index
importance-1 slot. The log reads: EVICT 40 20, then EVICT 304 99,
305 99, 306 99, ... 328 99. One slot became a revolving door that absorbed
all 25 remaining evictions; the other 9 sleepers were never touched.

Mechanism finding: under sustained single-wave pressure, the current
policy sacrifices exactly one unproven newcomer (the oldest unproven at
the lowest slot index) and then churns each new arrival against the
revolving door. Pre-existing never-queried newcomers are therefore NOT
churned aggressively: 9/10 survived a 30-item wave with zero queries.

## Kill-bar evaluation

- K1 (prereg precedence): PASS. Prereg 18fb10434 strictly precedes the
  implementation commit (verified with git merge-base --is-ancestor).
- K2 (churn question answered): PASS. Both arms completed all 6 phases;
  never-queried vs queried churn rates measured (control 9/10 vs 10/10;
  variant 10/10 vs 10/10); first-probe utility measured (control 3/4,
  variant 4/4); recovery cost measured (control: 1 re-learn, 1 flood
  victim, 0 earned/foundation victims; variant: no-op); the policy-fine
  falsifier TRIGGERED (control SURV_SLEEP 9/10 >= 5/10), so per the frozen
  prereg the churn hypothesis is rejected for this regime, the policy is
  fine, and no variant adoption is recommended. The variant's 10/10 vs
  9/10 margin is reported as an observation, not an adoption case: the
  frozen bar blocks adoption when the falsifier triggers, and a one-item
  margin on a rejected hypothesis does not clear a meaningful superiority
  bar.
- K3 (purity and determinism): PASS. Pure Zag, zero Python at every step
  (build, runs, and all analysis used only znc, shell, grep, cmp,
  sha256sum). 3/3 byte-identical runs per arm, exit 0, zero stderr. No em
  dashes (check_no_dash.sh clean on all docs).

## Honest scope notes

- The POLICY flag is a researcher-set build constant, not learned; the
  variant is a researcher-authored policy change.
- Exact-match retrieval only; integer-coded episodes; synthetic world.
- The falsifier threshold (5/10) and the single-wave regime were frozen in
  the prereg; the rejection applies to this regime, not to all possible
  pressure patterns.

## Recommendation (next step for this lane)

Keep the current consequence policy; do not adopt the LIFO-tie variant on
this evidence. The sharper follow-up is an EPISODIC-pressure experiment:
multiple separated pressure waves with the surviving flood items queried
(earned) between waves. The revolving-door finding predicts each new
episode sacrifices the next-lowest-index unproven newcomer, so repeated
episodes could slowly bleed sleepers that a single wave spares. That
experiment tests the hypothesis in the regime where it might actually
hold, and it directly extends the mechanism found here rather than
re-litigating the settled single-wave case.
