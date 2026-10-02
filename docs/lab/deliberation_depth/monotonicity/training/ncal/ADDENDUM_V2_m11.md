# ADDENDUM V2 — Hierarchical personal ledger, raw-rate pessimistic cap (mech m11)

- **Date:** 2026-09-25 (pre-run; mechanism frozen before Zag implementation)
- **Mech id:** m11 (m10 reserved for scale legs)
- **Parent:** PREREG_NCAL_V1_FROZEN.md §6 (variant protocol)

## Mechanism change (vs v0)

Add a **per-item personal ledger** alongside the §2.2 class ledger:

- Per item id: `(c_p, t_p)` = own correct / own total over PAST released
  judgments (online GT of the item's own past — same authorized class as
  §2.2, disclosed; current cell's GT never used).
- For a released cell with `t_p ≥ 1`: `p_raw = (c_p · 10^6) / t_p`
  (millionths, integer division — the item's RAW observed correctness rate).
- `conf_raw = min(conf_class_ledger, p_raw)` — the personal rate CAPS the
  class rate (pessimistic pooling). If `t_p = 0`, no cap (class rate only).
- The §2.3 deliberation ceiling still applies afterwards:
  `conf = min(conf_raw, conf_prev)`. Release/correctness untouched (B9).

What this is NOT: it is not shrinkage/weighted averaging (tested: cannot
move the adversarial item far enough), not a floor (tested: worsens B3),
not family-aware (no family labels, no depth, no family proxies).

## Target (§5 failure sources)

1. **redteam (2 G-violations).** RT-K12-01 is wrong at every depth but sits
   in a (margin,consumed) class saturated with honest-correct items, so the
   class ledger gives it 0.994. Its own record is 0/1, 0/2, 0/3… — the
   raw personal cap drags it to 0. d2→d4 rise (+0.161) is attacked.
   The d4→d8 rise (+0.522) is PROVEN unsatisfiable (see below) — residual.
2. **ceiling/D (2 G-violations, +0.001/+0.005).** Items with wrongs in
   their own history get capped, homogenizing the cohort; the
   selection-driven micro-rises are attacked.

## Stated principle (recorded per §6 — not tuned to the bar)

**Narrowest reference class.** When judging an item, the narrowest
applicable reference class is the item's own track record; the pooled
class rate is the fallback for items without one. Direct experience
dominates the generalization — when they conflict, the lower (pessimistic)
rate governs, because the class rate's optimism is earned by OTHER items.

**Why RAW (unsmoothed) for the cap.** Laplace smoothing is a device for
generalizing from a sample to a POPULATION (the reference class). The
personal ledger does not generalize — it summarizes the item's own direct
experience, applied to the item itself. Smoothing the personal rate with
the optimistic class prior (p0=0.95) would let pooled honest experience
inflate the cap for an item whose own record contradicts it (0/2 →
0.475) — precisely the adversarial-pooling failure. The cap is a
pessimistic BOUND, not an estimate; bounds are conservative. The `t_p ≥ 1`
gate ensures the cap binds only on actual direct experience.

**Why the cap can only help B2/B5.** `min()` only lowers confidence;
lowering cannot create per-item rises (V1/V2), and lowering wrong items'
confidence improves separation.

## Negative results documented (attack order §6, directions (b) exhausted)

- **(b) feature expansion:** verified f1..f8 semantics from
  PREREG_TRAINING.md §4 via training/src/feat.zag. Within shared
  (margin,consumed) classes, O-correct vs P-wrong items have IDENTICAL
  f3/f4/f6/f7/f8 (means and sds equal) and identical f1 values; f5
  differs by 1–17 units (adversarially matched noise — binning on it would
  be bar-gaming). **No epistemically legitimate feature separates them.
  Feature expansion is a dead end.**
- **(b) symmetric-continuity floor:** prototyped (floor = personal Laplace
  rate for perfect-record items). Result: B3 3→5 (adds d1→d2 rise on O:
  d1 cannot be lifted — no history — so any d2+ lift creates a B3 step),
  B13 stays 6 (d1 unfixable). **Rejected by the §6 selection rule.**
  Joint finding: on ceiling/O, B3-strict and B13 are jointly
  unsatisfiable — (B3=0 ∧ B13=0) requires mean_conf(d1) ≥ 0.9, but d1
  confidence can only come from (f1,f5) classes poisoned by P-wrong items
  (features matched); purifying them needs family labels (barred).
- **O selection micro-rises (+0.019, +0.005):** structural. M4 abstention
  (frozen, B9) removes below-mean-conf items; any calibrated confidence is
  positively correlated with M4's release criterion (both track margin);
  removing below-mean items mathematically raises the mean. Fixing it
  would require above-mean confidence on items M4 abstains (anti-calibrated)
  or uniform confidence (degenerate, breaks B4/B5).

## Proven unsatisfiable residual (redteam d4→d8, +0.522)

Given B9 (frozen release: d4 releases {M3 correct, K12 wrong}, d8 releases
{K12 wrong} alone), B2 (K12 wrong→wrong ⇒ conf nonincreasing, else V2>0),
the §2.3 ceiling, and conf ≤ 1000: G(d8) = c_K12(d8) ≤ c_K12(d4) forces
c_K12(d4) ≤ c_M3(d4) − 1000 ≤ 0 and c_M3(d4) = 1000, but the ceiling caps
c_M3(d4) ≤ c_M3(d1) = 994 (class rate at t_p=0). Contradiction. **At least
one redteam G-violation is mathematically unsatisfiable.**

## Expected outcome (from bit-exact Python prototype of the update rules)

B3: 6 → 3 (D: 2→0, redteam: 2→1, O: 2 residual). B13: 6 → 6 (no worse).
B2: V1=0, V2=0. B4 ≈ 0.972, B5 ≈ 0.874, B4b ≥ 0.568, B7 = 0.148. No bar
broken. A/B byte-identical (deterministic, zero RNG).

## Honest residual (if the Zag run confirms the prototype)

B3 = 3: ceiling/O 2 (structural selection) + redteam 1 (proven
unsatisfiable). B13 = 6 (all ceiling/O; d1 jointly unsatisfiable with B3).
