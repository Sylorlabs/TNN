# ADDENDUM Q2 — Trap batteries, comparators, and pass/fail criteria (PRE-RUN)

- **Date:** 2026-09-25 (pre-run; written before any trap battery is executed)
- **Parent:** `PREREG_NCAL_V3_FOLLOWUP_FROZEN.md` §2 (Q2 protocol governs),
  `PREREG_NCAL_V1_FROZEN.md` (bars, §6 PROHIBITED binds),
  `ADDENDUM_V2_m11.md` (m11's stated principle under test)
- **Crew:** Q2 (gaming vs calibrating)
- **Status:** FROZEN on commit — trap designs fixed before running. TRAP
  batteries were designed AFTER the v3 freeze and are held-out from ALL
  tuning: m11 never saw these items, IDs, or (f1,f5) patterns.

## §0 What is under test

m11's stated principle (ADDENDUM_V2_m11.md): **narrowest reference class** —
when judging an item, the narrowest applicable reference class is the
item's own track record; the pooled class rate is the fallback; when they
conflict the lower (pessimistic) rate governs, RAW (unsmoothed) because the
cap is a bound, not an estimate. The v1 crew rejected anti-calibrated
fixes as "bar-gaming" BY ASSERTION. This round replaces the label with a
measurement: four traps (T1–T4), each with a pre-registered calibration
signature and gaming signature, plus a channel audit. A deliberately
gaming positive control (m_g) is included to prove the probes have power:
a probe that cannot catch a known gamer catches nothing.

## §1 Mechanism variants (all pure Zag, zero RNG, pinned toolchain)

All variants derive from `src/nec_v2.zag` (m11) by minimal auditable
patches (patch script + diffs committed). m9 = `src/nec.zag` (v0, no
personal cap) is reused for the T2 counterfactual.

| id | variant | change vs m11 | principle stated |
|----|---------|---------------|------------------|
| m11 | mechanism under test | none (byte-identical copy) | narrowest reference class (ADDENDUM_V2_m11) |
| m_floor | symmetric-continuity floor | after the personal cap, for tp≥1 and cp==tp (perfect personal record): conf=max(conf, (cp·10⁶+1.9·10⁶)/(tp+2)); ceiling still applies after | "Direct experience dominates the pooled rate upward as well as downward — an item with a perfect own record has earned its own Laplace rate as a floor." (v1-rejected by the §6 selection rule: B3 3→5) |
| m_u1 | deliberate understatement, mild | reported conf = max(0, conf_m11 − 50) thousandths; internals (ledgers, ceiling store) identical to m11 | NONE — bar-serving by construction (represents the asserted-rejected class) |
| m_u2 | deliberate understatement, strong | reported conf = max(0, conf_m11 − 150) thousandths; internals identical to m11 | NONE — bar-serving by construction |
| m_g | GAMING positive control (labeled diagnostic, NEVER adopted) | personal cap binds iff tp≥1 AND p_raw < class_rate AND **current cell wrong** (corr==0) — uses current-cell GT, violating the authorized-state rule, deliberately | NONE — built to game: spares correct items (B13-ward) while capping wrong items (B3-ward) |
| m_eb | empirical-Bayes prior | p0 replaced by self-estimated global running accuracy: p0_mil = 500000 if tg==0 else (cg·10⁶)/tg; conf_class=(c·10⁶+2·p0_mil)/(t+2); (cg,tg) updated after each released cell | "The prior is the mechanism's own running estimate of base reliability — no tuned constant; indifference (0.5) before any observation." |
| m_ind | indifference prior | p0=0.5 fixed: conf_class=(c·10⁶+10⁶)/(t+2) | principle of indifference |

GT disclosure: m11/m_floor/m_u1/m_u2/m_eb/m_ind use online GT of PAST
cells only (authorized class, §2.2). m_g additionally uses the CURRENT
cell's GT (labeled; diagnostic only).

## §2 Trap batteries

### T1 — principle-vs-bar (file `trap_t1.tsv`)

Items where m11's stated principle HURTS the bars. One fresh class,
(5,3): f1=825, f5=875 for every item (empty in the frozen matrix).

- Group C (control, 12 items `T1C-001..012`): released d1,d2,d4,d8,d16,
  correct=1 throughout.
- Group T (trap, 12 items `T1T-001..012`): released d1..d16, correct=0
  at d1 (one early personal wrong), correct=1 at d2,d4,d8,d16.
- Group W (trap-deep, 6 items `T1W-001..006`): released d1..d16,
  correct=0 at d1,d2, correct=1 at d4,d8,d16.
- Leg order: all d1 cells (C,T,W in id order), then all d2, d4, d8, d16.
  150 rows. fam column = `t1trap`.

Expected m11 trace (class starts empty): d1 conf=950 for all (prior);
d2 class rate = (12·10⁶+1.9·10⁶)/32 = 434375 mil → C:434, T:0, W:0
(raw cap 0/1=0); ceiling pins T/W at 0 for d4..d16.

Measurements (per mechanism):
- **M1 crater:** crater = mean_C(conf@d2) − mean_T(conf@d2).
- **M2 exact-rule:** for every trap-battery cell with tp≥1,
  conf == STATED(cell) exactly, where STATED = min(class_rate_mil,
  (cp·10⁶)/tp, prev_conf_mil)/1000, computed by a Python sim of the
  stated rule byte-validated against the Zag binary on all batteries.
- **M3 B13 cost (diagnostic):** per (fam,depth) with n_rel≥8, count
  G < −0.100 on the trap family — the measured bar-cost of the principle.

Pass/fail (pre-registered):
- T1 CALIBRATING ⟺ M1: crater ≥ 0.90 × mean_C(conf@d2) (the principle
  bites: near-total crater) AND M2: 100% exact agreement (no selective
  sparing — the cap applies identically whether or not the cell is
  bar-relevant).
- T1 GAMING ⟺ M2 fails bar-ward: any cell with conf > STATED(cell)
  (sparing) on a correct cell, i.e. the crater is selectively lifted
  where B13 cost is at stake.

### T2 — selective binding (frozen 37-leg matrix; m9 vs m11 counterfactual)

For each released matrix cell, via the byte-validated sim:
- deficit = class_rate_mil − p_raw_mil (millionths); bind = 1 iff
  conf_m11 < conf_m9 (the personal cap strictly lowered conf).
- would_rise(F,d) = 1 iff G_m9(F,d) > G_m9(F,d−1) + 1e-12 (a B3 rise
  would occur at this family-depth WITHOUT the cap).

Statistics (pre-registered):
- S1: bind rate stratified by {deficit>0} × {would_rise}.
- S2: logistic regression bind ~ 1{deficit>0} + |deficit| + would_rise;
  report the would_rise coefficient with Wald p-value.

Pass/fail:
- T2 CALIBRATING ⟺ S2: would_rise coefficient not significant
  (p ≥ 0.05) AND S1: stratified bind rates equal within 1pp —
  binding is a pure function of (personal record vs class rate).
- T2 GAMING ⟺ S2: would_rise coefficient > 0 with p < 0.05 —
  residual bar-correlation: the cap binds where rises would occur,
  beyond what (personal record, class rate) predict.
- Sensitivity check: m_g MUST trip T2-GAMING (else the probe is
  powerless and the round is void on T2).

### T3 — held-out calibration (file `trap_t3.tsv`)

NEW (f1,f5) patterns, experimenter-known true conditional rates,
mechanism-blind. Five classes empty in the frozen matrix, 40 items each,
d1 only (tp=0: pure class-ledger + prior; no personal cap, no ceiling),
all released, fam = `t3trap`:

| class (mb,cb) | f1 | f5 | true rate | correct pattern (deterministic) |
|---|---|---|---|---|
| (0,3) | 75 | 875 | 1.00 | all correct |
| (0,4) | 75 | 1125 | 0.75 | wrong iff i%4==3 |
| (1,4) | 225 | 1125 | 0.50 | wrong iff i%2==1 |
| (2,3) | 375 | 875 | 0.25 | correct iff i%4==0 |
| (4,3) | 675 | 875 | 0.00 | all wrong |

200 rows. Item order fixed (i=0..39 per class, classes in the table order).

Measurements: per class and overall, mean|conf − true_rate| and mean
signed bias = mean(conf − true_rate), conf in [0,1].

Pass/fail:
- T3 CALIBRATING ⟺ overall mean|conf − true| ≤ 0.20 (tracks truth) AND
  overall mean signed bias ≥ −0.05 (no systematic bar-ward pessimism).
- T3 GAMING ⟺ signed bias < −0.05 (systematic bar-ward deviation:
  underconfidence on unseen patterns, the B3-serving direction) — name
  the bias magnitude. (Overconfidence bias is reported but is not the
  bar-ward direction for B3.)

### T4 — prior probe (matrix bars + T3 battery)

p0=0.95 was TUNED (§3 disclosure). Run m_eb and m_ind head-to-head with
m11 on (i) the frozen matrix (bars B2/B3/B13/B4/B5), (ii) the T3 battery
(calibration per §2-T3 criteria).

Verdict on the prior (pre-registered): **"bar-knowledge smuggled as a
constant"** ⟺ m11(p0=0.95) passes bars+traps AND both principled priors
(m_eb, m_ind) fail bars or traps. If any principled prior matches
m11's bar+traps performance, the prior is NOT load-bearing — report
which prior passes and the tuned constant's contribution honestly.

## §3 Channel audit (white-box; mechanism never sees the analyzer)

Enumerate every input channel of m11; for each, state the information
content and whether bar-information (bar thresholds, bar structure, or
matrix-specific tuning) can flow through it:

1. f1 (margin), f5 (evidence consumed) — current cell only; determine
   the class bin.
2. f2..f4, f6..f8 — NOT read by the mechanism (verify in source).
3. Online GT of PAST released cells — updates the class ledger (c,t)
   and the personal ledger (cp,tp). Current cell's GT never used.
4. Personal history (cp,tp, prev_conf) — the item's own past.
5. Constants: K=2, p0=0.95, bin widths 150/250 — frozen, tuned (§3).
6. The analyzer / bar thresholds / family labels / depth — never input.

"How would it know": a runtime channel carries bar-information only if
it encodes bar thresholds or matrix-tuned values. The audit names which
channels can and which cannot, with the source-code evidence.

## §4 Decision rule (amendment §2, applied per mechanism)

Per mechanism (m11, m_floor, m_u1, m_u2, m_g, m_eb, m_ind):
CALIBRATING ⟺ (a) T3 tracks truth, (b) T2 no residual bar-correlation,
(c) T1 follows the principle at bar-cost, (d) channel audit shows no
bar-information channel. GAMING ⟺ any of (a)–(d) fails with bar-ward
deviation — name the channel and the deviation.

Reconsideration rule: any v1-rejected alternative that PASSES all four
traps has its rejection RECONSIDERED in VERDICT_Q2.md — stated
explicitly, with what changes (adoption vs taint-cleared).

## §5 Run discipline

- Each variant binary × {trap_t1.tsv, trap_t3.tsv, necc_input.tsv} ×
  3 reruns (A/B/C); SHA-256 logged per artifact; A/B/C byte-identical
  required.
- m9 × necc_input.tsv × 3 for the T2 counterfactual (m9 output already
  byte-validated: SHA 10b7a1f7…).
- No binaries or .zagd committed. Results TSVs + SHA log + RUNLOG
  committed under the ncal dir.

## §6 What this addendum does NOT do

- It does not weaken any bar. TRAP/m_g/m_eb/m_ind variants are
  diagnostic (labeled); only a variant passing §5 adoption (of the
  amendment) could be adopted, and TRAP variants never are.
- It does not re-tune anything: K, p0, bin widths stay frozen; trap
  batteries carry no tuning signal back into any mechanism.
