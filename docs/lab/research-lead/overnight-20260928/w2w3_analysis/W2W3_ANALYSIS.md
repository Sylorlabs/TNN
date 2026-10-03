# W2/W3 Shared-Cause Analysis

Date: 2026-09-30. Analyst: W2/W3 shared-cause analyst.
Scope: ANALYSIS ONLY. No implementation is proposed. The cause is identified; code is not.

## Verdict

**W2 and W3 share one architectural cause.** Both fail because the frozen core's
query path is exact-key associative lookup over stored (subject, relation, object)
triples, with no step that constructs a general mapping from stored exemplars and
applies it to unobserved keys. W2 needs invariance-abstraction (a procedure);
W3 needs function-construction-and-evaluation (a causal law). These are two
computational faces of one architectural gap: **the core cannot construct
learner-owned executable/functional structures from regularities in its stored
experience, persist them, and apply them at query time.**

## Evidence base (K1)

- World files (sealed, hashes verified MATCH in the run):
  - `core_freeze/worlds_prefreeze/W2_world.txt` (23 lines; seal
    33958a4d0e01e7f9d02a9f1d5744247a0c7bdc82754a055191695f23699d7635)
  - `core_freeze/worlds_prefreeze/W3_world.txt` (54 lines; seal
    01b4ee0d8095a073eb50113934b6ee377504c03d013280b470163ca73be9a662)
