# TNN-2 Next-Generation Preregistration

Date: 2026-09-30. Status: PREREG-FROZEN.
Governance: Micah's Core Freeze workflow (BUILD GENERATION → FREEZE → SEALED ADVERSARIAL TEST → ROOT-CAUSE ANALYSIS → NEXT GENERATION).
Root-cause basis: `ed38121d4` (ROOT-CAUSE-ANALYSIS-COMPLETE).

## 1. Mandate

Build TNN-2, the next architecture generation addressing the three
shared architectural gaps identified in the CORE-FREEZE-TNN1
root-cause analysis. All five failure clusters (FW3/W3 arithmetic,
FW7/W7 planning, FW8/W8 novel utterance, FW9/W9 relational DAG,
FW6/W6 degenerate inquiry) trace to failures of generation: TNN-1
is a competent retrieval and standing machine that cannot construct
novel executable structure at runtime.

## 2. The three changes

### Change 1: One executable graph type, constructed at runtime

**Problem:** The miss path (`ev_query` → `mp_run`) has exactly three
fixed plan templates. The approved EXECUTE 4-op ISA (MOVE, BRANCHEQ,
INC, DEC) is dead code in the cognition path; its only callers are
test functions. Plans run through a different executor. Two graph
types, one dead.

**Change:** Integrate the MUL Rung B trial loop
(propose/execute/verify/promote) into the miss policy. On a miss,
the learner constructs a 4-op executable graph at runtime using
trial-based search, verifies it against the triggering observation,
and promotes it to persistent learner state on success. The fixed
plan templates are removed; all executable structure flows through
the single 4-op ISA via EXECUTE.

**Fixes:** FW3, FW8, FW9, half of FW7.

### Change 2: Close the miss-to-act loop in learner state

**Problem:** A miss (-2) creates no uncertainty state. The validated
inquiry mechanism (commit `18ed3331c`: 149 cognition lines, all bars
pass) exists only in the standalone build, never integrated. `ev_act`
is selection-only over POLICY_ROOT, but guide construction is called
only from test scaffolding, so POLICY_ROOT is always empty and
`ev_act` always returns its hardcoded 0 fallback. The constant
CHOICE 0 is structural.

**Change:** Integrate the `18ed3331c` inquiry build into TNN-2.
On a miss, create an UNCERTAINTY node in learner state, construct a
guide through the inquiry mechanism, and link it to POLICY_ROOT
using existing node and edge types. `ev_act` then selects over
learner-constructed guides. No new node types, no new edge types,
no new modes.

**Fixes:** FW6 and the other half of FW7.

### Change 3: Generic revision operator over executable graphs

**Problem:** `contradict_map` demotes standing but nothing
restructures an executable graph after a counterexample. MUL Rung B
proved construction works standalone but revision is 0/4. Shipping
construction without revision moves the failure inside the learner.

**Change:** Implement a generic revision operator over 4-op
executable graphs. On a counterexample to a promoted graph, the
operator restructures the graph: retarget a branch, adjust a loop
bound, insert or remove a step. This is distinct from standing
demotion. It operates on the graph topology, not on scalar
confidence values.

**Fixes:** The MUL Rung B 0/4 revision ceiling. Future-proofs
Change 1 against the next counterexample.

## 3. Integration sources

- Base: TNN-1 ACT-remediated source (`d3895083c9f8b5b0f82ac1c74b11eb2c90341059fcf9e37be30b9c085de0cc6b`, 1328 lines)
- Trial loop: MUL Rung B build (`a2223cc11`; propose/execute/verify/promote)
- Inquiry: standalone inquiry build (`18ed3331c`; 149 cognition lines)
- ISA: frozen 4-op (MOVE, BRANCHEQ, INC, DEC) + EXECUTE (approved per Micah's ruling; the two documented deviations remain recorded)

## 4. Architectural constraints (from Micah's rulings)

- No new opcodes. The ISA is frozen.
- No new modes, bridges, handlers, or task-specific semantic cases.
- One-System Rule: capability must arise from learner-created state, not new subsystems.
- The three changes must converge on one executable graph type, not create parallel machinery.
- Standing question for every line added: "Why can the existing general architecture not learn this behavior?"

## 5. Kill bars

- K-T2-1 (ordering): This prereg commit strictly precedes TNN-2 implementation. Verified by git merge-base --is-ancestor.
- K-T2-2 (single graph type): After integration, exactly one executor handles all runtime-constructed executable structure. The dead-code EXECUTE path and the separate `exec_plan` must converge; no two parallel executors remain.
- K-T2-3 (no fixed templates): The three fixed plan templates are removed. Every miss-path executable structure is constructed at runtime through the trial loop.
- K-T2-4 (inquiry integration): A miss creates an UNCERTAINTY node in persistent learner state; a guide is constructed and linked to POLICY_ROOT without test-scaffolding calls.
- K-T2-5 (act path live): `ev_act` returns a non-constant choice derived from learner-constructed guides in at least one non-test scenario. The hardcoded 0 fallback remains only for the empty-policy edge case.
- K-T2-6 (revision operator): A promoted executable graph is restructured (topology change, not standing change) after a counterexample in at least one test. Standing demotion alone does not satisfy this bar.
- K-T2-7 (determinism): All TNN-2 tests pass 3/3 byte-identical.
- K-T2-8 (toolchain): Pure Zag, safebin mandatory, zero Python.

## 6. Falsifiers

- F-T2-1: Any new opcode, mode, bridge, handler, or semantic case is added (ISA freeze violation).
- F-T2-2: Two parallel executors remain after integration (single-graph-type failure).
- F-T2-3: The trial loop is reimplemented as a fixed template menu (construction theater).
- F-T2-4: POLICY_ROOT is populated by test-scaffolding calls rather than the integrated inquiry mechanism.

## 7. Out of scope (deprioritized per root-cause analysis)

- The two EXECUTE deviations (code-literal budget, absent kind guard): documented, not failure causes.
- Standing/demotion tuning: already passes (FW1/FW2/FW4/FW5).
- Compression below the 1200-line ceiling: separate axis per Micah's ruling. Measure first, compress after capability is proven.

## 8. Success criteria

TNN-2 BUILD-PASS requires all of: K-T2-1 through K-T2-8 pass, no
falsifiers trigger, and the existing TNN-1 test suite (35/35) plus
the ACT suite (24/24) continue to pass without modification to
their assertions.

SURVIVES requires the full 11-step promotion pipeline per standing
governance.

## Verdict: TNN2-PREREG-FROZEN
