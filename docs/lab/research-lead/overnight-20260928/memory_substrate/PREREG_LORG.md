# PREREG: Learner-Owned Retention Graph (LORG)

## General Memory Substrate for the Frozen Core

Date: 2026-09-30. Worker: General Memory Substrate Designer.
Status: PREREG-FROZEN. No implementation authorized until review.
Parent directive: Micah 2026-09-30, Core Freeze Challenge as central benchmark.
Claim context: C75 EVICTION-TIE-BREAKER-PATHOLOGY.

---

## 1. Analysis: Why the C75 Pathology Arises

Frozen source: `core_freeze/stage0/world_learn.zag` at e129b2fbd
(source b761efd90cb1, binary 8733af3d2814).

### 1.1 The mechanism

The store is 36 slots. Each slot is an 11-field i32 record (44 bytes):
fields are subj(0), rel(4), obj(8), correct(12), wrong(16), dependents(20),
contradictions(24), last_used(28), taught(32), superseded(36), valid(40).

Retention priority is computed by a hardcoded function:

```
importance_c = 10*(correct - wrong) + 5*dependents - 8*contradictions + 1
```

Eviction (`evict_c`) scans slots 0..35 and selects the valid slot with
minimum importance. Ties resolve by strict-less comparison
(`if(imp<bestk)`), so the lowest-index slot wins every tie.

`learn()` writes a new fact with all counters zeroed, giving every new
fact importance exactly 1.

### 1.2 The pathology, mechanistically

When the store fills with importance-1 entries (untaught, unprobed facts),
every call to `evict_c` returns slot 0. The new fact is written into slot 0
with importance 1. The next teach calls `evict_c` again, which again
returns slot 0, because slot 0 still has the minimum importance (1) and
the lowest index among ties. Sequential teaches overwrite slot 0 forever.
Observed signature: `OBSERVED 9601 610 10` immediately followed by
`EVICT 9601 610`. The substrate cannot stably hold 6 sequential new facts.

### 1.3 Root causes (not symptoms)

The tie-breaker is the symptom. The root causes are architectural:

R1. **Importance is a hardcoded formula.** The weights (10, 5, -8, +1) are
researcher-chosen constants. The learner cannot change what it values.
There is no mechanism by which experience modifies the retention policy.

R2. **No recency or newness term.** Fields `last_used` (28) and `taught` (32)
are recorded on every learn and query, but neither appears in
`importance_c`. A fact taught 1 tick ago and a fact taught 1000 ticks ago
have identical importance if neither was queried. The system cannot
distinguish "new and potentially useful" from "old and never used."

R3. **Positional tie-break creates a stable attractor.** Lowest-index-wins
is arbitrary. Slot 0 becomes a sacrificial slot through which all new
facts flow. Any deterministic positional rule creates such an attractor;
randomizing the tie-break would merely diffuse it, not remove the cause.

R4. **Flat representation.** The 36 slots are independent triples.
Field `dependents` (20) counts how many two-hop queries touched a record,
but there is no record of WHAT depends on it. Evicting a record cannot
consider the structure it participates in. A tree (W9), a causal law
(W4), or a procedure (W2) is N independent slots with no shared fate.

R5. **The learner has no retention agency.** The only way a fact escapes
the importance-1 pool is to be queried (correct increments raise
importance to 11). But queries are issued by the world driver, not by
the learner. The learner cannot say "I will need this later" or "this
belongs to a structure I am building." Retention is something that
happens TO the learner's knowledge, not something the learner DOES.

### 1.4 Why a tie-breaker fix is a treadmill patch

Changing `if(imp<bestk)` to oldest-first, or adding `+ recency_bonus` to
the formula, would fix the specific slot-0 attractor. But:

- The weights remain researcher-chosen. The next pathology will come
  from a different constant.
- The representation remains flat. W9 structures still have no shared fate.
- The learner still has no agency. The policy still cannot learn.

Micah's directive is explicit: this must NOT become another cache-policy
version treadmill. The design below changes WHO owns the policy, not
just the policy's constants.

---

## 2. Design Space Survey

### 2.1 What was considered and rejected

**(a) Learner-tunable linear weights.** Store the six weights in learner
state; adjust by gradient or heuristic. REJECTED as the primary mechanism:
it is cache-policy version 2. The representation stays flat, newness is
still just a term, and structures still have no shared fate. It addresses
R1 only.

