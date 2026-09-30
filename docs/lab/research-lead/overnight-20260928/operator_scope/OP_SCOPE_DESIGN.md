# Operator/Scope Representation Design (R1-R4)

Design-only document. No implementation performed. No empirical claims made.
Response to SEG_REVIEW2 (commit 842638d15), which fired the
architecture-review trigger after DEVANG-H1 BUILD-FAIL (4c753a9db).

## 0. Status and non-goals

- This document designs the R1-R4 operator/scope representation for a
  future builder, who must preregister separately against R4 before
  implementing anything.
- H2 is explicitly excluded. H2 (predictive boundary discovery /
  segmentation adaptivity) targets the segmentation representation;
  SEG_REVIEW2 sections 2-4 show segmentation is not the binding
  constraint (atomic "not" under three regimes, is_negator=0,
  T1 0/3). Building H2 would be a third hypothesis aimed at a
  non-binding constraint. This design does not implement, extend,
  modify, or presuppose H2, and it leaves the segmentation subsystem
  untouched except through its existing unit-output interface.
- No L3 claim is made or implied. The discovery criterion, the span
  combiner, the record structure, the signature family, and all frozen
  constants are researcher-authored machinery. What the learner
  creates: the operator inventory (which forms are triggers), the
  per-context records, and the routing bindings. Bounded L2 direction.

## 1. The representational gap (from SEG_REVIEW2)

Three specific ways the operator/grounding representation is wrong:

(a) Single-primary grounding. Each word carries one primary
consequence feature, learned across affirmative and negated episodes
alike. Negated contexts contaminate the primary. The only fix in the
lineage is the researcher-authored "skip grounding after not" rule: a
dedicated semantic case keyed on a word identity. It fails when "not"
itself fragments, it cannot generalize to an undiscovered operator,
and it is exactly the kind of pre-training semantic branch that the
mandate's C0-A would kill on sight.

(b) Pair-statistic operator detection. "not" earns is_negator=1 only
when ("not", X) pairs show X's primary violated at a 70% rate, where X
must be a clean single segment with a correct primary. In NEG episodes
with novel words, X is fragmented and its primary is polluted, so the
detector's preconditions are unsatisfiable exactly in the episodes
where the operator is active. The detector tries to learn a semantic
operator from surface adjacency statistics.

(c) Operator as word flag. The ontology contains words, consequence
features, and adjacency. It contains no scope object and no
interpretation-function object. But "not" IS a function over
interpretation: it maps the consequence prediction of its scope span.
An ontology without scope cannot represent an operator as what it is;
it can only approximate it as a flagged word plus statistics over
neighbors.

Falsifier (b) from the prior review has now fired twice: T1/T3 fail
despite correct segmentation of "not" under two independent regimes.
The binding constraint is representation-side, not segmentation-side.

Design principle: represent "not" as what it is, a scope-taking
operator over interpretation, with the operator inventory and its
semantic effect living in learner-created persistent state, and with
no word-specific branches anywhere in the learner source.

## 2. R1: Compositional interpretation over spans

### 2.1 Units and spans

- The learner receives a segmentation of each utterance into an
  ordered unit sequence U = [u1 ... un]. The segmentation mechanism is
  orthogonal; this design consumes its output through the existing
  interface and specifies nothing about it.
- A span is a contiguous subsequence of U. Two spans matter: REST
  (units before the trigger) and SCOPE (units after the trigger).

### 2.2 Records

- Every unit form has a DEFAULT grounding record: a feature-count
  vector over the consequence-feature vocabulary, learned by the
  learner's existing per-unit counting update. The counting update
  itself is unchanged; only the routing of updates changes (see R3).
- Every unit form additionally has one OPERATOR-CONTEXT record per
  installed operator O: record(u, O). Initially empty.
- The consequence-feature vocabulary and the counting rule are
  pre-existing machinery, unchanged.

### 2.3 The operator record (OPREC)

Persistent learner-created state. One OPREC per discovered operator:

- trigger_form: the unit-form id bound at discovery (a runtime value;
  never a source literal).
- scope_rule: REST_OF_UTTERANCE (frozen for v1; the generic family
  {NEXT_UNIT, REST_OF_UTTERANCE} is documented, v1 freezes one member;
  scope-rule learning is future work).
