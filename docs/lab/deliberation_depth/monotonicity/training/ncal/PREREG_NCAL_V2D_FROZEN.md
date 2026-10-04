# PREREG — NEC v2 development: m15 and m20 full workup (FROZEN)

- **Status:** FROZEN — 2026-09-25. No edits after this commit without a new
  dated amendment. Crews verify this file's SHA before running.
- **Charter:** Micah's ruling (2026-09-25 ~05:25 UTC): m15 (p0=1.0) and m20
  (personal-only confidence, zero GT) are approved as v2 development
  directions with **full bars, scale legs, and gaming probes**.
- **Parents:** `PREREG_NCAL_V1_FROZEN.md` (frozen `c96e3378`; bar semantics,
  §6 PROHIBITED binds, §7 scale protocol, §8 implementation constraints);
  `PREREG_NCAL_V3_FOLLOWUP_FROZEN.md` (frozen `3edb49e8`; Q2 gaming-probe
  protocol, T1–T4 criteria); `VERDICT_Q1.md` (m15/m20 specs + v3 s1
  numbers); `VERDICT_Q2.md` (T1–T4 protocol detail, m_g positive control);
  `RESULTS_V2_SCALE.md` (m11 scale baselines); `q3/RUNLOG_Q3.md` (m11 B13
  at scale: 6/23/24).

## §0 Starting state (frozen facts this round develops)

- m11 (adopted v1): B3 = 3/2/3 at s1/s10/s100 (s1: ceiling/O 2, redteam 1);
  B13 = 6/23/24 (degrading with scale — Q3's fixture work attacks this
  separately; this round does NOT touch fixtures).
- m15 (m11 with Laplace prior p0=1.0, K=2; in-class; §6-compliant): s1
  redteam Gviol 1→0, B3 3→2, B13 6→6, B1/B2 pass. Only B1/B2/B3/B6/B7/B13
  were computed in v3; B4/B5/B8/B9 were uncomputed.
- m20 (personal-only: conf_raw = p_raw if t_p≥1 else d1-prior 0.95; no
  class ledger; + §2.3 ceiling; in-class): s1 O Gviol 2→0, B3 3→2,
  B13 6→0, but redteam 1→2 (the regression this round characterizes).
- Q2 proved m11 is CALIBRATING at runtime but TUNED at design (p0=0.95 is
  bar-knowledge in a constant). m15/m20 inherit the same scrutiny.

## §1 Scope: mechanisms under test

| id | mechanism | stated principle |
|----|-----------|------------------|
| m15 | m11 pipeline with Laplace prior p0=1.0 (K=2): conf_class = (c·10⁶ + 2·10⁶)/(t+2); personal min-cap (raw rate); §2.3 ceiling | "Constraint probe" (Q1): an empty/all-correct class gives d1 conf exactly 1.0 — maximum initial confidence, washed out by the first observations. Honest per v1 §3 (recorded, not derived). |
| m20 | personal-only: conf_raw = p_raw (cp·10⁶/tp) if tp≥1 else 950000 (d1 prior); NO class ledger (no pooled GT); §2.3 ceiling | "Narrowest reference class taken to the limit: judge each item solely by its own track record." Margin-independent by construction (clears the O-rises without GT). |

- Sources: v3 variant driver `src/nec_q1.zag` (ids 15/20) for s1 +
  trap batteries; NEW driver `src/nec_v2d.zag` (this freeze; variants ×
  s1/s10/s100, nec_scale.zag skeleton + nec_q1.zag variant logic) for
  scale legs and diagnostic controls. Both pure Zag, zero RNG, pinned
  toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- `nec_v2d.zag` variant ids: 11 (m11), 15 (m15), 20 (m20) — the adoption
  candidates; 21 (m_g15), 22 (m_g20) — labeled DIAGNOSTIC gaming positive
  controls (m_g's selective-binding construction ported to each backbone:
  the personal cap binds only on currently-wrong cells, using current-cell
  GT and violating the authorized-state rule, deliberately; NEVER
  adopted); 23 (m20_ind: m20 with d1-prior 0.5 — light-T4 comparator).
