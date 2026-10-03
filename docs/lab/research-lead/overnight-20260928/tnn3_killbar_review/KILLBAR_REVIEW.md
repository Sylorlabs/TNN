# TNN-3 Kill-Bar Draft: Achievability and Consistency Review

Status: REVIEW ONLY. The draft (`76231baa8`) remains DRAFT-NOT-FROZEN.
This document does not amend, freeze, or weaken any bar. Micah decides.

Reviewer scope: six tasks from the parent. (1) Per-bar achievability.
(2) Verification soundness. (3) Internal consistency. (4) Recommendations
on the 6 open questions. (5) Redundancy. (6) Gaps against red-team
findings.

## 1. Per-bar achievability

Standard applied: a bar is achievable if a genuinely general (L3)
mechanism can pass it without violating the frozen ISA, the no-new-mode
rule, or the falsifiers, and if a clever L2 mechanism of the TNN-2
type deterministically fails it. "Clever L2" means: fixed schemas with
runtime-filled slots, researcher-authored orderings, oracle or
constant content, no cross-world structural novelty.

### K-T3-ADV (adversarial process bar)

Achievable: yes. This bar constrains the evaluation process, not the
implementation. Any implementation faces the same process. A genuine
L3 system is unaffected by when worlds were authored; a schema-L2
system fails because it cannot pre-enumerate post-freeze worlds.

The fail-closed BLOCKED (not pass) on pre-freeze assets is the
correct polarity. Git-ancestry verification (`merge-base --is-ancestor`)
is deterministic and auditable.

One risk: adversary quality. The bar assumes the independent adversary
actually authors worlds outside the builder's families. The draft
mitigates with minimum counts (4/3/3), pairwise-distinct signatures,
and the non-triviality rationale presence check. Presence check is
weak (it verifies existence, not quality), but the signature
pairwise-distinctness does the real work. Acceptable.

### K-T3-TOPO (learner-chooses-topology audit)

Part (a), mutual non-isomorphism: achievable. A genuine L3 construction
or repair space produces shapes keyed to world evidence. The
deterministic signature function is the load-bearing component; see
section 2.

Part (b), beyond-fixture shapes: achievable and well-designed. It
catches the "train on the test" failure without prescribing how the
builder tests. The "at least one" threshold is minimal but sufficient:
a single novel shape proves the space was not fixture-closed.

Potential gaming: a builder could ship a minimal fixture suite to make
(b) trivially easy. But minimal fixtures make (a) harder, because the
builder has fewer exercised shapes to draw on when facing sealed
worlds. The two parts create opposing pressures, which is good design.

TNN-2 fails both parts deterministically, as the draft states.

### K-T3-CON-1 (sealed constructions, derived content)

Achievable: yes. 3+ mutually non-isomorphic topologies from 4+ sealed
worlds is demanding but within reach of a genuine construction
mechanism. The frozen 4-op ISA does not bound depth, branching, or
reuse; TNN-2's bounds (depth 4, 96 paths, 12 values, fixed assemblers)
are builder choices, confirmed by the construction red team.

The derived-content condition ("structural information must not be
readable from the triggering event literals alone") is the
anti-lookup clause. It directly defeats the alternative-explanation
attacker's "lookup by observed facts" account (`ccee9e5e6`). The
adversary documents the required divergence; the checker computes
required content from hidden structure. Well-designed.

A clever L2 system with a larger finite menu (say, 10 families instead
of 3) still fails: the adversary authors 3+ non-isomorphic topologies
outside any fixed enumeration the builder could have completed before
the freeze, and the derived-content condition defeats literal-keyed
retrieval.

### K-T3-CON-2 (construction reuse, C0-D)

Achievable: yes. This is the key C0-D test for construction. Reuse is
composition; the bar does not prescribe the reuse mechanism
(sub-graph reference, invocation, copy with provenance), only the
observable structural reference and the control failure.

The control run (fresh state on the same world minus the earlier phase
must fail) is essential. Without it, a system could pass by building
fresh each time and incidentally referencing old cells. With it, the
bar proves necessity, not just occurrence.

TNN-2 fails deterministically (no MAP reading in the proposal path,
verified by the red team and the MUL comparator `e2e34a4ac`).

### K-T3-INQ-1 (derived discriminating need)

Achievable: yes. A learner that derives discriminating need from
uncertainty content produces guides whose action/content fields vary
with the uncertainty. The bar requires variation across 2 scenarios
and checker-computed match. Minimal threshold, correct polarity.

The draft correctly identifies the fields ACT selects on (not the
miss-identity fields). This prevents the trivial satisfier of varying
only the subject slot while keeping action constant.

### K-T3-INQ-2 (evidence updates behavior)

Part (a), resolution: achievable. Uncertainty lifecycle (create,
resolve, supersede) is ordinary state management over existing node
and edge types. The inquiry generalization analysis (`dedfad368`)
showed the type-3 supersession convention already exists and is
honored by `activate` and `ev_act`.

Part (b), misleading evidence: achievable and important. It tests
whether inquiry revises, not just resolves. TNN-2's lock-in (red team
Attack 2) is the target.

