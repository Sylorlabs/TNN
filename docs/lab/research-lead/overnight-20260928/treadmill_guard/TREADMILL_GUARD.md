# Treadmill Guard: Detecting the Treadmill in TNN-3 Development

**Status: DRAFT guard spec, not a kill bar.** This is a development
discipline document. It governs nothing until referenced by a frozen
TNN-3 preregistration. It exists so that TNN-3 does not repeat the
TNN-2 failure mode: targeted repairs that satisfy capability names
while leaving the required property untouched.

**Basis:** floor spec `f383dd11c`, SUF property definition `64eec921f`,
re-clustering draft `ed2357141`, GW evaluation `881fbb3d4`, GW
interpretation `42fa993ab`, bar inventory `1722884ad`.

---

## 1. Definition: what the treadmill is

The treadmill is the development pattern in which each failure of the
frozen core is met by adding researcher-authored machinery (new
operators, wider menus, more templates, benchmark-specific handlers)
that raises the score on the failing world without changing the
property that caused the failure. The score goes up. The envelope is
unchanged in kind.

The canonical instance is TNN-2 itself. TNN-1 froze at 4/9. The gap
analysis identified three missing capabilities (construction,
inquiry, revision) and TNN-2 implemented them. The reconciled result
was byte-identical pass/fail at the world level: zero clusters moved,
zero regressions (`ed2357141`). The prereg's causal account ("TNN-1
fails for lack of X; TNN-2 adds X") was falsified for all three X.

Why it happened, per the zero-improvement analysis: the diagnosis was
pitched at the wrong level. "Add construction to fix FW3" is
underdetermined, because template instantiation is a kind of
construction and it does not fix FW3. FW3 needed a specific property
of construction (history-parameterized generativity), not construction
in the abstract. The implemented mechanisms satisfied the capability
names while violating the required property. Zero movement with zero
regressions is the signature of orthogonality, not incompleteness:
the changes operated at a causal level that did not intersect the
bottlenecks at all.

The treadmill rule, as Micah stated it: reject repairs that only fix
one freeze-challenge world unless they reveal a general mechanism.
This guard operationalizes that rule for TNN-3.

Two related failure modes count as treadmill even when scores are
flat:

- **Scaffolding inflation.** The floor tests still pass, but only
  with more researcher help than TNN-2 needed (extra teaching,
  manual state resets, relaxed determinism). The floor spec's
  anti-gaming clause (`f383dd11c` criterion 4) calls this a
  regression in learner autonomy even when scores match.
- **Failure-mode preservation.** A known failure is relabeled as a
  feature: the FW6 constant act is presented as "inquiry," masked
  acceptance-without-verification is presented as "verification,"
  the floor is presented as the ceiling. The floor spec section 3
  lists the excluded items explicitly so they are not preserved.

---

## 2. Warning signs

Any one of these in a proposed TNN-3 change is a treadmill warning.
Two or more is a strong presumption of treadmill.

1. **The menu grows.** More templates, more operators, more fixed
   families are added to source to cover observed failures. The
   MUL comparator's objection applies at the operator level:
   "the ways of combining remain fixed." A larger finite menu is
   still a finite menu.
2. **Capability names satisfied, property absent.** The change is
   described as "construction" but is template instantiation; as
   "inquiry" but is a constant act; as "revision" but is a literal
   patch. Check the name against the SUF sub-property for the
   target cluster (section 5 of `64eec921f`), not against the
   English word.
3. **World-specific fixes.** The change fixes exactly one
   freeze or GW world and nothing else, and no general mechanism
   is named. Per the no-patch-treadmill rule, prefer changes that
   fix multiple worlds at once.
4. **Scaffolding inflation.** Floor tests pass only with added
   researcher help. Compare the harness against what TNN-2 needed.
