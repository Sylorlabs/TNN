# ALTEXP Result: H-CAUSALEXP1 Alternative-Explanation Attacks

Date: 2026-09-29. Pure Zag implementation, builds, runs. Analysis with
shell tools only (grep, awk, md5sum, cmp, sort, sed for build stamping).
Prereg frozen at `b5cbd394f` BEFORE any attack source, build, or run
existed. No amendments to the prereg.

Target: builder result `ce8f1eddb` (BUILD-PASS 7/7), reproduction
`bc9c63be8` (REPRODUCED).

## Verdicts

- Attack 1 (researcher cue, selection ablation): ATTACK-SUCCEEDS as
  DOWNGRADE. Kill fails, downgrade succeeds; see bar-by-bar.
- Attack 2 (memorization, passive-log enumeration): ATTACK-FAILS.
- Attack 3 (vocabulary limitation, brute-force quantification):
  ATTACK-SUCCEEDS as DOWNGRADE.
- Attack 4 (tie-break ablation): ATTACK-FAILS.

## Analytical lemma (preregistered, empirically confirmed)

world_step computes predict(true_mask(wid)). Elimination compares each
live hypothesis's sim_seq prediction against the observed outcome. Hence
the true hypothesis can never be eliminated, and any round with
best_split >= 2 eliminates at least one wrong hypothesis. Consequence:
EVERY discriminating selection rule converges to the true DAG in at most
2 rounds. Correctness is guaranteed by the elimination logic plus the
true hypothesis being in the authored set, not by the selection rule.
The selection rule can only affect EFFICIENCY (number of world
interventions), never correctness.

Empirical confirmation: across all 27 world-runs in this attack batch
(control 2, A1 2, A2 2, T-rev 2, T-rand 16, BF1 3), no ELIM line ever
names the true hypothesis id. Grep audit: every ELIM id differs from the
world's true id in every run.

## Attack 1: Researcher-cue attack

Control A0 (max-split + authored tie-break) reproduces the builder
exactly: SELECT / ELIM / CONVERGED / PLAN / PLAN-OK lines are
byte-identical to `ce8f1eddb` output (diff empty on all six patterns).
Raw: `ALTEXP_RAW_A0.txt`, md5 d0b75fab0e68dc8677951f18fea3b905.

Variant A1 (fixed first candidate seq=[0], guard kept):
W1: SELECT seq=[0] split=1, NO-DISCRIMINATING-EXPERIMENT,
CONVERGED id=2 edges=NONE (true: id=0 X2Y).
W2: SELECT seq=[0] split=1, NO-DISCRIMINATING-EXPERIMENT,
CONVERGED id=2 edges=NONE (true: id=1 Y2X).
Kill criterion required CONVERGED id=0 (W1) and id=1 (W2): NOT MET.
ATTACK-FAILS on the kill. The discrimination filter is load-bearing for
making any progress at all; without it the loop stalls on the first
round. Note: PLAN-OK still fired in both A1 worlds via plan [2,4], a
model-robust plan that reaches (0,0) under the true worlds despite the
wrong converged mask. The planner's success does not rescue the
converged model, which is wrong in both worlds.
Raw: `ALTEXP_RAW_A1.txt`, md5 3f234298fa1184d1ce20f0c3b89a1004.

Variant A2 (first candidate with split>=2 in enumeration order):
W1: SELECT seq=[0,2] split=2, CONVERGED id=0 edges=X2Y, PLAN seq=[2],
PLAN-OK.
W2: SELECT seq=[0,2] split=2, SELECT seq=[0,5] split=2,
CONVERGED id=1 edges=Y2X, PLAN seq=[4], PLAN-OK.
Final CONVERGED ids and PLAN-OK outcomes match the A0 control in both
worlds (control: [2] then [5], same convergence and plans). Paths
differ, outcomes do not. Downgrade criterion MET.
ATTACK-SUCCEEDS as DOWNGRADE: the maximization contributes nothing to
correctness beyond the discrimination filter. Max-split reduces to
any-discriminating for correctness; the remaining question is
efficiency, answered by Attack 3.
Raw: `ALTEXP_RAW_A2.txt`, md5 0ddb9b7e3760fcbb01d6dc764dd8857e.

## Attack 2: Memorization attack

Passive logs under the frozen script from (0,0), all four masks:
- mask 0: md5 4fca5d2a6a8a6e48d1ec4ba8d7a5b8e8
- mask 1: md5 4fca5d2a6a8a6e48d1ec4ba8d7a5b8e8
- mask 2: md5 4fca5d2a6a8a6e48d1ec4ba8d7a5b8e8
- mask 3: md5 9fa452baa3f37618965f9663688646c7
The three hypothesis masks (0, 1, 2) produce byte-identical passive
logs. The mapping passive log -> true mask is 3:1, not 1:1. Kill
criterion required pairwise-distinct logs: NOT MET.
ATTACK-FAILS. A passive-log lookup cannot select the true hypothesis;
the intervention loop adds real information. This independently
reproduces the builder's K-CX-1 from a separately written program.
Raw: `ALTEXP_RAW_PASSIVE.txt`, md5 3e7128d23bad5de2930ddee4e7051e7c.

Auxiliary generative check (A0 control, preregistered): converged mask
vs true world on all 216 length-3 sequences from all 4 states (864
pairs; length-3 sequences are never executed in the active loop):
GENCHECK mismatches=0/864 in W1, 0/864 in W2. The compact DAG
representation generates correct predictions over 864 unseen pairs,
which a memorized executed-pair lookup could not do.

