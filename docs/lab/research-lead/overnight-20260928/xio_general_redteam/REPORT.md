# REPORT.md -- XIO-General Red-Team Battery

## Verdict: XIO-GENERAL-REDTEAM-COMPLETE

Five adversarial attacks executed against the H-XIO-4 generalized XIO
core (xio_core2.zag, frozen, XIO-GENERAL-COMPLETE commit a36206064).
Per-attack verdicts:

- B1 sclass defeat (output-dead INC cells): **KILL**
- B2 class -1 over-conservatism: **BOUND**
- B3 sclass-difference gate admits a same-type pair: **KILL**
- B4 class-2 stage on a non-sum INC-only graph: **KILL**
- B5 exact A1 rerun against the generalized core: **KILL** (not fixed)

Three kills, one bound. This battery does not rerun H-XIO-4's frozen
kill bars (K1-K8) and does not void XIO-GENERAL-COMPLETE. It bounds the
trust: the generalized core is sound inside its tested envelope
(trial-promoted chain/count/sum families, two-stage compositions) and
unsound outside it, in ways the new machinery itself introduces.

## Method

`xrt_full.zag` = frozen base (`../composition_A/cx_core.zag`, sha256
dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6,
verified before and untouched) + frozen `../xio_general/xio_core2.zag`
(read-only in assembly, never edited) + new red-team driver
`xrt_driver.zag`. Five attack worlds, each a fresh 110656-byte learner.
Hand-built MAPs use the base's own constructors
(t2_lit/t2_guard/t2_set/t2_inc/t2_mov, seq_link, link_edge,
promote_graph) plus one local promote variant (xrt_promote) that
mirrors promote_graph exactly minus the ev_teach_in answer-fact teach,
so hand-built MAPs cannot poison the query relation via activate().
Pure Zag, safebin PATH. 3/3 runs byte-identical, sha256
`5fb0645b5337fa94d1005aef3706da70e1ad68ca578adc6537c9da007ceb102b`
(`xrt_run1/2/3.txt`). Line citations below refer to `xrt_run1.txt`.

---

## B1: sclass defeat -- KILL

**Design.** Hand-build MAP S exactly as the old red-team A1: a chain
graph (guard/set per link) with an INC cell on slot 1 after every set
(a step counter). The INCs are output-dead: the graph outputs slot 0
(the walked node); slot 1 is never read. If xio_sclass is a real
structural signature, a behaviorally-chain MAP must not classify as
mixed.

**Predicted.** sclass(S)=1 (misclassified); worse than the old core,
the new stage dispatch will not merely exclude S but will actively
stage it through the count branch, returning a NUMBER where S
computes a NODE.

**Observed.**
- Line 7: `B1 S=131 sclass=1 oty=1 exec=24 plen=-1 stage=3`. S is
  competent (executes to node 24) and is not even a strict chain
  graph (rb_chain_plen=-1, the old A1 dead zone), yet the new
  dispatch stages it as a counter: stage=3, a NUMBER.
- Line 8 control: `B1 countMAP=44 sclass=1 stage(50)=3`. The count
  branch itself is fine on a genuine count MAP; the dispatch is
  wrong, not the branch.
- Lines 9-11: `PAIRS c0=0 c1=3 c2=0 cm1=0 gated=6 tried=0`,
  `B1 ans=-2 adapters=0`. The true pair (S as chain stage, count MAP
  as count stage) is still killed by the gate, now on sclass
  equality instead of oty equality.

**Why KILL.** The generalization did not repair the proxy; it gave
the proxy a second, more dangerous failure mode. The old core
excluded S from pairing (A1). The new core excludes S AND, whenever
S is admitted cross-class, confidently computes the wrong-typed value
for it. A structural signature that reports "mixed" for a graph
whose INC cells provably cannot affect the output is not a type
system; it is the same INC-presence heuristic with more buckets.

**Honest bound.** The learner's current trial cannot promote a
step-counter chain on its own (chain/count/sum templates only), so
the signature holds on the trial's actual output distribution. The
kill is principled, not live: any future MAP family that uses INC
structurally breaks staging, not just pairing.

