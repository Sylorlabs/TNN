# TNN-2 Red Team Synthesis: Shared Architectural Causes

Date: 2026-10-01. Synthesizer session: dbbd2fef-29b8-4a77-99f2-1e9e21a130ab.
Inputs (read-only, commits verified in `tnn-native-lab` history):

- Construction ATTACK-SUCCESS: `340e94e3e`,
  `tnn2_redteam_construction/CONSTRUCTION_REDTEAM.md`
- Inquiry ATTACK-SUCCESS: `4e329c772`,
  `tnn2_redteam_inquiry/INQUIRY_REDTEAM.md`
- Revision ATTACK-SUCCESS: `687ba0219`,
  `tnn2_redteam_revision/REVISION_REDTEAM.md`

Target under attack: `tnn2.zag` at `f4de7ff46` (frozen).
This is root-cause clustering, not TNN-3 design. No source edits made.
No per-mechanism patches proposed.

## Verdict

REDTEAM-SYNTHESIS-COMPLETE.

All three ATTACK-SUCCESS results reduce to one shared architectural
pattern, named here the **enumerated-schema / filled-slot pattern**:
in each mechanism the researcher authored the schema (the space of
possible structures and the procedure that fills it) and the learner
fills runtime-chosen slots (literals, cell indices, miss content)
inside that schema. The filled result is then recorded as
"learner-created structure." Every mechanism is genuine at filling
slots and genuine at persisting the result; none of them lets the
learner choose the schema. Three different mechanisms, one shared
failure to transfer structural authority from source code to learner
state.

---

## 1. The shared architectural pattern

Across construction, inquiry, and revision, the division of labor is
identical in form:

1. **Researcher enumerates the possible.** In source, before any
   experience: the construction grammar (three assemblers), the
   inquiry guide (constants 30/-999), the repair procedure
   (tombstone + literal SETREG + rewire). The space of mechanism
   outputs is finite and enumerable from the source.
2. **Learner fills the blanks.** At runtime: which literal from
   observed facts, which cell index from provenance lookup, which
   (s, r) miss content. These are genuine runtime choices from
   genuine data.
3. **The filled schema is recorded as learner state.** Provenance
   edges, promoted graphs, uncertainty nodes, POLICY_ROOT links,
   revised graphs all persist. This part is real.
4. **The learner never chooses among schemas, because there is only
   ever one.** The choice of what kind of structure to build, what
   question to ask, or what repair topology to apply is not a learner
   decision; it is the only thing the code can do.

Micah's standing question ("What part of the topology was actually
chosen by the learner?") gets the same answer in all three cases:
**the operands, never the topology.** That is the shared cause. It is
also why all three mechanisms pass their surface kill bars while
failing generality: the kill bars tested that runtime filling and
persistence work (they do), not that the learner chose the schema
(it did not).

A sharper formulation: TNN-2 moved the *content* of cognition into
learner state but left the *form* of cognition in source code.
TNN-1's failure was fixed templates with fixed content. TNN-2's
residual failure is fixed templates with variable content. The
advance from TNN-1 to TNN-2 is real (variable content, runtime
rejection, persistence, provenance), and it is exactly one rung
short: variable content is L2 parameter filling; choosing form is
the missing L3 step.

### How the three attacks instantiate the pattern

- **Construction.** The finite family (chains, sums, counts; sums
  dead in production) is the schema. Literals, paths, relations from
  data are the slots. `t2_trial` enumerates the researcher's family
  in the researcher's order until the environment-supplied answer
  says yes. Open construction would require the learner to choose
  the grammar, not the literals.
- **Inquiry.** The guide is the schema: action 30, content -999,
  written as literals at `miss_inquire` lines 805-808. The miss
  trigger and the (s, r) content recorded in the uncertainty node
  are the learner-chosen slots. A derived discriminating need would
  be a learner-chosen schema; what exists is a constant schema with
  learner-filled trigger metadata. The missing L6 resolution
  transition is the same pattern from the other side: the schema for
  "what happens when evidence arrives" was never authored at all,
  so stale guides persist.
