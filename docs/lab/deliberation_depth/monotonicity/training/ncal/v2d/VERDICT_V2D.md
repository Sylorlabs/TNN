# VERDICT — NEC v2 development (m15 / m20 full workup)

- **Date:** 2026-09-25 (PDT)
- **Protocol:** `PREREG_NCAL_V2D_FROZEN.md` (frozen 3041ffc3, before any run; gen_scale.py numbering fix f874dfad, pre-scoring)
- **Drivers:** `src/nec_v2d.zag` (variants 11/15/20/21/22/23), `src/nec_q1.zag` (variants 15/20)
- **Toolchain:** pinned `znc_linux_x86_64_abed8aa1` (SHA-256 `498abcb5…`)
- **Determinism:** every run A/B/C byte-identical (SHA log in RUNLOG.md). Zero RNG. Pure Zag.

## 1. Full bar tables (B1–B9, B13) at s1/s10/s100

m11 baseline (frozen): B3 = 3/3/3 (s1/s10/s100 B3 not separately recorded; s1=3), B13 = 6/23/24.

| Bar | m15 s1 | m15 s10 | m15 s100 | m20 s1 | m20 s10 | m20 s100 |
|-----|--------|---------|----------|--------|---------|----------|
| B1 (1→0 flips) | 0 ✓ | 0 ✓ | 0 ✓ | 0 ✓ | 0 ✓ | 0 ✓ |
| B2 (V1/V2) | 0/0 ✓ | 0/0 ✓ | 0/0 ✓ | 0/0 ✓ | 0/0 ✓ | 0/0 ✓ |
| B3 (G-violations) | **2** ✓ | 2 | 3 | **2** ✓ | 2 | 2 |
| B4 (mean conf\|correct) | 0.977 ✓ | 0.911 ✓ | 0.900 ✓ | 0.950 ✓ | 0.950 ✓ | 0.950 ✓ |
| B4b (honest-fam min) | 0.571 ✓ | 0.605 ✓ | 0.614 ✓ | 0.950 ✓ | 0.950 ✓ | 0.950 ✓ |
| B5 (B4 − wrong-conf) | 0.876 ✓ | 0.847 ✓ | 0.842 ✓ | 0.543 ✓ | 0.543 ✓ | 0.543 ✓ |
| B6 (M4 recall) | 1.000 ✓ | 1.000 ✓ | 1.000 ✓ | 1.000 ✓ | 1.000 ✓ | 1.000 ✓ |
| B7 (abstention) | 0.148 ✓ | 0.148 ✓ | 0.148 ✓ | 0.148 ✓ | 0.148 ✓ | 0.148 ✓ |
| B8 (defective) | FAIL* | FAIL* | FAIL* | FAIL* | FAIL* | FAIL* |
| B9 (identity) | 1.000 ✓ | 1.000 ✓ | 1.000 ✓ | 1.000 ✓ | 1.000 ✓ | 1.000 ✓ |
| **B13** | **6** | **23** | **24** | **0** | **0** | **0** |

\* B8 computed per the frozen defective definition, reported, NON-GATING (standing instruction).
m11/m15 fail B8 on `logic` (G flat within 1e-3); m20 fails on O/admit/cost/logic/revoke
(its G is flat at −0.050 — the flatter the curve, the harder B8 is to pass, which is the defect).

**Adoption-rule check:**
- m15: B3(s1)=2 < 3 ✓. B13 = 6/23/24 — identical to m11 at every scale; **fails the
  frozen "no scale-wise increase" clause** (6→23→24). No passing bar broken ✓.
- m20: B3(s1)=2 < 3 ✓. B13 = 0/0/0 — **nonincreasing** ✓. No passing bar broken ✓.

## 2. T1 — principle-vs-bar (trap_t1)

| variant | M1 crater (C−T@d2) | M1 pass | M2 exact-rule | M3 B13-cost |
|---------|-------------------|---------|---------------|-------------|
| m15 | +0.515 (C=0.515, T=0.000) | True | 150/150 (100%) | 4 (= m11) |
| m20 | +0.950 (C=0.950, T=0.000) | True | 150/150 (100%) | 4 (= m11) |
| m_g15 (control) | −0.097 | **False** | 102/150 (68%) | 4 |
| m_g20 (control) | +0.000 | **False** | 102/150 (68%) | 3 |

