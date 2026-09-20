# INT-1 C7 — Deep-Dive: Why the Draft Metric Was Withdrawn (2026-09-20 ~02:00 UTC)

## Status

The draft C7-metric amendment (`DRAFT_AMENDMENT_2026-09-20-C7-METRIC-REDESIGN.md`)
is **WITHDRAWN**. It is incoherent: its prose formula and its expected re-score
disagree (880 vs 897 for DC-4). The independent checker caught this. §5 FAIL
stands. **S100 stays gated** (§9 binding). No further metric patching will be
attempted — the red team's warning is vindicated.

## The deeper mechanism (beyond the initial confound analysis)

The independent checker (`RESCORE_C7_CHECKER_2026-09-20.md`, commit `4ce4ba72`)
independently reproduced the re-score and found a second layer:

**1. Budget displacement (sign-flip).** The `o2_cap` claim-id budget is binding
and shared. The 17 forced hypotheses in DC-4 did not just *add* to the count —
they **displaced 17 proactive hypotheses 1:1** (proactive 639→622 in DC-4;
`met.hypotheses` flat at 639). So the gate's true autonomy effect in DC-4 was
−17 proactive (crowding out), while the old metric showed +17 (via `tr.l1_opened`).
The old metric got the **sign wrong** for autonomy.

**2. Double-counting.** The old metric sums `met.hypotheses` (639, which already
includes the 17 forced) **plus** `tr.l1_opened` (17) — L1 hypotheses are counted
twice. This predates the C5 redesign (baseline DC-2 had 12 double-counted) but
was symmetric until the gate fired asymmetrically.

**3. The draft's incoherence.** Two readings of "exclude forced hypotheses":
- *Subtraction reading:* 914 − 17 = 897 → 897→897 PASS. But this keeps the 17
  forced inside the 639 — it fixes the double-count, not the autonomy definition.
  Inconsistent with the draft's own prose.
- *Literal reading* (`hypotheses_autonomy` = proactive + elected = 622 + 0):
  256+2+622 = **880** vs DC-5 **897** → 897→880, bar `==` FAILS (in the
  cap5>cap4 direction — the opposite of teacher-dependence).

The draft's prose promised one thing; its expected numbers assumed another.
Withdrawn.

## What this means

- **No teacher-dependence.** DC-5 autonomy (639 proactive) = baseline DC-5 (639).
  Positive control convicts (897→641, composites-only collapse). The substantive
  fear C7 guards against did not materialize. This evidence is committed and stands.
- **Real gate cost (telemetry, not a bar failure).** The C5 gate crowds out ~17
  proactive hypotheses per firing stage via the shared budget (composites
  unaffected: 1024=1024). Known tradeoff of the redesign; recorded, not hidden.
- **C7's within-run bar is unsatisfiable under asymmetric mechanisms.** Any
  mechanism that fires differently across stages (gate × curriculum interaction)
  breaks the `cap5 == cap4` comparison — in either direction. This is a
  **control-design flaw**, not a patchable metric bug. Three formulations have
  now been tried post-hoc (subtraction, literal, double-count-fix); each
  revealed another layer. Patching is over.

## Redesign space (for the real C7 redesign — not attempted tonight)

1. **Non-inferiority bar.** "Survives withdrawal" is a non-inferiority claim, not
   an equality claim. `cap5 >= cap4` (withdrawn not impaired) is the correct
   statistical formulation; `==` was always the wrong test. (Bar change; needs tap.)
2. **Budget separation.** Separate claim-id budgets for forced vs proactive
   hypotheses (system change) eliminates displacement; then forced-exclusion is
   coherent. (Mechanism change; needs fresh run.)
3. **Drop the double-count.** `cap` = composites + commits + `met.hypotheses`
   (each hypothesis counted once). Fixes the objective bug; symmetric.
4. **Split the control.** C7a (withdrawal proper) vs C7b (mechanism-asymmetry
   telemetry with its own displacement bar).

## Recommendation

Keep S100 gated pending a real C7 redesign (direction 1+3 are cheapest; 2 is
cleanest). The no-teacher-dependence evidence is committed and available should
Micah judge the substantive case sufficient to override — that override is his
call, explicitly, not an automatic un-gating.
