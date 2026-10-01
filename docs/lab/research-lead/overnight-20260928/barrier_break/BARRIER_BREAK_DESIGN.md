# BARRIER BREAK DESIGN

**Status:** DRAFT-NOT-FROZEN
**Date:** 2026-10-01
**Worker:** Barrier-Breaking Designer
**Input:** Xfer experiment `cbd7bc803` (zero transfer, four barriers)

## The Four Barriers

From `cbd7bc803` (white-box, frozen source):

1. `t2_gather` reads only tag-1 FACTs, never tag-20 MAPs.
   Prior structures are invisible to construction.
2. Trial search order is source-fixed.
   The learner cannot adapt its construction strategy.
3. MAP lookup is exact (s,r).
   No similarity-based retrieval exists.
4. MAPs have literals baked in.
   No rebinding mechanism exists.

Each barrier alone guarantees zero transfer. Breaking one is necessary
but not sufficient.

## Barrier Pick: Barrier 1 (Visibility)

**Pick:** Break Barrier 1. Make prior structures visible to construction.

### Justification

**Information bottleneck.** Barriers 3 and 4 govern USE of structures
(retrieval, rebinding). Barrier 1 governs VISIBILITY. Without visibility,
barriers 3 and 4 cannot even be tested. The learner cannot attempt to
retrieve what it cannot see. Breaking barrier 1 is the necessary first
step that makes the other barriers empirically accessible.

**Maximum observability per change.** With structures visible, white-box
instrumentation can log exactly when a structure is seen but not used.
This pinpoints whether barrier 3 (retrieval) or barrier 4 (rebinding)
is the binding constraint in practice. Without visibility, we are
theorizing about invisible blockers.

**Minimal architectural change.** Breaking barrier 1 requires changing
what an existing function reads, not adding new opcodes, modes, or
semantic cases. Compare:
- Barrier 2 (search order): requires learner-owned policy machinery
  (already scoped in H3-lite; do not duplicate here).
- Barrier 3 (similarity): requires defining a similarity metric, a
  major architectural decision with no minimal form.
- Barrier 4 (rebinding): requires a variable binding mechanism, also
  a major architectural decision.

Barrier 1 is the only one breakable with a read-path change alone.