## B2: class -1 over-conservatism -- BOUND

**Design.** Hand-build MAP M: a sum graph with a MOVE epilogue
(INC x 8 on slot 1, then MOVE slot0 <- slot1), exactly mirroring the
count family's own epilogue. Behaviorally it is a correct total
function. Structurally the walk sees 8 INC cells plus one MOVE cell.

**Predicted.** sclass(M)=-1 (g==0, ic>0, other>0). The behaviorally
competent MAP fails closed at staging, and the meaningful chain->sum
composition (the PAIR-C shape) becomes impossible.

**Observed.**
- Line 14: `B2 M=13 sclass=-1 oty=1 exec0=8 stage(60)=-999999
  deprel=84`. Behaviorally a correct sum (masked execution gives 8);
  provenance is present (dep relation 84); the type system says
  unknown and the stage fails closed.
- Lines 17-19: the chain MAP promotes normally (chainq=33);
  `PAIRS c0=1 c1=0 c2=0 cm1=1 gated=0 tried=2`. Note the gate
  ADMITS both ordered -1/0 directions (tried=2); both then fail at
  the -999999 stage. The gate is coarser than the staging it guards.
- Line 20: `B2 comp ans=-2 adapters=0`. No wrong answer, no adapter.

**Why BOUND, not KILL.** The -1 path is fail-closed exactly as the
H-XIO-4 report documents (honest boundary 4). No mis-staging, no
wrong adapter, no poisoned state. But the generality claim in that
report ("the discriminators are total over graph structure... any
future trial-promoted family with guards+INC, guard-only, or INC-only
graphs is classified") is overstated in spirit: a one-cell,
ISA-level, count-family-precedented variant of the sum graph is
unclassifiable, so a behaviorally competent MAP family is
permanently excluded from composition on syntactic grounds. The
totality is over 3 of the 16 cell-type subsets, and the strict one
(class 2) is the family the repair was built to serve.

## B3: gate admits a same-type pair -- KILL

**Design.** S as in B1 (class 1, behaviorally a chain over
31->32->33) plus a trial-promoted genuine chain MAP C (class 0).
Plant (2,81,70),(70,81,71): node id 2 collides with the count of the
2-link 81-chain. Query (31,95) with expected 71.

**Predicted.** The sclass-difference gate admits (S,C) (1 != 0)
although both stages are behaviorally chains. xio_try mis-stages S
as a counter (v1=2), feeds the count as a node id into C's chain
stage (v2=71), verifies against the planted expectation, and builds
a wrong-procedure adapter with a clean audit trail.

**Observed.**
- Line 25: `B3 S=14 sclass=1 C=27 sclass=0 execS=33 stageS=2`.
  White-box proof of the mis-stage inside one line: S executes to
  node 33, the stage computes 2.
- Line 28: `XIO-BUILD id=72 m1=14 m2=27 c1=1 c2=0 rel1=81 rel2=81
  qr=95 mid=2 ans=71`. The audit trail claims count->chain; stage 1
  is really a chain. The pair the gate was built to prevent
  (same-type composition) is exactly what got built.
- Lines 31-32: `XIO-REUSE id=72 ans=71`, `B3 reuse41 ans=71`. On a
  fresh subject 41 (chain 41->42->43), the adapter answers 71: the
  answer is determined by the colliding node 2, not by the subject.
  The wrongness is live, not just provenance.

**Why KILL.** Two independent breaks compose: (1) the gate's
syntactic criterion cannot see that S and C denote the same
computation, so it admits the pair it exists to reject; (2) the
mis-staged handoff (a count used as a node id) verifies only
through the integer collision of node ids and numbers, which the
masked stage verification cannot detect. The old oty gate would
also have admitted this pair (both oty 1... no: S oty 1, C oty 0,
admitted too). The new gate was supposed to be the repair; B3 shows
the same-type admission survives the repair whenever the syntax
lies, and now the lie also corrupts the handoff value.

**Honest bound.** S is researcher-constructed; the trial cannot
promote it. The kill is principled: it demonstrates what the gate
criterion means, not what the trial currently feeds it.

## B4: class-2 stage on a non-sum INC-only graph -- KILL

**Design.** Hand-build MAP T: five INC cells on slot 2, no guards, no
MOVE. Structurally INC-only (class 2). Behaviorally the constant-5
function (slot 2 starts 0, output reads slot 2). Give T DEP edges to
84-facts on node 33, then run the PAIR-C-shaped chain->sum query
(31,95) with expected 10.

**Predicted.** sclass(T)=2 licenses the class-2 stage, which never
executes T's graph: it re-derives a sum from T's DEP edges. The
adapter builds on a computation T does not perform.

**Observed.**
- Line 35: `B4 T=11 sclass=2 oty=1 execT(31)=5 execT(99)=5
  stageT(33)=10 C=21 sclass=0`. T is the constant-5 function for any
  input, yet the stage computes 10 for it: the stage procedure never
  consults T's graph.
- Line 38: `XIO-BUILD id=83 m1=21 m2=11 c1=0 c2=2 rel1=81 rel2=84
  qr=95 mid=33 ans=10`. A confident wrong adapter: it denotes
  chain->T, but T's own computation (constant 5) appears nowhere in
  the staged values.
- Lines 41-42: `XIO-REUSE id=83 ans=3`, `B4 reuse51 ans=3`. Fresh
  subject 51 reuses "successfully" with answer 3, derived from 51's
  84-facts through T's DEP-licensed relation. Every reuse is
  confident; none of them involve T.

**Why KILL.** The class-2 dispatch assumes INC-only structure
denotes total semantics. Any straight-line INC graph qualifies,
including constants, and the re-derivation pattern (shared with the
class-0/1 branches) means the MAP's own graph is never executed at
stage time, so nothing can catch the mismatch. The H-XIO-4 report's
honest boundary 2 (same-relation facts outside the intended
aggregate set) understates the problem: the stage does not even
require the MAP to be an aggregate computer. INC-only is a fact
about the frozen ISA's mechanics, not a semantic license, which is
the same architectural smell as the old A1/A6 kills, now inside the
new machinery.

**Honest bound.** T is researcher-constructed. The trial's sum
template emits pure INC graphs, so the dispatch is correct on the
trial's output distribution. The kill targets the dispatch's
principle: re-derivation without ever executing the MAP's graph
cannot distinguish a sum from a constant.

## B5: A1 rerun -- KILL (not fixed)

**Design.** Byte-for-byte the old red-team A1 world (trainY count
MAPs, hand-built step-counter chain S over 21->22->23->24, count
facts, gap, query (21,93)->2), executed against xio_core2.zag, plus
the old control (trial-built chain MAP).

**Predicted.** sclass(S)=1; all three MAPs share class 1; the gate
excludes every ordered pair; the composition fails exactly as in A1.

**Observed.**
- Line 46: `B5 S=131 sclass=1 oty=1 exec=24`. Same node ids as the
  old run (S=131), confirming the world replicates exactly.
- Line 49: `PAIRS c0=0 c1=3 c2=0 cm1=0 gated=6 tried=0`.
- Line 51: `B5 ans=-2 adapters=0`. The composition still fails.
- Lines 58-63 control: `B5c C=138 sclass=0`,
  `PAIRS c0=1 c1=2 c2=0 cm1=0 gated=2 tried=4`,
  `XIO-BUILD id=223 m1=138 m2=44 c1=0 c2=1 rel1=81 rel2=82 qr=93
  mid=24 ans=2`, `B5c ans=2 adapters=1`. The trial-built chain
  composes fine; only the structurally-INC chain is excluded.

**Why KILL.** The question was explicit: does sclass fix A1? No.
The exclusion moved from oty-equality to sclass-equality with the
identical outcome, and B1 shows the new core additionally mis-stages
S where the old core only excluded it. The repair is strictly worse
than the disease for this family.

## Synthesis: what the kills have in common

All three kills are the same architectural smell the first red-team
battery localized, now inside the new machinery: the generalized
core reasons about MAPs through **graph-syntax proxies** (INC-cell
presence for class, guard/INC counts for the gate, DEP-edge order
for the relation, re-derivation instead of execution for the stage)
rather than through **behavioral evidence** (what the graph
computes). B1/B5 show the syntax lies about S; B3 shows the gate
believes the lie and the handoff inherits it; B4 shows the stage
never checks the graph at all. Inside the H-XIO-4 test envelope the
proxies agree with reality, which is why K1-K8 pass. Outside it they
diverge, and the new machinery converts silent exclusion (old core)
into confident miscomputation (new core): B1's stage=3 and B4's
stageT(33)=10 are wrong-typed, wrong-procedure values produced with
no error and no abstention. B2 is the honorable exception: where the
syntax gives up (-1), the core fails closed, which is to its credit,
but the give-up boundary is drawn one ISA cell too tight.

Candidate repairs, in order of leverage:
1. Behavioral stage dispatch: execute the MAP's own graph (or a
   per-family candidate set) and keep what verifies, instead of
   dispatching on syntax. Fixes B1 (mis-stage), B4 (constant staged
   as sum), and B5 (exclusion) at once. This was already repair
   candidate 1 from the first battery; the generalized core did not
   take it.
