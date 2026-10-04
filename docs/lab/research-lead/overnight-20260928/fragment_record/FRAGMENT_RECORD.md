# Fragment Record Format Specification

Status: DRAFT-NOT-FROZEN. Specification only; nothing built, nothing tested.
Resolves the Q3 information gap from BUILD_QUESTIONS.md (`97b80383a`):
"the design never specifies the fragment record's node tag or F-utility
field offsets; the build must specify these."

Grounding: tag census and field census performed read-only against the
frozen base (`bootstrap_loop/bl_base.zag`, byte-identical verbatim frozen
copy). Node layout: `noff(n) = 64 + n*40`, 10 header fields at byte
offsets 0, 4, 8, 12, 16, 20, 24, 28, 32, 36. Edge types 1-13 in use;
type 14+ free.

## 0. Correction to BUILD_QUESTIONS Q1 (must-read for the build)

BUILD_QUESTIONS.md Q1 specifies the composite splice trace as "field 12
(n_trace) and fields 40 + i for i = 0 .. n_trace - 1" and claims this
was "verified against the frozen base source." This is incorrect.

The frozen base node is 40 bytes with 10 fields (offsets 0-36). Fields
40 through 68 do not exist. Writing to field 40 of node n would corrupt
field 0 (the tag) of node n+1. The Q1 layout as written is not
implementable on the frozen node layout.

This specification resolves the problem in section 2 (node enlargement),
which simultaneously validates Q1's intended layout. Until the build
adopts the enlarged node, Q1's fields 40-68 must not be used. The build's
preregistration must state the node size explicitly.

## 1. Node tag: 20 (MAP). No new tag.

The design (section 1, One-System Rule compliance) states: "fragments
are the same executable graph type as every other MAP (tag-20 nodes with
the existing field layout), not a second representation." This
specification follows that decision.

- Fragment records are tag-20 nodes.
- No new node tag is introduced.
- Rationale: a fragment is an executable graph. Giving it the same tag
  as every other executable graph keeps one graph type, one execution
  path, one revision path. A new tag would be a second representation
  and a One-System Rule violation.

### 1.1 Distinguishing a fragment record from a regular MAP

A tag-20 node is a fragment record if and only if all three hold:

- field 0 = 20 (tag; same as any MAP)
- field 24 = -2 (FRAGMENT marker; regular MAPs hold a promotion
  index >= 0 here, read by `map_standing` at bl_base.zag line 569)
- field 4 = -1 and field 8 = -1 (r and s unused; regular MAPs hold
  valid subject/relation here)

The triple marker is redundant by design: any one of the three
suffices, but all three are written so that white-box inspection and
production guards have multiple independent checks. The primary
discriminator is field 24 = -2.

### 1.2 Production guard requirement

Every production scan that enumerates tag-20 nodes must skip fragment
records unless it explicitly intends to read the fragment store. In
particular:

- The query path (`activate`, `ev_query`) must not treat a fragment
  record as an answerable MAP. Guard: `ng(W,m,24) != -2` before any
  MAP-shaped read.
- `revise_on_contradict` dispatches on prov edges to MAPs; fragment
  records carry no prov edges as targets (they are patterns, not
  instantiated queries), so no guard is needed there, but the build
  must verify this by inspection.
- The fragment selection path reads ONLY nodes with field 24 = -2.

## 2. Node enlargement: 40 to 72 bytes (declared researcher decision)

### 2.1 Why enlargement is required

The fragment record's scalar bookkeeping does not fit in the 10-field
frozen layout. Counting the design-required scalars:

- F-utility: 2 counters (invocations, successes). Design-mandated.
- F-shape: 1 signature field. Required for selection matching.
- F-interface: 2 fields (entry cell, exit cell). Required for splicing.
- F-provenance: 3 fields (world id, episode counter, parent graph).
  Required for SUF evidence (tracing each fragment to its creating
  episode).
