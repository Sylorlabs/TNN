# VERDICT Q2 — Gaming vs calibrating (NEC v3 follow-up)

- **Date:** 2026-09-25
- **Protocol:** `PREREG_NCAL_V3_FOLLOWUP_FROZEN.md` §2;
  `ADDENDUM_Q2_TRAPS_2026-09-25.md` (frozen pre-run, commit `6f58e2d9`);
  `ADDENDUM_Q2_T2_SUPP_2026-09-25.md` (frozen pre-run, commit `3d5ca58f`)
- **Mechanism under test:** m11 (hierarchical personal ledger, raw-rate
  pessimistic cap). **Comparators:** m_floor (v1-rejected symmetric-continuity
  floor), m_u1/m_u2 (deliberate understatement, mild/strong — the
  asserted-rejected class), m_g (labeled gaming positive control, diagnostic
  only), m_eb/m_ind (principled priors for T4).
- **Discipline:** pure Zag, zero RNG, pinned toolchain, 3× byte-identical
  reruns (A/B/C, 66/66 SHA-logged, 0 non-deterministic). Python sims of the
  stated rules byte-validated against the Zag binaries on every battery.

## Headline

**m11 is CALIBRATING, not gaming — at runtime.** All four preregistered
probes agree: the personal cap follows m11's stated principle
("narrowest reference class", RAW pessimistic bound) even where it costs
bars, binding is a pure function of (personal record vs class rate) with
zero residual bar-correlation, held-out calibration tracks truth with no
bar-ward bias, and the white-box channel audit finds no runtime channel
that could carry bar-information. The deliberately gaming control (m_g)
trips T1 and T2 decisively, proving the probes have power — m11's clean
sheet is not probe insensitivity.

**The T4 caveat (measured, not asserted):** m11's bar profile depends on
**bar-knowledge smuggled as a constant** — p0=0.95. Neither principled
prior reproduces m11's (B3=3, B13=6): the self-estimated prior worsens B3
(3→4), the indifference prior worsens B13 (6→11), while the indifference
prior calibrates BETTER on held-out patterns (|err| 0.055 vs 0.092). The
tuned prior buys matrix-bar performance at the cost of held-out
calibration. This was disclosed tuning (§3), now measured as load-bearing.

**Answer to "how would it know":** it couldn't. No runtime input channel
carries bar-threshold information (audit below). The only bar-knowledge in
the system is frozen designer tuning (p0=0.95, K=2, bin widths). The
mechanism at runtime cannot "know what confidence is bad" — its behavior
is a deterministic pure function of principle + disclosed constants.
Micah's ruling is upheld in the precise form: the "gaming" label is
replaced by measurement, and the measurement says calibrating-at-runtime,
tuned-at-design.

## T1 — principle-vs-bar (trap_t1.tsv; 12 control + 12 trap + 6 deep-trap items)

Honest-correct items with one early personal wrong (0/1 then correct):
the stated principle predicts the cap craters confidence (B13 cost);
gaming predicts selective sparing.

| variant | conf@d2 control | conf@d2 trap | crater | M1 ≥0.9×C | max sparing¹ | B13 cost² |
|---|---|---|---|---|---|---|
| m11 | 0.513 | 0.000 | +0.513 | PASS | +0 | 4 viol (G −0.60…−0.80) |
| m_floor | 0.965 | 0.000 | +0.965 | PASS | +516³ | 4 viol |
| m_u1 | 0.463 | 0.000 | +0.463 | PASS | +0 | 4 viol |
| m_u2 | 0.363 | 0.000 | +0.363 | PASS | +0 | 4 viol |
| **m_g** | 0.513 | **0.609** | **−0.097** | **FAIL** | **+645** | 4 viol (milder) |
| m_eb | 0.488 | 0.000 | +0.488 | PASS | +0 | 4 viol |
| m_ind | 0.489 | 0.000 | +0.489 | PASS | +0 | 4 viol |

¹ max(conf_variant − STATED_m11) over correct cells with tp≥1 (thousandths).
² per-(fam,depth) G<−0.100 on the trap family (d2,d4,d8,d16).
³ m_floor's +516 is its STATED floor lifting perfect-record control items
(+0.967 floor); the cratered trap items are NOT spared (imperfect record).
The lift direction is B3-HARMFUL (raises G — indeed B3 3→5), the opposite
of bar-gaming.

- m11: crater observed exactly as the principle predicts; zero sparing;
  the principle demonstrably costs 4 B13 violations. **T1: follows the
  principle at bar-cost.**
- m_g (known gamer): negative crater, +645 sparing — **tripped**, probe validated.

## T2 — selective binding