- signature: the discovery signature that proposed it (v1: DELETION;
  the signature family is frozen researcher machinery, section 3.2).
- support: number of residual events behind the proposal.
- created_at: episode index of installation (must be > 0 for F1's
  "created after experience" check).
- Table cap: 8 operators (frozen; disclosed).

### 2.4 Interpretation function

```
interpret(U):
  O = first operator in table whose trigger_form occurs in U, else NONE
  if O is NONE:
    return UNION over u in U of record(u, DEFAULT)
  i = index of O.trigger_form in U       # first occurrence, frozen tie-break
  rest  = U[0 .. i-1]
  scope = U[i+1 .. n-1]                  # REST_OF_UTTERANCE
  # The trigger unit contributes no default vector while its operator is
  # active: its contribution IS the operator application. Uniform over
  # all discovered operators; not word-specific.
  return (UNION over u in rest  of record(u, DEFAULT))
       UNION (UNION over u in scope of record(u, O))
```

- UNION (bitwise OR over feature vectors) is the frozen generic span
  combiner. It is researcher-chosen machinery, disclosed; it matches
  the world's additive feature semantics. Learning the combiner is out
  of scope for v1.
- With no operators installed, interpret reduces exactly to the
  pre-existing baseline. The design degrades gracefully.

### 2.5 What is generic vs what is learned

Generic (researcher-authored, frozen): spans, UNION combiner, OPREC
structure, scope_rule family, signature family, routing by OPREC, all
constants in 3.7.

Learned (learner-created persistent state): the operator inventory
(which forms are triggers), every record vector, the support counts.
No word-specific branch exists in the learner source (see F3).

## 3. R2: Operator discovery from systematic prediction residuals

### 3.1 Residual events

After burn-in, for each training episode with units U and observed
target T (a feature set):

- Baseline prediction P0 = UNION over u in U of record(u, DEFAULT).
- If P0 == T: no residual; routine updates only.
- If P0 != T: for each position i with candidate trigger form W=U[i]:
  - scope = U[i+1 ..], rest = U[0 .. i-1]
  - scope_pred = UNION of record(u, DEFAULT) for u in scope
  - rest_pred  = UNION of record(u, DEFAULT) for u in rest
  - Record a residual event for W:
    (scope_pred, rest_pred, T, scope_forms).

### 3.2 The DELETION signature (frozen v1 signature family)

signature_match(W, event) iff all of:

  (a) scope_pred is nonempty,
  (b) rest_pred is a subset of T (the non-scope part is correctly
      predicted; the residual is localized to the scope),
  (c) (scope_pred minus T) is nonempty (at least one scope-predicted
      feature is absent from the target).

Rationale: the signature detects "the scope's predicted features
systematically fail to appear", the observable footprint of a
deletion operator. It mentions no word and no negation; any form
exhibiting the footprint is a candidate. INVERSION and SHIFT
signatures are documented extension points, not v1.

### 3.3 Trigger eligibility (anti-confound)

A form W is eligible for operator candidacy only if:

  (e1) W occurs in at least N_ep episodes (recurrence; frozen), and
  (e2) |record(W, DEFAULT)| <= Fmax features (frozen; W itself
       predicts little or nothing).

Rationale: without (e2), content words preceding an operator ("tak"
in "tak not red") accumulate signature-matching events and would be
proposed as spurious triggers. An operator is a form that
systematically modulates other words' predictions without predicting
much itself. This is a property of learned records, not a word list,
and it is what keeps the discovery from re-creating pair statistics
under a new name.

### 3.4 Proposal check (every E episodes after burn-in B0)

For each eligible W:

- support = number of residual events for W; require support >= N.
- consistency = fraction of W's events with signature_match;
  require >= C.
- scope diversity = number of distinct unit forms ever appearing in
  W's matching scopes; require >= K. This bars phrase memorization:
  the footprint must recur across varied scope content, the opposite
  of pair-statistic learning.
- Gate (falsifiability): over all episodes seen so far compute
    correct_sig  = episodes where sig_predict(W) == T
    correct_base = episodes where baseline P0 == T
  where sig_predict(W) for a W-containing episode = rest_pred (the
  deletion signature's zero-parameter prediction: the scope
  contributes nothing), and = P0 for episodes without W.
  Propose O for W iff correct_sig > correct_base (strict).
