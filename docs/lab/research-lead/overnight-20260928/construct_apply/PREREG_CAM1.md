# PREREG: Construct-and-Apply Mechanism (CAM-1)

Date: 2026-09-30. Worker: Construct-and-Apply Prereg Architect.
Status: PREREG-FROZEN (design only; no implementation in this commit).
Lane: Cluster B construct-and-apply, the major frontier (research director ruling J).

## Step 0 Name-Check

The standing rules from the top of repo-root LOOP_STATE.md that apply:
(1) PURE ZAG ONLY, the literal red line. This task is architecture
design, pure markdown; no code is written, no tooling is invoked, and
no Python is used for any purpose. (2) Shell-only byte checks: the
dash check for the documents below runs via the shell-only
check_no_dash.sh snippet, never python3. (3) No em dashes in loop
documentation: this document uses hyphens only. (4) Commits stay
local, owned paths only
(docs/lab/research-lead/overnight-20260928/construct_apply/),
explicit pathspecs, git status inspected before committing, the
contaminated paper untouched. (5) Preregistration strictly precedes
implementation: this prereg is frozen alone; no implementation may
reference it until reviewed. This paragraph was written before any
design work began.

## The standing question

> Why can the existing general architecture not learn this behavior?

The W2/W3 analysis (2121fd16d) gives the precise answer: the frozen
core implements one retrieval operation, exact-key lookup over stored
triples. It has no regularity detection in the learn() path, no
persistent format for a learner-owned function/procedure object
(the root: nothing to write to, nothing to invoke), and no
application step in query() on miss. Demonstrations are stored;
nothing is ever constructed from them.

## The shared cause, restated as the design target

W2 needs invariance-abstraction: the step->op mapping is constant
across the instance dimension; reify it; bind a novel instance.
W3 needs function-construction-and-evaluation: the addition law
induced from eight exemplars; evaluate it on novel pairs.
Both are: demonstrations -> infer reusable structure -> persist it
-> invoke it on unseen inputs. The mechanism below is ONE
mechanism for both. Per the research director's ruling, W2
procedure abstraction and W3 causal/function construction are
instances of the SAME general capability; a split requires
experimental proof (section "The bar for splitting").

## Design CAM-1: PROPOSE -> VERIFY -> PROMOTE -> APPLY

One loop, four generic structural operations, no domain knowledge.
The loop runs inside the CLA-1 event loop (the primary architecture
per the consolidation ruling): the TEACH step gains PROPOSE and
PROMOTE; the QUERY step gains APPLY on exact-key miss. The MAP
structures live in the learner-owned workspace as ordinary nodes.

### Operation 1: PROPOSE (regularity detection, learn path)

Input: the stored exemplar stream. The propose step performs
exemplar alignment by purely structural criteria, never by domain
labels:

- Group events whose relation-sets match: two events belong to one
  alignment group when they carry the same set of relations over
  different subjects (W2: relations 801..805 over instances 8001,
  8002, 8003; W3: relations 600, 601, 602 over pair subjects 9001..
  9008). No relation id is special; the grouping key is the
  relation-set signature, a generic structural property.
- Within one aligned group, compute field-level regularity
  statistics across group members. Two generic proposal
  generators run over every aligned group:

  P-INV (invariance): for a fixed relation within the group, if
  the object field is constant across all group members, propose
  a constant mapping: MAP(trigger=relation, parameter=varying
  dimension) = constant object. W2 is this case: for relation
  801 the object 9501 is constant across instances 8001..8003,
  so the proposal is MAP(801, instance) = 9501.

  P-DEP (dependence): for a fixed relation within the group, if
  the object field varies across members but is a deterministic
  function of other varying fields of the same member (identical
  input-field tuples always yield identical objects), propose a
  computed mapping whose body is built by finite-difference
  variation analysis (below). W3 is this case: relation 600
  varies, but is determined by relations 601 and 602 of the
  same pair subject.