- Fragment marker: field 24 = -2 (repurposed promotion index).
- Graph root: field 20 (the fragment topology; must keep).
- Live flag: field 36 (must keep for the eviction/selection protocol).

Required scalar fields: 2 + 1 + 2 + 3 = 8, plus root, live, and marker
fields. The frozen layout offers 6 repurposable fields on a non-query
MAP (4, 8, 12, 16, 24, 28; field 32 is reserved per Q1 for H3-lite).
Eight does not fit in six. Packing multiple scalars per field would
damage white-box readability, which the research program treats as a
hard constraint.

### 2.2 The decision

The composition-memory build enlarges the node from 40 bytes (10
fields) to 72 bytes (18 fields, byte offsets 0, 4, ..., 68).

- This is a +1 RESEARCHER-OWNED STRUCTURAL DECISION, explicitly
  declared here and to be declared in the build's preregistration.
- It is not learner-authored. It is layout machinery, like the
  existing 40-byte layout.
- Consequences the build must handle: `noff()` changes to
  `64 + n*72`; `alloc_node()` must zero 18 fields; the workspace
  size or node budget must be recomputed (72 * 1024 = 73728 bytes
  for nodes; edges unchanged at 65536; total fixed regions must
  still fit the workspace allocation).
- Frozen TNN-2 is untouched. This applies to the future
  composition-memory build only.

### 2.3 Q1 validation

With 72-byte nodes, fields 40, 44, 48, 52, 56, 60, 64, 68 exist.
Q1's splice-trace layout (field 12 = n_trace; fields 40+4i for
i = 0..7) becomes implementable exactly as written, with the
n_trace <= 8 bound satisfiable. Section 0's correction is thereby
resolved: Q1 was specified for the enlarged layout, not the frozen
one, and the preregistration must say so.

## 3. Fragment record field layout (72-byte node)

| Field | Name | Value | Notes |
|-------|------|-------|-------|
| 0 | tag | 20 | Same as any MAP |
| 4 | r | -1 | Unused; part of fragment marker |
| 8 | s | -1 | Unused; part of fragment marker |
| 12 | F-utility invocations | count | Incremented at splice selection (Q3 write path 1) |
| 16 | F-utility successes | count | Incremented on composite verification / R2-accepted revision (Q3 write paths 2, 3) |
| 20 | graph root | cell id | The fragment's walked topology cells |
| 24 | marker | -2 | FRAGMENT; regular MAPs hold promotion index >= 0 |
| 28 | F-shape | signature | 32-bit structural signature, literals excluded (section 4) |
| 32 | reserved | 0 | DO NOT USE. Reserved for H3-lite Node 1 coexistence (Q1). |
| 36 | live | 1 / 0 | 1 = selectable; 0 = retired/superseded (section 6) |
| 40 | F-interface entry | cell id | Cell receiving the input frame at splice |
| 44 | F-interface exit | cell id | Cell yielding the output value at splice |
| 48 | F-prov world | id | World/curriculum id of the creating episode |
| 52 | F-prov episode | counter | Learner episode counter at extraction |
| 56 | F-prov parent | node id | The promoted MAP the fragment was extracted from |
| 60 | spare | 0 | Reserved for future bookkeeping |
| 64 | spare | 0 | Reserved for future bookkeeping |
| 68 | spare | 0 | Reserved for future bookkeeping |

### 3.1 F-utility field offsets (the Q3 gap, closed)

- Invocations: field 12.
- Successes: field 16.
- Both initialized to 0 at extraction.
- Write paths (from Q3, anchored to build-time source lines):
  1. Invocation: in the splice function, when fragment F is selected
     for composite C, `ns(W,F,12,ng(W,F,12)+1)`. Once per splice,
     regardless of the composite's later fate.
  2. Success on verification: in `promote_graph` at the MAP creation
     point, for each fragment in C's fragment list (enumerated via
     ET_FRAGUSE edges, section 7), `ns(W,F,16,ng(W,F,16)+1)`.
  3. Success on revision: in `t2_revise_graph` at the `return 1`
     point, for each participating fragment, increment field 16 if
     and only if the revision was accepted with `out == new_o`
     (the R2 condition). On R2-rejection or total failure, field 16
     is not incremented; field 12 was already counted at splice.
