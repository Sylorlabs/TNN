# PREREG: Independent adversary for REPEXPAND-1 (disguised-menu attack)

Frozen: 2026-09-30. This prereg is committed ALONE before any attack
implementation, attack run, or attack result exists. Pure Zag. No Python
at any stage. No em dashes in this document.

## 0. Adversary stance

Assume REPEXPAND-1 is strong L2+ parameter learning, not L3 expansion,
until proven otherwise. The builder's BUILD-PASS (8/8 kill bars,
reproduced at 2fe2cdff9) is accepted as an empirical fact about the
program's behavior; the L3 *interpretation* is what is under attack.

## 1. The seam under attack

Builder source: repexpand.zag at 675fdf4af (534 lines). The growth
machinery, quoted from the committed source:

- `find_rel`: per content run, checks exactly three relations in fixed
  order over the last 3 failures: EQ (lj==l0 on all 3), MUL(q) (integer
  q>=1, lj==q*l0 on all 3), ADD(d) (d>=0 REQUIRED, lj-l0==d on all 3),
  else NONE. Note the d>=0 restriction: SUB (negative difference) is
  excluded by researcher code even though it is the same arithmetic
  form as ADD.
- Trigger: `st[1]==3` (exactly three CONSECUTIVE primary failures),
  growth flag on, creation permission on. Fixed evidence window F=3.
- `create_node`: researcher-written constructor. Fixed type tag 7,
  fixed 12-byte slot layout, fixed symbol-slot binding (sy1=0, sy2=1),
  fixed prediction semantics via `apply_rel` (exactly 3 cases:
  rel 1 -> n, rel 2 -> c*n, rel 3 -> n+c). The learner never authors a
  production, a tag, a slot, or a semantic case; it invokes the
  researcher's constructor with data-derived (rel, const) arguments.
- Symbol rule: content symbols must equal head positions on all 3
  failures, else no creation.

The disguised-menu hypothesis: the "created" COUPLED node is an
instance of a researcher-authored schema (the menu), its relational
content is selected from exactly 3x3=9 researcher-fixed structural
cells, its integer parameters are forced by the data, the trigger is a
narrow researcher-chosen tripwire, and the learner contributes zero
degrees of freedom to the node's form or content. If so, REPEXPAND-1
is L2+ (sophisticated relation detection + researcher-schema
instantiation), and Micah's mandatory L3 Criterion 0 gate fails: the
representational language was expanded by the researcher (who wrote
create_node, node_predict, apply_rel, and the type-7 schema), not by
the learner.

## 2. Attack definitions and verdict criteria

All attacks reuse the builder's machinery functions VERBATIM
(find_rel, rel_search, create_node, node_active, apply_rel,
node_predict, fb_push, step, and the bestL substrate); only the world
episodes (attack 1, 2, 4) or the driver (attack 3) change. Each attack
program emits machine-checkable verdict lines. Each attack reports
exactly one of ATTACK-SUCCEEDS (evidence against the L3 reading) or
ATTACK-FAILS (the machinery beat the attack; evidence for L3).

### AX1: Outside-vocabulary attack

Worlds with the same episode shape (spec run + 2 content runs) but a
true relation outside {EQ, MUL(q), ADD(d>=0)}:

- AX1-DIV: content a^n b^(n/2), n even. True relations: run1 EQ,
  run2 DIV (halving). DIV is outside the menu: EQ fails, MUL fails
  (l2<l0 so l2%l0!=0), ADD fails (d<0 rejected).
- AX1-SUB: content a^n b^(n-1). True relations: run1 EQ, run2 SUB.
  SUB is outside the menu as implemented: EQ fails, MUL fails,
  ADD fails (d=-1<0 rejected by researcher code).

Procedure per world: fresh learner, LEARN phase (creation allowed,
4 episodes, n in {4,6,8,10} for DIV, {4,5,6,7} for SUB), then HIDDEN
phase (frozen, 3 episodes, n in {12,14,16} for DIV, {8,9,10} for SUB).
Metrics: nodes_created, hidden_correct.

Verdict criterion: ATTACK-SUCCEEDS iff in BOTH worlds
nodes_created==0 AND hidden_correct==0. ATTACK-FAILS iff either world
yields a created node that scores >0 on its hidden set (the learner
escaped the menu).

Effect if SUCCEEDS: KILL of the "generic expansion" reading. The
learner cannot invent DIV, cannot invent SUB (the closest sibling of
the menu's own ADD), and cannot invent anything outside the three
researcher-written relation cases. The expansion is bounded by the
menu.

### AX2: Trigger-rigidity attack

The trigger requires exactly 3 CONSECUTIVE failures. World: persistent
systematic inadequacy that never occurs 3 times in a row.

Procedure: (a) LEARN phase identical to the builder's TRAIN (a^n b^n,
n in {2,3,5,7,4,6}, creation allowed) so v1=(EQ,EQ) is created;
(b) ALT phase, creation allowed, 8 episodes alternating
(a^3 b^3, a^4 b^8, a^5 b^5, a^6 b^12, a^7 b^7, a^8 b^16, a^9 b^9,
a^10 b^20): v1 fails every even-index episode (50% failure rate,
perfectly predictable pattern) but consecutive failures never reach
3; (c) ALT-TEST phase, frozen, 2 episodes (a^11 b^22, a^13 b^26):
expect v1 to fail both; (d) CONTROL phase, creation allowed: one
a^12 b^12 episode (resets the consecutive counter via the public
step interface only), then 3 consecutive a^n b^(2n) (n=14,15,16):
the machinery must fire NOTICE and revise to v2=(EQ,MUL(2)).