- Body construction for P-DEP uses successive finite-difference
  analysis, ONE generic mathematical operation, not a library of
  named operators. Across aligned group members, compute finite
  differences of the output field with respect to each input
  field; if the k-th order differences are constant, reify a
  polynomial map of order k with coefficients fitted from the
  exemplars. W3's addition emerges as order 1 in each input
  (dz/dx = 1, dz/dy = 1); FW3's multiplication emerges as order 2
  (d2z/dxdy = 1). The order is DISCOVERED per map, never selected
  from a researcher list. No ADD case, no MUL case, no operator
  menu exists in the source: the only arithmetic in the core is
  generic integer difference/fit/evaluate routines that name no
  domain concept (audited at implementation per guard G1).

- Scope honestly stated: the mechanism claims polynomial maps
  over integer fields (order discovered, coefficients fitted),
  plus constant maps (order 0). Non-polynomial regularities
  (parity, string edits, threshold logic) are out of scope and
  are named as a boundary, not silently absorbed. Generality
  here means one operation covering an open-ended family
  (any order, any coefficients, any fields), not one operation
  covering all computable functions.

### Operation 2: VERIFY (corroboration before persistence)

A proposed map is a CANDIDATE, not knowledge. Verification is
prediction against the teach stream itself:

- The candidate must predict at least K further exemplars in the
  aligned group that were not used in its construction (K is one
  generic constant, identical for W2-class and W3-class worlds;
  guard G3). For P-INV: the constant must hold on the held-back
  members. For P-DEP: the fitted polynomial must evaluate
  exactly on the held-back members.
- A candidate that fails verification is discarded, not
  repaired. No second-chance fitting, no researcher rescue.
- Verification records are workspace content: each corroborating
  exemplar gets a SUPPORTS edge to the candidate node. This is
  the white-box trace of why the map was trusted.

### Operation 3: PROMOTE (reification into persistent state)

A verified candidate becomes a first-class persistent structure:

- Format (CLA-1 workspace node): (type_tag, ref[4], payload[4]).
  The learner assigns the MAP type_tag through first use; the
  core never interprets tags. refs: [trigger-relation,
  parameter-dimension, exemplar-group, reserved]. payload:
  [body-kind (0 = literal, k = polynomial order), coefficient
  slots..., corroboration count, standing].
- The map node links to its supporting exemplars with SUPPORTS
  edges (written during VERIFY) and to the group with an
  INSTANCE-OF edge. Standing starts at the corroboration count.
- Revision without a REVISION_MODE: later contradictory
  evidence creates CONTRADICTS edges and decrements standing;
  when standing falls below the demotion threshold (one generic
  constant), the map is demoted to CANDIDATE and APPLY skips it.
  Queries then revert to -2 rather than serving stale answers.
  This is utility/standing update, the same machinery as the
  CLA-1 utility ledger, not a new mode.

### Operation 4: APPLY (query path, on exact-key miss)

The query path is: exact-key lookup first (W1 behavior preserved
bit-for-bit); on miss, and only on miss, run APPLY:

- Find promoted MAP nodes whose trigger-relation matches the
  query relation and whose parameter dimension can bind the
  query subject (the subject is novel along exactly the
  dimension the map was parameterized over).
- Bind the parameter, evaluate the body: literal return for
  order 0; generic polynomial evaluation over the stored
  coefficients for order k (evaluation is arithmetic on
  coefficients, not a semantic case).
- If several maps apply and disagree, prefer higher standing;
  record which map answered (participation trace for the
  utility ledger). If no map applies, return -2 exactly as
  before.

## Why W2 and W3 are the same operation

Trace both worlds through the four operations:

- W2: PROPOSE aligns instances 8001..8003 by relation-set
  {801..805}; P-INV finds object constant per relation
  (801->9501, 802->9502, 803->9503, 804->9504); VERIFY checks
  the constants against held-back instances; PROMOTE writes
  four order-0 MAP nodes; APPLY binds instance=8004 on query
  (8004, 801) and returns 9501.
