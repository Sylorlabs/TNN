# LEARNED SIMILARITY: PROBLEM ANALYSIS

**Status:** DRAFT-NOT-FROZEN. Analysis only; no implementation designed or built.
**Date:** 2026-10-01.
**Parent result:** Usability gap `2c4ca4e3a`, section 2.1: "The honest
version of retrieval is LEARNED similarity: the learner discovers which
structural features predict reuse success. No machinery for that exists,
and building it is a research program, not a patch."

This document analyzes what "learned similarity" would require: the
problem definition, why fixed metrics fail, what "learned" means
operationally, and the ranked architectural gaps.

## 1. Problem definition

### 1.1 What structural similarity is (and is not)

**Definition.** Two executable structures are structurally similar iff
they share computational topology independent of surface identity:
independent of literal values, subject/relation namespaces, node IDs,
and allocation order. Topology means the sequence of operation tags,
the branching structure, the arity pattern, the data-flow shape.

Concretely for TNN-2: the A-MAP (node 45, a 4-link chain over subjects
1-5) and the B-MAP (node 89, a 4-link chain over subjects 100-104)
are structurally similar. They differ in every literal and every
namespace token. They agree in tag sequence (101/102 chain cells),
depth (4 links), and data-flow shape (linear chain, each step feeding
the next).

**What it is not:**

- It is not literal equality. The xfer experiment proved exact matching
  is insufficient by construction on disjoint namespaces.
- It is not behavioral equality in the trivial sense. Two MAPs can
  compute the same function with different topologies (e.g., a chain
  vs a sum that happen to agree on one input). Behavioral signatures
  require execution, which is expensive and needs sandboxing.
- It is not provenance equality. The A-MAP and B-MAP have disjoint
  provenance (different (s,r), different facts). Provenance is the
  one thing guaranteed to differ across domains.

**The core tension.** Similarity must be invariant to exactly the
things that differ across domains (namespaces, literals) and sensitive
to exactly the things that transfer (topology, data-flow). The
researcher knows which is which for the xfer pair because the worlds
were designed to be isomorphic. The learner does not get to know.
Any metric that bakes in the researcher's knowledge of "what transfers"
is a benchmark-specific handler.

### 1.2 What it is for

Retrieval, analogy, transfer, and generalization are one capability
(structural comparison) applied four ways:

- **Retrieval (barrier 3, the immediate need).** Given a query Q, rank
  stored MAPs by likelihood of applicability. Input: one problem,
  many candidates. Output: a ranked shortlist.
- **Analogy.** Recognize that a new problem has the same structure as
  an old one, including the mapping between their parts. Retrieval
  plus a correspondence.
- **Transfer.** Retrieval plus rebinding (barrier 4). Similarity
  selects the candidate; rebinding adapts it.
- **Generalization.** Group experiences by structural type. Clustering
  over the same comparison the other three use pairwise.

Solving learned similarity once serves all four. That is why it is
high-leverage, and why getting it wrong (a fixed, tuned metric)
poisons all four at once.

### 1.3 The inputs: the problem-shape gap

A similarity comparison needs two sides. The stored side exists: MAP
graphs are in learner state, describable (however impoverished) by
`t2_sig` or its successors. The problem side does not.

TNN-2 represents a problem as an (s, r) pair. A pair of integers has
no structure. There is no representation of "what kind of problem is
this" prior to solving it. This is a gap independent of the metric:
even a perfect graph-to-graph similarity function cannot do retrieval
if one side of the comparison (the unsolved problem) has no structural
descriptor.

**Candidate problem-shape sources**, in increasing order of
informativeness:

- (a) The local FACT subgraph around (s, r): what `t2_gather` already
  returns. This describes the problem's data, not its required
  computation, but data shape constrains computation shape (a chain
  of facts suggests a chain computation).
- (b) The failed trial trace: which assemblers were tried, which
  rejected, at what cost. This is a behavioral fingerprint of the
  problem ("chain-3 failed, chain-4 is being attempted").
- (c) The uncertainty signature: the T30 node and its context, if the
  read path ever exists (currently theater, per `e0423538a`).