- If proposed: OPREC = {trigger_form: id(W),
  scope_rule: REST_OF_UTTERANCE, signature: DELETION,
  support, created_at: now}.

Rationale for the gate: it uses no fitted parameters, so an
improvement cannot come from memorization; it must come from the
hypothesis being right. It discriminates true triggers from
positional confounds: for a spurious content-word candidate, the
signature prediction drops real content and the gate fails.

### 3.5 Installation: re-grounding (anti-contamination)

On proposal acceptance:

  1. Replay stored episodes: rebuild every record(u, DEFAULT) from
     non-O-active episodes only.
  2. Build record(u, O) for all u from O-active episodes via the
     router (section 4).
  3. Install the OPREC.

This removes the pre-discovery contamination of default records by
operator-active episodes, which is exactly wrong (a) in the review.
Episode storage for 100 episodes is within budget (disclosed,
section 7).

### 3.6 Retirement

Every E episodes, re-run the gate for each installed operator against
all seen episodes; retire (remove OPREC, stop routing; records
retained but unused) if the gate no longer favors it. Specified here;
the frozen battery does not test retirement (disclosed).

### 3.7 Frozen constants (proposed; the builder's prereg freezes them)

| Constant      | Proposed | Meaning                                    |
|---------------|----------|--------------------------------------------|
| B0 burn-in    | 20       | episodes before first discovery check      |
| E interval    | 10       | discovery/retirement check cadence         |
| N_ep recur    | 5        | min episodes containing W                  |
| Fmax elig     | 1        | max features in record(W, DEFAULT)         |
| N support     | 4        | min residual events for W                  |
| C consistency | 0.75     | min signature-match fraction               |
| K diversity   | 3        | min distinct scope unit forms              |
| OPMAX         | 8        | operator table cap                         |

## 4. R3: Scope-conditioned grounding

### 4.1 Records per context

Each unit form keeps record(u, DEFAULT) plus record(u, O) per
installed operator O. Contexts are exactly the discovered operator
set; there is no other context inventory.

### 4.2 Routing rule (replaces "skip after not")

For an episode with active operator O (trigger at position i):

- units before i: update record(u, DEFAULT) with T (standard counting
  update, unchanged).
- units after i (scope): update record(u, O) with the residual target
  R = T minus rest_pred, where rest_pred uses DEFAULT records of
  pre-trigger units (section 4.3).
- the trigger unit: no record update while its operator is active.

For episodes with no active operator: all units update DEFAULT
records (unchanged behavior).

The routing predicate tests OPREC.trigger_form_id, a
runtime-discovered value. No branch in the learner source mentions
any word identity. This is the C0-A-relevant property audited by F3.

### 4.3 Why residual attribution

Under a deletion operator, a scope word's correct contribution is the
empty set, but naive co-occurrence counting would learn the subject's
features (e.g. record(red, O) would become {tak}). Updating scope
records with R = T minus rest_pred attributes to the scope only what
the rest does not explain. Under deletion this converges to {}; the
mechanism is generic credit assignment, not negation-specific code
(disclosed as researcher-authored machinery).

### 4.4 Worked walkthrough (illustrative, not empirical)

Training sees "tak red" -> {tak, red}; "tak not red" -> {tak};
"blu box" -> {blu, box}; "blu not box" -> {blu}; and so on.

- "not" recurs and predicts nothing itself: eligible under 3.3.
- Residual events for "not": scope_pred={red}, rest_pred={tak},
  T={tak}: signature matches. Across varied scopes ("not red",
  "not box", ...), the support, consistency, and diversity bars are
  met.
- Gate: sig_predict deletes the scope, giving {tak} == T on negated
  episodes, while baseline gives {tak, red} != T.
  correct_sig > correct_base: propose, install, re-ground.
- T3 ("not W", W familiar affirmatively but never negated): O is
  active; record(W, O) is empty, so W contributes {}; prediction =
  rest, and the target lacks W's features: pass. The operator's
  functional role generalizes to a word never seen under negation.
  Pair statistics cannot do this by construction.
- T1 ("tak not grn", grn rare or novel): same mechanism; the novel
  scope word contributes {} under O, which is exactly correct under
  deletion semantics.

## 5. R4: Frozen falsifiers F1-F5 (operationalized for the builder)

Battery: the frozen DEVANG battery (seed 123456789; 100 train
episodes, one-pass online; 20 test utterances). All runs 3/3
byte-identical, pure Zag. "Pass" per item = predicted feature set
exactly equals target feature set.

