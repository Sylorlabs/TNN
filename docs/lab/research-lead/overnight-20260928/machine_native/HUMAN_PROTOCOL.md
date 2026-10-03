# Human Protocol for MNSTRESS-1 Machine-Native Advantage

## Purpose

This protocol defines how to run the MNSTRESS-1 benchmark with human contestants, for future comparison against the machine-native engine. No human scores exist yet. This protocol is prepared in advance; do not fabricate human performance data.

## Task

The human contestant must demonstrate the same knowledge-integration capabilities as the MNSTRESS-1 engine, on a scaled-down but structurally identical task.

### Scale

- 30 entities
- 80 claims (attribute and relationship)
- 8 contradictions (contested slots, both values retained)
- 2 corrections (delayed, must propagate through derived beliefs)
- 1 withdrawal scenario (claim removed, dependent beliefs recomputed)

### Time Limit

45 minutes, strict. The contestant may not exceed the limit. Unfinished queries are scored as failures.

## Conditions

Two conditions, administered separately:

### Condition A: Unaided

- No notes, no paper, no tools.
- The contestant must hold all claims, provenance, contradictions, corrections, and derivations in memory.
- Queries are presented verbally or on screen, one at a time.
- The contestant responds verbally or in writing.

### Condition B: Human-with-tools

- Blank paper allowed (no pre-written notes).
- The contestant may write down claims, draw diagrams, and take notes during the 45 minutes.
- No electronic tools, no calculators, no external references.
- Queries are presented as in Condition A.

## Identical Observations and Scoring

Both conditions use:

- The same 30 entities, 80 claims, 8 contradictions, 2 corrections, 1 withdrawal.
- The same query batteries, scaled to the 30-entity world:
  - Q1: slot value queries
  - Q2: provenance queries (which source, which claim)
  - Q3: contradiction queries (both values, neither collapsed)
  - Q4: temporal queries (supersession order)
  - Q5: correction propagation (old vs new derived beliefs)
  - Q6: withdrawal impact (dependent beliefs after removal)
  - Q7: load-bearing claims (which claims support which beliefs)
- The same scoring rubric as the machine engine:
  - Each query: correct or incorrect (no partial credit).
  - Provenance must be exact (source ID and claim ID).
  - Contradictions: both values must be reported; collapsing to one is a failure.
  - Corrections: old (superseded) and new (active) derived values must both be identified.
  - Withdrawal: recomputed beliefs must match independent recomputation.

## Explicit Statement

No human contestants have completed this protocol. No human scores exist. Any future comparison must use real contestants completing the same frozen benchmark, under the conditions above. Do not claim human or machine superiority without such data.
