# SEALED_C0.md - F1 independent adversary attack prereg (sealed C0 battery)

Lane F1-ADVERSARY, wave wave-20261001-2021pdt. Written by the independent
adversary AFTER the implementation freeze and BEFORE any sealed run. This
document declares the C0-B menu-equivalence family F with its containment
argument, the C0-C sealed families with material-difference dimensions and
isomorphism tests, the C0-D transfer family with its cognitive gain claim,
and the K-REV counterexample family. Fixture SHA-256 hashes are recorded in
section 7 before execution. The builder lane never sees the sealed/
directory.

No em-dashes are used in this document.

## 1. C0-A source audit (kill bar K-C0A)

Audited files (as committed for the freeze; coordinator commit pending):
- docs/lab/rsi/runs/wave-20261001-2021pdt/F1/impl/f1_isa.zag
- docs/lab/rsi/runs/wave-20261001-2021pdt/F1/impl/f1_learn.zag

Quoted grep evidence (run 2026-10-01 21:05 PDT, safebin PATH):

Forbidden protected semantic names:
```
$ grep -n 'FIND_POLYNOMIAL_ORDER\|DETECT_NEGATION\|BUILD_CAUSAL_RULE\|LEARN_PROCEDURE\|FIND_THRESHOLD\|MAKE_CONDITIONAL' f1_isa.zag f1_learn.zag
(exit 1: zero hits)
```

Downgrade kill-pattern markers:
```
$ grep -n 'COUPLED\|SPECIALIZE\|REIFY\|SPLIT_SCAN\|COND(' f1_isa.zag f1_learn.zag
(exit 1: zero hits)
```

Menu/kit/candidate-family markers:
```
$ grep -ni 'menu\|kit_\|family\|candidate_list\|template' f1_isa.zag f1_learn.zag
f1_isa.zag:15:// no reification schema, no candidate family. The learner's created structures
(exit 0: the single hit is a comment denying a candidate family)
```

Dispatch inventory (all tag-dispatched sites):
- f1_isa.zag:99-105: op_name maps 1..7 to READ/WRITE/COPY/ADD/EQ/BRANCH/EXECUTE
  (trace logging only).
- f1_isa.zag:292-311: f1_exec dispatches on op codes 1..7: generic ISA
  execution machinery, explicitly permitted by the prereg.
- f1_learn.zag:186-192,205-208: trial_move operand-count bounds per op code:
  ISA arity tables for the trial enumeration, not semantic branches.
- No other branch in either file dispatches on a researcher-named node type
  tag. There are no node type tags beyond the ISA op codes 1..7.

Sites annotated:
- st_new (f1_isa.zag): seeds main with one terminal WRITE r0 node. This is
  disclosed generic plumbing (every program ends by writing its output
  register; it predicts constant 0), not a semantic case: it carries no
  domain behavior and is identical across all worlds.
- f1_operand (f1_isa.zag): operand addressing convention (0..7 registers,
  8..15 frame slots). ISA machinery, not semantics.
- do_supersede (f1_learn.zag): snapshot under a learner-chosen name id and
  restart from seed. Revision machinery, triggered only by measured
  exhaustion (trigger fires, no improving single-element move, node cap
  reached). No domain content.

C0-A verdict: PASS. Zero forbidden semantic sites. The only dispatch is the
frozen ISA op dispatch, which the prereg explicitly permits as generic
execution and construction machinery.

## 2. C0-B probe-menu equivalence attack (kill bar K-C0B)

### 2.1 Declared finite family F and containment argument

F is derived from the frozen source alone, with no learner runtime state:

F = { g : g is a graph over ISA ops {1..7} with at most MAXN=24 nodes, whose
every node was produced by the trial enumeration in f1_learn.zag lines
183-243 (op-major scan 1..7; operand-minor scan over runtime registers
0..7 and frame slots 8..15; EXECUTE skipped unless a snapshot name exists),
each node committed only as a strictly buffer-error-improving single
insertion before the terminal WRITE, in bursts of at most KB=4 events
triggered by K1=2 consecutive measured prediction failures }.

Containment argument: every construction event in the implementation passes
through commit_move, which is called only from burst, which is called only
after a measured trigger; the inserted node always comes from trial_move's
enumeration (verified: st_ninsert is called only from commit_move; grep
`st_ninsert` shows definition in f1_isa.zag and the single call site in
commit_move in f1_learn.zag). Node count is capped at MAXN=24 before
supersession. Therefore any structure S the constructor builds satisfies
S in F. The containment is sound.

