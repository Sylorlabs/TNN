# Architecture Ruling: Protected Core ISA Boundary

Date: 2026-09-30 (late). Source: Micah's direct ruling.
Status: FROZEN ARCHITECTURE RULING.

## The ISA boundary

The protected core may contain a SMALL, FROZEN, domain-neutral
computational basis comparable to a CPU ISA.

Acceptable core primitives (machinery, not intelligence):
ALLOC, READ, WRITE, LINK, COPY, COMPARE/EQ, basic arithmetic
such as ADD, BRANCH, APPLY/EXECUTE, generic state/register
operations.

These do not tell TNN what to think. They give it machinery
with which learner-created structures can think.

## Frozen rule

No core operation may encode a target-domain regularity detector.

Not acceptable as protected semantic operations:
FIND_POLYNOMIAL_ORDER, DETECT_NEGATION, BUILD_CAUSAL_RULE,
LEARN_PROCEDURE, FIND_THRESHOLD, MAKE_CONDITIONAL,
or benchmark/domain equivalents.

Those already contain cognitive solutions.

## Consequences

1. Remove finite-difference regularity detection from CAM-1
   core intelligence. Prefer trial/compositional discovery
   using learner-created structures.

2. Do NOT add MUL merely because FW3 requires multiplication.
   Test whether the learner can construct and persist MUL
   from the generic computational basis. That would be
   L3-ish evidence.

3. Freeze the computational basis deliberately. Do not grow
   it one benchmark at a time. SUB acceptable as ISA-level
   arithmetic, but the same freeze applies.

4. If CAM needs subtraction/differences, the learner must
   construct the required computation using generic primitives
   unless a lower-level primitive is justified as truly
   domain-neutral.

## Approved package

The integration coordinator's package (A1-A12) is APPROVED
with the above boundary added:
- 10 generic core operations
- MISS_POLICY register
- POLICY_ROOT register
- generic sentinel/state machinery
- trial-based P-DEP (finite-difference OUT)
- edge-derived standing
- zero modes/bridges/handlers

## Confirmed directions

- CLA-2 consolidated direction: APPROVED as primary.
- Procedure and causal rule: remain on the path toward being
  the SAME executable graph type with different evidence
  and lifecycle edges, not separate engines.
- FW1-FW9: APPROVED as sealed evaluator assets.
- Construct-and-apply: APPROVED as major frontier.
- ACT: APPROVED as learner-state-driven generic action
  selection.
- CLA-1/CLA-2 primary over contlearn2 unless the
  discriminating comparison says otherwise.

## Architectural goal

"A tiny general machine for cognition whose intelligence is
increasingly in what it builds, not in how many cognitive
subsystems humans wrote."

## Governance: worker toolchain guard

Five accidental Python invocations in one cycle is a
process-system problem. Before each worker begins:
- verify allowed toolchain
- remove python/python3 and other forbidden interpreters
  from that worker's PATH where technically possible
- workers must use Zag for any computational research
  operation
- if a forbidden executable is invoked, that research
  worker's current scientific wave is automatically
  PROCESS-FAIL and must be cleanly re-frozen if its
  result matters
