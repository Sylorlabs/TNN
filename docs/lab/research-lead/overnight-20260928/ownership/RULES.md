# STANDING RULES -- TNN RESEARCH PROGRAM

Standing policy. Supersedes ad-hoc per-lane decisions.
Not lane-local. Applies to every experiment from here on.

Derived from C1431-C1510 defects and program review.

---

## R1. NO NAMED COGNITIVE MODES

Forbidden as permanent source-level structure:

```
PLAN_MODE  INVENT_MODE  VERIFY_MODE  PREDICT_MODE  CAUSAL_MODE
REVISE_MODE  ROUTER  BELIEF_MODULE  CHECKER  INVENTOR
```

The test for a name like this: if the name is chosen by the
researcher *because* of what it does cognitively, it is
researcher cognition wearing a learner hat.

Permitted only as a **temporary baseline explicitly marked for
deletion**, recorded in the report's delete list.

Rationale: "planning", "verification", "prediction" should be
*descriptions of emergent behaviour*, not enum values. If the
source says `PLAN_MODE`, the researcher partitioned cognition
and TNN inherited the partition.

Corollary: a behaviour may be *named in a report* freely.
Naming is description, not architecture.

---

## R2. NO BRIDGES

Forbidden:

```
A_TO_B_BRIDGE  B_TO_C_BRIDGE  GRAPH_TO_PROGRAM_BRIDGE
FORMAL_TO_ACTION_BRIDGE
```

Bridges are temporary research scaffolding, never
architecture. The path of adding one bridge per discovered
interaction is the path to hundreds of mechanisms.

**The required move instead:** when structures A and B fail to
interact, ask what *generic property* blocked it. Candidates:

- input/output contract
- learned compatibility
- reference mechanism
- constraint compatibility
- state-effect compatibility
- shared addressing
- dependency relation

Fix that one generic property. Then arbitrary future
structures can interact without a bridge written for that
pair.

A bridge is acceptable ONLY as a temporary baseline marked
for deletion, and ONLY to establish that the generic
property is the real blocker.

---

## R3. RECOMPUTE EVERY PROMOTED BAR FROM RAW MEASUREMENTS

**Never trust a precomputed `ok=1` field emitted by the
experiment.**

This is now an enforced lint (see `tools/tnn_bars_lint.sh`).

Origin: in C1471 I wrote in my own prereg "no bar may be set
from a printed constant" and then set `random_ok=1` from a
printed constant without comparing. That fake bar concealed a
real evaluator bug for an entire lane.

Rules:

1. Every bar must be recomputed from raw printed measurements.
2. Every numeric bar must be cross-checked against a closed
   form or an independent recomputation.
3. If measured disagrees with theory, **investigate the
   measurement** before reporting. Do not report the
   measurement and move on.
4. A bar whose name contains `ok`, `valid`, `pass`, `clean`,
   or `uniform` MUST have an adjacent comparison against a
   measured quantity in the source. The lint enforces this.

---

## R4. DO NOT DESIGN AGAINST H16

Do not ask "how do we pass H16?"

Ask: **what architectural mechanism should exist if TNN truly
becomes more self-organizing?**

Then let H16v3 try to kill it.

L3 is the *consequence* of genuinely learner-owned cognition.
It is not the optimization target. Designing to pass the judge
produces judge-shaped artifacts.

---

## R5. STEAL PRINCIPLES, NOT SUBSYSTEMS

Never bolt on another architecture. Never integrate an LLM as
a cognitive module.

TNN is meant to be general intelligence, not hardcoded for any
particular action. Hardcoding prediction is what LLMs do.

Study what other architectures *discovered*, then ask whether
TNN's substrate can develop that behaviour without the
subsystem:

| Source | Principle (steal this) | Forbidden (subsystem) |
|---|---|---|
| Transformers | content-dependent interaction, dynamic routing | attention module bolted on |
| Hopfield / attractors | distributed states settle to stable configs | a Hopfield array + router |
| Hebbian | local co-activation modifies connectivity | global hand-written constructors |
| Predictive coding | local mismatch drives representation change | a central `REVISE_MODE` |
| Program synthesis | structures compose from generic primitives | fixed mutation operator menu |
| Evolution | open populations mutate, combine, compete | fixed researcher mutation ops |

Concretely rejected as architecture: "put a transformer inside
TNN", "bolt on a symbolic planner", "add a Hopfield subsystem
and route into it".

---

## R6. THE OWNERSHIP SPLIT

**Researcher-owned machine substrate** -- small, semantically
neutral, and it should shrink over time:

- allocate state
- read / write state
- reference state
- compare
- arithmetic
- branch
- link / unlink
- execute a stored structure
- receive observations
- issue actions
- receive consequences

**Learner-owned cognition** -- ownership must keep expanding:

- what gets stored
- how things are grouped
- what structures mean through use
- which structures execute
- applicability
- procedures
- abstractions
- addressing organizations
- internal evaluators
- search organization
- memory organization
- composition
- revision
- method construction
- how new methods are learned

The claim is **not** "zero researcher code". The claim is:

> researcher code increasingly stops containing cognition.

Something must execute the learner. A CPU does not relearn
`ADD` every boot. The substrate is the floor, not the target.

---

## R7. CONTROLS ITS OWN COGNITION WITHOUT BREAKING ITSELF

TNN does not own *everything*. It controls as much as possible
**without breaking its own thoughts, outputs, plans, and
state.**

So a candidate mechanism must be checked for self-damage, not
just self-improvement. A mechanism that improves task score
while corrupting its own persistent structures, its own
addressing, or its own ability to produce output is a failure,
not an advance.

This makes "self-modification" a hazard class that must be
tested, not a goal to be maximized.

---

## R8. NO BOLT-ONS, NO GIVING UP

Test all forks of the research. Do not bolt other
architectures onto TNN, and do not abandon the local search for
TNN-native architecture because an external system looks
stronger.

---

## R9. ONE WORLD, EMERGENT ROLES, NO FIXED IDENTITIES

Target architecture: one large persistent adaptive structural
world. No source-level declaration of role. A structure that
consumes goal+state and emits actions is *functionally* a
planner. A structure that consumes candidates and emits
confidence is *functionally* a checker. Roles emerge through
learned relationships and use.

And roles must be **fluid**: a structure learned for one
functional context should be recruitable in another with no
bridge written for that pair of roles.

**The flagship domain-blind test** (see BORROW prereg):

> Can a structure learned in one functional context be
> recruited in another, without a bridge explicitly written
> for those two roles?

If that works, R2 is satisfied empirically. If it fails, the
missing abstraction is whatever blocks it, and we name *that*.

---

## R10. REPORT NEGATIVES AS RESULTS

A mechanistic negative closes more of the map than a marginal
positive. State the mechanism, not just "it failed".

Prefer: "the feedback geometry was flat, so there was nothing
meaningful to learn about proposal quality" over "proposal
learning failed".