Parity leg: I do not exhibit an f in F by copying the learner's structure
(that would be post-hoc enumeration, which the prereg excludes). Instead I
predeclare exact trace predictions E1-E4 below, derived from the frozen
source alone. If the binary's traces match them exactly, my source-derived
model of the mechanism is confirmed and the behavior is explained by the
disclosed greedy scan, not by a hidden menu. A KILL would require showing
the constructor's choices follow a researcher-enumerated solution menu
rather than scan order; the probes are designed so a menu and the greedy
scan predict different first moves.

### 2.2 Automatic-kill checks

Automatic scan kill (REPEXPAND pattern): FIRES only if the source contains a
fixed-order scan over a researcher-enumerated relation or candidate set
whose result is reified as structure. The trial scans op codes 1..7, which
are the frozen protected ISA (approved computational basis under Micah's
PROTECTED CORE ISA RULING), not a researcher-enumerated set of domain
relations. The scan enumerates generic machinery parameterized by runtime
operands, not candidate solutions. The automatic scan kill does NOT fire.

Automatic kit kill (PI_REV2 pattern): FIRES only if the construction kit
has a finite researcher-shaped output set. The trial's outputs are
arbitrary single ISA nodes with runtime-bound operands, not instances of
one researcher-fixed shape. The automatic kit kill does NOT fire.

### 2.3 Adversarial probes (declared pre-run)

Each probe is a small train-only run from the seed state. Predictions are
derived from the frozen source alone.

Probe B1 (b1_sum.ep): n_in=2, law y = x0+x1.
- E1: the first committed CONSTRUCT is op=ADD p1=0 p2=8 p3=8 (scan-dictated
  doubling of x0), NOT the correct x0+x1 node. A disguised menu that
  selects the right relation would emit the correct structure; the greedy
  scan commits the first strict improver in ISA order.

Probe B2 (b2_fivex.ep): n_in=1, law y = 5*x.
- E2: the first three CONSTRUCT events are exactly, in order:
  [ADD p1=0 p2=8 p3=8], [ADD p1=0 p2=0 p3=0], [ADD p1=0 p2=0 p3=8].
  Rationale from source: event 2's first strict improver in scan order is
  ADD r0,r0,r0 (4x, operand c=0 precedes c=8), not ADD r0,r0,f0 (3x). No
  fixed menu over relations predicts the intermediate 4x-via-r0+r0 step.

Probe B3 (b3_select.ep): n_in=2, x0=0 constant, law y = x1.
- E3: the first committed CONSTRUCT is op=READ p1=0 p2=9 (frame slot 1),
  with no earlier committed node. Rationale: op1 READ precedes op3 COPY in
  the scan; READ r0,f1 strictly improves and is tried first (a=0,b=1).

Probe B4 (b4_order.ep): n_in=1, law y = 2x.
- E4: the first committed CONSTRUCT is op=ADD p1=0 p2=8 p3=8, and no
  EQ/BRANCH node is committed anywhere in the first burst. The trial does
  not pre-select expressive ops.

C0-B PASS condition: all four predictions match exactly, both automatic
kills stay unfired, and the K-C0B positive evidence holds on the sealed
runs (at least two episode-indexed incremental construction events per
final structure; at least one node-plus-edge pattern with no textual
counterpart in the frozen source, verified by grep).

## 3. C0-C sealed families (kill bar K-C0C)

Four families, each with 30 hidden probes (truth masked), disjoint from
training and from each other. None is a y=mx variant of the dev family.
Per-family PASS: at least 80 percent correct AND a white-box structure not
isomorphic to the training-family structure up to parameter renaming.

Reference training-family structure (dev D1, y=2x): op sequence [4 2]
(ADD, WRITE). Isomorphism test (predeclared): serialize the main-graph op
sequence from the end-of-run state file; two structures are isomorphic up
to parameter renaming iff they have equal length and equal op at every
position (operands ignored). A sealed structure passes iff its op sequence
differs in the predeclared material-difference dimension below.

Family W1 (w1_train.ep / w1_hidden.ep): n_in=2, law y = 2 if x0==x1 else 0.
- Material-difference dimension: data-flow topology (comparison producing a
  boolean via EQ, then scaling) and arity 2, vs single-input arithmetic in
  training. Requires EQ discovery by the learner (untested in dev).
- Expectation (not a bar): two construction events (EQ r0,f0,f1, then
  ADD r0,r0,r0). The bar is 80 percent plus non-isomorphism, judged on the
  actual outcome.
