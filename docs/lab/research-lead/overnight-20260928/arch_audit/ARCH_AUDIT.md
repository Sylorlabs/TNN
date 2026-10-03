# Architecture Audit: One-System Rule Compliance

**Status:** AUDIT ONLY. No implementation, no design changes proposed as
builds. Findings and recommendations.
**Date:** 2026-10-01
**Verdict:** ARCH-AUDIT-COMPLETE

## 0. The rule being audited

Micah's ONE-SYSTEM RULE (2026-09-30): TNN must not become dozens of
cognitive subsystems joined by routers, bridges, special modes, and
task-specific admission gates. Target: one general cognitive substrate
(small generic protected core + learner-created cognitive structures +
persistent experience). New capability should require EXPERIENCE leading
to NEW LEARNED STATE/STRUCTURE, not a NEW ZAG SUBSYSTEM/MODE/BRIDGE/
HANDLER.

Smell triggers from the ruling: new modes (CAUSAL_MODE etc.) are
architectural smells; three custom bridges around one boundary trigger
ARCHITECTURE REVIEW and block further bridge work.

## 1. Mechanisms audited

Five specified mechanisms, all from the post-freeze research wave:

| # | Mechanism | Spec commit | State |
|---|---|---|---|
| M1 | Discount (per-FACT field) | `62fa77192` | Spec only |
| M2 | Shared substrate (pursuit/strategy store) | `550fa268b` | Spec only |
| M3 | Fragment records (composition memory) | `8b7b0f12a` | Spec only (DRAFT design) |
| M4 | Corruption detector | `ff2d1e1ef` | Spec only (driver-side) |
| M5 | H3-lite Node 1 (trial order policy) | `45c55ed83` | Built, 3/3 byte-identical |

## 2. Per-mechanism audit

### M1. Discount

- **Modes:** 0 new. No mode added; discount is a field read inside
  existing `bootstrap_miss`.
- **Bridges:** 0. No connectors between subsystems.
- **Task-specific handlers:** 0 new. Write paths (W1/W2/W3) and read
  path (R1) are integrated into existing production functions
  (`ev_observe`, `bootstrap_miss`). These are extensions of general
  paths, not task-shaped handlers.
- **State format:** one signed i32 per FACT node (field 12). No new
  node type, no new edge type, no new opcode. The state lives inside
  the existing FACT representation, not in a parallel store.
- **Assessment:** CLEAN. Discount adds a field and rules, not a
  subsystem. It is the smallest possible structural footprint for
  its function.

### M2. Shared substrate

- **Modes:** 0 new.
- **Bridges:** 0 new.
- **Task-specific handlers:** 0 new handlers, but 4 new decision
  points (decline gate, abandonment gate, retention input, trial
  reorder). These are gates inside existing paths (query, miss,
  eviction, trial dispatch), not standalone subsystems. The spec is
  explicit that each gate must satisfy read-path-first or be
  classified theater.
- **State format:** one keyed store, two namespaces (PURSUIT,
  STRATEGY), one record format, one reclamation policy. The spec's
  central claim is architectural compression: this REPLACES
  per-decision private counters rather than adding to them.
- **Convergence check:** Section 5.4 specifies migration of H3-lite
  Node 1's field-32 private counter into STRATEGY records. The
  direction is convergence (narrow counter -> shared store), not
  proliferation. However, the built Node 1 (`45c55ed83`) still uses
  field 32; the migration is specified but not implemented. Until
  migration happens, both exist. This is a tracked transition, not
  a violation, but it must not become permanent parallel machinery.
- **Assessment:** CLEAN with one tracked item (M5 field-32 migration).

### M3. Fragment records

- **Modes:** 0 new.
- **Bridges:** 0 new.
- **Task-specific handlers:** extraction runs on the promotion path;
  splice selection is a new production path but it is the
  composition capability itself, not a task-shaped handler bolted
  onto an unrelated system.
- **State format:** tag-20 nodes (same as every MAP), distinguished
  by field 24 = -2. The spec is explicit: "fragments are the same
  executable graph type," "a new tag would be a second
  representation and a One-System Rule violation." One graph type,
  one execution path, one revision path.
