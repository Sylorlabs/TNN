# Sign-off resolution (a) — §7 metric-count interpretation: coherence proof

**Date:** 2026-09-22. **Status:** analysis complete; counting-rule change AWAITS Micah's signature (nothing applied).
**Frozen source:** `units/PREREG_FREEZE.md` (signed 2026-09-21, commit `b0b9140c0eda`), §5/§7.
**Question:** what exactly are the "8 scored metrics" in §7 rules 2 and 4?

## 1. Frozen texts (verbatim)

- **§7 rule 2:** "Section champion (best scorecard value; ties broken by transfer-tax / lower-cost secondary, then co-champions) in **≥ 6 of the 8 scored metrics** (M1–M7 scored; M8 is eligibility only; M9 informational, never counts)."
- **§7 rule 4:** "**N/A discipline:** N/A metrics excluded from numerator and denominator — threshold is ≥ 6 of *applicable* scored metrics, or ≥ 75% of applicable rounded up, whichever is larger (an arm with M7 N/A needs ≥ 6 of 7)."
- **§5 M1:** "Sub-scores: content recall rate … and boundary fidelity …, **recorded separately, never folded**."
- **§5 M6 / M-28:** "champion = smallest transfer tax" — ONE champion for M6 (P→C and C→P are separate scorecard columns, never averaged, but the championship is single).
- **§5 M7:** "Non-ID arms: N/A (no ID layer) … excluded from the arm's blowout denominator (§7 rule 4)."
- **M-40** (signed): "≥ 6-of-8 section championships" — consistent with 8, not 7.

The parenthetical in rule 2 names **7** metrics (M1–M7) and calls them "**8** scored metrics". Exactly one of the seven must contribute two scored columns. The only metric whose internal split is declared non-foldable is M1.

## 2. Candidate readings, tested mechanically

| # | Reading | Total scored | M7-N/A → applicable | Rule 4 computes | Matches "≥ 6 of 7"? | Rule 2 "8" holds? | Other frozen text |
|---|---|---|---|---|---|---|---|
| R1 | M1 split: {M1-content, M1-boundary, M2, M3, M4, M5, M6-tax, M7} | 8 | 7 | max(6, ⌈0.75×7⌉=6) = **6 of 7** | **yes** | **yes** | §5 "never folded" respected; M-28 single M6 champion respected |
| R2 | M1 folded: {M1, M2, M3, M4, M5, M6, M7} | 7 | 6 | max(6, ⌈0.75×6⌉=5) = 6 of 6 | **no** | **no** | — |
| R3 | M1 folded, M6 split P→C/C→P: {M1, M2, M3, M4, M5, M6-P→C, M6-C→P, M7} | 8 | 7 | 6 of 7 | arithmetically yes | yes | **violates** §5 M1 "never folded" (folds the one metric declared non-foldable) and M-28 (one M6 champion); contradicts §7's own tie-break, which treats transfer-tax as a single tie-break input |
| R4 | M1 split AND M6 split | 9 | 8 | max(6, ⌈0.75×8⌉=6) = 6 of 8 | **no** | **no** | — |

(M8-as-scored and M9-as-scored are not candidate readings: rule 2 excludes them explicitly.)

## 3. Coherence proof

**R1 is the uniquely coherent reading.** It is the only reading under which all three of these frozen statements are simultaneously true:

1. Rule 2's "**8** scored metrics" (R2 and R4 give 7 and 9);
2. Rule 4's parenthetical "**≥ 6 of 7**" for the M7-N/A case (R2 computes 6-of-6, R4 computes 6-of-8);
3. §5's "**recorded separately, never folded**" for M1's sub-scores, and M-28's single M6 champion (R3 folds M1's declared-non-foldable split and invents a second M6 championship the prereg never names).

R3 is the only rival that survives the arithmetic, and it dies on the text: it requires folding exactly the metric the frozen §5 says is never folded.

## 4. Consequence check (does the reading change any verdict?)

No. Under R1, Y5 holds 7/8 ≥ 6 ✓ (CONFIRMED BLOWOUT stands). Under R2, Y5 would hold 6/7 ≥ 6 ✓ — same verdict. The amendment is rule-clarity, not outcome-changing: it ratifies the convention already used in `TRACKA_VERDICT_SHEET.md` §3 (per-column champions) and §6.2.

## 5. What Micah must sign (exact sentence)

> Dated amendment 2026-09-22 to `PREREG_FREEZE.md` §7 rules 2 and 4 (counting convention; no numeric change): the "8 scored metrics" are {M1-content, M1-boundary, M2, M3, M4, M5, M6-transfer-tax, M7} — M1's two sub-scores count as two scored columns per §5 ("recorded separately, never folded"); M6-transfer-tax counts as one scored column per M-28 ("champion = smallest transfer tax"). Rule 2's threshold remains ≥ 6 of 8; rule 4's N/A-discipline applies as written (M7-N/A → ≥ 6 of 7). No scorecard, verdict, bar, kill criterion, or championship is altered; this ratifies the convention used in `TRACKA_VERDICT_SHEET.md` §3/§6.2. — Signed: Micah, 2026-09-22.

Per §13 this is a verdict-rule counting change: it needs the dated amendment + his re-approval. **Nothing has been applied** — the verdict sheet's §6.2 adoption remains PROPOSED-interpretation until he signs.

## Evidence refs

- Frozen prereg: `docs/lab/units/PREREG_FREEZE.md` (commit `b0b9140c0eda`), §5 (M1/M6/M7), §7 rules 2/4, M-28, M-40.
- Adopting interpretation: `docs/lab/tracka-closeout/TRACKA_VERDICT_SHEET.md` §3, §6.2.
