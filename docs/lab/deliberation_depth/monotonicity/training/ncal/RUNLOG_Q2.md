# RUNLOG — NCAL Q2 crew (gaming vs calibrating)

- **Date:** 2026-09-25
- **Crew:** Q2 (subagent session 3cf09d5d)
- **Protocol:** `PREREG_NCAL_V3_FOLLOWUP_FROZEN.md` §2, `ADDENDUM_Q2_TRAPS_2026-09-25.md`
  (committed BEFORE any trap run: `6f58e2d9`), `ADDENDUM_Q2_T2_SUPP_2026-09-25.md`
  (`3d5ca58f`, committed before the supplementary analysis)
- **Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)

## Verification (pre-run)

1. Branch `tnn-native-lab` HEAD at start: `3edb49e87b91` (= frozen amendment
   commit); moved to `f64876d640` (unrelated RSI-8 commits) then `c921d274b0`
   before our commits. Frozen amendment file verified unchanged (blob
   `238e5266`, content-sha256 `48cafacc83450cf6…`) at every commit base.
2. `src/nec_v2.zag` (m11) compiled clean; output on `necc_input.tsv`
   differs from committed `necc_out_A2.tsv` (SHA `10b7a1f7…`) from line 1506 —
   expected: that file is m9's (v0) output.
3. `src/nec.zag` (m9) output on `necc_input.tsv` byte-identical to committed
   `necc_out_A2.tsv` (SHA `10b7a1f7ffac3006666943de074e306e899dd91e0d44be6613255e69f7cd471e`).
4. m11 output → analyzer 11-col legs byte-identical to committed
   `results_m11/` on 4/4 spot-checked legs
   (admit_d1, ceiling_d8, redteam_d1, trap_d2).
5. Frozen `training/analyze.py` (blob `fb5e0d5e`) on regenerated m11 legs:
   B3=3 (ceiling/O:2, redteam:1), V1=V2=0 — reproduces frozen numbers exactly.

## Trap battery generation (deterministic Python; frozen by addendum)

- `gen_traps.py` → `trap_t1.tsv` (150 rows; class (5,3) f1=825,f5=875;
  C:12 all-correct, T:12 wrong@d1, W:6 wrong@d1d2; depths 1,2,4,8,16),
  `trap_t3.tsv` (200 rows; 5 empty-matrix classes × 40 items, d1 only,
  true rates 1.00/0.75/0.50/0.25/0.00), `trap_t3_truth.tsv`.

## Variant sources (auditable patches from frozen `nec_v2.zag`)

- `gen_variants.py` (exact-match anchors, asserts single occurrence):
  `q2_m11.zag` (byte-identical copy, verified by cmp),
  `q2_floor.zag` (symmetric-continuity floor for perfect personal records),
  `q2_u1.zag` (−50 reporting shift), `q2_u2.zag` (−150 reporting shift),
  `q2_g.zag` (gaming control: cap binds only on currently-wrong cells),
  `q2_eb.zag` (self-estimated prior), `q2_ind.zag` (p0=0.5).
- All 7 compiled clean with the pinned toolchain (no warnings besides the
  zagd-unavailable notice).

## Runs (`run_all.sh`)

- 7 variants × {trap_t1, trap_t3, necc_input} × {A,B,C} = 63 runs, plus
  m9 × necc_input × {A,B,C} = 3, plus m9 × trap_t1 (T2-SUPP counterfactual).
- 66/66 in SHA_LOG.tsv; A/B/C byte-identical within all 22 variant×battery
  groups (0 non-deterministic).

## Analysis scripts (all committed)

- `sim_m11.py` — Python sim of m11's stated rule; byte-exact vs the Zag
  binary on all three batteries (cmp clean ×3).
- `sim_variants.py` — sims recording per-cell CAP binding; byte-exact for
  m11 and m_g on trap_t1.
- `analyze_t1.py` (M1 crater / M2 sparing / M3 B13 cost),
  `analyze_t2b.py` (matrix S1/S2, analyzer families),
  `analyze_t2supp.py` + cap-level check (T2-SUPP),
  `analyze_t3.py` (held-out calibration), `bars.py` (B1/B2/B3/B4/B5/B13),
  `to_analyzer.py` (6-col → 11-col legs).

## Key measured results (full tables in VERDICT_Q2.md)

- T1: m11 crater +0.513 (C@2=0.513, T@2=0.000), sparing +0 → principle
  followed at cost of 4 B13 violations on the trap family. m_g: crater
  −0.097, sparing +645 → probe catches the known gamer.
- T2 matrix: bind ⟺ deficit>0 exactly (bind rates 0/0/1/1 across
  deficit×would_rise); would_rise β=+0.000, p=1.0. T2-SUPP cap-level:
  m11 binds 66/66 correct + 6/6 wrong deficit cells; m_g 0/66 + 6/6.
- T3: m11 |err|=0.092 bias=+0.089 PASS; u2 bias=−0.051 FAIL (bar-ward);
  ind best |err|=0.055.
- T4 bars: m11 B3=3/B13=6; eb B3=4/B13=6; ind B3=3/B13=11. Neither
  principled prior reproduces m11's profile → p0=0.95 is bar-knowledge
  smuggled as a constant (per preregistered rule).
- Channel audit: only f1/f5 read; corr (GT) used solely in post-conf ledger
  updates (source lines 181/190/198) and output passthrough; f2–f4,f6–f8
  unread; analyzer/thresholds/family/depth never input.

## Commits (tnn-native-lab, force:false)

1. `6f58e2d9` — ADDENDUM_Q2_TRAPS_2026-09-25.md (pre-run, before any trap run)
2. `3d5ca58f` — ADDENDUM_Q2_T2_SUPP_2026-09-25.md (pre-run supplement)
3. (this commit) — trap batteries, variant sources, results, SHA log, RUNLOG
4. (next) — VERDICT_Q2.md