2. Gate on behavioral type: derive the pairing criterion from what
   stages compute (e.g., probe each MAP once and record
   node-output vs number-output), not from cell counts. Fixes B3's
   same-type admission.
3. Make -1 less conservative by construction: whitelist generic ISA
   cells (MOVE, DEC) in the walk so semantically neutral variants
   classify with their family. Narrows B2's bound.
4. Never re-derive without executing: at minimum, stage_exec could
   cross-check the re-derived value against the MAP's own graph
   execution and abstain on disagreement. Defense in depth for B4.

## Incidental finding (not scored, base executor quirk)

While building B4, a first attempt used INC on frame slot 5 and
observed execT(31)=5 but execT(99)=10: not constant. Root cause in
the frozen base: fr_get/fr_set store slots >= 4 by walking field-4
links, and a fresh frame node's field 4 is 0, so slots >= 4 alias
into node 0's header fields (slot 5 = header field 24, the promo
counter). Any graph using slots >= 4 has ambient write authority
over global header state. Slots 0..3 are the frame node's own
fields and are safe; the final B4 uses slot 2 (execT 5/5,
constant). This is frozen-base behavior, out of this battery's
scored scope, recorded here so no future worker re-discovers it.

## Red-team limitations (honest)

- S, M, and T are researcher-constructed; the current trial cannot
  promote step-counter chains, MOVE-epilogue sums, or constant
  graphs on its own. The attacks target the proxies' principle,
  with live-learner scope stated per attack, as in the first
  battery.
