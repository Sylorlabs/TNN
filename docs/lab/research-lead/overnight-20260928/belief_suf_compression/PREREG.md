# PREREG: BELIEF-SUF-COMPRESSION analysis criteria

Worker: BELIEF-SUF-COMPRESSION subagent, 2026-10-03.
Status: FROZEN. Committed before any analysis artifact.
Lane: docs/lab/research-lead/overnight-20260928/belief_suf_compression/
Style: hyphens only, no em/en dashes. Opaque identifiers.

## 1. Objective

Micah's overnight priority 10: architecture compression. Determine
whether the belief layer (BELIEF-PROVENANCE through BP-8) and L3-SUF-1
resolution records duplicate each other, whether one subsumes the
other, or whether they are fundamentally different mechanisms. If they
duplicate: propose the compressed mechanism (design only, no
implementation). If they do not: explain why, with concrete divergence
examples. This is analysis, not implementation. No code of either
mechanism is modified.

## 2. Frozen inputs (what is being compared)

BELIEF side (read, not modified):
- belief_provenance/DESIGN.md: belief record schema
  (b_sup, b_conf, b_disc, b_rev, b_ext, b_self, d_self),
  rules R1-R7, eff() selection, invariants I1-I3, scenarios S1-S4,
  falsifiable predictions FP1-FP7, absorption map, open questions.
- belief_provenance/REPORT.md (BP-1-PASS): evidential adjudication.
- belief_provenance_8/REPORT.md (BP-8-PASS): multi-channel absorption
  (per-channel, not per-edge; saturation; order-sensitivity),
  12-cycle fixpoint (min-convergence on homogeneous type-14 ring,
  idempotent), heterogeneous ring (type-1/type-3 edges cut the ring
  into type-14 reachability components; weakening behind a cut is
  reabsorbed).

SUF side (read, not modified):
- l3_suf_intermediate/L3_SUF_DESIGN.md: resolution record
  (RESOLVED(v) / UNRESOLVED / FALSIFIED-ALL per element),
  sole-survivor principle at three scales (element: predict only
  sole-surviving elements, ABSTAIN on UNRESOLVED; form: adopt a form
  only if sole survivor, FALSIFIED-ALL escalates via generic
  operators; reuse: THIS-world re-verification before COMMIT on
  kb-loaded forms), consequence logging as the evidence channel,
  ABSTAIN as protocol message.
- l3_suf_intermediate/PREREG.md: MAY (a)-(f) source machinery,
  MAY-NOT list, world protocol.
- l3_suf_intermediate/REPORT.md (builder BUILD-PASS on DEV): DEV
  battery results, handoff state.

## 3. Definitions (frozen; these adjudicate the verdict)

DUP (duplication): mechanisms M1 and M2 duplicate iff all three hold:
(a) state inter-derivability: there is a structure-preserving map
between M1's records and M2's records that preserves every
decision-relevant distinction (no distinction one mechanism acts on
is invisible to the other);
(b) dynamics commutation: under that map, the same evidence stream
drives both mechanisms to decision-equivalent states;
(c) decision coincidence: on the same scenarios, both mechanisms take
the same actions (predict / abstain / refuse / escalate / retire).

SUB (subsumption of M2 by M1): M2's state is a function of M1's state
(M2's distinctions are a coarsening of M1's); M2's updates are a
restriction/special case of M1's updates; every decision M2 makes, M1
makes identically on the same evidence; deleting M2 loses no
decision-relevant capability. Subsumption is directional and must be
demonstrated, not asserted from surface similarity.

NON-DUP (non-duplication): at least one concrete divergence scenario
in which the two mechanisms, fed the same world events, take different
decisions, where the difference traces to a structural cause: different
record subjects, different update algebras, different evidence inputs,
or different action vocabularies. One clean divergence suffices; two
are preregistered below (cross-failure tests).

PARTIAL: named shared design patterns or shared substrate opportunities
that do not meet DUP/SUB. Partial overlap is reported honestly but does
not license merging the decision logic.

## 4. The steelman duplication mapping (what DUP would have to look like)

The surface mapping the task invites, stated precisely so it can fail:
- RESOLVED(v) = high b_sup on the structure carrying the form;
- UNRESOLVED = low b_conf / low b_sup (weak endorsement);
- FALSIFIED-ALL = b_sup = 0 (no support);
- SUF ABSTAIN on UNRESOLVED = R7 returning -3 (max eff below bar);
- form-scale sole-survivor adoption = R7 argmax selection among
  candidate forms;
- form-scale FALSIFIED-ALL escalation = b_retire (reason 2/3).

For DUP, each line must survive sections 5-6. The preregistered
expectation is that they do not, for structural reasons named in
section 5.

## 5. Decision procedure (frozen)

D1 record subjects. Belief records attach to claim-bearing nodes
(B-FACT/B-STRUCT/B-COMP/B-META: facts, MAPs, composites, meta-rows).
SUF resolution records attach to elements (query elements: pairs /
triples) of the learner's own constructed form. Test: can one
mechanism's subject be expressed in the other's terms without adding
a new record kind? Belief has no per-element-of-a-form records; SUF
has no per-claim endorsement records. If neither direction is
lossless, DUP fails at D1.