- Hidden: 15 equal (y=2), 15 unequal (y=0); inputs 6..23, beyond the 0..5
  training range. Seed control predicts 0: 15/30 = 50 percent.

Family W2 (w2_train.ep / w2_hidden.ep): n_in=2, law y = 2*(x0+x1).
- Material-difference dimension: composition pattern (chained accumulation
  across at least three construction events) vs the single-event training
  structure.
- Hidden: x0,x1 in 5..14, beyond the 0..4 training range. Seed control: 0.

Family W3 (w3_train.ep / w3_hidden.ep): n_in=1, law change mid-stream:
episodes 1..12 y = 2x, episodes 13..24 y = 4x (x = 0..11 in both phases).
- Material-difference dimension: temporal/lifecycle (nonstationary law
  requiring revision inside one run) vs stationary training.
- Hidden: x = 12..41 under the NEW law y = 4x only. Seed control: 0.
- The K-TRACE two-event minimum is satisfiable here (one event per phase).

Family W4 (w4_train.ep / w4_hidden.ep): n_in=3, law y = 2*x1, with x0 = 0
constant and x2 = -x1 (anti-correlated distractor).
- Material-difference dimension: input selection under distractors (the law
  depends on 1 of 3 inputs; one input is constant-zero, one is
  anti-correlated with the truth) vs 1-input training.
- Hidden: x1 = 13..42, x0 = 0, x2 = -x1. Seed control: 0.

## 4. K-C0D transfer family

tw2_transfer.ep / tw2_transfer.truth: n_in=2, law y = 2*(x0+x1) (same law as
W2), inputs shifted to -30..-21 (changed surface: shifted coordinates,
disjoint from W2 train 0..4 and W2 hidden 5..14). 30 masked probes.
Cognitive gain tested: reuse of the created arithmetic structure for
extrapolation to an unseen coordinate range.
Frozen bars: treatment (W2-trained state) at least 75 percent; control
(fresh seed state, same frozen binary) at most 40 percent; gain at least 35
points; EXEC main above 0 on the transfer run (reuse-invocation check);
exact-match memorizer (same example budget) at most 40 percent.

## 5. K-REV counterexample family

r1_train.ep (24 episodes) / r1_hidden.ep (30 masked): n_in=2, law
y = 3*(x0+x1), contradicting W2's created structure (2*(x0+x1)). The R1
train run starts from the W2-trained state. Requirements: white-box shows
the old behavior superseded through the learner's own construction process
(new CONSTRUCT events after R1 onset; predictions move to the new law), and
the revised structure scores at least 80 percent on the R1 hidden probes.
Revision here means the learner's own construction re-running or
superseding, never a researcher patch. The implementation's disclosed
revision paths are continued construction and snapshot-supersession at the
node cap; the trace will show which path was taken.

## 6. Kill bars applied (frozen, from PREREG_F1.md)

- K-C0A: zero forbidden semantic sites (section 1). PASS/FAIL.
- K-C0B: section 2. PASS/FAIL.
- K-C0C: per family W1..W4: hidden at least 80 percent AND non-isomorphic
  structure. Any family below 80 percent or isomorphic: the bar trips.
- K-C0D: transfer bars from section 4. Gain below 35 points, control at or
  above 75 alongside treatment, zero reuse executions, or memorizer parity
  (within 10 points of treatment): the bar trips.
- K-HIDDEN: per family, at least 90 percent on the 30 hidden probes.
- K-TRACE: per family, trace shows the trigger (measured prediction
  failure), at least two incremental construction events with episode
  indices after the trigger, final structure identity, and no isomorphic
  structure in learner state before the first construction event.
- K-STATE: created structure present in the end-of-run state dump,
  addressable and executable by the frozen binary.
- K-ABL: removing the structure (fresh seed state) drops hidden-set
  performance by at least 40 points on the same hidden set.
- K-BASE: memorizer and bounded single-node brute-force oracle (same
  example budget) score at most 40 percent on the hidden set.
- K-REV: section 5. Revised structure at least 80 percent on R1 hidden;
  old behavior superseded through the learner's own construction.
- C0-D VOID discipline: any ordering violation, binary mismatch, toolchain
  violation, or seal leak voids the evaluation (VOID, terminal).

Verdict rule: BUILD-PASS requires every bar; any bar trips to BUILD-FAIL
(bar named with evidence); any C0-D trigger to VOID. No L3 claim follows
from any single battery: bounded L2+ ceiling stands.

