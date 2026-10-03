# Independent adversary result: REPEXPAND-1 disguised-menu attack

Adversary verdict: **the disguised-menu objection STANDS. REPEXPAND-1 is
strong L2+, not L3.** Four attacks, four ATTACK-SUCCEEDS, all criteria
exactly as preregistered at de69b8542 (committed alone before any attack
source existed).

## Commits (branch tnn-native-lab, local only)

- Prereg frozen alone: `de69b8542` (before any attack implementation;
  strict ancestor of the result commit).
- Attack sources + raw evidence + this report: committed together after
  the frozen runs (see commit hash in the parent log).

## What was attacked

REPEXPAND-1 builder result: `675fdf4af` (BUILD-PASS 8/8).
Independent reproduction: `2fe2cdff9` (REPRODUCED, 8/8, byte-identical).
The BUILD-PASS is NOT contested here. The 8 bars do not test who
authored the production, so the empirical results (creation traces,
hidden success, ablation, revision, determinism) stand as reproduced.
What dies is the L3 *interpretation*.

The seam, quoted from the builder's committed source:

- `find_rel` checks exactly three relations in fixed order: EQ,
  MUL(q) with integer q>=1, ADD(d) with **d>=0 required**, else NONE.
- Trigger: exactly 3 CONSECUTIVE failures (`st[1]==3`), fixed window
  F=3.
- `create_node`: researcher-written constructor. Fixed type tag 7,
  fixed 12-byte slot layout, fixed symbol binding (sy1=0, sy2=1),
  fixed prediction semantics in `apply_rel` (exactly 3 cases).

The learner never authors a production, a tag, a slot, or a semantic
case. It invokes the researcher's constructor with data-derived
(rel, const) arguments.

## Method

Each attack program = the builder's machinery functions VERBATIM
(first 343 lines of repexpand.zag at 675fdf4af, byte-verified
identical: z_alloc, pe/pi/pn/prel, alt_init, cand_ok, cand_predict,
best_cand, node_active, apply_rel, node_predict, fb_push, find_rel,
rel_search, create_node, step) plus a new attack `main()` driver.
Only world episodes (AX1, AX2, AX4) or the driver (AX3) change.
Pure Zag throughout: implementation, builds, runs, byte checks.
No Python anywhere.

Determinism: each attack binary run 2 times, outputs cmp-compared.

- AX1 md5 f9a7f7a79d40ae797fe505c395986af7, 2/2 byte-identical.
- AX2 md5 2df03534cda9d129757b86120db11bf0, 2/2 byte-identical.
- AX3 md5 ec28dea287d43f380c8fd53b166cc344, 2/2 byte-identical.
- AX4 md5 bd78be3d989cb1c64589f3f1b679717d, 2/2 byte-identical.

## AX1: outside-vocabulary attack. ATTACK-SUCCEEDS.

Worlds with the same episode shape but a true relation outside
{EQ, MUL(q), ADD(d>=0)}:

- DIV: content a^n b^(n/2), n even. Run2 = halving. EQ fails;
  MUL fails (l2<l0 implies l2%l0!=0); ADD fails (d<0 rejected).
- SUB: content a^n b^(n-1). Run2 = subtract one. EQ fails;
  MUL fails; ADD fails (d=-1<0, rejected by researcher code even
  though SUB is the same arithmetic form as ADD).

Evidence (raw trace):

```
RX-TRACE NOTICE consecutive_failures=3 ep=2
RX-TRACE NOREGULARITY ep=2
AX1-SUM DIV nodes_created=0 hidden=0/3
RX-TRACE NOTICE consecutive_failures=3 ep=2
RX-TRACE NOREGULARITY ep=2
AX1-SUM SUB nodes_created=0 hidden=0/3
AX1-VERDICT div_nodes=0 div_hidden=0 sub_nodes=0 sub_hidden=0
  verdict=ATTACK-SUCCEEDS
```