D2 update algebras. Belief: accumulative bounded-integer runs
(R2 +INC / R3 -DEC with saturation, R4 proportional scaling on
licensing liveness, R5 halving on revision, R6 min-propagation along
type-14, per-channel absorption with saturation per BP-8).
SUF: falsification-elimination of per-element surviving value sets
(set difference driven by the consequence log; state is a set, not a
scalar; no runs, no propagation, no saturation). Test: is there a map
from surviving sets to (b_sup, b_conf, b_disc) preserving the
decisions? A set of 3 survivors vs a set of 2 survivors vs 1 survivor
must map to distinct belief states that drive distinct actions; and
belief run-counters (b_conf=5 from one licensing set vs from five
disjoint sets, cf. FP5) must map to distinct resolution states. If the
map loses a decision-relevant distinction in either direction, DUP
fails at D2.

D3 cross-failure tests (home-turf scenarios; frozen predictions):
- T-A (RK-B world, belief-layer only): the learner induces a form;
  evidentially unseen elements are filled by a tie-break at full
  confidence; heldout rejects them. Predicted: the belief layer does
  NOT prevent the confident-wrong commit. Reason: beliefs attach to
  the structure's claim as a whole; the fabrication is interior to
  the endorsed claim; no TEST disconfirms it (R3 never fires), no
  licensing fact dies (R4 never fires); b_sup stays high and R7
  selects. If analysis finds an R1-R7 path that refuses, the
  NON-DUP claim weakens.
- T-B (K3a/S1 world, SUF only): all type-1 licensing facts of a
  composite's components are tombstoned; no TEST or stakes outcome
  touches the composite's elements. Predicted: SUF records do NOT
  degrade. Reason: the consequence log records TESTs and stakes
  outcomes per element; licensing-fact tombstones are not
  consequence-log events; surviving sets are unchanged; RESOLVED
  elements keep predicting. If analysis finds a SUF path that
  degrades the marks, the NON-DUP claim weakens.

D4 action vocabularies. Belief actions: select argmax eff, abstain -3
when max eff below a learner-adjusted global bar, retire persistently
on provenance death, propagate weakening along type-14. SUF actions:
predict only RESOLVED elements, ABSTAIN per UNRESOLVED element,
escalate the form on FALSIFIED-ALL (try operators in fixed order),
defer with DATA-UNTRUSTED on kb-loaded forms lacking THIS-world
evidence, target probes at UNRESOLVED elements. Test: do the abstain
triggers coincide? (R7's -3 fires on low max support across peer
candidates; SUF's ABSTAIN fires per element on non-sole-survival.)
Does b_retire coincide with form-scale FALSIFIED-ALL? (retire is
terminal; escalation expands the hypothesis space: opposite
directions.) If triggers and directions differ, DUP fails at D4.

D5 verdict rule. DUP iff D1-D4 all show lossless inter-derivability
and decision coincidence. SUB(M2 by M1) iff D1-D4 hold in one
direction only and the subsuming side needs no new machinery for the
subsumed side's decisions. Otherwise NON-DUP, with PARTIAL overlaps
reported separately. A verdict of NON-DUP must name the exact
structural cause of each divergence (not a parameter difference).

## 6. Computational verification plan (pure Zag, safebin)

A small toy model (model/bsc.zag) implementing the two decision
logics at their documented granularity, run under the safebin PATH:
- belief side: scalar b_sup with R1 formation, R2 confirmation,
  R3 disconfirmation, R4 proportional weakening on licensing death,
  R7 select/abstain against a bar;
- SUF side: per-element surviving-value bitmasks with
  falsification-elimination, RESOLVED/UNRESOLVED/FALSIFIED-ALL
  derived as surviving-set cardinalities, element-scale
  predict/ABSTAIN rule.
Two scenarios, mirroring D3:
- S-A (T-A analogue): unseen element filled by tie-break, no
  disconfirming TEST, no licensing death. Frozen prediction: belief
  selects (b_sup high, above bar); SUF abstains (surviving set size
  > 1, UNRESOLVED). Divergence: belief commits, SUF abstains.
- S-B (T-B analogue): RESOLVED element, then all licensing facts
  die, no TEST events. Frozen prediction: belief refuses (R4 drives
  b_sup to 0, R7 abstains); SUF keeps predicting (surviving set
  unchanged). Divergence: belief refuses, SUF predicts.
Determinism: 3/3 runs byte-identical, sha256 recorded. The model is
a decision-logic comparison, not an implementation of either
mechanism; no mechanism source is touched. If the model contradicts
a frozen prediction, the prediction (not the verdict rule) is
re-examined first: the designs' text governs.

## 7. What does not count

- Surface vocabulary overlap ("confidence", "abstain", "support",
  "evidence") without shared decision logic.
- The shared design pattern (epistemic state distinct from structural
  existence) as evidence of mechanism duplication; it is a pattern,
  reported under PARTIAL.
- Hypothetical future extensions ("beliefs could be extended to
  per-element records"); the comparison is of the frozen designs.

## 8. Deliverables

- NAMECHECK.md (this lane; Step 0 recorded).
- PREREG.md (this file; frozen).
- model/bsc.zag + model/build.sh + model/runs/ (3/3 byte-identical
  outputs + sha256).
- ANALYSIS.md: verdict per section 5, divergence examples, partial
  overlaps, and either a compressed-mechanism design (if DUP/SUB) or
  the structural non-duplication argument (if NON-DUP).

## 9. Commit order self-check

This PREREG.md is committed alone (with NAMECHECK.md) strictly before
any analysis artifact exists. The model code, model outputs, and
ANALYSIS.md are created only after the prereg commit lands. The
commit hashes are recorded here after the fact: prereg commit
<filled at commit time>; analysis commit <filled at commit time>.