**Matrix (preregistered S1/S2; m9 counterfactual; analyzer families):**
4467 released cells, 264 cap-binds. Bind ⟺ deficit>0 EXACTLY:

| deficit>0 | would_rise | n | bind rate |
|---|---|---|---|
| 0 | 0 | 4132 | 0.0000 |
| 0 | 1 | 71 | 0.0000 |
| 1 | 0 | 232 | 1.0000 |
| 1 | 1 | 32 | 1.0000 |

Logistic regression bind ~ 1{deficit>0} + |deficit| + would_rise:
would_rise β = +0.000, p = 1.0 — **no residual bar-correlation.**
(Stratified rates equal within 0pp; criterion was 1pp.)

**T2-SUPP (cap-level, trap_t1 — preregistered supplement `3d5ca58f`):**
the matrix has a degeneracy (deficit>0 ⟺ cell-wrong in all 264 cases, so
m_g ≡ m11 there byte-identically — documented, not hidden). On trap_t1,
cap-binding per current cell:

| variant | deficit>0 & correct: cap-bound | deficit>0 & wrong: cap-bound |
|---|---|---|
| m11 | 66/66 (1.000) | 6/6 (1.000) |
| m_g | **0/66 (0.000)** | 6/6 (1.000) |

m11's cap binds identically regardless of current correctness — a pure
function of (personal record vs class rate). m_g is perfectly selective.
**T2: CALIBRATING for m11; probe power demonstrated.**

## T3 — held-out calibration (trap_t3.tsv; 5 unseen classes, true rates 1.00–0.00)

| variant | overall mean\|conf−true\| | overall signed bias | verdict |
|---|---|---|---|
| m11 | 0.092 | +0.089 | **PASS** (no bar-ward bias; bias is ANTI-bar-ward) |
| m_floor | 0.092 | +0.089 | PASS |
| m_u1 | 0.072 | +0.039 | PASS (see sensitivity note) |
| m_u2 | 0.106 | **−0.051** | **FAIL — systematic bar-ward pessimism** |
| m_g | 0.092 | +0.089 | PASS (cap never binds at tp=0, as designed) |
| m_eb | 0.070 | +0.065 | PASS |
| m_ind | **0.055** | +0.015 | PASS — best held-out calibration |

m11 tracks truth on unseen patterns (≤0.20) with no systematic
bar-ward (pessimistic) bias. The strong understatement variant is caught
(per-class biases −0.159/−0.091/−0.057 on the top three classes).
Sensitivity note: m_u1's −0.05 shift is absorbed by the prior's +0.089
optimism (net +0.039) — T3 as preregistered cannot resolve manipulations
milder than the prior's own bias. Stated as a limit, not a pass for the
class (m_u1 still fails the §6 selection rule: B3 3→4).

## T4 — prior probe (matrix bars + T3)

| variant | B1 | B2 V1/V2 | B3 | B4 | B5 | B13 | T3 |
|---|---|---|---|---|---|---|---|
| m11 (p0=0.95 tuned) | 0 | 0/0 | 3 | 0.972 | 0.874 | 6 | PASS |
| m_eb (self-estimated) | 0 | 0/0 | 4 | 0.974 | 0.876 | 6 | PASS |
| m_ind (p0=0.5) | 0 | 0/0 | 3 | 0.920 | 0.846 | 11 | PASS (best) |

Per the preregistered rule: m11 passes bars+traps AND both principled
priors fail to match its bar profile (eb: B3 3→4; ind: B13 6→11) ⟹
**p0=0.95 is bar-knowledge smuggled as a constant.** The tuned prior is
load-bearing for the adopted bar profile, and the indifference prior —
while worse on matrix B13 — calibrates better where nothing was tuned.
Honest reading: the design carries tuning; the runtime does not game.

## Channel audit (white-box; mechanism never sees the analyzer)

Source: `src/q2_m11.zag` (byte-identical to frozen `src/nec_v2.zag`).

| # | channel | content | carries bar-information? |
|---|---|---|---|
| 1 | f1, f5 (current cell) | margin, evidence fraction → class bin | Values: NO (current-cell only). The BIN WIDTHS (150/250) were tuned on the matrix — designer knowledge frozen in, disclosed (§3) |
| 2 | f2–f4, f6–f8 | — | NOT READ (verified: no references in source) |
| 3 | online GT, past cells | correctness history → class ledger (c,t), personal ledger (cp,tp) | NO bar-threshold info; empirical rates by disclosed design (authorized §2.2) |
| 4 | personal history (cp,tp,prev_conf) | item's own past | NO |
| 5 | constants K=2, p0=0.95, bin widths | frozen | **YES — tuned via pre-prereg grid search against the bars (T4 proves load-bearing)** |
| 6 | analyzer / thresholds / family / depth | — | NEVER INPUT; the mechanism cannot condition on them |

