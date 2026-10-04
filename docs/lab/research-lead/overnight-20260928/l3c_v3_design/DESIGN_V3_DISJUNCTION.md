# DESIGN: L3C v3 Disjunction Coverage (design only)

Date: 2026-09-30. Status: DESIGN ONLY. No implementation, no builds, no runs.
Question: can the L3C construction mechanism cover disjunction WITHOUT a
dedicated researcher-authored OR case?
Parent result: L3C-V2-ADV2-SURVIVES-THIS-ROUND (prereg c3fc2b964, results
593cc5906). The only confirmed structural ceiling is F2's disjunction blind
spot: the mechanism cannot build OR discriminators, by design of `disc2`.

## 0. Standing-rules name-check (Step 0, written before proceeding)

Four standing sections govern this work. (1) PURE ZAG ONLY: honored, this is
a design-only task, so there is no implementation, no build, no run, and no
analysis scripting of any kind; the document is pure markdown and the only
verification used is the shell-only dash check. Zero Python anywhere.
(2) Fork testing: not applicable, there is no code artifact to battery-test.
(3) Pure-Zag red line scope for fixtures: not applicable, no fixtures are
provisioned. (4) Shell-only byte checks: honored, the committed markdown is
checked with docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
and nothing else. The contaminated paper
(TNN_RESEARCH_PAPER_20260929.md) is untouched.

## 1. Why disjunction is unbuildable in v2 (mechanism-level)

The v2 mechanism (l3c_v2.zag, frozen prefix in 593cc5906, attack main in
l3c_v2_adv2.zag) has three independent properties whose conjunction makes OR
inexpressible. Each is a deliberate design choice, not a bug.

(a) The search vocabulary is conjunctive with an all-instances satisfaction
criterion. `disc2` searches single equality atoms (level 1), conjunctions of
2 distinct-feature equality atoms (level 2), and tightest-bound inequalities
(level 3). Every candidate must satisfy `separates1`/`separates2`: ALL
contradiction instances satisfy the candidate AND NO target instance does.
A disjunction (A OR B) cannot be written as one conjunction of atoms, so it
is not in the searchable vocabulary. In F2 (sig 702, truth: out=0 iff f1==1
OR f2==9), contradiction rows are (3,1,0,7) and (3,0,9,7) against target
(3,0,0,7): no single atom and no 2-conjunction holds for both contradiction
rows while excluding the target row, and no inequality separates either.
Result: `disc2` returns 0 (NONE).

(b) The builder emits a single labeled path whose path semantics is
conjunction. `build_chain` creates one dispatch node per atom, each with
exactly one labeled edge; `interp`/`select_edge` follows the labeled edge
only when that node's atom matches, else the default edge. Traversing D1
then D2 to reach TERM(newout) requires atom1 AND atom2 to match in
sequence. The structure physically cannot route two alternative conditions
to the same terminal, even though the interpreter's `select_edge` already
implements first-match over multiple labeled edges. The union semantics
exists in the interpreter but is never emitted by the builder.

(c) The ambiguity policy withholds instead of composing. When `disc2` finds
2+ all-satisfying separators it emits AMBIGUOUS and withholds (anti-fiat
design, confirmed exact in round-1 and round-2). Multiple alternative
explanations are therefore never assembled into a composite discriminator.
In F2 the policy is not even reached (search returns NONE), but it is the
second wall: even a search that found alternatives would currently refuse
to compose them.

Consequence (round-1 F2, sig 702): exactly 3 HONEST_FAIL trace lines, built
delta 0, rule stays TERM(2), zero AMBIGUOUS events. Honest, exact, and
permanent under the current design.

## 2. Candidate A: alternative-cover dispatch (minimal set cover over the
existing separator vocabulary)

Idea: generalize the search criterion from "one atom satisfied by ALL
contradiction instances" to "a minimal SET of atoms whose union covers all
contradiction instances, with no atom covering any target instance." Build
one dispatch node carrying one labeled edge per cover element, all labeled
edges targeting the shared TERM(newout), default edge targeting the old
leaf. General operation added: cover-set hypothesis formation (set cover
over the separator vocabulary). No new node kind, no new edge kind, no new
op code, no interpreter change: `select_edge` already scans multiple labeled
edges and returns the first match, which is exactly union semantics.

Specification:

- Search: over the existing `disc2` vocabulary (single atoms, 2-atom
  conjunctions, tightest-bound inequalities), find all atoms that cover at
  least one contradiction instance and zero target instances. Find minimal
  covers (fewest atoms) of the full contradiction set. Each cover element
  must independently meet the existing deferred-construction corroboration
  bar (EVID_MIN instances). If exactly one minimal cover exists, build. If
  2+ distinct minimal covers exist, emit AMBIGUOUS and withhold (existing
  anti-fiat policy, unchanged). If no cover exists, HONEST_FAIL (unchanged).
