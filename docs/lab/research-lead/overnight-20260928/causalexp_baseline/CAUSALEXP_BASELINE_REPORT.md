# H-CAUSALEXP1 Simple-Baseline Comparison: Report

Date: 2026-09-30. Pure Zag. No Python at any stage.
Prereg frozen at `8367c007b` BEFORE implementation (byte-identical file,
md5 6a71eb042a27649120e7a2ae121d18d9; committed inside a concurrent
worker's commit, content untouched). No amendments.

## Verdict: H-CAUSALEXP1-WINS

No baseline beats or matches H-CAUSALEXP1. This is a baseline-comparison
verdict under the frozen K-BL-4 rule, not a promotion. H-CAUSALEXP1
remains BUILD-PASS, bounded L2, NOT SURVIVES.

## What was built

`cxbase.zag`: the three frozen baselines sharing all of H-CAUSALEXP1's
authored machinery (predict, sim_seq, intervention semantics, passive
phase, hypothesis store, elimination rule, planner). Only world_step
takes wid. The only difference from H-CAUSALEXP1 is the selection policy:

- BL-RANDOM: uniform random pick among the 42 candidates per round,
  deterministic LCG, frozen seeds 7, 42, 999, round cap 4.
- BL-FIXORDER: fixed script of length-1 actions 0..5 cycled, one per
  step, max 12 steps, stop when live==1.
- BL-MEM: lookup table keyed on the passive-log pattern, zero
  interventions, stored plan seq=[2].

## Bar-by-bar

**K-BL-1 (build/run): PASS.** Compiled with the frozen toolchain
(`znc 2026.07.0-dev`), exit code 0 on all runs, stderr 0 bytes.

**K-BL-2 (determinism): PASS.** 3 consecutive runs byte-identical,
md5 99a3d43339ff362457fd3f1b9c62dfcd.

**K-BL-3 (complete report): PASS.** SUMMARY lines for every
baseline x seed x world (true ids: W1->0 X2Y, W2->1 Y2X):

| baseline | seed | world | n_int | conv_id | correct | plan | plan_ok |
|---|---|---|---|---|---|---|---|
| H-CAUSALEXP1 (ref) | - | W1 | 1 | 0 | yes | [2] | OK |
| H-CAUSALEXP1 (ref) | - | W2 | 2 | 1 | yes | [4] | OK |
| BL-RANDOM | 7 | W1 | 4 | -1 (live=2) | no | SKIP | n/a |
| BL-RANDOM | 7 | W2 | 1 | 1 | yes | [4] | OK |
| BL-RANDOM | 42 | W1 | 2 | 0 | yes | [2] | OK |
| BL-RANDOM | 42 | W2 | 4 | -1 (live=3) | no | SKIP | n/a |
| BL-RANDOM | 999 | W1 | 4 | -1 (live=2) | no | SKIP | n/a |
| BL-RANDOM | 999 | W2 | 1 | 1 | yes | [4] | OK |
| BL-FIXORDER | 0 | W1 | 3 | 0 | yes | [2] | OK |
| BL-FIXORDER | 0 | W2 | 5 | 1 | yes | [4] | OK |
| BL-MEM | 0 | W1 | 0 | n/a | n/a | [2] | OK |
| BL-MEM | 0 | W2 | 0 | n/a | n/a | [2] | FAIL |

Trace notes (from raw output):
- BL-RANDOM seed 7, W1: first pick [1,4] (split=2) eliminates only Y2X;
  three following picks have split=1 and waste the round cap; ends
  live=2, NO-CONVERGE.
- BL-RANDOM seed 42, W2: four straight split=1 picks ([5,5], [3,0],
  [0,0], [0]); zero eliminations; ends live=3, NO-CONVERGE.
- BL-RANDOM seeds 7 and 999, W2: a single lucky length-2 pick
  ([1,4] / [2,5], split=2) eliminates both wrong hypotheses at once;
  converges in 1 intervention. Random selection can get lucky; it
  cannot be relied on (0/3 seeds converge in both worlds).
- BL-FIXORDER W1: [0] and [1] are split=1 no-ops at (1,1); [2]
  eliminates Y2X and NONE; converges in 3.
- BL-FIXORDER W2: [0], [1] no-ops; [2] eliminates X2Y; [3] no-op
  (Y2X and NONE agree at (1,1)); [4] splits Y2X vs NONE; converges
  in 5.
- BL-MEM: MEM-KEY hash -1295811391 in BOTH worlds (passive logs
  byte-identical). The single table entry returns plan [2] for both:
  W1 reaches (0,0) MEM-PLAN-OK; W2 reaches (0,1) MEM-PLAN-FAIL.

**K-BL-4 (verdict rule): H-CAUSALEXP1-WINS.**
- BASELINE-BEATS requires a baseline converging correctly in both
  worlds with total n_int < 3 and both plans OK, or BL-MEM OK in both
  worlds with zero interventions. BL-RANDOM: 0/3 seeds converge in
  both worlds. BL-FIXORDER: total 8. BL-MEM: fails W2. Not met.
- BASELINE-MATCHES requires both-worlds convergence with total
  n_int == 3 and both plans OK. BL-FIXORDER totals 8. Not met.
- Intervention efficiency: H-CAUSALEXP1 uses 3 total interventions;
  the naive fixed script needs 8 (2.67x); random selection fails to
  converge in both worlds on every tested seed.

**K-BL-5 (purity): PASS.** Grep audit: `wid==` appears only inside
`true_mask` (the oracle); `wid` elsewhere is a loop bound, a label, or
passed straight to `world_step`. No world-conditional learner logic.
Zero Python. Zero em dashes (byte-checked in source, prereg, raw
output, and this report).

## Interpretation

1. Max-split discriminating selection buys real, measured intervention
   efficiency: 3 interventions vs 8 for the fixed script. The fixed
   script wastes interventions on non-discriminating actions (idle and
   trigger at (1,1) have split 1); the adaptive loop never selects
   them.
2. Random selection is unreliable on this task: 3/6 world-seeds
   converge correctly, 0/3 seeds converge in both worlds within the
   4-round cap. It burns the intervention budget on split-1
   candidates and stalls with 2-3 hypotheses still live.
3. The memorization check is the sharpest result: because the passive
   logs are byte-identical across worlds, ANY lookup table from
   passive patterns alone must return the same plan in both worlds,
   and no single plan works in both ([2] fails W2, [4] would fail W1).
   The intervention loop is not just more efficient; it is necessary.
   This is direct evidence for the prereg's core claim that passive
   observation is provably insufficient here.

## Honest scope and limitations

- The baselines reuse all authored machinery; the comparison isolates
  the selection policy only. It does not test representational
  invention (H-CAUSALEXP1 is bounded L2 per the builder).
- The fixed script tested is the naive lexicographic one. A fixed
  script equal to the adaptive trace ([2] then [5]) would total 3 and
  match, but that script encodes the answer; it is not discoverable
  without running the adaptive learner first. This was not built as a
  baseline (not in the frozen prereg); noted as a limitation, not a
  post-hoc addition.
- Random selection was tested at 3 frozen seeds, not exhaustively.
- This verdict does not promote H-CAUSALEXP1. Steps 6-11 of the
  pipeline (alternative-explanation attack, OOD, ablation, transfer,
  red team, governance audit) remain.

## Governance disclosures

1. The prereg file was committed inside concurrent worker commit
   `8367c007b` (an arena amendment commit that swept the staged file).
   The committed bytes are identical to what I authored (md5
   6a71eb042a27649120e7a2ae121d18d9); no implementation, build, or
   run existed at that commit. Prereg-before-implementation ordering
   is intact.
2. Pure Zag throughout: implementation, builds, runs. Analysis used
   only shell tools (grep, awk, md5sum, cmp, od). Zero Python.
3. Build artifacts lived only in /tmp/cxbase; no binaries committed.
4. This is the baseline-comparison verdict under the frozen prereg,
   not canonical acceptance.

## Commits (tnn-native-lab, local only)

- `8367c007b` prereg frozen (content mine, byte-identical; see
  disclosure 1)
- (this commit) `cxbase.zag` + `CAUSALEXP_BASELINE_RAW.txt` +
  `CAUSALEXP_BASELINE_REPORT.md`, owned paths only

Raw: `CAUSALEXP_BASELINE_RAW.txt`
(md5 99a3d43339ff362457fd3f1b9c62dfcd).
