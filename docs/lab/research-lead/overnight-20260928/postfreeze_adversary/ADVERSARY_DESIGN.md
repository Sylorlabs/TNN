# Post-Freeze Adversary Design: Generality Worlds GW1-GW8

Status: DESIGN + SEALED ASSETS. Approved by: Micah's 2026-09-30 overnight
directive (post-freeze adversarial battery). This document is the design
record. The sealed world files live in `worlds/`. Exact id triples and
expected values are in the sealed files only, not in this document.

Date: 2026-10-01. Adversary: POST-FREEZE Adversary (independent of the
TNN-2 builder and of the FW1-FW9 evaluator).

## 0. Stance and ground rules

TNN-2 was built AFTER seeing the FW1-FW9 failures, so FW1-FW9 now measure
regression, not generality. These eight worlds (GW1-GW8) are the important
generality test. They were designed from the PUBLIC architecture claim only
(TNN2_BUILD_REPORT.md at f4de7ff46: the three mechanisms A, B, C below).
The adversary did not read hidden builder fixtures, builder test files, or
sealed FW world contents.

TNN-2's three claimed mechanisms (public claim):

- (A) Runtime executable-graph construction: `t2_trial`, a propose /
  execute / verify / promote trial loop over the frozen 4-op ISA
  (MOVE / BRANCHEQ / INC / DEC). Gather is BFS depth 1-4 from the miss
  subject (skipping relation -999), direct values for sums, per-relation
  chains for counts. Assembly builds GUARD (BRANCHEQ), SETREG (MOVE),
  unrolled INC cells for sums, GUARD+SET+INC links plus a MOVE epilogue
  for counts. Search order: chains k=2..4, then sums, then counts, then
  single hops. Promotion writes a MAP node plus provenance edges plus
  the taught answer fact. Genuine rejections are counted.
- (B) Learner-originated uncertainty to action: `miss_inquire` on a true
  miss (after trial and P-INV bootstrap fail) reifies an UNCERTAINTY node
  (type 30) and a POLICY_ROOT-linked guide (type 1, choice 30); `ev_act`
  then returns 30 instead of the 0 fallback. No new modes.
- (C) Counterexample-driven executable-graph revision:
  `revise_on_contradict` on the contradiction branch finds MAPs with DEP
  edges to the contradicted fact, locates the stale SETREG step via its
  provenance edge, tombstones it (tag 0), inserts a corrected step,
  rewires the GUARD's field12 and SEQ edges, re-executes to verify, and
  reverts on verification failure. MAP standing is untouched.

Global constraints on all eight worlds:

- Event streams use integer ids only. No natural language, no task labels.
- GW id range is [40000, 49999], disjoint from FW [30000, 39999] and W
  ranges. Each GW world owns a disjoint 100-id sub-block (GWn owns
  [40000+100*(n-1), 40099+100*(n-1)]). Answer values are small integers
  outside the GW id range.
- Line format follows the frozen public protocol: `OBSERVE s r o`,
  `QUERY s r expected`, `ACT`. Grading compares emitted ANSWER values to
  the QUERY expected field, and CHOICE values on ACT lines.
- No world requires a new opcode. Every world is solvable in principle
  with the frozen 4-op ISA; the question is whether TNN-2's three
  mechanisms generalize to these shapes, not whether the ISA can express
  them.
- Each world runs with FRESH learner state (recommended), so worlds are
  independent. GW5 is multi-phase with a responder contract (see below).
- Nothing here is a surface variant of an FW world: see the
  material-difference argument per world.

How to read predictions: these worlds are ADVERSARIAL. Several are
predicted to fail. A predicted fail that fails as predicted confirms the
identified boundary. A predicted fail that PASSES is strong generality
evidence and must be investigated (mechanism attribution goes to the red
teams, not to these black-box worlds).

## GW1: composition depth beyond the demonstrated ceiling (attacks A)

Mechanism attacked: (A) runtime construction, specifically the depth
generality of the gather/assemble loop. The builder demonstrated a 4-hop
chain (T2-CHAIN4); the gather is BFS depth 1-4 and the search order covers
chains k=2..4.

