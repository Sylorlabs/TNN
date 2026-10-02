# PREREG_F1: Generic Executable Semantics Frontier Evaluation

Lane: F1 (generic executable semantics frontier), wave wave-20261001-2021pdt.
Phase 1 deliverable: writing only. No implementation written, no experiments run.

## 0. Step 0 (toolchain guard)

Safebin activated and verified before any other work; recorded in
`NAMECHECK.md` Step 0 of this lane. PATH is safebin only. `which python3`
prints nothing. All work in this lane is pure Zag compiled by the pinned
znc, or shell invoking znc, running binaries, git ops, cmp/sha256sum, and
file moves/copies. Any forbidden executable invocation is automatic
PROCESS-FAIL and will be reported honestly. This prereg is authored as
documentation only; no code was written or executed to produce it.

## 1. Scope and non-duplication

F1 is the frontier-evaluation side of the generic executable semantics
work. It does not implement the TNN-3 substrate hypotheses: TNN3H1
(learner-named procedure objects) and TNN3H5 (generic supersession
transition) are writing and freezing their own preregs in parallel this
wave, and this lane duplicates none of their substrate work. A candidate
under F1 may be a TNN-3 build that incorporates H1/H5, or a standalone
experiment; in both cases the kill bars in this prereg govern whether any
result may be claimed as L3 generic executable semantics. The standing
owner criterion: a procedure (or executable structure) that TNN creates
and that the programmers did not supply.

## 2. Re-derived adversary lessons (what the prereg must survive)

The two downgrades that motivate this prereg were re-derived from the
primary records, not cited from memory.

REPEXPAND-1 (BUILD-PASS, then DOWNGRADED to L2+): the COUPLED node
(type tag 7) was a researcher-written semantic case in source; the
relation search scanned a fixed researcher-enumerated family {EQ, MUL,
ADD} in a fixed order; the node shape (spec run plus two content runs
with runtime-bound length slots) was researcher-designed. The learner
supplied only which relation from the menu and which lengths to bind:
parameter filling (L1), not representational invention (L3). Kill
pattern: researcher-authored semantic case plus disguised fixed-order
menu, with data-determined parameters mistaken for invented semantics.

H-PROCLANG1 (BUILD-PASS, then DOWNGRADED to L2+): the COND(t,A,B)
reification schema (SPLIT_SCAN over integer thresholds, then REIFY)
was researcher-written in Phase B. The learner found the threshold t
and the sub-programs A, B, but the "invented operator" was the
researcher's own semantic case. Kill pattern: researcher-authored
invention schema with learner-filled parameters, presented as
operator invention.

PI_REV2 standing attacks (attached to its BUILD-PASS, still live kill
vectors): S1, the primitive-construction kit whose only possible output
is a byte-equality test at a position is a researcher-added primitive
shaped exactly for the test worlds; S3, the diagnosis space (64
positions by 256 bytes) is finite, so the composed conditional is menu
selection at one remove; S4, the frozen position-ascending rank matches
the tester's intent and was never tested against a world needing a
different bias; the F2 "adversary" was the same implementer choosing
from a set the implementer knew. Lesson: a builder-run adversary is
not independent, and a finite kit is a menu no matter how the rank is
described.

Forbidden response: the researcher may not add SUB, DIV, PARITY,
2-threshold COND, or additional researcher-authored semantic cases in
response to downgrades. Recreating the treadmill at the L3 frontier is
forbidden. The L3B adversary continues: a finite menu means redesign
toward incremental construction, never menu expansion.

## 3. The claim under test

An L3 generic-executable-semantics claim asserts: the learner, through
experience, constructed an executable structure (procedure, graph, or
equivalent) whose semantics reside in learner-created persistent state;
whose exact final topology emerged incrementally and was not chosen
from a finite researcher-enumerated solution family; which the frozen
mechanism can rebuild in materially different forms on sealed worlds
designed after freeze by an independent adversary; and which improves
later cognition (it is reused, not merely exhibited). All four of
Micah's Criterion 0 clauses are conjunctive: failing any one clause
kills the L3 claim. A claim passing all other bars but failing any
C0 clause is bounded L2+ at most.

## 4. Frozen kill bars: Criterion 0 operationalizations

### K-C0A: runtime-defined semantics (source-audit criterion)

Positive requirement: every executable element of the learner's final
created structure traces, in the white-box execution trace, to a frozen
ISA primitive node whose execution path contains no researcher-written
semantic branch. The semantics of the structure live in learner-created
persistent state; source holds only generic execution and construction
machinery.

