# Inquiry Scenarios for TNN-3 Kill Bars: Design Draft

Status: DRAFT-NOT-FROZEN. 2026-10-01. Author: Inquiry Scenario
Designer (subagent).

This document designs the inquiry scenario battery for the TNN-3
kill bars, per Micah's accepted recommendation: raise inquiry
scenarios to 5+. It retains K-T3-INQ-1, K-T3-INQ-2, K-T3-INQ-4 as
drafted in `tnn3_killbars/TNN3_KILLBARS_DRAFT.md`, retains
K-T3-INQ-3 verbatim as drafted (per Q4), and adds K-T3-INQ-5,
K-T3-INQ-6, K-T3-INQ-7. Total: 7 bars, 11 scenario slots.

Nothing here is frozen. Freezing is Micah's decision. No bar may
be weakened after results are seen; a broken prereg is amended
transparently and re-frozen.

## 0. What these bars decide

TNN-2's inquiry mechanism is a miss flag plus a constant action
(red team `4e329c772`: L3 discriminating need hardcoded as
action 30 / content -999; L6 evidence-to-behavior link absent).
It satisfied the letter of K-T2-4/K-T2-5 (uncertainty node
created; non-constant act vs the 0 fallback) but not the spirit:
the "choice" never varies with the uncertainty, and nothing ever
clears the flag. The inquiry generalization analysis
(`dedfad368`) named the prereg miss precisely: the frozen kill
bars tested the structure of the chain, not the information
content of the question.

These bars test question content. Every bar below asserts on
what the learner asks, not only that it asks. A system that
varies only miss-identity fields while keeping question shape
constant fails. A system whose questions never respond to
evidence fails. A system that cannot revise its questions fails.

Framing (per Q5): each INQ bar is a kill bar. Failing a bar
kills the inquiry claim for TNN-3 (INQUIRY-BUILD-FAIL for the
claim). Bars are not promoted to falsifiers of the whole
architecture.

## 1. Retained bars (INQ-1 through INQ-4)

INQ-1, INQ-2, and INQ-4 are retained as drafted in
`tnn3_killbars/TNN3_KILLBARS_DRAFT.md` section 4. INQ-3 is
retained verbatim below (per Q4: keep as drafted, no
weakening). Summaries are given for completeness; the draft
text governs.

### K-T3-INQ-1 (derived discriminating need)

Summary: the sealed battery includes at least 2 inquiry
scenarios whose warranted inquiries differ. The learner's
constructed guides must carry derived content: the guide's
action and content fields (the fields ACT selects on and that
name the inquiry to perform, not the miss-identity fields)
must differ across the two scenarios, and each must match the
content the world's checker computes from the world's private
hidden structure. Constant guide content across differing
uncertainties fails. 2 scenario slots.

### K-T3-INQ-2 (evidence updates later behavior; closes the missing L6 link)

Summary: two sealed scenarios. (a) Resolution: after the
environment supplies the missing fact, the UNCERTAINTY node
must transition to resolved (visible in the deterministic
state dump) and a subsequent ACT call in the same context must
not select the stale guide; ACT output must differ before and
after resolution. (b) Misleading evidence: evidence showing
the inquiry's premise was wrong must revise or supersede the
guide, and ACT must not select it afterwards. 2 scenario
slots.

### K-T3-INQ-3 (ambiguity handled non-arbitrarily; the swap test)

Retained verbatim as drafted (Q4):

Statement: two sealed scenarios present two simultaneous
warranted uncertainties each. The world's hidden structure
makes inquiry-A strictly dominate in scenario 1 (it resolves
both uncertainties; B resolves one) and inquiry-B strictly
dominate in scenario 2. The adversary orders the triggering
misses so that incidental heuristics (first-created wins,
most-recent wins, highest event-count wins) select the
dominated inquiry in at least one scenario. Bar: ACT selects
the dominating guide in both scenarios, 3/3 byte-identical.

Why TNN-2 fails: both guides are content-identical (constant
30/-999 differing only in the subject slot), so selection
cannot be based on informativeness at all. ACT selects by
context match then max bid (event counts); ties resolve to
first found in edge order. In the scenario where the
dominated uncertainty's miss is presented first, TNN-2
deterministically selects the dominated guide. The swap is
untrackable by any constant or incidental ordering.

Achievability: a learner that derives discriminating need can
compare the inquiries' expected coverage over its own open
uncertainties. The bar does not prescribe the comparison
computation; it requires only the observable swap-tracking in
cases where dominance is unambiguous by design.