World shape: a 4-hop control chain (fresh ids) probed via a composed
relation, then two independent 5-hop chains (fresh ids, disjoint subjects)
probed via the same composed relation. The 5-hop answers sit at depth 5
from the query subject: one hop beyond the gather ceiling.

Pass criterion (frozen bar): control probe correct (1/1; validates the
world) AND both 5-hop probes correct (2/2) for WORLD-PASS.

Material difference: FW1 used 3-hop chains; the builder fixture used 4-hop.
Five hops is exactly one step beyond the demonstrated ceiling, so the world
discriminates "open-ended construction" from "ceiling at 4". It is not a
longer FW1: FW1 tested compositional recall under pressure, GW1 tests the
constructor's depth bound in isolation.

Prediction: control PASSES; both 5-hop probes FAIL (miss sentinel, since
no depth-5 path is gathered and no other shape yields the answer). A pass
on the 5-hop probes would be strong evidence that construction depth is
not researcher-capped.

What it establishes: FAIL confirms the depth-4 bound is architectural, not
incidental, and that (A) does not generalize in depth. PASS would show the
gather loop is genuinely open in depth.

## GW2: a cyclic executable structure (attacks A)

Mechanism attacked: (A) runtime construction, specifically the topology
family. The claimed repertoire is chains, sums (unrolled INC), and counts:
all directed acyclic shapes. Nothing in the claim builds a back-edge.

World shape: two independent probes. Each teaches a seed value and an
iteration count on a fresh subject, then queries a result relation whose
correct answer is the seed doubled iteration-count times (exponential by
repeated doubling). The answer is a computed value, not a retrieved fact:
it is not the object of any single taught triple, not a chain endpoint,
not a sum, not a count. Building it requires a loop (counter plus
double step with a back-edge), or unrolling that first computes the
unroll count by exponentiation (which the constructor cannot do, since the
count fact carries the exponent, not the unrolled total).

Pass criterion: 2/2 probes correct for WORLD-PASS.

Material difference: not isomorphic to multiplication tables or to any FW
arithmetic. FW3 tested arithmetic/composition over taught products; GW2
tests whether the constructor can build a CYCLIC graph for iterative
computation, a shape absent from the builder fixtures (which used DAG
chains and unrolled sums). The useful abstraction (iteration to a fixed
point/count) was not anticipated by the arithmetic examples.

Prediction: FAIL (both probes miss). The constructor has no loop shape;
sums/counts/single-hops cannot verify to the expected values.

What it establishes: FAIL shows (A) is a DAG-family constructor (a larger
finite family: chains/sums/counts), not an open graph constructor. PASS
would be major generality evidence for (A) and would demand immediate
white-box attribution by the construction red team.

## GW3: hierarchical reuse plus revision propagation (attacks A and C)

Mechanisms attacked: (A) construction over learner-created structure, and
(C) revision through multi-level provenance. This is the MUL-from-ADD
pattern used as a probe of the general mechanism, per the directive
(MUL is evidence, not the destination): a structure built in phase 2 must
traverse a relation whose answers were taught by a phase-1 promoted graph,
and a phase-3 contradiction must propagate through the dependency levels.

World shape, four phases, one world file:

1. Teach a 2-hop chain on fresh ids; probe its composed relation (call it
   the level-1 relation). The learner promotes a graph and teaches the
   answer fact.
2. Teach a further chain whose FIRST hop traverses the level-1 answer
   fact (the level-1 value used as a subject), then probe the level-2
   composed relation. This requires the constructor to treat its own
   taught answer facts as first-class traversable edges: cross-level
   reuse of learned structure.
3. Contradict the level-1 chain's terminal value fact (the demonstrated
   value-revision pattern). Probe the level-1 relation: this is a
   regression check on the demonstrated (C) capability.
4. Probe an independent control chain (must be unaffected) and probe the
   level-2 relation. The level-2 chain is now broken (its first hop's
   object changed and no replacement link was taught), so the correct
   answer is the miss sentinel: the dependent structure must be retired,
   not left stale.

