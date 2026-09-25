# VERDICT — m11 + FIX-A (pure-Zag pipeline), s1/s10/s100

Frozen mechanism m11; fixtures from pure-Zag `q3/fixbuild.zag`
(byte-identical to the deleted Python — proof in `SHA_LOG_FIXA_ZAG.md`).
Driver outputs 3× byte-identical per scale and match the Q3 reference SHAs.

## Bar table (B1–B9 + B13)

| Bar | s1 | s10 | s100 | Bar | Met |
|---|---|---|---|---|---|
| B1 (1→0 = 0) | 0 | 0 | 0 | = 0 | YES |
| B2 (V1 / V2 = 0) | 0 / 0 | 0 / 0 | 0 / 0 | = 0 | YES |
| B3 (G-viol, ≤3, not worsened vs m11=3) | 1 | 2 | 2 | ≤ 3 | YES |
| B4 (meanConfCorrect ≥ 0.50) | 0.990 | 0.982 | 0.981 | ≥ 0.50 | YES |
| B4b (per honest family ≥ 0.50) | min 0.946 | min 0.955 | min 0.950 | ≥ 0.50 | YES |
| B5 (separation ≥ 0.20) | 0.862 | 0.891 | 0.896 | ≥ 0.20 | YES |
| B6 (recall vs M4 ≥ 0.95) | 1.0 | 1.0 | 1.0 | ≥ 0.95 | YES |
| B7 (abstention ≤ 0.30) | 0.148 | 0.148 | 0.148 | ≤ 0.30 | YES |
| B8 (G-flatness) | computed | computed | computed | — | REPORTED ONLY |
| B9 (release+correct identity vs M4) | 100% | 100% | 100% | 100% | YES |
| B13 (G ≥ −0.100 per (F,d), n_rel≥8) | 0 viol | 0 viol | 0 viol | 0 | YES |

B4b minima: s1 — O family 0.946 (n=180); s10 — redteam 0.955 (n=50);
s100 — redteam 0.950 (n=500). All honest families pass with wide margin.

B8 detail (frozen-defective — computed, reported, NOT gated): the bar
requires G "not all equal within 1e-3" on families with enough defined
slots. It trips precisely on the best-calibrated families (s10/s100:
logic, revoke, cost — G constant to 3 decimals because calibration is
genuinely good; s1: logic). The bar punishes the flatness that good
calibration produces — the defect. Per-family table:

| Scale | pass | FLAT (bar trips) | family-excluded (<4/5 slots) |
|---|---|---|---|
| s1 | D,O,P,admit,cost,revoke | logic | redteam (0/5), trap (2/5) |
| s10 | admit,cost,redteam | logic,revoke | trap (3/5) |
| s100 | admit,redteam | cost,logic,revoke | trap (3/5) |

## Adoption eligibility

m11 + FIX-A meets every gating bar at s1/s10/s100 with the pure-Zag
pipeline: B1=0, B2=0/0, B3 ≤ 2 (≤ m11's 3), B4/B4b/B5 with wide margins,
B6=1.0, B7=0.148, B9=100%, B13=0/0/0. Determinism: 3× byte-identical at
each scale. The Python generator is deleted; the Zag port is proven
byte-identical.

Two disclosed caveats (unchanged from Q2/Q3, now re-measured on the Zag
pipeline):
1. T4: p0=0.95 remains load-bearing design tuning (m_ind still fails B13
   with 5 violations under FIX-A; m_eb converges to m11's profile).
   Design-level, disclosed — not runtime gaming (T1/T2 clean).
2. T3: FIX-A is a blunt diet instrument — it overconfidences classes with
   true rate < 0.95 (probe: bias +0.302). Safe for NEC-like deployment
   distributions; miscalibrated for genuinely low-rate classes.

**Eligible for adoption** on the NEC distribution, with the two caveats
above disclosed. B8 remains frozen-defective and non-gating.
