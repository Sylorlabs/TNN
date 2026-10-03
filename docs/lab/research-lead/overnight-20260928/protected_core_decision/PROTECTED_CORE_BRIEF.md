# Protected-Core Decision Brief: Structural Graph Mutation

## PREPARED FOR MICAH - NOT DECIDED

Date: 2026-10-01 (UTC)
Preparer session: c7a2367f-1cd2-4bf7-90b8-aefdaf7886bc

This document prepares a decision for Micah. It does not make the decision.
Nothing here authorizes implementation. Any TNN-3 work building on any
alternative below must go through its own preregistration with frozen kill bars.

---

## 1. The Exact Decision

**Question:** May the protected core expose structural graph mutation operations
to learner-built executable graphs, and if so, which operations?

**Precise formulation:** The frozen TNN-2 ISA (MOVE, BRANCHEQ, INC, DEC over frame
registers) has exactly one read bridge into the workspace (operand 0..999 reads
field20 of a node) and no write bridge back. A learner-built executable graph
cannot allocate a node, write a node field, link or kill an edge, or deactivate
a cell. The H3 hypothesis (procedures as learner-built graphs) requires closing
this effect-domain gap. The decision is whether to close it, how, and with what
governance.

**What is NOT being decided:**
- Whether to implement H3-lite (that needs no ISA change; it is a design awaiting preregistration)
- Whether to build TNN-3 (that needs its own preregistration)
- The specific TNN-3 kill bars (draft, not frozen, awaiting Micah's review separately)
- Any change to the frozen TNN-2 binary (it stays frozen regardless)

**Why this is Micah's decision:** Under the escalation boundary, a decision that
changes the protected-core boundary is his. The protected-core ISA ruling
(2026-09-30) established that the core is a small frozen domain-neutral
computational basis. Growing it, even with domain-neutral operations, changes
that boundary.

---

## 2. Alternatives

### Alternative A: Forbid structural ops (keep the ISA frozen as 4 ops)

The protected core remains MOVE, BRANCHEQ, INC, DEC over frame registers.
No ALLOC, no field WRITE, no edge LINK/KILL, no node/edge structural READ
beyond the existing field20 peek. The effect-domain gap stays open permanently.

Under this alternative:
- Full H3 (procedures as learner-built graphs) is impossible. The H3 probe
  (section 1d) proved the revision procedure cannot be expressed without
  structural effects.
- H3-lite remains available. It moves decisions into learner state without
  moving procedures. No ISA change needed.
- The "procedures remain source" limitation is permanent architectural fact,
  not a temporary gap.

### Alternative B: Allow the minimal structural set in the protected core

Add to the protected core the smallest set of domain-neutral structural
operations sufficient for learner-built procedures to manipulate the workspace
graph store. The H3 probe (section 1c) sketches the requirement:

- ALLOC: allocate a node, return its id
- WF (write field): write a value to a node's field
- LINK: create an edge (from, type, to)
- KILL: remove an edge, or deactivate a node
- Structural READ: read node fields and edge fields (beyond the current
  field20-only peek)

These are the operations the revision procedure performs in Zag source today
(lines 706-763 of `tnn2.zag`): scan edges, allocate nodes, write fields,
link edges, rewire, tombstone. The probe's 40-60 cell sketch shows the control
flow is already ISA-expressible; only the effects are missing.

Under this alternative:
- Full H3 becomes architecturally possible. Learner-built graphs could
  implement blame localization, repair application, search policies.
- The ISA grows from 4 ops to approximately 9-10 ops. This is a protected-core
  boundary change.
- The bootstrap problem is solvable via the MUL Rung B template (fixed minimal
  basis, learner structure above it, one reflective level).

### Alternative C: H3-lite only (defer the structural decision)

Adopt H3-lite as the TNN-3 direction. Parameterize the three mechanisms'
researcher-chosen decision points as reads from learner-state policy nodes,
with production write paths from experience. No ISA change. Revisit the
structural question only if H3-lite proves insufficient.

Under this alternative:
- The decision is deferred, not made. H3-lite is explicitly a stepping stone
  that routes around the gap.
- If H3-lite delivers policy revisability but procedures remain unrevisable
  in ways that block L3, the structural question returns.
- Risk: "revisability theater" (the movable-priorities analysis, `f70ab617c`).
  Write paths exist but are never meaningfully exercised. K-H3 condition (d)
  guards via sealed tests where decision change must be outcome, not input.

### Alternative D: A second executable graph type for structural procedures

Keep the 4-op ISA frozen for computational procedures. Add a separate
structural graph type with its own executor for procedures that manipulate
the workspace. This is the option the H3 probe (section 1d, option b) names
and rejects without a strong unification argument.

Under this alternative:
- Reintroduces the two-graph-type problem the TNN-2 prereg eliminated
  (K-T2-2/K-T2-3 killed `exec_plan` vs `execute`).
- Would need to survive the One-System Rule. The probe judges this unlikely
  without overwhelming justification.
- Included for completeness; not recommended.

---

## 3. Evidence

### 3a. The H3 probe (`94cecdba4`)

**Finding:** The frozen 4-op ISA cannot express the revision procedure because
its effect domain is frame registers and the procedure's work is workspace
graph mutation. The gap is precisely the structural effect class.

**Cheap check result:** No production path in the frozen source can modify the
trial search order, the guide schema, or the repair topology from experience.
H3 confirmed as structural fact for all three mechanisms.

**Bootstrap assessment:** Solvable via MUL Rung B template. The hard part is
not bootstrapping but the effect-domain gap.

**Single blocker:** Everything in H3 reduces to one gap (structural effects)
plus one governance decision (whether the protected core may expose it).

### 3b. The DOF map (`d2af26581`)

**Finding:** Pure LEARNER decisions in the cognition path: 0. MIXED: 5.
RESEARCHER: approximately 240.

**The "any topology?" answer:** No. Nowhere does the learner choose a topology,
a procedure, or a question.

**Movable-priorities refinement (`f70ab617c`):** "Zero learner-owned criteria
is the disease; zero pure decisions is the symptom. Every MIXED point uses a
researcher-fixed criterion (argmax bid, first-to-verify, scan order) over
learner-supplied data: the learner supplies facts, the researcher supplies
judgment."

**Relevance:** The DOF map shows the locus-of-control problem is total. H3-lite
moves criteria into learner state. Full H3 moves procedures. The structural
decision determines whether the second move is possible.

### 3c. The C0-D analysis (`8bfb80fdd`)

**Finding:** Promoted graphs shadow themselves via `ev_teach_in` at line 541.
MAPs are never read at query time. "No FW1-FW9 score, even 9/9, can establish
C0-D for construction, since the output is causally inert at query time
regardless of score."

**Second cause:** Graphs are value traces, not portable procedures. The ISA has
no relational-dereference, so subject-general procedures are inexpressible.

**Relevance:** C0-D fails for two reasons: (1) the wiring bypass (fixable without
structural ops), and (2) the value-trace encoding (a deeper architectural issue).
Structural ops would enable learner-built procedures but would not by themselves
fix the value-trace problem. The decision should not be oversold as fixing C0-D.

### 3d. The red teams (all three ATTACK-SUCCESS)

**Construction (`340e94e3e`):** Three fixed assemblers, finite family, oracle
verifier. L2, not L3.

**Inquiry (`4e329c772`):** Constant action 30, content -999. Miss flag, not
discriminating inquiry. L6 absent.

**Revision (`687ba0219`):** Single-schema literal-patch. Learner selects stale
cell and observed literal. L1.

**Shared pattern (synthesis `42b4dfa91`):** "Enumerated-schema / filled-slot."
The researcher chooses the form; the learner fills runtime-selected indices
and literals.

**Relevance:** All three mechanisms fail C0-A (runtime-defined semantics) for
the same reason: procedures live in source. H3 is the hypothesis that names
this shared cause. The structural decision is whether to enable the fix.

### 3e. The ISA ruling context

Micah's protected-core ISA ruling (2026-09-30) allows as protected machinery:
"ALLOC, READ, WRITE, LINK, COPY, COMPARE/EQ, basic arithmetic such as ADD,
BRANCH, APPLY/EXECUTE, generic state/register operations."

The ruling permits the class. The frozen TNN-2 ISA contains none of the
structural half (no ALLOC, no WRITE, no LINK). The ruling allows; the freeze
fixed an instance without them. Reconciling those is the governance work this
brief prepares.

---

## 4. Consequences

### If Alternative A (forbid):

**What becomes possible:** H3-lite. Policy revisability without procedure
ownership. The TNN-3 roadmap's minimal three components (H3-lite policies,
repair-proposal generator, inquiry resolution) all work within the frozen ISA.