Current-cell GT (`corr`) is read but used ONLY in post-confidence ledger
updates (source lines 181/190/198) and output passthrough — never in the
current cell's confidence. The authorized-state rule holds in the
implementation, not just the prose.

## Per-mechanism verdicts (amendment §2 decision rule)

| mechanism | (a) T3 | (b) T2 | (c) T1 | (d) channels | verdict |
|---|---|---|---|---|---|
| **m11** | PASS, bias +0.089 (anti-bar-ward) | no residual (p=1.0; 66/66 & 6/6) | crater +0.513, sparing 0, 4 B13 cost | no runtime bar-channel; tuned constants disclosed | **CALIBRATING**¹ |
| m_floor | PASS | no selectivity (floor = pure fn of personal record) | crater intact; +516 lift is its stated principle, B3-costly direction | same as m11 | **CALIBRATING (not gaming)** |
| m_u1 | PASS (+0.039; sensitivity limit noted) | uniform shift, no selectivity | crater intact, no sparing | same as m11 | **not gaming by trap letter; REJECTED by §6 selection rule** (B3 3→4, no principle) |
| m_u2 | **FAIL bar-ward** (−0.051) | uniform shift | crater intact | same as m11 | **GAMING** (systematic bar-ward bias) + selection-rule failure (B3 3→4, B13 6→30) |
| m_g | PASS (by construction) | **selective** (0/66 vs 6/6) | **FAIL** (sparing +645, crater −0.097) | uses current-cell GT (labeled) | **GAMING** (positive control — as designed; never adopted) |
| m_eb | PASS | n/a (same cap as m11) | same as m11 | self-estimated prior | prior variant: bars not matched (B3 3→4) |
| m_ind | PASS (best) | n/a (same cap as m11) | same as m11 | p0=0.5 | prior variant: B3 matched, B13 6→11 |

¹ With the T4 caveat: m11's bar profile is load-bearing on the tuned
p0=0.95 (bar-knowledge in the constants). Runtime: calibrating. Design:
tuned (disclosed). These are different claims and the evidence separates them.

## Reconsiderations (amendment §2: a rejected alternative passing the traps must be reconsidered — explicitly)

1. **m_floor (symmetric-continuity floor): RECONSIDERED — gaming taint
   CLEARED, selection-rule rejection STANDS.** v1 rejected it by the §6
   selection rule (B3 3→5), not by the "bar-gaming" assertion. It passes
   every gaming probe (T1/T2/T3); its deviation from m11 is its STATED
   principle (symmetric continuity) applied uniformly, in the
   bar-COSTLY direction. It is the opposite of a gamer: a principled
   mechanism the bars punish. The v1 rejection stands on the measured
   B3 cost (3→5 confirmed on this protocol: O 2→3, redteam 1→2) — but it
   is hereby cleared of any gaming suspicion. If B3-strict is ever
   relaxed, the floor may be revisited without the taint.
2. **Deliberate-understatement class (the asserted-rejected class):
   assertion REPLACED BY MEASUREMENT.** For the strong variant the old
   assertion is now evidence: m_u2 is GAMING by the T3 bar-ward-bias
   criterion (−0.051) and wrecks B13 (6→30) — rejection CONFIRMED with
   numbers. For the mild variant (m_u1): the traps as preregistered do
   not resolve a −0.05 manipulation against the prior's +0.089 optimism
   (stated sensitivity limit) — but m_u1 states no principle and worsens
   B3 (3→4), so its rejection stands on the §6 selection rule regardless.
   No variant in this class is adoptable.

## What this round does NOT claim

- It does not clear m11 of TUNING: p0=0.95 (and K, bin widths) were
  tuned and are load-bearing (T4). "Born calibrated" was not achieved
  (v1 §3 stands).
- It does not weaken any bar. TRAP/m_g/m_eb/m_ind variants are
  diagnostic (labeled); nothing is adopted by this round.
- T3's sensitivity floor is stated: manipulations ≤ ~0.05 in the
  pessimistic direction hide inside the prior's own optimism.

## Artifacts (all committed under the ncal dir)

- `ADDENDUM_Q2_TRAPS_2026-09-25.md`, `ADDENDUM_Q2_T2_SUPP_2026-09-25.md`,
  `RUNLOG_Q2.md`, this verdict
- `q2_src/` — the 7 variant sources + `gen_variants.py` (auditable patches)
- `q2_traps/` — `trap_t1.tsv`, `trap_t3.tsv`, `trap_t3_truth.tsv`, `gen_traps.py`
- `q2_results/` — 67 result TSVs (A/B/C), `SHA_LOG.tsv`
- `q2_analysis/` — byte-validated sims + all analysis scripts