**Does not presume the solution.** Making structures visible does not
dictate HOW the learner should use them. It creates the precondition
for learner-driven discovery without hardcoding cross-domain mappings
(Micah's constraint).

### Alternatives Considered

**Barrier 2 (search order):** H3-lite already scopes this as Policy Node 1
(trial search order). Breaking it here would duplicate H3-lite. Also,
adaptive search order without visible structures is just learning
statistics about assembler families, not reusing structures. Less
transfer-specific information.

**Barrier 3 (similarity retrieval):** No minimal form exists. Similarity
over what? Topology? Literal patterns? Behavioral signature? Each
choice is a researcher-owned semantic decision that risks recreating
the treadmill. This is a research program, not a minimal change.

**Barrier 4 (rebinding):** Requires deciding what a "variable" is in
TNN's graph substrate. This interacts with the protected-core ISA
ruling (is VARIABLE a new opcode? is REBIND?). Not minimal, and
blocked by Alternative C until evidence justifies it.

## Minimal Machinery Design

### What Changes

**Function:** `t2_gather` (construction input gathering).

**Current behavior:** Reads only tag-1 FACT nodes. Returns facts relevant
to the current (s,r) query.

**Minimal break:** Add structure visibility. When gathering inputs for
construction, also enumerate live tag-20 MAP nodes. Return their
structural descriptors (topology signature + literal list) alongside
facts.

### Specific Mechanism

1. **New read path (not new opcode):** A helper `gather_structures(W)`
   that scans for live tag-20 nodes and extracts:
   - Node ID
   - Structural signature (via frozen `t2_sig`)
   - Literal vector (the baked-in constants)
   - Creation provenance (which (s,r) it was built for)

2. **Integration point:** `t2_gather` calls `gather_structures` and
   appends structure descriptors to its result set, tagged as
   STRUCTURE (not FACT) so downstream code can distinguish them.

3. **No automatic use:** The construction process receives the
   descriptors but has NO automatic reuse logic. The trial assembler
   continues to work from facts as before. Structures are visible
   but inert unless future machinery acts on them.

4. **White-box instrumentation:** Counter at `hg(W,53)` increments
   each time a structure descriptor is visible during construction.
   Counter at `hg(W,54)` increments if construction references a
   descriptor (initially always zero; documents the gap).

### Where It Lives

**In source, not in protected core ISA.** This is a change to `t2_gather`,
an existing cognitive function, not a new protected opcode. The
protected core already has READ and SCAN primitives; we are using them
to read a different tag type.

**Not learner-composed (yet).** The visibility is researcher-provided
infrastructure. The learner does not choose to see structures; they
are made visible. Learner-owned USE of visible structures is future
work (requires breaking barriers 3 and/or 4).

**Why not protected core:** The ISA ruling allows READ of state. We are
not adding ALLOC/LINK/KILL or any structural mutation opcode. This is
a read-path extension, compliant with Alternative C.

### Smallest Change

The diff is:
- One new helper function (`gather_structures`, ~15 lines)
- One call site in `t2_gather` (~3 lines)
- Two white-box counters (~4 lines)
- Structure descriptor format (topology + literals, reuses `t2_sig`)

Total: ~25 lines. No new opcodes. No new modes. No new bridges.
No new handlers. No new semantic cases.

## Honesty Analysis

### Does Breaking Barrier 1 Enable ANY Transfer?

**No.** Be explicit: breaking barrier 1 alone enables zero transfer.

Barriers 3 and 4 still completely block:
- **Barrier 3:** MAP lookup remains exact (s,r). Domain B uses disjoint
  namespace (subjects 100-104 vs 1-5). Exact lookup fails. The visible
  structure cannot be retrieved by the query path.
- **Barrier 4:** Even if manually retrieved, literals are baked in.
  The A-domain MAP contains literals 1-5; B-domain needs 100-104.
  No rebinding mechanism exists. The structure cannot be applied.

**What breaking barrier 1 DOES enable:**
- Observability: white-box logs show "structure visible but unused"
- Diagnostic precision: we can now measure whether barrier 3 or 4
  is the tighter constraint by attempting manual retrieval in
  experiments
- Precondition: any future work on barriers 3/4 requires visibility
  first; this lays that groundwork

### What Remains Blocked

After breaking barrier 1, the xfer experiment `cbd7bc803` would still
show zero transfer. The trial counts would still be identical. The
A-MAP would still never be invoked. The only difference: white-box
counters would show the A-MAP was VISIBLE during B construction
(`hg(W,53)` > 0) but never REFERENCED (`hg(W,54)` = 0).

This is the honest result: visibility without usability.

### Path Forward (Not Claimed Here)

Breaking barriers 3 and 4 requires:
- **Barrier 3:** A similarity metric (researcher-owned decision; high
  risk of treadmill; needs independent justification)
- **Barrier 4:** A rebinding mechanism (interacts with Alternative C;
  needs evidence that visibility alone is insufficient, which this
  design provides)

This design does NOT propose solutions for 3 or 4. It creates the
empirical precondition for studying them.

## Compliance Checks

### One-System Rule

**Pass.** No new modes, bridges, routers, or subsystems. The change is
within the existing construction pathway (`t2_gather`). Structures are
returned as descriptors in the existing result format, not via a new
subsystem.

### Alternative C

**Pass.** No structural graph-mutation opcodes added. No ALLOC/LINK/KILL
in learner-executable ISA. This is a read-path change only. The
deferred opcodes remain deferred.

### Protected-Core ISA Ruling

**Pass.** No new protected operations. Uses existing READ/SCAN
primitives to access tag-20 nodes. Does not encode a target-domain
regularity detector. The structural signature reuses frozen `t2_sig`.

### Micah's Constraints

- **No hardcoded cross-domain mappings:** Pass. Visibility is
  domain-agnostic; no A-to-B mapping is provided.
- **Do not build larger grammar:** Pass. No new templates, assemblers,
  or capability-shaped operators.
- **White-box architecture:** Pass. Design includes white-box counters
  (`hg(W,53)`, `hg(W,54)`) for observability.

## Explicit Non-Claims

1. **Breaking barrier 1 does NOT establish transfer.** Zero transfer is
   the expected result after this change alone.
2. **This is a design, not a result.** No implementation was done. No
   experiment was run. No claim about empirical outcomes is made.
3. **Visibility is not usability.** Making structures visible does not
   imply the learner can use them. Barriers 3 and 4 remain.
4. **This does NOT establish SUF, L3, or C0-D.** The change is
   researcher-owned infrastructure. Learner-owned structural decisions
   remain zero.
5. **This does NOT obsolete H2, H3-lite, or reuse work.** It is a
   parallel infrastructure design for future transfer research.

## Standing Architectural Metric (Projected)

If implemented as designed:

| Metric | Value |
|---|---|
| RESEARCHER-OWNED STRUCTURAL DECISIONS | 1 (make structures visible to gather) |
| LEARNER-OWNED STRUCTURAL DECISIONS | 0 |
| SOURCE-ENUMERABLE FORMS | all (no new assemblers) |
| SUF DECISIONS | 0 |
| LEARNER-INTERNAL CRITERIA | 0 |
| REUSE EVENTS | 0 (visible but not used) |
| REVISION EVENTS | 0 |
| COGNITION LINES | ~25 added |
| MODES | 0 |
| BRIDGES | 0 |
| HANDLERS | 0 |
| SEMANTIC CASES | 0 |

## Summary

**Barrier picked:** 1 (visibility of prior structures to construction).

**Minimal machinery:** Extend `t2_gather` to enumerate tag-20 MAPs
alongside tag-1 FACTs. Return structure descriptors. Add white-box
counters. ~25 lines. No new opcodes, modes, or bridges.

**Honest result:** Zero transfer enabled. Barriers 3 and 4 still block
completely. But visibility is the necessary precondition for studying
them, and this design provides maximum diagnostic information per unit
of architectural change.

**Status:** Design only. Not implemented. Not frozen.

---

No em dashes were used in this document (verified).