**What is foreclosed:** Full H3. Procedures as learner-built graphs. Any future
claim that "the learner invented this procedure" where "procedure" means the
operational method, not just its parameters. C0-A remains permanently failed
at the procedure level.

**Risks:** The "revisability theater" risk (write paths exist, never exercised).
The "criteria without procedures" ceiling: the learner can revise which repair
topology to use but cannot invent a sixth topology. H1 remains unaddressed.

**Architectural consequence:** The protected core stays at 4 ops permanently.
The One-System Rule is satisfied trivially (one graph type, one executor).
The cost is a permanent capability ceiling on procedure invention.

### If Alternative B (allow minimal structural set):

**What becomes possible:** Full H3. Learner-built procedures for search,
repair, inquiry policies. One reflective level (procedure that edits procedure
graphs, executed by the same core). The MUL Rung B pattern extends across the
effect-domain gap.

**What is required:** A governance process for the ISA extension. The new ops
must be domain-neutral (no FIND_POLYNOMIAL_ORDER equivalents). The bootstrap
must be specified (copy-then-revise is the cheapest). Kill bars must cover
the new capability (K-H3 needs strengthening to procedure-level).

**Risks:**
- **Scope creep:** "Minimal" is hard to hold. Each new world may suggest "just
  one more op." The freeze rule ("never grow it one benchmark at a time") must
  be enforced by governance, not goodwill.