m15/m20: **CALIBRATING** (principle bites, exact rule, no added cost vs m11).
The g-controls trip T1 as designed (selective sparing: max +647/+950 on correct cells),
confirming T1-M2 has power against correctness-selective gaming.

## 3. T2 — selective binding (s1 matrix)

- **m15:** bind ⟺ deficit>0 exactly (264 binds). S1: within def>0, bind rate 1.000
  vs 1.000 across would_rise strata (Δ=0pp); within def≤0, 0.000/0.000. S2:
  would_rise β=+1.11, p=1.0 (perfect separation).
  → Mechanical deficit binding, no rise-selective gaming-direction selectivity.
- **m20:** S1: within deficit>0, bind 1.000/1.000; within deficit=0, bind 0.899
  (would_rise=0) vs 0.282 (would_rise=1) — **anti-gaming direction**. S2: would_rise
  β=−3.12, p≈0 (significant negative). → No gaming; significant anti-selectivity.
- **Probe-power caveat (disclosed):** m_g15/m_g20 outputs are **byte-identical** to
  m15/m20 on the matrix (verified: same SHAs). Per-item correctness is constant
  across depths in the matrix battery, so "bind only on wrong cells" coincides
  exactly with the full cap — the controls are degenerate on this battery, not
  because the S1/S2 probe is powerless but because the control adds no variation.
  T2's S1/S2 statistics stand on their own (no gaming-direction selectivity found
  for either backbone). T1-M2 is the probe that catches correctness-selective
  gaming, and it fires on the g-controls.

## 4. T3 — held-out calibration (trap_t3)

| variant | mean\|err\| | bias | verdict |
|---------|-----------|------|---------|
| m11 (Q2) | 0.092 | +0.089 | PASS |
| m_eb (Q2) | 0.070 | +0.065 | PASS |
| m_ind (Q2) | 0.055 | +0.015 | PASS |
| m15 | 0.097 | +0.097 | PASS |
| m20 | 0.470 | +0.450 | **\|err\| FAIL** (disclosed limit, see §6) |
| m20_ind (d1prior 0.5) | 0.300 | +0.000 | **\|err\| FAIL** (disclosed limit) |

m15 passes T3 but is slightly *more* overconfident than m11 (+0.097 vs +0.089);
the ladder shows lower priors calibrate better (ind 0.055 < eb 0.070 < m11 0.092).
m20/m20_ind: no GAMING (bias +0.450/+0.000, not < −0.05 bar-ward); the |err|
failures are the preregistered measured calibration limit of a constant prior
on unseen classes (m20 has no class ledger by principle).

## 5. T4 — prior vs principle (m15); light-T4 (m20)

**T4-A (washout):** m11 vs m15 conf identical on only 14.8% of released cells
(output precision); the prior binds on 85.2%, propagating through the class
ledger AND the per-item ceiling chain (d1: 950 vs 1000 seeds all later depths).
**T4-B (bar ladder, s1):** B3: m15=2 < m11=3 = m_ind=3 < m_eb=4. B13: m11=m15=m_eb=6
< m_ind=11. The "principled" empirical-Bayes prior is *worse* on B3 (4); the
indifference prior is worse on B13 (11).
**T4-C (T3 ladder):** §4 — m15 more overconfident than m11.

**Where m15's B3 gain comes from:** it clears the redteam d4→d8 rise (+0.025 → 0).
Mechanism: p0=1.0 raises the pooled class_rate, lifting RT-M3-01's d4 conf from
950 to 1000, flattening G(d4) from −0.025 to 0.000. M3's personal channel does
NOT bind (p_raw=1000 ≥ class_rate) — the gain is entirely the **pooled class-ledger
margin**, with no personal-channel story. Per the preregistered T4 criterion
(prior binds mechanically + no personal-channel story + overconfidence
uncorrected on T3), **m15's p0=1.0 is classified as TUNING, not a derived
principle**. (Q1 had already described p0=1.0 as a constraint probe; T4 confirms
no principle emerged. The Laplace-canonical-prior argument is noted but does not
survive the preregistered test: the gain is a broad mechanical prior effect.)

**m20 light-T4:** d1prior 0.95 → 0.5: matrix bars unchanged in structure
(B3=2, B13=0 both; conf binary {500,0} vs {950,0}); T3: |err| 0.470→0.300,
bias +0.450→+0.000 (unbiased but still too coarse). Reported, no adoption claim.

