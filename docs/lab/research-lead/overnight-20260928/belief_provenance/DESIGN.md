# DESIGN: Belief Reasoning from Provenance (priority 9)

Worker: BELIEF-PROVENANCE subagent, 2026-10-03.
Status: DESIGN ONLY. No implementation, no build, no runs, no
prereg (nothing was implemented; per lane convention no prereg
is required for analysis-only work). Non-ledger task; nothing
minted.
Lane: docs/lab/research-lead/overnight-20260928/belief_provenance/
Style: hyphens only, no em/en dashes; opaque identifiers for
code entities.

## 0. What this document is

A concrete mechanism design for Micah's overnight priority 9:
belief reasoning from provenance and evidence. It answers the
three assigned questions (what a belief is, how provenance
affects belief, whether beliefs revise when provenance changes)
with data structures, update rules, and falsifiable
predictions. Section 11 separates tested claims (prior lanes)
from reasoned claims (this document).

This design does not replace BP-1 (lane REPORT.md, verdict
BP-1-PASS). It generalizes BP-1's evidential adjudication into
a standing belief layer and absorbs six other prior results
into one mechanism (Section 9).

## 1. Provenance inventory: what is stored today

Survey of the countmap, xhier, and composition lanes. Every
item below is already in learner state in some frozen build;
none of it is currently reasoned about as belief.

P1. Type-1 DEP edges. `promote_graph` writes type-1 edges from
each promoted MAP to its licensing facts: the facts whose
values verified the trial. Read today by `xs5_agg_rel` (which
relation the count MAP licenses) and by `t2_revise_graph`
(which licensing facts went stale). Licensing facts carry
their own relation (field24) and value (field28).

P2. Field8/field4 on MAP nodes. The formation address: field8 =
query subject, field4 = query relation, field20 = graph root,
field28 = answer. Written by `promote_graph` at formation.

P3. Type-14 edges. Two uses. (a) Composite provenance:
`link_edge(W,zm,14,cm,0)` records which nav MAP and which
count MAP a MAP_Z was composed from (read by
`xhier_mapz_agg`, honored by the XHIER-COUNTMAP-FIX patch).
(b) Delivery parent: answer node -> structure (BP-1).

P4. Type-15 edges. Co-use edges written on episode success
(mechanism B, retired into U; revived in BP-1 as
co-consideration winner<->loser edges on adjudication).

P5. Type-16 edges. Combine provenance. BP-1: meta-row ->
winner and meta-row -> loser. The learner's evidential policy
carries provenance.

P6. Source tags. C170: field 16 on tag-1 FACT, values 0
UNKNOWN, 1 OBSERVED, 2 TAUGHT, 3 INFERRED, 4 PREDICTED, 5
REVISED, 6 DERIVED-FROM-STRUCTURE. Partition: EXTERNAL =
OBSERVED/TAUGHT/REVISED, SELF = INFERRED/PREDICTED/DERIVED.

P7. corr/rev counters. BP-1: per-MAP corroboration count
(incremented on confirmed observation) and revision count
(provisioned, always 0 in BP-1).

P8. Meta-table. BP-1: learner-written rows of (wcorr, lcorr,
wmid, lmid, ep) after each resolved conflict; the learned
evidential policy content.

P9. Contract state. C424 contract module: (consumes, produces,
constraint-clauses, confidence) plus per-clause
disconfirmation counters and a contract-level
consecutive-failure run; ops induct/check/grow/invalidate/
revise.

P10. Retirement provenance. grammar_program_gpi3: provenance
kind 3 edges with reason codes on retirement (e.g. reason 2).

P11. Revision machinery. `t2_revise_graph` walks type-1 edges
to find stale licensing facts. Sum lane: the same walk can
structurally touch any MAP's provenance.

What is missing: nothing in the codebase turns P1-P11 into a
graded, revisable commitment. Today a live structure is
trusted implicitly: `xs5_find_countmap` returns it,
`xhier_exec` gates on existence, and the XHIER-COUNTMAP-FIX
K3a control leg showed the sharpest consequence: a composite
whose entire type-1 provenance had been destroyed was still
used to compute an answer (silently, wrong-relation). The
patched build fences per query (-2). Neither build maintains a
persistent, graded belief that weakens as provenance dies.

## 2. What a belief is