- The success-to-invocation ratio is the demotion signal. No
  separate failure counter (per Q3: keeps the F-utility format at
  exactly the two counters the design specifies).

## 4. F-shape signature (field 28)

- A 32-bit deterministic signature over the fragment's topology:
  the sorted list of (cell role, edge wiring) pairs walked at
  extraction, with literal values excluded.
- Requirements: deterministic across runs (byte-identical builds
  must produce identical signatures); literal-excluding (two
  fragments differing only in stripped literal values must have
  equal signatures, enabling the W6 dedupe); order-independent
  (cell visit order must not affect the signature).
- The exact hash function (FNV-1a, djb2, or equivalent) is a build
  decision, but the preregistration must name it and the build must
  include a test showing that literal-varying extractions of the
  same topology produce equal signatures.
- Collision risk: 32 bits over a small fragment store (tens to
  hundreds of entries) is adequate; the dedupe path (section 6)
  must confirm full topology equality on signature match before
  merging, so a hash collision causes a missed dedupe, not a
  wrong merge.

## 5. Variable-length data: F-slots and F-setreg-hist as edges

F-slots (parameter slots with default fillings) and F-setreg-hist
(extraction-episode provenance pairs) are variable-length and cannot
fit in fixed header fields. They are stored as edges, which is TNN's
native white-box idiom for relations (per Q3's rationale for
ET_FRAGUSE).

### 5.1 ET_FRAGSLOT (type 15): slot default fillings

- Edge type value: 15 (next free after ET_FRAGUSE 14; types 1-13
  used in the frozen base, verified by census).
- From: the fragment record node.
- To: a literal-holder node carrying the default value.
- Edge aux field (`eg(W,e,12)`): the slot's cell index within the
  fragment graph (which SETREG's stripped literal this default
  fills at splice time).
- Literal-holder node: a tag-102 graph cell with the default value
  in its value field. Tag 102 is the existing cell type; no new
  tag. (If the build's cell layout stores literals differently,
  the preregistration must state the exact encoding.)
- Created at: extraction time, one edge per stripped literal.
- Read at: splice time, to fill slots the new problem does not
  provide values for (amendment section 2.2 default branch,
  prov=null).
- This is a +1 RESEARCHER-OWNED STRUCTURAL DECISION (one new edge
  type), to be declared in the preregistration alongside
  ET_FRAGUSE.

### 5.2 ET_FRAGHIST (type 16): historical SETREG provenance

- Edge type value: 16.
- From: the fragment record node.
- To: the fact node cited by the SETREG during the extraction
  episode.
- Edge aux field (`eg(W,e,12)`): the cell index of the citing
  SETREG within the fragment graph.
- Created at: extraction time, one edge per provenance-carrying
  SETREG in the walked topology.
- Read-only after extraction. No production path modifies these
  edges. They serve white-box inspection, debugging, and SUF
  evidence (amendment section 2.1).
- They are explicitly NOT live dependencies: the blame walk
  (`revise_on_contradict`) must not traverse type-16 edges.
  The build must verify this by inspection and state it in the
  preregistration (amendment K-COMP-REV-4 depends on it).
- This is a +1 RESEARCHER-OWNED STRUCTURAL DECISION (one new edge
  type), declared in the preregistration.

## 6. Lifecycle

### 6.1 Creation (extraction on promotion)

Trigger: `promote_graph` (or its successor) promotes a verified
executable graph. The promotion path additionally runs fragment
extraction (design section 2.1). Extraction is part of the
production promotion path, not a separate researcher-invoked step.

