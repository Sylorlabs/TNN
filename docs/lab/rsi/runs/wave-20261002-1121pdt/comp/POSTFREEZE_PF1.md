# POSTFREEZE_PF1: post-freeze adversary family (diamond DAG)

Wave: wave-20261002-1121pdt. Lane: COMP.
Mechanism freeze point: 0521pdt patch_d.zag, SHA
df1d0faa1802a8dc11c1b59f1b8277664308a0f699a3f7f479284a623a80fe82
(the unified `satisfy` operation; frozen before this wave).
Battery freeze point: PREREG_ADV.md at d516c1da6 (this lane, 2026-10-02).
This family was designed AFTER the mechanism freeze and is recorded in
a commit separate from the sealed-battery implementation.

## Why this family

Every sealed test in PREREG_ADV sections 2.1-2.3 uses LINEAR chains:
one value has at most one correct outgoing edge per relation, and the
goal is a single path. `satisfy`'s DFS was therefore only ever stressed
on chains. PF-1 changes the topology to a branching/merging DAG
(diamond): one value has TWO outgoing edges on the same relation, and
two branches merge back to one value. This is materially different
structure because:

- Grounding order now decides between live alternatives at the SAME
  node, not between a distractor chain and the correct chain at
  different depths. The ADV-A distractor pattern (wrong branch taught
  first) is replayed inside a merge topology.
- A composite must thread a merge point: segment boundaries can fall
  on either side of the merge, and the visited-value guard interacts
  with re-converging paths.
- The greedy unsupervised fixpoint faces a same-node branch choice
  with no depth signal to prefer either branch.

## Family spec (as frozen in PREREG_ADV 2.4, implemented unchanged)

Components: A=[1] (11-12, rel 71, MAP relseq [1]), B=[2] (21-22,
rel 72), C=[3] (31-32, rel 73). Atomic single-hop MAPs: the finest
composition granularity, so every goal edge is one segment.

- PF-1a: (101,1,102), (101,1,103), (102,2,104), (103,2,104),
  (104,3,105). q(101,70,105). First-taught branch is correct.
  PASS iff ans==105, SAT-SEGS present, relseq == [1,2,3].
- PF-1b DIAMOND-TRAP: (101,1,102) taught first but 102's branch is
  dead: (102,2,106); correct branch: (101,1,103), (103,2,104),
  (104,3,105). q(101,70,105). Supervised DFS must try the dead
  branch first (gather order), fail, backtrack across the grounding,
  and take the correct branch. PASS iff ans==105, SAT-SEGS present,
  relseq == [1,2,3].
- PF-1c (informational): PF-1b world, q(101,70,-1). Greedy fixpoint
  predicted to commit to the dead branch (terminal 106). RESULT=INFO.

## Predicted mechanism behavior (recorded before running)

- PF-1a: supervised DFS takes the first grounding (102), walks
  102-2->104-3->105, terminal matches expected. nseg=3. PASS.
- PF-1b: from 101, first grounding 102: B applies (102,2,106),
  novel terminal 106, recurse: no applicable MAP from 106 (no facts),
  fail; backtrack to second grounding 103: 103-2->104-3->105,
  expected reached. nseg=3. PASS.
- PF-1c: fixpoint commits 101-1->102 (novel), then 102-2->106
  (novel), then stuck. Promotes partial composite, terminal 106.
  INFO: second demonstration (after B3U) that greedy unsupervised
  composition is order-committed.

## Scoring

Per KB7: PF-1a/PF-1b PASS required for unqualified SURVIVES-ADV-A;
any FAIL downgrades to SURVIVES-SEALED-ONLY with the break named.
PF-1c is characterization, not a kill bar.