- F1 (T1 NEG-novel): all 3 frozen T1 items pass AND the result
  includes a white-box dump of the operator table showing an OPREC
  whose trigger_form resolves (via the committed lexicon dump) to the
  "not" unit, with signature=DELETION, created_at > 0, and
  support >= N. Rationale: the operator record is present in
  persistent learner state, bound to the "not" form, created after
  experience.

- F2 (T3 scope-shift): the frozen T3 item(s) pass. Rationale: the
  operator role generalizes to a word never seen under negation;
  pair-statistic mechanisms cannot pass this.

- F3 (source audit): in committed learner source (learner .zag
  files; explicitly excluding world, harness, and test-data files,
  whose paths the prereg lists): grep for the byte string "not"
  returns 0 hits; grep -i for "negat" and "is_negator" returns
  0 hits; the routing predicate references only
  OPREC.trigger_form_id, confirmed by an inspection note in the
  result doc. The builder pastes verbatim grep output. Any hit
  fails F3.

- F4 (ablation): from the trained persistent state, produce an
  ablated copy with the operator table emptied (routing disabled;
  records otherwise intact); re-run frozen T1 with no further
  learning. Pass iff T1_ablated < T1_full (strictly worse; expected
  0/3). Additionally re-run the full 20-item test under ablation and
  report per-item scores: the drop must be localized to negation
  items (T1/T3), not a global collapse.

- F5 (floors): test accuracy >= 16/20 AND K6 SIZE = 3/3 (DEVANG4
  levels: meet or beat the 16/20 baseline without regressing SIZE).

Falsifier interaction: if F1 fails while F3 and F4 pass (an operator
is found, it is causal, but T1 still fails), the review's specified
next target is signal sparsity (one target per utterance), not the
representation. If F2 fails while F1 passes, the scope-generalization
claim fails and the design's core value proposition is void.

## 6. Interaction with segmentation

None beyond the existing unit-sequence interface. This design neither
implements nor requires any segmentation hypothesis (H1, H2, H3, H4,
or other). Whatever units the segmenter emits, the operator machinery
consumes. Segmentation errors remain the segmenter's failures,
measurable independently of this design.

## 7. Limitations and honest scope

1. Single active operator per utterance (first trigger wins; frozen
   tie-break). Nesting ("not not red") is out of scope for v1.
2. Scope rule frozen to REST_OF_UTTERANCE; scope-rule learning is
   future work.
3. Signature family v1 = {DELETION} only; the world's operator is
   negation. Extension points are documented, not implemented.
4. Retirement is specified but untested by the frozen battery.
5. Signal sparsity (one target per utterance) is an open empirical
   risk. The discovery bars (N, C, K), the eligibility rule, and the
   zero-parameter gate are the design's answer; the
   F1-fail-with-F3+F4-pass branch names sparsity as the next target.
6. Researcher-authored machinery: discovery criterion, UNION
   combiner, OPREC structure, signature family, residual-attribution
   routing, all constants. Bounded L2 direction, not L3. The learner
   creates the inventory, the records, and the routing bindings.
7. Memory: per unit, 1 + (#operators) records; episode store for
   re-grounding; OPMAX=8 cap. The builder sizes static arrays and
   reports usage.
8. T5 (revision) is out of scope; trigger bindings do not revise
   in v1.

## 8. Kill bar checklist (this design task)

- K1 PASS: R1 (section 2), R2 (section 3), R3 (section 4) designed,
  with data structures, algorithms, pseudocode, and frozen constants.
- K2 PASS: R4 specified (section 5) with operationalized F1-F5,
  per-item pass bars, and audit procedures.
- K3 PASS: H2 explicitly excluded (section 0 and section 6); no
  segmentation hypothesis is built, extended, or presupposed; the
  binding constraint addressed is the operator representation, per
  SEG_REVIEW2.

## 9. Handoff to the builder

The builder must preregister separately before implementing: freeze
the constants in 3.7 (may adopt the proposed values or justify
changes), freeze the battery paths for the F3 audit scope, freeze
the exact T1/T3 item ids, and commit the prereg before any
implementation. Builders report BUILD-PASS or BUILD-FAIL only; only
the complete 11-step pipeline can yield SURVIVES.