Option (a) is available today. Option (b) is available but never
recorded as a first-class object. Option (c) requires the inquiry
machinery to become real. The problem-shape descriptor is a
prerequisite for retrieval, and defining it is researcher work with
treadmill risk: the descriptor defines what "similar problem" means,
and tuning it to the xfer pair is benchmark-fitting.

## 2. Why fixed metrics fail

### 2.1 The treadmill mechanism, precisely

A fixed similarity metric has three researcher-chosen components:

- **L1, features:** which structural properties are measured
  (tag n-grams, depth, branching factor, literal histograms, ...).
- **L2, weights:** how the features combine into a score.
- **L3, decision rule:** threshold, top-k, ranking normalization.

The treadmill operates as follows:

1. Researcher defines a metric with plausible features.
2. Metric is tested on the xfer pair (or any benchmark).
3. If the A-MAP does not rank first for the B query, the researcher
   adjusts features or weights until it does.
4. The metric now "works," but its parameters encode the researcher's
   knowledge that the benchmark rewards 4-link-chain matching.
5. On a new domain pair requiring different structures, the metric
   fails; the researcher adds features; repeat.

Step 3 is the treadmill step. It is indistinguishable from ordinary
engineering iteration, which is why it is dangerous. The output of
step 4 is functionally a chain-detector: a researcher-authored
mechanism that recognizes the regularity the benchmark rewards.
This is the class Micah's ISA ruling forbids as protected operations
(FIND_POLYNOMIAL_ORDER and kin), applied one level up in the
cognitive architecture rather than the core.

**The signature of treadmill capture:** the metric's features or
weights cannot be justified without reference to the benchmark.
"Depth matters because chains transfer" is benchmark-relative if
chains are what the benchmark contains. A feature justified as
"topology is domain-neutral" is infrastructure; a weight tuned so
that depth-4 outranks depth-3 on the xfer pair is benchmark-fitting.

### 2.2 Is there a principled boundary?

Three properties separate infrastructure from detector. A similarity
metric is honest infrastructure only if all three hold, or if the
fixed portion is justified as domain-neutral with no benchmark tuning:

1. **Target of detection.** Does the metric detect regularities in the
   world (forbidden class) or in the learner's own structures
   (introspection)? A topology metric over MAP graphs is introspective:
   it examines the learner's own constructions, not the environment.
   This is the strongest argument that topology features are
   ISA-adjacent (like READ) rather than detector-class. But
   introspection alone does not prevent treadmill: a metric can be
   introspective and still tuned to the benchmark.

2. **Provenance of parameters.** Are features and weights
   researcher-fixed or learner-revisable? Fixed is researcher-owned,
   full stop. This is the SUF-relevant distinction. A fixed
   topology metric is researcher-owned infrastructure; it can be
   legitimate infrastructure (like the 4-op ISA) but it can never be
   a learner achievement.

3. **Benchmark independence.** Were the parameters tuned to make a
   specific evaluation pass? Any tuning against the xfer pair (or
   any sealed set) converts the metric into a handler for that set.

**The deep honesty.** Even "topology" as a feature family is a
researcher hypothesis: the belief that topology predicts reuse.
That belief might be wrong (perhaps literal patterns predict reuse
better in some domains, perhaps provenance does). A system that
cannot revise this belief cannot learn similarity; it can only
execute the researcher's belief about similarity. The minimal
learned system therefore requires at least L2 (weights) to be
learner-set from experience, even if L1 (features) is
researcher-provided. The researcher must then label L1 as hypothesis,
not truth.

**Boundary verdict:** There is no boundary in the metric's content
that saves a fixed metric. The boundary is in provenance (who sets
the parameters) and revisability (can experience change them).
A fixed metric is always researcher-owned. It can be legitimate
domain-neutral infrastructure, but the "generic" label must be
earned by benchmark independence, not asserted from content.

### 2.3 Case study: t2_sig

The frozen `t2_sig` (lines 511-533 of `tnn2.zag`) records (tag,
literal) per cell for tags 101-104, including literal values for
tags 101/102. This voided the H2 calibration (`72173fe11`): the
prereg required literals excluded, the implementation included them.