ACT output must differ before and after: this is the observable that
prevents a sham resolution marker with no behavioral effect.

### K-T3-INQ-3 (ambiguity swap test)

Achievable: yes, but this is the most demanding inquiry bar. It
requires dominance-tracking across scenarios where incidental
heuristics (first-created, most-recent, highest bid) pick wrong in at
least one scenario.

The "unambiguous by design" clause is the achievability bound: the
adversary must construct worlds where dominance is clear, not where
reasonable systems could disagree. This keeps the bar from demanding
optimal inquiry in genuinely ambiguous cases.

A genuine L3 inquiry system derives expected coverage over its own
open uncertainties and should track dominance. A constant-guide
system (TNN-2) fails deterministically. A system with derived content
but no comparison (guides vary, but selection is still incidental)
also fails, which is correct: INQ-1 without INQ-3 would admit
"varied but uncompared" guides.

On prescriptiveness (Open Question 4): the bar prescribes the
observable (ACT selects the dominating guide in both scenarios), not
the decision criterion. Any internal mechanism that produces the
observable passes. This is the right level.

### K-T3-INQ-4 (inquiry reuse and transfer, C0-D)

Achievable: yes. Structural reference to retained inquiry structures
plus strictly fewer misses in episode 2. The "strictly fewer" is
measurable and prevents sham references.

TNN-2 fails (no episode records, no resolution, constant guides).

### K-T3-REV-1 (two structurally different sealed repairs, derived content)

Achievable: yes. The revision generalization analysis (`edbb0e9b5`,
section 4a) sketched repair-family search within the frozen ISA using
existing assemblers, `t2_exec`, and `t2_try_verify`. The bar does not
prescribe the repair family; the six examples (guard-predicate edit,
branch rerouting, multi-step, step-count/type conversion, deletion
without insertion, cross-MAP borrow) are illustrative.

The derived-content condition is the anti-literal-patch clause: the
world is built so the observation's literal is NOT the correct repair
content. This directly defeats TNN-2's "overwrite the stored constant
with the new stored constant" (alternative-explanation `ccee9e5e6`).

The diversity set must include at least one reuse-without-insertion
repair (rerouting or borrow). This is important: without it, a system
could pass with two insertion-style repairs that are topologically
distinct but operationally similar. The reuse requirement forces
genuine structural thinking.

### K-T3-REV-2 (retained-set regression)

Achievable: yes. 100 percent of the retained set must verify. This is
strict but correct for a kill bar: a repair that breaks retained cases
is not a repair.

The retained set is already in learner state as provenance edges; the
bar requires the revision mechanism to actually consult it. TNN-2's
failure (never consults retained facts) is the target.

### K-T3-REV-3 (successive revision including revert)

Achievable: yes. Repair history is ordinary learner state; deletion is
the tombstone/rewire machinery without insertion. The bar requires the
final graph to not contain A's edit as an active step and the retained
set to pass.

This is the hardest revision bar because it requires the system to
represent "my last repair was wrong" and act on it. TNN-2's failure
(no history, no deletion path) is the target.

## 2. Verification soundness

All bars specify 3/3 byte-identical checks, pure-Zag sealed checkers,
and deterministic state dumps. This matches the loop's standing
determinism standard. No human judgment at eval time.

Specific soundness notes:

**Signature function (K-T3-TOPO, used in ADV, CON-1, REV-1).** The
draft proposes: canonical string over cell tags, edge types, step
counts, adjacency shape; no literals, no addresses, no allocation
order. This is the right exclusion set: literals vary with world
content (must not count as structural difference), addresses and
allocation order are implementation artifacts (must not count).

Risk: coarseness. If two genuinely different topologies produce the
same signature, the bar under-detects. Risk: fineness. If trivial
variations (e.g., one extra no-op step) produce different signatures,
the bar over-detects. The function must be calibrated so that the
TNN-2 families (chain k=2 vs k=3) count as different (they are
structurally different depths) but isomorphic graphs with different
literals count as same. The draft's proposal handles this, but the
exact function must be frozen in the prereg and tested against known
pairs before the evaluation.