Pass criterion: phase-3 probe correct AND control probe correct AND
phase-4 level-2 probe returns the miss sentinel (3/3) for WORLD-PASS.

Material difference: no FW world tested construction over
learner-taught composed relations, and none tested whether revision
propagates past one level. FW5 tested a long chain under memory pressure,
not revision propagation. The builder's revision test was single-level
value replacement.

Prediction: phase-3 probe PASSES (demonstrated pattern); phase-4 probe
FAILS (stale level-2 answer retained), documenting that (C) does not
propagate through dependent structures. If phase 4 passes, it shows the
DEP-edge provenance design genuinely supports multi-level revision.

What it establishes: FAIL isolates a real boundary: revision is
single-level while construction is multi-level, so learned hierarchies
rot from the top down. PASS would show the provenance design is
compositional.

## GW4: guard retarget instead of value replacement (attacks C)

Mechanism attacked: (C) revision, specifically the topology of the repair.
The demonstrated repair (builder test) is value replacement: tombstone the
stale SETREG step and insert a corrected value step. The claim ALSO says
the operator rewires the GUARD's field12 (branch retarget), but no
demonstrated test exercises a repair where the guard is wrong and the
value is right.

World shape: teach a 2-hop chain; probe the composed relation (promotes a
graph whose guard tests the first hop and whose SETREG carries the value).
Then teach the same value reachable from a NEW middle node, and
contradict the chain's first-hop fact (replacing the middle node). The
value is unchanged; the guard's expected middle is stale. The correct
repair retargets the guard to the new middle node (topology change); there
is no corrected VALUE for a value-patcher to insert, because the
contradiction carries a subject id, not a value.

Pass criterion: final probe returns the (unchanged) value, 1/1, with the
pre-contradiction probe correct as validity.

Material difference: the builder's revision test contradicted a VALUE
fact (corrected value available in the contradiction). GW4 contradicts a
LICENSING fact (no corrected value available), forcing a topological
repair. It is the complement of the demonstrated case.

Prediction: UNCERTAIN. Distinctive outcomes: the unchanged value means a
genuine topological repair (or a successful rebuild) occurred; the
contradicting subject id as the answer means a naive value-patcher
inserted the wrong kind of literal; the sentinel or the stale value means
no repair. Mechanism attribution (revision vs re-trial) is left to the
revision red team; this world establishes the behavioral boundary.

What it establishes: PASS shows (C) is a graph rewriter, not a
value-patcher. The subject-id answer would show the operator inserts
literals without kind discipline. Stale/sentinel shows (C) only handles
the demonstrated value case.

## GW5: inquiry-gated construction, two stages (attacks B; responder)

Mechanism attacked: (B) learner-originated inquiry, specifically whether
inquiry is NECESSARY and SUFFICIENT to unlock a construction the learner
could not otherwise build, and whether inquiry re-fires after partial
progress. This is the full B-to-A loop: miss, uncertainty, act, world
answers, construct.

World shape (responder contract, after the FW6 pattern):

- Phase A (static file): teach a 2-hop chain; probe the composed relation
  (promotes a graph); contradict the chain's first-hop fact (the chain is
  dead and the replacement link is untaught); probe the composed relation
  (diagnostic: miss expected on the inquiry path); ACT (the test act).
- Responder: releases phase B1 iff the phase-A transcript contains a line
  exactly `CHOICE 30` (a genuine learner-chosen inquiry act); otherwise
  releases phase B2 (control).
- Phase B1: teaches the missing replacement link (the fact the inquiry
  asked for, in effect). Phase B2: teaches an unrelated junk fact.
- Phase C (static file): probes the composed relation. Only a learner
  that inquired (treatment arm) can construct the answer; the control arm
  cannot.

Pass criterion: treatment arm phase-C probe correct for WORLD-PASS. The
control arm is reported separately (expected to fail; it is the baseline
showing the reveal was necessary).