Steps:
1. Walk the cells the executor touched between entry and
   answer-producing step (the execution trace, not a fixed slice;
   design W3 guard).
2. Allocate a new tag-20 node; write the section 3 field layout:
   tag 20; fields 4, 8 = -1; field 24 = -2; field 36 = 1;
   F-utility fields 12, 16 = 0; field 20 = root of the copied
   walked cells; field 28 = F-shape signature; fields 40, 44 =
   interface entry/exit from the trace; fields 48, 52, 56 =
   world id, episode counter, parent MAP id.
3. Copy the walked cells into fresh graph cells (the fragment's
   topology). Strip literals to parameter slots.
4. For each stripped literal, create an ET_FRAGSLOT edge (type 15)
   to a literal-holder with the default value; record the slot
   cell index in the edge aux field.
5. For each provenance-carrying SETREG in the walked topology,
   create an ET_FRAGHIST edge (type 16) to the cited fact;
   record the cell index in the edge aux field.
6. Dedupe (section 6.2) before committing.

### 6.2 Dedupe on insert (design W6 guard)

Before committing a new fragment record, compute its F-shape
signature and scan existing live fragment records (field 24 = -2,
field 36 = 1) for a matching signature. On signature match,
confirm full topology equality (cell roles and wiring); on
confirmation, discard the new record and increment the existing
fragment's provenance count. The provenance count is stored as an
additional ET_FRAGHIST-style edge or a spare-field counter; the
build must specify which (recommendation: field 60, the first
spare, as a creation-count).

This is generic machinery (signature equality), not a researcher
judgment about which fragments are "good."

### 6.3 Updates (F-utility write paths)

Per section 3.1. The three write paths (splice selection,
verification success, R2-accepted revision success) are the only
production writes to fields 12 and 16. No other path modifies
F-utility.

### 6.4 Retirement (not deletion)

When a fragment's success-to-invocation ratio falls below the
retirement threshold, or when a fragment is superseded by revision
of a composite that demonstrates the pattern itself is faulty
(design section 2.4), the fragment is retired: field 36 set to 0.

- Selection skips field-36 = 0 fragments (production guard).
- The node, its cells, and its edges remain in learner state,
  inspectable as white-box evidence of what was tried and
  abandoned.
- Retirement is distinct from eviction: eviction is budget-driven
  and may remove any node; retirement is quality-driven and only
  removes the fragment from the candidate set.
- The retirement threshold value and its justification are
  preregistration decisions, not specified here.

### 6.5 Deletion

