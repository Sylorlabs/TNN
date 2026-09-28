# Run-1 Re-score with Rule (v) — RESULTS ADDENDUM

**Date:** 2026-09-24. **Crew:** H2 run-2 FIXTURES/SCORER.
**Authority:** `PREREG_H2_RUN2.md` §7 (stable-decoy scoring amendment), commit
order step 2. Scorer certified by D8 (`job2_scorer/d8_certify.py` — 7/7
hand-checked fixtures, byte-identical 2×).

## Method

1. Regenerated the 20 run-1 cells' MAIN arms deterministically from the frozen
   run-1 artifacts (`battery.py` + `build.py` + `teacher.zag` + `orig/`
   learners, all unmodified). KB-DET held: rep1 vs rep2 byte-identical on all
   20 cells, and the regenerated genomes/verdicts reproduce the run-1
   RESULTS.md traces (A1's r2 sham-find, f3×A4's r3/r5/r6 actfault kills).
2. Fed every round's (genome, seal table from the audit export, facts) into
   the D8-certified scorer (`scorer.zag`, pure Zag). Run-1 genomes carry no
   declared-target field → `target=−1`; static audit of the frozen
   `teacher.zag` confirms `teach_lie ∈ {0,1}` at every emission site, so the
   DE shape (teach_lie=−1 on a*) cannot occur in run-1.
3. Applied per-round (v) and the DECOY-KILL rule: decoy-kill iff a variant's
   phase-2 (v)-loss count exceeds T-DEF's on the same teacher.

## Per-round (v) table

(v)=0 on all 120 phase-1/2 rounds (20 cells × 6 rounds). chase/sham diagnostics
varied by round (learners chased/uninstalled in the usual (i–iv) shapes) but
(v) never fired: no round had a declared target with a mismatched seal.

## Verdict comparison

| Cell | Baseline | Phase-2 (v) | T-DEF phase-2 (v) | Decoy-kill | New verdict |
|---|---|---|---|---|---|
| default×A1..A4 | SURVIVE ×4 | 0 | 0 | no | SURVIVE ×4 |
| a2×A1..A4 | SURVIVE ×4 | 0 | 0 | no | SURVIVE ×4 |
| a3×A1..A4 | SURVIVE ×4 | 0 | 0 | no | SURVIVE ×4 |
| b1×A1..A4 | SURVIVE ×4 | 0 | 0 | no | SURVIVE ×4 |
| f3×A1 | SURVIVE | 0 | 0 | no | SURVIVE |
| f3×A2 | SURVIVE | 0 | 0 | no | SURVIVE |
| f3×A3 | SURVIVE | 0 | 0 | no | SURVIVE |
| f3×A4 | **KILL** | 0 | 0 | no | **KILL** |

## Headline

**NO VERDICT FLIPS.** 19/20 SURVIVE + 1 KILL (f3×A4) stands under rule (v).
This is the outcome the prereg predicted: A1's run-1 fitness F had no target
term, so the DE genome was never found and the re-score records (v)=0
everywhere. The amendment's re-score baseline is therefore non-vacuous going
forward only via run-2's F2 (which adds the target term — `f2_fitness.zag`).

Raw per-round data: `job2_scorer/rescore_out/rescore.json`.