5. **H1 widening before H2.** The construction menu is expanded
   while the oracle still supplies answers through verification.
   The TNN-3 roadmap (`67a420cca`, via the prereg structure
   `206499c03`) orders H2 probes before H1 widening for exactly
   this reason: a larger menu under the same oracle is the
   treadmill's favorite move.
6. **Preserved failure modes.** A documented failure (FW6 constant
   act, masked acceptance-without-verification, one-shot revision)
   appears in the new design unchanged but renamed.
7. **Source-enumerable outputs.** The SUF operational test on the
   new mechanism returns an empty list: every producible form is
   listable from source alone. This is treadmill by definition,
   regardless of score movement.
8. **Score up, property flat.** The freeze score improves but the
   SUF test still fails and no bar from the kill-bar set
   (`1722884ad`) is newly passed. The score moved inside the
   enumerated envelope.

---

## 3. The guard: five checks

Run these on every proposed TNN-3 change before it is adopted.
A change that fails check 1 or check 2 is rejected. A change that
fails check 3, 4, or 5 is returned for redesign with the failure
named.

**Check 1: SUF check (primary).** Run the SUF operational test
(`64eec921f` section 5) on the new or changed mechanism: list every
structural decision the learner can make that the source cannot
(topology, wiring, operator arrangement, ordering, bounds,
acceptance criteria that select among forms). If the list is empty,
the mechanism cannot move any cluster, and the change is treadmill
by definition. No score movement overrides this.

**Check 2: anti-gaming check.** Run the seven floor tests
(`f383dd11c` section 4) with no more researcher scaffolding than
TNN-2 needed: same teaching sequences, no manual state resets
between probes, same determinism requirement (three runs,
byte-identical transcripts). If any test needs a crutch TNN-2 did
not need, that is a regression in learner autonomy per floor spec
criterion 4, even if the score matches.

**Check 3: generality check.** Name every freeze/GW world the change
is expected to move, and name the shared architectural cause it
addresses (per the re-clustering `ed2357141` cause clusters R1/R2/R3
plus the C0-D shadow). A change expected to move exactly one world
must name the general mechanism it reveals; otherwise it is a
one-world patch and is rejected.

**Check 4: property check.** State the property the change adds, not
just the capability. Map it to the target cluster's SUF
sub-property: FW3 history-parameterized generativity, FW6
epistemic-state-contingent discrimination with a resolution
transition, FW7 goal-conditioned composition, FW8 combinatorial
novelty, FW9 learner-scaled search (`64eec921f` section 4). If the
preregistration names only a capability ("add construction"), it is
underdetermined and treadmill-risky; it must name the property.

**Check 5: menu check.** Count researcher-enumerated schema
families (templates, operators, fixed wirings, literal bounds) in
the affected mechanism before and after the change. A real advance
moves schema decisions into learner state; it does not increase
the menu. A menu increase with no corresponding SUF gain is the
treadmill's signature move.

---

## 4. Per-capability treadmill analysis

For each of the seven floor capabilities (`f383dd11c`), what the
treadmill looks like and how the guard catches it.

### F1. Associative recall (FW1, FW2)

**Treadmill form:** pre-loading answers into learner state before
the probe run; world-ID-indexed fact tables in source or in the
teaching script; benchmark-specific teaching sequences that the
researcher tuned to the probe order.

**How the guard catches it:** Check 2 requires fresh learner state
and the same teaching sequences TNN-2 used. Pre-loading is a
scaffolding change and fails the anti-gaming check. The
determinism requirement (three byte-identical runs) catches
order-dependent tuning.

### F2. Law change and revert (FW4)

**Treadmill form:** pre-registering the revert value in source
(the researcher knows the test sequence: change to Y, revert to
X); hardcoding "law change handlers" per world that pattern-match
the probe keys.

**How the guard catches it:** Check 2 with sealed revert values:
run the FW4 sequence with values the researcher did not see at
build time. The mechanism must derive the reverted answer from
the contradiction content, not from source. A handler that only
works on the published probe keys fails the generality check.

### F3. Targeted update without collateral damage (FW5)