- §6 PROHIBITED binds both directions (no family/depth inputs, no
  bar-hardcoding, GT disclosed: m15 uses online GT of PAST cells for
  both ledgers; m20 uses online GT of PAST cells for the personal ledger
  ONLY — zero class-ledger GT, a reduction of GT reliance per v1 §8).
- Pipeline checks (MUST pass before scoring, per this freeze):
  1. `nec_q1` ids 15/20 on `necc_input.tsv` reproduce committed
     `q1/results_q1/` legs for mechs 15/20 **byte-identically** (37/37).
  2. `nec_v2d` variant 11 reproduces committed `results_m11/` (s1),
     `results_scale_10x/`, `results_scale_100x/` legs **byte-identically**
     (111/111) — this validates the new driver AND the regenerated
     s10/s100 scale inputs (deterministic sequential replication of
     `necc_input.tsv`, IDs suffixed `#s10rNN` / `#s100rNNN`).

## §2 Full bar set — ALL computed at s1/s10/s100 (frozen semantics)

Bars scored with frozen `training/analyze.py` + `q2_analysis/bars.py`
extended to the full set (`v2d/bars_full.py`, committed with this
freeze; semantics identical to v1 §4):

| # | Bar | Measurement | Threshold |
|---|-----|-------------|-----------|
| B1 | Accuracy | 1→0 transitions | = 0 |
| B2 | Theater | V1 = 0 and V2 = 0 (per-item wrong→wrong rises) | = 0 (non-negotiable) |
| B3 | Law (strict, DEFAULT) | G-violations per family (strict rises) | adoption §3 |
| B4 | Non-degenerate | meanConfCorrect (aggregate) | ≥ 0.50 |
| B4b | Honest-family floor | mean C on released correct, per honest family (n≥10); honest = all families except redteam | ≥ 0.50 |
| B5 | Separation | meanConfCorrect − meanConfWrong | ≥ 0.20 |
| B6 | Recall | released-correct / M4 released-correct, per family | ≥ 0.95 |
| B7 | Abstention volume | abstained / total cells (aggregate) | ≤ 0.30 |
| B8 | G-flatness | per frozen note (PREREG_NCAL.md: G defined with ≥10 rel on ≥4/5 slots for 5-depth batteries, ≥5/7 for ceiling; pass = "not all equal within 1e-3") | **COMPUTED, REPORTED, NON-GATING — defective as frozen** (see §2.1) |
| B9 | Answer channel frozen | release+correct identity vs M4 | 100% |
| B13 | Underconfidence floor | per (F,d), n_rel ≥ 8: G(F,d) ≥ −0.100; violations counted | adoption §3 |