**(b) Hardcoded probationary protection.** New records immune to eviction
for N ticks, N a constant. REJECTED: N is researcher-chosen. It fixes the
C75 symptom for one N but creates a new cliff at N+1. Treadmill.

**(c) Generational tiers (nursery/tenured).** REJECTED: tier boundaries and
promotion criteria are researcher-chosen. A more complex cache policy,
not a learner-owned one.

**(d) Explicit pin/unpin operations.** The learner marks records protected.
REJECTED as a standalone mechanism: without a learning rule for WHEN to
pin, it is a manual override. Pinning without principled unpinning
exhausts the store. The decision logic must itself be learned.

**(e) Full importance-function synthesis.** The learner writes its own
importance function from combinators. REJECTED as premature: the search
space is large, degenerate functions are likely, and it does not address
the structural (R4) or agency (R5) causes. A possible later step, not
the substrate.

### 2.2 What the design must do

From Micah's question, the substrate must let one frozen learner preserve:

- **Newly useful knowledge** (addresses R2, R5, and the C75 symptom)
- **Dependencies** (addresses R4: WHAT depends on a record)
- **Hypotheses** (tentative beliefs needing protection until confirmed)
- **Structures** (multi-record units with shared fate, addresses R4)

without task-specific storage logic (no per-world-type branches), and the
policy must reside in learner state (addresses R1).

---

## 3. Proposed Design: Learner-Owned Retention Graph (LORG)

### 3.1 Core principle

The frozen core provides generic retention MACHINERY. The learner owns the
POLICY. Three mechanisms, each general, each addressing distinct root
causes:

1. **Probationary protection with learner-controlled duration** (R2, R5).
2. **Dependency links with structural eviction cost** (R4).
3. **Regret-based weight adaptation** (R1).

### 3.2 Representation (all in learner state, W buffer)

**Weight vector** (6 i32, fixed offset in W header region):
`w_correct, w_wrong, w_dependents, w_contradictions, w_recency, w_newness`.
Initialized to defaults reproducing current behavior
(10, 10, 5, 8, 0, 0). Modified ONLY by the regret update rule (3.6).
Never written by world-type-specific code.

**Probation duration** (1 i32): ticks of eviction immunity granted to each
new record. Initialized to a default (e.g. 12). Modified ONLY by the
regret update rule. This is the learner's own "how long do I give new
knowledge to prove itself" parameter.

**Per-record probation clock** (1 i32 per slot, new field 44): ticks of
immunity remaining. Set to probation duration at teach time. Decremented
once per global tick. Records with clock > 0 are skipped by eviction.

**Dependency links** (2 i32 per slot, new fields 48, 52): slot indices of
records this record depends on, or -1. Created ONLY through the generic
`link_depend(s, t)` operation (3.5). Read by eviction to compute
structural cost. No semantic content: the core does not know what a link
MEANS, only that it exists.

**Group table** (learner-created, up to 8 groups): each group has a member
bitmask (36 bits, 2 i32) and a group bid (1 i32). Groups are created by
the generic `group_create()` operation and joined via `group_add(g, s)`.
A group is a learner-declared structural unit: "these records stand or
fall together."

**Eviction ring buffer** (8 i32): keys (subj) of the 8 most recently
evicted records, with eviction tick. Used ONLY by the regret rule.

Total new learner state: approximately 110 i32 (440 bytes) in the 32KB
W buffer. Negligible.

### 3.3 Bid computation (replaces importance_c)

```
bid(s) = w_c*correct(s) - w_w*wrong(s)
       + w_d*dependents(s) - w_k*contradictions(s)
       + w_r*recency_bonus(tick - last_used(s))
       + w_n*newness_bonus(tick - taught(s))
       + structural_cost(s)
```

where `recency_bonus` and `newness_bonus` are fixed decreasing functions
of age (e.g. `max(0, 32 - age)`), and `structural_cost(s)` is:

```
structural_cost(s) = link_penalty * (number of live records linking to s)
                   + group_bonus(s)
```

`link_penalty` is in learner state (default 50, modified only by regret).
`group_bonus(s)` is the group bid if s belongs to a group with at least
2 live members, else 0.

### 3.4 Eviction (revised evict_c)

