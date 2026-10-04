# Composition Build Questions: Resolutions

Status: DRAFT-NOT-FROZEN. Analysis only; nothing built, nothing tested.
Resolves the four open questions in section 6 of
AMENDMENT_R1_SETREG_PROVENANCE.md (commit bda26cf91).

Grounding: field numbers verified against the frozen base source
(bootstrap_loop/bl_base.zag, byte-identical verbatim frozen copy).
MAP (tag 20) production field usage: field 0 = tag, field 4 = r,
field 8 = s, field 20 = graph root, field 24 = promotion index,
field 28 = answer, field 36 = live flag. Fields 12, 16, 32, 40, 44,
48, 52, 56, 60 are written but never read by any production path
(field 12 and field 16 are set to -1 by promote_graph; field 32 is
written 0). Header field 16 (hg(W,16)) is the global trial-stats
counter and is unrelated to MAP field 16.

## Q1. Splice trace storage format

### Decision

The per-SETREG rebound-vs-nulled trace lives in the composite MAP's
own spare header fields. No sidecar node. No new edge type.

Exact layout (composite MAP, tag 20):

- Field 12: n_trace, the number of traced SETREGs (0 if the
  composite's fragment SETREGs were all nulled or the composite
  used no fragments). Overwrites the frozen -1; the -1 is never
  read by production code.
- Fields 40 + i, for i = 0 .. n_trace - 1: the cited fact node id
  for SETREG i in fragment-walk order (the order the extraction
  walk records SETREGs; splice preserves it), or -1 if the
  rebound-vs-nulled decision for that SETREG took the nulled
  branch.
- Bound: n_trace <= 8. A splice that would trace more than 8
  SETREGs must fail at splice time (splice returns failure; the
  composite is not built). This is a build-enforced bound stated
  in the preregistration, not silent truncation. Fragments are
  small by design (chain graphs of k = 2..4 steps carry 2-4
  SETREGs; the count and sum families carry comparably few), so
  8 is headroom, not a constraint on realistic composites.

White-box read procedure (for the K-COMP-REV-1 precondition and
any audit): read ng(W, composite, 12) for the count, then
ng(W, composite, 40 + i) for each entry. All data is inside the
MAP node. No edge-table scan required.

### Rejected alternative

A sidecar trace node (new tag, linked from the composite) was
rejected: it adds a node type, an allocation failure mode, and a
link-maintenance burden for data that fits in 9 verified-free
fields. If a future design needs traces beyond 8 SETREGs, that
design must justify the sidecar then; this build does not pay
for it now.

### Field 32 is not used

Field 32 is verified free in frozen production, but H3-lite
Node 1's variant uses field 32 as its miss-count. To avoid a
cross-build field collision if composition memory and H3-lite
ever coexist in one learner, this specification reserves field 32
and does not touch it.

## Q2. Non-fact slot fillings

### Decision

The amendment's default is confirmed and tightened into a rule
with no exceptions:

**A prov edge points only at a fact node (tag 1). Any slot
filling whose value does not originate from a live fact node
gets prov = null.**

Case table (exhaustive for the design's splice mechanics):

1. Slot filled from the new problem's data, and that data
   originates from a live fact node f_new: prov = f_new.
   This is the rebound branch. The only case that creates a
   live dependency.
2. Slot filled from the fragment's default filling (stripped
   literal recorded at extraction): prov = null. The value is
   a cached constant. (Amendment section 2.3 rationale stands:
   pointing at the old fact would manufacture a false
   dependency and reintroduce cross-domain blame.)
3. Slot filled from a computed intermediate: a value produced
   by another SETREG or graph cell inside the same composite
   (for example the output of an earlier fragment's graph in
   a chained composite). prov = null.

   Justification for case 3: the intra-composite data
   dependency is already carried by the composite's SEQ edges
   (type 12), which encode cell-to-cell data flow. Revision
   granularity is the composite, not the cell: copy-and-commit
   revises the composite's graph as a unit. And the composite
   is still reachable by the blame walk, because the producing
   upstream SETREG carries its own rebound prov edge to the
   live fact that licensed its value; contradicting that fact
   reaches the composite through the upstream cell. Null on
   the downstream cell loses nothing the blame walk needs.
4. Slot filled from a harness-supplied literal with no fact
   node: prov = null. A literal with no fact node is a
   constant by construction.