A belief is a learner-owned record of commitment to a claim,
distinct from the structure that carries the claim. Structures
are mechanisms (graphs that execute). Beliefs are endorsements
(graded, revisable, evidence-driven). The separation is the
whole design: today "structure is live" and "learner endorses
its claim" are the same bit. They must become two different
facts, because provenance can die while the structure lives
(K3a) and structures can be reformed while old evidence is
stale (tombstone-is-destroy, XHIER-COUNTMAP-FIX Section 2).

Three belief kinds, derived from structure shape (not stored
as a label):

- B-FACT: the claim "(s, r, v) holds" for a tag-1 fact node.
  Grounded in P6 source tags and direct observations.
- B-STRUCT: the claim of a tag-20 MAP, e.g. "count MAP over
  (s, r) yields v". Claim identity read from P2
  (field8/field4/field28 plus executed terminal). Grounded in
  P1 licensing facts and P7 corroborations.
- B-COMP: the claim of a MAP_Z composite. Grounded in the
  beliefs of its components via P3 type-14 edges (belief
  propagates along provenance).
- B-META: the claim of a meta-row (P5/P8): "provenance
  profile X beat profile Y". Meta-beliefs are beliefs too,
  with their own records; this is what makes the evidential
  policy itself revisable (the BP-2 open question).

Conflict is structural: two B-STRUCT/B-COMP beliefs with the
same (field8, field4) and different terminals are in conflict
(BP-1 criteria C1-C4, unchanged).

## 3. The mechanism

### 3.1 Belief record (learner-owned state)

One record per claim-bearing node id, created at formation,
destroyed at tombstone (Section 5, invariant I3). Fields:

- b_sup (u8, 0..255): current support strength.
- b_conf (u8): consecutive confirmation run.
- b_disc (u8): consecutive disconfirmation run.
- b_rev (u8): revision count.
- b_ext (u8): live EXTERNAL licensing facts (P6 partition).
- b_self (u8): live SELF licensing facts.
- d_self (u8, 0..255, fixed-point): learner-owned discount
  applied to self-sourced support. Starts at 255 (no
  discount); learned downward only through experience
  (Section 6).

Effective support for selection:
  eff(mid) = b_sup * (b_ext*255 + d_self*b_self)
             / (255 * (b_ext + b_self))
with eff = b_sup when b_ext + b_self = 0 (no licensing
facts; e.g. taught facts). All arithmetic is structural:
counts, liveness, edge types. No domain content anywhere.

### 3.2 Update rules (generic machinery, frozen form)

R1 formation. `b_form(mid)`: on promote with licensing set L:
b_sup = BASE; b_ext/b_self from P6 tags of L; b_conf = 1
(formation verified once); b_disc = 0; b_rev = 0;
d_self = 255. BASE is a researcher constant.

R2 confirmation. `b_confirm(mid, indep)`: b_sup += INC_HI if
indep else INC_LO (independence discount: confirmation from
a disjoint licensing set counts more than confirmation from
the same set; the C211 Probe-R lesson). b_conf++,
b_disc = 0, saturate at 255. P7 corr is subsumed: corr is
the count of R2 applications.

R3 disconfirmation. `b_disconfirm(mid)`: b_sup -= DEC;
b_disc++, b_conf = 0, floor at 0. P9's per-clause dc
counters and fail runs are the contract-side analogue.

R4 licensing change. `b_relicense(mid)`: recompute live
type-1 targets; let live = live count, formed = count at
R1. b_sup = b_sup * live / formed (proportional weakening;
integer arithmetic). Refresh b_ext/b_self from current
targets' P6 tags. If live = 0, `b_retire(mid, reason=2)`
(provenance-death), writing a P10 kind-3 edge. This is the
graded replacement for the XHIER-COUNTMAP-FIX binary fence.

R5 revision. `b_revise(mid)`: b_rev++; b_sup = b_sup / 2
(the claim changed; old evidence is partially
invalidated); b_conf = 0, b_disc = 0. This makes P7 rev
load-bearing for the first time (BP-1 provisioned it but
never varied it).

R6 propagation. `b_propagate(mid)`: for each live composite
z with a type-14 edge z -> mid: b_sup[z] = min over z's
live type-14 component targets c of b_sup[c]. A composite
is only as trustworthy as its weakest licensed component.
The type-14 graph is the belief-dependency graph; R6 is
belief revision propagating along provenance.

