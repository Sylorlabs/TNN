# PREDICTIONS_LOCKED addendum — corrected volume legs (vol2-a / vol2-b)

Dated 2026-09-27, locked BEFORE any vol2 run.

## Protocol correction

The prereg (§6.2) specifies the volume leg as 48 NEW items (8E+8W per family)
delivered as one 96-item block: **original 48 + 48 new**. The legs already run
as `vol-a`/`vol-b` used 96 ALL-NEW items (16E+16W per family) — a composition
deviation. Those legs are retained as supplementary "96-novel" measurements;
the prereg-compliant legs are `vol2-a`/`vol2-b` using `cal_vol2.txt` =
`cal_abc.txt` (48 original, cc01–cc48) + 48 new (first 8E+8W per family from
the authored sets, 16-byte-disjoint from the original 48 by verifier).

## A priori predictions

### vol2-a — design α, 48 orig + 48 new (C: 8 orig W + 8 new W), E→W

The original-48 C W-items under α already caused the abc-a catastrophe; adding
8 more novel C W-items can only add installs. PREDICT:
- `2c_sinc_dp_*` FAILS for ≥3 types (SINC-DP ≤5/10).
- `2c_sinc_lk_3` FAILS (≤5/10); `2c_sinc_lk_2`, `2c_sinc_lk_4` also FAIL.
- TR/PA/NO per type stay ≥16/20.
- MDUMP: live (status 1) joke field-1 markers `says evenly` present.
- Falsification: all 2c bars pass → the abc-a/vol-a catastrophe does not
  survive the 48+48 composition (e.g. original-48 E-items change the dynamics).

### vol2-b — design β, 48 orig + 48 new, E→W

β pool = 40 + 48 E-items (24 orig + 24 new) = 88 entries, as the prereg
specifies. PREDICT:
- ALL `2c_*` checks PASS; `2c_sinc_lk_3` ≥9/10.
- The prereg's ceiling prediction (§6.2: "no better than L1–L4") is tested
  here: L1–L4 hit 9/10; a 10/10 here favors "β+C genuinely helps" over
  "ceiling effect".
- MDUMP: joke `says evenly`/`says plainly` CTX markers status 3 (revoked).
- Falsification: any 2c SINC-DP/LK failure → volume churns even under β.

## Standing predictions (unchanged)

Determinism 3/3 byte-identical per leg; frozen `H7_CHECK` lines show only the
pre-existing `sinc_lk_3` failure; `2CITEMS|96|design|0|pool|40` (vol2-a) and
`2CITEMS|96|design|1|pool|88` (vol2-b).
