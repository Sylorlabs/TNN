# VERDICT — D1 Defense-Stack Battery (G1 + MG6 + H6)

**Date:** 2026-09-24. **Prereg:** `2b3a485fca5a1ce0953f8db243f976f398cd1cd9`.
**Verdict: KILL** (frozen KB-D1b).

## What was tested

The surviving defense stack **G1 (gate) → MG6 (guard) → H6 (hardening)**,
composed per the frozen prereg. F5 was excluded by its 300-percept kill
verdict — a killed mechanism is not composed. Four legs, 758 trials,
pure Zag, zero RNG, three byte-identical runs
(`d38b3d8a…eb2a6bf` ×3), 758/758 match hand-verified EXPECT.

## Kill-bar results

- **KB-D1a (ANY false install → KILL): PASS.** 0 false installs across all
  758 trials. The stack refuses every wrong candidate:
  - Leg 1: all 9 false accepts refused (3 guard-vetoed, 6 gate-withheld).
  - Leg 2: all 12 sustained TMB-5 wrongs refused (gate never forms proposals).
  - Leg 3: CC1's wrong correlated pair vetoed (margin+span+temporal).
  - Leg 4: 0 installs on all four streams (incl. 8 spoofed decoys, R2).

- **KB-D1b (true retention <26/34 → KILL): FAIL → KILL.** 0/34 true
  candidates install. The 4 true install proposals are all vetoed by MG6's
  temporal arm (`|Δseq|` 1, 3, 5, 2 — all < 20). On the 43-candidate
  geometry, true corroborators are as temporally clustered as wrong ones;
  the guard's temporal arm cannot distinguish them. G1's sequential
  re-anchoring misses the remaining true pairs. The conjunction withholds
  too much truth: 0/34 vs the 26/34 bar.

## Honest report on the 8 TMB-5 false accepts (no F5)

F5 used to block 8/9 false accepts. Without it, G1+MG6 handles the 8 TMB-5:
3 vetoed at the install-proposal point (temporal arm), 5 refused earlier
by the gate (never form corroborated proposals). The defense holds — but
only because the guard is so aggressive it also vetoes every true
corroboration. The stack is safe but useless on this geometry: it installs
nothing true.

## What this means

1. **The R3-4 conjunction hypothesis is dead.** F5's kill removed the only
   layer that blocked wrong installs at low true-cost (0/34 over-block).
   The surviving G1+MG6+H6 stack passes the safety bar (KB-D1a) but fails
   the cost bar (KB-D1b) catastrophically (0/34, not a near-miss).
2. **MG6's temporal arm is miscalibrated for stream geometry.** Its
   verified setting (`|Δseq| ≥ 20`) was tuned on cell geometry where wrong
   pairs were clustered and correct pairs were separated. On real stream
   replays, correct corroborators cluster too. The arm needs re-tuning
   against stream geometry, or a different independence signal.
3. **H6's R4 margin (≥100) is stricter than G1+MG6 alone.** It would have
   withheld C1's correct revision (mrg 77) had the guard allowed it —
   defense in depth, but more throughput cost. (In the event, the guard
   vetoed first on span+temporal.)
4. **Per the frozen bar, layers must be re-tuned separately.** The
   guard's arms need recalibration on stream-temporal geometry before any
   recomposition. The gate's re-anchoring also deserves review (it missed
   true pairs with `|Δseq| ≥ 20`).

## Limits (from the frozen prereg, not post-hoc)

- `mrgF := measure` and phash-derived spans on stream trials are
  substitutions; the guard's margin arm is calibrated on cell geometry.
- The 43-candidate `prog = PASS` replay is the frozen modeling choice.
- Cell gatt tags generated with the frozen key.
- MG6's V9 ceiling inherited: a wrong pair strong on all three guard-visible
  axes still defeats it. Cross-task interference untested.

## Artifacts

`gen_d1.py`, `stack_main.zag`, `stack_records.zag` (generated),
`R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag`,
`EXPECT_D1.tsv`, `EXPECT_D1_CELL.tsv`, `gatt_leg3_*.txt`,
`score_d1.py`, `evidence/run{1,2,3}/`, `evidence/score.txt`,
`RUNLOG_D1_STACK.md`, this verdict.
