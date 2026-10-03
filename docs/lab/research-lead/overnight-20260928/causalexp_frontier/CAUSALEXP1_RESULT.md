# H-CAUSALEXP1 Result: BUILD-PASS

Date: 2026-09-29. Pure Zag. No Python at any stage.
Prereg frozen at `bd883d969` BEFORE implementation. No amendments.

## Verdict: BUILD-PASS

All seven frozen kill bars hold. Per the frontier rules, the builder does
NOT promote to SURVIVES. Promotion requires the 11-step pipeline
(independent reproduction, baselines, OOD, ablation, transfer, red team,
governance audit).

## What was built

`causalexp.zag`: an active causal discovery loop. A causal hypothesis is a
DAG over {x,y} (edge mask: bit0 = x->y, bit1 = y->x). The program:

1. runs a fixed passive episode script against a hidden true world,
2. generates all three DAG hypotheses, each checked against the passive
   log (evidence = matches/6),
3. dumps the hypotheses white-box (HYPO lines: id, edges, status,
   evidence),
4. loops: enumerate 42 candidate experiments (action sequences length
   1..2), compute each live hypothesis's predicted outcome, select the
   maximum-split candidate (tie-break: shorter, then lexicographic),
   execute it in the true world, eliminate hypotheses whose predictions
   mismatch the observation,
5. plans with the survivor: BFS over action sequences length 1..3 under
   the surviving DAG to a frozen goal, executes the plan in the true
   world.

Two true worlds run in one binary: W1 (true x->y), W2 (true y->x).

## Bar-by-bar

**K-CX-1 (passive indistinguishability): PASS.** Both worlds emit
`PASSIVE-CHECK hypo=0/1/2 edges=X2Y/Y2X/NONE ev=6/6` and all three enter
the active loop LIVE. The passive logs are identical across worlds, and no
hypothesis is eliminated passively. Passive observation provably cannot
distinguish the three structures on this data.

**K-CX-2 (explicit representation): PASS.** Raw output contains HYPO lines
for all three edge codes with evidence 6/6 and status LIVE in each world,
plus PRED lines giving every live hypothesis's predicted outcome for each
selected experiment (e.g. W1 round 1: X2Y -> (0,0); Y2X -> (0,1);
NONE -> (0,1) for seq=[2]).

**K-CX-3 (discriminating selection): PASS.** Every SELECT has split=2
(W1: [2]; W2: [2] then [5]). A CAND-line audit of all 42 candidates per
round confirms split 2 is the maximum and the selected experiment is the
shortest, lexicographically smallest achiever. No round selects a
non-discriminating experiment.

**K-CX-4 (elimination correctness): PASS.** ELIM lines name exactly the
hypotheses whose predictions mismatch the observed outcome:
W1: id=1,2 eliminated (predicted (0,1), observed (0,0));
W2 round 1: id=0 eliminated (predicted (0,0), observed (0,1));
W2 round 2: id=2 eliminated (predicted (0,1), observed (1,1)).
Final: W1 CONVERGED id=0 X2Y (true); W2 CONVERGED id=1 Y2X (true).
The W2 path needs two interventions while W1 needs one, showing the loop
adapts to elimination results rather than following a fixed script.

**K-CX-5 (planning from surviving model): PASS.** W1 PLAN seq=[2]
(do(x:=0)); W2 PLAN seq=[4] (do(y:=0)). Both are the first
(shortest, lexicographic) goal-achieving plans under the surviving DAG,
both execute in the true world reaching (0,0) (PLAN-OK). Same goal,
different plans: the planner uses the converged causal model, not a fixed
policy.

**K-CX-6 (transfer, one binary): PASS.** K-CX-1..K-CX-5 hold for W1 and W2
in a single run. Grep audit of `wid`: the token appears only in
`true_mask`/`world_step` (the oracle), the main loop variable, WORLD
labeling lines, and as an argument passed to `world_step`. No
world-conditional logic exists in any learner function (predict, sim_seq,
selection, elimination, planning).

**K-CX-7 (determinism): PASS.** 3 consecutive runs byte-identical
(md5 612580bd641860d021dd48b453e2295b), exit code 0, empty stderr.

## Required evidence mapping

- Worlds where passive observation cannot distinguish H1/H2/H3: K-CX-1
  (6/6 for all three, both worlds, identical passive logs).
- Explicit hypothesis representation: K-CX-2 (HYPO + PRED white-box
  lines).
- Discriminating experiment selection: K-CX-3 (max-split selection,
  CAND audit).
- Hypothesis elimination via intervention: K-CX-4 (ELIM lines, converged
  on truth).
- Revised causal structure used for planning: K-CX-5 ([2] vs [4]).
- Transfer to new causal world: K-CX-6 (W2 with different true DAG).

## Honest scope

Authored machinery: the hypothesis vocabulary (all DAGs over 2
variables), the experiment vocabulary (do-operations, sequences up to
length 2), trigger/root semantics, selection tie-breaks. The learner
contributes: representing competing hypotheses with evidence and
intervention predictions, selecting discriminating experiments from its
own uncertainty, eliminating via intervention outcomes, planning with the
survivor.

Classification: bounded L2 architecture-signal response. NOT L3: the
causal graph vocabulary is fixed and researcher-enumerated; no
representational expansion occurs. The advance over CAUSALV6 is
architectural: a closed intervention loop (act -> eliminate -> plan)
instead of another passive observation heuristic. No confirmation rule,
floor, or guard was added to any observation-only learner.

## Governance disclosures

1. Prereg commit `bd883d969` also contains
   `proclang_frontier/PREREG_PROCLANG1.md`, staged concurrently by another
   worker before my commit ran. My prereg file at that commit is
   byte-identical to what I authored (md5 verified), and no H-CAUSALEXP1
   implementation, build, or run existed at that commit. The
   prereg-before-implementation ordering is intact; the extra file is an
   unrelated worker's prereg, not my implementation.
2. Pure Zag throughout: implementation, builds, runs. Analysis used only
   shell tools (grep, awk, md5sum, cmp). Zero Python. Zero em dashes
   (byte-checked in source, prereg, raw output, and this report).
3. Build artifacts lived only in /tmp/cxbuild; no binaries committed.
4. This is the builder verdict under the frozen prereg, not canonical
   acceptance. The 11-step promotion pipeline (independent reproduction,
   baselines, OOD, ablation, transfer, red team, governance audit)
   remains for the parent to schedule.

## Commits (tnn-native-lab, local only)

- `bd883d969` prereg frozen (alone as authored; see disclosure 1)
- (this commit) `causalexp.zag` + `CAUSALEXP1_RAW.txt` +
  `CAUSALEXP1_RESULT.md`, owned paths only

Raw: `CAUSALEXP1_RAW.txt` (md5 612580bd641860d021dd48b453e2295b).
