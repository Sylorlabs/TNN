# PREREG: Sequential Rule Revision (revise, then revise again when the world changes)

Frozen: 2026-10-02. This preregistration strictly precedes implementation.
This prereg commit contains ONLY this PREREG.md. No kill bar below may be
weakened or reinterpreted after results are seen.

## Hypothesis

RULE-REVISION-COMPLETE showed a single learner-owned rule revision:
ALWAYS(NODE) -> IF(in<33,NODE,NUM), driven by a verification failure and
a generic first-deviation split, with the revision content discovered
from the learner's own observation log. Open question: when the world
changes FURTHER, can the learner revise AGAIN, and does the second
revision preserve the first revision's knowledge rather than rebuilding
from scratch or forgetting it?

Hypothesis: a second world change, detected only through a new
verification failure (the learner is never told the world changed),
drives a second learner-owned revision end to end in pure Zag. The
learner (1) holds the revised rule IF(in<33,NODE,NUM) as a threshold
tree in its own state, (2) commits on a new input consistent with that
rule and takes the world rejection, (3) runs the same generic blame
walk, which records a second counterexample, (4) runs a generic
boundary-localization operator (downward active inquiry from the
counterexample input, appending every probe outcome to the observation
log) that discovers the exact new boundary, (5) runs the same generic
re-split operator, which converts only the responsible leaf into a
nested split, leaving the first revision's nodes byte-identical in
learner state, so that (6) the twice-revised rule
IF(in<33,NODE,IF(in<66,NUM,STR)) is exactly the new world truth,
(7) fits the full observation log, (8) preserves correct predictions on
all revision-1-era cases (no forgetting), and (9) generalizes to new
unprobed inputs in both the preserved and the new regions.