Material difference: FW6 tested diagnostic inquiry (ask, then combine two
revealed calibrations). GW5 tests CONSTRUCTION-ENABLING inquiry: the
revealed fact is a missing structural link, and the payoff is a newly
buildable executable graph. The builder's inquiry test was single-shot;
GW5's responder releases only on the inquiry act, making inquiry load
bearing rather than decorative.

Prediction: treatment PASSES if (B) fires on the post-contradiction miss
and the trial loop rebuilds from the revealed link. If (B) does not fire
(e.g. a stale graph answers instead of missing), the world takes the
control arm, which documents that failure mode.

What it establishes: PASS shows the miss to uncertainty to guide to act
to evidence to construction chain works end to end under adversarial
conditions (post-contradiction, not just a fresh miss). Control-arm
execution shows what happens without inquiry.

## GW6: inquiry discrimination and retirement (attacks B)

Mechanism attacked: (B), specifically whether inquiry tracks CURRENT
learner state: it must fire on new ignorance, must NOT fire spuriously,
and must retire when the ignorance is resolved. The builder demonstrated
single firing (returns 30 after a public miss). Nothing demonstrates
retirement or re-firing.

World shape (one file, eleven lines): teach a 2-hop chain and probe it
(construction sanity); ACT (expect 0: no uncertainty yet, no spurious
inquiry); probe a never-observed key (expect miss sentinel); ACT (expect
30: inquiry fires on true miss); teach the missing fact; probe it
(expect the value: learning worked); ACT (expect 0: uncertainty resolved;
PREDICTED FAIL, stale 30); probe a second never-observed key (expect
miss); ACT (expect 30: re-fire on new ignorance).

Pass criterion (primary, frozen): the seven probes excluding the
retirement probe must all be correct (7/7) for WORLD-PASS. The retirement
probe is a SECONDARY boundary probe, reported separately, not part of the
pass bar.

Material difference: the builder's act test was fire-once. GW6 is a
state-tracking battery: fire, resolve, retire, re-fire. The stale guide
is the locally attractive wrong question: after resolution, re-asking
(30) is the easy default, and the world checks whether the learner
resists it.

Prediction: primary 7/7 PASSES; the retirement probe FAILS (returns the
stale 30), documenting that (B) has no uncertainty-retirement mechanism:
inquiry is append-only. That is a precise, honest boundary, not a vague
failure.

What it establishes: PASS on primary shows inquiry discriminates miss
from non-miss and re-fires. The secondary documents the staleness gap the
next architecture must close (guides need a lifecycle).

## GW7: interference between construction, revision, and action (attacks A, B, C)

Mechanisms attacked: all three, interleaved. Each mechanism was
demonstrated in isolation; nothing shows they do not corrupt each
other's state when a construction, an inquiry, and a revision happen in
rapid succession.

World shape (one file, seventeen lines): construct a graph (probe correct);
miss on a fresh key and inquire (ACT 30); teach and probe the inquired
fact; contradict the constructed graph's value fact and probe the
revision; construct a SECOND graph after the revision (probe correct);
miss on another fresh key and inquire again (ACT 30: inquiry still works
post-revision); final probes on all three learned items.

Pass criterion: all eleven probes correct (11/11) for WORLD-PASS.

Material difference: no FW world interleaved all three mechanisms. FW
worlds tested one capability each. GW7 is an integration stress: revision
must not break the inquiry guides, inquiry must not disturb promoted
graphs, second construction must not reuse first-construction state
incorrectly.

Prediction: PASS (the mechanisms look decoupled in the claim). Any
failure pinpoints a concrete interaction bug and is high-value.

What it establishes: PASS shows the three mechanisms compose without
interference: a prerequisite for one continuing learner. FAIL localizes
the interaction (which final probe broke tells which mechanism was
corrupted).

## GW8: revision lifecycle: successive revisions and revert (attacks C)

Mechanism attacked: (C), specifically whether the revision operator is a
general graph rewriter or a one-shot patcher. The builder demonstrated ONE
revision (value 201 to 999). Nothing demonstrates revising an
already-revised graph, or reverting to an earlier regime.

