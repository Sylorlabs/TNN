# F1 Prereg Review: GENEXEC2 Criterion 0 Compliance

Date: 2026-09-30.
Reviewer: F1 Prereg Reviewer (independent).
Scope: Review only. The prereg is frozen; this review does not modify it.
Prereg commits: c4423dabd (initial), 35fbf0f9c (A1), 787066b60 (A2).
All three precede any implementation (verified via git log).

## Verdict: REVIEW-COMPLETE with GAPS FOUND

The prereg explicitly addresses C0-A, C0-C (as partial), and C0-D with
numbered kill bars. It has a substantive gap on C0-B regarding the
fixed 54-probe family. It does not fully rule out the
H-CAUSALEXP-CONSTRUCT failure modes. Details below.

## C0-A: Runtime-defined semantics: ADDRESSED (strong)

K-A1 (source audit): explicit kill bar. Auditor searches for ABS, STEP,
DOUBLE, COUPLED, COND identifiers and switch/if-chains dispatching on
invented-object type with task-specific semantics. PASS if clean.

K-A2 (state residence): committed trace must show STEP and ABS as lib
entries with full instruction sequences, created at runtime with
phase logs. Semantics not in source.

Assessment: Both bars are explicit and falsifiable. The prereg states
the source-audit question ("where are the semantics of ABS
implemented?") and the required answer ("in learner state"). Strong.

## C0-B: Open structural form: GAP FOUND

K-B1 (growth): T1 program length must exceed P1 max length (12).
K-B2 (incremental topology): trace must show three-part assembly
(probe, body_T, body_F), not whole selection.

Gap: The P3 probe family is fixed and finite. Section 4 defines probes
as [IN0, PUSH k, LT], [IN0, PUSH k, GT], [IN0, PUSH k, EQ], [IN1, PUSH
k, LT], [IN1, PUSH k, GT], [IN1, PUSH k, EQ], for k in -4..4, in fixed
order. That is 6 templates times 9 k values = 54 probes, researcher
defined, researcher ordered.

P3 selects "the first useful probe (fixed order)". The output family
is therefore {54 fixed probes} x {P1-synthesized body_T} x
{P1-synthesized body_F} through a single fixed
[probe][JZ][body_T][JMP][body_F] template.

This is structurally similar to the H-CAUSALEXP-CONSTRUCT disguised
menu: a finite researcher-enumerated family (there: 1364 sequences;
here: 54 probes times bounded synthesis spaces) with a
researcher-defined selection order ("first" in fixed order).

The prereg's defense (K-B1, K-B2) addresses assembly vs whole-program
selection, but does NOT include a kill bar for "an independent
enumerator over the 54-probe family cannot byte-reproduce the T1
program." A1-Continued's preregistered AX-GX1 attack is designed to
test exactly this gap. The prereg should have anticipated it.

Severity: Moderate. The bodies are synthesized on data-dependent
subsets (not pre-enumerated), which distinguishes this from the pure
H-CAUSALEXP-CONSTRUCT case. But the probe selection itself is
filter-only over a fixed menu, and the prereg does not rule out the
disguised-menu reading.

## C0-C: Multiple unforeseen forms: ADDRESSED (explicitly partial)

K-C1: T1 (conditional), T2 (periodic), T3 (relational) solved by the
same frozen machinery, no source edits. K-C2: T4 (repeated), T5
(hierarchical) solved with required CALL counts.

The prereg explicitly marks full C0-C as PARTIAL: "A sixth family (T6)
is RESERVED for the independent adversary (A1) after mechanism freeze.
This wave's BUILD-PASS covers T0-T5 only."

Assessment: Honest scoping. Not a gap; the limitation is declared
upfront. The adversary step is correctly deferred to the promotion
pipeline.

## C0-D: Cognitive reuse: ADDRESSED (strong)

K-D1 (reuse constructed): T4 and T5 programs must each contain >= 2
CALLs to the ABS fragment (verified from program dumps).

K-D2 (ablation): with CALL disabled, T4 and T5 must fail to reach
exact (or accuracy drops >= 30pp). Proves invented structures are
load-bearing.

K-P1 (persistence): ABS lib entry from T1 must byte-match the entry
used by T5 (not re-synthesized).

Assessment: Three complementary bars (construction, ablation,
persistence). Strong. Amendment A2 strengthens this by changing T4 to
||x|-2|, which is unsolvable without the library (P1 cannot express
it, P3 cannot assemble it with a single probe).

## H-CAUSALEXP-CONSTRUCT failure modes

1. Finite enumeration with researcher order: NOT FULLY RULED OUT.
   See C0-B gap above. The 54-probe fixed order plus "first useful"
   selection mirrors the "first disagreeing in lexicographic order"
   pattern. The prereg relies on K-B1/K-B2 to distinguish assembly
   from selection, but lacks an explicit anti-enumerator bar.

2. Fixed depth bound: ADDRESSED. P1 max length 12 and P2 max length 10
   are explicit bounds, not hidden. The prereg claims open-endedness
   comes from P2 library composition (CALL enables unbounded nesting)
   and P3 assembly (length 29 exceeds P1 bound). Unlike
   H-CAUSALEXP-CONSTRUCT's hidden MAXD=5, the bounds here are declared
   and the unboundedness claim rests on a specific mechanism (CALL
   composition), which K-D1/K-D2 test.

3. Filter-only (no guidance): PARTIAL GAP. P3's probe selection is
   "first useful probe (fixed order)" - a filter, not guidance by
   hypothesis structure. The prereg does not explicitly distinguish
   this from H-CAUSALEXP-CONSTRUCT's filter-only approach. Mitigating
   factor: the bodies are synthesized (via P1 on data-dependent
   subsets), not selected from a pre-enumerated list. But the probe
   choice itself is unguided.

## Additional observations

- Amendment A1 (removing compare ops from P1) is well-justified: it
  prevents P1 from solving T1 via a sign trick, ensuring T1 genuinely
  exercises P3. This is a modular design choice, not task-specific
  tuning.

- Amendment A2 (T4 changed to ||x|-2|) strengthens C0-D by making the
  library provably load-bearing. Good.

- Honest limitations (Section 7) are thorough: linear programs not
  graphs, no true recursion, probes are input-only, P1 is bounded,
  T2 is weak, C0-C is partial. The prereg does not overclaim.

- The prereg does not claim C0-C is complete. This honesty is a
  strength, not a weakness.

## Gaps summary

1. C0-B: No explicit kill bar ruling out independent-enumerator
   reproduction of P3 programs from the fixed 54-probe family.
   (A1-Continued AX-GX1 will test this.)

2. Probe selection is filter-only ("first useful in fixed order")
   with no guidance mechanism; prereg does not explicitly address
   the filter-vs-guidance distinction from the H-CAUSALEXP-CONSTRUCT
   postmortem.

3. No gap on C0-A, C0-C (partial, declared), C0-D. All have explicit
   numbered kill bars.

## Recommendation to coordinator

The prereg is strong enough to proceed. The C0-B gap is real but is
exactly what the preregistered A1-Continued attacks (AX-GX1, AX-GX2,
AX-GX3) are designed to test. Do not weaken the prereg; let the
adversary do its job. If AX-GX1 succeeds (byte-identical reproduction
via independent enumerator), the L3 claim dies and the gap becomes a
kill. If it fails, the gap is closed by evidence.

The builder should not be asked to amend the prereg to address these
gaps pre-hoc; that would be moving the bar. The bars are frozen. The
adversary tests them.