- **Complexity:** The protected core grows from 4 to ~10 ops. More machinery
  in the trusted base. The "tiny general machine" gets less tiny.
- **False promise:** Structural ops enable H3 but do not guarantee it. The
  learner must still actually build procedures. The value-trace problem (C0-D
  analysis) is separate. The oracle problem (H2) is separate.

**Architectural consequence:** The protected core boundary moves. This is
irreversible in practice (removing ops breaks learner-built procedures that
depend on them). The One-System Rule is preserved (one graph type, one
executor, extended ISA). The benefit is removing the ceiling on procedure
ownership.

### If Alternative C (H3-lite only, defer):

**What becomes possible:** Everything in Alternative A, plus the option to
revisit. H3-lite tests whether moving decisions suffices before paying for
moving procedures.

**What is deferred:** The structural question. If H3-lite hits the "criteria
without procedures" ceiling, the decision returns with more evidence.

**Risks:**
- **Delay:** If full H3 is needed, time is spent on H3-lite first. But H3-lite
  is cheap (no ISA change) and its failure mode is informative.
- **Theater:** The revisability-theater risk is highest here, because H3-lite
  is explicitly a compromise. K-H3 condition (d) is the guard.

**Architectural consequence:** No boundary change now. Maximum option value.
The cost is time and the risk of building on a stepping stone that does not
reach the far bank.

### If Alternative D (second graph type):

Not recommended. The H3 probe already judged this against the One-System Rule.
Included only for completeness.

---

## 5. Specific Questions

### Minimal set if allowed?

From the H3 probe section 1c, the revision procedure needs:
1. **ALLOC** (node allocation)
2. **WF** (field write)
3. **LINK** (edge creation)
4. **KILL** (edge removal / node deactivation)
5. **Structural READ** (node fields, edge fields; beyond current field20 peek)

This is 5 operations. The probe notes the ISA ruling already lists ALLOC, READ,
WRITE, LINK, COPY as the allowed class. The minimal set is that class minus COPY
(not needed for the revision sketch) plus KILL (needed for tombstoning).

**Open sub-question:** Should structural READ be a separate op, or an extension
of the existing operand 0..999 peek? The current peek reads field20 only. A
general structural read would specify field. This is a design detail for the
preregistration, not this brief.

### Interaction with the ISA freeze?

The TNN-2 ISA freeze (F-T2-1: no new opcode/mode/bridge/handler/semantic case)
governs the frozen TNN-2 binary. It does not govern TNN-3. Any TNN-3
preregistration would specify its own ISA, frozen at preregistration time.

The question is not "can we change TNN-2's ISA" (no, it is frozen). The question
is "may TNN-3's protected core include structural ops." That is a new
preregistration with a new freeze, not a violation of the old one.

**Critical:** The decision must be made before TNN-3 preregistration, because
the preregistration freezes the ISA. Deciding after preregistration would
require amending the freeze, which the governance rules forbid (never weaken
or retroactively alter a frozen kill bar; same principle for a frozen ISA).

### Where is the "protected core" boundary?

From the ISA ruling and the H3 probe:

**Inside the protected core (frozen, domain-neutral machinery):**
- The ISA ops (currently 4; possibly extended per this decision)
- The executor (`execute`)
- Memory management (allocation, field access)
- The APPLY/EXECUTE primitive

**Outside the protected core (learner state, revisable):**
- Cognitive procedures (search policies, repair policies, inquiry policies)
- Policy nodes (H3-lite)
- Promoted graphs (MAPs)
- Facts, uncertainties, guides

**The boundary question:** Are structural mutation ops "machinery" (inside) or
"intelligence" (outside)?

