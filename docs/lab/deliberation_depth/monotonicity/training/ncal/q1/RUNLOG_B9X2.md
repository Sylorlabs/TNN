# B9X2 RUNLOG — second B9 release-redesign search

**Crew:** NEC v3 B9 coordinator (subagent). **Date:** 2026-09-25 PDT.
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned;
SHA-256 prefix `498abcb5ab346f8cb246` matches the lab-pinned toolchain).
**Protocol:** `ADDENDUM_B9X2_2026-09-25.md` (committed `9118d6a1`, corrected `ae23cb5d`;
BOTH committed BEFORE any B9X2 input was generated or run).
**Parent rule:** `PREREG_NCAL_V3_FOLLOWUP_FROZEN.md` §1 Q1b/c; strict amendment rule:
O-rises cleared AND B13 not worsened AND no passing bar broken.

## Verification (pre-run)
- Driver `src/nec_q1.zag` rebuilt from the committed source with the pinned toolchain.
- Conversion check: variant 11 on `necc_input.tsv` → `sixcol_to_legs.py` reproduces
  committed `results_m11/` **37/37 byte-identical**.
- Full-bar scorer `q1/score_bars.py` verified against the round-1 RUNLOG table
  (all 16 mechs: redteam/O/TOTAL Gviol and B13 match; B6 min matches, e.g. DECORR 0.429).
- B13 counting note: the frozen bar is per (F,d) with n_rel ≥ 8. Re-scoring round-1
  legs under the exact frozen definition gives FIXED B13 = 13 (table said 15) and
  DECORR B13 = 5 (table said 7) — the round-1 table counted small-n cells
  (FIXED redteam d8/d16 n_rel=3; DECORR ceiling/O d32/d64 n_rel=1). Baseline m11 = 6
  under both countings. Historical verdicts unchanged under either counting
  (FIXED worsens B13 both ways; DECORR breaks B6 either way). This search gates on
  the frozen definition and reports both.

## Generation (deterministic Python, zero RNG; script committed)
- `q1/gen_b9x2.py` → `q1/inputs/b9x_strat.tsv`, `q1/inputs/b9x_grad.tsv`
  (5240 rows each; labels imputed per verified 1000/1000 constancy; frozen f1/f5 kept).
- STRAT counts per (battery,depth) == M4's counts exactly (verified); nested; d1 set == M4 d1 set.
- GRAD is a superset of M4 at every depth (verified); nested. Ceiling example:
  d8 85 (M4 70; keeps 15 of the 30 dropped), d16 60 (M4 50), d32 40 (M4 30), d64 20 (M4 10).

## Execution (all A/B/C byte-identical, SHA-256 logged)
- 2 designs × 3 runs = 6 driver runs (variant 11 = m11 confidence, unchanged).
  A/B/C SHAs identical per design
  (strat `8dbd7f43…`, grad `dc32c35a…`).
- `q1/results_b9x2/`: 222 leg files (2 mechs × 37 legs × 3 runs).
- `q1/sha256sums_b9x2.txt`: 230 entries (2 inputs + 6 sixcol + 222 legs).

## Variant outcomes (s1, A-run; frozen analyzer + full-bar scorer; B6 ref = m11)

| mech | design | O Gviol | redteam Gviol | TOTAL Gviol | B13 strict (unfilt) | B6 min | B1/B2 | B4/B5/B7 |
|------|--------|---------|---------------|-------------|---------------------|--------|-------|----------|
| 11 | m11 baseline | 2 | 1 | 3 | 6 (6) | 1.000 | 0 / 0,0 | .972/.874/.148 ✓ |
| 33 | B9X-FIXED (r1) | 0 | 0 | 0 | 13 (15) | 1.000 | ✓ | ✓ |
| 35 | B9X-DECORR (r1) | 0 | 1 | 2 | 5 (7) | **0.429** ✗ | ✓ | ✓ |
| 37 | B9X-STRAT | **3** | 0 | **5** | 6 (7) | **0.657** ✗ | 0 / 0,0 ✓ | .962/.863/.148 ✓ |
| 38 | B9X-GRAD | **3** | 1 | **4** | **15** (15) | 1.000 ✓ | 0 / 0,0 ✓ | .936/.852/.125 ✓ |

(B8 computed, reported, not gated — defective as frozen. B9 excluded by design.
B13 strict cells for 37: the same 6 ceiling/O cells as m11.)

## Measured O G-curves (ceiling/O)
- m11: d1 −0.414, d2 −0.439, d4 −0.449, d8 −0.430 (+0.019✗), d16 −0.425 (+0.005✗), d32 −0.433
- STRAT: d1 −0.414, d2 −0.434, d4 −0.452, d8 −0.453, d16 −0.450 (+0.004✗), d32 −0.449 (+0.001✗), d64 −0.446 (+0.003✗)
- GRAD: d1 −0.414, d2 −0.439, d4 −0.458, d8 −0.461, d16 −0.453 (+0.009✗), d32 −0.434 (+0.019✗), d64 −0.433 (+0.002✗)

## Key findings
- **STRAT kills the d4→d8 rise it was designed for** (d4→d8 is now a fall, −0.452→−0.453)
  and holds B13 strict at 6 (the only B9X besides DECORR-strict not to worsen it) —
  but the strict 1e-12 bar catches tiny residual rises deeper (d8→d16 +0.004,
  d16→d32 +0.001, d32→d64 +0.003): battery-level stratification does not hold the
  FAMILY-level mix constant as counts shrink, and it breaks B6 on ceiling/D (0.657)
  by reshuffling which correct items get released. Fails rule prongs (a) and (c).
- **GRAD refutes the abruptness hypothesis**: the rise is not caused by the suddenness
  of the cut — it FOLLOWS the drop wherever it happens. d4→d8 becomes a fall (−0.004,
  the kept low-conf items overshoot), then d8→d16 rises +0.009 when the kept items
  drop, and d16→d32 rises +0.019 (as large as the original) when the next kept batch
  drops. Keeping low-conf items longer also deepens underconfidence: B13 6→15
  (5 new ceiling/D cells + 3 new cost cells + deeper O cells). Fails prongs (a) and (b).
- **No B9X2 design meets (a)∧(b)∧(c).** The search now spans four designs
  {FIXED: freeze cohort; DECORR: break selection correlation; STRAT: hold composition
  constant; GRAD: phase the cut gradually} and the v1 §4 joint-constraint note is
  confirmed empirically: on ceiling/O, B3 and B13 pull in opposite directions —
  every release-side clearing of the rise either deepens underconfidence (FIXED,
  GRAD) or breaks recall/coverage (DECORR, STRAT).

## Commits
- Pre-run amendment: `9118d6a1`; pre-run correction: `ae23cb5d` (both before any run).
- (Inputs, legs, SHAs, scorer, RUNLOG, verdict updates, plain-language rewrite: this commit.)