For similarity purposes, literal inclusion is fatal, not merely
miscalibrated: a literal-contaminated signature cannot match across
disjoint namespaces by construction. The A-MAP's signature contains
literals 1-5; the B query's namespace is 100-104. No comparison
function over these signatures can find the structural match,
because the signatures differ in exactly the fields that differ
across domains.

A literal-free `t2_sig` (tags only, no literal values) would be the
minimal domain-neutral structural descriptor. It is not learned
similarity; it is the substrate on which learned similarity could
operate. Its absence means the current codebase has no structural
descriptor suitable for cross-domain comparison at all. The
barrier implementation (`d7a62ea34`) stored only the cell count
(`nc`), discarding even the contaminated signature bytes, so the
implemented descriptor is weaker still.

## 3. Defining learned similarity

### 3.1 Operational definition

"Learned similarity" holds iff the retrieval decision satisfies the
SUF-relevant conditions adapted from `7dddf3933`:

1. **Structural decision:** the system selects among candidate
   structures (not just values) based on a computed comparison.
2. **Learner-state read path:** the comparison reads weights,
   utility counters, or feature selections stored in learner state.
3. **Exercised production write path:** experience updates those
   stored values through a path that actually fires in production
   (not test-only, not dead code; cf. theater audit `e0423538a`).
4. **History dependence:** the comparison's outcome for the same
   query differs depending on the learner's experience (fresh vs
   experienced learner retrieve differently).
5. **Ablation:** zeroing or randomizing the learned parameters
   changes retrieval behavior (anti-theater clause).
6. **Non-enumerability:** the effective similarity function is not
   one entry in a researcher-enumerated menu of metrics.

Missing any of 2-5 yields SUF-UNPROVEN for the similarity claim.
Condition 6 distinguishes learned similarity from H3-lite-style
policy-menu selection (choosing among researcher-enumerated metrics
is L1, not learning).

**Minimal bar.** At minimum, L2 (feature weights) must be
learner-set from experience with an exercised write path. L1
(features) may be researcher-provided but must be labeled
hypothesis. L3 (decision rule) may be fixed if domain-neutral
(e.g., "highest score wins" is not benchmark-specific).

### 3.2 Training signal candidates

The central difficulty is the chicken-and-egg problem: the natural
training signal for similarity is reuse success, but reuse requires
similarity to function. Five candidates, with analysis:

- **(a) Reuse success.** When a retrieved structure is adapted and
  verified, upweight the features on which it matched the query;
  when retrieval leads to failed verification, downweight. This is
  the correct signal in the limit. Problem: it requires the full
  chain (retrieval, applicability, rebinding, verification) to
  function at least minimally. Today the chain is entirely absent.
  Chicken-and-egg is binding.

- **(b) Construction co-occurrence.** Structures built for "similar
  problems" should be similar. Circular: "similar problems" is what
  the metric is supposed to define. No independent ground truth.

- **(c) Prediction error on retrieval.** Predict which features will
  matter for the next query; check against verification outcome.
  Requires verification (see 3.4). A variant of (a) with an
  explicit predictive step, which is better (it creates a
  falsifiable expectation) but harder (needs the expectation
  machinery).

- **(d) Exact-match bootstrap.** Start from what works today: exact
  (s,r) reuse (reuse experiment `ea8fc0ac1`). The learner has ground
  truth for "this structure was useful for this query" in the
  exact-match case. Generalize outward: relax one feature at a time
  (same relation, different subject; same topology, different
  literals) and observe whether reuse still succeeds. The
  relaxation schedule is the learned object. This is the most
  promising escape from chicken-and-egg because it starts from a
  working capability and expands its envelope empirically rather
  than positing cross-domain matching from nothing.

- **(e) Contrastive pairs.** Structures that led to successful
  verification vs structures that were tried and rejected, for the
  same query family. The trial loop already generates negatives
  (rejected candidates). Problem: rejections are currently caused
  by fixed-order trial and harness verification, not by similarity
  judgments, so the contrast is confounded.

**Assessment.** (d) is the only candidate with a working starting
point. (a) is the correct asymptotic signal but unusable at cold
start. The honest research program is (d) first: measure how far
the exact-match envelope can be expanded by experience before any
cross-domain claim is made.

### 3.3 Representation candidates

What is the learned object, physically?