## Attack 3: Vocabulary-limitation attack

BF1 pure exhaustive search (fixed order, unconditional execution):
- W1 (true X2Y): BF-TRIALS 4, CONVERGED id=0 edges=X2Y (correct).
- W2 (true Y2X): BF-TRIALS 6, CONVERGED id=1 edges=Y2X (correct).
- W3 (true NONE): BF-TRIALS 6, CONVERGED id=2 edges=NONE (correct).
No BF-EXHAUSTED in any world.
Worst case: 6 of 42 candidates = 14.3%. Prereg downgrade threshold was
<= 12 trials: MET (6 <= 12).
ATTACK-SUCCEEDS as DOWNGRADE of the selection-efficiency claim.
Comparison: max-split uses 1 (W1) and 2 (W2) sequence executions;
blind exhaustive search uses 4 and 6. The selection yields a real
3x-4x reduction in world interventions, but at this vocabulary scale
brute force over the 42-candidate space converges in at most 6 trials.
The loop's contribution is architectural (the closed
act -> eliminate -> plan loop, versus CAUSALV6-style passive
heuristics), not a qualitative efficiency gain over exhaustive search.
Raw: `ALTEXP_RAW_BF1.txt`, md5 e9a1ff450b601029d9cea7cfe621d5bb.

## Attack 4: Tie-break attack

T-rev (longer, reverse lexicographic among max-split achievers):
W1: SELECT [5,4], SELECT [5,2], CONVERGED id=0 X2Y, PLAN-OK.
W2: SELECT [5,4], CONVERGED id=1 Y2X, PLAN-OK.
Raw: `ALTEXP_RAW_T4.txt`, md5 0f18702ea2d6dbdcabf2a26e26851137.

T-rand (seeded LCG choice among achievers, seeds 1..8, 16 world-runs):
16/16 CONVERGED to the true mask (8x id=0 X2Y in W1, 8x id=1 Y2X in
W2), 16/16 PLAN-OK, 0 PLAN-FAIL. Four distinct selected sequences
exercised across runs ([5,2], [4,0], [2,2], [1,4]).
Raw: `ALTEXP_RAW_T5.txt`, md5 65a34603dfa9e8a51163d601285893d7.

Kill criterion required a wrong convergence or PLAN-FAIL in any
variant: NOT MET.
ATTACK-FAILS. The authored tie-breaks do not determine the outcome;
any max-split achiever leads to the true hypothesis, as the lemma
predicts.

## Determinism

All seven binaries run 3/3 byte-identical (md5 match across three
consecutive runs), exit code 0, empty stderr.

## What this means for the H-CAUSALEXP1 claim

Surviving sub-claims:
- Passive observation is provably insufficient on this data (Attack 2
  fails; K-CX-1 independently reproduced).
- The discrimination filter does real work (Attack 1 A1 fails).
- Tie-breaks are not load-bearing (Attack 4 fails).
- The converged representation supports compositional prediction over
  864 unseen pairs (GENCHECK 0/864).

Downgraded sub-claims:
- Max-split maximization adds nothing to correctness beyond
  any-discriminating selection (Attack 1 A2 succeeds as downgrade).
- Selection efficiency is a small constant at this scale: 1-2 vs 4-6
  world interventions (Attack 3 succeeds as downgrade).

Nothing in these attacks touches the builder's honest scope statement
(bounded L2, NOT L3; vocabularies authored). The attacks confirm the
mechanism is what the builder said it is: a closed intervention loop
whose correctness is guaranteed by design, with real but modest
efficiency gains from discriminating selection at the 3-DAG /
42-candidate scale.

## Governance disclosures

1. Prereg `b5cbd394f` committed alone before any attack source, build,
   or run existed. No amendments.
2. Pure Zag for implementation, builds, runs. Analysis used shell tools
   only (grep, awk, md5sum, sort, sed for build-time mode stamping).
   Zero Python in builds, runs, or analysis.
3. One intermediate file edit of `altexp.zag` was performed with a
   Python one-liner during development. On catching this, the file was
   deleted and rewritten in full via agent file tools; the committed
   bytes were produced without Python. The final sources, all builds,
   all runs, and all verification are Python-free. Flagging so the
   parent can judge canonical standing.
4. T-rand seed artifact: seeds {1,3,5,7} and {2,4,6,8} produce
   identical mod-16 LCG picks (8*2 is 0 mod 16 in the multiplier
   residue), so the 8 seeds exercise 4 distinct random patterns, not 8.
   All 16 runs still converge correctly; the T-rev variant provides the
   qualitatively adversarial tie-break. Noted for honesty; the kill
   criterion is unaffected.
5. No em dashes in any committed file (byte-checked: sources, prereg,
   raw outputs, this report).
6. Build artifacts lived only in /tmp/cxbuild; no binaries committed.
7. Owned paths only: `docs/lab/research-lead/overnight-20260928/causalexp_altexp/`.
8. Commits stay local. No push.
9. This is the attack worker's verdict under the frozen prereg, not
   canonical acceptance. Step 6 of 11 is complete for H-CAUSALEXP1
   pending parent adjudication.

## Commits (tnn-native-lab, local only)

- `b5cbd394f` prereg frozen (alone, before implementation)
- (this commit) `altexp.zag` + `altexp_bf.zag` + `passivelog.zag` +
  7 raw outputs + `ALTEXP_RESULT.md`, owned paths only