Verification: ACT output comparison against the checker's
designated dominant guide per scenario, 3/3 byte-identical.

### K-T3-INQ-4 (inquiry reuse and transfer, C0-D)

Summary: a sealed scenario presents the same uncertainty kind
twice (two episodes with the same hidden discriminating
structure but different surface subjects). Bar: the second
episode's guide must structurally reference the first
episode's retained inquiry structures (edge-link visible in
the deterministic state dump), and the learner must reach the
correct inquiry action with strictly fewer miss events before
correct ACT selection than in episode 1. 1 scenario slot
(two episodes).

## 2. New bars (INQ-5 through INQ-7)

### K-T3-INQ-5 (non-obvious optimal inquiry; the confirmation trap)

**What uncertainty the learner faces.** A sealed scenario
presents one warranted uncertainty with three open
hypotheses H1, H2, H3 about a hidden regularity. H1 is the
leading hypothesis: it has the most supporting evidence in
the taught facts, and any salience-tracking heuristic (bid,
recency, evidence count) ranks it first. The world offers
two probes. P-confirm asks about H1's distinctive
prediction: a "yes" confirms H1, a "no" eliminates only H1.
P-discriminate asks about a shared discriminator: its two
possible outcomes split the hypothesis set {H1,H2} vs {H3}
regardless of which outcome arrives. The checker's private
computation shows P-discriminate has strictly higher
expected hypothesis-elimination than P-confirm.

**What counts as good vs bad inquiry.** Good: ACT selects
the P-discriminate guide. Bad: ACT selects the P-confirm
guide. The bad inquiry is the locally attractive one: every
surface heuristic that tracks the leading hypothesis (ask
about what you most believe; ask about the most evidenced
candidate) points at P-confirm. Only a learner that
computes expected split over its own open hypotheses picks
P-discriminate. This is the confirmation-shaped local
attractiveness named in the inquiry generalization
analysis, section 1.5.