- **New edge types:** 3 (ET_FRAGUSE 14, ET_FRAGSLOT 15, ET_FRAGHIST
  16). These are new enumerable relations, not bridges. Each names
  a distinct relation (composite-uses-fragment, fragment-has-slot,
  fragment-cites-fact). Reusing an existing type would conflate
  relations; the new types are justified.
- **Node enlargement 40 -> 72 bytes:** +1 researcher-owned
  structural decision, the largest layout change in the spec set.
  This is layout machinery (like the existing 40-byte layout), not
  a mode/bridge/handler. It does not create a second
  representation. But it is a significant researcher intervention:
  80% more bytes per node, `noff()` change, workspace budget
  recomputation. The spec names the edge-overflow alternative
  without developing it. Flagged for Micah awareness, not as a
  rule violation.
- **Assessment:** CLEAN on the One-System Rule. The tag-20 reuse is
  the correct call. Node enlargement is a cost/complexity flag,
  not an architectural smell.

### M4. Corruption detector

- **Scope:** driver-side (researcher harness), not learner state.
  It reads frozen-state layout and logs CORRUPTION events for the
  lifetime protocol.
- **Modes/bridges/handlers (learner):** not applicable. The detector
  adds zero learner machinery.
- **Assessment:** OUT OF SCOPE for the One-System Rule. It is
  measurement infrastructure, explicitly labeled researcher-owned.
  It cannot proliferate learner subsystems because it is not in
  the learner.

### M5. H3-lite Node 1 (built)

- **Modes:** 0 new. Verified in build report.
- **Bridges:** 0 new. Verified.
- **Handlers:** 0 new. Verified.
- **State format:** tag-40 policy node, subtype 1. This IS a new
  node tag for a policy structure. The prereg authorized it as a
  bounded probe ("policy revisability, not SUF").
- **Narrow counter:** field 32 (rejection count) is a private
  per-node counter, the exact pattern the shared substrate is
  meant to replace.