### Build requirement

The build must state this rule verbatim in its source comments
at the splice function, and the preregistration must include a
probe for case 3: build a composite with a chained computed
intermediate, contradict the upstream live fact, and verify
that revision fires on the composite (via the upstream
SETREG's rebound edge) and does not attempt to revise the
intermediate cell as a separate target. If revision fails to
fire, FAIL (the null-prov cell broke blame reachability).

## Q3. F-utility write-path identification

### What the design leaves unspecified (information needed)

COMPOSITION_MEMORY_DESIGN.md specifies F-utility as "two
counters, invocations and successes" on the fragment record
(section 2, lines 72-75) but does not specify the fragment
record's node tag or the field offsets of the two counters.
The build must specify these before any write path can be
identified at the source line. This is the one piece of
information this analysis cannot supply from the frozen base:
the fragment record does not exist in frozen TNN-2.

### Write paths, anchored to the frozen base

Once the fragment record layout is specified, the write paths
are the following production events (function names and line
anchors are in bl_base.zag, the verbatim frozen base):

1. Invocation write (selection): in the future splice
   function (new code, no frozen anchor). When fragment F is
   selected and instantiated into composite C, increment F's
   invocation counter exactly once per splice. This happens
   regardless of the composite's later fate; selection is the
   event, not success.

2. Success write (verification): in promote_graph
   (bl_base.zag line 532). After the trial graph verifies and
   at the MAP creation point (the ns(W,m,0,20) writes), for
   each fragment id in C's fragment list, increment its
   success counter. The write is part of the same production
   event as promotion; it must not be a separate deferred
   pass.

3. Success write (revision): in t2_revise_graph
   (bl_base.zag line 706), at the `return 1` point (after
   ns(W,m,28,out), the answer retarget). For each
   participating fragment, increment success if and only if
   the revision was accepted with out == new_o (the R2
   condition). This is the amendment section 4.2 requirement
   made line-concrete.

4. No-success writes: on R2-rejection (the new branch the
   build adds: out != new_o with matching (s,r) causes
   revert and return 0) and on total failure (the existing
   `return 0` paths in t2_revise_graph), success counters
   are not incremented. Invocation was already counted at
   splice; the success-to-invocation ratio is the demotion
   signal. Recording failures as explicit non-increments
   (rather than a separate failure counter) keeps the
   F-utility format at exactly the two counters the design
   specifies.

### How the composite names its fragments

The revision-time write path (item 3) starts from the
composite MAP and must find the participating fragment
records. Node spare fields are insufficient for both the
splice trace (Q1, fields 40-47) and a fragment-id list, so
fragment participation is recorded relationally: an edge
from the composite MAP to each participating fragment
record node, using one new edge type ET_FRAGUSE (value 14,
the next free value after the 13 existing types).

Rationale: edges are TNN's native white-box idiom for
relations; the edge table is scanned by the existing blame
walk machinery; composites are few so edge-table cost is
negligible. This is a +1 researcher-owned structural
decision (one new edge type) that the build's
preregistration must declare explicitly. It is not hidden
inside the Q1 field layout.

At revision time, the write path enumerates edges of type 14
from the composite to collect fragment ids, then increments
the counters on the fragment records. The K-H3 write-path
audit applies: the preregistration must show each of the
three write paths (items 1-3) firing on the sealed test
transcripts.

## Q4. H3-lite Node 3 interaction

### What each mechanism governs

- H3-lite Node 3 (frozen prereg 9084a7760, section Node 3):
  selects which repair topology t2_revise_graph attempts.
  Field 20 of the tag-40 subtype-3 policy node holds the
  preferred topology id 0-5 (default 5, literal-patch). The
  body of t2_revise_graph becomes a dispatch on field 20.
  Each topology is researcher-written and preserves the
  verify-by-reexecution and revert-on-failure contract.
  Success counters for the six topologies are packed in
  fields 24, 28, 32 of the policy node.
- The R1 amendment: governs what a topology's provenance
  means (rebind-or-null at splice, section 2) and the
  acceptance criterion (R2: if the MAP's (s,r) equals the
  contradicted fact's (s,r), require out == new_o).

These compose without overlap: Node 3 chooses the repair
procedure; the amendment constrains what the procedure may
conclude. Neither implies the other.

### Does Node 3 see composites?

Yes, through the existing path, with no composite-specific
logic required. revise_on_contradict (bl_base.zag line 685)
dispatches on prov edges (type 1) from the contradicted fact
to MAPs. A composite's rebound prov edges are type-1 edges
to live facts, so contradicting such a fact reaches the
composite through the unmodified dispatch loop, and the
Node 3 dispatcher then selects the topology. The dispatch
is topology selection; it is orthogonal to the MAP's
provenance structure. No composite-shaped branch is added
to the dispatcher.

### Does Node 3 revise composites?

Yes, via the same path. The selected topology operates on
the composite's graph under copy-and-commit. The
amendment's section 4.1 stands regardless of topology: the
composite is revised, the fragment is not auto-superseded,
and fragment quality flows through F-utility (Q3).

### The R2 enforcement requirement

If both mechanisms are built into one learner, every one of
the six researcher-written topologies must implement the R2
refinement in its verification step, because any topology
could be dispatched onto a composite. The preregistration
for the combined build must state whether Node 3 is
present:

- Node 3 absent: the K-COMP-REV bars run with topology 5
  (literal-patch) only.
- Node 3 present: the K-COMP-REV bars must pass regardless
  of which topology the dispatcher selects on each episode.
  In particular the K-COMP-REV-2 trap (wrong-but-running
  with matching (s,r) must be rejected) must hold for all
  six topologies, not just the default.

This is a preregistration-level decision. It must not be
discovered at build time.

### Separate credit assignments

When a composite is revised via topology T and accepted,
two counters increment for two different purposes and must
not be conflated:

- F-utility success on each participating fragment record
  (fragment quality; Q3 item 3).
- The Node 3 policy node's packed success counter for
  topology T (topology quality; H3-lite prereg Node 3
  production write path).

A fragment being good and a topology being good are
independent claims. The build must keep the write paths
separate and the preregistration must not allow one
counter's movement to be cited as evidence for the other.

### Residual risk (stated, not hidden)

The success-criteria analysis (commit 04af42736) established
that Node 3's counters are vulnerable to the V2 hole:
wrong-but-running repairs increment the topology's success
counter, so a topology producing systematically
wrong-but-running repairs becomes preferred. R2 closes this
for the matching-(s,r) case. For the non-matching-(s,r)
case the lenient check (out != -999999) remains, and Node 3
can still learn the wrong lesson there. This residual is
inherent to the R2 stopgap; the general fix is MAP
contracts (red-team R4, TNN-3 scope). The combined-build
preregistration must name this residual explicitly and
must not claim Node 3's learned preference is correct
beyond the R2-covered cases.

### Independence

Node 3 can be built without composition memory (it operates
on trial-built MAPs). Composition memory can be built
without Node 3 (revision uses topology 5, the default).
The sections above apply only to the combined build.

## Standing architectural metric (analysis delta)

This analysis adds no cognition lines, modes, bridges,
handlers, or semantic cases. It specifies build decisions
for machinery the design and amendment already propose.

- RESEARCHER-OWNED STRUCTURAL DECISIONS: +2, honestly
  labeled as build-specification decisions, not
  learner-authored: (1) the Q1 splice-trace field layout
  (field 12 count, fields 40+i entries, n_trace <= 8
  bound, field 32 reserved); (2) the Q3 fragment-
  participation edge type ET_FRAGUSE (value 14).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0.
- SUF DECISIONS: 0. LEARNER-INTERNAL CRITERIA: 0.
- REUSE EVENTS: 0. REVISION EVENTS: 0.
- COGNITION LINES: 0. MODES: 0. BRIDGES: 0.
- HANDLERS: 0. SEMANTIC CASES: 0.
- SOURCE-ENUMERABLE FORMS: +1 (the ET_FRAGUSE edge type
  is enumerable from the build source once specified).

## What remains for the build's preregistration

1. Fragment record node tag and F-utility field offsets
   (Q3 information gap).
2. The n_trace <= 8 splice-failure bound, stated as a
   kill-bar-adjacent build invariant.
3. The case-3 computed-intermediate probe (Q2).
4. The Node 3 presence/absence decision and the
   all-topologies R2 requirement if present (Q4).
5. The named R2 residual for non-matching (s,r) (Q4).
6. K-H3 write-path audit transcripts showing the three
   F-utility write paths firing (Q3).

No em dashes were used in this document.
