# D3 reconciliation — z.ai `recall-harm-q1` vs VERDICT2

**Date:** 2026-09-27 | **Status:** substantive — amends VERDICT2's K1 row, not its evidence

## The tension

z.ai (GLM-5.3) audited the ORIGINAL phase-2 record against frozen PREREG2 K1 and found
D3 mis-scored; VERDICT2 (commits `e811b9515`/`7b5b694e`) labels D3 "moderate harm" on the
same numbers (45,084 / 52,000) and carries K1 as PASS.

## What the frozen bar actually says

PREREG2 (`docs/lab/invention/survival/PREREG2.md`, frozen at `20c5302e2`), K1:

> Reflexive-recall harm (**R_home ≤ Z, or R_home < 0.8×R_true** in shifted regimes)
> replicates in FEWER than 2 of the 3 domains → KILL H1.

## D3 under the frozen predicate

| Check | Value |
|---|---|
| R_home / R_true | 45,084 / 52,000 = **86.7%** |
| 0.8 × R_true | 41,600 — R_home > 41,600 → prong 2 fails |
| Z_D3 | **unreported** in BAR_RESULTS2, EVIDENCE2, and the follow-up (D3 agents reused from phase 2) → prong 1 unresolvable |
| Verdict under frozen predicate | **NO HARM** |

z.ai's audit is **correct**. The phase-2 record itself is where the mis-application
happened: `BAR_RESULTS2.md` line 27 scores D3 harm = **"Yes"** on a descriptive
"degradation" label (45,084 vs 52,000), never applying the frozen predicate. VERDICT2
inherits that label as "moderate" without re-auditing it.

## Corrected scorecard on the frozen 3-domain denominator

| Domain | Frozen-predicate harm? |
|---|---|
| D2 | **Yes** (−1,500 < 0.8×4,500; below chance) |
| D3 | **No** (86.7% ≥ 80%; Z unreported) |
| D1 (original) | No — and VERDICT2 itself agrees the legs were void/mismeasured |

**1 of 3 → K1 FIRES → KILL H1** on the frozen experiment. The committed "2 of 3, PASS"
was invalid, exactly as z.ai states.

## What VERDICT2's K1 row gets wrong

VERDICT2's kill-bar table reads `K1 harm <2/3 domains → PASS`, justified by "Evidence
stronger than claimed (new D1 4/4, D4)". Two deviations from the frozen bar:

1. **Inherited D3 mis-score** — D3 is counted as harm descriptively, not per-predicate.
2. **Silent re-denominator** — the new D1 shifts and D4 were not part of the frozen
   experiment. Counting them toward "≥2 of 3" re-scopes the frozen bar with no prereg
   amendment. (The follow-up *does* apply the frozen predicate honestly to the new
   domains — GENERALIZATION2's D4 table reports Z and classifies per-predicate — so
   the new evidence itself is sound; it is the bar-verdict bookkeeping that is off.)

## What stands, what amends

- **Stands:** VERDICT2's evidence — D2 severe harm, 4/4 new D1 shifts severe (the
  first D1 shifts that actually bite), D4 harm per the frozen predicate, D_wrongKB 81%,
  repair generalizes as a mechanism where the agent survives ~10 samples. The Q1
  headline "harm broader than the committed result" is defensible **as a descriptive
  scientific claim** on the extended evidence set.
- **Amends:** the K1 row. Honest entry: **K1 (frozen, 3-domain denominator) = KILL at
  1/3** — the original D3 score was a predicate mis-application and the original D1
  was void. The new-domain evidence supports H1 descriptively but does not convert
  the frozen bar to a PASS; converting it would require a dated prereg amendment
  (Micah's sign-off), not a verdict-table qualification.
- **Unresolved either way:** Z_D3. If a committed run ever reports Z_D3 ≥ 45,084, the
  chance prong would flip D3 to harm under the frozen predicate (2/3 with D2, D1 void).
  Until then, D3 = no harm per the frozen rule.

## Recommended amended K1 row for VERDICT2

| Bar | As written | Corrected |
|---|---|---|
| K1 harm <2/3 domains | ~~PASS~~ | **KILL (frozen denominator, 1/3)** — D3 mis-scored in phase-2 record (86.7% ≥ 80%, Z unreported); original D1 void. New-domain evidence (D1-new 4/4, D4) supports H1 descriptively; promoting it to a bar PASS needs a prereg amendment. |