- **Assessment:** CLEAN as a preregistered probe, with the
  migration to M2 tracked (see M2 assessment). The tag-40 node
  itself remains as the decision point under the substrate spec
  ("the node itself remains as the decision point; what migrates
  is the evidence"). One policy node per decision is the intended
  steady state, not per-decision counter proliferation.

## 3. Cross-mechanism convergence checks

### 3.1 Discount (M1) vs substrate (M2): two failure trackers?

Both mechanisms record failure-related state:

- Discount: per-FACT graded suspicion (field 12). Consumer:
  bootstrap evidence scan. Granularity: individual fact.
  Question answered: "which facts should I trust as evidence?"
- Substrate PURSUIT: per-(s,r) attempts/successes/consec_fail.
  Consumers: decline gate, abandonment gate. Granularity: pursuit.
  Question answered: "should I keep pursuing this?"

Overlap point: bootstrap failure writes to both. Discount W3
increments minority-fact discounts; the substrate records the
pursuit failure with last_mode F4 (bootstrap disagreement). Same
event, two bookkeeping entries at different granularities.

Finding: NOT redundant. Fact-grained epistemic liability and
pursuit-grained outcome summaries answer different questions for
different consumers. Collapsing them would force false
commensurability (a suspect fact is not a failed pursuit; a failed
pursuit does not imply its facts are suspect). The specs are
consistent on this separation: discount Section 4.4 claims
"disjoint mechanism space" from H3-lite, and the substrate spec
does not claim the discount field.

Tracked item: the W3/F4 double-write should be documented as a
single event with two records, not two independent judgments. If a
future design unifies "outcome" representation, revisit. No action
now.

### 3.2 Fragments (M3) vs substrate STRATEGY records

Fragment F-utility (fields 12/16: invocations, successes) tracks
per-fragment outcomes. Substrate STRATEGY records track
per-strategy (family/topology) outcomes. A fragment is a reusable
strategy-like entity; is F-utility a third narrow counter?

Finding: POTENTIAL OVERLAP, deferred. The fragment spec predates
final substrate convergence thinking; F-utility fields 12/16 on
fragment nodes serve the same role as STRATEGY records (which
strategy works). The substrate spec reserves STRATEGY keys for
"family id" and "topology id" but does not mention fragment ids.
If composition memory is built, fragment utility should migrate
to STRATEGY records keyed by fragment id, with the node fields
becoming a cache or being removed. This is the same convergence
pattern as Node 1 field 32. Flagged as a build-time requirement:
the composition preregistration must state whether F-utility stays
on-node or migrates to the substrate. Not a violation today
(neither is built).

### 3.3 Substrate vs Node 1 policy node (M2 vs M5)

Covered in M2 assessment. The substrate spec is explicit:
policy node remains as decision point, evidence migrates to
STRATEGY records. Steady state: one node per decision, zero
private counters. Tracked, not violated.

### 3.4 Corruption detector (M4) vs everything

No interaction. Driver-side only.

## 4. Smell inventory

| Smell class | Found | Where |
|---|---|---|
| New modes (CAUSAL_MODE pattern) | 0 | -- |
| Custom bridges | 0 | -- |
| Task-specific handlers | 0 | -- |
| Second representation / new graph type | 0 | M3 correctly reuses tag-20 |
| Parallel private counters (permanent) | 0 permanent; 2 tracked transitions | M5 field-32 -> M2; M3 F-utility -> M2 (build-time) |
| Researcher magic numbers (treadmill surface) | 2 noted | M1 threshold T, floor C (spec acknowledges; requires fixed + sensitivity-reported) |
| Large researcher layout change | 1 flagged | M3 node 40->72 bytes (not a smell; cost flag) |

No smell triggers ARCHITECTURE REVIEW. The three-bridge trigger is
nowhere near firing (zero bridges).

## 5. Recommendations

1. **Keep M1 and M2 separate.** Fact-grained discount and
   pursuit-grained outcome records answer different questions.
   Document the W3/F4 double-write as one event, two records.
   Revisit only if a unified outcome representation emerges from
   implementation experience.

2. **Enforce the M5 -> M2 migration.** The built Node 1's field-32
   counter must not become permanent parallel machinery. Any
   follow-on Node 1 work (including the weak K-LT-5 sealed
   evaluation currently running) uses the built form; the
   migration is a specified future step, not a blocker. But no
   second narrow counter (for Node 2 or 3, if revived) should be
   built on the field-32 pattern; new decisions go directly to
   the substrate.

3. **Composition build must resolve F-utility placement.** The
   composition preregistration (when written) must state whether
   fragment F-utility lives on-node (fields 12/16) or migrates to
   substrate STRATEGY records keyed by fragment id. Recommendation:
   migrate, following the Node 1 precedent. Do not ship both
   permanently.

4. **Node enlargement needs a Micah-visible cost note.** The
   40->72 byte change is honest researcher-owned machinery, but
   at 1024 nodes it is ~32KB additional fixed cost plus budget
   recomputation, and it interacts with the scaling wall (the
   budget-pressure finding). The edge-overflow alternative
   should be sketched (not necessarily built) before the
   composition preregistration is frozen, so the choice is
   documented as considered.

5. **No new node tags for future mechanisms without audit.**
   M3 set the right precedent (tag-20 reuse). Any future spec
   proposing a new tag for a cognitive structure should be
   flagged to this audit pattern before implementation.

6. **Threshold discipline for M1.** T and C must be fixed once,
   documented, and sensitivity-reported (T=1/2/3) in any
   evaluation. Tuning per result is benchmark-fitting and
   invalid per the spec's own Section 6.4. This is a governance
   note, not an architectural one.

## 6. Bottom line

The five mechanisms converge on one substrate family, not five
subsystems. Zero modes, zero bridges, zero task-specific handlers,
zero second representations. Two narrow counters are tracked for
migration into the shared store (Node 1 field-32, fragment
F-utility); neither is built in duplicate today. The discount
field and the substrate records are complementary, not redundant.
The corruption detector is not learner architecture.

**The One-System Rule holds across the current spec set.** No
architecture review triggered.

## 7. Standing metrics (this audit)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (audit only)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: 0
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: 0
- MODES: 0 (found across all five mechanisms)
- BRIDGES: 0 (found)
- HANDLERS: 0 (new task-specific; found)
- SEMANTIC CASES: 0

**Verdict: ARCH-AUDIT-COMPLETE.**