- W3: PROPOSE aligns pairs 9001..9008 by relation-set
  {600, 601, 602}; P-DEP finds relation 600 determined by 601
  and 602; finite differences discover order 1 in each input;
  coefficients fit to (1, 1, const 0); VERIFY checks the
  polynomial against held-back pairs; PROMOTE writes one
  order-1 MAP node; APPLY binds pair=9011 on query
  (9011, 600), reads the pair's 601/602 values, evaluates,
  returns the sum.

Same alignment, same propose/verify/promote/apply path, same
MAP node format, same query hook. The ONLY difference is what
the propose step discovers in the field statistics: a constant
(order 0) versus a polynomial dependence (order >= 1). The
order is a discovered payload value, not a code branch: one
format carries both, one evaluator serves both. Invariance is
order-0 dependence. That is the unity claim, stated as
architecture: W2 and W3 differ in the regularity found, not in
the machinery that finds, keeps, and uses it.

## The bar for splitting (what experiment proves they differ)

The unified claim stands until one of the following fires.
Any one of them authorizes, and requires, the split the
research director's ruling contemplates:

- S1 (separable fix): an implementation of CAM-1 reaches 7/8 or
  better on W2-class probes while W3-class remains 0/10 (or
  9/10 on W3-class while W2-class remains 0/8), AND closing
  the remaining gap requires a source-level branch on
  regularity kind: a second propose path, a second map format,
  or a second apply path that cannot share the MAP node
  layout. Separable fixes prove separable causes.
- S2 (format split): the reified MAP format sufficient for
  invariance cannot carry a computed body without adding a
  second persistent format. If literal maps and polynomial
  maps cannot share one node layout and one evaluator, the
  unity claim is false at the representational root.
- S3 (joint-world failure): a sealed world requiring BOTH
  regularities in one stream (constant maps for some
  relations, polynomial maps for others, e.g. the FW8
  induction half) is solvable only with kind-specific tuning
  of the propose or promote bars. If one generic K and one
  generic threshold cannot serve both in one learner, the
  mechanisms are not one mechanism.

Until S1, S2, or S3 fires, no `procedure constructor` and no
`causal constructor` may be built. The burden of proof is on
the split.

## Falsifiable predictions

On sealed W2-class and W3-class worlds, under one frozen
implementation with zero per-world tuning:

- P1 (W2-class): demonstrations of a k-step procedure over N
  instances, probes on novel instances: 7/8 or better answered
  from promoted maps. Zero probe keys ever appear as OBSERVE
  targets in the battery (anti-memorization; verified by grep
  over the battery output; any probe-key teach voids the run).
- P2 (W3-class): 8+ exemplars of a polynomial law, probes on
  held-out subjects: 9/10 or better from the promoted map.
- P3 (fresh adversarial): FW2 (5-step procedure) and FW3
  (integer multiplication) both pass under the same frozen
  binary. FW3 is the discriminator: affine-only fitting and
  operator menus both fail it; discovered order-2 succeeds.
- P4 (no hallucination): W1 stays 10/12 with the 2 composition
  probes at -2. The mechanism must not promote maps where no
  regularity verified; composition is Cluster C, out of scope,
  and APPLY on miss with no applicable map returns -2.
- P5 (negative control): a sealed world with random,
  non-regular mappings across instances (no constant field,
  no deterministic dependence) yields zero promotions and
  all novel probes stay -2. Construction without regularity
  is fabrication; the mechanism must abstain.
- P6 (verification load-bearing): ablating VERIFY (promote on
  first proposal) makes P5 fail: the negative control starts
  producing wrong answers instead of -2. This proves
  corroboration, not proposal, carries the precision.
- P7 (revision): after promotion, a teach stream of
  contradictory exemplars demotes the map (standing below
  threshold via CONTRADICTS edges) and subsequent queries
  revert to -2 rather than serving the stale map. Learning
  continues; no REVISION_MODE is introduced.

## Anti-treadmill guards (frozen)

- G1 (no semantic cases): the source contains no ADD, MUL,
  PROCEDURE, STEP, LAW, CAUSE, or domain case in any form.
  The core's arithmetic is limited to generic integer
  difference, fit, and evaluate routines. Implementation
  review includes a source audit: grep for domain-named
  operations must return nothing.