- **(i) Feature weight vector.** Learner-state fields, one per
  structural feature, updated by the training signal. Researcher
  defines features (L1 hypothesis); learner sets weights (L2).
  This is L1 parameter learning on researcher features: bounded,
  testable, the honest starting point. Anti-theater: ablation must
  change retrieval ranking.

- **(ii) Fragment utility counters.** The composition-memory
  direction (`19fa59b6f`): fragments carry F-utility. Similarity
  between two MAPs is then shared fragment membership: they are
  similar iff they were built from the same fragments. No separate
  metric is needed; similarity emerges from construction history.
  This bypasses the feature-definition problem elegantly, but it
  relocates the learning to fragment formation (which fragments
  get extracted is the learned object). Unimplemented.

- **(iii) Exemplar memory.** No parametric metric; store past
  (problem-shape, successful-structure) pairs and retrieve by
  nearest match. But "nearest" requires a distance function, which
  is the metric. Relocates rather than solves, unless the distance
  is itself learned (regress).

- **(iv) Graph-valued metric.** The similarity function is itself
  an executable graph in the 4-op ISA (One-System Rule convergence).
  Most general, most difficult. Requires the plan constructor,
  learner-authored procedures, and SUF. This is the asymptotic
  target, not a starting point.

**Assessment.** (i) is the implementable starting point. (ii) is
the most architecturally interesting because it dissolves the
metric into construction history. (iv) is the north-star form.

### 3.4 The verification dependency

Learned similarity is downstream of learner-internal verification,
and this dependency is binding:

- The training signal (reuse success) requires judging whether a
  retrieval was good.
- "Good" currently means "harness `expected` matched" (V1,
  `t2_try_verify`) or "executed without degenerate output" (masked
  branch, which accepts anything).
- If verification is harness-supplied, the learned metric learns
  to predict harness approval. That is supervised learning of the
  researcher's judgment, not autonomous similarity learning.
- The verification-criterion analysis (`c2a48bee6`) found no
  learner-internal verification exists; V2 does not even check
  `out == new_o`.

**Dependency chain:**

```
learner-internal verification -> reuse success signal
  -> similarity weight updates -> learned retrieval
```

Each arrow is a missing capability. Learned similarity cannot be
built before verification exists, because there is no autonomous
ground truth for "this retrieval was correct." Any similarity
work that assumes harness verification is building
researcher-supervised reuse, which the usability gap already
identified as "not transfer."

This is arguably the most important finding of this analysis: the
similarity problem is not self-contained. It inherits the
verification problem, which inherits the criterion problem (K-H2-3,
currently predicted FAIL independent of sealed content per
`8510e327b`).

### 3.5 The composition-memory alternative, noted

If the composition-memory design (`19fa59b6f`) were implemented,
similarity could be operationalized without a learned metric:

- Fragments extracted from execution traces, stored with provenance.
- Two MAPs are similar iff they share fragments (or fragments with
  shared substructure).
- F-utility counters already provide the learner-state weight
  mechanism; "similarity" is then "expected utility given shared
  fragments," which is learned through the same write path.

This does not eliminate the learning problem (fragment extraction
and utility update are their own gaps), but it eliminates the
separate metric-learning problem by grounding similarity in
construction history rather than in a comparison function. It is
worth recording as the alternative path, because it suggests the
metric-learning framing may itself be a researcher imposition:
perhaps learners do not "compute similarity"; perhaps they
"recognize their own past work."

## 4. Gap analysis, ranked by difficulty

**G1. Literal-free structural descriptor (substrate).**
Fix or supplement `t2_sig` to emit topology without literals.
Researcher work, low implementation difficulty. Not learning;
infrastructure. Treadmill risk LOW if pure topology (domain-neutral,
no benchmark tuning). Prerequisite for everything below.

**G2. Problem-shape descriptor.**
A structural description of the unsolved problem, from FACT
subgraph (available), trial trace (available but unrecorded), or
uncertainty state (theater). Researcher-defined with MEDIUM
treadmill risk (it defines "similar problem"). Difficulty HIGH:
the descriptor must be informative before the solution exists.

**G3. Feature weight storage with exercised write path.**
Learner-state fields for weights, updated by experience. The
H3-lite pattern (policy nodes with read and write paths) applies
directly. Difficulty MEDIUM. Anti-theater required: ablation must
change retrieval.

