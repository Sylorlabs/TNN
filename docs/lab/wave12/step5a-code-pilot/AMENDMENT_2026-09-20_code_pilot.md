# Dated prereg clarification — CODE pilot (2026-09-20)

This amendment freezes BEFORE any repaired evidence is generated. The original
`PREREG_CODE_PILOT.md` is unchanged; where this note and the prereg disagree,
flag for Micah's retroactive review.

## PC3 intended plant (resolves the internal contradiction)

The prereg pins BOTH of the following:

- Section 4, C1: the op table includes `AND`/`OR`.
- Section 7: the planted omission "omits the AND/OR discriminating contexts",
  tied to an eager-vs-short-circuit tie-break selecting `eager`.

These two together only make sense under one reading: **C1 introduces the
AND/OR operators themselves (eager value logic, exact-op identification, like
the other C1 operators), while the C4 scaffold — which teaches the
eager-vs-short-circuit distinction — deliberately omits the branch contexts
that discriminate eager from short-circuit evaluation.** The disclosed
tie-break then selects the `eager` candidate; the C4 K3 variants (which are
exactly the omitted discriminating contexts) must fire, ≥2/10. This is the
plant the checker will verify, and it is the reading the repaired build
implements.

The words "AND/OR discriminators" in section 7 therefore refer to
eager-vs-short-circuit discriminating *contexts* in C4 (e.g. `ANDO` with a
`NONE` operand under a live guard), not to the `AND`/`OR` *operators* in C1.
The C1 operators stay; only the C4 contexts are omitted. The "C4" label in
section 7 is the curriculum stage number (C4 = `IFZ` + short-circuit
contexts), not the old implementation's stage number.

## C11 invariant Q&A (concrete interpretation, frozen here)

Section 12 pins C11 as "invariant questions machine-generated from the REAL
`st_memory_core` guard table". The repaired build implements this as:
questions are `(op, condition)` pairs over the real guard semantics —
`KILL`/`STRENGTHEN`/`EVIDENCE`/`FORCE_PIN`/`ADD`/`JUSTIFY` crossed with
conditions (pinned, force-pinned, core region, dead slot, bad strength, bad
code, duplicate cite, trainer-only caller). The answer is the exact refusal
code the real guard table emits (`0`, `101`, `102`, `103`, `122`, `123`,
`126`, `127`). The learner induces the mapping by elimination over a
disclosed space (true table / always-allow / pin-blind). The guard table
itself is not modified, and the learner's answers are audited to its own
stage-11 ledger slot. During C11 the pilot counts ledger ops touching
constitution slots 0/1 (the MA1 CORE slots) and the checker requires exactly
zero — that is the C11 refusal probe.

## C12 path-trace predicate (concrete interpretation, frozen here)

Section 12 pins C12 as "path-trace predicate check". The repaired build
implements this as: episodes are `(program, predicate)` pairs; the learner
simulates the program's full execution path with locked C1–C10 rules,
recording a compact event trace (loop-body executions, branch directions)
plus final state and fault flag, then evaluates the predicate over that path.
Predicates: loop-body-runs, then-branch-taken, path-faults,
`r7≠0`-at-end, loop-body-runs-≥3, both-branches-taken. Hypothesis space:
correct event-based check / inverted verdict / final-state-only
approximation. The oracle is the instrumented world machine (the same
`semantics.zag` the other stages use), never exposed to the learner.

## C1 operator space (frozen reading)

Section 4's "arithmetic/comparison = exact-op identification over the
committed op table" covers `LIT,ADD,SUB,MUL,DIV,MOD,NEG,EQ,LT,GT,AND,OR,NOT`.
The induced (non-exact) aspects stay what the old build had, now as one
product space: div/mod semantics (`trunc+fault` / `floor+div0→0` /
`trunc+div0→0`) × comparison semantics (`signed` / `unsigned` / `≤`-style).
`AND`/`OR`/`NOT`/`NEG` and the arithmetic ops are exact. The
`{short_circuit, eager}` hypothesis space in section 4 attaches to C4's
`ANDO`/`ORO` (the short-circuit contexts), not to C1's `AND`/`OR`.

## Amendment procedure

Any further deviation discovered during the repair will be documented in a
new dated amendment BEFORE the evidence that depends on it is generated.
No evidence in this repair predates this amendment.

— repair agent, 2026-09-20. Flagged for Micah's retroactive review.