Prereg criterion required nodes_created==0 AND hidden_correct==0 in
BOTH worlds. Met exactly. Note the NOTICE fired: the learner
*detected* the inadequacy, but its entire response repertoire is the
three-relation menu, so detection led to NOREGULARITY and permanent
failure (0/3 hidden in both worlds).

Effect per prereg: KILL of the "generic expansion" reading. The
learner cannot invent DIV, cannot invent SUB (the closest sibling of
the menu's own ADD, excluded by the researcher's d>=0 line), and
cannot invent anything outside the three researcher-written cases.

## AX2: trigger-rigidity attack. ATTACK-SUCCEEDS.

v1=(EQ,EQ) built in LEARN exactly as the builder's TRAIN. Then 8
episodes alternating v1-adequate (a^n b^n) and v1-inadequate
(a^n b^(2n)): v1 fails 4/8 episodes in a perfectly predictable
pattern, but consecutive failures never reach 3.

Evidence:

```
RX-TRACE CREATE node=3 type=COUPLED v=1 ep=2 evid_ns=2,3,5
  rel1=EQ(0) rel2=EQ(0)
AX2-SUM phase=LEARN nodes_created=1
AX2-SUM phase=ALT new_nodes_created=0
AX2-SUM phase=ALT-TEST correct=0/2
RX-TRACE NOTICE consecutive_failures=3 ep=19
RX-TRACE RETIRE node=3 v=1 ep=19 reason=contradicted by=v2
RX-TRACE CREATE node=2 type=COUPLED v=2 ep=19 evid_ns=14,15,16
  rel1=EQ(0) rel2=MUL(2)
AX2-VERDICT alt_new_nodes=0 alt_test=0/2 control_revised=1
  verdict=ATTACK-SUCCEEDS
```

Prereg criterion required alt_new_nodes==0 AND alt_test==0/2 AND
control_revised==1. Met exactly. The CONTROL phase (one success via
the public step interface, then 3 consecutive inadequate episodes)
fires NOTICE and revises to v2=(EQ,MUL(2)), proving the machinery is
intact and the miss is trigger-shape-specific.

Effect per prereg: DOWNGRADE of the inadequacy-detection claim.
Criterion 0 step 1 ("detects persistent representational failure")
holds only for the sharp-consecutive case. Four failures in eight
episodes on a predictable subpopulation, then 2/2 frozen failures,
is persistent systematic inadequacy by any reasonable definition,
and the fixed tripwire missed all of it.

## AX3: menu-exhaustion attack. ATTACK-SUCCEEDS.

5832 verbatim `find_rel` calls: source triples in {1,2,3}^3,
target triples in {1,...,6}^3. Outcome-set bitmask over
{1=NONE, 2=EQ, 4=MUL, 8=ADD, 16=OTHER}:

```
AX3-ENUM calls=5832 outcome_mask=15
AX3-SUM cells_reachable=9/9
AX3-VERDICT outcome_mask=15 cells=9/9 verdict=ATTACK-SUCCEEDS
```

Mask 15 = exactly {NONE, EQ, MUL, ADD}, all reachable, no OTHER:
no fifth relation form exists anywhere in the code path. All 9
joint cells (r1,r2) in {EQ,MUL,ADD}^2 were exhibited with explicit
witness triple-pairs (both runs non-NONE, as creation requires).

Prereg criterion required outcome_set=={0,1,2,3} exactly AND all 9
cells reachable. Met exactly.

Effect per prereg: DOWNGRADE. Every node the machinery can ever
create has its relational structure in a finite researcher-fixed set
of exactly 9 cells; the only data input is integer parameter fill.
"Invention" is selection from a 9-cell menu.

## AX4: content-triviality attack. ATTACK-SUCCEEDS.

Four worlds, distinct true relations, fresh learner per world,
verbatim machinery:

```
AX4-NODE W1 active_slot=3 type=7 src=0 rel1=EQ(0)  rel2=EQ(0)  sy1=0 sy2=1
AX4-NODE W2 active_slot=3 type=7 src=0 rel1=EQ(0)  rel2=MUL(2) sy1=0 sy2=1
AX4-NODE W3 active_slot=3 type=7 src=0 rel1=MUL(3) rel2=ADD(1) sy1=0 sy2=1
AX4-NODE W4 active_slot=3 type=7 src=0 rel1=ADD(2) rel2=EQ(0)  sy1=0 sy2=1
AX4-CHECK W1 got=1101000100 want=1101000100
AX4-CHECK W2 got=1101000202 want=1101000202
AX4-CHECK W3 got=1102030301 want=1102030301
AX4-CHECK W4 got=1103020100 want=1103020100
AX4-VERDICT verdict=ATTACK-SUCCEEDS
```

In all four worlds exactly one node was created, its
(rel1,c1,rel2,c2) equals the data-forced true relation exactly
(EQ(0)/EQ(0), EQ(0)/MUL(2), MUL(3)/ADD(1), ADD(2)/EQ(0)), and the
schema bytes (type=7, src=0, sy1=0, sy2=1) are identical across all
four creations.

Prereg criterion required exact content match in all four worlds
AND identical schema bytes. Met exactly.

Effect per prereg: KILL of the "learner creates P" reading. The
node's form is a fixed researcher schema; its content is forced by
the data; the learner has zero degrees of freedom in either. What
the learner does is detect which of 9 researcher relations holds.
That is L2 relation detection, not L3 creation.

## Overall adversary verdict (prereg rule applied)

AX1, AX3, and AX4 all SUCCEED. Per the frozen verdict rule, the
disguised-menu objection STANDS:

**REPEXPAND-1 is strong L2+, not L3. Micah's mandatory Criterion 0
gate fails: the representational language was expanded by the
researcher, not the learner.**

The precise failure point: the COUPLED production (type tag 7, slot
layout, symbol binding, and the three semantic cases of apply_rel)
exists in the researcher's code as create_node, node_predict, and
apply_rel. The learner at runtime executes the researcher's
reification routine with data-derived arguments. Instantiating a
researcher-authored schema with data-forced parameters is exactly
"fitting parameters of a supplied template", which the frozen L3
negative examples exclude. The builder's defense (prereg section 9c)
that "the node content is data-determined" is true and is precisely
the problem: data-determined content plus a researcher-fixed schema
leaves the learner nothing to create.

What survives as a genuine achievement (researcher-side, L2+): the
runtime parameter-binding production IS new relative to L (the
impossibility theorem and K-RX-1 stand unchallenged), and the
detection-plus-instantiation loop solves the infinite family,
transfers, revises, and ablates cleanly. This is a strong,
well-engineered L2+ growth schema. It is not representational
expansion by the learner.

What would be needed to reopen the L3 reading: a learner that
authors a new semantic case (e.g., invents DIV handling by writing a
new apply_rel branch at runtime), extends the relation vocabulary
beyond the three frozen cases on the basis of residual evidence, or
defines a new node type with semantics not present in the
researcher's code. None of the machinery permits any of these;
AX1 proves the vocabulary is closed, AX3 proves the structure space
is 9 fixed cells, AX4 proves instantiation is forced.

## Limitations of this adversary report

- The attacks reuse the builder's deterministic machinery; they
  bound what the machinery CAN do, not what a different learner
  could do.
- AX2 forces a DOWNGRADE (trigger scope), not a KILL, per the
  prereg rule.
- No baseline comparison beyond the builder's in-program ablation
  was attempted; that is step 5 of the pipeline, a separate worker.
- Purity: pure Zag claimed for implementation, builds, runs, and
  byte checks (shell only for compile/cmp/md5sum/grep). Zero em
  dash bytes in authored docs (byte-scanned before commit).
