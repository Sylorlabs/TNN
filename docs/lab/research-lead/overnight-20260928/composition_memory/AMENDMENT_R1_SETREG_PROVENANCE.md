# Amendment R1: SETREG-Provenance Through Extraction and Splice

Status: DRAFT-NOT-FROZEN. Amends COMPOSITION_MEMORY_DESIGN.md
(`19fa59b6f`). Design only; nothing built, nothing tested.

This amendment resolves red-team recommendation R1 from
COMPOSITION_REDTEAM.md (`3eeb0d78e`, verdict VULNERABLE). The design
was silent on SETREG-level provenance (prov->fact edges) through
fragment extraction and splice. This amendment specifies the
semantics, requires the R2 criterion fix, defines revision behavior
for composites, and unblocks the kill bar for the contrast test's
revision leg.

## 1. The decision: rebind, not preserve-verbatim, not strip

The red team identified two resolutions, both bad under the current
criterion: (A) preserve provenance verbatim, which enables direct V2
exploitation and cross-domain blame contamination; (B) strip
provenance, which makes composites revision-inert with no specified
staleness semantics.

This amendment adopts a third option: **provenance rebinding at
splice time**. The rationale:

A fragment is a computational pattern, not a persistent query. When
fragment F is extracted from a WORLD A graph, its SETREGs cite WORLD
A facts because those facts supplied values during the extraction
episode. When F is spliced into a composite C solving a WORLD D
problem, C does not read WORLD A facts; it reads WORLD D facts (via
F-slot fillings from the new problem's data) or uses cached constants
(via default fillings). Preserving verbatim prov->WORLD-A-fact edges
in C is semantically incorrect: it asserts a live data dependency
that does not exist. Stripping all provenance loses the genuine live
dependencies C does have (on WORLD D facts). Rebinding records the
actual data flow.

## 2. The Provenance Rebinding Rule

### 2.1 Extraction: preserve as historical metadata

When the extraction walk records a fragment's topology, it preserves
the SETREG provenance edges from the extraction episode as
**historical metadata**, stored in the fragment record alongside
F-provenance (world id, episode counter, parent graph). These edges
are explicitly marked historical, not live. They serve white-box
inspection, debugging, and SUF evidence (tracing a fragment's shape
to the episode that created it). They are NOT live dependencies of
the stored fragment: the fragment as a pattern has no outstanding
fact reads.

New fragment record field: F-setreg-hist, the list of (cell-index,
cited-fact-id) pairs from the extraction episode. This is read-only
after extraction; no production path modifies it.

### 2.2 Splice: rebind to actual data sources

When the splice operation instantiates a fragment into a composite,
it does NOT copy F-setreg-hist edges verbatim into the composite
graph. Instead, for each SETREG cell in the fragment whose value
slot is filled at splice time, it applies the following rule:

- If the slot is filled from the new problem's data, and that data
  originates from a live fact node f_new in the current learner
  state, the composite's SETREG gets prov->f_new. This is a live
  dependency: the composite genuinely reads f_new.
- If the slot is filled from the fragment's default filling (the
  stripped literal value recorded at extraction), the composite's
  SETREG gets prov=null. The value is a cached constant, not a live
  fact read. There is no dependency to track.

The splice operation must record, per rebound SETREG, which rule
branch applied (rebound vs nulled), as white-box trace data. This is
required for the revision-leg kill bar in section 5.

### 2.3 Why defaults get null, not old-fact pointers

A default filling is a copy of a value observed during extraction.
The composite using that default is not consulting the old fact; it
is using a constant the learner chose to retain. If the old fact is
later contradicted, the composite's constant does not become "wrong"
in any sense the revision path can act on: the constant was never a
claim about the old fact's current value, it was a computational
ingredient for a different problem. Pointing prov at the old fact
would manufacture a false dependency and reintroduce cross-domain
blame contamination through the back door. Null is the honest value.