**Checker-computed content (CON-1, INQ-1, REV-1).** The sealed world's
checker computes required content from the world's private hidden
structure, not from the event stream. This is sound: the builder
cannot precompute it, and the check is deterministic.

**ACT output comparison (INQ-2, INQ-3).** Observable behavior, no
state-reading ambiguity. Sound.

**State-dump reference checks (CON-2, INQ-4).** "Shared cells or edges
visible in the deterministic state dump." The dump format must be
frozen in the prereg to prevent post-hoc reinterpretation. The draft
implies this but should state it explicitly in the frozen version.

**Control runs (CON-2).** Fresh-state control must fail. Sound
necessity test.

**Git ancestry (ADV).** `merge-base --is-ancestor`, fail-closed
BLOCKED. Deterministic, auditable. Sound.

**Builder signature log (TOPO(b)).** The builder commits the log at
build freeze; the sealed evaluation compares sets. Sound, provided
the log format is frozen in the prereg.

No bar is gameable by a TNN-2-type system without genuine
generalization, because ADV's post-freeze authorship prevents
pre-enumeration and the derived-content conditions prevent
literal-keyed retrieval.

## 3. Internal consistency

Checked for contradictions and incompatible architecture assumptions:

- **ADV vs TOPO:** compatible. ADV governs when worlds are authored;
  TOPO(b) governs what the builder logged. No conflict.
- **Signature function scope:** the draft says the function is "fixed
  in the frozen prereg" (section 2) but also "allows per-world
  functions" (Open Question 3 notes "the draft allows per-world
  functions"). This is the one internal tension. See recommendation
  on Q3: fix a single function.
- **ISA freeze:** section 10 states no new opcodes permitted; all
  bars are achievable within the 4-op ISA plus EXECUTE per the
  cited analyses. Consistent.
- **No new modes/bridges:** section 10 carries forward the F-T2-1
  falsifiers. Consistent with the bars' behavior-only design.
- **C0-A as regression:** retaining TNN-2's genuine C0-A achievements
  while adding B/C/D bars is coherent. No bar requires un-learning
  C0-A.
- **"Two structurally different" generalization (section 6):** the
  counts differ per mechanism (3 for construction, 2+2 for inquiry,
  2 for revision). This is not an inconsistency; it reflects the
  different diversity requirements per mechanism. Construction needs
  3 because its space is larger; revision needs 2 because repairs
  are more constrained.
- **INQ-3 vs "no prescribed criterion" (section 10):** INQ-3 requires
  dominance-tracking, which is a behavioral observable, not a
  prescribed internal criterion. Consistent with the design rule.

No blocking inconsistencies. The signature-function scope question
(Q3) should be resolved at freeze.

## 4. Open questions: recommendations

### Q1. World counts

Draft: construction 4+ worlds (3+ non-isomorphic), inquiry 3+
scenarios, revision 3+ scenarios (2+ non-isomorphic repairs).

**Recommendation:** raise inquiry to 5+ scenarios; keep the rest.

Reasoning: count the scenario slots the inquiry bars need. INQ-1
needs 2 scenarios with differing warranted inquiries. INQ-2 needs 2
(resolution + misleading evidence). INQ-3 needs 2 (the swap).
INQ-4 needs 1 (two episodes). That is 7 slots. Some can overlap
(e.g., one scenario could serve INQ-1 and INQ-2(a)), but forced
overlap risks coupling bars that should be independent. With 3
scenarios, the adversary must triple-book; with 5, there is room
for clean separation plus one spare. Construction's 4 worlds for
3 topologies already includes a spare; revision's 3 scenarios for
2 repairs likewise. Inquiry is the outlier. 5+ scenarios is the
proportionate count.

### Q2. TOPO(b) builder burden

**Recommendation:** keep the requirement; specify the log format in
the prereg.

Reasoning: the burden is test instrumentation, not architecture.
The builder already maintains a test suite; logging a signature
string per promoted/revised graph is a small addition. It is
essential to the beyond-fixture check, which is one of the two
mechanisms (with ADV) that prevent train-on-test. Without it, a
builder could pass TOPO(a) with shapes that happen to match
fixtures, and no check would detect the closure. The format
(cell tags, edge types, step counts, adjacency shape, canonical
ordering) should be frozen in the prereg so the sealed
evaluation's comparison is mechanical.

### Q3. Signature function: single fixed vs per-world

**Recommendation:** single function fixed in the frozen prereg.