**Treadmill form:** a researcher-specified update radius hardcoded
in source; world-specific neighbor lists that tell the mechanism
which keys are "neighbors" for the test worlds.

**How the guard catches it:** Check 3: the update target must be
identified from the contradiction content, not from source. Run
the FW5 probes with novel keys not present at build time. A
hardcoded radius that happens to match the test geometry is a
one-world patch.

### G1. Construction over learner-taught facts (GW3 phase 2)

**Treadmill form:** hardcoding the level-2 construction to read
the specific level-1 fact used in the GW3 probes (a world-specific
edge); a "constructor" that consumes taught facts only for the
tested keys.

**How the guard catches it:** Check 3 with novel taught facts:
teach a fresh level-1 chain on keys the builder never saw, then
require the level-2 construction to traverse the fresh fact as an
edge. A world-specific edge fails; general edge consumption
passes. Check 1 also applies: the decision of which taught fact
to traverse must be learner-resolved, not source-listed.

### G2. Single-level value revision, no dependents (GW7 probe 5)

**Treadmill form:** hardcoding the 100-to-200 mapping (the
researcher knows the test values); a revision path that works
only on the specific tested key.

**How the guard catches it:** Check 2 with novel contradiction
values: contradict with values not in the published probes and
require the revised value to surface through the query path. A
mapping hardcoded for the test values fails. Note the boundary:
the floor is the no-dependent case; extending to the dependent
case (GW3 phase 3) is the target, not the floor.

### G3. Inquiry discrimination and re-fire (GW6 primary, GW7)

**Treadmill form:** hardcoding CHOICE 30 for the specific test
keys rather than general miss detection; pre-listing "untaught"
keys in source so the miss path fires by lookup; a re-fire that
triggers on probe count rather than on fresh ignorance.

**How the guard catches it:** Check 2 with novel keys: fresh
taught keys must return CHOICE 0, fresh untaught keys must miss
with CHOICE 30, and new ignorance after teaching must re-fire.
A lookup table of test keys fails on novel keys. Also check 6's
warning sign: the constant act is discrimination infrastructure,
not contingency. Presenting G3 as satisfying FW6 is
failure-mode preservation.

### The floor is not the ceiling

A final treadmill form cuts across all seven: treating the floor
as the target. The floor spec section 3 excludes FW3/FW7/FW8/FW9,
FW6 contingent inquiry, GW6 retirement, GW8 rev2/revert, GW3
phases 3-4, GW4, GW5, the GW1 depth ceiling, and the GW2 DAG-only
bound. A TNN-3 program that optimizes the seven floor tests and
declares victory has built a treadmill that runs in place. The
floor is what TNN-3 must keep while climbing. The kill bars
(`1722884ad`) are the climb.

---

## 5. When the guard itself could be gamed

Three ways to game this guard, named so they can be watched for:

1. **SUF theater.** The mechanism exposes a learner-state knob
   that selects among source-enumerated schemas, and the SUF
   check is run on the knob rather than on the schema set. The
   SUF definition (`64eec921f` section 2b) is explicit: selecting
   among 3 fixed templates using learner state fails SUF,
   because the 3 templates are enumerable from source alone.
   Run the check on the producible forms, not on the selector.
2. **Checklist compliance without property.** All five checks are
   performed formally but the property statement (check 4) is
   vague enough to match any outcome. The property must be
   falsifiable: state what observation would show the property
   absent.
3. **Floor-only optimization.** The seven floor tests become the
   de facto benchmark and all effort goes into keeping them
   green while no kill bar moves. Track kill-bar movement
   alongside floor status; a flat kill-bar count across two
   consecutive build cycles with a green floor is the treadmill
   running quietly.

---

**Verdict: TREADMILL-GUARD-COMPLETE.**

Five checks, seven per-capability analyses, three guard-gaming
modes named. The guard is a development discipline document; it
governs TNN-3 work only if a frozen preregistration references it.
