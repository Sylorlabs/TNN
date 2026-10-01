# Edge-Overflow Alternative to Fragment Node Enlargement

Status: SKETCH ONLY. No implementation, no build, no test.
Parent task: sketch the alternative named in FRAGMENT_RECORD.md section
11.4 ("interface and provenance as linked records") so the composition
preregistration can choose between enlargement and overflow with both
options on the table.

## 1. The 8 design-required scalars

From FRAGMENT_RECORD.md sections 2.1 and 3. The fragment record needs
these scalar values beyond the tag, root, live flag, and marker:

| # | Scalar | Field (enlarged) | Meaning |
|---|--------|------------------|---------|
| 1 | F-utility invocations | 12 | Splice-selection count |
| 2 | F-utility successes | 16 | Verification / R2-revision success count |
| 3 | F-shape signature | 28 | 32-bit literal-excluding topology signature |
| 4 | F-interface entry | 40 | Cell receiving the input frame at splice |
| 5 | F-interface exit | 44 | Cell yielding the output value at splice |
| 6 | F-prov world | 48 | World/curriculum id of the creating episode |
| 7 | F-prov episode | 52 | Learner episode counter at extraction |
| 8 | F-prov parent | 56 | The promoted MAP the fragment was extracted from |

### 1.1 Which scalars fit the frozen 40-byte layout

The frozen node has 10 fields (offsets 0-36). On a fragment record:

- Fields 0, 20, 36 are taken (tag, graph root, live flag).
- Fields 4, 8, 24 are taken by the triple fragment marker (-1, -1, -2).
- Field 32 is reserved for H3-lite coexistence (do not use).

Remaining repurposable fields: 12, 16, 28. Three fields.

Scalars 1-3 (invocations, successes, F-shape) fit in fields 12, 16, 28
with no layout change. This is already established in
FRAGMENT_RECORD.md section 8 (collision checks).

