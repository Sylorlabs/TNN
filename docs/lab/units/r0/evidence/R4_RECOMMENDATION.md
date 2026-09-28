# R-4 RECOMMENDATION — B-T3 dose-curve degradation tolerance

Swarm: R-4 DEBATE SWARM (RDTDT parameter-setting run, Track R0) · 2026-09-21
Parent task: Track R0 parameter setting. **Do NOT commit** (per task).

## Recommended tolerance

**25/1000, defined as: maximum drawdown from the running maximum of the dual
hard-grounding score (/1000) across doses 250 → 8000 must be ≤ 25/1000.**

Formally, with scores S₂₅₀ … S₈₀₀₀: let Pᵢ = max(S₂₅₀…Sᵢ); require
maxᵢ(Pᵢ − Sᵢ) ≤ 25/1000. Boundary semantics: a drawdown of exactly 25 passes
(≤); 30 fails. 25/1000 = 5 probes of the 200-occurrence battery.

**Measured battery against this rule:** drawdown 0/1000, both legs → **PASS
with full margin** (budget untouched).

## Why this number is principled (not arbitrary)

1. **Measurement granularity.** Score = correct_probes × 1000/200, so each
   probe is exactly 5/1000. Any tolerance must be a multiple of 5; 25 = 5 probes.
2. **The knee / materiality quantum.** The battery's own structure gives the
   natural unit of "a unit of knowledge lost": the 22 consistent vocabulary
   spans account for 110/200 occurrences → 5 occurrences per average span.
   25/1000 = one average consistent span's occurrence budget. The tolerance is
   an *occurrence budget* (≤5 of 200 probes may regress); "one span" is the
   interpretation of its scale, not a claim that spans are uniform — a
   6-occurrence loss (30/1000) fails regardless of span identity.
3. **Label ceiling.** 950 is the label-3 ceiling (10 inconsistent occurrences
   excluded by b=0), so the score cannot rise; the only movable direction is
   down. The tolerance therefore polices pure regression, never
   improvement. (Resolved during review: 190 = 110 consistent-chunked + 80
   rare/novel grounded via the raw route; the 10 inconsistent are the misses.
   Dual = raw = 950 in both legs, dual−raw = 0.)
4. **Determinism is not a noise band — and doesn't need to be.** The system
   is deterministic and byte-identical, so a nonzero drop is real signal, not
   noise; the exact drop is reported regardless. The tolerance is not a noise
   band but a *materiality threshold* for the claim "the system does not
   degrade with dose": a 1–5 probe delta is a real behavioral difference but
   below the structural resolution at which "a unit of knowledge was lost"
   is a meaningful verdict for this battery.

## Why drawdown-from-running-max (not adjacent-drop, not cumulative-from-baseline)

Test 1 (sensitivity, 10 synthetic curves × 5 candidate rules) and Test 2
(16 stress cases) were computed exactly; tables below. Findings:

- **Strict 0/1000** fails a 1-probe transient that fully recovers (S2) —
  over-strict, and it nullifies R-4's purpose as a tolerance-setting item
  (it would be redundant with "flat or non-decreasing").
- **Adjacent-drop ≤ 25 alone** has a fatal loophole: a slow −50 bleed spread
  as −10/step (S3b) passes every adjacent check. Killed by Test 1.
- **Cumulative-from-baseline ≤ 25 alone** matches all normative judgments on
  *this* battery but misses improve-then-crash (900→950→925→900, drawdown 50
  from peak) and oscillation (950→900→950→900…, drawdown 50) — both pass it.
- **Max drawdown from running maximum ≤ 25** matches every normative
  judgment, subsumes both clauses above, and under the 950 ceiling it reduces
  exactly to cumulative-from-baseline (the adjacent clause is then redundant,
  so it is dropped — cleaner for signing).

## Test 1 — candidate × synthetic-curve discrimination

Curves over doses 250/500/1000/2000/4000/8000. `adj` = max adjacent drop,
`cum` = drop from dose-250 baseline, `dd` = drawdown from running max.
Normative = what the bar *should* do. `*` = full budget spent; flag for review.

