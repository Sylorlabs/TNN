# RESULTS — NEC variant m11 (ADDENDUM_V2_m11.md), s1/s10/s100

- **Date:** 2026-09-25
- **Mech:** m11 (hierarchical personal ledger, raw-rate pessimistic cap)
- **Binary:** `src/nec_scale.zag` (one binary, `argv[1]` = s1/s10/s100; m11 logic;
  s1 output bit-identical to `src/nec_v2.zag`)
- **Scale inputs:** deterministic 10x/100x replication of frozen `necc_input.tsv`
  (sequential passes, IDs suffixed `#s10rNN` / `#s100rNNN`)

## Bar summary (frozen analyzer + bars.py)

| Bar | v0 (s1) | m11 s1 | m11 s10 | m11 s100 |
|-----|---------|--------|---------|----------|
| B1 (1→0) | 0 | 0 | 0 | 0 |
| B2 V1 | 0 | 0 | 0 | 0 |
| B2 V2 | 0 | 0 | 0 | 0 |
| **B3 G-viol** | **6** | **3** | **2** | **3** |
| B4 | 0.972 | 0.972 | 0.909 | — |
| B5 | 0.668 | 0.874 | 0.846 | — |
| B7 | 0.148 | 0.148 | 0.148 | — |
| B13 | 6 | 6 | 23 | — |

B3 breakdown:
- s1: ceiling/D 0, ceiling/O 2, redteam 1
- s10: ceiling/D 0, ceiling/O 0, redteam 2
- s100: ceiling/D 0, ceiling/O 1, redteam 2

## Selection-rule verdict (§6)

- (a) B2 remains V1=0, V2=0 at all scales ✓
- (b) B3 strictly decreases vs v0 at s1 (6→3) ✓
- (c) No passing bar breaks (B1/B2/B4/B5/B7/B4b all ≥ v0 at s1) ✓
- (d) B13 does not worsen at s1 (6→6) ✓
- **ADOPTED.**

## A/B determinism

- s1: byte-identical (SHA `0fe2a9bf…`)
- s10: byte-identical (SHA `94c56e56…`)
- s100: byte-identical (SHA `d7fbb08f…`)

## Red-team containment (H5 vectors, K12 adversarial)

| Scale | K12 d1 | K12 d2+ | M3 min |
|-------|--------|---------|--------|
| s1 | 0.994 | 0.000 | 0.950 |
| s10 | 0.997 | 0.000 | 0.686 |
| s100 | 0.997 | 0.000 | 0.674 |

K12 (wrong every depth) is contained to 0.0 from d2 onward at all scales
(personal cap: 0/1, 0/2, …). d1 uses the class rate (no personal history
yet — first-observation unavoidable).

## Honest residual (B3 cannot reach 0)

1. **redteam d4→d8 (+0.522 s1): PROVEN unsatisfiable.** Given B9 (frozen
   release), B2, the §2.3 ceiling, and conf ≤ 1.0: containing K12 requires
   c_K12(d8)=0, which forces c_M3(d4) ≥ 1.0, but the ceiling caps
   c_M3(d4) ≤ c_M3(d1) = (c+1.9)/(t+2) < 1.0 strictly. Contradiction.
2. **redteam d2→d4 at s10/s100: selection effect.** With a warm/stable
   ledger, M6 (correct) has conf ~0.52; when M4 abstains it at d4, acc
   falls faster than mean-conf → G rises. Structural (calibrated conf +
   frozen abstention).
3. **ceiling/O micro-rises (+0.019/+0.005 s1, 1e-5 s100): structural.**
   M4 abstains below-mean-conf items; removing them raises the mean.
   Fixing requires anti-calibrated confidence (barred).

## Files

- `ADDENDUM_V2_m11.md` — preregistered mechanism, principle, targets,
  negative results, unsatisfiability proofs (written before run)
- `src/nec_v2.zag` — m11 mechanism (s1)
- `src/nec_scale.zag` — m11 mechanism + s1/s10/s100 scale selection +
  hash-map item lookup (bit-identical to nec_v2.zag on s1; verified)
- `results_m11/` — 37 s1 legs (mech 11), A-run
- `results_scale_10x/` — 37 s10 legs (mech 10), A-run
- `results_scale_100x/` — 37 s100 legs (mech 10), A-run
