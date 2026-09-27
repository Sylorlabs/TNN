# Experiment 2: Evidence

## 1. Holdout per-problem results (confirmatory)

`results/holdout_onebrain.tsv` (one-brain), `results/holdout_baseline.tsv`
(baseline), `results/holdout_ablation.tsv` (ablation). All 10 forked under
one-brain; baseline never forks (no fan-out); ablation forks with private
ledgers. Columns: id, forked, verdict, expected, correct, margin, rounds,
consumed, t_consume, t_elim, ledger_head.

| ID | Expected | One-brain | Baseline | Ablation (bv0/bv1/bv2) |
|----|----------|-----------|----------|------------------------|
| HO-01 | R1 | R1 correct | R2 wrong | R2 wrong (R2/R1/R2) |
| HO-02 | R2 | R2 correct | R1 wrong | R1 wrong (R1/R2/R1) |
| HO-03 | R1 | R1 correct | R2 wrong | R2 wrong (R2/R1/R2) |
| HO-04 | R2 | R2 correct | R1 wrong | R1 wrong (R1/R2/R1) |
| HO-05 | R1 | R1 correct | R2 wrong | R2 wrong (R2/R1/R2) |
| HO-06 | R2 | R2 correct | R1 wrong | R1 wrong (R1/R2/R1) |
| HO-07 | R1 | R1 correct | R2 wrong | R2 wrong (R2/R1/R2) |
| HO-08 | R2 | R2 correct | R1 wrong | R1 wrong (R1/R2/R1) |
| HO-09 | R1 | R1 correct | R2 wrong | R2 wrong (R2/R1/R2) |
| HO-10 | R2 | R2 correct | R1 wrong | R1 wrong (R1/R2/R1) |

One-brain ledger stats per verdict: 7 shared consumes, 1 elimination,
3 rounds, final margin 730. Baseline: 6 consumes, 0 eliminations, final
margin 1000 (it eliminates the correct reading early at the 400 margin,
then the decisive attack only weakens the survivor). Ablation branch
verdicts: branch 0 (payload-order confirmer, the designated single
verdict) is wrong on all 10; branch 1 (attack lens) is right on all 10;
branch 2 agrees with branch 0. The ablation's designated verdict is
0/10, so the gain is not explained by extra passes alone.

## 2. K2 poison test (causal cross-talk)

Full log: `results/poison_test.log`. Driver: `ob_poison.zag` (pure Zag).
Problems: OB-01, OB-07 (developmental set; the test exercises machinery,
not battery accuracy).

OB-01 reference (shared): verdict R2, b0=[e3,e5], b1=[e6,e7], b2=[e4].
Poison: invalidate shared e6 pre-fanout (the evidence branch 1 took first
in the reference run). Result: verdict flips R2->R1; every branch's
consumption changes (b0=[e3,e7], b1=[e4], b2=[e5]); eliminations change.
Hypothesis poison (eliminate R2 pre-fanout): verdict flips R2->R1,
elimination count 1->0. Control (ablation, poison applied to branch 0's
private copy only): branch 1 and branch 2 traces byte-identical to the
unpoisoned ablation run. OB-07 shows the same pattern (verdict R2->R1 on
evidence poison, R2->R3 on hypothesis poison; control isolated).

Verdict: a shared-ledger write changes other branches' bids, consumptions,
and the joint eliminations within the same deliberation (PASS), while
poisoning one independent ledger changes nothing else (PASS).

## 3. K3 scaffold-removal test

Full log: `results/scaffold_test.log`. Driver: `ob_scaffold.zag`, the
minimal loop: parse each line, call ob_deliberate, print forked/verdict.
Source audit: zero occurrences of `fan_out`; the six "fork" mentions are
comments, the output label, and the struct field read for printing. No
fork threshold, no branch logic, no selection logic in the driver.

Result: 10/10 holdout problems fork under the minimal driver; fork flags
and verdicts are identical to the full `ob_run` driver (empty diffs in
the log). The fork decision (probe 2 evidence, fork iff >=2 readings
survive, evidence remains, margin < 350) fires inside the machinery from
ledger state. Not crew scaffolding (PASS).

## 4. K4 delete/reorder test (decorative sharing?)

Full log: `results/delete_reorder_test.log`. Driver: `ob_delreord.zag`
(pure Zag). Problems: OB-01, OB-07, OB-14.

- Delete (remove 3rd evidence item) changed the shared fan-out trace
  (ledger head hash) on 3/3 problems: PASS.
- Reorder (reverse evidence order) changed the shared fan-out trace on
  3/3 problems: PASS.
- Verdict distribution: shared {R2,R2,R2} vs branch-0 {R1,R1,R1},
  branch-1 {R2,R3,R2}, branch-2 {R1,R1,R2}. The fan-out distribution
  differs from every independent branch run: PASS.
- Caveat: on OB-01 and OB-14 the attack-lens branch independently reached
  the shared verdict (R2), so per-problem verdict-level non-reproducibility
  holds only on OB-07. Trace-level evidence is stronger: in the K2 log,
  branch 1's shared consumption [e6,e7] differs from its private
  consumption [e6,e3,e4], i.e. branches read each other's writes.

## 5. K5 determinism

Full manifest: `results/determinism_manifest.txt`. Three full runs of
each arm on the holdout (results TSV plus ledger JSONL): all six files
byte-identical across runs (each SHA-256 appears exactly 3 times).
Canonical result files equal run 1 (verified with cmp).

## 6. K6 RNG audit

`grep -rni "rand\|rng\|srand\|random" --include="*.zag"`: the single match
is a comment ("Zero RNG, no threads, byte-identical reruns"). No RNG in
any decision path. Interleaving is fixed round-robin; all choices are
argmax/first-valid-index. PASS.

## 7. Example shared-ledger trace (HO-01)

Probe consumes e1 (R2:+300), e2 (R1:+280): margin 20 < 350, fork fires.
Round 1: b0 confirms payload order (e3, R2:+600 -> R2=900); b1 attacks the
leader (e6, R2:-650 -> R2=250); b2 supports the runner-up (e5, R1:+300 ->
R1=580). Joint reconciliation: leader R2 cross-examined (attack 650 meets
the 650 refutation threshold) and eliminated; R1 survives as the sole
reading. Round 2: b0 takes e4 (R2 dead, no-op), b1 takes e7 (R1:+150).
Final ARGMAX: R1, margin 730. The baseline, by contrast, consumed e3 in
payload order, eliminated R1 at the 400 margin before ever seeing e6, and
answered R2.

## 8. What was NOT measured

Wall-clock parallelism (the claim is cross-talk, never speed); problems
outside the early-mislead/late-refutation structure; any single
deliberation policy other than the frozen deliberation-v1 baseline.