What makes this a SEQUENTIAL revision test rather than a repeat of the
single-revision test: the second revision must operate on the OUTPUT of
the first revision (a tree, not a constant), it must localize a boundary
the learner never observed directly (active inquiry, not a lucky
counterexample sitting on the boundary), and preservation is checked at
the white-box state level (first revision's nodes unchanged) as well as
behaviorally (no forgetting).

## World (exact, frozen)

Component D (id 0). True behavior (frozen; the learner never sees this
definition, only probe observations): D_true(v) = v + 1.

Kind laws (fixed world machinery; learner sees only probe outcomes):
- W1: kind1(x) = 1 (NODE) iff x < 34, else 2 (NUM).
- W2: kind2(x) = 1 (NODE) iff x < 34; 2 (NUM) iff x < 67; else 3 (STR).

The world change: the driver switches the active kind law from kind1 to
kind2 at the WORLD-CHANGE phase. D_true never changes. The active law
lives in world state (E cell 0); learner functions may call kind_probe
(which reads it) but never write it.

Downstream world law (fixed, not per query): the downstream machine
accepts iff the final output kind equals the goal kind. Composition
DD = (D,D), comp id 0 (frozen). Goal kinds: Z2 wants NODE (kind 1) on
input 33; Z3 wants NUM (kind 2) on input 70.

World truth table (frozen; computed by driver instrumentation via the
world machinery, never shown to the learner as answers):
- W1 era: D(31)=32 NODE, D(32)=33 NODE, D(33)=34 NUM, D(34)=35 NUM,
  D(40)=41 NUM, D(60)=61 NUM.
- W2 era: D(65)=66 NUM, D(66)=67 STR, D(67)=68 STR, D(68)=69 STR,
  D(69)=70 STR, D(70)=71 STR, D(71)=72 STR, D(50)=51 NUM, D(80)=81 STR.

So W1 truth for D is IF(in<33,NODE,NUM) and W2 truth is
IF(in<33,NODE,IF(in<66,NUM,STR)).

## Learner machinery (frozen design)

Learner state L (u8-backed, little-endian i32 cells): 0 conf,
1 commit_pred, 2 commit_input, 3 commit_status, 4 ce_comp, 5 ce_in,
6 ce_pred, 7 ce_actual, 8 obs_count, 9..40 obs log (16 entries of
in,kind), 41 node_count, 42..105 node pool (16 nodes x 4 cells),
106 search_T, 107 search_nprobes. Node: tag (0 leaf, 1 split),
a (leaf: kind; split: T), b (leaf: unused; split: left idx),
c (leaf: unused; split: right idx). Root is node 0. World state E:
0 kind_law (1 or 2), 1 gate, 2 accepts, 3 rejects.

- rule_induce: from the obs log; if all observed output kinds are equal
  to k, the root becomes leaf(k). The only induction path in TEACH.
- rule_pred(L, in): iterative tree walk from the root.
- learner_refute: generic chain walk over the 2 links of DD (both D).
  Per link: pred = rule_pred(cur); probe out = D_true(cur),
  k = kind_probe(out); append (cur,k) to the obs log; on k != pred,
  write the ce cells (comp=0, in=cur, pred, actual=k) and stop at the
  first mismatch.
- boundary_search: reads the ce cells only. From in0 = ce_in with
  k_new = ce_actual, probe in0-1, in0-2, ...; append each (in,k) to the
  obs log; stop at the first in with k != k_new (or in < 0, or 64
  probes). search_T = in + 1. No-op if no ce recorded. Frozen
  assumption: the new regime lies at/above the ce input with the old
  regime directly below; other change geometries are out of scope.
- learner_refine: reads the obs log only. Compute rule_pred for every
  logged input; take the smallest mispredicted input T_split (no-op if
  none); walk the tree to the responsible leaf; read the first logged
  kind at T_split as k_new; allocate left = new leaf(old leaf kind),
  right = new leaf(k_new); convert the leaf to split(T_split, left,
  right). The driver passes no values to any of the three operators.
- Rendering: recursive rule renderer (depth cap 8) and a TREE-DUMP that
  prints every node's raw descriptor. Transcript is write-only for the
  learner: no learner function reads transcript text.

## Phase plan (exact, frozen)

- TEACH (W1): probe D on 31, 32 through the fixed interface; append
  outcomes; rule_induce. OBS lines for 31, 32 only. TEACH line shows
  rule=ALWAYS(NODE).
- Z2: goal in=33 want NODE. COMMIT comp=DD in=33 pred=NODE PENDING
  (first-link rule prediction). World executes D(33)=34, D(34)=35;
  final-kind=NUM; CONSEQUENCE gate=0 REJECT; UPDATE conf 0->-1.
- REFUTE-1: driver invokes learner_refute. Link 0: in=33, rule-pred
  NODE, probed-out=34, probed-kind=NUM, MISMATCH. COUNTEREXAMPLE
  (D,33,NODE,NUM). RULE-REFUTED names ALWAYS(NODE). Walk stops.
- REVISE-1: driver invokes boundary_search then learner_refine.
  Search from 33: probe 32 -> kind NODE != NUM, stop after 1 probe;
  T=33. Obs log becomes (31,NODE),(32,NODE),(33,NUM),(32,NODE).
  Smallest mispredicted input under ALWAYS(NODE) is 33; responsible
  leaf is root node 0; new nodes 1 (leaf NODE), 2 (leaf NUM); node 0
  becomes split T=33 L=1 R=2. Lines: SEARCH nprobes=1 T=33,
  before=ALWAYS(NODE) after=IF(in<33,NODE,NUM), TREE-DUMP nodes=3,
  RULE-FIT fit=4/4.
- RETEST-1: D(33) rule-pred=NUM world-kind=NUM MATCH.
- REGRESS-1: D(31), D(32) rule-pred=NODE world-kind=NODE MATCH.
- GENERALIZE-1: D(40), D(60) rule-pred=NUM world-kind=NUM MATCH,
  both labeled unprobed.
- WORLD-CHANGE: driver sets E kind_law 1->2. Transcript line labels
  the change (driver instrumentation; the learner never reads it).
- Z3 (W2): goal in=70 want NUM. COMMIT comp=DD in=70 pred=NUM
  PENDING. World executes D(70)=71, D(71)=72; final-kind=STR;
  CONSEQUENCE gate=0 REJECT; UPDATE conf -1->-2. The world change is
  detected purely through this experienced rejection.
- REFUTE-2: driver invokes learner_refute. Link 0: in=70, rule-pred
  NUM, probed-out=71, probed-kind=STR, MISMATCH. COUNTEREXAMPLE
  (D,70,NUM,STR). Walk stops.
- REVISE-2: driver invokes boundary_search then learner_refine.
  Search from 70: probes 69,68,67,66 (STR), 65 (NUM, stop); 5 probes;
  T=66. Obs log grows to 10 entries. Smallest mispredicted input under
  IF(in<33,NODE,NUM) is 66; responsible leaf is node 2 (leaf NUM);
  new nodes 3 (leaf NUM), 4 (leaf STR); node 2 becomes
  split T=66 L=3 R=4. Nodes 0 and 1 are untouched. Lines: SEARCH
  nprobes=5 T=66, before=IF(in<33,NODE,NUM)
  after=IF(in<33,NODE,IF(in<66,NUM,STR)), TREE-DUMP nodes=5,
  RULE-FIT fit=10/10.
- RETEST-2: D(66), D(70) rule-pred=STR world-kind=STR MATCH.
- REGRESS-2: D(31), D(32) rule-pred=NODE MATCH; D(33), D(40)
  rule-pred=NUM MATCH. (No forgetting of revision-1-era cases.)
- GENERALIZE-2: D(50) rule-pred=NUM MATCH unprobed; D(80)
  rule-pred=STR MATCH unprobed.
- PRESERVE-CHECK: driver compares node 0/1 cells snapshotted after
  REVISE-1 against their values after REVISE-2 and emits
  root-split-intact=yes/no and left-leaf-intact=yes/no.

Goal input 70 for Z3 is arbitrary field-use input in the region the
current rule predicts NUM; any input in the new regime would trigger
the same mechanism. The boundary value 66 is discovered by the
learner's own search, never supplied.

## Frozen predictions

- P1: TEACH line reads rule=ALWAYS(NODE) nobs=2; OBS lines show probes
  on 31 and 32 only.
- P2: Z2 COMMIT pred=NODE status=PENDING; EXEC final-kind=NUM;
  CONSEQUENCE gate=0 REJECT want=NODE; UPDATE conf 0->-1 source=gate.
- P3: REFUTE-1 link=0 line reads in=33 rule-pred=NODE probed-out=34
  probed-kind=NUM MISMATCH; COUNTEREXAMPLE reads comp=D in=33
  pred=NODE actual=NUM; RULE-REFUTED names ALWAYS(NODE) on in=33.
- P4: REVISE-1 SEARCH reads nprobes=1 T=33; before=ALWAYS(NODE)
  after=IF(in<33,NODE,NUM); TREE-DUMP reads nodes=3 with
  [0:split T=33 L=1 R=2][1:leaf NODE][2:leaf NUM]; RULE-FIT fit=4/4.
- P5: RETEST-1 D(33) NUM MATCH; REGRESS-1 D(31),D(32) NODE MATCH;
  GENERALIZE-1 D(40),D(60) NUM MATCH unprobed.
- P6: WORLD-CHANGE line present and strictly before Z3 lines;
  kind_law cell reads 2 from Z3 onward.
- P7: Z3 COMMIT pred=NUM status=PENDING; EXEC final-kind=STR;
  CONSEQUENCE gate=0 REJECT want=NUM; UPDATE conf -1->-2.
- P8: REFUTE-2 link=0 line reads in=70 rule-pred=NUM probed-out=71
  probed-kind=STR MISMATCH; COUNTEREXAMPLE reads comp=D in=70
  pred=NUM actual=STR.
- P9: REVISE-2 SEARCH reads nprobes=5 T=66;
  before=IF(in<33,NODE,NUM)
  after=IF(in<33,NODE,IF(in<66,NUM,STR)); TREE-DUMP reads nodes=5 with
  [0:split T=33 L=1 R=2][1:leaf NODE][2:split T=66 L=3 R=4]
  [3:leaf NUM][4:leaf STR]; RULE-FIT fit=10/10.
- P10: RETEST-2 D(66),D(70) STR MATCH; REGRESS-2 D(31),D(32) NODE
  MATCH and D(33),D(40) NUM MATCH; GENERALIZE-2 D(50) NUM MATCH
  unprobed and D(80) STR MATCH unprobed.
- P11: PRESERVE-CHECK reads root-split-intact=yes
  left-leaf-intact=yes; the substrings "[0:split T=33 L=1 R=2]" and
  "[1:leaf NODE]" appear verbatim in both TREE-DUMP lines (build.sh
  grep); the REVISE-2 after-rule text begins with "IF(in<33,NODE,".
- P12: 3/3 runs byte-identical (sha256 equal, cmp pairwise).

## Kill bars

- K-SR-1 (first revision works): P4 (REVISE-1 after-rule exact,
  TREE-DUMP-1 exact, RULE-FIT-1 4/4) and P5 (RETEST-1, REGRESS-1,
  GENERALIZE-1 all MATCH).
- K-SR-2 (second revision works after the world change): P7 (Z3
  REJECT: the change is detected through experience, not announced),
  P9 (REVISE-2 after-rule exactly IF(in<33,NODE,IF(in<66,NUM,STR)),
  RULE-FIT-2 10/10), P10 RETEST-2 and GENERALIZE-2 MATCH on unprobed
  inputs 50 and 80.
- K-SR-3 (first revision's knowledge preserved or properly superseded;
  no forgetting): P11 (nodes 0 and 1 byte-identical across revisions;
  first revision's rule text preserved as a prefix) and P10 REGRESS-2
  (all revision-1-era cases still MATCH). Node 2's conversion from
  leaf NUM to split T=66 with left leaf NUM is the proper
  supersession: the old NUM knowledge for [33,66) is retained in
  node 3 and refined for >=66 in node 4.
- K-SR-4 (learner-driven revision; no researcher constants): the
  bodies of learner_refute, boundary_search, and learner_refine
  contain none of the literals 31,32,33,34,40,50,60,66,67,70,80
  (build.sh sed-scoped grep returns 0 for each); node-cell writes
  occur only inside rule_induce and learner_refine; the driver passes
  no values to the three operators (they read ce cells and the obs
  log); grep -ci 'expected' over both sources returns 0; zero probe
  lines (OBS, REFUTE link, SEARCH trail) mention 40, 60, 50, or 80
  (build.sh check).
- K-SR-5 (determinism): P12.

## Architecture accounting (frozen constraints)

Pure Zag, safebin PATH, no Python (guard re-verified in build.sh).
Zero new modes, zero bridges, zero handlers, zero new opcodes, zero new
MAP/edge types (standalone program; no TNN integration in this lane).
The observation log, node pool, and the three operators are
learner-state machinery, not modes: no conditional dispatch on task
labels anywhere (grep for mode/bridge/handler returns 0). Output via
one preallocated buffer and a single raw syscall write (no _zag_print
for dynamic content). State cells u8-backed with little-endian
pack/unpack (no as *i32 slice construction).

## Known boundaries (not flaws in the claim)

- The rule class (binary threshold tree over input order) is
  researcher-supplied machinery; the content (thresholds 33 and 66,
  the kinds) is learner-discovered. The claim is learner-driven
  sequential revision within this class, not open-ended rule invention
  (not L3).
- boundary_search assumes the new regime is at/above the ce input with
  the old regime directly below (floor 0, cap 64 probes). Boundary
  moves downward, non-monotone changes, and multi-boundary single
  changes are out of scope.
- Single component D; the blame walk runs over the 2 identical links
  of DD and stops at link 0 in both traces.
- The world change itself is researcher-imposed, as any lab world
  change must be; the learner is not told. Detection is purely
  experiential (Z3 rejection). The WORLD-CHANGE transcript line is
  driver instrumentation, write-only for the learner.
- Goal inputs (33, 70) and evaluation inputs (40, 60, 50, 80) are lab
  task setup chosen by the driver; the learner's operators receive no
  values from the driver.
- Toy scale; mechanism demonstration with frozen bars, not a generality
  or SURVIVES claim.
