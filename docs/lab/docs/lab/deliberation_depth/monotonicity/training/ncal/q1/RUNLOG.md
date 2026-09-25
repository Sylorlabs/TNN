# Q1 RUNLOG

**Crew:** NEC v3 Q1 (subagent). **Date:** 2026-09-24/25 PDT.
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).
**Base commit:** `3edb49e87b91` (V3 follow-up). Pre-run addendum: `b50f1f1a` (committed BEFORE any variant ran).

## Verification (pre-run)
- `PREREG_NCAL_V3_FOLLOWUP_FROZEN.md` @ `3edb49e8`: MATCH (byte-compare).
- `PREREG_NCAL_V1_FROZEN.md` @ `c96e3378`: MATCH.
- `ADDENDUM_V2_m11.md` @ `9388f247`: MATCH.
- `necc_input.tsv`, `src/nec_v2.zag`, `training/analyze.py` @ `3edb49e8`: MATCH.
- SHA-256: input `714df05f…`, nec_v2 `85b91ac4…`, analyze `e013f435…`.

## Pre-run data findings (frozen m11 A-results, frozen analyzer)
- Redteam G: d1 +0.313, d2 −0.020, d4 −0.025, d8 +0.000, d16 +0.000.
  Measured d4→d8 residual: **+0.025** (1 B3 violation), NOT +0.522 (stale v1 figure; struck).
- Ceiling/O G: d1 −0.414, d2 −0.439, d4 −0.449, d8 −0.430 (+0.019), d16 −0.425 (+0.005), d32 −0.433. 2 B3 violations.
- Label constancy: 1000/1000 items label-constant across depths; 0 never-released. (Imputation basis for B9X.)
- M4 release nested: released(d+1) ⊆ released(d) for all 7 batteries (verified).
- O/d8 selection: M4 drops the f5=142 subgroup (10 items, d4 mean conf 470) while keeping f5∈{76,47,24} (d4 mean 566); survivor-mean shift +24/1000 matches the +0.019 rise.

## Build
- `src/nec_q1.zag`: unified parameterized driver (variant ids 11–20, 31, 32).
  Compiled with pinned znc. Variant 11 reproduces `nec_v2` **byte-identically** on `necc_input.tsv`.
- `q1/inputs/b9x_{fixed,topcut,decorr,inv}.tsv`: deterministic Python generation (labels imputed per verified constancy).
- `q1/inputs/cv_empty.tsv`: synthetic 2-item probe (empty class + p0=1.0).

## Execution (all A/B/C byte-identical, SHA-256 logged)
- 16 mechs × 3 runs = 48 driver runs. All A/B/C triples byte-identical.
- 6-col → 11-col conversion verified: variant-11 output reproduces committed `results_m11/` (37/37 byte-identical).
- `q1/results_q1/`: 1776 leg files (16 mechs × 37 legs × 3 runs).
- `q1/sha256sums.txt`: 1824 entries (48 sixcol + 1776 legs).
- Frozen `training/analyze.py` (unmodified) scored all mechs; output in `q1/analysis_all.txt`.

## Variant outcomes (s1, A-run; frozen analyzer)
| mech | variant | redteam Gviol | O Gviol | TOTAL Gviol | B13v | notes |
|------|---------|---------------|---------|-------------|------|-------|
| 11 | m11 reproduce | 1 | 2 | 3 | 6 | baseline; matches frozen |
| 12 | personal outright | 2 | 3 | 5 | 6 | worse |
| 13 | outright, no ceiling | 0 | 1 | 5 | 1 | redteam cleared BUT O d1→d2 +0.414 rise; not viable |
| 14 | optimistic max | 2 | 3 | 7 | 6 | much worse (redteam +0.500) |
| 15 | p0=1.0 | 0 | 2 | 2 | 6 | **redteam CLEARED**; B3 3→2; B13 held |
| 16 | finer bins | 1 | 2 | 3 | 6 | no improvement |
| 17 | no ceiling | 1 | 2 | 15 | 6 | ceiling load-bearing for G-flatness |
| 18 | K=8 | 1 | 2 | 3 | 6 | no improvement |
| 19 | global class | 2 | 0 | 2 | 18 | O cleared BUT B13 wrecked |
| 20 | personal-only | 2 | 0 | 2 | 0 | **O cleared**; B13 6→0; redteam 1→2 |
| 31 | ORACLE-d1 | 1 | 2 | 3 | 6 | does NOT clear redteam (predicted) |
| 32 | ORACLE-full | 0 | 0 | 0 | 0 | clears all (GT upper bound) |
| 33 | B9X-FIXED | 0 | 0 | 0 | 15 | clears all BUT B13 6→15 |
| 34 | B9X-TOPCUT | 1 | 3 | 8 | 6 | worse |
| 35 | B9X-DECORR | 1 | 0 | 2 | 7 | O cleared; B6 broken (0.429); B13 6→7 |
| 36 | B9X-INV | 1 | 0 | 1 | 3 | degenerate (d8+ n/a); B6 broken |

## CV-EMPTY probe
- p0=1.0 + empty/all-correct class: M3 d1=1000 → d4=1000 → G4=0, G8=0. **Step cleared.**
- p0=0.95 contrast: M3 d1=950 → d4=950 → G4=−0.025 → violation.
- Proves the "d1 conf exactly 1.0" premise is load-bearing (counterfactual).

## Key refutations
- **m15 (p0=1.0, in-class, §6-compliant) clears the redteam d4→d8 step** (Gviol 1→0). The v1 "proven" impossibility claim is FALSE. The proof's load-bearing premise was p0<1 ("d1<1.0"); m15 violates it within §6.
- **m20 (personal-only, in-class) clears the O-rises** (Gviol 2→0) AND improves B13 (6→0). Not a knowledge problem.
- **B9X-FIXED (33) clears all G-violations** (3→0) but worsens B13 (6→15). Selection account confirmed mechanistically; strict bar-holding not met.

## Commits
- Pre-run addendum: `b50f1f1acbdafcb7c94eeaacb3778f448d183a49`.
- (Driver, inputs, results, RUNLOG, VERDICT commits to follow.)