The ISA ruling's allowed class includes ALLOC, READ, WRITE, LINK, COPY as
"machinery, not intelligence." By that standard, structural ops belong inside.
The frozen TNN-2 instance simply did not include them.

The counterargument: every op added to the core is a commitment. The core is
"small" by design. Growing it from 4 to ~10 ops is a 2.5x increase. "Small" is
not a number, it is a judgment. That judgment is Micah's.

### How does H3-lite relate? Sufficient or stepping stone?

**The H3-lite design (`22197da2c`) is explicit:** It is a stepping stone, not
a destination.

What H3-lite delivers:
- Policies revisable by experience (trial order, guide template, repair
  dispatcher)
- H3's testable prediction without H3's governance cost
- The K-H3 kill bar (draft)

What H3-lite does NOT deliver (section 7 of the design):
1. Procedures remain researcher-authored Zag code. C0-A still fails at the
   procedure level.
2. The repair family remains researcher-enumerated. H1 unaddressed.
3. The acceptance oracle remains. H2 unaddressed.
4. The guide remains non-discriminating (revisable, not discriminating).
5. All heuristics (thresholds, margins) are researcher-chosen.
6. No capability improvement predicted on frozen FW1-FW9.

**Is it sufficient?** For policy revisability, yes. For procedure ownership,
no. The design states this plainly: "H3-lite moves decisions into learner
state; it does not move procedures there."

**Stepping stone assessment:** H3-lite is worth doing regardless of the
structural decision, because:
- It is cheap (no ISA change)
- It tests the H3 prediction at the decision level
- If it suffices, the structural decision may never be needed
- If it fails, the failure is informative about what procedures (not just
  decisions) need to be learner-owned

The TNN-3 roadmap (`67a420cca`) places H3-lite at Step 2, after H2 probes
(Step 1) and before H1 widening (Step 4). This order is deliberate: do not
widen the constructor (H1) before fixing the oracle (H2), and do not pay for
procedures before testing whether decisions suffice.

---

## 6. Recommendation

### RECOMMENDATION (NOT A DECISION)

**Recommended: Alternative C (H3-lite only, defer the structural decision),
with the structural question banked for re-examination after H3-lite results.**

**Reasoning:**

1. **H3-lite is cheap and informative.** It requires no ISA change, no
   governance exception, no irreversible commitment. It directly tests whether
   moving decisions into learner state delivers the H3 prediction. If it does,
   the structural question may be moot. If it does not, we will know exactly
   what procedures (beyond decisions) need learner ownership.

2. **The structural decision is irreversible in practice.** Once learner-built
   procedures depend on ALLOC/WF/LINK/KILL, removing those ops breaks them.
   The core only grows; it never shrinks. Deferring preserves option value.

3. **The roadmap order supports deferral.** H2 probes come first (Step 1),
   then H3-lite (Step 2). The structural question is not on the critical path
   for the next experiments. Deciding now would be premature; deciding after
   H3-lite results would be informed.

4. **The risks of Alternative B are real.** Scope creep ("just one more op"),
   core complexity growth, and the false promise that structural ops guarantee
   H3. These risks are manageable but not zero. Deferral avoids them for now.

5. **Alternative A (permanent forbid) is too strong.** It forecloses full H3
   forever based on current evidence. The H3 probe showed the gap is tractable
   and well-localized. A permanent forbid would be a stronger claim than the
   evidence supports.

**Conditions for re-examination:** Bank the structural question with explicit
triggers:
- H3-lite is implemented and evaluated (per its own preregistration)
- H3-lite shows the "criteria without procedures" ceiling (policies revise,
  but capability does not improve because procedures remain fixed)
- OR a sealed world requires a procedure topology that H3-lite's
  researcher-enumerated families cannot express

If any trigger fires, the structural decision returns with empirical evidence
about exactly which procedures need learner ownership.

**What Micah is asked to approve (not decide now):**
- That H3-lite may proceed to preregistration (separate decision)
- That the structural question is banked with the above triggers (this brief)
- That Alternative A (permanent forbid) is rejected (the question stays open)

---

## 7. Banked Items

- This decision (structural graph mutation in the protected core)
- Triggers for re-examination (see section 6)
- K-H3 DRAFT-NOT-FROZEN (needs Micah's review before governing anything)
- The 6 open questions from the kill-bar draft (separate brief)
- Full H3 preregistration (pending this decision and H3-lite results)

---

## Verdict

PROTECTED-CORE-BRIEF-COMPLETE.

Brief prepared. No decision made. Committed locally. Nothing pushed.

*End of brief. Paper untouched. No source modified. No scores claimed.*
