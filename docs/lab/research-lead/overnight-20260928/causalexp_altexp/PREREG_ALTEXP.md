# Preregistration: H-CAUSALEXP1 Alternative-Explanation Attacks (ALTEXP)

Role: Alternative-Explanation Attack Worker. Step 6 of the 11-step frontier
promotion pipeline for H-CAUSALEXP1.
Target: builder result commit `ce8f1eddb`, independent reproduction `bc9c63be8`.
Method: pure Zag only. No Python at any stage. Implementation, builds, runs in
Zag. Analysis with shell tools only (grep, awk, md5sum, cmp, sort, sed for
build stamping).
Owned paths only: `docs/lab/research-lead/overnight-20260928/causalexp_altexp/`.
No em dashes in any committed file. Commits stay local. No push.

## Standing facts assumed from the builder result

- Hypothesis vocabulary: 3 DAGs over {x,y}, edge masks 1 (x->y), 2 (y->x),
  0 (none). Authored.
- Experiment vocabulary: 42 candidates, a in 0..5, b in -1..5 (b=-1 means
  length 1). Authored.
- Selection rule: maximum split, tie-break shorter then lexicographic.
  Authored.
- Passive script: actions [0,1,0,1,1,0] from state (0,0). Authored.
- W1: true mask 1. W2: true mask 2.
- Builder honesty: bounded L2, NOT L3.

## Analytical lemma (drives the attack design, verified empirically below)

world_step uses predict(true_mask(wid)). Elimination compares each live
hypothesis's sim_seq prediction against the observed outcome. Therefore the
true hypothesis can never be eliminated, and any round with best_split >= 2
eliminates at least one hypothesis. Consequence: EVERY discriminating
selection rule converges to the true DAG in at most 2 rounds. Correctness is
guaranteed by the elimination logic plus the true hypothesis being in the
set, not by the selection rule. The selection rule can therefore only affect
EFFICIENCY (number of world interventions), never correctness. Attacks 1, 3,
and 4 are interpreted under this lemma: they quantify efficiency and
invariance, they cannot change the converged truth.

## Attack 1: Researcher-cue attack (selection-rule ablation)

Question: is the max-split selection actually doing work, or would a trivial
rule converge identically?

Variant A0 (control): max-split + authored tie-break (shorter,
lexicographic). Must reproduce the builder's SELECT / ELIM / CONVERGED /
PLAN lines before any attack variant is trusted.

Variant A1 (no discrimination filter): selection replaced by the fixed first
enumerated candidate seq=[0]. The loop's existing best_split < 2 guard is
kept (it is stopping logic, not the selection rule).
KILL criterion: if A1 emits CONVERGED id=0 in W1 and id=1 in W2 with PLAN-OK
in both worlds, the selection machinery is decorative: ATTACK-SUCCEEDS, and
the discriminating-selection claim is KILLED.
Otherwise (NO-DISCRIMINATING-EXPERIMENT stall, no convergence):
ATTACK-FAILS. The discrimination filter is load-bearing for making any
progress at all.

Variant A2 (filter kept, maximization removed): selection replaced by the
first candidate in enumeration order with split >= 2.
DOWNGRADE criterion: if the final CONVERGED id and the PLAN-OK / PLAN-FAIL
outcome match the A0 control in both worlds, the maximization contributes
nothing to correctness beyond the discrimination filter: ATTACK-SUCCEEDS as
a DOWNGRADE. The max-split claim reduces to any-discriminating for
correctness; the efficiency question moves to Attack 3.
If the final outcome differs from control: ATTACK-FAILS.

## Attack 2: Memorization attack (passive-log enumeration)

Question: can the entire behavior be explained as a finite lookup of
passive log -> correct hypothesis -> correct plan?

Program: run the frozen passive script from (0,0) under every mask in
{0,1,2,3} and emit the full 6-episode log per mask.
KILL criterion: if the four logs are pairwise distinct (the mapping from
passive log to true mask is 1:1), then passive observation suffices and the
active intervention loop is unnecessary: ATTACK-SUCCEEDS, and the passive
insufficiency premise (builder K-CX-1) is KILLED.
Otherwise (any collision; in particular masks 0, 1, 2 producing
byte-identical logs): ATTACK-FAILS. A passive-log lookup cannot select the
true hypothesis, so the intervention loop adds real information.

Auxiliary generative check (in the A0 control binary): after convergence,
compare the converged mask's sim_seq predictions against the true world's
predictions on all 216 length-3 action sequences from each of the 4 states
(864 unseen pairs; length-3 sequences are never executed in the active
loop). Report the mismatch count. Zero mismatches evidences compositional
prediction from the compact DAG representation rather than memorized
executed pairs. Auxiliary only; the verdict rests on the kill criterion.

## Attack 3: Vocabulary-limitation attack (brute-force quantification)

Question: is the space so small that active intervention is indistinguishable
from exhaustive search?

Variant BF1 (pure exhaustive search): fixed enumeration order (a=0..5,
b=-1..5). Execute each candidate unconditionally in the true world,
eliminate mismatching hypotheses after each trial, stop at 1 or fewer live
hypotheses or after 42 trials (emit BF-EXHAUSTED if the latter). Count
sequence executions (trials) to convergence for true masks 1, 2, and 0
(mask 0 added for completeness; the builder ran only masks 1 and 2).
Metric: worst-case trials divided by 42.
DOWNGRADE criterion: worst-case trials <= 12 (under ~29% of the candidate
space): ATTACK-SUCCEEDS as a DOWNGRADE of the selection-efficiency claim.
The loop's contribution is then architectural (the closed
act -> eliminate -> plan loop versus CAUSALV6-style passive heuristics), not
a qualitative efficiency gain over exhaustive search at this scale.
Otherwise: ATTACK-FAILS.
The builder's max-split trial counts (W1: 1, W2: 2) are reported alongside
for direct comparison.

## Attack 4: Tie-break attack (tie-break ablation)

Question: do the authored tie-breaks determine the outcome more than the
max-split criterion?

Variants, differing only in how max-split achievers are chosen:
T-auth: shorter, then lexicographic (control, same as A0 selection).
T-rev: longer, then reverse lexicographic (larger a, then larger b).
T-rand: seeded LCG choice uniformly among the max-split achievers,
seeds 1..8, full wid=1..2 run per seed, deterministic.
KILL criterion: if any variant converges to a wrong mask (CONVERGED id not
matching the true mask) or yields PLAN-FAIL, the tie-breaks are
load-bearing for the outcome: ATTACK-SUCCEEDS.
If every variant converges to the true mask with PLAN-OK: ATTACK-FAILS.
Path length (number of interventions) is reported per variant; only the
final outcome governs the verdict, per the analytical lemma.

## Reporting

Each attack reports exactly one of ATTACK-SUCCEEDS or ATTACK-FAILS with the
exact evidence (commit hashes, raw output md5, grep-extracted lines).
SUCCEEDS on Attacks 1/4 is a KILL of the targeted sub-claim; SUCCEEDS on
Attacks 2/3 is scoped as labeled above (Attack 2 kill is scoped to the
passive-insufficiency premise; Attack 3 success is a DOWNGRADE, not a kill,
of the efficiency claim).

## Governance

This prereg is committed BEFORE any attack implementation exists. No
`.zag` attack source, no build, and no run exists at this commit.