- Design predictions and mechanism-level reasons:
  `core_freeze/worlds_prefreeze/DESIGN_WORLDS_PREFREEZE.md`
  (W2 predicted FAIL 0/8: "no procedure abstraction or execution machinery;
  novel-instance keys never observed"; W3 predicted FAIL 0/10: "no hypothesis
  construction machinery behind the generic interface; held-out sums unobserved").
- Run outcomes: `core_freeze/run_phase/RUN_RESULTS.md` per-world table
  (W2: observed 0/8 all -2, WORLD-FAIL, CONFIRMS; W3: observed 0/10 all -2,
  WORLD-FAIL, CONFIRMS).
- Raw battery outputs:
  - `core_freeze/run_phase/battery/W2.out`: all 8 probes
    `ANSWER 8004 801 -2` through `ANSWER 8005 804 -2`.
  - `core_freeze/run_phase/battery/W3.out`: all 10 probes
    `ANSWER 9011 600 -2` through `ANSWER 9020 600 -2`.
- Interface contract: `core_freeze/stage0/INTERFACE.md` (OBSERVE routes 1:1 into
  the existing `learn()` driver; QUERY routes 1:1 into the existing `query()`
  driver, returning the stored object for an exact (subject, relation) key or
  the -2 not-found sentinel; no semantic cases, no modes, no handlers).

## What each world asked, and what happened

### W2: new procedures

Input: 15 OBSERVE events. Three demonstrations of one 4-step procedure.
Instances 8001, 8002, 8003 each observe (instance, 801..804, op 9501..9504)
and (instance, 805, 9505). The ordered operation sequence is identical across
the three instances.

Probes: 8 QUERY events on two novel instances, 8004 and 8005, asking for each
step 801..804 with the demonstration ops as expected values.

Result: 0/8, every probe -2. The construction half passed (the 15 demonstration
slots were created in the fact store); the execution half failed completely.

What answering required: recognizing that the step-to-op mapping (801->9501,
802->9502, 803->9503, 804->9504) is INVARIANT across the instance dimension,
reifying that invariant as an executable structure, binding a novel instance,
and emitting the mapped op per step. The core stored 15 triples and performed
8 exact-key lookups on keys that were never observed.

### W3: causal laws

Input: 24 OBSERVE events. Eight interventions, each three triples for one pair
subject 9001..9008: (pair, 601, x), (pair, 602, y), (pair, 600, x+y). The law
is integer addition, outside the frozen DDES case families.

Probes: 10 held-out trials on fresh pair subjects 9011..9020. Each trial
presents the two inputs as OBSERVE events and asks QUERY (pair, 600, x+y).

Result: 0/10, every probe -2. The intervention triples were stored; no
hypothesis was constructed.

What answering required: constructing the function f(x, y) = x + y from the
eight exemplars, persisting it as a learner-owned structure, and evaluating it
on each novel pair's inputs at query time. The core stored 24 triples and
performed 10 exact-key lookups on sum keys that were never observed.

### Neither failure is eviction-confounded

Both worlds' probes hit never-observed keys, so the -2 answers are
deterministic consequences of the lookup-only query path, not of the
eviction tie-breaker pathology (C75). The raw outputs do show teach-side
churn (each OBSERVE evicting the prior slot under the lowest-index tie-break),
but even with perfect storage the probes would return -2: no stored triple
could answer them. The design predicted exactly this, and the run confirmed it.

## What W1 has that W2/W3 lack

W1 (new concepts) PASSED 10/12 with retention 10/10. Its 10 passing probes were
exact-key recalls of taught (subject, relation) pairs: storage plus lookup,
which is everything the frozen core implements. Its 2 failing probes were the
two-hop composition probes (QUERY 7005 599 21, QUERY 7010 599 22), which
returned -2 as predicted: the composed keys were never observed and the core
has no chaining machinery.

So W1 does not possess a capability W2/W3 lack. W1's pass is a pass on
STORAGE + LOOKUP, and W1's own internal failure (the 2 composition probes)
documents the same boundary that W2 and W3 hit in full: **anything requiring
more than exact-key recall fails.** W1 is the mildest member of the
construct-and-apply cluster, not a counterexample to the shared cause.

## The shared cause, stated precisely

The frozen core implements one retrieval operation: exact-key lookup of a
stored (subject, relation, object) triple. It lacks all three of the following,
and W2/W3 each require all three:

1. **Regularity detection.** Nothing in the learn() path scans stored triples
   for regularities across exemplars (invariance across instances in W2;
   a functional input-output relation in W3).
2. **Reification.** There is no persistent format for a learner-owned
   function/procedure object. The 36-slot fact store holds triples; no region
   or encoding represents "mapping M from inputs to outputs" as a
   first-class persistent structure. With nothing to construct, there is
   nothing for learning to update.
3. **Application at query time.** query() is lookup-only. On a miss it
   returns -2; it never attempts to derive the answer from stored
   regularities. With nothing applicable, there is nothing for inference
   to invoke.

The root is representational (2): because no function/procedure format exists
in persistent learner state, detection (1) has no target to write to and
application (3) has no object to invoke. The three gaps are one gap seen from
the learning, storage, and inference sides.

## Same cause or two causes?

At the architectural level: ONE cause (no construct-and-apply substrate).
At the computational level: the regularities differ in kind, and this
difference is load-bearing for Micah's directive.

- W2's regularity is INVARIANCE: the step->op mapping is constant across the
  instance dimension. Fixing W2 alone requires abstracting over a varying
  dimension and instantiating to a novel value of that dimension.
- W3's regularity is COMPUTATION: the output is a function (addition) of two
  other stored values. Fixing W3 alone requires evaluating an induced
  function on novel inputs.

A W2-only repair (for example, "on lookup miss, return the object stored for
the same relation under a different subject when the mapping is constant")
would leave W3 at 0/10. A W3-only repair (for example, "on lookup miss, try
arithmetic combinations of co-stored values") would leave W2 at 0/8. Either
single-world repair is exactly the kind of patch Micah's directive says to
reject: it fixes one freeze-challenge world without revealing a general
mechanism. The general mechanism must be a substrate for constructing and
applying learner-owned functions/procedures, of which W2's procedure and W3's
law are both instances.

## Falsifiability (K2)

The shared-cause claim is: "W2 and W3 fail for the same architectural reason:
the query path cannot apply any learner-constructed mapping to unobserved
keys; the construction half (storing exemplars) works in both worlds."

This claim is REFUTED if any of the following is shown:

(a) A repair achieves 7/8 or better on W2's probes while W3 remains 0/10
    (or 9/10 or better on W3 while W2 remains 0/8) through a change that is
    NOT a general construct-and-apply substrate. Separable fixes prove
    separable causes at the mechanism level.
(b) The probe keys turn out to have been observed after all (for example, a
    world-file or harness bug placing probe answers in the teach stream),
    which would reclassify the failure as a storage/eviction bug rather than
    a construction gap. The battery outputs rule this out today: all 18
    probes returned -2 and none of the probe keys (8004/8005 steps;
    9011..9020 relation 600) appear as OBSERVE targets.
(c) The frozen core is shown to construct and apply a mapping on some other
    sealed world while still failing W2/W3, which would show the gap is
    narrower than "no construct-and-apply" (for instance, limited to
    particular regularity kinds).

## Missing mechanism(s), in architectural terms

No code is proposed. The missing capability, stated as architecture:

- A persistent, learner-owned representation for functions/procedures:
  first-class objects in declared persistent state (not triples, not
  source-side cases), created after experience, with a white-box trace of
  their construction.
- A learn()-path step that detects regularities across stored exemplars and
  reifies them into such objects.
- A query()-path step that, on lookup miss, attempts to apply applicable
  reified mappings before returning -2.

Under the One-System Rule this must arrive as EXPERIENCE -> NEW LEARNED
STATE/STRUCTURE, with capability-source delta approaching zero: no new Zag
subsystem, no PROCEDURE_MODE, no per-family handler. The standing question
applies: "Why can the existing general architecture not learn this
behavior?" The answer this analysis gives is: because the existing
architecture has no persistent format for a constructed mapping and no
query-time application step, so there is nowhere for such learning to live
and nothing to invoke it.

## L3B/L3C integration assessment

None of the surviving mechanisms plug into the frozen core under the
One-System Rule. Each is a separate subsystem with its own interface, and
bridging any of them to the core's generic OBSERVE/QUERY path would add
exactly the kind of mode/bridge/handler the rule forbids.

- **L3B v2 (C64, C68): procedure invention.** Status: SURVIVES as bounded L2.
  The independent adversary confirmed it is a finite 205-program menu with a
  fixed archive. It operates on string examples through its own driver, not
  on the fact store's integer triples. It cannot supply W2's missing
  procedure: W2 needs incremental construction from the core's own stored
  triples, applied through the core's query path. The lane ruling already
  mandates redesign toward incremental construction, never menu expansion;
  that redesign is the direction, not a plug-in of the current menu.
- **L3C v3 (C66, C73): cover-set composition.** Status: SURVIVES as bounded
  L2. The mechanism is a general learning operation (not disjunction
  specific) with an EMPTY interpreter diff, which is the right shape
  architecturally. But it operates on the L3C interpreter's
  feature/predicate representation, not on the frozen core's fact store,
  and it constructs dispatch structures for classification, not
  functions/procedures for query-time application. Same integration
  barrier: reaching the core's triples and query path requires a bridge.
- **Causal edit-invent (C65, narrowed by C71).** Status: SURVIVES as bounded
  L2+, delay-specific. The adversary proved the diagnose-and-relax
  generality claim was scope collapse: the mechanism is provably
  delay-specific, not parameter-generic. It is not a candidate for W3's
  addition law, which needs general function induction, not envelope
  repair in one family.

Assessment: the missing piece is not any one of these mechanisms. It is a
general substrate for learner-constructed functions that lives in the core's
own persistent state and is driven through the existing learn()/query()
path. L3C v3's cover-set composition is the closest in spirit (a general
operation, no new semantic cases), but generality of operation is not the
same as integration into the core's state and query path.

## Clustering with the other worlds

- **W2/W3: the clean cluster.** Both are clean FAILs (no eviction confound),
  both are construct-and-apply gaps, both confirmed as predicted. This is
  the cluster this analysis covers.
- **W7 (planning): adjacent but distinct.** Shares the "no constructed
  structure applied at decision time" shape, but additionally lacks
  action-selection machinery entirely (ACT emits the fixed placeholder
  CHOICE 0 per INTERFACE.md). A construct-and-apply substrate would not fix
  W7 without learner-driven action selection also arriving.
- **W8 (synthetic language): adjacent but distinct.** Shares the induction
  gap (grammar induction from exemplars is a construct-and-apply problem),
  but needs compositional symbol-system induction specifically. A general
  function substrate plausibly covers it; the analysis does not claim it.
- **W4/W5: separate cluster.** Dominated by the eviction tie-breaker
  pathology (C75), not by a construction gap. Different cause, different
  repair class (state management, and per Micah's directive, not a
  cache-policy treadmill).
- **W1 composition probes: mildest member of the W2/W3 cluster.** The 2
  predicted -2s are chaining failures, the same family at lower severity.
- **W6/W9: confounded.** C1-confounded by eviction per the pre-registered
  clause; not clean measures of their target capabilities.

## Bottom line

W2 and W3 are not two problems. They are one problem seen twice: a core that
can store experience as triples and recall it by exact key, but cannot turn
regularities in that experience into persistent, applicable mappings. W2's
procedure (invariance across instances) and W3's law (computation over
inputs) are both instances of the missing construct-and-apply substrate.
Any repair that fixes only one of them is, by Micah's stated rule, to be
rejected unless it reveals the general mechanism. The surviving L3B, L3C,
and causal-edit mechanisms do not supply it and cannot be bridged in without
violating the One-System Rule; the substrate has to be built into the core's
own persistent state and query path, driven by experience rather than by new
source machinery.