1. Skip all records with probation clock > 0.
2. Among eligible records, select minimum bid(s).
3. Tie-break: oldest `taught` first. The tie-break RULE is in learner
   state (default oldest-first); the core implements the selected rule.
   This removes the positional attractor without hardcoding a new one.

### 3.5 Generic operations (frozen core machinery)

- `link_depend(s, t)`: record that slot s depends on slot t. Sets link
  fields, increments dependents count. No semantic interpretation.
- `group_create() -> g`: allocate a group id from the learner-owned table.
- `group_add(g, s)`: add slot s to group g member mask.
- `group_bid(g, v)`: set the group's retention bid (learner decides v).
- `protect(s, ticks)`: grant additional probation ticks to slot s
  (learner-initiated, e.g. "this hypothesis needs more time").
- `release(s)`: end probation early (learner-initiated).

These are domain-general. None branches on world type, relation id, or
subject range. The LEARNER's cognitive process (the existing Zag program
logic, extended) decides when to call them, based on its own processing,
not on hardcoded world-type dispatch.

### 3.6 Regret-based weight adaptation (the learner-owned policy update)

This is the mechanism by which the policy becomes LEARNER-OWNED rather
than researcher-set. It is generic: it responds to the learner's own
experience, not to world-type labels.

**Trigger:** a query misses (key not found in store) AND the missing key
appears in the eviction ring buffer with eviction tick within the last
`regret_window` ticks (regret_window in learner state, default 64).

**Update (all deltas in learner state, defaults small):**

- `w_newness += regret_delta` (protect new knowledge more)
- `w_recency += regret_delta` (protect recently used knowledge more)
- `probation_duration += 1` (give new knowledge more time), capped at a
  learner-state maximum
- `w_correct -= regret_delta / 2` (slightly reduce reliance on earned
  correctness, which favors old knowledge)

**Anti-trigger (stability):** if no regret event occurs for
`stability_window` ticks (learner state, default 512), decay all weights
5 percent toward defaults and decay probation_duration 1 toward its
default. This prevents runaway protection that would fill the store
with immortal junk.

The update rule is fixed generic machinery. The WEIGHTS are learned.
After experience in varied worlds, the learner's weight vector reflects
what actually preserved useful knowledge IN ITS EXPERIENCE. That is what
"learner-owned policy" means: the policy parameters are a function of
the learner's history, not the researcher's priors.

### 3.7 How hypotheses are preserved

A hypothesis is a tentative record the learner creates before confirmation.
Mechanism: the learner teaches the hypothetical fact (generic `learn`),
then calls `protect(s, extra_ticks)` to extend its probation while it
gathers evidence. If evidence confirms it, queries raise its correct
count and it earns retention normally. If evidence refutes it, the
learner calls `release(s)` or lets probation expire, and normal eviction
applies. No hypothesis-specific code path: hypotheses are records with
learner-extended probation.

### 3.8 Worked example: W9 tree preservation

W9 teaches 28 edge triples forming tree A. Under LORG:

1. Each triple is taught; each gets probation_duration ticks of immunity.
   The 28 triples do NOT overwrite each other (C75 eliminated).
2. As the learner processes the tree (queries traversing edges), it calls
   `link_depend(child_slot, parent_slot)` for each edge it traverses.
   The tree structure is now in the dependency graph.
3. The learner calls `group_create()` and `group_add()` for all 28 slots,
   declaring the tree a structural unit, and sets a group bid reflecting
   its ongoing use.
4. When memory pressure comes, eviction must pay `link_penalty` per
   dependent plus overcome the group bid to evict any tree member.
   The tree survives as a unit or not at all; it cannot be silently
   hollowed out one edge at a time.

No tree-specific code. The same operations preserve a causal law (W4),
a procedure's steps (W2), or a vocabulary (W8).

---

## 4. One-System Rule Accounting

| Item | Count |
|---|---|
| Cognition source lines added (est.) | 100-130 |
| New hardcoded semantic cases | 0 |
| New modes | 0 |
| New bridges | 0 |
| New task-specific handlers | 0 |
| Per-world-type branches | 0 (verified by inspection in review) |
| Learner-state structures created | weight vector (6 i32), probation duration (1 i32), per-record probation clock + 2 link fields (3 i32 x 36), group table (8 x 3 i32), eviction ring buffer (8 i32), link_penalty, regret_window, stability_window, regret_delta (4 i32) |
| Capability source delta | The substrate is generic machinery. Capability (what is preserved) comes from learner-initiated link/group/protect calls and regret-adapted weights, all in learner state. |