World shape (one file, nine lines): teach a 2-hop chain; probe the
composed relation (100). Contradict the terminal value fact three times
in succession: to 200 (revision 1), to 300 (revision 2: must locate the
CURRENT step, not the original), then back to 100 (revision 3: revert to
the original regime; the corrected literal equals a tombstoned earlier
value). Probe after each contradiction.

Pass criterion: all four probes correct (4/4) for WORLD-PASS.

Material difference: the builder's revision test was a single
contradiction. GW8 is a lifecycle: revise, revise-again, revert. The
revert is the adversarial core: many patchers assume monotonic
correction and mishandle "the right answer is the one we tombstoned."

Prediction: UNCERTAIN. Revision 1 should pass (demonstrated pattern).
Revision 2 tests whether the operator tracks current vs original steps.
The revert tests tombstone discipline. Partial credit (e.g. 3/4) is
informative about which lifecycle stage breaks.

What it establishes: 4/4 shows (C) is a genuine revision operator over
graph state, not a one-shot patch. Failure at revision 2 shows the
operator cannot find current steps; failure at the revert shows it cannot
re-admit tombstoned values. Either is a precise characterization of the
operator's actual semantics.

## Coverage of the required adversarial pressure

- Unfamiliar executable structures not isomorphic to multiplication: GW2
  (cyclic doubling graph).
- Composition depth/shape absent from builder tests: GW1 (depth 5).
- Revision with a different topological repair than the demonstrated MAP
  repair: GW4 (guard retarget vs value replacement).
- Multiple successive revisions including revert: GW8.
- Ambiguity where several repairs fit current evidence: GW5 (the
  contradiction alone underdetermines the repair; the learner must
  inquire) and GW4 (no corrected value in the contradiction).
- Action selection where the informative action changes with learner
  state: GW6 (ACT 0 vs 30 as uncertainty appears, resolves, reappears).
- Inquiry where the wrong question is locally attractive: GW6 (the stale
  guide invites re-asking a resolved question).
- Cross-domain reuse of a learned executable structure: GW3 (level-2
  construction traverses level-1 taught answer facts).
- Interference and memory pressure between construction, revision, and
  action: GW7 (all three interleaved; memory pressure is light by design
  to isolate interaction from eviction).
- A domain whose useful abstraction was not anticipated by arithmetic
  examples: GW2 (iterative computation as a loop abstraction).

## What a pass or fail means in general

These worlds do not establish broad generality or L3 even at 8/8: they
are a targeted battery against three specific mechanisms. Per the
directive, a pass here is regression-grade evidence for the mechanism
under attack, and the fresh post-freeze battery is the important
generality test only in the sense that it is INDEPENDENT of the
builder's fixtures. Failures cluster by mechanism: GW1/GW2 implicate (A),
GW4/GW8 implicate (C), GW5/GW6 implicate (B), GW3/GW7 implicate
integration. A repair that fixes one world without moving its cluster
mates is suspect under the no-patch-treadmill rule.

## Sealed assets

- `worlds/gw1_world.txt` (17 lines)
- `worlds/gw2_world.txt` (6 lines)
- `worlds/gw3_world.txt` (10 lines)
- `worlds/gw4_world.txt` (6 lines)
- `worlds/gw5_phaseA.txt` (6 lines), `worlds/gw5_phaseB1.txt` (1 line),
  `worlds/gw5_phaseB2.txt` (1 line), `worlds/gw5_phaseC.txt` (1 line)
- `worlds/gw6_world.txt` (11 lines)
- `worlds/gw7_world.txt` (17 lines)
- `worlds/gw8_world.txt` (9 lines)
- `seal_src/gw5_respond.zag` (responder logic, sealed)
- `seal_src/gen_gw.zag` (generator; all computed values, including the
  GW2 doubling products, are computed in-generator, never transcribed)

Line counts are verified in SEAL_GW.md. SHA-256 per file in SEAL_GW.md.