- Construction: single dispatch node D; for each cover atom a_i, one labeled
  edge (a_i -> TERM(newout)); one default edge (D -> old leaf). Uses only the
  existing generic ops (`op_new_node`, `op_mark_term`, `op_new_edge`,
  `op_label_edge`).
- Inductive bias preserved: unseen inputs fall through all labeled edges to
  the default (old/base class), exactly the conservative routing the current
  direct construction uses. No new bias is introduced.

Prediction on F2: atoms covering a contradiction row and no target row are
(f1==1) [covers row (3,1,0,7); target has f1=0] and (f2==9) [covers row
(3,0,9,7); target has f2=0]. Unique minimal cover: {(f1==1), (f2==9)}.
Builds D with two labeled edges to TERM(0), default to old leaf. Eval on
truth: (3,1,9,7)->0 correct, (3,0,0,7)->2 correct, (3,5,5,7)->2 correct,
(3,1,0,7)->0 correct. Predicted: 4/4 on ground truth, 1 build, exact trace.

New failure modes introduced:

- Cover-search combinatorics: set cover is NP-hard in general; with the
  tiny frozen histories (at most 32 rows, small vocabulary) exhaustive
  search is fine, but a scaled-up learner needs a greedy bound with a
  disclosed approximation gap.
- Memorization by singleton covers: without the per-element EVID_MIN bar
  and the minimality preference, the search could cover each contradiction
  instance with its own narrow atom (rote memorization as disjunction).
  The minimality preference (Occam) plus per-element corroboration is the
  principled guard; a red team should attack it with sparse-history worlds.
- Ambiguity explosion: cover sets multiply faster than single separators,
  so the AMBIGUOUS-withhold path fires more often. That is the honest
  outcome, but it means disjunctive worlds with symmetric evidence stay
  unresolved, which bounds the capability.

## 3. Candidate B: disjunction as negated conjunction via De Morgan
(analyzed; rejected as standalone)

Idea: NOT(A OR B) = (NOT A) AND (NOT B). Build the conjunction of negated
atoms targeting the OLD terminal, with the default edge targeting
TERM(newout). This would reuse the existing conjunction machinery
completely.

Why it fails: the vocabulary has no negation primitive (ops are EQ, GE,
LE). Over integer features, NOT(fi==v) = (fi<=v-1) OR (fi>=v+1), which is
itself a disjunction. De Morgan does not eliminate the disjunction; it
pushes it inside the negated atoms. Adding a NEQ op would be a vocabulary
extension that still cannot express the needed unions without a
disjunction mechanism. Candidate B is therefore not a general construction;
it is a restatement of the problem. Rejected as a standalone candidate. Its
valid core (complement reasoning) is preserved in Candidate C.

## 4. Candidate C: inverted construction (complement via a polarity
parameter)

Idea: add one general construction parameter, polarity in {direct,
inverted}, selected by evidence. Run `disc2` twice: direct (separate
contradiction rows from target rows, as today) and complement (separate
target rows from contradiction rows, i.e. swap the SCR_T/SCR_C buffers, a
pure data-routing change). If direct yields a unique separator, build as
today. If direct yields NONE and complement yields a unique separator P,
build the inverted dispatch: the labeled path for P targets the OLD
terminal, and every default edge targets TERM(newout). Semantics: P holds
-> old output; otherwise -> newout. By De Morgan this expresses exactly the
disjunction of the negated atoms of P, without naming any OR case and
without any new vocabulary, ops, or interpreter change. `build_chain`
already takes deftarget and newout as parameters; inversion is a
target swap at the call site.

Prediction on F2: direct search returns NONE (as in v2). Complement search:
level 1 finds no single atom (every atom true of the single target row
(3,0,0,7) is also true of some contradiction row); level 2 finds exactly
one 2-conjunction, (f1==0 AND f2==0), true of the target and of no
contradiction row. Unique -> build inverted: D1 labeled (f1==0)->D2,
default->TERM(0); D2 labeled (f2==0)->TERM(2), default->TERM(0). Eval on
truth: (3,1,9,7)->0 correct, (3,0,0,7)->2 correct, (3,1,0,7)->0 correct,
(3,5,5,7)->0 WRONG (truth 2). Predicted: 3/4 on ground truth.

New failure mode introduced (decisive): the inverted default routes ALL
unseen inputs to the contradiction (rare) class. This breaks the
conservative-default invariant that the entire L3C line relies on for honest
withhold, and in a continuing learner every inverted rule would claim all
unseen inputs for its rare class, a direct interference hazard. Candidate C
converts an honest blind spot into an aggressive bias. Mitigations exist
(higher corroboration bar for inverted builds, explicit HONEST_INVERTED
trace flag so red teams can attack the bias), but the bias is structural.