- Worlds are small (hundreds of nodes); nothing here tests scaling.
- Masked xio_try behavior verified only through the stage probes
  and the reuse queries, not by direct masked-composite calls.
- The B3/B4 reuse queries use expected=-2 (no answer check); the
  wrongness demonstrated is procedural (the answer is determined
  by colliding state, not by the subject), not a failed
  verification.

## Standing metrics

- New code: `xrt_driver.zag` (~330 lines), all unfrozen
  driver-level; frozen base + xio_core2.zag byte-untouched
  (assembly by cat; base sha256 re-verified
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6).
- Modes / bridges / handlers / new core semantic cases: 0 / 0 / 0 / 0.
- Capability-source delta of the attacks: zero new capabilities;
  all findings are about the generalized core's trust envelope.
- Determinism: 3/3 byte-identical runs, sha256
  5fb0645b5337fa94d1005aef3706da70e1ad68ca578adc6537c9da007ceb102b.

## Deliverables (all in xio_general_redteam/)

- NAMECHECK.md (toolchain guard Step 0, scope, build log, scorecard)
- REPORT.md (this file)
- xrt_driver.zag (red-team driver, unfrozen, new)
- xrt_full.zag (assembly: frozen base + frozen xio_core2.zag + driver)
- xrt_bin (pinned znc build), xrt_compile.txt (warnings only)
- xrt_run1.txt, xrt_run2.txt, xrt_run3.txt (3/3 byte-identical)

Pure Zag, safebin PATH, zero em/en dashes in worker-authored content
(byte-verified), paper untouched, frozen files untouched, committed
locally with explicit pathspecs, nothing pushed.
