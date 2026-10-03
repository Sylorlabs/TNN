# HYPOTHESES: substrate changes for TNN-3

Lane: TNN3, wave-20261001-1721pdt. Analysis only; nothing built, no experiments run.
Grounding: `ROOT_CAUSE.md` (three shared architectural causes) and `ARCH_ACCOUNTING.md`
(researcher-written vs learner-owned structure per mechanism) in this lane.
Battery record: `docs/lab/rsi/runs/wave-20261001-1421pdt/sealed_adv/RESULT_SEALED_ADV_BATTERY.md`.

Standing rules honored: no-patch-treadmill (cluster by shared cause; hypotheses must fix
multiple failure members, never one world); ONE-SYSTEM RULE (no new modes, bridges,
routers, handlers, or task-specific admission gates); capability-source delta near zero
(each hypothesis records cognition source lines added as zero or negative); new capability
must come from EXPERIENCE leading to new LEARNED STATE, not a new Zag subsystem.
Protected-core ISA additions, where any appear, are restricted to the allowed class
(ALLOC, READ, WRITE, LINK, COPY, COMPARE, arithmetic, BRANCH, APPLY/EXECUTE, generic
state operations): machinery, never benchmark-specific semantic operations.

## The three clusters, restated as substrate gaps

- Cluster A (no abstraction tier): every learned structure is keyed to the demonstrating
  instance. Members: M1-W1 (novel P-then-Q composition), M1-W3 (shared-step diamond),
  M3-W1 generalization probes. Gap (a): learner-owned procedure representation.
- Cluster B (no lifecycle): creation without supersession, unpromotion, or re-derivation.
  Members: M2-W2 (stale guide re-fires), M3-W2 (second contradiction silently no-ops),
  M3-W3 (reverted revision vetoes relearning). Gap (b): content-bearing
  lifecycle-managed uncertainty (M2 side); also implicated in revision (M3 side).
- Cluster C (closed control plane): every decision lives in researcher code that
  experience cannot reach. Members: M1-W2 (no inversion), M2-W1 (no informant
  discrimination), M2-W3 (no action content), M3-W1 singleton (no evidence weighting).
  Gaps (a), (b), (c) each carry part of this.

## Gap (a): learner-owned procedure representation

### H1. Learner-named procedure objects over the frozen ISA

Substrate change: promote executable graphs from stamped per-instance literals to
learner-owned named objects. The learner gains one generic affordance: LINK cells into
a sequence and NAME the sequence with a learner-chosen handle; EXECUTE (already
approved protected machinery) runs any named object. Procedures stop being keyed by
(subject, relation) MAP fields and become addressable structures the learner creates,
references, and reuses across instances.

Fixes multiple members: M1-W1 (composition becomes naming a sequence that references
two named procedures, which the menu could never enumerate); M1-W3 (a shared step
becomes one named object linked by two graphs, which stamped literals could never
express); M3-W1 generalization (a named procedure with unbound parameter slots applies
to unseen subjects, which per-instance MAPs could never do). One change addresses all
three Cluster A members because all three are the same missing thing: an
instance-independent procedure object.

Capability-source delta: cognition source lines added zero; lines deleted about 155
(the four assemblers at roughly 75 lines and the schema menu order at roughly 80
lines). No new modes, bridges, routers, or handlers. Naming and linking ride on the
existing node and edge allocation machinery.

Falsifiable prediction: on a sealed composition world, if the learner creates named
procedures but white-box inspection shows zero reuse of any name across instances
(every name is written once and executed once on its demonstrating instance), H1 is
dead: the affordance alone does not produce abstraction, and the missing piece is not
naming.

### H2. Learner-asserted derivation direction (invertible learner links)

Substrate change: the learner may assert derivation links in either direction over
structures it created, including cells whose guard tests an output slot and whose set
writes an input slot. Inversion becomes a construction the learner expresses with the
generic LINK affordance, not a schema the researcher must supply. Structurally
distinct from H1 (which is about naming and composition): this is about the learner
owning the direction of derivation.

Fixes multiple members: M1-W2 (backward queries become learner-constructed inverse
derivations rather than a missing menu entry); M1-W1 (composition can be chained as
learner-linked derivation steps even before naming exists); M3-W2 (provenance becomes
learner-maintained bidirectional links instead of researcher-anchored DEP edges
pointing at superseded fact nodes, so the second contradiction finds a live target).
It spans Cluster A and Cluster B because both contain failures of researcher-fixed
directionality.