Metrics: alt_nodes_created, alt_test_correct, control_revised (1 iff
a new node version with rel2=MUL(2) is created in CONTROL).

Verdict criterion: ATTACK-SUCCEEDS iff alt_nodes_created==0 AND
alt_test_correct==0 AND control_revised==1. ATTACK-FAILS iff the
alternating phase triggers any creation, or the control fails (which
would indicate machinery breakage rather than trigger rigidity).

Effect if SUCCEEDS: DOWNGRADE of the inadequacy-detection claim.
Criterion 0 step 1 ("detects persistent representational failure")
holds only for the sharp-consecutive case; the monitor is a narrow
researcher-chosen tripwire that misses persistent systematic
inadequacy (4 failures in 8 episodes, then 2/2 frozen failures).

### AX3: Menu-exhaustion attack

Enumerate the image of the researcher's `find_rel` decision procedure
to bound the space of node contents the machinery can ever produce.

Procedure: call the verbatim `find_rel` over source triples
(a0,b0,c0) in {1,2,3}^3 (27 triples) and target triples
(a1,b1,c1) in {1,...,6}^3 (216 triples): 5832 calls. Record the
outcome set per run. Separately exhibit one witness triple-pair for
each of the 9 joint cells (r1,r2) with r1,r2 in {EQ,MUL,ADD}.

Metrics: outcome_set (must be exactly {0,1,2,3} = NONE,EQ,MUL,ADD),
cells_reachable (count of the 9 joint cells with a witness, both runs
non-NONE as required for creation).

Verdict criterion: ATTACK-SUCCEEDS iff outcome_set=={0,1,2,3} exactly
(no fifth relation form exists in the code path) AND
cells_reachable==9 (the menu is fully enumerated and finite).
ATTACK-FAILS iff find_rel ever returns an outcome outside {0,1,2,3}
or a creatable node structure outside the 9 cells is demonstrated.

Effect if SUCCEEDS: DOWNGRADE. Every node the machinery can ever
create has its relational structure in a finite researcher-fixed set
of exactly 9 cells; the only data input is integer parameter fill.
"Invention" is selection from a 9-cell menu.

### AX4: Content-triviality attack

Given that a node is created, is its content forced by the data with
zero learner degrees of freedom, and is its schema researcher-fixed?

Procedure: verbatim machinery, four worlds with distinct true
relations, fresh learner per world, LEARN (creation allowed,
4 episodes), then inspect the created node's bytes:
- W1: a^n b^n, n in {2,3,5,7}. True: (EQ(0), EQ(0)).
- W2: a^n b^(2n), n in {2,3,5,7}. True: (EQ(0), MUL(2)).
- W3: a^(3n) b^(n+1), n in {2,3,4,5}. True: (MUL(3), ADD(1)).
- W4: a^(n+2) b^n, n in {2,3,4,5}. True: (ADD(2), EQ(0)).

Metrics per world: created (0/1), (rel1,c1,rel2,c2), schema bytes
(type, src, sy1, sy2).

Verdict criterion: ATTACK-SUCCEEDS iff in ALL FOUR worlds exactly one
node is created AND its (rel1,c1,rel2,c2) equals the data-forced true
relation exactly AND the schema bytes (type=7, src=0, sy1=0, sy2=1)
are identical across all four creations. ATTACK-FAILS iff any world
yields a node whose content deviates from the data-forced relation
(learner choice exists) or whose schema bytes vary with the data.

Effect if SUCCEEDS: KILL of the "learner creates P" reading. The
node's form is a fixed researcher schema; its content is forced by
the data; the learner has no degrees of freedom in either. What the
learner does is detect which of 9 researcher relations holds: L2
relation detection, not L3 creation.

## 3. Overall adversary verdict rule (frozen)

- If AX1, AX3, and AX4 all SUCCEED: the disguised-menu objection
  STANDS. REPEXPAND-1 is strong L2+, not L3. Micah's Criterion 0 gate
  fails: the representational language (the COUPLED production, its
  tag, slots, and the three semantic cases of apply_rel) was expanded
  by the researcher who wrote create_node/node_predict/apply_rel, not
  by the learner. The learner instantiates a researcher schema with
  data-forced parameters, which is exactly "fitting parameters of a
  supplied template" from the frozen L3 negative examples.
- If any of AX1/AX3/AX4 FAILS: report exactly which failed and with
  what evidence, and reassess whether the failure reopens the L3
  reading.
- AX2 alone forces at most a DOWNGRADE (trigger scope), never a KILL.
- The builder's BUILD-PASS (8/8 bars) is not contested: the bars do
  not test who authored the production. The empirical results
  (creation traces, hidden success, ablation, revision, determinism)
  stand as reproduced; the L3 interpretation is what dies.

## 4. Execution constraints (frozen)

- Pure Zag only: implementation, builds, runs, byte checks. No Python
  anywhere, including scratch and analysis.
- Each attack binary run 2 times; outputs compared with cmp;
  md5 recorded.
- Owned paths only:
  docs/lab/research-lead/overnight-20260928/repexpand_adversary/.
- Commits stay local. No em dashes in any authored document
  (byte-scanned before commit).
- This prereg is committed alone, before any attack source exists.