Reasoning: per-world functions multiply audit surface. Each
function would need its own correctness review, and inconsistencies
between functions could create disputes about whether two graphs
are "really" different. A single function is simpler to audit,
simpler to test against known pairs (chain k=2 vs k=3 must differ;
same topology with different literals must not), and harder to
game. The draft's proposed canonical string is a sound starting
point. Freeze it, test it, use it everywhere.

### Q4. INQ-3 prescriptiveness

**Recommendation:** keep as drafted.

Reasoning: the bar prescribes an observable (ACT selects the
dominating guide in both swap scenarios), not a decision criterion.
Any internal mechanism producing the observable passes. The
"unambiguous by design" clause bounds the adversary: dominance
must be clear, not debatable. A system that cannot track dominance
in unambiguous cases is not doing discriminating inquiry; it is
doing incidental selection. The bar measures exactly the
capability the inquiry red team found missing (arbitrary
disambiguation under ambiguity). Removing or weakening it would
leave that failure mode uncovered.

### Q5. Kill bars vs falsifiers

**Recommendation:** keep all as kill bars; do not promote.

Reasoning: the falsifier/kill-bar distinction is load-bearing.
Falsifiers (F-T2-1 style) govern architecture rules: ISA freeze,
no new modes/bridges/handlers, no semantic cases. Violation means
the submission broke the experimental contract. Kill bars govern
capability/generality: failure means this generation did not
achieve the goal, not that it cheated. A TNN-3 that fails
K-T3-CON-1 but respects the ISA has produced a valid negative
result; promoting the bar to a falsifier would misclassify honest
failure as rule-breaking and chill the reporting of negative
results. Keep the distinction clean.

### Q6. C0-A regression bars

**Recommendation:** retain as regression bars; do not strengthen.

Reasoning: TNN-2 genuinely achieved C0-A in all three mechanisms
(content traceable to evidence, persistent learner state, no
scaffolding). The red teams confirmed these as honest passes.
Strengthening C0-A would move the goalposts on achievements
already banked. The L3 advance is in B/C/D, which the new bars
cover. Retention without strengthening is the right call: it
prevents regression without demanding more than the research
program requires at this step.

## 5. Redundancy

Checked pairwise:

- **TOPO(a) vs CON-1 / REV-1:** TOPO(a) is the cross-cutting
  mechanism (mutual non-isomorphism via the signature function);
  CON-1 and REV-1 are its per-mechanism applications with
  additional conditions (derived content, world counts). Not
  redundant: TOPO(a) states the rule, the others apply it.
- **TOPO(b) vs ADV:** complementary. ADV ensures worlds are
  post-freeze; TOPO(b) ensures shapes are beyond fixtures. A
  post-freeze world could still require a fixture shape (adversary
  error or deliberate easy world); TOPO(b) catches that. Not
  redundant.
- **INQ-2(a) vs INQ-4:** INQ-2(a) is single-episode resolution;
  INQ-4 is cross-episode reuse with a miss-count improvement.
  Different observables. Not redundant.
- **REV-1 vs REV-3:** REV-1 is diversity of repair topologies;
  REV-3 is successive revision with revert on the same graph.
  A system could pass REV-1 (two different repairs on two graphs)
  and fail REV-3 (cannot revert its own repair). Not redundant.
- **CON-1 vs CON-2:** CON-1 is structural diversity; CON-2 is
  reuse with control. A system could construct 3 novel topologies
  fresh each time and fail reuse. Not redundant.
- **INQ-1 vs INQ-3:** INQ-1 is content variation across scenarios;
  INQ-3 is dominance-tracking under swap. A system could vary
  guide content (pass INQ-1) but select incidentally (fail INQ-3).
  Not redundant; INQ-3 is the teeth behind INQ-1.

No bars are redundant. Each covers a distinct observable.

## 6. Gaps against red-team findings

Mapped every red-team and analysis finding to bar coverage:

**Construction (`340e94e3e`):**
- 3 linear families, 2 reachable in production: covered by CON-1
  (3+ non-isomorphic) and TOPO(b) (beyond fixtures).
- Fixed assembly order: covered by CON-1 derived-content
  condition (wiring order must diverge from surface order).
- Hard bounds (depth 4, 96 paths, 12 values): covered by CON-1;
  the adversary can require depth 5+, which the red team proved
  unrepresentable.
- Oracle verifier (accepts first family member matching expected):
  covered by ADV (post-freeze; builder cannot pre-fit) and
  CON-1 derived content (checker computes from hidden structure,
  not event literals).
- DEC never emitted: covered by CON-1; adversary can require it.
- Sum family dead in production: covered by TOPO(b); fixture-only
  shapes do not count.