**The lure flip (second slot).** A second sealed scenario
keeps the three-hypothesis structure but the checker
assigns the discriminating probe to the salient
hypothesis's distinctive prediction: now P-confirm (asking
about H1) IS the high-split probe and the alternative is
the low-split one. Bar: ACT selects the high-split probe
in both scenarios. A trivial satisfier ("always avoid the
salient hypothesis" or "always ask about the leader")
passes one slot and fails the other. Only
informativeness-tracking passes both. This mirrors INQ-3's
swap logic, applied to the confirmation lure rather than
to incidental ordering.

**Non-redundancy vs INQ-3.** INQ-3 tests
dominance-tracking across two simultaneous uncertainties
against incidental ordering heuristics. INQ-5 tests
informativeness-tracking within a single uncertainty
against the confirmation lure (asking about the leading
hypothesis). A system could compare coverage across
uncertainties (pass INQ-3) yet still ask confirming
questions about its leading hypothesis (fail INQ-5).
Not redundant.

**Why TNN-2 fails.** Deterministic. Both guides are the
constant 30/-999; there is no probe differentiation at
all, so selection cannot track expected split. In slot 1
TNN-2's incidental selection may land on either probe;
the bar requires the discriminating probe in both slots,
3/3 byte-identical, which a constant system cannot
satisfy by design.

**Achievability.** A learner that derives discriminating
need as expected hypothesis-elimination over persisted
hypothesis structures (the L2 sketch in `dedfad368`,
section 1.4) computes the split for each candidate probe
and selects the max. The bar prescribes the observable
(ACT selects the checker-designated high-split probe in
both slots), not the split computation.

**Verification.** ACT output comparison against the
checker's designated probe per slot; guide content fields
logged per the INQ log format (section 4); 3/3
byte-identical. 2 scenario slots.

### K-T3-INQ-6 (inquiry revision: ask, partial answer, better follow-up)

**What uncertainty the learner faces.** A sealed scenario
presents a warranted uncertainty with four open hypotheses
{H1,H2,H3,H4}. The checker's private structure defines a
two-stage discriminating sequence. Stage 1: probe Q1 splits
{H1,H2} vs {H3,H4}. The environment answers Q1, eliminating
H3 and H4. Residual uncertainty: {H1 vs H2}. Stage 2:
probe Q2 splits H1 vs H2, and Q2 is only identifiable as
the right question after the stage-1 answer arrives (its
discriminating power is conditioned on the residual set).

**What counts as good vs bad inquiry.** Good, in order:
(a) the stage-1 guide's content matches the checker's Q1
spec; (b) within K=10 events of the stage-1 answer, a new
guide appears whose content matches the checker's Q2 spec:
it targets the residual {H1 vs H2} uncertainty and does
not re-ask the settled Q1 discriminator; (c) the stage-1
guide is superseded or resolved (the INQ-2 lifecycle,
applied here as refinement rather than retirement); (d)
ACT selects the Q2 guide, not a repeat of Q1. Bad: any
re-asking of Q1 after its answer; any follow-up whose
content is not conditioned on the stage-1 answer; no
follow-up at all (the learner treats the partial answer
as terminal).

**The evidence-conditioning control.** A control run
presents the same stage-1 setup but the environment's
answer is uninformative (eliminates no hypotheses). Bar:
the learner must NOT produce a changed Q2 in the control;
the follow-up content must be conditioned on the answer,
not on elapsed events. This proves the revision is
evidence-driven, the inquiry analog of the revision loop.
A system that emits a second question on a timer fails
the control.

**Why this bar matters.** INQ-2 tests the guide lifecycle
(create, resolve, supersede). INQ-6 tests question
refinement: the learner's question representation itself
updates on partial evidence. This is the "ask, get answer,
ask better follow-up" behavior the mission requires, and
it is the inquiry-side counterpart of counterexample-
driven revision. TNN-2 cannot pass any clause: it has one
constant guide, no follow-up machinery, no residual-
uncertainty representation.

**Why TNN-2 fails.** Deterministic, on every clause. The
constant 30/-999 guide cannot match Q1 content (clause
a); no second guide is ever constructed (clause b); no
supersession path exists (clause c); ACT cannot select a
Q2 guide that does not exist (clause d).

**Achievability.** A learner with persisted hypothesis
structures and a derived-question procedure re-runs
derivation on the residual set after the stage-1 answer:
the same machinery that produced Q1 from {H1..H4}
produces Q2 from {H1,H2}. The bar does not prescribe the
derivation; it prescribes the observable sequence and the
control.

**Verification.** Stage-1 guide content vs checker Q1
spec; post-answer guide construction within 10 events
with content vs checker Q2 spec; state-dump supersession
check on the stage-1 guide; ACT output selects Q2;
control run shows no content change on uninformative
answer. All 3/3 byte-identical. 1 scenario slot (two
stages plus control).

### K-T3-INQ-7 (cross-domain question-pattern reuse)

**What uncertainty the learner faces.** Two sealed domains
with disjoint relations and entities. Domain A is a chain
world where the learner derives diverging-link probes
(the pattern: find where candidate value-paths diverge,
ask about the divergence point). Domain B is a disjoint
relation family (e.g., sum/count structure) where the
same abstract pattern applies (identify the discriminator
among competing hypotheses) but no surface mapping is
given: relations, entities, and literals share nothing
with A.

**What counts as good vs bad inquiry.** Good: (a) the
guide content constructed in B is derived and matches the
checker's B-spec; (b) the deterministic state dump shows a
structural reference edge from B's inquiry structures to
A's retained question-pattern structures (the pattern,
not A's answers: the checker verifies the referenced
structure is A's guide/question node and that A's answer
facts are not referenced); (c) source inspection shows no
per-domain question branches in the inquiry path
(one-system rule: the mapping is learner-derived, never
hardcoded); (d) a fresh-state control learner on B alone
takes strictly more miss events to reach the correct
inquiry than the A-experienced learner (proves the
transfer did work, not fresh derivation). Bad: correct
content in B with no structural reference to A (fresh
derivation, not reuse); reference to A's answers rather
than A's question pattern (answer copying, not pattern
reuse); any domain-identity branch in source (hardcoded
mapping, fails outright).

**Non-redundancy vs INQ-4.** INQ-4 is same-kind reuse:
same hidden discriminating structure, different surface
subjects, within one domain family. INQ-7 is cross-domain
pattern reuse: the discriminating structure differs, only
the abstract question pattern transfers. A system could
reuse a retained question within its home domain (pass
INQ-4) yet fail to recognize the pattern's applicability
in a disjoint domain (fail INQ-7). This bar is the
inquiry-side operationalization of Micah's lifetime
criterion: a procedure shape adapted to an unfamiliar
domain.