Capability-source delta: cognition source lines added zero; the forward-only
assumption is deleted from the assemblers and the generic LINK operation (already
protected machinery) is no longer direction-restricted by researcher code. Net
negative.

Falsifiable prediction: on a sealed backward world, if the learner creates inverse
links but EXECUTE of the inverted structure still cannot answer because the 4-op ISA
cannot express the needed computation (for example inversion requires arithmetic the
ISA lacks), H2 is dead in its current form: learner-owned direction is insufficient
without richer executable content, and the ISA boundary itself is the constraint.

### H3. Procedure-as-operand unification (graphs are ordinary nodes)

Substrate change: executable graphs live in the same addressable memory as facts, so
a procedure can be an operand of another procedure. The separate graph-cell
allocation path is folded into the generic node allocator; the fact machinery's
READ/LINK operations apply to graphs without special casing. Structurally distinct
from H1 (naming) and H2 (direction): this is about applicability, enabling
meta-structure such as a procedure that takes another procedure as input.

Fixes multiple members: M1-W3 (the diamond becomes one shared sub-procedure applied
by two parent procedures, a step object referenced twice); M1-W1 (compose becomes
apply-procedure-Q to the output of procedure-P, with both as first-class operands);
M3-W1 generalization (a law can be represented as a procedure parameterized by
another procedure's output). All three are failures of procedures being second-class
relative to facts.

Capability-source delta: cognition source lines added zero; the MAP-versus-graph
special casing (separate layouts, separate selectors) is deleted. Net negative. No
new modes, bridges, or handlers.

Falsifiable prediction: after unification, if on sealed worlds the learner never
stores a graph as a fact operand (white-box shows zero procedure-as-operand links
despite the affordance being exercised elsewhere), H3 is dead: representational
unification does not by itself produce meta-use, and the barrier is behavioral, not
representational.

## Gap (b): content-bearing lifecycle-managed uncertainty

### H4. Learner-authored content-to-action projection

Substrate change: replace the researcher-constant action write in `miss_inquire`
(field20=30) with a learner-owned projection structure, a small executable cell over
the frozen ISA that the learner authors, mapping uncertainty content (subject,
relation, and whatever the learner has attached) to an action value. `ev_act` keeps
only the generic machinery of reading field20. The action alphabet becomes
learner-extensible because the learner writes the projection.

Fixes multiple members: M2-W1 (informant discrimination: the learner can author a
projection emitting 1/2/3 for different uncertainty contents, which the fixed
alphabet {30, 0} forbade); M2-W3 (the constant-action triple: the projection is
exactly the missing content-to-action wire, so actions can now carry bits about
content). Both are Cluster C members on the M2 side, and both are the same missing
wire.

Capability-source delta: cognition source lines added zero; the constant write and
the fixed-alphabet assumption are deleted. The projection cell is learner-created
and executed by existing protected EXECUTE machinery. Net negative.

Falsifiable prediction: on a sealed informant-selection world, if the learner
authors projections but white-box inspection shows they collapse to constants (the
projection cell ignores the content fields and emits one value regardless), H4 is
dead: content is available but the learner does not exploit it, so the missing piece
is a signal that rewards discrimination, not the wire.

### H5. Generic supersession transition on the cognition path

Substrate change: supersession, unpromotion, and re-derivation become one generic
protected transition applicable to ANY learner structure (guides, MAPs, taught
facts), driven by learner-maintained standing rather than researcher-written
per-type handlers. The dormant `contradict_map` machinery is connected to the
cognition path; the selectors (`ev_act`, `activate`) already honor supersession, so
the change is permitting the cognition path to write CON edges on guides and MAPs,
which today no code path does. Structurally distinct from H4 (content): this is
about time.

Fixes multiple members: M2-W2 (the guide is superseded when its uncertainty
resolves, so it cannot re-fire); M3-W2 (the MAP is superseded on the second
contradiction and re-created against live facts, so the stale-provenance lookup
cannot silently no-op); M3-W3 (the taught fact is unpromoted on revert, so
`ev_query`'s exact-hit check cannot veto re-derivation). This is Cluster B wholesale,
and notably it spans M2 and M3, which the per-mechanism clustering keeps separate.

Capability-source delta: cognition source lines added near zero (call sites that
connect existing dormant code); the special-case contradiction path in `ev_observe`
is folded into the generic transition, so net lines are negative. No new modes,
bridges, routers, or handlers: one transition, all structure types.

Falsifiable prediction: after wiring, if on a sealed resolution world the learner
still re-fires stale guides because no experience ever writes the CON edge
(white-box shows zero guide-CON edges across the run), H5 is dead: the machinery is
permitted but never used, so lifecycle must be driven by something the learner
maintains (standing, per H6/H11), not merely permitted by the core.

### H6. Standing-bearing uncertainty objects

Substrate change: merge the UNCERT node with the evidence model so that uncertainty
carries support counts the learner updates on every related experience, and the same
standing drives inquiry action selection and retirement. The researcher's fixed
`bid()` formula (edge-type counts) is deleted; a guide's bid becomes the
learner-maintained standing of its UNCERT node, updated by generic
CONFIRM/CONTRADICT events the learner links. Structurally distinct from H4
(projection of content) and H5 (generic transition): this makes uncertainty itself
a persistent evidence-bearing structure whose magnitude the learner controls.

Fixes multiple members: M2-W2 (standing falls to zero on resolution, retiring the
guide through the H5 transition); M3-W1 singleton probe (a single contradiction
against high standing does not cross the revision threshold); M2-W1 (uncertainties
with higher standing outbid trivial ones, giving selection real content). It spans
M2 and M3 because both mechanisms needed evidence magnitudes and neither had them.

Capability-source delta: cognition source lines added zero; `bid()`'s fixed formula
(about 12 lines) is deleted and standing updates are learner-linked events, not
researcher decisions. Net negative.

Falsifiable prediction: on a sealed noise-versus-signal world, if the learner's
standing counts do not discriminate (a singleton contradiction and a systematic
shift produce identical standing trajectories), H6 is dead: the learner cannot
maintain meaningful support magnitudes, and evidence weighting would require
researcher-defined counting semantics, which contradicts the zero-delta claim.

## Gap (c): evidence-weighted revision

### H7. Revision as re-derivation from live facts

Substrate change: delete the single literal-swap revision schema
(`t2_revise_graph`, about 46 lines) and replace the revision operator with
supersede-then-rederive: the contradiction marks the old MAP superseded (H5
transition) and the learner's own construction process runs again against the
current fact store. The unit of revision becomes re-derivation, not patching.
Structurally distinct from H5 (the generic transition) and H6 (standing): this is
about what revision DOES.

Fixes multiple members: M3-W2 (no stale provenance: re-derivation reads live facts,
so there is no DEP edge to a dead node to miss); M3-W3 (no revert veto: a failed
re-derivation leaves the old structure superseded rather than restoring a stale
taught fact, so relearning is never short-circuited); M3-W1 generalization (if
construction is learner-owned and abstract per H1/H8, re-derivation lifts the
correction to all instances at once).

Capability-source delta: cognition source lines added zero; about 66 lines of
revision-schema code deleted. Net negative. No new handlers: re-derivation reuses
whatever construction the learner owns.

Falsifiable prediction: on a sealed law-reversion world, if re-derivation
reproduces the identical stale structure (because the learner's construction
process is still the stamped-path schema and nothing about it changed), H7 is dead:
re-derivation without a changed construction process is a treadmill that re-learns
the same wrong thing, and revision cannot be fixed independently of construction.

### H8. Law objects with parameter slots and generic BIND edges

Substrate change: the learner can create one LAW structure representing a regularity
with named parameter slots instead of stamped literals, plus generic BIND edges from
instances to slots; revision edits the law once and all bound instances see it.
Structurally distinct from H1 (naming whole procedures) and H7 (the revision
process): this is about parameterization as a first-class relation, separating the
regularity from its instances.

Fixes multiple members: M3-W1 generalization (one edit to the x+5 law propagates to
unseen subjects 42105/42106, which per-instance literal patching could never do);
M3-W1 singleton probe (a law with accumulated standing resists single-instance
noise, since the trigger weighs the law's support, not the instance's); M3-W2
(provenance anchors to the law node, which instance fact turnover never supersedes,
so repeated revision keeps finding its target).

Capability-source delta: cognition source lines added zero; the laws themselves are
learner-created. The only researcher addition is protected-core-class machinery
(a BIND edge type and slot addressing in the ISA, comparable to LINK), which is
domain-neutral and frozen after introduction, never grown per benchmark. No new
modes, bridges, routers, or handlers.

Falsifiable prediction: on a sealed law world, if the learner creates laws but
binds every instance to its own private copy (white-box shows N law objects for N
instances with no shared slot structure), H8 is dead: the learner does not discover
parameterization even when it is expressible, so the regularity stays instance-keyed
regardless of the affordance.

### H9. Standing-gated revision trigger from dormant instruments

Substrate change: the revision trigger reads the MAP's learner-maintained standing
(SUP/CON balance via the dormant `map_standing`, updated by the dormant `log_ev`
event stream) instead of firing on any contradiction; `contradict_map` retires MAPs
whose standing collapses. This connects instruments the researcher already wrote but
never wired to the cognition path. Structurally distinct from H6 (uncertainty
standing) and H7 (re-derivation): this is specifically the decision policy for WHEN
to revise, owned by learner-maintained counts.

Fixes multiple members: M3-W1 singleton probe (noise below threshold never triggers
the schema); M3-W2 (the second contradiction arrives against a MAP with
accumulated standing history, so the trigger consults standing rather than
depending solely on the dead provenance lookup). Both are Cluster C members on the
M3 side: the trigger was a researcher-fixed any-contradiction rule.

Capability-source delta: cognition source lines added near zero (wiring call sites
to existing dormant functions); the any-contradiction trigger path is deleted. Net
negative or zero.

Falsifiable prediction: on a sealed singleton-noise world, if the learner's
standing still triggers revision on the first contradiction (because the learner
never writes SUP edges, so standing sits at zero and any threshold is trivially
crossed), H9 is dead: the counting instruments exist but the learner does not feed
them, so evidence weighting needs a researcher-defined update rule and cannot be
learner-owned in this form.

## Continuing learner

Requirement: one persistent learner experiencing new vocabulary, concept learning,
procedure invention, conflicting evidence, active inquiry, causal learning, memory
pressure, unrelated interference, corrections, and delayed reuse, with no process
reset, no task label supplied to cognition, and no recompilation per task.

### H10. One learner-owned structural workspace

Substrate change: all subsystem state (MAPs, guides, UNCERT nodes, taught facts,
standing records) lives in a single learner-addressable workspace with one node and
edge format; subsystem boundaries become learner-created link types, not separate
stores with separate layouts and selectors. Selectors become generic graph queries
over the unified store. This is the architectural precondition for the continuing
learner: with no process reset and no task labels, there is nowhere for a subsystem
wall to be rebuilt between experiences.

Fixes multiple pressures at once: retention under memory pressure (the K-S14 12/12
result must survive lifelong running; a unified store lets one standing-based
eviction policy apply uniformly instead of per-subsystem ad hoc rules);
unrelated interference (new vocabulary learning and old procedure memory share the
store, so interference becomes observable and manageable in one place rather than
hidden across formats); cross-capability reuse (a procedure invented during a
vocabulary phase is addressable during a causal phase because no format wall
separates them); delayed reuse (old structures persist in the same space the
learner still queries).

Capability-source delta: cognition source lines added zero; the per-format
selectors and layout conventions are deleted. Net negative. No new modes, bridges,
or routers: unification removes boundaries rather than adding coordination.

Falsifiable prediction: after unification, if a sealed interference world shows
catastrophic interference (new vocabulary learning evicts or corrupts previously
learned procedures, with white-box evidence of cross-type edge collisions in the
shared store), H10 is dead: format unification does not by itself yield
non-interfering coexistence, and the continuing learner needs content-addressed
separation, not merely a shared store.

### H11. Consequence-derived lifelong standing economy

Substrate change: one generic standing rule, maintained by the learner and derived
from consequences (structures whose use leads to confirmed predictions gain
standing; structures implicated in contradictions lose it), governs retention,
eviction, inquiry priority, and revision candidacy across all capabilities for the
life of the run. The researcher writes no per-subsystem budgets, no per-task
quotas, and no separate retention policies. Structurally distinct from H10 (the
workspace format) and from H6/H9 (local standing): this is the global resource
economy of a lifelong run.

Fixes multiple lifelong pressures: delayed reuse (high-standing old structures
survive memory pressure while low-standing recent noise is evicted first);
unrelated interference (new learning enters at low standing and cannot evict
established structures until it earns standing through confirmed use); the
retention-versus-revision tradeoff (the same standing that protects a structure
from eviction also gates whether contradicting it triggers revision, unifying H6
and H9 across the run's lifetime).

Capability-source delta: cognition source lines added zero; per-subsystem ad hoc
policies (fixed bid formulas, any-contradiction triggers, special-case eviction)
are replaced by the one generic rule. Net negative. No new modes or routers: one
economy, all structures.

Falsifiable prediction: on a sealed lifelong world with memory pressure, if the
standing economy collapses into either total retention (nothing is ever evicted
and the store grows without bound) or total forgetting (recency dominates and
delayed-reuse probes fail despite high prior standing), H11 is dead: a single
scalar standing cannot simultaneously serve retention, eviction, inquiry, and
revision, and the economy needs researcher-designed multi-dimensional
bookkeeping, which would violate the zero-delta claim.

## Ranking by information gain (not optimism)

Ordered by expected reduction in architectural uncertainty: decisiveness of the
test, number of clusters discriminated, and how foundational the question is.
A negative result that kills a direction outranks a positive result that merely
confirms a narrow fix.

1. H5 (generic supersession transition). One test spans two mechanisms and all of
   Cluster B; both outcomes are decisive (works: lifecycle was purely a wiring gap;
   fails: the learner needs standing-driven retirement, pointing at H6/H11), and it
   is the cheapest decisive test available.
2. H1 (learner-named procedure objects). The central L3-adjacent question: is the
   abstraction failure about missing affordances or about the learner not using
   them? A negative result redirects the entire procedure-invention frontier.
3. H10 (one structural workspace). Foundational bet of the continuing learner; a
   negative result (interference despite unity) kills format unification as a
   direction and forces content-addressed separation research.
4. H7 (revision as re-derivation). Discriminates the revision ontology itself; a
   negative result isolates construction as the true bottleneck and stops revision
   work from proceeding independently.
5. H8 (law objects with parameter slots). Cleanest test of instance-keyed versus
   law representation; a negative result shows parameterization is not discovered
   even when expressible.
6. H11 (lifelong standing economy). Tests the global resource question for the
   continuing learner; a negative result reveals single-scalar insufficiency before
   large lifelong runs are built on it.
7. H6 (standing-bearing uncertainty). Narrower than H11; discriminates whether the
   learner can maintain evidence magnitudes at all.
8. H2 (learner-asserted derivation direction). Narrow; discriminates direction
   versus content as the binding constraint on M1-W2.
9. H4 (content-to-action projection). Narrow; discriminates whether the missing
   wire on the M2 side was content-to-action encoding.
10. H9 (standing-gated revision trigger). Narrowest decision-policy test; largely
    subsumed by H6/H11 outcomes, informative mainly if those pass and this fails.
11. H3 (procedure-as-operand unification). Furthest frontier with the lowest prior;
    presupposes H1's success, so it is tested last despite high variance.

## Cross-hypothesis notes

- H5 is load-bearing for H6, H7, H9, and H11: several hypotheses assume a working
  generic transition. If H5 fails negatively (machinery permitted but never used),
  the dependent hypotheses must be retested in their standing-driven form rather
  than assumed dead.
- H1 is load-bearing for H3 and partly for H7/H8: re-derivation and laws inherit
  whatever construction the learner owns. If H1 fails, H7's negative prediction
  (re-learning the same wrong thing) becomes the expected outcome rather than a
  surprise.
- H10 is load-bearing for H11: the standing economy needs one store to govern.
  Test H10 before committing to H11-scale lifelong runs.
- No hypothesis in this set adds a researcher-authored schema, semantic case,
  mode, bridge, router, or task-specific handler. Every capability gain is
  specified as experience creating new learner state through generic affordances,
  which is the no-patch-treadmill and ONE-SYSTEM requirement.