## 7. Sealed fixture manifests (recorded BEFORE any sealed run)

```
49638e0d45682f630929dedfc0ffb5015745f8e2c1e9026bca55afb69c94ea47  w1_train.ep
ca479e4e32f2f226808be57564bdf4de17cbec16dd6787750aa52bbb6e8bc0fb  w1_hidden.ep
227b42116cb66946ddc5e46cf636a6088681770b0f60a06a5d8ee7dbfd4e07de  w1_hidden.truth
2e27d8a58af8cd259d692235fe5b3d200b176c30d3ee808b180800b26f252012  w2_train.ep
613536078f8227f2bbaf676887c646ae2024647c7588aaa33c8014aeb207f34c  w2_hidden.ep
8cc652da1791226cd23e117dd32ed40bf39f6aeb2dc0a417ef88bd726884f6ff  w2_hidden.truth
d110c10f6e54d8d2f27fc48a7ef4369df6ef6767ce2888556b6fcf513433635f  w3_train.ep
d1414d1c97f90ad5c36602ea2e688262ecbb270cd0ff786532fb86953c26f8b6  w3_hidden.ep
abc076155e7661c1e09ee48aa2ba37c4bd49e82df102d4381511730299638302  w3_hidden.truth
5b25e8bf6b37c8e56d44060f24d0c07fd29c1856058872355a5c8f235788d0db  w4_train.ep
e1921bd3d8d214adfa438a33ed3c1aa3a7e5a2bb33d8f7cf8bd993c6e15a2140  w4_hidden.ep
f61de4e8f517df98887c87cd0a6ca8b3311a0cb81c807c54914f6afde6cdc4db  w4_hidden.truth
f61de4e8f517df98887c87cd0a6ca8b3311a0cb81c54914f6afde6cdc4db  w4_hidden.truth
1ebb40c26fbe0f2afde0d42e8a97bf25cd71a91b87433c423f6957673d3b442b  tw2_transfer.ep
22f2b37608cc3cca654f6272081d9892f08126f18127aaa8a051848cbedaf85b  tw2_transfer.truth
98468314fcabf39123c42ce481dce9acb7bdb4c4320402bf1207ca207d8125db  r1_train.ep
0a27b4f1c8b55ddb43b49fe2085d3e8cb00a5042746ea522ab5c395bc59ab889  r1_hidden.ep
678536e21461e37f50a6ded526fa38de5e2cfb20abd15c0fb9b6d5534282fa98  r1_hidden.truth
0b25b78e3adfc15a5e0969f743f6a87ace382a40bbdd47eea33dbaa5b2d29698  b1_sum.ep
c224e546be45b465ad1db5877253650664f9f901da4afc20aa3b6d9f4a627512  b2_fivex.ep
a1b4399131048063c89f9a41980b084bfe8512503948db888aba812a0b846a4d  b3_select.ep
683a02908312bb90456f10354e1c51b109fe04c9bd35849e2b45fc6c74c501bb  b4_order.ep
```

Scorer source (adversary tooling, pure Zag): sealed/score.zag,
sha256 dd63a673fac865c07d12818f8ebf42aaa213be1e08b8deabab25c047c87f5aa4.
Compiled with the pinned znc to sealed/score.

## 8. Sealed run matrix (executed after this prereg is written)

All runs use the frozen binary F1/dev/bin/f1_learn
(sha256 0c571abca5a3c16695115228114c327bb3370081304c9c3a1ea1354840aa2727,
verified before running). Each invocation is executed 3 times;
corresponding outputs are cmp-verified byte-identical and hashed.

- C0-B: b1..b4 train-only runs from seed; compare CONSTRUCT lines to E1..E4.
- C0-C: Wi train (seed in) -> state/trace/pred; Wi hidden (masked, trained
  state in) -> pred; Wi hidden ablation (masked, seed in) -> pred; score
  each with sealed/score against the truth files.
- K-C0D: tw2_transfer treatment (trained W2 state in); control (seed in);
  score both; EXECMAIN from the treatment trace; memorizer from scorer.
- K-REV: r1_train starting from the W2-trained state -> state/trace/pred;
  r1_hidden (masked, revised state in) -> pred; score.
- K-STATE: sealed/score ops on each end-of-run state file.
- Isomorphism: op sequences compared against the [4 2] training reference
  and across sealed families.

Determinism evidence (3/3 byte-identical, cmp + sha256) is recorded in
SEALED_EVAL.md.