**G4. Training signal from reuse.**
The update rule mapping reuse outcomes to weight changes. Blocked
on the reuse chain functioning (retrieval, rebinding) and on
verification (3.4). Difficulty HIGH. Chicken-and-egg binding
unless the exact-match bootstrap (3.2d) works.

**G5. Cold start / bootstrap.**
Learning similarity before the first successful cross-domain
reuse. Candidate: exact-match envelope expansion (3.2d).
Difficulty HIGH. Unproven; may fail if the envelope does not
generalize (exact matches may teach "identity matters," the wrong
lesson for cross-domain).

**G6. Learner-created features (L1).**
The learner invents structural features, not just weights. This
is representational invention, the primary frontier (L3). Difficulty
VERY HIGH. Not a prerequisite for the minimal bar (3.1), which
allows researcher-provided features labeled as hypothesis.

**Dependency order:** G1 -> G2 -> G3 -> G4 -> G5, with G6
orthogonal (asymptotic). G4 further depends on learner-internal
verification (3.4) and on rebinding (barrier 4), neither of which
exists. The full chain to learned similarity is therefore at
least five missing capabilities deep, two of which (verification,
rebinding) are major research programs in their own right.

## 5. Relation to barriers and ongoing work

- **Barrier 3** is the retrieval problem; learned similarity is its
  honest form. Fixed similarity is the treadmill form.
- **Barrier 1** (broken, `d7a62ea34`) was the correct first step:
  the visibility counters `hg(W,56)`/`hg(W,60)` now provide the
  diagnostic vocabulary ("visible but unreferenced") against which
  any future retrieval mechanism will be measured.
- **H2 (void, `72173fe11`):** the t2_sig calibration failure is
  directly relevant. The signature function is the closest thing
  TNN-2 has to a structural descriptor, and it is literal-
  contaminated. Any similarity work inherits this defect until G1
  is addressed.
- **H3-lite:** policy nodes are the template for G3 (weight storage
  with write paths), but H3-lite moves procedure selection, not
  similarity weights. Do not conflate.
- **Composition memory (`19fa59b6f`):** the alternative path (3.5).
  If pursued, it may dissolve rather than solve the metric problem.
- **Verification criterion (`c2a48bee6`, in progress at time of
  writing):** the binding dependency (3.4). Similarity learning
  without learner-internal verification is supervised, not
  autonomous.
- **Theater audit (`e0423538a`):** any similarity weight without an
  exercised write path and ablation-tested read path is theater
  by the same standard applied to MISS_POLICY and P-INV.

## 6. Explicit non-claims

- This analysis does not design a similarity metric, learned or
  fixed. No features are proposed as the right ones; no weights,
  no decision rule.
- It does not claim learned similarity is near. The dependency
  chain is five deep, including two major missing capabilities
  (verification, rebinding).
- It does not claim the composition-memory alternative works; it
  is unimplemented, and its own gaps are recorded in its design
  document.
- It does not establish SUF, L3, C0-D, or any transfer capability.
  Researcher-owned structural decisions in this analysis: 0.
  Learner-owned: 0. This is analysis, not mechanism.
- The "principled boundary" (2.2) is a proposal, not a ruling.
  Micah's ISA ruling governs the protected core; the extension
  to cognitive-architecture metrics is this analyst's reasoning
  and should be treated as argument, not doctrine.

## Verdict

**LEARNED-SIMILARITY-COMPLETE.** The problem is defined (1),
the fixed-metric failure mode is characterized with a precise
treadmill mechanism and a proposed principled boundary (2), the
operational meaning of "learned" is specified with SUF-compatible
conditions (3.1), training signals and representations are
enumerated with the chicken-and-egg problem made explicit
(3.2-3.3), the binding verification dependency is identified
(3.4), the composition-memory alternative is recorded (3.5), and
six gaps are ranked with dependency ordering (4). The central
architectural finding: learned similarity is at least five missing
capabilities deep and inherits the verification problem; the most
promising near-term path is the exact-match bootstrap (3.2d),
and the most promising structural alternative is grounding
similarity in fragment construction history rather than in a
comparison function.