- **Revision.** `t2_revise_graph` is a single-member repair schema:
  tombstone the BRANCHEQ-guarded SETREG, insert a literal SETREG,
  rewire guard target and SEQ. Which cell and which observed literal
  are the learner-chosen operands; the procedure, the replacement
  type, the rewire targets, and the always-tombstone decision are
  researcher-chosen. The trial machinery is never invoked, so there
  is not even a search over a family; there is one schema and it
  always fires.

### What this rules out as an explanation

It is not the case that one mechanism is learner-driven and the
others are hardcoded. All three sit at the same level: genuine
runtime slot filling inside a researcher-enumerated schema. It is
also not the case that the mechanisms are broken in implementation:
each does what its source says, deterministically, with real
persistence, real rejection (construction), real revert on failure
(revision), and real selection machinery (inquiry's `ev_act`). The
attacks succeeded on generality, not on correctness. This matters
for interpreting the freeze scores in section 4.

---

## 2. Learner-chose vs researcher-chose tabulation

### 2a. Construction (`t2_trial`, lines 581-672)

| Decision | Chosen by | Evidence |
|---|---|---|
| The three graph families and their exact wirings | Researcher | `t2_asm_chain`, `t2_asm_sum`, `t2_asm_count` (363-413); 4 `promote_graph` call sites, all in `t2_trial` |
| Slot assignment (slot0 subject/output, slot1 counter) | Researcher | `t2_exec` (421-422); only slots 0,1 initialized |
| Guards test slot0; sets write slot0 | Researcher | assembler code, no alternative |
| Search order (chains k=2..4, sums, counts, single hops) | Researcher | hardcoded with "composition-preserving" comment |
| All bounds (depth 4, 96 paths, 12 values, 4095 subsets, total <= 900, 16 links, 32-cell signature) | Researcher | literals in source |
| Frame layout and verifier semantics | Researcher | `t2_try_verify` (497-510) |
| Which literal values fill the guards/sets | Learner (data) | from observed facts via `t2_gather` |
| Which paths/subsets/relations exist | Learner (data) | from workspace content |
| Which candidate verifies first | Learner (data) | order-dependent but data-dependent |
| The expected answer used for verification | Environment | `ev_query` param; parsed from QUERY event in shim |
| Whether sums are reachable in production | Researcher (test-gated) | `comb_present` needs type-8 node; only created at line 1106 in test `t_p2` |

Net: learner fills literals and selects among candidates; researcher
chose the grammar, the order, the bounds, and the oracle criterion.

### 2b. Inquiry (`miss_inquire` 795-812, `ev_act` 859-911)

| Decision | Chosen by | Evidence |
|---|---|---|
| Miss trigger (fires only after retrieval, construction, bootstrap all fail) | Learner-originated | `ev_query` 813-834; verified on empty state |
| Uncertainty node creation with miss-specific (s, r) content | Learner-originated | `miss_inquire` 796-799; no scaffolding |
| Guide -> POLICY_ROOT linkage in persistent state | Learner-originated | 800-804, 809-810; sole production site |
| Guide action value (30) and content (-999) | Researcher | constants at 805-808 |
| What evidence would discriminate; which question is informative | Nobody (absent) | no such computation anywhere on the path |
| ACT selection machinery (bid, context, supersession) | Researcher (machinery), learner (state) | `ev_act` real code over learner state; trivially satisfied with one guide |
| What happens to uncertainty/guides when evidence arrives | Nobody (absent) | no resolution, no supersession; stale guides persist |

Net: learner detects the miss and records it; researcher fixed the
guide's content to a constant and authored no resolution procedure.
Inquiry is a miss flag plus a constant action.

### 2c. Revision (`revise_on_contradict` 685, `t2_revise_graph` 706-763)

| Decision | Chosen by | Evidence |
|---|---|---|
| Which MAP to revise | Deterministic lookup | contradicted fact (690-694) |
| Which cell is stale | Deterministic lookup; last-match-wins on ties | provenance scan (711-717); arbitrary on ties |
| Which guard protects it | Deterministic pointer chase | field 12 (719-724) |
| Replacement cell type (always SETREG tag 101) | Researcher | 726; no alternative branch |
| Replacement value | Observed literal `new_o`; no search | 725; supplied by environment |
| Rewire targets (guard->new->succ) | Researcher | 727-730 |
| Tombstone vs keep | Researcher (always tombstone) | 731 |
| Guard predicate revision, branch insertion, rerouting to existing steps, loop changes, multi-step repair | Nobody (absent) | no code paths; operator returns 0 |
| Whether to use the trial/search machinery | Researcher (never) | `t2_trial` never invoked on revision path |

Net: learner (plus deterministic lookup) supplies operands: which
cell, which literal. Researcher chose the single repair topology.
The "corrected step" stores the observed constant; it does not
compute anything.

### 2d. The pattern, compressed

| Mechanism | Researcher chose | Learner chose | Missing |
|---|---|---|---|
| Construction | grammar, order, bounds, oracle | literals, which candidate | choice of grammar |
| Inquiry | guide constants, no resolution schema | miss trigger, (s,r) content | derived discriminating need, resolution |
| Revision | repair topology, always-literal replacement | operands (cell, value) | search over repair topologies |

In all three: **operands yes, topology no.**

---

## 3. One change or three?

### The honest answer

No single *small* change addresses all three, because each mechanism's
researcher-chosen schema lives in a different place (assemblers,
guide literals, repair procedure) and each would need its own
integration work. But there is a single *architectural* change that
addresses all three at the root, and it is worth stating precisely
because it is also the compression direction from section 5 of
Micah's directive:

**One open recursive graph-construction substrate, used by all three
mechanisms, whose output space is not enumerated in source.**

Concretely, the change has one core and three integrations:

- **Core:** replace the finite assemblers with a constructor whose
  productions include composition of previously promoted graphs
  (MUL Rung B demonstrated this standalone; `t2_trial` does not use
  it). The constructible space then grows with learner state instead
  of being bounded by source literals. Bounds, if any, emerge from
  learner-managed resources rather than hardcoded caps.
- **Construction integration:** the trial loop proposes in this
  open space. This directly attacks the finite-menu finding.
- **Revision integration:** contradiction re-invokes the same
  constructor over a repair space with more than one member, instead
  of executing the single-schema patch. The revision red team named
  exactly this as the acceptance condition. This directly attacks
  the single-schema finding.
- **Inquiry integration:** the "guide" becomes a constructed
  discrimination structure built by the same substrate (a question
  is a small executable graph whose execution selects the informative
  action), and resolution becomes re-invocation of the substrate
  when evidence arrives. This directly attacks both the constant
  guide and the missing L6 link.

Why this one change fixes multiple failures (per Micah's
requirement): the shared cause in section 1 is that form lives in
source. A single substrate that constructs form from learner state,
shared by construction, revision, and inquiry, moves form into
learner state once and serves all three mechanisms. It is also a
deletion story: three fixed assemblers, the constant guide
literals, and the single-schema repair procedure are all replaced
by uses of one mechanism. Capability up, researcher-authored
machinery down, which is the mandated compression direction.

### The caveat that must be recorded

The core above is necessary but not sufficient for inquiry. Even
with an open constructor, the learner must decide *which*
discrimination structure to build and *when* a guide is resolved.
That decision procedure is itself a schema that could be
researcher-authored again (a fixed "build the most informative
question" routine is just a fancier constant). The inquiry failure
has two layers: the guide's form is fixed (addressed by the shared
substrate) and the informativeness criterion is absent (not
addressed by the substrate alone). Any TNN-3 proposal must say
where the informativeness criterion lives; if it lives in source,
inquiry stays L2 at best. This is banked as an open design question
in section 6, not decided here.

Similarly, revision needs more than the substrate: the acceptance
criterion for a repair candidate must not be "reproduces the
observed literal," or the substrate will just rediscover
literal-storing patches. The verification-oracle issue (section 5,
hypothesis H2) interacts with the substrate change and must be
handled alongside it.

---

## 4. Implications for the running TNN-2 freeze evaluation

The freeze measures **capability**: can the frozen TNN-2 binary pass
FW1-FW9 and hold W1-W9. The red teams measure **mechanism
generality**: does the way it passes transfer to structures the
researcher did not enumerate. Both can be true at once, and the
expected outcome is that both ARE true:

- **If TNN-2 scores above 4/9 on FW:** that is a legitimate
  capability result. The frozen FW1-FW9 worlds were sealed before
  TNN-2 existed, so improvement over TNN-1's 4/9 is a valid causal
  comparison: the three new mechanisms fixed the capability gaps
  they were designed to fix. The sealed-evaluation discipline is
  intact. Report the score plainly and credit the mechanisms for
  what they do.
- **The score does not establish generality or L3, and must not be
  claimed as such.** FW1-FW9 target exactly the structures the
  finite families can express (chains to depth 4, counts,
  BRANCHEQ-guarded SETREG repairs, single-constant inquiry). A
  9/9 would show the schemas cover the battery, not that the
  learner chooses schemas. Per Micah's directive, FW1-FW9 are now
  a regression / targeted-repair battery for TNN-2, since TNN-2
  was designed with TNN-1's failures on those worlds in view.
- **The red team results bound the interpretation of any freeze
  score.** A high score plus three ATTACK-SUCCESS verdicts means:
  TNN-2 is a more capable slot-filler than TNN-1, not a general
  constructor. The honest summary line for the freeze report is
  that capability improved within the researcher-enumerated
  envelope and the envelope itself is unchanged in kind.
- **The post-freeze adversarial battery is the important
  generality test,** exactly as Micah ordered. It must contain
  worlds whose required structures are outside the three
  families, repairs outside the single schema, and inquiries
  whose informative action varies with learner state. The red
  team reports are effectively a specification for that battery:
  each "what would change this verdict" section (construction
  section 7, inquiry's derived-need and resolution requirements,
  revision section 7) names the adversarial pressure to apply.
- **No freeze outcome invalidates the red teams, and no red team
  outcome invalidates the freeze.** They answer different
  questions. A freeze regression on a prior pass (FW1/FW2/FW4/FW5)
  would be a capability bug to root-cause; it would not change the
  generality analysis.

---

## 5. At least three structurally different hypotheses for the root bottleneck

Per Micah's requirement: before TNN-3, >=3 structurally different
hypotheses for the bottleneck, with an explicit argument for why a
change under each hypothesis fixes multiple failures. These are
competing explanations at different architectural levels, not three
patches. They are hypotheses to discriminate experimentally, not
recommendations.

### H1. The output space of every mechanism is enumerated in source (the grammar hypothesis)

**Statement.** The bottleneck is that each mechanism's possible
outputs form a finite set written by the researcher: three linear
assemblers, one guide shape, one repair topology. The learner's
freedom is selection and parameterization within the set. This is
the pattern documented in section 1, stated as a causal claim:
because the space is enumerated, no mechanism can produce a
structure the researcher did not pre-shape, which is exactly what
the construction boundary probes (5-hop unrepresentable), the
inquiry constant-guide finding, and the revision single-schema
finding each demonstrate independently.

**Why a change here fixes multiple failures.** All three
mechanisms fail at the same level: the set of things they can emit
is fixed. Replacing enumeration with recursive composition of
learner-promoted structures (the section 3 substrate) removes the
enumerated bound once and widens all three mechanisms'
output spaces simultaneously: construction can emit deeper and
nonlinear graphs, revision can emit structurally different repairs
(repair candidates are just constructed graphs), inquiry guides
can be constructed discrimination structures rather than
constants. One change to the constructor, three mechanisms widened.
This is also the hypothesis most aligned with the MUL Rung B
evidence: hierarchical construction from a primitive basis was
demonstrated standalone, so the missing piece is integration, not
invention of a new idea.

**How to discriminate it.** Freeze the constructor change alone
(open compositional proposals, everything else identical) and
re-run the three red team probe suites: the 5-hop construction
probe, a two-schema repair probe (e.g., guard-predicate change),
and a varying-informative-action inquiry probe. H1 predicts all
three move together. If construction opens but revision stays
single-schema, H1 is insufficient and the bottleneck is at the
integration level (each mechanism re-imposes its own enumeration),
which points toward H3.

### H2. The environment supplies the answer, so nothing must be discovered (the oracle hypothesis)

**Statement.** The bottleneck is verification, not generation.
Construction accepts a candidate iff its output equals an
environment-supplied expected value parsed from the QUERY event;
revision inserts the just-observed literal as the "corrected"
value. In both cases the mechanism never needs to discover
anything: the answer is given, and the mechanism's job reduces to
encoding the given answer in an acceptable shape. A system that is
handed the answer on every trial has no selection pressure to
develop genuine discovery, discrimination, or derivation; slot
filling is the optimal strategy under an oracle, and the
architecture converged to it.

**Why a change here fixes multiple failures.** The oracle appears
in two of the three mechanisms and its absence explains the third's
weakness. Under H2, the fix is learner-internal acceptance:
candidates are accepted by prediction (the learner predicts, the
world confirms or surprises) rather than by matching a supplied
target. For construction, masked verification (predict the
unobserved value, then check) forces the graph to compute rather
than match. For revision, the corrected content must be derived
or selected among alternatives, not copied from the contradicting
observation; otherwise revision is memorization. For inquiry, the
oracle hypothesis explains why no discriminating need is computed:
when answers are always supplied, there is never a need to ask a
good question. Removing the oracle creates the selection pressure
that makes inquiry's missing L3 link load-bearing. One change to
the verification regime, and all three mechanisms face genuine
discovery pressure.

**How to discriminate it.** Keep the finite grammar fixed and
change only verification: masked queries where `expected` is
withheld, plus revision probes where the corrected value must be
computed from other facts rather than copied from the observation.
H2 predicts the current mechanisms fail these probes while
passing unmasked ones, and that no grammar widening alone fixes
the failure. Note the tension with H1: H1 says the space is too
small; H2 says the acceptance test is too generous. Both can be
true; the discrimination experiment tells us which binds first.

### H3. The mechanisms' operating procedures are source code, not learner state (the procedure-ownership hypothesis)

**Statement.** The bottleneck is one level up from H1. Even the
procedures that fill the slots; the trial loop's search order, the
miss-to-guide pipeline, the tombstone/insert/rewire sequence; are
Zag source, not learner-constructed executable graphs. C0-A fails
in all three mechanisms for the same reason: the semantics of how
to construct, how to inquire, and how to revise reside in
researcher-authored code. The learner owns data and parameters;
the researcher owns every procedure. TNN-2 moved content into
learner state but no procedure followed it. Until a mechanism's
operating procedure is itself a learner-built structure executed
by the protected core, each mechanism is a researcher-authored
cognitive subsystem wearing learner-state persistence as a
disguise, which is precisely what the One-System Rule was written
to forbid.

**Why a change here fixes multiple failures.** H3 is the deepest
cut and the only one that addresses the inquiry caveat in section
3. If the trial search policy, the guide-derivation policy, and
the repair policy are themselves constructed executable graphs in
learner state (bootstrapped from the protected ISA, one level
down), then improving the constructor improves all three policies
at once, because they are all uses of the same substrate. It also
collapses the architecture: instead of three researcher-written
mechanisms plus a constructor, there is one constructor and three
learner-built policies, which is the compression direction Micah
mandated. The multi-failure argument is structural: the three
ATTACK-SUCCESS verdicts are three instances of "procedure lives in
source"; moving procedure into learner state retires the entire
class, not one instance.

**How to discriminate it.** The test is whether a mechanism's
policy can be revised by experience. Construct a world where the
fixed search order (chains before counts) systematically picks the
wrong family first, or where the constant guide action is
systematically uninformative, and check whether the learner can
alter its own policy from evidence. H3 predicts the current
architecture cannot: policies are source literals, unrevisable by
any production path (consistent with the inquiry red team's
finding that no production path revises guides). A weaker,
cheaper discrimination: check whether any production path can
modify the trial search order or the repair schema from
experience. If none exists, H3 is confirmed as a structural fact
regardless of which hypothesis explains the capability gap.

### How the three hypotheses relate

- H1 (enumerated output space) and H2 (oracle verification) are
  about what the mechanisms can emit and accept. They are
  experimentally separable per the discrimination sketches above,
  and both may bind.
- H3 (procedure ownership) is about where the mechanisms themselves
  live. It contains H1 as a special case in one sense (an
  enumerated grammar is a procedure living in source), but it makes
  a distinct, stronger prediction: that no experience can revise the
  mechanisms' policies. That prediction is testable without building
  TNN-3.
- The recommended experimental order before any TNN-3 design is:
  (1) run H3's cheap policy-revisability check (pure analysis of
  production paths, no new worlds needed); (2) run H2's masked
  verification probes; (3) only then consider H1's constructor
  widening, because widening the space before fixing the oracle
  produces a larger finite menu under the same generous acceptance
  test, which is the exact treadmill Micah forbade.