What the existing architecture cannot learn this behavior without:
the current `importance_c` weights are immediates in code. No experience
can modify them. The per-record link fields do not exist. Probation does
not exist. The question "why can the existing general architecture not
learn this" is answered: the retention policy is not represented in
mutable state at all. LORG moves it into mutable learner state with a
generic update rule. That is the architectural change; everything else
is consequence.

---

## 5. Predicted Outcomes (for future implementation, on fresh worlds)

The preregistered predictions below are for an implementation of THIS
design, evaluated on FRESH adversarial worlds (not the frozen ones, which
the learner has already seen). They are falsifiable.

P1. **C75 pathology eliminated.** In a fresh sequential-teach stress
(36+ new facts, no intervening probes), all facts taught within the
probation window survive. Zero occurrences of the
OBSERVED-then-EVICT-same-key signature. (Mechanism: 3.4 step 1.)

P2. **W4-class (law change/revert), fresh world.** Predicted 6/6 pre,
6/6 post, 6/6 revert, vs frozen-core 1/6, 2/6, 3/6. (Mechanism:
probation protects the 6 sequential facts; dependency links preserve
the law structure across the change.)

P3. **W5-class (contradictions), fresh world.** Predicted full targeted
and collateral retention, vs frozen-core 1/2 and 4/6. (Mechanism:
probation plus regret adaptation increasing w_newness after the first
regret events.)

P4. **W8-class (synthetic language), fresh world.** Predicted 5/5 novel,
4/4 recall, vs frozen-core 0/5, 0/4. (Mechanism: probation protects new
vocabulary until probed.)

P5. **W9-class (representational structure), fresh world.** Predicted
above 20/28 and 20/31 edge retention, vs frozen-core 0/28, 0/31.
(Mechanism: dependency links plus group bid preserve the tree as a
structural unit.)

P6. **No single-world overfitting.** The SAME implementation, without
modification, achieves P2 through P5. If per-world tuning is required,
the generality claim fails.

P7. **Learner-ownership observable.** After the fresh-world battery, the
weight vector differs from defaults in the direction predicted by the
regret rule (w_newness and w_recency elevated relative to w_correct),
and the difference correlates with the number of regret events. If
weights never move, the adaptation mechanism is broken.

### Falsification conditions

- F1. If P1 fails (the slot-0 attractor reappears in any form), the
  probation mechanism is insufficient. REJECT the design.
- F2. If P5 fails while P2-P4 pass, the dependency/group mechanism is
  insufficient for structures. NARROW the design claim to flat knowledge.
- F3. If implementation requires any branch on world type, relation id
  range, or subject id range in the retention path, the generality claim
  is violated. REJECT the implementation (not necessarily the design).
- F4. If a fixed-weight ablation (weights pinned at defaults, no regret
  updates) matches the full design on P2-P5, the learner-ownership
  claim is unnecessary. SIMPLIFY: adopt probation plus links without
  adaptation.
- F5. If the store fills with immortal junk (junk count rising across
  worlds without bound), the stability decay is insufficient. REVISE
  the anti-trigger.

---

## 6. What This Design Deliberately Does Not Do

- It does not change the 36-slot capacity. Capacity is a physical
  constraint; the pathology was never about capacity.
- It does not add a semantic case for trees, laws, procedures, or
  vocabulary. All structures use the same link/group/protect operations.
- It does not pre-specify which knowledge is valuable. Value is
  determined by the learner's experience through the regret rule.
- It does not implement. Implementation follows review of this prereg.

---

## 7. Review Questions for the Parent

Q1. Is the regret-based adaptation (3.6) sufficiently general, or does
the choice of WHICH weights move on regret encode a researcher prior
that should itself be learned?

Q2. Should `protect`/`release` be learner-callable operations, or does
giving the learner direct probation control risk a degenerate "protect
everything" policy? (Mitigation proposed: the stability decay and the
fact that protection consumes the shared probation budget implicitly
through slot occupancy.)

Q3. Is 100-130 lines of new cognition source acceptable under the
One-System Rule, given that zero lines are task-specific and all policy
content moves to learner state? The alternative (no substrate change)
accepts the C75 ceiling permanently.

---

Prereg frozen 2026-09-30. No code written. Awaiting review before
implementation.