Consequence: composites that rely heavily on default fillings have
sparse provenance. This is correct: their answers depend on constants
and on the rebound live reads, not on historical facts.

## 3. Criterion fix requirement (R2)

The V2 hole (`705833a27`, CONFIRMED) applies to composites under
rebinding, because rebound SETREGs are interior to the composite
with trailing value-transforming steps from chained fragments. The
acceptance criterion `out != -999999` (re-execution succeeded)
without checking `out == new_o` will accept wrong-but-running
revisions of composites exactly as the probe demonstrated for
hand-built graphs.

Therefore: **no preregistration for composition memory may be frozen
without the R2 criterion fix (or a strictly stronger fix) specified
as a build requirement.** R2, from COMPOSITION_REDTEAM.md section 5:

After revision re-execution, if the MAP's (s,r) equals the
contradicted fact's (s,r), require `out == new_o`; otherwise retain
the current `out != -999999` check.

This closes the probe-1 shape (identity-answer composites) without
breaking the probe-2 shape (computed-answer structures whose (s,r)
differs from the contradicted fact). It is explicitly a stopgap: the
general solution requires MAP contracts (answer-vs-fact dependency
semantics), which is TNN-3 scope per red-team R4. The preregistration
must name R2 as a stopgap and must not claim the criterion is
general.

Frozen TNN-2 is untouched by this requirement. R2 applies to the
future composition-memory build only.

## 4. Revision semantics for cross-fragment composites

### 4.1 Revision operates on composites, not fragments

When a fact f_new cited by a composite C's rebound SETREG is
contradicted, the revision path (`revise_on_contradict` or its
successor) operates on C as a MAP, using the standard blame walk
keyed on the rebound prov->f_new edges. The copy-and-commit
discipline applies: the revised composite is built in fresh cells
and committed atomically.

The fragment F from which C was partially built is NOT
automatically superseded. Rationale: F is a pattern; C is an
instantiation. If C's revision fails or produces a wrong-but-accepted
repair (blocked by R2), that is evidence about this instantiation
(the splice choice, the slot fillings, the problem match), not
necessarily evidence that F's shape is bad. Automatic fragment
supersession on composite revision would penalize reusable patterns
for single bad applications, destroying the reuse the mechanism
exists to provide.

### 4.2 Fragment quality is managed via F-utility, not supersession

The design's existing F-utility mechanism (section 2.4) is the
channel for fragment-level credit assignment: when a composite built
with fragment F is verified (success written) or fails verification
or revision (no success written, or explicit failure mark), F's
invocation counter increments and its success counter increments
only on composite success. Demotion past the retirement threshold
removes F from the candidate set without deleting it.

This amendment clarifies: composite revision outcomes (success,
safe failure, or R2-rejection) write to the participating fragments'
F-utility counters via the same path as composite verification
outcomes. A fragment whose composites repeatedly fail revision
demotes and retires. This is the learner-written, experience-driven
quality signal; researcher-authored fragment invalidation is not
added.

### 4.3 Cross-domain blame is eliminated by construction

Under verbatim preservation (red-team Case A), contradicting a
WORLD A fact would trigger revision of every WORLD D composite
whose fragments cited that fact, a blame fan-out across the
composition boundary. Under rebinding, this cannot occur: no
composite contains prov edges to facts outside its own problem's
domain, because every prov edge was either rebound to a live
current-domain fact or nulled. The reuse fan-out vector the red
team identified in section 4 step 3 note is closed. Contradicting
f_old affects only structures with live rebound dependencies on
f_old, which are structures in f_old's domain, as intended.

## 5. Kill bar for the contrast test's revision leg (unblocking R1)

Red-team R1 states the missing provenance specification "blocks
stating a kill bar for the contrast test's revision leg." With
sections 2 through 4 specified, the revision leg is now statable.
The future preregistration must include:

**Setup:** EXPERIENCED learner holds composite C built with
fragment F (F-provenance traces to WORLD A curriculum). C's (s,r)
is (s_c, r_c). At least one of C's SETREGs was rebound to a live
fact f_live = (s_c, r_c, o_old) per the section 2.2 trace data
(white-box precondition: the splice trace must show the rebound
branch applied to a SETREG citing f_live).

**Intervention:** Contradict f_live with observation new_o, where
new_o != o_old.

**Predicted outcomes (kill bar K-COMP-REV):**

- K-COMP-REV-1 (revision fires): the revision path triggers on C
  via the rebound prov->f_live edge. White-box: blame walk reaches
  C. If no revision fires despite the rebound edge existing, FAIL
  (the rebind was not live).
- K-COMP-REV-2 (R2 enforced): after re-execution producing out:
  if out == new_o, the revision is accepted and C is retargeted;
  if out != new_o, the revision is REJECTED (safe failure), C is
  not retargeted, and no fact (s_c, r_c, out) is taught. If a
  revision with out != new_o and matching (s,r) is accepted, FAIL
  (the V2 hole is open in the build; this is the trap condition).
- K-COMP-REV-3 (fragment not auto-superseded): after the revision
  episode (whether accepted or R2-rejected), fragment F is not
  marked superseded. White-box: F's supersede flag unchanged.
  F-utility counters for F reflect the episode (invocation
  incremented; success incremented iff the composite revision was
  accepted with out == new_o). If F is superseded as a side effect
  of C's revision, FAIL.
- K-COMP-REV-4 (no cross-domain fan-out): contradicting a WORLD A
  fact f_A cited only in F's F-setreg-hist (historical, not rebound
  into any composite) triggers revision of zero composites.
  White-box: blame walk from f_A reaches no composite MAP. If any
  composite is revised due to f_A's contradiction, FAIL (verbatim
  preservation leaked through).

**Determinism:** 3/3 byte-identical runs per the standard.

These four sub-bars are the revision leg. The preregistration may
add further bars; it may not weaken these.

## 6. Open questions left for the build

1. The splice trace data (section 2.2, rebound-vs-nulled per SETREG)
   needs a specified storage format in the composite MAP's
   bookkeeping fields. This amendment requires its existence and
   white-box readability; the exact layout is a build decision.
2. When a slot is filled from new-problem data that does NOT
   originate from a live fact node (e.g., a computed intermediate
   or a harness-supplied literal with no fact node), the rebind
   target is undefined. Default: prov=null (treat as constant).
   The build must state this explicitly if such fillings occur.
3. F-utility write paths for revision outcomes (section 4.2) need
   source-line identification at build time, per the SUF 4-condition
   evidence standard the design already imposes.
4. Interaction with H3-lite Node 3 (revision repair-topology
   policy), if both are ever built: Node 3 selects repair topology;
   this amendment governs what the topology's provenance means.
   The two compose but neither implies the other.

## 7. What this amendment does not do

1. It does not freeze the composition memory design. Status remains
   DRAFT-NOT-FROZEN. It does not authorize implementation.
2. It does not fix the V2 hole in frozen TNN-2. R2 is specified as
   a build requirement for the future composition-memory build
   only.
3. It does not solve the MAP-contracts gap (red-team R4). The
   (s,r)-match refinement is a stopgap; answer-vs-fact dependency
   semantics remain TNN-3 scope.
4. It does not establish SUF, L3, or any capability claim.

## 8. Standing architectural metric (amendment delta)

This amendment adds no cognition lines, modes, bridges, handlers, or
semantic cases. It specifies semantics for machinery the design
already proposes.

- RESEARCHER-OWNED STRUCTURAL DECISIONS: +1 (the Provenance
  Rebinding Rule: historical preservation at extraction, rebind-or-
  null at splice). Honestly labeled as researcher-specified
  semantics, not learner-authored.
- LEARNER-OWNED STRUCTURAL DECISIONS: 0 (unchanged; the design's
  predicted 3 remain predictions).
- All other fields: 0 delta.

No em dashes were used in this document.
