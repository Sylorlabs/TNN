# PREREG: A1-Continued Adversary Methodology (frozen before target results)

Date: 2026-09-30.
Status: FROZEN. Committed before the F1 genexec2 builder reports and before
any F1 implementation is examined beyond the frozen prereg
(`docs/lab/research-lead/overnight-20260928/genexec2/PREREG_GENEXEC2.md`
plus amendment A1). The F2 autonomous-scientist builder has no prereg yet;
its attack methodology is stated here as a standing kill condition.

Lane: frontier architecture adversary (A1-continued). Pure Zag for all
attack code. No Python at any stage. No em dash bytes in committed docs.

## Target 1: F1 genexec2 (prereg frozen, implementation in progress)

The builder claims L3 candidacy under Criterion 0 with construction
machinery P1 (bounded beam synthesis), P2 (library CALL composition), P3
(failure-driven conditional assembly from a fixed 54-probe family into a
single if-then-else template). Three attacks are preregistered below.
Each names its exact procedure and its kill criterion. ATTACK-SUCCEEDS
means the criterion is met; ATTACK-FAILS means it is not.

### AX-GX1: probe-menu equivalence (C0-B)

Procedure: after the builder's result commit lands, write an independent
pure-Zag program from the prereg spec only (no builder code). The program
enumerates the fixed probe family (54 probes: [IN0/IN1, PUSH k, LT/GT/EQ],
k in -4..4, fixed order) and, for each probe that separates T1 train
episodes, beam-searches body_T/body_F on the subsets with the P1 op set
and bounds, then assembles [probe][JZ][body_T][JMP][body_F] exactly as
specified. Compare its T1 program byte-for-byte with the builder's
committed T1 program.

Kill criterion: byte-identical match. Rationale: P3's output space is the
finite family {probe} x {P1 body_T} x {P1 body_F} (54 x bounded x bounded).
If an independent enumerator over that family reproduces the builder's
program exactly, then P3's "assembly" is selection from a finite
researcher-bounded family of complete candidate answers, and C0-B
("no finite list of complete candidate answers") fails for the
conditional construction. The builder's "assembled, not selected" defense
is void by the A1 precedent on H-CAUSALEXP-CONSTRUCT: a deterministic
traversal of a finite family with a filter is selection, however guided
the traversal.

ATTACK-SUCCEEDS iff byte-identical. Anything else is ATTACK-FAILS.

### AX-GX2: template boundary via sealed nested-conditional family (C0-B/C0-C)

Design principle (frozen here; instances designed AFTER the F1 mechanism
freeze, per C0-C, and sealed from the builder): T6 requires a
two-level data-dependent branch, expressible in the frozen op set
(JZ/JNZ/JMP available) but NOT expressible in P3's single-template form.

Concretely: P3 assembles exactly one probe, one JZ, and two bodies, and
bodies are P1-synthesized (straight-line arithmetic/stack ops only, no
jumps, no CALL). Therefore no P3 output can contain a branch inside a
branch arm. P2's top level is straight-line plus CALLs; a CALL applies a
whole fragment to the input and cannot be made data-dependent without a
top-level branch, which P2 cannot emit. Hence a task whose correct
program needs two nested data-dependent branches is outside the
builder's reachable form family.

T6 will be a piecewise task with three segments (two thresholds on one
input), e.g. y = f1(x) for x < a, y = f2(x) for a <= x < b, y = f3(x)
for x >= b, with f1/f2/f3 distinct straight-line functions and
thresholds not coinciding with any T1-T5 probe. Instances are generated
after freeze; the builder never sees them.

Kill criterion: the frozen learner (no source edits, library as left by
T0-T5) fails to reach exact on T6 train episodes, while a hand-written
nested-conditional program in the same op set reaches exact. Then the
structural form available to the learner is researcher-bounded to a
single if-then-else template, C0-B fails (the "open structural form"
collapses to one template), and any L3 claim is KILLED.

ATTACK-SUCCEEDS iff the frozen learner is not exact on T6 and the
reference nested program is exact. Otherwise ATTACK-FAILS.

Note: the builder's prereg explicitly marks C0-C PARTIAL pending this
adversary step, so AX-GX2 executes the preregistered plan rather than
ambushing it.

### AX-GX3: source audit of conditional semantics (C0-A)

Procedure: search the committed F1 source for the P3 assembly template.
Record the exact code that emits [probe][JZ L_else][body_T][JMP
L_end][L_else:][body_F][L_end:] and the fixed 54-probe enumeration.

Kill criterion (partial): if the branch STRUCTURE of every conditional
the learner can ever produce is fixed by this template (one probe, one
JZ, two straight-line arms, fixed emission order), then the dominant
semantic content of e.g. ABS ("if x<0 then -x else x") resides in a
researcher-authored construction template, not in learner-created state.
The learner's contribution is slot-filling: which of 54 probes, which
two bounded bodies. C0-A ("semantics must reside in learner-created
persistent state; source contains only generic execution/construction
machinery") then fails for the conditional form: a dedicated
conditional-construction procedure is a dedicated semantic case for the
invented representation's form, even though it is not task-specific.
Generic JZ in the interpreter is fine; a source template that only ever
emits single if-then-else programs is not generic construction machinery.

Verdict levels: CLEAN (no such template; conditionals emerge from
generic composition ops), PARTIAL-FAIL (template exists; semantic
authority over conditional form stays with researcher), combined with
AX-GX1/AX-GX2 for the overall L3 verdict.

## Target 2: F2 autonomous scientist (no prereg yet; standing kill condition)

When the F2 builder reports, the attack applies the Program 3 kill
condition: enumerate the effective candidate experiment set implied by
the builder's construction procedure (primitive set, max depth/length,
enumeration order, selection criterion, all as committed). If any
reportedly "constructed" experiment maps directly to one entry of that
finite researcher-enumerated candidate list, DOWNGRADE the autonomy
claim to L2 (bounded search with hypothesis filtering, per the
H-CAUSALEXP-CONSTRUCT precedent). Genuine construction requires the
experiment's form to be underdetermined by the researcher's enumeration:
hypothesis-GUIDED generation (candidate proposals derived from
hypothesis structure), not hypothesis-FILTERED enumeration.

A separate attack prereg will be committed before examining the F2
implementation, once its prereg exists.

## Determinism and purity

All attack programs: 3/3 byte-identical runs, exit 0, zero stderr,
md5 recorded. Pure Zag only: build, runs, and analysis via shell tools
only. No Python at any stage including /tmp scratch. Byte-check for
em dash in committed docs.

## What is NOT claimed here

This prereg freezes attack methodology and kill criteria. It does not
prejudge the F1 result: if the builder's implementation differs
materially from its prereg in ways that defeat these attacks, the
attacks FAIL honestly and that is recorded. The sealed T6 instances are
not designed here; designing them now would violate the after-freeze
requirement.