R7 selection. `b_select(cands)`: among live candidates,
pick argmax eff(mid); exact tie at the top, or max eff <
bar, returns -3 (abstain, no commitment; BP-1's
INDETERMINATE, now at the belief layer). bar starts at
researcher constant BAR0 with floor MIN_BAR and is
learner-adjusted: a disconfirmed commitment does bar += 1
(become more cautious); a confirmed commitment with
eff >> bar does bar -= 1. The bar VALUE is learner-owned;
the adjustment rule is disclosed machinery.

### 3.3 Invariants

I1. Belief records are per node id and die with the node.
Tombstone destroys the record; slot recycling gives the new
occupant a fresh R1 record, never an inheritance. This turns
the XHIER-COUNTMAP-FIX v1/v2 slot-recycling lesson into a
design invariant: there is no restore path for beliefs.

I2. Every belief-weakening event writes provenance: R4
writes kind-3 edges on retirement; R5 increments b_rev; R2/R3
adjust b_conf/b_disc runs. The evidential chain stays
white-box auditable (P10 convention).

I3. No selection without support: R7 is the only path from
beliefs to commitment. Existence (node live) never implies
endorsement.

## 4. How provenance affects belief (mapping)

| Provenance (P#) | Belief effect | Rule |
|---|---|---|
| Type-1 DEP edges (P1) | define the licensing set; liveness fraction scales support; total death retires | R4 |
| Field8/field4 (P2) | define claim identity; same (s,r) + different terminal = conflict set for R7 | R7 |
| Type-14 edges (P3) | define the belief-dependency graph; component weakening propagates to composites | R6 |
| Type-15 edges (P4) | mark adjudicated pairs; R2 applies to winner, R3 to loser on resolution | R2/R3 |
| Type-16 edges (P5) | meta-rows get B-META records; their support updates on confirm | R2/R3 |
| Source tags (P6) | set b_ext/b_self; partition weights eff() via d_self | 3.1 |
| corr (P7) | count of R2 applications | R2 |
| rev (P7) | incremented by R5; halves support | R5 |
| Meta-table (P8) | rows become B-META beliefs; the evidential policy is revisable state | R2/R3 |
| Contract confidence/dc/fail-run (P9) | contract-side names for b_sup/b_disc/b_conf; invalidate maps to R3 | R3 |
| Kind-3 retirement + reasons (P10) | written by b_retire; reason 1 = disconfirmation-runout, 2 = provenance-death, 3 = superseded | R4/R3 |
| t2_revise_graph (P11) | triggers R5 + R4 recompute on the revised structure | R5/R4 |

## 5. Belief revision when provenance changes

Four concrete scenarios, each tied to a frozen finding.

S1. Provenance death (XHIER-COUNTMAP-FIX K3a replay). All 4
type-1 licensing targets of MAP_V3 are tombstoned. R4:
b_sup[MAP_V3] scales 4/4 -> 3/4 -> ... -> 0/4, then
b_retire(reason=2) with a kind-3 edge. R6: MAP_Z2's belief
becomes min(...) = 0. R7: MAP_Z2 is never selected again,
persistently, not per query. Current builds: per-query -2
fence (fixed) or silent wrong-relation answer (control).
The belief version is graded (losing 1 of 4 facts weakens
but does not kill) and persistent (retirement is state,
not a gate trip).

S2. Tombstone-is-destroy. MAP_Y is tombstoned. Its belief
record dies with the node (I1). If the slot is recycled by
a new structure, that structure gets a fresh R1 record.
There is no belief-restore path, matching the substrate's
no-restore reality.

S3. Conflict then revision. Two MAPs, same (s,r), different
terminals. R7 picks the higher eff; the world's
confirmation disconfirms the winner: R3, bar += 1. Later
`t2_revise_graph` revises the loser: R5 halves its support
but it stays selectable; subsequent confirmations rebuild
via R2. Revision is evidence, not erasure.

S4. Composite propagation without touching the composite.
Tombstone one licensing fact of composite A's count MAP:
R4 weakens the count MAP, R6 lowers A's belief below rival
composite B, R7 flips selection to B. No edge of A itself
was modified; the flip traveled the type-14 provenance
path. This is the behavior the current architecture cannot
express: today only existence gates change selection.

## 6. Researcher/learner boundary (load-bearing)

Researcher-supplied generic machinery (frozen form,
disclosed): the record schema; R1-R7 rule forms; the
constants BASE, INC_HI, INC_LO, DEC, BAR0, MIN_BAR; the
edge-type semantics (type-1 = licensing, type-14 =
compositional dependence); the min combiner; the abstain
rule; the eff() formula shape.

Learner-owned content (nothing the researcher sets per
world): every b_sup/b_conf/b_disc/b_rev value; b_ext/b_self
counts; the bar value; d_self (the self-source discount);
B-META rows. In particular: no researcher rule says
external beats self. d_self starts at 255 and moves only
when the learner experiences disconfirmed self-sourced
beliefs (the C183 lesson made structural). A learner that
never experiences self-amplification failure keeps
d_self = 255; the FP4 adversarial control checks exactly
this.

Status honesty: this design tests that belief CONTENT is
learned, not that the update rules are learned. The
constants and combiner are machinery in the same sense as
BP-1's argmax-over-counts. Whether the update rule itself
could be learner-revisable is out of scope, as it was for
BP-1.

## 7. Domain-blindness

Every rule references only: node liveness, edge types
(1/14/15/16), integer counts, the P6 external/self
partition (structural, from field 16), and field8/field4
equality. No relation is interpreted; no domain label is
read; no structure identity is matched. Renaming every
relation and entity with an opaque permutation leaves the
belief table and the selection trace byte-identical (FP6).
The 2026-10-03 clarification is satisfied structurally:
beliefs are described by learned properties (licensing
liveness, corroboration runs, source partition, revision
history, provenance graph position), never by human domain
identity.

## 8. Falsifiable predictions

Each is preregisterable as a sealed experiment in the
BP-1/BP-2 style (frozen binary, byte-identical runs,
in-driver white-box checks). Predicted values would be
hand-derived in the prereg.

FP1 graded weakening flips selection. Two candidate MAPs,
same (s,r), different terminals; leader has 4 licensing
facts. Tombstone the leader's facts one at a time.
Predicted: b_sup drops by the exact R4 fraction at each
step and R7 flips to the rival at the predicted step.
Falsifier: flip at a different step, or no flip while
eff stays above the rival.

FP2 provenance-death retires persistently. After all
licensing facts of a structure are tombstoned, the
structure is never selected again for the rest of the run
although its node stays live, and a kind-3 edge with
reason 2 exists on it. Falsifier: any later selection of
the retired structure, or retirement without the edge.

FP3 propagation flip. Rival composites A and B; tombstone
one licensing fact of A's count MAP only. Predicted: R6
drops A's belief below B at the R4-predicted fraction and
R7 flips to B; no edge of A itself was written except the
tombstone. Falsifier: no flip, or a flip at a
non-R6-predicted point.

FP4 learned source discount. Two arms. Arm T first
experiences a self-amplification failure (C170 shape: a
self-inferred majority is wrong); arm C does not. Both
then choose between an external-sourced and a self-sourced
belief with equal b_sup. Predicted: T selects the
external belief (d_self < 255), C shows no systematic
discount (d_self = 255). Falsifier: T shows no discount
(the discount is not learned) or C also discounts
(researcher bias leak).

FP5 independence discount. Six confirmations from one
licensing set vs six from disjoint sets. Predicted:
b_sup differs by exactly the INC_HI/INC_LO ratio
accumulated over six R2 applications. Falsifier: equal
supports (the C211 Probe-R failure mode: repetition
without independence goes falsely confident).

FP6 domain blindness. Opaque permutation of all relation
and entity ids, world otherwise identical. Predicted:
belief table and full selection trace byte-identical.
Falsifier: any byte difference.

FP7 abstention. No candidate above bar. Predicted: R7
returns -3, no commitment, no B-META row written (the
BP-1 K-4 result at the belief layer). Falsifier:
commitment without support.

Kill criterion for the design itself. If a sealed battery
shows that R7's selections always agree with plain
liveness-gating (pick any live candidate), the belief
layer is decorative and must not ship. The design is
vindicated by at least one sealed world where existence
says use-it, belief says refuse, and belief is right.
The S1/K3a replay is the first candidate world.

## 9. Absorption map: what this design does with prior results

- BP-1 (BP-1-PASS): corr becomes R2 applications; the
  meta-table becomes B-META beliefs; -3 abstention becomes
  R7; the STANDARD/REVERSED flip becomes differing
  b_sup histories. BP-1 stays valid as the first
  demonstration; this design is its generalization.
- C211 BELIEF-FORMATION (exploratory): support scores
  become b_sup; PROVISIONAL/UNCERTAIN/CONFIDENT bands
  become the learner-set bar; the independence discount
  becomes R2's indep flag; Probe R becomes FP5.
- C170 PROVENANCE-COMPLETE (exploratory): source tags
  become b_ext/b_self; the external/self partition becomes
  the eff() weighting; the majority-wrong adversary becomes
  the FP4 arm-T experience.
- C183 PROVENANCE-LEARNING (exploratory): learned source
  reliability becomes the learner-owned d_self value; the
  "no hardcoded rank" requirement becomes I-status of the
  d_self initial value (255, unmoved without experience).
- C424 contract module (SUBSUMES): confidence becomes
  b_sup; dc counters and fail runs become b_disc/b_conf;
  invalidate becomes R3; revise becomes R5. The contract
  module keeps its clause structure; beliefs attach to the
  contract node the same way they attach to MAPs.
- t2_revise_graph: becomes the trigger for R5 + R4
  recompute, instead of a structural walk with no belief
  consequence.
- XHIER-COUNTMAP-FIX fences: become graded R4 weakening
  plus persistent retirement. The loud -2 fences stay
  correct as a backstop; beliefs make them rarely reached.
- grammar_program kind-3 + reasons: becomes the
  b_retire edge convention (reasons 1/2/3).

One-system accounting for a future implementation: new
learner machinery = the belief table, R1-R7, eff(), all
generic over claim-bearing nodes. 0 new edge types (1/14/
15/16 and kind-3 reused), 0 new node types, 0 modes, 0
bridges, 0 handlers, 0 semantic cases. Beliefs are
learner-state records, not a subsystem.

## 10. Open questions (not claimed)

- The constants (BASE, INC_HI, INC_LO, DEC, BAR0, MIN_BAR)
  are researcher-chosen; their values are not derived.
  Sensitivity analysis is future work.
- The min combiner (R6) is one fixed form; product and
  weighted combiners are untested alternatives.
- Multi-hop propagation dynamics: type-14 cycles could
  oscillate under R6; needs a fixpoint analysis before
  implementation near cyclic composites.
- Per-belief bars vs one global bar: the design uses a
  global learner-adjusted bar; per-belief bars are more
  expressive and untested.
- B-FACT belief formation leans on C170, which is
  exploratory (no frozen prereg); a belief implementation
  should not cite C170 as canonical.
- Whether the update rules themselves could be
  learner-revisable is out of scope (Section 6).
- Interaction with eviction pressure: belief records under
  memory pressure (which beliefs are forgotten first) is
  unaddressed; b_sup is the natural eviction key, untested.

## 11. What was tested vs what was reasoned

Tested (prior lanes, cited): BP-1 K1-K8 (evidential
adjudication from learned meta-state, 3/3 byte-identical);
XP-COUNTMAP-1 K1-K4 (formation/addressability split);
XHIER-COUNTMAP-FIX K1-K3c (per-composite provenance use,
both loud fences, tombstone-is-destroy); C424 K1-K7
(contract unify, 7/7 bars); C170/C183/C211 (exploratory,
belief-adjacent findings, no frozen preregs).

Reasoned (this document, no implementation, no runs): the
belief/structure separation (Section 2); the record schema
and R1-R7 (Section 3); the provenance-to-belief mapping
(Section 4); scenarios S1-S4 (Section 5); the
researcher/learner boundary (Section 6); the
domain-blindness argument (Section 7); FP1-FP7 and the
kill criterion (Section 8); the absorption map (Section
9); the open questions (Section 10). The predicted values
inside FP1-FP7 are shapes of predictions, not measured
numbers; exact numbers belong in a future prereg.

## 12. Notes for the parent

- No ledger entry: non-ledger task, nothing minted.
- No implementation was built and no code was run, so no
  safebin activation was needed and no prereg was required.
  A future implementation lane needs a frozen prereg with
  hand-derived FP1-FP7 values before any code.
- Commits local on tnn-native-lab only, explicit pathspec,
  never pushed. This DESIGN.md is the only new file.
- BP-1's REPORT.md is untouched; this design generalizes
  it and does not reinterpret its verdict.
- Suggested next step if this design is approved: BP-2 as
  specified in the BP-1 open questions (regime change
  mid-stream), with FP2/FP3 as the provenance-death and
  propagation arms, since S1 already has a frozen world
  (XHIER-COUNTMAP-FIX) to replay against.
