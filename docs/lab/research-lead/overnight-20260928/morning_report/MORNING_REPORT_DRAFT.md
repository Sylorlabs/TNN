# TNN-2 Red-Team Cycle: Morning Report (DRAFT)

**DRAFT - FREEZE PENDING. FREEZE SCORE PENDING - DO NOT QUOTE.**
**KILL BARS DRAFT-NOT-FROZEN - AWAITING MICAH REVIEW.**
**UPDATE 2026-10-01 06:52 UTC: Prereg audit found the evaluator draft claims 5/9 but documents 4 passes. Correct score is 4/9, matching TNN-1. See section 8.**

Date: 2026-10-01. Assembler: Morning Report Assembler (assembly only, no
new analysis). All claims below are transcribed or compressed from the
committed reports listed in section 9. Nothing here is new analysis,
and nothing here invents a freeze score.

## 1. Executive summary

All three TNN-2 mechanisms (runtime executable-graph construction,
learner-originated inquiry, counterexample-driven revision) received
ATTACK-SUCCESS verdicts from independent red teams, and all three
failures reduce to one shared architectural pattern: the researcher
authored the schema and the learner fills runtime-chosen slots. A
degree-of-freedom audit found **zero** pure learner decisions in the
cognition path (5 mixed, about 240 researcher). Separately, a
structural analysis proved that no freeze score, even 9/9, can
establish C0-D (cognitive reuse), because promoted graphs are causally
inert at query time: every promotion shadows itself with a memoized
fact and the query path cannot read MAPs. The freeze evaluation draft
is internally inconsistent: it claims 5/9 but documents 4 passes
(FW1, FW2, FW4, FW5). The prereg-compliance audit (`8959a7c14`)
corrects this to **4/9, matching TNN-1**. Under the prereg criteria
(">4/9 confirms the diagnosis" vs "at or below 4/9 falsifies and
requires re-clustering"), the TNN-2 diagnosis is falsified and
re-clustering is required. The post-freeze adversarial battery
(GW1-GW8) is designed, sealed, and evaluated (GW-EVAL-COMPLETE 2/8 WORLD-PASS). TNN-3 kill
bars are drafted (DRAFT-NOT-FROZEN, six open questions banked). Ledger
stands at 159 claims with **zero L3 anywhere**.

## 2. The shared pattern: enumerated-schema / filled-slot

Named in the red-team synthesis (`42b4dfa91`). The identical division
of labor in all three mechanisms:

1. Researcher enumerates the possible (in source, before experience).
2. Learner fills the blanks at runtime (literals, cell indices, miss
   content from genuine data).
3. The filled schema is recorded as learner state (real persistence,
   real provenance, real rejection traces).
4. The learner never chooses among schemas, because there is only
   ever one.

Micah's standing question ("What part of the topology was actually
chosen by the learner?") gets the same answer thrice: **the operands,
never the topology.** TNN-1 was fixed templates with fixed content.
TNN-2 is fixed templates with variable content. The advance from
TNN-1 to TNN-2 is real (variable content, runtime rejection,
persistence, provenance) and it is exactly one rung short of L3.

Evidence per mechanism (synthesis section 2 tables):

| Mechanism | Researcher chose | Learner chose | Missing |
|---|---|---|---|
| Construction | grammar, order, bounds, oracle | literals, which candidate | choice of grammar |
| Inquiry | guide constants (30/-999), no resolution schema | miss trigger, (s,r) content | derived discriminating need, resolution |
| Revision | repair topology, always-literal replacement | operands (cell, value) | search over repair topologies |

The alternative-explanation attacker (`ccee9e5e6`) compressed this to
its floor and could not go simpler: **form from researcher, content
from learner.** TNN-2 is answer-fed, not answer-derived: construction
receives `expected` from the QUERY event, inquiry's action is the
constant 30, revision stores the observed literal. The learner's total
degrees of freedom compress to indices and literals. The unified
hypothesis also predicts the genuine parts (honest guard rejections,
real ACT machinery, real topology edits), because content-layer
activity is real; retrieval-only was rejected as too simple to predict
runtime composition exceeding the old template ceiling.

## 3. Per-mechanism findings

**Construction (`340e94e3e`, CONSTRUCTION-ATTACK-SUCCESS).** `t2_trial`
searches exactly three researcher-authored linear graph families
(chains, sums, counts; sums dead in production because its type-8 gate
is created only inside test `t_p2`). All wirings, slot assignments,
search order, and bounds are fixed in source. Chain depth capped at 4;
a 5-hop chain is behaviorally unrepresentable. DEC is never emitted.
The verifier receives the expected answer from the environment and
accepts the first fixed-grammar candidate matching it. Verdict: L2
structural learning (bounded), fails C0-B/C0-C.

**Inquiry (`4e329c772`, INQUIRY-ATTACK-SUCCESS).** Miss trigger,
uncertainty-node creation, and guide-to-POLICY_ROOT linkage are all
genuinely learner-originated and reachable from empty state
(L1/L2/L4 PASS). But the "discriminating need" is hardcoded:
action 30, content -999, literals at `miss_inquire` lines 805-808
(L3 FAIL). No production path ever resolves an uncertainty or
supersedes a guide (L6 ABSENT); stale guides stay ACT-eligible
forever. Under ambiguity selection is arbitrary; under misleading
evidence the system locks in. Honest characterization: a miss flag
plus a constant action, not discriminating inquiry. It satisfies the
letter of K-T2-4/K-T2-5 (chain structure present, 30 read from a
guide slot, 30 not 0) but not the spirit: a prereg spec gap the
inquiry-generalization analyst traced to bars that tested structure,
not question content.

**Revision (`687ba0219`, REVISION-ATTACK-SUCCESS).** `t2_revise_graph`
implements exactly one repair topology: find a BRANCHEQ-guarded
SETREG, tombstone it, insert a SETREG containing the just-observed
literal, rewire guard to new to successor. It cannot perform
delete-only, insertion-only, branch retargeting, loop/sequence
conversion, guard editing, or coordinated multi-step repair. `t2_trial`
is never invoked on the revision path. The learner chooses the cell
and literal; the researcher chose the repair topology. Corrected
content is memorized from the observed value, not derived: the
T2-REVISE trace is L0 storage dressed as revision. C0-A/B/C FAIL,
C0-D unestablished. Verdict: L1 parameter filling.

Ledger implications (`af093bd94`): no L3 claim survives for any
mechanism. The three ATTACK-SUCCESS verdicts do not alter the frozen
TNN2-BUILD-PASS (C144) or TNN2-REPRO-PASS (C145); they are
mechanism-generality results, not capability results, and neither
confirm nor break any frozen kill bar.

## 4. The zero-decision result

The degree-of-freedom enumerator (`d2af26581`) audited every decision
point in TNN-2's cognition path (lines 1-917 of the frozen source):

- **Pure LEARNER decisions: 0.** Nowhere does the learner originate
  a choice.
- MIXED (researcher fixes space and rule; state/data selects): 5
  (activate winner, evict victim, trial winning candidate,
  literal embedding, ev_act action).
- RESEARCHER: about 240 (37 layout/type constants plus fixed
  templates, orders, rules, schemas per function).

Two findings were flagged to the red teams: the sum phase is gated
on a type-8 node no cognition-path code can create (an entire
assembler branch switched on by external scaffolding), and
verification is answer-keyed: `expected` flows driver to `ev_query`
to `t2_trial` to `t2_try_verify`, and the loop keeps the first
candidate matching it. The system's largest capability lever is not
learner-owned. Ten researcher decisions were identified as movable
to learner state without new opcodes; the prioritizer (`f70ab617c`)
ranked them by impact/difficulty ratio. **Top 3 quick wins:**
(1) Trial phase order (ratio 2.0, cleanest locus move);
(2) Comb gate (ratio 1.5, resurrects dead sum branch);
(3) Repair target selection / operator choice (ratio 1.0, core
revision fix). Explicitly not quick wins: the acceptance criterion
(#9, H2 oracle problem, needs masked probes first), sum subset
order alone (#3, moot without the comb gate), guide probe content
(#7, theater without connecting inquiry to a consumer). **Key
insight:** "zero learner-owned criteria is the disease; zero pure
decisions is the symptom." Every MIXED point uses a
researcher-fixed criterion (argmax bid, first-to-verify, scan
order) over learner-supplied data. The high-value moves relocate
criteria, not just parameters.

## 5. C0-D structural failure

The C0-D analysis (`8bfb80fdd`) verified the interaction analyst's
claim by exact call-site enumeration and added a second independent
sufficient cause:

1. **Promotion shadows itself.** `promote_graph` (line 541) calls
   `ev_teach_in`, inserting an exact-match fact for the same (s, r)
   it just built a graph for. `ev_query` answers via `activate`,
   which scans tag-1 facts only; MAPs (tag 20) are structurally
   invisible to the query path. A promoted graph executes exactly
   twice in its life (trial verification, revision re-verification)
   and never to answer a query. Answers come from memoized facts;
   MAPs are derivation certificates the query path cannot read.
2. **Graphs are value traces, not portable procedures.** Assembled
   cells embed gathered literals; the relation lives only in DEP
   provenance. The frozen 4-op ISA has no relational-dereference
   operation, so subject-general procedures are inexpressible. The
   transfer probe P2 confirms behaviorally: executing subject 1's
   graph on subject 7 returns -999999.

Consequences (verbatim from the report): **no FW1-FW9 score, even
9/9, can establish C0-D for construction, since the output is
causally inert at query time regardless of score.** Even a perfect
freeze score would be fact-memoization performance, not procedure
reuse. Execution is necessary but not sufficient for C0-D: it would
make reuse testable, not true. The minimal wiring that would make
C0-D structurally possible (MAP-lookup branch in `ev_query`, delete
the shadow teach, a MAP liveness/shadowing policy, contradiction
retargeted at the MAP) is sketched for TNN-3 only; the Layer-2
value-trace fix touches the protected-core boundary and is banked
as Micah's decision.

## 6. Three hypotheses for the root bottleneck

From the synthesis (`42b4dfa91` section 5), three structurally
different, experimentally separable hypotheses, with the recommended
discrimination order: **H3 check first, then H2 probes, then H1
widening** (widening before fixing the oracle is the treadmill
Micah forbade; the interaction analyst concurs).

- **H1 (grammar):** the output space of every mechanism is
  enumerated in source. Fix: one open recursive
  graph-construction substrate whose output space grows with
  learner state (composing previously promoted graphs, per the
  MUL Rung B precedent). This widens all three mechanisms at once.
  Caveat: the composition operators, remapping rules, order, and
  bounds stay researcher-authored, so the "larger finite menu"
  objection survives at the operator level (MUL comparison,
  `e2e34a4ac`).
- **H2 (oracle):** the environment supplies the answer, so nothing
  must be discovered. Fix: learner-internal prediction-based
  acceptance (masked verification, derived repair content). This
  creates genuine discovery pressure across all three mechanisms
  and explains why inquiry never computes a discriminating need:
  under an oracle there is never a need to ask a good question.
- **H3 (procedure ownership):** the mechanisms' operating
  procedures are source code, not learner state. Fix: procedures
  as learner-built graphs. The H3 probe (`94cecdba4`) executed
  the cheap policy-revisability check: **no production path can
  modify the trial search order, guide schema, or repair topology
  from experience**, confirming H3 as a structural fact of frozen
  TNN-2. The probe also found the 4-op ISA's effect domain is
  frame registers only, so full H3 is a protected-core boundary
  decision (banked for Micah); the H3-lite design (`22197da2c`)
  parameterizes the three decision points as learner-state policy
  nodes without any ISA change and moves the locus of control,
  not scores.

The inquiry caveat (synthesis section 3): even with an open
constructor, the learner must decide which discrimination
structure to build and when a guide is resolved. That
informativeness criterion is itself a schema that could be
researcher-authored again. Where it lives is banked as the
central design question for any inquiry work.

## 7. What TNN-3 needs

- **Kill bars drafted** (`76231baa8`, DRAFT-NOT-FROZEN):
  K-T3-ADV (adversarial process with post-freeze authorship
  verification), K-T3-TOPO (learner-chooses-topology audit via
  structural signatures), K-T3-CON-1/2 (two structurally
  different sealed constructions with derived content; sealed
  reuse), K-T3-INQ-1/2/3/4 (derived discriminating need;
  evidence updates behavior; ambiguity swap test; cross-episode
  reuse), K-T3-REV-1/2/3 (two structurally different sealed
  repairs with derived content; retained-set regression;
  successive revision with revert). The achievability review
  (`eb354e3a2`) judged all 11 bars achievable by a genuinely
  general mechanism, deterministically failed by a clever L2,
  sound in verification, with no blocking inconsistencies and no
  redundancy. The "two structurally different" requirement is
  generalized across all three mechanisms and closes the K-T2-6
  process loophole ("in at least one test" admitted the
  single-schema operator).
- **H3-lite designed** (`22197da2c`): three learner-state policy
  nodes (trial search order, guide template, repair dispatcher)
  with production read and write paths, plus a draft K-H3
  prereg bar (every structural decision lists its learner-state
  fields, production write path, triggering event, and a sealed
  test showing variation). Explicit non-deliveries: procedures
  remain researcher code, the repair family stays
  researcher-enumerated, the oracle remains, and no FW1-FW9
  improvement is predicted.
- **Target selection designed** (`01c2aacfe`): the fourth
  H3-lite site and the underexploited site of learner authority
  (MUL Rung B never had to choose among procedures; TNN-2
  accumulates many MAPs). Central dependency: **target
  selection is downstream of the reuse path**; the two signals a
  learner-authored policy needs (reuse history, composition
  outcomes) do not exist today.
- **Reuse path required.** The foundational dependency for both
  C0-D and target selection. A reuse-path designer is active.
- **Roadmap synthesized** (`67a420cca`): minimal TNN-3 is not a
  full L3 architecture; H3-lite is a stepping stone with marked
  limits (watch for "revisability theater"); three biggest
  risks are prereg spec gap redux, H3-lite as theater, and
  solving H1 before H2. **Recommended order:** Step 0 H3 check
  (done, confirmed); Step 1 H2 masked verification probes (no new
  machinery); Step 2 H3-lite policy parameterization; Step 3
  repair-proposal generator plus inquiry resolution; Step 4 H1
  widening (ONLY after Step 1, to avoid the treadmill Micah
  forbade); parallel track reuse path for C0-D; full H3 pending
  Micah's protected-core governance decision.

## 8. Open items

1. **Freeze evaluation.** The CORE-FREEZE-TNN2 evaluator is still
   running. Its reconciled result is not committed. **NO FREEZE
   SCORE IS RECORDED OR QUOTED HERE.** Per the TNN-3 prerequisites
   analyst (`f795807cc`) and the ledger (`af093bd94`): the
   evaluator's on-disk draft is internally inconsistent (claims a
   5/9 FW score but lists only 4 passing worlds; marks K-FZ2-4
   PENDING while the draft verdict line says COMPLETE). The
   prereg-compliance audit (`8959a7c14`) found the 5/9 claim is an
   arithmetic error: the table documents 4 PASS (FW1, FW2, FW4,
   FW5) and 5 FAIL. **Correct score is 4/9, matching TNN-1.**
   Under the prereg (">4/9 confirms the diagnosis" vs "at or
   below 4/9 falsifies and requires re-clustering"), the TNN-2
   diagnosis is falsified. Six reconciliation steps are specified,
   including correcting the score, resolving K-FZ2-4, completing
   the W battery, and per-cluster analysis. A re-clustering
   drafter is preparing the required analysis. Seal integrity was
   verified independently (`0c97a669a`): all 16 files intact,
   hashes match, git clean, seal commit strictly precedes the
   freeze prereg. Interpretation framework: per Micah's ruling
   FW1-FW9 are a regression/targeted-repair battery for TNN-2
   (designed after seeing TNN-1's failures), so even 9/9 would not
   establish broad generality or L3; the honest summary line is
   "capability improved within the researcher-enumerated envelope;
   the envelope is unchanged in kind." A freeze-interpretation
   drafter is preparing honest templates for each possible
   outcome.
2. **Post-freeze adversarial battery.** Design complete and sealed
   (`e409f5eea`, ADVERSARY-DESIGN-COMPLETE): **GW1-GW8**, designed
   from the public architecture claim only, pure-Zag generator,
   anti-smuggling scan PASS, no new opcodes required, TNN-2
   unmodified. GW1 depth-5 chains (attacks the depth ceiling);
   GW2 cyclic executable structure; GW3 hierarchical reuse plus
   revision propagation; GW4 guard retarget instead of value
   replacement; GW5 inquiry-gated construction, two stages with a
   responder contract; GW6 inquiry discrimination and retirement;
   GW7 A/B/C interference; GW8 revision lifecycle with revert.
   Predictions frozen in ADVERSARY_DESIGN.md. **GW-EVAL-COMPLETE 2/8 WORLD-PASS**
   (three runs per world, authorized, no TNN-2 modifications). These are the important generality test, per
   Micah's directive.
3. **Six open questions for Micah** (from the kill-bar draft,
   `76231baa8` section 11; achievability review `eb354e3a2`
   section 4 gives a recommendation on each, but Micah decides):
   (1) world counts, review recommends raising inquiry to 5+
   scenarios; (2) K-T3-TOPO(b) builder signature-logging burden,
   review recommends keeping with a specified log format;
   (3) structural-signature function per-world vs fixed,
   review recommends one function fixed in the frozen prereg;
   (4) whether K-T3-INQ-3 is too prescriptive, review says keep
   as drafted; (5) kill bars vs falsifiers, review says keep all
   as kill bars; (6) C0-A regression bar strength, review says
   retain without strengthening.
4. **Protected-core boundary decisions banked for Micah:**
   whether the ISA may expose structural effect ops (ALLOC,
   field WRITE, LINK, KILL, node/edge READ), needed for full H3;
   and the Layer-2 value-trace fix (relational dereference),
   needed for portable reusable procedures.

## 9. Ledger state

Canonical ledger (`canonical_ledger/CLAIM_LEDGER.md`): **149 to 159
claims** (`af093bd94`, red-team cycle appendix C150-C159).

- C150 construction ATTACK-SUCCESS (`340e94e3e`); C151 inquiry
  ATTACK-SUCCESS (`4e329c772`); C152 revision ATTACK-SUCCESS
  (`687ba0219`).
- C153 compression analysis (`b2a6ae82c`): 1591 lines, about 103
  dead-in-cognition, sum assembler dead in production; 1200-line
  ceiling needs architectural deletion, not trimming.
- C154 governance audit PASS (`622363372`).
- C155 frontier scout, 17 ranked questions (`65effc909`).
- C156 revision generalization analysis (`edbb0e9b5`): five
  structurally different repair topologies enumerated; K-T2-6
  process loophole documented ("in at least one test" admitted the
  single-schema operator); future bars must require two
  structurally different demonstrations.
- C157 red-team synthesis (`42b4dfa91`): enumerated-schema /
  filled-slot; H1/H2/H3 with discrimination experiments and
  recommended order.
- C158 alternative-explanation attack (`ccee9e5e6`): form from
  researcher, content from learner; "answer-fed, not
  answer-derived."
- C159 inquiry generalization analysis (`dedfad368`): derived
  questions possible within the frozen ISA; trial discards its
  candidates before `miss_inquire` runs; resolution via existing
  type-3 supersession; shared cause note: learner state records
  verdicts but not the structures verdicts were about.

Aggregate: **zero new SURVIVES. L3 achieved anywhere: still zero.**
BUILD-PASS totals unchanged.

## 10. Provenance of this assembly

All claims transcribed or compressed from committed, read-only
sources on branch `tnn-native-lab` (local only, nothing pushed):

| Claim | Source commit | Deliverable |
|---|---|---|
| Construction ATTACK-SUCCESS | `340e94e3e` | `tnn2_redteam_construction/CONSTRUCTION_REDTEAM.md` |
| Inquiry ATTACK-SUCCESS | `4e329c772` | `tnn2_redteam_inquiry/INQUIRY_REDTEAM.md` |
| Revision ATTACK-SUCCESS | `687ba0219` | `tnn2_redteam_revision/REVISION_REDTEAM.md` |
| Enumerated-schema / filled-slot | `42b4dfa91` | `tnn2_synthesis/REDTEAM_SYNTHESIS.md` |
| Answer-fed, not answer-derived | `ccee9e5e6` | `tnn2_altexp/ALTERNATIVE_EXPLANATIONS.md` |
| No unsupervised loop; interaction | `9009ff259` | `tnn2_interaction/INTERACTION_ANALYSIS.md` |
| 0 pure learner decisions | `d2af26581` | `tnn2_dof/DEGREE_OF_FREEDOM_MAP.md` |
| C0-D structural failure | `8bfb80fdd` | `tnn2_c0d/C0D_STRUCTURAL_ANALYSIS.md` |
| H3 feasibility; cheap check | `94cecdba4` | `tnn2_h3probe/H3_FEASIBILITY.md` |
| H3-lite design; K-H3 bar | `22197da2c` | `tnn2_h3lite/H3LITE_DESIGN.md` |
| MUL comparison; target selection | `e2e34a4ac` | `tnn2_mulcompare/MUL_COMPARISON.md` |
| Target-selection design | `01c2aacfe` | `tnn2_targetsel/TARGET_SELECTION_DESIGN.md` |
| TNN-3 kill bars (draft) | `76231baa8` | `tnn3_killbars/TNN3_KILLBARS_DRAFT.md` |
| Kill-bar review; 6 recommendations | `eb354e3a2` | `tnn3_killbar_review/KILLBAR_REVIEW.md` |
| TNN-3 roadmap synthesis | `67a420cca` | `tnn3_roadmap/TNN3_ROADMAP.md` |
| Ledger C150-C159 | `af093bd94` | `canonical_ledger/CLAIM_LEDGER.md` |
| Seal integrity verified | `0c97a669a` | `seal_integrity/SEAL_INTEGRITY.md` |
| GW1-GW8 designed and sealed | `e409f5eea` | `postfreeze_adversary/ADVERSARY_DESIGN.md` |
| Prereg audit; 5/9 corrected to 4/9 | `8959a7c14` | `freeze_audit/PREREG_COMPLIANCE_AUDIT.md` |
| Movable priorities; top 3 quick wins | `f70ab617c` | `tnn2_movable/MOVABLE_PRIORITIES.md` |

Standing conventions honored: pure Zag (safebin PATH, no forbidden
executables); no source edits to the frozen build; paper untouched;
sealed world contents never inspected; no em dashes; explicit
git pathspecs on commit.

*End of morning report draft. Verdict: MORNING-REPORT-DRAFT-COMPLETE.*