## 6. m20 redteam characterization + principled-fix analysis

m20 redteam B3: 2 violations — d4→d8 **+0.025** (inherited from m11) and d2→d4
**+0.008** (new vs m11's 1).
- The +0.008: at d2, released set = {M3,M6 correct@950; K12 wrong@0}, G=−0.033.
  At d4, M6 abstains (frozen rel=0), released = {M3 correct@950; K12 wrong@0},
  G=−0.025. The rise is **purely the abstention-composition change** (denominator
  3→2); K12's conf=0 is *earned* (wrong at d1, p_raw=0) and M3/M6's 950s are
  correct. No cell is miscalibrated.
- **Principled-fix analysis:** no mechanism-side fix eliminates a
  composition-driven rise without (a) dishonestly raising K12's earned conf,
  (b) altering the frozen release pattern (out of scope), or (c) re-adding
  pooled smoothing (which would reintroduce the O-rises m20 clears — contrary
  to the design). The O-clearing is structural (binary confs from constant
  per-item correctness ⇒ flat G), not tuned, so it is retained under any
  fix that preserves the personal-only design. **Conclusion: no principled
  mechanism fix exists; none tested** (per protocol, no addendum frozen since
  no fix qualifies).

## 7. Channel audit (white-box, nec_v2d.zag)

- m15: conf = min(class_rate(p0=1.0), p_raw if tp≥1, prev_conf); updates (class
  ledger, personal ledger, ceiling) all AFTER conf. Authorized state only
  (past releases' corr; f1/f5 stimulus features). No GT of the current cell.
- m20: no class ledger reads or writes (verified in source); conf = p_raw
  (tp≥1) else d1prior; same ceiling. **Disclosure:** "zero GT" means zero
  *pooled* GT — the personal ledger still learns from the item's own past
  corr (as does m11/m15). The elimination is of cross-item pooling, not of
  all ground truth.
- Determinism: input-order output, FNV-1a map for lookup only, no RNG/time.

## 8. Verdicts

**m15: REJECT.** Improves B3 (3→2) with zero bar regressions and passes T1/T2/T3,
but (a) fails the frozen B13 adoption clause — B13 = 6/23/24 exhibits the exact
scale-wise increase the rule forbids (identical to m11; no improvement where the
rule demands nonincrease), and (b) T4 classifies p0=1.0 as tuning under the
preregistered criterion (broad mechanical prior binding, B3 gain via the pooled
margin with no personal-channel story, T3 overconfidence uncorrected and
slightly worsened). A better-tuned prior with no principle and no B13-scale
improvement does not meet the adoption bar as frozen.

**m20: ADOPT (with disclosed limits).** Meets every frozen adoption criterion:
B3(s1)=2<3; B13=0/0/0 nonincreasing with scale (6/23/24 → 0/0/0); no passing bar
broken at any scale; T1 CALIBRATING; T2 no gaming-direction selectivity
(significant anti-selectivity); T3 no GAMING (bias +0.450, overconfident
direction, not bar-ward). **Disclosed limits:** (1) T3 |err|=0.470 — the
preregistered measured calibration limit of the constant d1-prior on unseen
classes (no class ledger by principle; cannot be fixed without defeating the
design); (2) redteam B3 1→2 — the +0.008 is a frozen-abstention composition
artifact with no principled mechanism fix (characterized in §6, O-clearing
retained structurally); (3) conf is binary {950,0} on constant-correctness
batteries (coarse but honest); (4) B8 fails (defective bar, non-gating).

## 9. Provenance

- Freeze: 3041ffc3 (prereg + nec_v2d.zag + v2d/ scripts + RUNLOG skeleton).
- gen_scale.py 1-based fix: f874dfad (pre-scoring; pipeline check now 111/111).
- Pipeline: nec_q1 15/20 → 37/37 each vs committed Q1 legs; nec_v2d-11 → 111/111
  vs committed m11 legs (s1/s10/s100).
- sim_v2d.py byte-validated vs Zag for m11/m15/m20; check_g.py byte-validated
  variants 21/22/23 (scratch, reported).
- All runs A/B/C byte-identical; SHA logs in RUNLOG.md.