| curve | adj | cum | dd | strict ≤0 | adj ≤25 | cum ≤25 | **dd ≤25 (rec.)** | normative |
|---|---|---|---|---|---|---|---|---|
| M0 measured (950×6) | 0 | 0 | 0 | PASS | PASS | PASS | **PASS** | PASS |
| S1 one-span loss @8000 (−40) | 40 | 40 | 40 | FAIL | FAIL | FAIL | **FAIL** | FAIL |
| S1b sub-span loss @8000 (−20) | 20 | 20 | 20 | FAIL✗ | PASS | PASS | **PASS** | PASS |
| S2 1-probe transient, recovers (−5) | 5 | 5 | 5 | FAIL✗ | PASS | PASS | **PASS** | PASS |
| S3 slow bleed to −25 | 5 | 25 | 25 | FAIL✗ | PASS | PASS | **PASS*** | PASS* |
| S3b deep bleed to −50 | 10 | 50 | 50 | FAIL | PASS✗ | FAIL | **FAIL** | FAIL |
| S4 cliff −50 @2000 | 50 | 50 | 50 | FAIL | FAIL | FAIL | **FAIL** | FAIL |
| S5 sawtooth ±20 | 20 | 20 | 20 | FAIL✗ | PASS | PASS | **PASS** | PASS |
| S6 early dip, non-decreasing | 0 | 0 | 0 | PASS | PASS | PASS | **PASS** | PASS |
| S7 boundary single −25 | 25 | 25 | 25 | FAIL✗ | PASS | PASS | **PASS*** | PASS* |

✗ = mismatch vs normative. Strict: 5 mismatches. Adj-only: 1 (S3b — the
fatal bleed loophole). Cum-only and drawdown: 0 on this battery. Drawdown
additionally catches the two cases below that cum-only misses.

## Test 2 — stress cases (drawdown rule)

| case | dd | rule | expected |
|---|---|---|---|
| T1 improve-then-crash 900,950,950,925,900,900 | 50 | FAIL | FAIL |
| T2 oscillation 950,900,950,900,950,950 | 50 | FAIL | FAIL |
| T4a boundary dd = 25 | 25 | PASS | PASS |
| T4b dd = 30 (6 probes) | 30 | FAIL | FAIL |
| T6 saturation onset @2000, score flat (leg-1-like) | 0 | PASS | PASS |
| M0 both legs | 0 | PASS | PASS |

16/16 stress cases match (full table in table above + these). Scripts:
`/tmp/r4_test1.py`, `/tmp/r4_test2.py` (analysis arithmetic on measured
numbers; not an AI decision path).

## Ledger-saturation finding (the disclosed caveat)

Raw logs (`b_t3_leg0_p0.log`, `b_t3_leg1_p0.log`, branch `tnn-native-lab`):

- Leg 0 ledger by dose: 1875 → **2048** → 2048 → 2048 → 2048 → 2048
  (saturates at dose 500; trust-update entries past 2048 dropped silently).
- Leg 1 ledger by dose: 651 → 926 → 1476 → **2048** → 2048 → 2048
  (saturates at dose 2000).
- Dual score at every unsaturated dose (leg 0 d250; leg 1 d250/500/1000):
  **950** — identical to every saturated dose. Saturation onset coincides
  with no score change in either leg.
- Supporting: promoted/live counts are dose-invariant too
  (leg 0: 700/700 at all doses; leg 1: 88/88 at all doses); only the
  compression ratio grows (leg 0: 1234→1898; leg 1: 1184→1219).

Conclusions:

1. **The flat 950 curve does not survive *because* the ledger saturates.**
   Unsaturated doses already sit at 950, and the two legs saturate at
   different doses (500 vs 2000) with no score movement at either onset.
   The flatness is overdetermined: vocabulary complete by dose 250 (nested
   prefixes, fresh arena per dose) + 950 is the label ceiling.
2. **No saturation correction to the tolerance is needed.** A masked drop is
   impossible here: the score is a count over a fixed 200 occurrences, and
   the only non-grounded occurrences are the 10 label-excluded ones — any
   consistent-occurrence loss changes the count. Saturation cannot hide a
   drop; it can only fail to produce one.