- G2 (no per-domain constructors): one propose path, one MAP
  format, one apply path. The polynomial order is discovered
  per map and stored as payload; it is never a code branch.
- G3 (one generic bar): the corroboration minimum K and the
  demotion threshold are single constants, identical for
  W2-class and W3-class worlds. Kind-specific tuning is a
  split signal under S3, not a tuning knob.
- G4 (no probe smuggling): probe keys are never observed. Any
  battery in which a probe key appears as an OBSERVE target
  is VOID, not a result.
- G5 (fresh worlds are evaluators): per the architecture
  ruling, FW2/FW3 are adversary assets, not design hints.
  The implementation may not branch on, or be tuned to,
  their surface details (5-step, multiplication). P3 must
  hold because the mechanism is general, which is exactly
  what makes it a test.

## Relation to the other lanes (no duplication)

- CLA-1 (primary architecture): CAM-1 is specified as
  operations inside the CLA-1 event loop and workspace. The
  MAP node is an ordinary workspace node; SUPPORTS edges use
  the standard typed-edge discipline; standing uses the
  utility-ledger machinery. No new store, no new loop.
- LORG ideas (folded per the consolidation ruling): the MAP
  node's survival under memory pressure comes from the
  learner-owned preservation system (utility ledger,
  dependency graph via SUPPORTS edges, protection set), not
  from a separate memory engine. A promoted map protects
  its supporting exemplars through DEPENDS-ON position,
  automatically.
- L3B/L3C (bounded controls, redesign approved): CAM-1 does
  not integrate either mechanism. It answers the same
  frontier from the core's own state: L3B's menu is replaced
  by incremental proposal from the learner's own exemplars;
  L3C v3's cover composition remains the closest in spirit
  (a general operation with no new semantic cases) but
  operates on a different representation for a different
  task. If a future experiment shows cover composition and
  map promotion share a deeper operation, the clusters
  merge per the ruling; until then they stay separate.
- Cluster C (composition) and Cluster D (action): out of
  scope. CAM-1 constructs maps; it does not chain them
  (W9 traversal, W8 grammar) and it does not select actions
  (W6/W7). P4 pins this boundary.

## One-System Rule accounting (prereg; measured at implementation)

- Cognition source lines added: estimated modest (the four
  operations are generic: align, difference-table, fit,
  evaluate, bind). The estimate is directional; the exact
  count is an implementation measurement. The prereg binds
  the direction: net capability from generic operations,
  zero domain knowledge.
- New hardcoded semantic cases: 0 (guard G1).
- New modes: 0.
- New bridges: 0.
- New task-specific handlers: 0 (guard G2).
- Learner-state structures created: MAP nodes,
  SUPPORTS/VERIFY/CONTRADICTS edges, standing counters.
  All ordinary workspace content under the CLA-1 format;
  no new store.

## What this prereg does NOT authorize

- No implementation in this commit. The implementation
  worker builds only after this prereg is reviewed.
- No second propose path, second map format, or second
  apply path unless S1, S2, or S3 has fired and the firing
  is recorded in the ledger.
- No researcher-authored operator library, no COND-style
  case growth, no per-world tuning. Any of these fails K2
  at review.
- The surviving mechanisms are not bridged in; CAM-1 is
  built from the core's own state and event path.

## Kill bars for the implementation (frozen here)

K1: this prereg (frozen alone, before any implementation
commit) completely specifies the four operations, the MAP
format, the unity argument, the split bar S1-S3, predictions
P1-P7, guards G1-G5, and the accounting.

K2: the implementation contains zero per-domain
constructors, zero new hardcoded semantic cases, zero modes,
zero bridges, zero task-specific handlers (verified by source
inspection at review, including the G1 domain-name audit);
one frozen binary passes both W2-class (P1) and W3-class
(P2) sealed worlds; failure on either while passing the
other through a non-general change rejects the unified
claim per S1.

K3: pure Zag plus shell orchestration only; zero Python at
every step; all documents dash-clean via the shell-only
check_no_dash.sh; the contaminated paper untouched; commits
local with explicit pathspecs under construct_apply/ only.