## 5. Considered and rejected: two nearer options

Ambiguity promotion: when `disc2` returns AMBIGUOUS (2+ all-satisfying
separators), compose the competitors as alternatives instead of
withholding. Rejected for F2: the blind spot returns NONE, not AMBIGUOUS,
so this never fires on the actual ceiling. It addresses a different
phenomenon (genuine evidential ties, correctly withheld).

Sequential refinement reuse: route F2's contradictions through the existing
`try_refine` edge-partition machinery. Rejected: F2's contradictions hit
the root TERM node (kind==1), never a dispatch edge, so no edge partition
exists to refine; they correctly go to `try_construct_root`, which honestly
fails. There is nothing to iterate on.

## 6. Scoring

Scale 1-10, higher is better. CAPABILITY SOURCE DELTA is scored as
smallness of delta (10 = zero new cognition-source lines).

Candidate A (alternative-cover dispatch):
- GENERALITY: 8. Cover-set formation is domain-general: unions of whatever
  separator vocabulary the substrate has, applicable to every signature,
  selected from evidence. Not OR-specific.
- ARCHITECTURAL COMPRESSION: 7. Adds a cover-search routine and a
  multi-edge builder variant; interpreter untouched, no new node/edge
  kinds, no new ops, no new modes. Estimated +80 to 120 lines, all in the
  search/construction layer.
- LEARNER AUTHORITY: 9. The learner discovers the alternative set; the only
  biases are minimality (Occam, general) and per-element corroboration
  (existing EVID_MIN policy). No researcher enumerates alternatives.
- CAPABILITY SOURCE DELTA: 8. Zero interpreter delta; new code confined to
  search plus one builder variant reusing existing generic ops.

Candidate C (inverted construction):
- GENERALITY: 7. Symmetric hypothesis-class extension (complements of
  buildable conjunctions), evidence-selected. Narrower class than A.
- ARCHITECTURAL COMPRESSION: 9. One swapped `disc2` call plus a polarity
  flag at the `build_chain` call site. Smallest possible delta (~25 lines).
- LEARNER AUTHORITY: 8. Evidence-selected, but the direct-first fallback
  order is a researcher-set policy.
- CAPABILITY SOURCE DELTA: 9. Minimal.
- Bias penalty (not in the four scores, but decisive): converts honest
  withhold into aggressive rare-class default routing; 3/4 on F2 truth vs
  A's 4/4; interference hazard for the continuing learner.

Candidate B: not scored; fails the generality test (Section 3).

## 7. Recommendation

Recommend Candidate A: alternative-cover dispatch.

Rationale: it is the only candidate that covers disjunction while
preserving every existing invariant (conservative default routing,
withhold-on-ambiguity, deferred construction, exact traces). The union
semantics it needs already exists in `select_edge`; the current builder
simply never emits it, so no interpreter change and no new semantic case
are required. The new machinery is a general learning operation (minimal
set cover over the separator vocabulary), not a disjunction-specific case:
the same operation unions conjunctions, inequalities, or any future atom
type. The memorization hazard is bounded by two general principles already
in the architecture's spirit (minimality preference, per-element
corroboration), both attackable by a red team. Candidate C is documented
as the compression-favorite alternative, but its rare-class default bias
is a structural regression for a continuing learner and should only be
revisited with explicit bias accounting. No dedicated OR semantic case is
proposed or needed; such a case is explicitly excluded from this design.

## 8. What a v3 prereg would freeze (for a future builder; not this task)

A v3 prereg should freeze: the cover-search specification (vocabulary,
minimality rule, per-element EVID_MIN, tie -> AMBIGUOUS), the multi-edge
builder emission format, and the exact-trace schema for cover builds.
Frozen predictions should include: F2 builds exactly one cover
{(f1==1),(f2==9)} with 4/4 truth eval; a memorization-attack world where
singleton covers are available but lose to minimality (predicted withhold
or minimal build, preregistered); an ambiguity world with two distinct
minimal covers (predicted AMBIGUOUS withhold); and F1/F3 regression
(predicted unchanged: direct unique separators still take the direct
path, so prior families are unaffected). This task performs no
implementation.

## 9. Explicit exclusions

No hardcoded OR semantic case is introduced anywhere in this design. No
new interpreter op, no new node or edge kind, no new cognitive mode, no
new bridge, no task-specific handler. The standing question "why can the
existing general architecture not learn this behavior" is answered: it
cannot because the search criterion demands one all-satisfying atom and
the builder emits one labeled edge per node; the missing piece is the
GENERAL operation of cover-set composition, which Candidate A supplies.