**Inquiry (`4e329c772`):**
- L3 hardcoded (30/-999): covered by INQ-1.
- L6 absent (no resolution): covered by INQ-2(a).
- Misleading-evidence lock-in: covered by INQ-2(b).
- Arbitrary disambiguation: covered by INQ-3.
- No cross-episode learning: covered by INQ-4.

**Revision (`687ba0219`):**
- Single-schema literal patch: covered by REV-1 (2+ topologies).
- Content always copied from observation: covered by REV-1
  derived-content condition.
- No deletion without insertion: covered by REV-1 diversity set
  (must include reuse-without-insertion) and REV-3 (revert).
- Guards lack provenance (cannot edit predicates): covered by
  REV-1 diversity set (guard-predicate edit listed).
- t2_trial never invoked on revision path: not directly named,
  but REV-1's diversity (multi-step, borrow) effectively requires
  search machinery; a straight-line patch cannot produce the
  required variety.

**Synthesis (`42b4dfa91`) shared pattern (enumerated-schema /
filled-slot):** covered structurally by ADV + TOPO + the
derived-content conditions jointly. No single bar names the
pattern, but the combination (post-freeze worlds the builder
never saw, shapes beyond fixtures, content derived from hidden
structure rather than event literals) makes filled-slot
satisfaction impossible: there is no fixed schema whose slots,
filled from event literals, produce the required novel shapes
with checker-computed content.

**Interaction (`9009ff259`): no closed feedback loops; promoted
graphs never executed; inquiry dead-end.** Covered by CON-2
(reuse requires execution of promoted graphs), INQ-4 (inquiry
reuse), REV-3 (repair history). The bars do not explicitly
require "closed loops" as an architectural property, which is
correct: they require the observable behaviors (reuse, revision
of inquiry, successive revision) that only a looped architecture
can produce.

**H3 (procedure ownership; `94cecdba4` cheap check: no policy
write paths exist).** The bars are behavior-only by design
(section 1: "Observable behavior only. No bar prescribes a
search algorithm, a proposal mechanism, an internal
representation, or a decision criterion."). A system could in
principle pass all bars with researcher-authored policies that
happen to generalize to the sealed worlds. In practice ADV
makes this infeasible: the builder cannot pre-author policies
for worlds authored after the freeze. The bars test the
capability that learner-owned procedures would produce, without
mandating the implementation. This is the right level for kill
bars; procedure-ownership audits belong in red-team review, not
in pass/fail thresholds.

**One minor gap:** the "verdicts without structures" finding
(`dedfad368`: learner records verdicts but not the structures
verdicts were about) is addressed implicitly (INQ-1's derived
content requires retaining uncertainty structure; REV-2's
retained set requires provenance), but no bar explicitly checks
that trial candidates, uncertainty alternatives, or repair
options are retained in learner state. If a TNN-3 passes the
behavioral bars while still discarding intermediate structures,
a future generation would hit the same wall. Consider, at
prereg freeze time, adding a state-retention probe to the
governance audit (not a kill bar): dump learner state after
each sealed scenario and verify that candidate structures
(tried/rejected graphs, alternative guides, repair options)
are present with provenance. This is audit-grade, not
bar-grade, because the exact retention format is
implementation-specific.

## 7. Summary judgment

The draft is well-constructed. Every bar:

- names a concrete TNN-2 failure mode as its target;
- states an observable pass criterion with no judgment calls;
- is achievable by a genuinely general mechanism within the
  frozen ISA;
- deterministically fails a clever TNN-2-type L2 system;
- specifies 3/3 byte-identical verification.

The discrimination check (section 8 of the draft) is honest:
TNN-2 passes only the C0-A retention bars and fails everything
else, which bounds the impossibility risk.

Recommendations for the frozen version:

1. Raise inquiry scenarios to 5+ (Q1).
2. Specify the TOPO(b) log format in the prereg (Q2).
3. Fix a single signature function in the prereg (Q3).
4. Keep INQ-3 as drafted (Q4).
5. Keep all bars as kill bars, not falsifiers (Q5).
6. Retain C0-A as regression bars without strengthening (Q6).
7. Add a state-retention probe to the governance audit
   (section 6 minor gap; audit-grade, not bar-grade).
8. Explicitly freeze the state-dump format in the prereg so
   reference checks (CON-2, INQ-4) are mechanical.

Nothing in this review weakens, amends, or freezes any bar.
DRAFT-NOT-FROZEN stands. Micah decides.

## Verdict

KILLBAR-REVIEW-COMPLETE.
