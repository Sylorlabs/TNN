# Composition Memory vs the V2 Hole: Red Team Assessment

Verdict: **VULNERABLE**. The composition memory design, as written,
introduces the exact graph shape the confirmed V2 hole exploits, under
normal operation rather than adversarial construction. The design is
silent on SETREG-level provenance through extraction and splice, so it
neither prevents the exploit shape nor defines the revision interaction
for composites. This is a required design amendment before any
preregistration, not a reason the mechanism is unbuildable.

## 1. The confirmed hole

V2 probe (`705833a27`, V2-HOLE-COMPLETE: CONFIRMED):

- `t2_revise_graph` accepts a repair iff `out != -999999`
  (re-execution succeeded). It never checks `out == new_o`, where
  `new_o` is the contradicting observation.
- Exploit shape: value-transforming steps AFTER the
  provenance-carrying SETREG. Probe 1 demonstrated with a hand-crafted
  graph `g0 -> st0(set reg0<-300, prov->f0) -> st1(set reg0<-999)`:
  contradicting `f0=(100,200,300)` with `new_o=500` retargets `st0` to
  500, but trailing `st1` overwrites to 999. `out=999 != new_o=500`,
  yet accepted because `999 != -999999`. The MAP was retargeted to 999
  and a fact `(100,200,999)` was taught, silently discarding the
  observation `(100,200,500)`.
- Honest scope from the probe: "deficient but not currently exploited"
  because the trial assemblers happen to build graphs where the
  provenance SETREG is terminal (chain), the repair fails safe
  (interior guard failure), or the acceptance is coincidentally
  correct (count). The probe states the hole "would become exploitable
  if graphs with value-transforming steps after provenance-carrying
  SETREGs ever entered learner state (e.g., via composition memory or
  hand-built procedures)."

The precise corruption condition: the hole bites when the MAP's
`(s,r)` matches the contradicted fact's `(s,r)` but `out != new_o`.
In that case the revision teaches a fact that directly contradicts
the observation that triggered the revision. (Probe 2, the count
case, is safe on this reading: the count MAP's `(s,r)` differs from
the contradicted link fact's `(s,r)`, so no direct contradiction is
taught. This distinction matters for the recommended criterion fix
in section 5.)

## 2. How composition memory introduces the exploit shape

The design (`19fa59b6f`, DRAFT-NOT-FROZEN) creates interior
provenance with trailing transforms through three normal mechanisms:

**2a. Chained fragments (the normal multi-fragment case).** The splice
operation connects a fragment's exit cell to the splice point's output,
and the design explicitly contemplates chaining fragments through the
problem's dependency shape (W5: "the inter-fragment wiring is derived
from the fragments' recorded F-interfaces chained through the
problem's dependency shape"). In a chain `F1.exit -> F2.entry ->
F2.exit -> answer`, every provenance-carrying SETREG inside F1 is
interior to the composite, with F2's value-transforming steps
trailing. This is not a degenerate case; it is the mechanism's
intended mode of operation for novel composites.

**2b. Fragment-internal walked topology.** Extraction walks "the cells
the executor touched between the graph's entry point and its
answer-producing step." That walked set includes interior SETREGs
carrying provenance (e.g., a chain's intermediate steps each cite the
fact they read). If the composite places any steps after the
fragment's exit cell, those interior SETREGs gain trailing
transforms they did not have in the original verified graph.

**2c. Literal-stripping preserves transform structure.** Extraction
"records that walked topology with literals stripped to parameter
slots." A trailing literal overwrite (Probe 1's `st1(set reg0<-999)`)
becomes a slot with default filling 999; the overwrite SHAPE survives
extraction. Splicing with default fillings reproduces the
value-destroying tail. The design's W3 guard (trace-walk, not fixed
slices) ensures the SHAPE is history-determined, which is good for
SUF, but it does not remove trailing transforms; it preserves them
faithfully.

The frozen trial's safety rested on a distributional assumption: the
assemblers emit graphs where the provenance SETREG is terminal. The
V2 probe confirmed the criterion is safe only under that assumption.
Composition memory breaks the assumption by design, because
composition IS the placement of computed structure after
provenance-carrying steps.

## 3. The design's provenance silence

Grep over the design document: 9 mentions of "provenance," all
referring to F-provenance (episodic: world id, episode counter,
parent graph). Zero mentions of SETREG-level provenance (prov->fact),
zero mentions of SETREG at all.

Two notions are conflated by omission:

- F-provenance (tracked): which experience created the fragment.
- SETREG provenance (untracked): which fact a graph step cites, the
  field the revision blame path keys on ("picks one SETREG by direct
  provenance," blame assignment `0917f3e25`).

The design specifies neither whether extraction preserves SETREG
provenance fields nor what the revision path should do with a
composite whose provenance structure spans multiple fragments and
domains. Both resolutions are bad under the current criterion:

- **Case A: provenance preserved.** The V2 hole applies directly
  (section 4). Additionally, a fragment's SETREGs cite facts from the
  fragment's original domain; splicing into a composite for a new
  problem embeds cross-domain provenance edges, so contradicting an
  old-domain fact triggers revision of a new-domain composite
  (blame contamination across the composition boundary).
- **Case B: provenance stripped.** Composites become revision-inert:
  contradicting the original fact finds no provenance-carrying
  SETREG in the composite, so no revision fires and the composite
  goes silently stale. This is a different correctness gap (stale
  composites, no repair path), not the V2 hole, but it is
  unaddressed all the same.

The blame assignment analysis already flags "fragment provenance"
(step->fragment edges) as missing machinery, but for the purpose of
blaming fragments, not for the SETREG prov->fact interaction. The
composition design does not reference that gap.

## 4. Conceptual exploit demonstration

Setup (no implementation; trace through specified mechanisms only):

1. WORLD A curriculum promotes a chain graph. Extraction walks the
   trace; fragment F is stored. F's walked topology contains interior
   SETREG `st` with `prov->fA` (an intermediate chain step), followed
   within F by the remaining chain steps (value-propagating
   transforms).
2. A WORLD D composition problem selects F (structural match on
   F-shape) and splices it, chaining a second fragment G after F's
   exit to transform F's output into the required answer form.
   Composite C is verified against the harness and promoted. C's
   graph contains `st` (prov->fA) with trailing transforms from both
   F's tail and G.
3. `fA` is contradicted with `new_o`. `ev_observe` ->
   `revise_on_contradict` -> blame walk finds `st` by direct
   provenance (the fixed researcher-authored walk; it does not know
   about fragments). `t2_revise_graph` copies C's graph into fresh
   cells (copy-and-commit), retargets `st` to `new_o`, re-executes.
4. The trailing transforms (F's tail, G's steps) compute
   `out = T(new_o)` where T is the composed transform. In general
   `T(new_o) != new_o`. `out != -999999` (execution succeeded), so
   the V2 criterion accepts.
5. The MAP is retargeted to `out`; a fact `(s,r,out)` is taught. If
   C's `(s,r)` matches `fA`'s `(s,r)`, the taught fact contradicts
   the observation `(s,r,new_o)`. The revision has manufactured a
   contradiction with the evidence that triggered it, and the
   observation is silently discarded. Copy-and-commit does not
   mitigate this: it commits the wrong repair atomically and safely,
   preserving the original only as a fossil of the error.

Note on step 3: the blame walk "broadcasts blame to every
provenance-linked MAP" and revises each. Under Case A, a single
contradiction could trigger wrong-but-accepted revisions across
every composite that ever spliced a fragment citing the fact,
multiplying one observation's corruption across the fragment
reuse graph. The reuse the design seeks (section 7: "fragments are
reused as parts of novel wholes") is exactly the fan-out vector.

## 5. Recommendations

**R1 (required before preregistration): amend the design to specify
SETREG-provenance through extraction and splice.** The two options:

- (a) Preserve provenance, and require the build to carry the
  criterion fix in R2. Accept cross-domain blame edges as specified
  behavior with the R3 trap probe guarding it.
- (b) Strip provenance, and specify explicit staleness semantics for
  composites (when a cited fact is contradicted and no provenance
  survives, what retires or re-verifies the composite?).

The current draft specifies neither. This blocks the
fresh-vs-experienced contrast test's revision leg: without a
specified provenance semantics, a contradiction episode on a
composite has no predicted outcome, and the preregistration cannot
state a kill bar for it.

**R2 (criterion fix, for the future build; frozen TNN-2 untouched):
strengthen V2 with an (s,r)-match refinement.** After revision,
if the MAP's `(s,r)` equals the contradicted fact's `(s,r)`,
require `out == new_o`; otherwise retain the current
`out != -999999` check. This closes Probe 1 (MAP `(100,200)`
vs fact `(100,200)`, `999 != 500`, rejected) without breaking
Probe 2 (count MAP's `(s,r)` differs from the link fact's
`(s,r)`, lenient check applies, accepted). This is precise and
minimal, but it is a stopgap: it patches the symptom for the
identity-answer case and leaves the deeper gap in R4.

**R3 (prereg guard): contradiction episode on a composite.** The
fresh-vs-experienced contrast test (design section 6) must include
a contradiction of a fact cited by an interior fragment SETREG,
with the predicted outcome stated per the R1 amendment (correct
retarget, safe failure, or specified staleness handling). Silent
acceptance of `out != new_o` with matching `(s,r)` is the trap
condition. Lifetime protocol v2 (`dd745851e`) already banks a
V2-hole trap probe in World C; the composition preregistration
should reference it rather than invent a second one.

**R4 (deeper, TNN-3 scope): answer-vs-fact dependency semantics.**
The V2 criterion cannot in general distinguish "the answer should
equal the new fact value" (chain/identity) from "the answer is a
function of the fact value" (count/computed). The architecture has
no representation of this relationship; it is the "MAP contracts"
gap from the plan-constructor analysis (`61402fd25`). Until graphs
carry their answer's dependency semantics, any acceptance
criterion is either too strict (a blanket `out == new_o` rejects
the correct count revision) or too lenient (the current hole).
The R2 refinement is the best local patch; the general solution
is contractual.

## 6. Explicit non-claims

1. This assessment does not show composition memory is
   unbuildable. It shows the current draft has an unaddressed
   correctness interaction (fragment composition vs
   provenance-keyed revision under a vacuous acceptance
   criterion) that would become a silent-corruption vector. The
   vector is closable via R1+R2, but the closure must be
   specified before building, not discovered after.
2. The exploit is demonstrated conceptually per the tasking ("not
   by building it"). No variant was constructed; no new
   measurements were taken. The shape argument rests on the
   design's specified splice semantics and the probe's confirmed
   criterion behavior.
3. Copy-and-commit (revision substrate `880c87c4c`) is not a
   mitigation for this hole: it makes wrong revisions atomic,
   not correct. Its safety guarantee covers failed revisions;
   the V2 hole is about wrongly accepted ones.
4. No SUF, L3, or architecture claims are made or affected. This
   is a correctness finding about a design/criterion
   interaction.

## Standing metric (red-team delta)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: 0
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: 0
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0
