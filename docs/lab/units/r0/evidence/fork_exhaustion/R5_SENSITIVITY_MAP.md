# R-5 SENSITIVITY MAP — fork exhaustion (B-T4 support-gap floor)

Fork-exhaustion crew · Track R0 · 2026-09-21
Harness: `fork_exhaustion.py` — rebuilds the deterministic 384-row battery
(clean 8/exposure/leg, contested 4/exposure/leg, exposures 1–16, onset leg0
e=3 / leg1 e=4) and applies flips. No RNG. Raw: `r5_raw.json`.

## Grid

Clean floor wordings × contested-recruitment rules:

| Wording | Meaning |
|---|---|
| W1 strict 8/8 per exposure per leg | recommended |
| W2 ≥7/8 per exposure per leg | descriptive crew's margin |
| W3a flat average ≥7.5/8 across exposures | average fork |
| W3b flat average ≥7/8 across exposures | average fork, laxer |
| W4a pooled ≥8/8 per leg | pooled-100% |
| W4b pooled ≥63/64 per leg | pooled, one case slack |
| W4c pooled ≥7/8 per leg | pooled, lax |
| W5 onset-split (behavior-phased) | 100% abstain below support_min / 100% byte-exact recruit at-or-above; reason codes ignored |
| W7 cross-leg pooled ≥8/8 | pooled-100% across both legs |
| W8 cross-leg pooled ≥255/256 | pooled, one case slack across both legs |

| Contested rule | Meaning |
|---|---|
| C1 zero recruitments | recommended |
| C2 ≤1 per (leg, exposure) cell | per-cell leniency |
| C3 ≤1 total per leg | proportional 1/16 |
| C4 ≤1 total across both legs | proportional 1/32 |

Scenarios: measured M0 + inherited D1–D7 + 8 new adversarial
(D8 contested leak at 2 exposures, D9 one collapsed exposure, D10 wrong-reason
across 2 exposures, D11 single e-1 recruit, D12 contested 3/4, D13 onset
delayed both legs, D14 contested full leak, D15 single wrong case leg-1 e-1).

## Map — mismatches vs normative, wording × contested

| wording \ contested | C1 zero | C2 ≤1/cell | C3 ≤1/leg | C4 ≤1 total |
|---|---|---|---|---|
| W1 strict 8/8 | **0** | 3 | 2 | 2 |
| W2 ≥7/8 | 3 | 6 | 5 | 5 |
| W3a avg ≥7.5/8 | 10 | 13 | 12 | 12 |
| W3b avg ≥7/8 | 11 | 14 | 13 | 13 |
| W4a pooled 100% | **0** | 3 | 2 | 2 |
| W4b pooled 63/64 | 3 | 6 | 5 | 5 |
| W4c pooled 7/8 | 11 | 14 | 13 | 13 |
| W5 onset-split | 2 | 5 | 4 | 4 |
| W7 x-leg pooled 100% | **0** | 3 | 2 | 2 |
| W8 x-leg pooled 255/256 | 3 | 6 | 5 | 5 |

## Which scenarios kill which fork

| Fork | Mismatching scenarios | Diagnosis |
|---|---|---|
| W2 (≥7/8) × C1 | D6, D11, D15 | Any single-rep flake (1/8 wrong) passes — the margin is exercisable only by bugs, exactly the swarm's D6 finding, now with two more instances |
| W4b (pooled 63/64) × C1 | D6, D11, D15 | Same three — pooled slack is margin by another name |
| W8 (x-leg 255/256) × C1 | D6, D11, D15 | Same three |
| W3a/W3b/W4c (averages) | D9, D13 + 8–9 more | A collapsed exposure hides behind healthy ones (D9: avg 7.5/8 passes a 0/8 exposure at the boundary) — the frozen "no collapse at 1 exposure" clause kills every averaging form |
| W5 (onset-split, reason-ignored) × C1 | D7, D10 | Kills the outcome-only fork: wrong abstain-reason (d2=2 vs 1) passes, but the swarm's D7 precedent and D10 name reason codes load-bearing — a wrong reason is a wrong mechanism state, not a cosmetic label |
| W1 × C2 (≤1/cell) | D5, D8, D12 | Any per-cell leniency misses single contested leaks — including D8's two-exposure leak |
| W1 × C3/C4 (≤1/leg, ≤1 total) | D5, D12 | Miss single leaks by design (1 ≤ 1 passes at the boundary) |
| W1 × C1 | — | matches all 16 scenarios |

## Equivalence finding (not a fork — a restatement)

W1, W4a, and W7 produce **byte-identical pass/fail on every scenario × every
contested rule** (verified programmatically across the full grid):
pooled-100% ⟺ every cell 100% ⟺ every exposure 8/8. Cross-leg vs per-leg
pooling differs only when slack is nonzero; at 100% they coincide. These are
three wordings of one bar, not three candidate bars. The amendment can use
whichever wording Micah finds clearest without changing what is signed.

## Fork-closure statement

Every non-equivalent fork is killed by at least one named scenario:
- all margin/slack forms (W2, W4b, W8) → D6/D11/D15
- all averaging forms (W3a, W3b, W4c) → D9/D13 (+8 more)
- outcome-only wording (W5) → D7/D10
- all contested leniency (C2, C3, C4) → D5/D8/D12

**No experimental fork remains untested.** The surviving set is exactly
{(strict per-exposure 8/8 ⟺ pooled-100% ⟺ cross-leg-100%) × contested
zero-tolerance} — i.e., the recommendation, up to wording.

## Verdict on R-5

**CONFIRM.** Strict 8/8 per exposure per leg + zero contested recruitments is
the unique surviving (wording, rule) pair up to provable equivalence. The
exhaustion closes Micah's keep-forks question for R-5: the keepable "forks"
are restatements, and every genuinely different candidate fails a named
failure mode.