Scalars 4-8 (entry, exit, world, episode, parent) do not fit. There is
no field for them on the frozen layout. These five are the true
overflow set. The enlargement decision exists for these five (plus the
three spares at 60/64/68 and Q1's composite splice trace).

## 2. Edge-overflow sketch: the five that do not fit

Design principle: follow the existing fragment edge idiom.
ET_FRAGSLOT (15) stores variable-length slot data as edges from the
fragment to literal-holders; ET_FRAGHIST (16) stores historical
provenance as edges from the fragment to cited facts. The overflow
scalars become reference edges from the fragment record.

### 2.1 Node-ID scalars: edge to the referenced node

Three of the five overflow scalars are node references. The edge target
IS the value; no auxiliary storage is needed.

- ET_FRAGENTRY (type 17): fragment record -> entry cell node.
  Meaning: "input frame enters the fragment at this cell."
  Created at extraction. Read at splice time to wire the input.
- ET_FRAGEXIT (type 18): fragment record -> exit cell node.
  Meaning: "the fragment's output value is read from this cell."
  Created at extraction. Read at splice time to wire the output.
- ET_FRAGPARENT (type 19): fragment record -> parent MAP node.
  Meaning: "this fragment was extracted from this promoted MAP."
  Created at extraction. Read for SUF evidence and white-box audit.
  Never traversed by production blame or selection paths.

Each is a single edge. Lookup is a scan of the fragment's outbound
edges filtered by type, O(out-degree). Fragments carry few edges
(ET_FRAGUSE inbound, ET_FRAGSLOT/ET_FRAGHIST outbound, plus these
three), so the scan is short.

### 2.2 Integer scalars: value in the edge aux field

Two of the five are plain integers, not node references. TNN edges
carry an aux field (`eg(W,e,12)`), a 32-bit slot already used by
ET_FRAGSLOT and ET_FRAGHIST for cell indices. The integer value rides
in aux.

- ET_FRAGWORLD (type 20): fragment record -> fragment record
  (self-target; the target carries no information), aux = world id.
  Meaning: "creating world/curriculum id." Written once at
  extraction. Read for SUF evidence only.
- ET_FRAGEPISODE (type 21): fragment record -> fragment record
  (self-target), aux = episode counter.
  Meaning: "learner episode counter at extraction." Written once.
  Read for SUF evidence only.

Self-targets are used because the edge needs a target and there is no
meaningful node to point at. Alternative: point at the parent MAP and
overload, but that conflates two relations on one edge type. Separate
types with self-targets keep one relation per type, matching the
white-box readability constraint.

### 2.3 Write and read paths for the overflow edges

- Creation: at extraction, after the fragment node is allocated and
  fields 12/16/28 are written, the five edges are created (three
  reference edges, two aux-carrying edges). All five are written
  exactly once per fragment. No production path modifies them
  afterward.
- Reads:
  - ET_FRAGENTRY / ET_FRAGEXIT: read at splice time (hot path, once
    per fragment selection).
  - ET_FRAGPARENT / ET_FRAGWORLD / ET_FRAGEPISODE: read for audit
    and SUF evidence (cold path; not in the selection hot loop).
- Non-traversal: like ET_FRAGUSE and ET_FRAGHIST, none of types
  17-21 are traversed by the blame walk (`revise_on_contradict`),
  the selection scan, or the eviction policy. The build must verify
  by inspection, as required for types 14 and 16.

### 2.4 Researcher-owned decision count for this sketch

+5 edge types (17, 18, 19, 20, 21). Each is a researcher-owned
structural decision to be declared in the preregistration, alongside
the +3 already counted (ET_FRAGUSE 14, ET_FRAGSLOT 15, ET_FRAGHIST
16). Total fragment edge-type decisions under overflow: 8.

No node enlargement. The 40-byte layout is untouched. F-utility and
F-shape stay in fields 12, 16, 28.

## 3. Full-overflow variant (all eight as edges)

For completeness: scalars 1-3 could also move to edges, leaving the
fragment node with only tag, marker, root, and live flag.

- ET_FRAGINV (type 22): self-target, aux = invocation count.
- ET_FRAGSUCC (type 23): self-target, aux = success count.
- ET_FRAGSHAPE (type 24): self-target, aux = 32-bit signature.

Trade-offs vs the section 2 sketch:

- F-utility counters are incremented on the hot path (every splice
  selection, every verification, every R2 revision). Edge-aux update
  requires locating the edge (outbound scan) before the read-modify-
  write; field update is a direct `ns`. Under heavy splice traffic
  the scan cost accumulates.
- F-shape is read on every selection scan (signature matching for
  candidate ranking). Edge lookup per candidate fragment multiplies
  the selection cost by the outbound scan.
- Benefit: fields 12, 16, 28 stay at their frozen-layout values
  (-1, -1, answer-slot), so a fragment record's field image is even
  closer to a regular MAP's. Marginal white-box gain.

Recommendation: do not overflow scalars 1-3. They fit, they are hot,
and fields are the right substrate for counters. The section 2 sketch
(overflow only the five that do not fit) dominates full overflow.

## 4. Cost comparison: enlargement vs edge-overflow

### 4.1 Byte cost

Edge size: the frozen workspace reserves 65536 bytes for 4096 edge
slots, so one edge is 16 bytes.

- Enlargement: +32 bytes per node x 1024 nodes = +32768 bytes fixed,
  paid regardless of fragment count. Node region grows from 40960
  to 73728 bytes; the workspace allocation must absorb it.
- Edge-overflow (section 2 sketch): +5 edges x 16 bytes = +80 bytes
  per fragment, paid only for fragments that exist. 100 fragments
  cost 8000 bytes; 400 fragments cost 32000 bytes.

Break-even: 32768 / 80 = 409.6. Fewer than ~410 live fragments favors
overflow on bytes; more favors enlargement. Expected fragment store
size is tens to low hundreds (per the F-shape section: "tens to
hundreds of entries"), which lands on the overflow side of break-even,
but not decisively.

Caveat: this counts only the five overflow scalars. Under enlargement
the three spare fields (60/64/68) and Q1's composite splice trace also
consume the new space; under overflow, Q1 needs its own separate
solution (see section 5).

### 4.2 Access cost

- Enlargement: field read/write is one `ng`/`ns`, O(1), no scan.
- Overflow: each scalar read is an outbound-edge scan of the fragment
  filtered by type, O(out-degree). Out-degree per fragment is small
  (roughly 5 overflow edges + slot edges + hist edges, typically
  under 20), so the constant is modest but nonzero, and it applies on
  the splice hot path for entry/exit.

### 4.3 Researcher-owned decisions

- Enlargement: +1 (the layout change), plus the field layout itself
  (already counted in the fragment spec's +4).
- Overflow: +5 edge types (17-21).

Fewer decisions favors enlargement. The One-System Rule does not
distinguish here (both keep one graph type, no new tags, no modes),
but decision-count parsimony is a stated program value.

### 4.4 Layout risk

- Enlargement: touches `noff()`, `alloc_node()`, workspace sizing.
  Every node pays. A layout bug corrupts everything. This is the
  largest researcher-owned layout change in the program so far.
- Overflow: touches nothing global. A bug in a new edge type is
  contained to fragment handling.

Risk containment favors overflow.

### 4.5 White-box readability

- Enlargement: all eight scalars visible in the node's field dump.
  One glance shows the whole fragment record.
- Overflow: five scalars require edge traversal to inspect. Field
  dump shows only the three hot scalars.

Readability favors enlargement. The program treats white-box
readability as a hard constraint (FRAGMENT_RECORD.md 2.1).

## 5. The Q1 interaction (decisive)

The node layout is global. BUILD_QUESTIONS.md Q1 specifies the
composite splice trace as field 12 (n_trace) plus fields 40+4i for
i = 0..7 on the composite MAP node. Those fields do not exist on the
40-byte layout (FRAGMENT_RECORD.md section 0 correction).

Therefore:

- If the build adopts enlargement for Q1 (composites need fields
  40-68), then every node is 72 bytes, and the fragment fields
  40-68 exist at zero marginal layout cost. Choosing edge-overflow
  for fragments while enlarging for Q1 would pay the layout risk
  without using the space. Incoherent.
- If the build rejects enlargement globally, then Q1 also needs an
  edge-based splice trace (not sketched here; the trace is up to 8
  fact references, a natural edge list, but the preregistration
  would need to specify it). Fragment overflow and Q1 overflow
  stand or fall together.

The fragment overflow decision cannot be made independently of Q1.
They share one layout.

## 6. Recommendation

Primary recommendation: **enlarge, do not overflow**, on the
condition that Q1's splice trace also uses the enlarged fields, which
is already the specified design. Rationale:

1. Q1 already requires fields 40-68 on composites. The layout change
   is then sunk; fragment fields 40-68 are free.
2. Eight scalars in one field dump beats five scalars behind edge
   scans for white-box readability (hard constraint).
3. Hot-path scalars (F-utility increments, F-shape matching,
   entry/exit wiring at splice) stay O(1).
4. +1 layout decision vs +5 edge-type decisions.

Fallback: **if Micah judges the 40 to 72 byte enlargement an
unacceptable deviation from the frozen substrate**, adopt the section
2 sketch (five edge types 17-21, scalars 1-3 in fields 12/16/28) AND
specify an edge-based Q1 splice trace in the same preregistration.
Do not mix: a 72-byte layout with edge-overflowed fragments, or a
40-byte layout with field-addressed Q1 traces, are both incoherent.

Explicit non-recommendation: full overflow of all eight scalars
(section 3). It moves hot counters behind edge scans for no layout
benefit, since fields 12/16/28 are already repurposable.

## 7. Standing metrics (this sketch)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: +5 if adopted (edge types
  17-21), 0 as a sketch.
- LEARNER-OWNED STRUCTURAL DECISIONS: 0.
- SUF DECISIONS: 0. LEARNER-INTERNAL CRITERIA: 0.
- REUSE EVENTS: 0. REVISION EVENTS: 0.
- COGNITION LINES: 0. MODES: 0. BRIDGES: 0. HANDLERS: 0.
- SEMANTIC CASES: 0.

## 8. Checklist for the composition preregistration (overflow branch)

If the preregistration takes the overflow branch, it must declare:

1. The five edge types (17-21) with the section 2.1/2.2 semantics
   (+5 researcher-owned structural decisions).
2. Self-target convention for aux-carrying edges (types 20, 21),
   or a named alternative target.
3. Non-traversal of types 17-21 by blame, selection, and eviction,
   verified by inspection.
4. The edge-based Q1 splice trace (companion specification; the
   field-based Q1 layout is void on the 40-byte node).
5. F-utility (12, 16) and F-shape (28) field offsets (unchanged
   from the fragment spec).
6. Fragment selection's per-candidate edge-scan cost budget, or a
   measured bound from the DYN-1 harness.

No em dashes were used in this document.