3. **Scope note (goes in the amendment):** doses above saturation test
   *build-stability of a saturated store*, not dose-response learning. The
   tolerance therefore polices "more data must not produce a worse store."
   B-T3 is a no-degradation bar on the fixed 200-probe battery — it makes no
   claim about unseen queries, retrieval margins, or store-internal churn
   under saturation (those need per-probe identity/provenance vectors, which
   this battery does not emit).

## Second opinion (gpt-5.6-sol, adversarial)

Consulted as red-team; it recommended **rejecting 25 in favor of 0/1000**,
arguing the span derivation is numerology under non-uniform spans,
determinism removes any need for slack, and the rule misses identity churn /
margin degradation / unseen-probe damage. Adopted from it:

- the **drawdown-from-running-max** formulation (strictly better than the
  adjacent+cumulative pair originally considered — catches T1/T2);
- the scope note (§3 above) and the monotone-bleed flag convention below.

Not adopted: the 0/1000 gate. Reasons: (a) R-4 exists in the frozen prereg
as a *tolerance* sign-off item, implying the bar contemplates a nonzero
budget; zero would be redundant with "flat or non-decreasing". (b) The
tolerance is a materiality threshold for "degradation," not a noise band;
determinism means drops are reported exactly either way. (c) Sensitivity
analysis shows 0 fails a 1-probe transient-recovery (S2) — labeling a
self-healed 0.5% dip "DEGRADED" mislabels reorganization as degradation.
The dissent is recorded here so the signer sees the strongest counterargument.

## Verdict hygiene (non-binding, recommended for the verdict sheet)

- Report the exact drawdown number always, even when it passes.
- **Flag** any monotone cumulative bleed (S3-pattern), even within budget —
  a dose-correlated loss signature deserves investigation, not silent passage.
- Future batteries: emit per-probe outcome vectors by dose (identity-stability
  check); if ledger capacity changes, re-derive (the 25 is calibrated to this
  battery's 200-occurrence / label-3 structure).

## What Micah signs

Dated prereg amendment to §0 I R-4 / §2 R0.2 (Track R0), suggested wording:

> **R-4 degradation tolerance (signed YYYY-MM-DD):** for the B-T3 dose curve
> (doses 250 → 8000), let S be the dual hard-grounding score (/1000) and
> Pᵢ the running maximum of S up to dose i. The battery passes iff
> maxᵢ(Pᵢ − Sᵢ) ≤ 25/1000 (boundary: exactly 25 passes). Scope: this is a
> no-degradation bar on the fixed 200-probe battery; doses above ledger
> saturation test build-stability of a saturated store. Measured: drawdown
> 0/1000 both legs → PASS with full margin.

Changed by this swarm vs the descriptive proposal: the number (25/1000) is
kept but re-derived (one-span occurrence budget, not an arbitrary round
number) and re-defined (drawdown-from-running-max, not adjacent-drop-only —
the adjacent-only form has a proven slow-bleed loophole).

## Review challenge log (RDTDT step 1)

- Challenged the descriptive crew's 25/1000: no derivation was given; traced
  it as plausibly inherited from R-3's proposed ε (|dual−raw| ≤ 25/1000).
  Replaced with the independent span-budget derivation above.
- Challenged "flat curve ⇒ saturation artifact": refuted — unsaturated
  doses already at 950; onset at different doses per leg with no movement.
- Challenged per-span uniformity assumption: the budget is occurrence-counted
  (5 probes), so non-uniform spans don't break it; documented.
- Challenged the adjacent-drop framing: proven insufficient (S3b loophole);
  replaced with drawdown.
- Source inspected: `docs/lab/units/r0/impl/ablation/b_t3.zag`,
  `b_t3_leg0.md`, `b_t3_leg1.md`, `verdict_bt2_bt3.md`, raw logs
  `b_t3_leg0_p0.log` / `b_t3_leg1_p0.log`, all on `tnn-native-lab`
  (branch head `1f0c057b9dd8` at review time). Formal verdict commit
  `13bbaf07067e` confirmed the blocked-UNDECIDED status this resolves.
