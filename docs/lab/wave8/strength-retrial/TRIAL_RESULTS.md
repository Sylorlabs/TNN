# Wave-8 Strength Re-Trial: Results

> **Dated note (2026-09-20):** the line "**None advance to S10**" below misread the prereg's advancement rule (killed arms do not advance; survivors do — PREREG_STRENGTH_V2.md §15, wave-4 PREREG §6). Arm B survived S1 and **did** run S10/S100. See `TRIAL_RESULTS_SCALE_LEGS.md` for the correction and the scale-leg results. The S1 numbers below are unchanged.

**Prereg:** `PREREG_STRENGTH_V2.md` | **Scale:** S1 only (32 slots, 500 episodes) | **Date:** 2026-09-20

## Verdict by Arm

**B (uniform):** SURVIVES as control. Drops=0, VUP retention 19% (29/150), WBS R=100% (40/40, lat 25), JI I_rej=100% (6/6), junk 0.3%. Not promoted (baseline).

**C (hybrid):** KILLED at S1. P2 drop ceiling: drops=470 in all 3 VUP variants (>64). VUP 100% (9/9) but only 9 important admitted; JI junk retention 100% (21/21) vs 5% bar.

**C-P3 (hybrid+expiry):** KILLED at S1. Identical to C: drops=470, VUP 100% (9/9), JI junk 100%. P3 expiry had zero measurable effect.

**None advance to S10.** No champion; no-free-lunch holds (no config beats B in ≥2 curricula).

## P1/P2/P3 Agreement

All three agree C/C-P3 are frozen:

- **P1 (freeze distinguisher):** C/C-P3 show EC=1.0, PTR=1/1 — but only 1 designated memory was alive during pressure (others never admitted). The metric is technically satisfied but vacuous; the freeze prevented meaningful evaluation.
- **P2 (drop ceiling):** Decisive. Drops=470 (C) and 470 (C-P3) vs ceiling 64. The tripwire fired in 3/3 variants for both.
- **P3 (expiry rule):** Expiries were issued (maintenance ran), but no expiry enabled a kill. The BASELINE cost (≥1 cite) still requires evidence the learner cannot produce in VUP/JI. P3 did not fix the freeze.

**Clash:** None. P1, P2, P3 converge: graded protection without a citation source freezes the store.

## No-Free-Lunch Verdict

B wins by survival. On primary metrics: VUP — C beats B (100% vs 19%) but on a 9 vs 150 denominator; WBS — tie at 100% but B has larger cohort (40 vs 36) and 3× better latency (25 vs 75); JI — B crushes C (0.3% vs 100% junk). No graded config beats uniform in ≥2 curricula. The hybrid's VUP "win" is an artifact of admitting almost nothing.

## Kill Criteria Applied

- **P2 drop ceiling:** C FAILED 3/3, C-P3 FAILED 3/3 → both killed as main-line candidates.
- **VUP retention (symmetric):** B is 80pp below C/C-P3, but B is exempt as control per prereg.
- **WBS rigidity:** All achieve R_wbs=100%. Latency 75 vs B's 25 = 3.0× (kill requires >3×) → survive, barely.
- **JI bars:** C/C-P3 fail junk retention (100% > 5%).

## Integrity / Determinism

- GATE: 3/3 arms pass (including C-P3 P3 probes: expiry, BASELINE kill, refresh).
- Static checks: no RNG, no direct strength writes outside core, frozen formulas verbatim, bare @imports.
- Exact replay: all 27 cells (3 arms × 3 curricula × 3 variants) run twice, byte-identical stdout.
- Independent checker: 0 failures across all cells (replay, refusals, lineage, kill-effort, P3 no-permanent-lock).

## Honest Limits

1. **S1 only.** S10/S100 not run; all candidates killed at S1. Scale behavior unproven.
2. **VUP metric misleading.** Held/admitted favors C (9/9) over B (29/150); B retains 3× more important memories absolutely.
3. **P3 needs learner change.** Expiry alone cannot work — the learner policy (unchanged per prereg) provides no evidence-against in VUP/JI. A P3 fix requires citing revelation-of-non-importance, which the prereg forbids.
4. **B's PTR unevaluated.** B's EC=0.2–0.3 (<0.5), so its pressure-test retention was not meaningfully measured.
5. **C-P3 = C.** The trial tested P3 and found no effect. This is a real result, not a bug: the mechanism as specified does not address the citation gap.