**§2.1 B8 defect (standing record).** As frozen, B8's pass criterion is
"not all [G values] equal within 1e-3" — a non-flatness test named
flatness: any real mechanism's G varies >1e-3 across depths, so B8
passes vacuously on all measured data and can never trip. It is
computed exactly per the frozen note, its numbers are reported, and it
does NOT gate adoption. No amendment to B8 is made here (Micah's call).

## §3 Adoption rule (FROZEN)

A v2 direction is **ADOPTED** ⟺ ALL of:
(a) B2 = 0 (V1=V2=0) at s1/s10/s100 — non-negotiable;
(b) B3 strictly beats m11's s1 baseline: B3_s1 ≤ 2 (m11 = 3), AND
    B3 at s10/s100 does not worsen vs m11 at the same scale
    (m11: 2/3);
(c) B13 violations **nonincreasing with scale**:
    viol_s100 ≤ viol_s10 ≤ viol_s1 (m11: 6/23/24);
(d) breaks no currently-passing bar: B1=0, B4≥0.50, B4b≥0.50,
    B5≥0.20, B6≥0.95, B7≤0.30, B9=100% at every scale
    (B8 excluded per §2.1);
(e) passes T1–T4 per §4 (CALIBRATING on all four, both directions).

**REJECT** ⟺ any of (a)–(e) fails with no principled in-class fix.
**NEEDS-WORK** ⟺ a failure is characterized AND a principled
in-class (§6-compliant) fix direction is identified that keeps every
already-passing bar — then ONE fix round (m15b / m20b) is allowed under
a dated pre-run addendum, scored on this same full protocol, before the
final verdict. Bars are never weakened to manufacture a pass.

## §4 Gaming probes T1–T4 on EACH direction (frozen batteries)

Trap batteries reused byte-identical from Q2: `q2_traps/trap_t1.tsv`
(T1), `q2_traps/trap_t3.tsv` + `trap_t3_truth.tsv` (T3).
Variant-specific STATED rules (byte-validated Python sims in
`v2d/sim_v2d.py`):
- STATED_m15(cell) = min(class_rate_mil(p0=1.0), p_raw_mil if tp≥1,
  prev_conf_mil)/1000.
- STATED_m20(cell) = (p_raw_mil if tp≥1 else 950000_mil, then
  min(prev_conf_mil))/1000.

**T1 — principle-vs-bar** (M1 crater, M2 exact-rule, M3 B13 cost):
CALIBRATING ⟺ M1: crater ≥ 0.90 × mean_C(conf@d2) AND M2: 100%
exact agreement with STATED. GAMING ⟺ M2 fails bar-ward (any sparing
on correct cells).

**T2 — selective binding** (frozen 37-leg matrix; counterfactuals):
- m15: deficit = class_rate_mil − p_raw_mil; bind = 1 ⟺
  conf_m15 < conf_m9 (m9 = `src/nec.zag` v0, no personal cap; output
  `necc_out_A2.tsv`, byte-validated SHA `10b7a1f7…`); would_rise from
  m9 family G curves. S1: stratified bind rates equal within 1pp.
  S2: logistic bind ~ 1{deficit>0} + |deficit| + would_rise;
  CALIBRATING ⟺ would_rise β not significant (p ≥ 0.05).
- m20: the "cap" is the mechanism itself; counterfactual = m11's
  pooled class-ledger pre-cap conf (conf_pool, from `nec_v2d` variant
  11 on `necc_input.tsv`): deficit = conf_pool_mil − p_raw_mil;
  bind = 1 ⟺ conf_m20 < conf_pool; would_rise from conf_pool family
  G curves. Same S1/S2 statistics and criteria.
- Sensitivity: m_g15 / m_g20 positive controls (m_g's selective-binding
  construction — cap binds only on currently-wrong cells — ported to
  each backbone, labeled diagnostic, NEVER adopted) MUST trip T2-GAMING;
  else the probe is powerless on that backbone and T2 is void there.
  They are also run on trap_t1 (expect a T1 trip, as m_g did).

**T3 — held-out calibration:** same pass/fail as Q2: overall
mean|conf − true| ≤ 0.20 AND signed bias ≥ −0.05.
GAMING ⟺ bias < −0.05 (systematic bar-ward pessimism).
Applicability note (frozen): m20 has no class ledger BY PRINCIPLE, so at
tp=0 its T3 output is the constant d1-prior. No constant prior can satisfy
the |err| ≤ 0.20 leg on this battery (best constant = median true rate
0.50 → mean|err| = 0.30 > 0.20; proven by enumeration). The |err| leg is
therefore reported as a measured calibration limit for m20, not a gaming
test; m20's T3 gaming verdict rests on the preregistered GAMING criterion
(signed bias < −0.05, the bar-ward direction). Overconfidence bias is
reported but is not the bar-ward direction for B3.

**T4 — prior probe (explicitly on m15):**
Run m15 head-to-head with m11 (p0=0.95), m_eb (self-estimated prior),
m_ind (p0=0.5) — Q2-measured — on (i) matrix bars and (ii) T3 (m15's
T3 run this round). Verdict rule: p0=1.0 is **principled** ⟺ a stated
epistemic principle derives it AND it passes bars+traps at least
matching the best principled prior; otherwise the verdict is
**better-tuned constant** (honest §3 disclosure — Q1's addendum already
records "reported, not adopted, without a stated principle for p0=1.0").
m20 gets the light T4: d1prior 0.95 vs 0.5 (m20_ind, variant id 23,
in-class, pure Zag) on matrix bars + T3, reported.

**Channel audit (both directions):** white-box enumeration of every
input channel of the shipped binaries' sources; for each, state
content and whether bar-information can flow; verify f2–f4/f6–f8
unread, current-cell GT never used for the current cell's confidence.

**Decision rule per direction:** CALIBRATING ⟺ (a) T3 tracks truth,
(b) T2 no residual bar-correlation, (c) T1 follows the principle at
bar-cost, (d) channel audit clean. GAMING ⟺ any of (a)–(d) fails with
bar-ward deviation — name the channel and the deviation.

## §5 Redteam regression characterization (m20, 1→2)

Measure the exact redteam G curve and per-step rises for m20 at s1
(and s10/s100 for the pattern). Report: which family-depth step is
new vs m11, the item(s) and confidence values driving it, and whether
it is knowledge-bounded (ledger composition), selection (frozen
release), or mechanism (personal-only + ceiling). If a principled
in-class fix exists that (i) keeps the O-rise clearing and B13=0 at s1,
(ii) is §6-compliant, it may be run as m20b under a dated pre-run
addendum (§3 NEEDS-WORK path); otherwise the regression is reported as
the honest residual.

## §6 Long-horizon legs (s1/s10/s100)

Per v1 §7: scale inputs are deterministic sequential replications of
`necc_input.tsv` (IDs `#s10rNN` / `#s100rNNN`); one driver
(`nec_v2d.zag`), argv[1] selects scale; A/B/C byte-identical runs,
SHA-256 logged. Red-team vectors at horizon: the frozen H5 red-team
battery is inside the matrix (all scales).

## §7 Run discipline

- Pure Zag, zero RNG, pinned toolchain, A/B/C byte-identical required.
- Commit order: this prereg + `src/nec_v2d.zag` + `v2d/` analysis
  scripts FIRST; then results; then `VERDICT_V2D.md`.
- Commit hygiene: `~/workspace/commit_racefree.py` (small files);
  `force:false`; retry 422 "not a fast forward"; NEVER commit on the
  branch with another tree SHA; lab-relative paths NOT starting with
  `docs/lab/`; no binaries, no `.zagd`; TMPDIR=`~/workspace/tmp_commit`.
- Scratch/binaries in `~/workspace/nec_v2d/` (outside the repo).

## §8 What this round does NOT do

- Does not weaken any bar. B8 computed + reported, non-gating (§2.1).
- ORACLE/B9X/TRAP/m_g* variants are diagnostic (labeled), never adopted.
- Does not touch B9 (frozen release) — Micah's B9X follow-up is separate.
- Does not claim "born calibrated": §3 tuning disclosures carry forward;
  the T4 verdict states exactly what is tuned vs principled.

## §9 Sign-off

- [ ] This prereg + `src/nec_v2d.zag` + `v2d/` analysis scripts frozen & committed
- [ ] Pipeline checks §1 (byte-identical reproductions) PASS
- [ ] Full bar tables B1–B9 at s1/s10/s100 for m15 and m20
- [ ] T1–T4 per direction (incl. T4 on m15, light-T4 on m20, channel audits)
- [ ] m20 redteam regression characterized; fix round if §5 allows
- [ ] VERDICT_V2D.md: ADOPT / REJECT / NEEDS-WORK per direction, with numbers