Audit procedure: full-text inventory (grep over the committed source at
the implementation-freeze hash) of (i) all researcher-named node type
tags, (ii) all branches dispatching on such tags, (iii) all
reification or construction schema sites. The adversary annotates each
site. The audit is committed as evidence.

What the adversary must show to kill: one source site (file, line,
committed hash) where a researcher-named semantic case executes
behavior of the final structure and that behavior is not decomposable
into the frozen ISA primitives alone. One such site kills the L3
claim. Examples that kill: a COUPLED-style type tag with
researcher-written execution semantics; a COND-style reification schema;
a SPECIALIZE operator whose output shape is researcher-fixed.

PASS threshold: the audit finds zero such sites, and the execution
trace of the final structure resolves every step to an ISA primitive.

### K-C0B: open structural form (probe-menu equivalence attack)

Positive requirement: the final structure was not chosen as one
complete answer from a finite researcher-enumerated solution family;
its exact final topology emerged incrementally.

Attack protocol (frozen):
1. Before any sealed run, the adversary writes an attack prereg
   declaring a finite family F derived from the frozen source alone
   (no learner runtime state): an explicit generator or list, plus a
   containment argument that the construction machinery's output
   space is a subset of F. Post-hoc enumeration (writing F after
   seeing the learner's structure) does not count.
2. The adversary exhibits one f in F and shows exact I/O parity with
   the learner's final structure S on the full sealed probe set
   (at least 60 probes: the hidden set plus the transfer set).
3. Kill requires both exact parity on all probes and a sound
   containment argument.

Two automatic kills (no parity test needed):
- The source contains a fixed-order scan over a researcher-enumerated
  relation or candidate set whose result is reified as structure
  (the REPEXPAND {EQ, MUL, ADD} pattern). That scan is itself the
  exhibited F.
- The construction kit has a finite researcher-shaped output set
  (the PI_REV2 byte-equality-only pattern, or any kit whose outputs
  are all instances of one researcher-fixed shape). That kit is
  itself the exhibited F.

Survival also requires positive evidence: the white-box trace shows
at least two incremental construction events for S (each adding one
ISA-level element, episode-indexed after the triggering failure), and
S contains at least one node-plus-edge pattern with no textual
counterpart in the frozen source (verified by grep; absence required).

PASS threshold: no adversary-declared F reproduces S with exact
parity, no automatic-kill pattern is present, and the positive
incremental-construction evidence holds.

### K-C0C: multiple unforeseen forms (post-freeze adversarial family protocol)

Protocol (frozen):
1. Implementation freeze is committed (source SHA-256 recorded). No
   source edits, no recompilation, no handler/mode/semantic-case
   additions are permitted afterward for the sealed run.
2. An independent adversary (a different agent than the builder, with
   no access to the builder's private reasoning; reading committed
   builder source is allowed) designs at least two new evaluation
   families. For each family the adversary preregisters the structural
   dimension in which it differs from the training family
   (control-flow shape, arity, data-flow topology, or composition
   pattern: the predeclared material-difference dimension).
3. Family manifests (SHA-256) are committed before any sealed run.
   The builder lane never sees family files before execution.
4. The learner runs the frozen binary. Each family ships at least 30
   hidden probes, disjoint from training and from each other.
5. Per family, PASS requires at least 80 percent correct AND a
   white-box structure that is not isomorphic to the training-family
   structure up to parameter renaming. The adversary preregisters the
   isomorphism test: a graph comparison showing at least one
   difference in the predeclared material-difference dimension.

Kill conditions: any family scores below 80 percent, or the
constructed structure is isomorphic to the training structure. In the
isomorphism case the family is judged a near-variant, not a material
difference: the run does not count as a C0-C pass, the adversary
redesigns, and the builder may not patch in response. FW1-FW9 style
regression sets do not satisfy C0-C; only post-freeze
adversary-designed families count.

### K-C0D: cognitive reuse (transfer task family, minimum transfer gain)

Positive requirement: the invented structure improves later cognition:
transfer, prediction, procedure learning, causal inference, memory,
planning, or sample efficiency. Existence alone is insufficient.

Transfer family (frozen): sealed, disjoint from training, with changed
surface representation (renamed tokens, shifted coordinates, distractor
content, or a different domain encoding). Designed by the independent
adversary post-freeze and preregistered with the cognitive gain it
tests. At least 30 hidden transfer probes.

Frozen bars:
- Treatment (created structure active): at least 75 percent on the
  transfer probes.
- Control (same frozen binary, same experience, created structure
  ablated or removed; equivalently the pre-invention learner
  snapshot): at most 40 percent on the same probes.
- Minimum transfer gain: treatment minus control is at least 35
  percentage points.
- Reuse-invocation check: white-box must show the created structure
  executed at least once on the transfer family. Zero executions
  fails C0-D regardless of scores.
- Memorizer control: an exact-match table baseline with the same
  example budget must score at most 40 percent on the transfer
  family. Parity with treatment (within 10 points) kills C0-D: the
  advantage is storage, not the invented structure.

Kill conditions: gain below 35 points, control at or above 75 percent
alongside treatment (structure not load-bearing), zero reuse
executions, or memorizer parity.

## 5. The 12 L3 criteria mapped to frozen kill bars

1. Final procedure not in source: K-C0A, K-C0B.
2. Not enumerated as one complete candidate: K-C0B.
3. Created after experience: K-TRACE (below).
4. Present in persistent learner state: K-STATE (below).
5. White-box trace explains creation: K-TRACE.
6. Hidden instances solved: K-HIDDEN (below).
7. Ablation destroys the advantage: K-ABL (below).
8. Reused later: K-C0D reuse-invocation and transfer bars.
9. Transfers across changed surface representation: K-C0D transfer
   family with changed surface.
10. Beats simple memorization/search controls: K-BASE (below).
11. Survives independent red team: the adversary battery defined in
   section 4, run by the independent adversary post-freeze.
12. Revisable after counterexample: K-REV (below). If K-REV fails
   while all else passes, the claim is bounded L2+, not L3.

K-HIDDEN: at least 90 percent on at least 30 hidden probes, disjoint
from training, extending beyond the training range in at least one
dimension. Frozen before the run.
K-TRACE: white-box trace lines show the trigger (a measured
prediction failure), at least two incremental construction events with
episode indices after the trigger, and the final structure identity.
No structure isomorphic to the final one may be present in learner
state before the first construction event. The trace must explain the
creation, not merely log it.

K-STATE: the created structure is present in the end-of-run state dump,
addressable and executable by the frozen binary.

K-ABL: removing or disabling the created structure drops hidden-set
performance by at least 40 percentage points on the same hidden set.
The ablation must remove the structure only, not capacity, compute,
or unrelated machinery.

K-BASE: a memorizer (exact-match table) and a bounded brute-force
search control, each with the same example budget as the learner,
score at most 40 percent on the hidden set. If either matches or
beats the learner, criterion 10 fails.

K-REV: a counterexample family (adversary-designed, post-freeze,
contradicting the created structure) is presented. The learner must
revise or retire the structure through its own construction process:
white-box shows the old structure superseded and not executed after
supersession, and the revised structure scores at least 80 percent on
the counterexample family's hidden probes. Revision means the
learner's own construction re-running or superseding, never a
researcher patch. A frozen rule that overrides the old output without
re-derivation fails K-REV.

## 6. Sealed evaluation protocol (ordering is load-bearing)

1. The coordinator commits this prereg alone. Its SHA-256 and commit
   are recorded in the wave record before any implementation exists.
2. Implementation is written only after that commit. The
   implementation freeze commit records the source SHA-256 and
   `git diff --stat` against the frozen baseline.
3. The independent adversary writes an attack prereg (declaring the
   menu-equivalence family F with its containment argument, the C0-C
   families with their material-difference dimensions and
   isomorphism tests, the C0-D transfer family with its cognitive
   gain claim, and the K-REV counterexample family) and commits it
   before any sealed run.
4. Family manifests (SHA-256) are committed. The builder lane never
   sees family files before execution.
5. Sealed runs use the frozen binary only. Full sealed evaluation is
   executed 3 times; outputs are byte-identical and hashed.
6. Verdicts are computed by frozen Zag scripts against the frozen
   bars. No bar may be altered after the sealed run begins.

Any violation of this order, any post-freeze source edit before the
sealed run completes, or any bar alteration after runs begin, voids
the prereg: the results cannot be adopted that wave. Unverifiable
ordering voids the prereg.

## 7. Construction mechanism (design level)

A candidate mechanism must satisfy all of the following at the design
level. These are frozen constraints on any implementation that claims
to be evaluated under this prereg.

- The frozen protected ISA is the only executable vocabulary:
  ALLOC, READ, WRITE, LINK, COPY, COMPARE/EQ, ADD, BRANCH,
  APPLY/EXECUTE, plus EXECUTE(root, frame) and any frozen amendments
  approved by Micah before the implementation freeze. No other
  operation may appear in a constructed graph.
- Node semantics are ISA op semantics only. Source holds generic
  execution and construction machinery; no dedicated
  researcher-written semantic branch, case, type tag, or reification
  schema anywhere in the cognition path.
- Incremental growth: each construction event adds one ISA-level
  element (one node or one edge). No event instantiates a multi-node
  researcher-shaped template. The exact final topology emerges from
  the sequence of events.
- No enumerated candidate families in source: no template lists, no
  finite candidate generators, no fixed-order scans over
  researcher-enumerated relation sets, no construction kits with
  finite researcher-shaped output sets.
- Construction is triggered by the learner's own measured prediction
  failure through a generic monitor. Trigger constants are disclosed
  in the implementation commit and frozen at implementation freeze;
  tuning them after seeing sealed families voids the evaluation.
- Created structures persist in learner-created state, are
  addressable (nameable) by the learner, are reusable across
  instances, and are revisable or supersedeable on counterexample.
- Procedure and causal rule remain on the path toward being the same
  executable graph type with different evidence and lifecycle edges,
  not separate engines. Separate construction engines for procedures
  versus causal rules would violate the one-system rule.

## 8. Negative controls

These controls demonstrate that each kill bar has teeth. A bar that
cannot fire on a known-bad pattern is miscalibrated.

- NC-A (audit teeth): a control mechanism built on the REPEXPAND-1
  or H-PROCLANG1 pattern (researcher semantic case plus
  learner-filled parameters) must be killed by K-C0A.
- NC-B (menu teeth): a control mechanism built on the PI_REV2
  pattern (finite construction kit with a fixed rank) must be killed
  by K-C0B, either by exhibited parity or by the automatic-kit kill.
- NC-C (freeze teeth): a control mechanism that only rebinds
  parameters of a single topology must fail K-C0C on a materially
  different family, and the isomorphism check must flag near-variant
  families as variants rather than passing them.
- NC-D (reuse teeth): a control mechanism whose created structure is
  never invoked on the transfer probes must fail K-C0D on the
  zero-executions check.
- NC-BASE (calibration): the memorizer control must fail to match
  treatment on both the hidden and transfer sets. If it matches, the
  task is miscalibrated: the bars are renegotiated in a fresh prereg,
  never weakened post hoc.

## 9. Determinism standard

The full sealed evaluation runs 3 times. All 3 raw outputs are
byte-identical (cmp-verified); SHA-256 of each raw output is recorded.
Zero randomness in decision paths. Any pseudorandom generator uses a
seed that is a frozen constant recorded at implementation freeze. Any
nondeterminism voids the run.

## 10. Toolchain purity

Pure Zag for implementation, harnesses, verifiers, scorers, fixture
provisioning, and analysis, compiled by the pinned znc. Shell invokes
only znc, runs compiled binaries, performs git ops, cmp and
sha256sum, and file moves or copies. No Python and no other
interpreter anywhere, including scratch and analysis. Authored docs
are byte-checked for zero em-dash bytes.

## 11. Architecture accounting

Relative to the frozen baseline recorded at implementation freeze:
cognition source lines added must be zero or negative; new hardcoded
semantic cases zero; new modes zero; new bridges zero; new routers
zero; new task-specific handlers zero. Capability-source delta must
approach zero: new capability comes from experience leading to new
learner state, not from new researcher-written machinery. Each sealed
run records the learner-state structures the learner created. Three
custom bridges around one boundary trigger architecture review and
block further bridge work.

## 12. Verdict rule and void conditions

- BUILD-PASS: all frozen bars pass. This is not a promotion. The
  candidate faces the adversary battery in section 4 (run by the
  independent adversary) before any promotion step. SURVIVES requires
  the full 11-step frontier pipeline.
- BUILD-FAIL: any kill bar fails. The failed bar and the evidence
  are named in the verdict.
- VOID: ordering violation, contamination, toolchain violation, or
  any forbidden researcher response (adding SUB, DIV, PARITY,
  2-threshold COND, or other researcher-authored semantic cases after
  a downgrade). A VOID verdict is terminal for this prereg:
  correction proceeds only as a fresh preregistration plus fresh
  sealed worlds, never salvage or amend-and-promote.

A frozen kill bar is never weakened to force a pass. Verdicts name
the exact frozen bars that governed them.