---

## 6. Banked items and open questions (no blocking)

This synthesis is analysis only and blocks nothing. The following
are recorded for the parent coordinator; none requires Micah's
ruling tonight, and independent lanes continue.

1. **Informativeness criterion placement (from section 3 caveat).**
   If TNN-3 adopts the shared substrate, where does the criterion
   for "which question is worth asking" live? Source placement
   keeps inquiry at L2. Learner placement requires the learner to
   construct its own value-of-information estimate, which is itself
   a hard open problem. Banked as the central design question for
   any inquiry work.
2. **H1 vs H2 binding order.** Both hypotheses may be true; the
   discrimination experiments in section 5 determine which binds
   first. The recommended order (H3 check, H2 probes, H1 widening)
   is a recommendation to the coordinator, not a governance
   decision.
3. **Freeze-score interpretation language.** Section 4 proposes the
   honest summary line for the freeze report ("capability improved
   within the researcher-enumerated envelope; the envelope is
   unchanged in kind"). The coordinator may adopt or refine it when
   the evaluator lands.
4. **No architectural decision is requested of Micah at this
   time.** Per his directive, work continues on all independent
   lanes: the running freeze evaluation, the post-freeze
   adversarial battery, compression analysis, and reproduction.
   The hypotheses above are inputs to the next root-cause cycle,
   not a TNN-3 proposal.

---

## 7. Ledger and claim implications (for the governance lane)

- The three ATTACK-SUCCESS verdicts are mechanism-generality
  results, not capability results. They do not alter any frozen
  kill bar and do not retroactively change TNN-2's BUILD-PASS or
  REPRO-PASS, which were correctly scoped to build and
  reproduction.
- No L3 claim survives for any of the three mechanisms:
  construction is L2 (finite-family structural learning),
  inquiry is a learner-triggered miss flag with constant action
  (below L2 as inquiry; the trigger/uncertainty creation alone is
  L1-L2 infrastructure), revision is L1 (parameter filling inside
  a researcher-authored repair template; the T2-REVISE trace shows
  L0 storage of the observed literal).
- Criterion 0 status: construction fails C0-B/C0-C (finite
  enumerable family); inquiry fails at L3 (hardcoded) and L6
  (absent); revision fails C0-A/B/C with C0-D unestablished.
- The shared pattern in section 1 should be recorded as a named
  architectural finding ("enumerated-schema / filled-slot") so
  future mechanisms are audited against it at preregistration
  time rather than discovered by red teams after the fact. A
  preregistration checklist item of the form "list every
  structural decision the learner can make that the source cannot"
  would have caught all three.

---

*End of synthesis. Verdict: REDTEAM-SYNTHESIS-COMPLETE.*