Fragments are never deleted by fragment-specific logic. They are
subject to the same general eviction policy as all other learner
structures (design section 2.1: "no fragment-specific storage
logic"). If evicted, later selection cannot select the fragment;
that is correct behavior and a natural ablation (design section
2.1).

## 7. ET_FRAGUSE (type 14): composite-to-fragment participation

Per Q3 (already decided; restated here for completeness):

- Edge type value: 14. Verified free (frozen base uses types
  1-13; census in section 0 preamble).
- From: composite MAP node (tag 20, regular marker).
- To: participating fragment record node (tag 20, field 24 = -2).
- Meaning: "this composite was built using this fragment."
- Created at: splice time, one edge per fragment spliced into
  the composite.
- Read at: (a) promotion time, to enumerate fragments for the
  F-utility success write (section 3.1, write path 2);
  (b) revision time, to enumerate fragments for the
  R2-conditional success write (section 3.1, write path 3);
  (c) white-box audit, to trace composite provenance.
- Not traversed by the blame walk (it is a bookkeeping edge, not
  a data-dependency edge). The build must verify this.

## 8. Collision checks (explicit)

| Decision | Value | Collision status |
|----------|-------|------------------|
| Node tag | 20 | No new tag. Distinguished by field 24 = -2 (regular MAPs: promotion index >= 0, read at bl_base.zag:569). |
| Field 32 | untouched (0) | Reserved for H3-lite Node 1 coexistence per Q1. This spec writes nothing to field 32. |
| Field 12, 16 on fragments | F-utility | Regular MAPs: set to -1 by promote_graph, never read in production. No collision (fragment vs regular distinguished by field 24). |
| Field 28 on fragments | F-shape | Regular MAPs: answer field, live-read. No collision (disjoint node sets). |
| Fields 40-68 | interface, provenance, spares | Do not exist in frozen 40-byte layout; created by the section 2 enlargement. Q1's splice trace uses 12, 40-68 on composites; fragments use 40-56 for interface/provenance. A node is never both a composite and a fragment record (extraction copies; it does not convert), so no intra-node collision. |
| Edge type 14 (FRAGUSE) | composite -> fragment | Free (1-13 used). |
| Edge type 15 (FRAGSLOT) | fragment -> literal | Free. |
| Edge type 16 (FRAGHIST) | fragment -> fact | Free. Must not be blame-walked (amendment K-COMP-REV-4). |
| Node enlargement 40 -> 72 | layout change | Declared researcher decision (section 2.2). Frozen TNN-2 untouched. |
| Query path | guard required | Section 1.2: skip field-24 = -2 nodes in MAP enumeration. |

## 9. What the build's preregistration must declare (checklist)

1. Node size: 72 bytes; updated `noff()`, `alloc_node()`, workspace
   budget recomputation (section 2).
2. The three new edge types (14, 15, 16) with the semantics in
   sections 5 and 7 (+3 researcher-owned structural decisions).
3. The F-shape hash function name and the literal-variance test
   (section 4).
4. The literal-holder encoding for ET_FRAGSLOT targets (section 5.1).
5. The non-traversal of types 14 and 16 by the blame walk,
   verified by inspection (sections 5.2, 7).
6. The retirement threshold and its justification (section 6.4).
7. The provenance-count storage for dedupe merges (section 6.2).
8. The query-path fragment guard, with a test showing fragments
   are not answerable as MAPs (section 1.2).
9. The R2 criterion fix as a build requirement (amendment section
   3; restated, not weakened).
10. The Q1 correction: splice-trace fields 40-68 exist only under
    the enlarged layout (section 0).

## 10. Standing architectural metric (specification delta)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: +4, honestly labeled as
  build-specification decisions, not learner-authored: (1) node
  enlargement 40 -> 72 bytes; (2) ET_FRAGSLOT (type 15);
  (3) ET_FRAGHIST (type 16); (4) the section 3 field layout
  (F-utility offsets 12/16, F-shape 28, interface 40/44,
  provenance 48/52/56, marker convention 24 = -2).
  (ET_FRAGUSE type 14 was already counted in Q3's +2.)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0.
- SUF DECISIONS: 0. LEARNER-INTERNAL CRITERIA: 0.
- REUSE EVENTS: 0. REVISION EVENTS: 0.
- COGNITION LINES: 0. MODES: 0. BRIDGES: 0. HANDLERS: 0.
- SEMANTIC CASES: 0.
- SOURCE-ENUMERABLE FORMS: +3 (the three new edge types are
  enumerable from the build source once specified).

## 11. Explicit non-claims

1. This specification does not freeze the composition memory
   design. Status remains DRAFT-NOT-FROZEN.
2. It does not authorize implementation. The build requires a
   frozen preregistration Micah reviews.
3. It does not fix the V2 hole in frozen TNN-2. R2 remains a
   future-build requirement.
4. The node enlargement is the largest researcher-owned layout
   change in this specification; if Micah judges it an
   unacceptable deviation from the frozen substrate, the
   alternative is the edge-overflow design (interface and
   provenance as linked records), which this specification does
   not develop.
5. No capability, SUF, L3, or utility claim is made or implied.

No em dashes were used in this document.
