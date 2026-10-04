# SEALED_EVAL_PART2.md - F1-FOLLOWUP Part 2 characterization results

Lane F1-FOLLOWUP, wave wave-20261001-2321pdt. Sealed runs executed
2026-10-02 ~00:05 PDT against the frozen F1 binary
`../F1/impl/f1_learn` (sha256
6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847,
verified before running; match confirmed). 24 fresh sealed sum2
worlds (frozen 5100-series seeds, manifest sealed2/FIXTURE_SHA256.txt,
all hashes verified before runs). Characterization prereg:
PREREG_PART2.md (committed alone at 6dee24671 before any Part 2
fixture was generated; fixture manifest committed at 63922a500
before any Part 2 sealed run; no implementation work exists in this
lane; the constructor is used read-only).

No em-dashes are used in this document.

## 1. Determinism evidence

Each of the 48 sealed invocations (24 seeds x train/hidden) was
executed 3 times (runs2/1, runs2/2, runs2/3). All corresponding
outputs are byte-identical across the three repetitions
(cmp-verified, zero diffs). SHA-256 of all runs2/1 outputs is
recorded in runs2/DETERMINISM_SHA256.txt. The N>=20 finding bar with
3/3 determinism per seed is met (24/24).

## 2. Overfit rate (frozen classification)

OVERFIT = hidden accuracy below 80 percent (f1_score acc on the
30-probe masked set, frozen pure-Zag scorer). CORRECT = at least 80
percent. The split is cleanly bimodal; no seed is near the boundary.

| seed | hidden | class |
|---|---|---|
| 2 | 5/30 = 16% | OVERFIT |
| 3 | 0/30 = 0% | OVERFIT |
| 5 | 2/30 = 6% | OVERFIT |
| 13 | 0/30 = 0% | OVERFIT |
| 17 | 1/30 = 3% | OVERFIT |
| 18 | 0/30 = 0% | OVERFIT |
| 0,1,4,6,7,8,9,10,11,12,14,15,16,19,20,21,22,23 | 30/30 = 100% | CORRECT |

Overfit rate: 6/24 = 25 percent. Every overfit seed's hidden accuracy
is catastrophic (0 to 16 percent), matching the F1 sealed rW2
overfit (0/30) and the dev sum3 overfit (0/30).

## 3. Frozen separation analysis (pure-Zag cw2_sep)

Best single-threshold separation per fixture property (misc =
total misclassified seeds; bar for an identified pattern: misc <= 2;
cells = ovf_ge/cor_ge/ovf_lt/cor_lt):

| feature | best ge | misc | best le | misc |
|---|---|---|---|---|
| F1 distinct pairs | k=19 | 7 | k=13 | 5 |
| F2 duplicates | k=12 | 5 | k=5 | 6 |
| F3 x0==x1 | k=8 | 7 | k=2 | 5 |
| F4 y==0 | k=2 | 6 | k=0 | 6 |
| F5 distinct y | k=9 | 8 | k=6 | 5 |
| F6 zero-input | k=12 | 8 | k=6 | 4 |

Full contingency output is in the analysis record (dev/cw2_sep run on
the frozen results table). No fixture property separates OVERFIT from
CORRECT with at most 2 misclassifications. The best is F6 (predict
OVERFIT when zero-input episodes <= 6) with misc = 4, which does not
meet the frozen bar.

## 4. Verdict: NOT-FOUND (per the frozen decision rule)

No pre-registered fixture property (F1..F6) meets PREREG_PART2 section
5(c) (separation with at most 2 misclassified seeds on the frozen
24-seed set). The verdict is therefore NOT-FOUND, with all hypothesis
tables reported above. The overfit rate 6/24 stands as the
characterized finding. No L3 claim follows; this is a constructor
limitation, not a capability.

Consistency check (post-hoc, not part of the decision rule): F1's
sealed rW2 overfit fixture (seed 2301) has F1=15, F2=9, F3=0, F4=0,
F5=7, F6=9. It does not share any cleanly separating property with
the 6 overfit seeds found here, consistent with NOT-FOUND.

## 5. Mechanistic explanation (post-hoc, explanatory only)

The following is explanatory analysis from the frozen F7/F8/F9
behavior properties and trace inspection. It is NOT the identified
pattern under the frozen rule and must not be reported as one; it is
a candidate hypothesis for a future prereg.

Final structures of the 6 overfit seeds (main-graph op/operand
signatures):

| seed | final structure | hidden |
|---|---|---|
| 2 | 2x0 +x0 +x1 = 3x0+x1 | 5/30 |
| 3 | 2x0 +x0 +x1 +x1 = 3x0+2x1 | 0/30 |
| 5 | 2x0, r0+r0=4x0, +x1 = 4x0+x1 | 2/30 |
| 13 | 2x1 +x1 +x0 +x0 = 3x1+2x0 | 0/30 |
| 17 | 2x1, r0+r0=4x1, +x0 = 4x1+x0 | 1/30 |
| 18 | 2x1 +x1 +x0 +x0 = 3x1+2x0 | 0/30 |

Correct seeds converge to 2x0+2x1 or 2x1+2x0 (e.g. seed 1:
2x0 +x1 +x1, 30/30; seed 9: 2x1 +x0 +x0, 30/30).

The mechanism is visible in the traces: the first construct always
doubles one feature (ADD r0,fi,fi, the largest single-step buffer
error reduction). The correct continuation is to add the OTHER
feature twice. In all 6 overfit seeds the greedy second step adds
the SAME feature again (or doubles the accumulator r0), compounding
the initial choice; the strictly-improving depth-1 argmin then locks
into a degenerate composition that fits the trial buffer but not the
hidden set. The trigger fires at episode 1 on all 6 overfit seeds
(and on 22 of 24 seeds overall), so the greedy path is decided by the
x0/x1 balance of the first 1 to 2 train episodes, the buffer present
at first trigger. Whole-fixture features F1..F6 average over all 24
train episodes and therefore cannot see the property that decides
the path: the x0-vs-x1 error-mass imbalance inside the first-trigger
buffer. That property was not in the frozen feature set, so it
cannot be claimed as the identified pattern here; it is the natural
next prereg (features computed over the trigger-time buffer, frozen
before runs).

Evidence paths (all under
docs/lab/rsi/runs/wave-20261001-2321pdt/F1-FOLLOWUP/):
- PREREG_PART2.md (frozen finding-characterization bars)
- sealed2/ (24 fresh fixtures, gen2.sh, run_sealed2.sh,
  FIXTURE_SHA256.txt)
- runs2/ (1, 2, 3 repetitions; DETERMINISM_SHA256.txt)
- dev/cw2_analyze.zag, dev/cw2_sep.zag (pure-Zag frozen analysis)