**Why TNN-2 fails.** Deterministic. No question pattern
is ever derived (constant guides), nothing is retained
that could be referenced, and every domain rebuilds the
same constant from scratch. Clauses (a) through (d) all
fail.

**Achievability.** A learner that represents derived
questions as structures (per the `dedfad368` sketch:
guide nodes with derived slots and provenance edges to
hypotheses) can link a new domain's inquiry structures
to a retained pattern node when the abstract match
(divergence structure) is detected. The bar prescribes
observables (derived content, reference edge, no source
branches, control improvement), not the match
computation.

**Verification.** Guide content in B vs checker B-spec;
state-dump edge check (B inquiry structures to A
question-pattern node; A's answer facts unreferenced);
source inspection for domain branches; miss-event counts
from the sealed driver log (A-experienced vs fresh
control), strictly fewer for the experienced learner.
All 3/3 byte-identical. 1 scenario slot (two domains
plus control).

## 3. Scenario budget

| Bar | Slots | Notes |
|---|---|---|
| INQ-1 | 2 | differing warranted inquiries |
| INQ-2 | 2 | resolution + misleading evidence |
| INQ-3 | 2 | the swap (retained verbatim) |
| INQ-4 | 1 | two episodes, one slot |
| INQ-5 | 2 | confirmation trap + lure flip |
| INQ-6 | 1 | two stages + control, one slot |
| INQ-7 | 1 | two domains + control, one slot |
| Total | 11 | exceeds the 5+ requirement with room for clean separation |

The Q1 review counted 7 slots for INQ-1..4 and recommended
5+ scenarios to avoid forced triple-booking. This design
keeps every bar's slots independent: no scenario serves
two bars. Overlap is permitted only where explicitly
noted (none above).

## 4. Topology log format for inquiry (Q2)

Per the Q2 recommendation (explicit log format), the
evaluator logs one line per inquiry-structure event in
this exact format:

```
INQ <world-id> <uncertainty-id> <run-idx> <event:construct|select|supersede|resolve> <guide-id> <t2_sig-string>
```

Fields are space-separated. `<t2_sig-string>` contains no
spaces. `<uncertainty-id>` is the learner-state node id of
the UNCERTAINTY node the guide is anchored at (or `none`
for supersede/resolve events on already-unlinked
structures, with the guide id still identifying the
structure). The log is written to stdout and captured per
run. The sealed evaluation compares these logged strings
mechanically; no human judgment enters the comparison.

Event semantics:

- `construct`: a guide node was created, anchored at the
  given uncertainty. The signature covers the guide plus
  its anchor and provenance edges (section 5).
- `select`: ACT selected this guide at an inquiry
  opportunity. One select line per ACT call that returns
  an inquiry action.
- `supersede`: the guide was superseded (type-3 self-edge
  or the architecture's own convention). Logged when the
  transition is created, not when observed.
- `resolve`: the uncertainty node transitioned to
  resolved. The guide id field carries the uncertainty's
  primary guide, or `none` if it had none.

Determinism: the full INQ log must be byte-identical
across 3 runs (the inquiry analog of K-INQ3 from the
INQUIRY-1 prereg). Any nondeterminism in guide ids (e.g.,
allocator order) must be canonicalized by the driver
before logging, or the bar fails on determinism.

## 5. Structural signature applied to inquiry traces (Q3)

**Function.** `t2_sig`, the one fixed preregistered
function (per Q3), as implemented in the frozen TNN-2
source (commit `f4de7ff46`, file
`docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`).
No second signature function is introduced.

**Application to inquiry structures.** For each logged
INQ event, the signed object is the inquiry structure:
the guide node as traversal root, plus the uncertainty
anchor node reached via the guide's anchor edge, plus
provenance edges from the guide to the hypothesis
structures it discriminates (or to the retained
question-pattern node it references, for INQ-7). The
existing `t2_sig` rules apply unchanged: cell tags in
canonical traversal order, edge types, per-node step
counts, adjacency shape; literals (subject/object/value
payloads) EXCLUDED.

**Why this is the right level.** The letter-vs-spirit gap
was that bars tested chain structure while the failure
was in question content. A signature over the inquiry
structure's topology detects exactly the trivial
satisfiers the old bars admitted: a system that varies
only the miss-identity subject slot while keeping the
question shape constant produces IDENTICAL signatures
across scenarios, because literals are excluded and the
topology did not change. Derived content that changes
the question shape (different probe parameters,
different discriminated hypothesis sets, different
provenance edges) changes the signature.

**Calibration properties (frozen at freeze time; the
evaluator must verify before scoring, else the
evaluation is void, mirroring the H2 rule).**

- (i) Two guides encoding different question shapes
  (e.g., a diverging-link probe vs a confirming probe,
  or Q1 vs Q2 in INQ-6) produce DIFFERENT signatures.
- (ii) Two guides encoding the same question shape with
  different literals (same probe structure, different
  subjects) produce IDENTICAL signatures.
- (iii) A guide with provenance edges to 2 hypotheses vs
  the same guide shape with provenance edges to 3
  hypotheses produces DIFFERENT signatures (the
  discriminated set is part of the topology).

**Scope note.** `t2_sig` as implemented traverses
promoted-graph cells. Applying it to inquiry structures
requires specifying the traversal root (guide node id)
and the included edge set (anchor edge + provenance
edges) as a wrapper at the driver level. The function
itself is unchanged. If the frozen implementation
cannot traverse an arbitrary root, the evaluator records
this at calibration time and the freeze amendment covers
the wrapper only, never the function.

## 6. Kill-bar framing and verdicts (Q5)

Each K-T3-INQ bar is a kill bar: failing it kills the
inquiry claim for TNN-3. The verdict taxonomy:

- INQUIRY-CLAIM-PASS: all of INQ-1 through INQ-7 hold at
  their stated bars, 3/3 byte-identical; no falsifier
  triggered; determinism holds on the INQ log.
- INQUIRY-CLAIM-FAIL: any bar below its threshold, any
  determinism failure, or any triggered falsifier. The
  evaluation report must localize the failure to the bar
  and clause, as the INQUIRY-1 prereg's section 7
  requires.

Bars are not falsifiers of the architecture. A failed
INQ bar is evidence about the inquiry mechanism's
generality boundary, clustered by shared architectural
cause per the no-patch-treadmill rule.

## 7. Determinism, governance, and accounting

- Determinism: every scenario runs 3 times; the INQ log,
  ACT outputs, and state dumps are byte-identical
  across runs. Any deviation fails the determinism
  requirement for the affected bar.
- Governance: pure Zag for all research logic; zero
  Python or other forbidden executables; the
  contaminated paper stays untouched; commits local with
  explicit pathspecs; no sealed FW1-FW9 or H2 world
  contents accessed during design or (later) evaluation.
- One-system accounting: the evaluation report must
  record researcher-owned vs learner-owned structural
  decisions for the inquiry mechanism, source-enumerable
  forms, SUF decisions, cognition lines added, and
  zero new modes/bridges/handlers/semantic cases (any
  found fails the corresponding bar by inspection).
- The standing architectural metric (12 fields per
  Micah's ruling) is a required section of every
  inquiry evaluation report.

## 8. Explicit non-claims

- This document is DRAFT-NOT-FROZEN. No bar is frozen
  until Micah freezes it. The freeze commit must
  strictly precede any implementation or evaluation it
  governs.
- Passing INQ-1 through INQ-7 does not by itself
  establish SUF, L3, C0-B, or C0-C. It establishes
  derived, evidence-responsive, revisable, reusable
  inquiry content under sealed adversarial design.
  C0-B requires the open-construction story; C0-C
  requires the post-freeze generality battery; SUF
  requires the write-path audit showing a structural
  decision resolved by learner history.
- INQ-7's cross-domain clause does not establish
  general cross-domain cognition. It establishes one
  question-pattern transfer under sealed design.
- The `t2_sig` inquiry application is a specified
  wrapper, not a change to the frozen function. If
  calibration property (i), (ii), or (iii) fails at
  evaluator check time, the evaluation is void and the
  wrapper is repaired and re-frozen; the function is
  never edited in place.
- No implementation is authorized by this draft.

## 9. Dependencies and ordering

- Requires: the frozen `t2_sig` specification
  (`f4de7ff46`); the INQ log format in section 4
  (frozen at bar-freeze time); sealed inquiry worlds
  authored by a named adversary after freeze (per the
  C0-C visibility protocol to be frozen with the bars).
- Independent of: H2 evaluation (H2 runs now, per
  Micah's ruling; these bars govern TNN-3 inquiry
  work, which waits for H2/H3-lite/reuse evidence).
- Recommended order: freeze INQ-1..7 as one battery;
  implement against the frozen battery; evaluate sealed.
