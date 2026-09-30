# PREREG: GENEXEC2 (Learner-Authored Executable Semantics, clean wave)

Date: 2026-09-30.
Status: FROZEN. Committed before any implementation, build, or run.
Lane: highest-priority frontier (F1). Clean lineage; the voided genexec_proto wave is not used.

## 0. Amendment A1 (2026-09-30, before any implementation)

The P1/P2 op sets are restricted to arithmetic/stack operations only:
{PUSH, IN0, IN1, ADD, SUB, MUL, DIV, MOD, NEG, DUP, DROP, SWAP, OVER}.
LT, EQ, GT are REMOVED from P1/P2. They remain available ONLY in the
P3 probe family.

Justification: With compare ops in P1, |x| is computable straight-line
via a sign trick (x * (1 - 2*(x<0)), ~10 ops), which would let P1 solve
T1 and prevent P3 (conditional assembly) from ever running. Removing
compare ops from P1 makes straight-line |x| impossible (the input sign
cannot be reified without comparison), so T1 genuinely exercises P3.
This is a modular design choice (arithmetic in P1, conditionals in P3),
not a task-specific restriction. T3 (parity) still works via MOD.

## 0b. Amendment A2 (2026-09-30, before any implementation)

T4 is changed from y=16x+15 to y=||x|-2| (nested absolute value),
x in -6..6 (13 train episodes).

Justification: 16x+15 is affine, so P1 can find a short straight-line
program ([IN0, PUSH 8, MUL, PUSH 4, MUL, PUSH 1, SUB], 9 ops), which
means the CALL-based solution is merely shorter, not required. The
ablation (K-D2) would not destroy correctness. By contrast, ||x|-2|
has three kinks (at x=-2, 0, 2) and requires conditional logic that P1
cannot express (no compare ops) and P3 cannot assemble (single probe
handles at most one kink). It is solvable only via P2 with two nested
CALLs to ABS: [IN0, CALL ABS, PUSH 2, SUB, CALL ABS]. This makes the
library provably load-bearing for T4, strengthening C0-D.

T4 now tests repeated (nested) application of the same invented
fragment. T5 (|x|+|x-2|) tests hierarchical composition (two CALLs
combined with ADD). Both require ABS from T1.

K-D1 is updated: T4's program must contain >= 2 CALLs to ABS (not STEP).
T5's program must contain >= 2 CALLs to ABS (unchanged).

## 0c. Amendment A3 (2026-09-30, before final implementation run)

Beam search scoring is clarified: the *success criterion* is exact-match
count (a program is a solution iff it matches all train episodes). For
*beam selection* (which candidates to retain), candidates are ordered
lexicographically by (exact_match_count desc, total_absolute_error asc,
program_length asc, program_bytes asc). The total_absolute_error term
provides gradient in the sparse-reward regime where many prefixes have
zero exact matches; it does not change the definition of a solution.

Beam width is increased from 200 to 500 to retain more diverse prefixes
through the sparse early depths. Max lengths unchanged (12 for P1,
10 for P2).

## 1. Objective

Build the first L3 candidate under the refined mandatory Criterion 0
(C0-A through C0-D, 2026-09-29). The learner must construct persistent
executable programs whose semantics reside in learner-created state,
executed by a generic interpreter containing no task-specific semantic
case. The same construction machinery must solve qualitatively different
tasks and reuse invented structures for later cognition.

This wave does NOT copy the voided prototype. Conceptual direction only:
generic stack VM, learner-created instruction sequences, generic
construction machinery (beam search, probe-based conditional assembly,
library promotion with CALL).

## 2. Substrate (authored; generic execution machinery only)

A stack-based virtual machine. A program is a sequence of (op, arg)
pairs. The interpreter implements exactly these generic operations:

- PUSH k: push constant k (k in -9..9)
- IN0, IN1: push input[0], input[1]
- ADD, SUB, MUL: pop b, pop a, push a+b / a-b / a*b
- DIV, MOD: pop b, pop a, push (b==0 ? 0 : a/b) / (b==0 ? 0 : nonneg a mod b)
- NEG: pop a, push -a
- DUP, DROP, SWAP, OVER: standard stack manipulation
- LT, EQ, GT: pop b, pop a, push (a<b ? 1 : 0) etc.
- JZ addr, JNZ addr, JMP addr: pop condition (for JZ/JNZ); set pc
- CALL f: invoke library fragment f (push return address; jump to fragment)
- RET: return from fragment

Execution: pc starts at 0; halt when pc past end or step limit reached.
Result is top of stack (0 if empty). A return stack supports CALL/RET.

The interpreter contains NO operation whose meaning is task-specific.
There is no ABS, no STEP, no DOUBLE, no MOD3, no COUPLED, no COND
operator. JZ is a generic conditional jump, not a task semantic case.
The forbidden pattern (switch on invented-object type with
researcher-written semantics per case) does not appear.

## 3. Learner state (learner-created persistent state)

- lib: ordered list of named fragments. Each fragment is an instruction
  sequence created by the learner and promoted after solving a task.
  Fragments are callable via CALL. The library grows monotonically
  (cap 8, FIFO eviction; eviction events are logged).
- best: current best program for the active task.

The semantics of STEP (2x+1) and ABS (|x|) live in lib as instruction
sequences. They are not in source. Source-audit question "where are the
semantics of ABS implemented?" must be answered: "in learner state (lib
entry created at runtime); the source contains only the generic
interpreter and generic construction machinery."

## 4. Construction machinery (authored; generic, not task-specific)

Per task, the learner runs these phases in order. All search is
deterministic (fixed op order, tie-break by shorter length then
lexicographic byte order). No randomness.

Phase P1 (straight-line beam search):
  Beam over ops {PUSH, IN0, IN1, ADD, SUB, MUL, DIV, MOD, NEG, DUP,
  DROP, SWAP, OVER} (see Amendment A1; no compare, no jumps, no CALL).
  Max length 12. Beam width 200. Score is exact-match count on train
  episodes. Returns best program.

Phase P2 (library call composition):
  If lib is non-empty, beam over P1 ops plus {CALL f for f in lib}.
  Max length 10. The learner may compose CALLs with straight-line ops.
  If P2 finds an exact solution shorter than P1's best exact solution,
  P2's is selected. Otherwise P1's stands.

Phase P3 (failure-driven conditional assembly):
  If no exact solution yet, analyze the best program's failures.
  For each probe in a fixed generic family:
    probes are [IN0, PUSH k, LT], [IN0, PUSH k, GT], [IN0, PUSH k, EQ],
    [IN1, PUSH k, LT], [IN1, PUSH k, GT], [IN1, PUSH k, EQ],
    for k in -4..4, in fixed order.
  A probe is useful if it separates failing episodes from passing
  episodes (all fail have probe=1 and all pass have probe=0, or vice
  versa; both subsets non-empty).
  For the first useful probe (fixed order):
    synthesize body_T on the probe=1 subset via P1 (on subset episodes)
    synthesize body_F on the probe=0 subset via P1
    if both bodies are exact on their subsets, assemble:
      [probe][JZ L_else][body_T][JMP L_end][L_else:][body_F][L_end:]
    where L_else and L_end are computed addresses.
  The assembled program is the solution. Its length exceeds the P1
  bound; it was not selected from a bounded menu but assembled from
  separately synthesized parts.

Promotion:
  If a task is solved exactly, its solution program is appended to lib
  with a generated name (e.g., FRAG0, FRAG1). The white-box trace logs
  the creation (which phase, which probe if P3, which CALLs if P2).

Notes on scope:
  P1 alone is generic program synthesis over a bounded space. The
  L3-relevant construction is P2 (growing library, unbounded composition
  space) and P3 (assembled conditional whose full form was never
  enumerated). T2 is the weakest family (P1 synthesis); T1, T4, T5
  exercise genuine construction.

## 5. Frozen task sequence (evaluator-designed; not learner cases)

The learner receives (input, target) episodes only. It is not told task
names or families. Tasks run in fixed order; lib persists across tasks.

- T0: y = 2x+1, x in 0..8 (9 train). Warmup. Expected: P1 solves.
  Promotes STEP.
- T1: y = |x|, x in -8..8 (17 train). Conditional. Expected: P1 fails
  (no straight-line program with these ops computes |x| exactly);
  P3 solves via probe [IN0, PUSH 0, LT]. Promotes ABS.
  Held-out: x in -12..12 excluding train (extrapolation check).
- T2: y = x mod 3, x in 0..16 (17 train). Periodic. Expected: P1 solves
  via [IN0, PUSH 3, MOD].
- T3: y = 1 if (a+b) even else 0, a,b in 0..4 (25 train). Relational.
  Expected: P1 solves (must relate both inputs).
- T4: y = ||x|-2|, x in -6..6 (13 train). Repeated (nested).
  Expected: P1 fails (no compare; three kinks); P3 fails (single probe
  cannot handle three kinks); P2 solves via two nested CALLs to ABS:
  [IN0, CALL ABS, PUSH 2, SUB, CALL ABS]. The program must contain at
  least 2 CALLs to ABS. This tests repeated application structure.
  Without the library, T4 is unsolvable.
- T5: y = |x| + |x-2|, x in -4..8 (13 train). Hierarchical composition.
  Expected: P2 solves via CALL ABS twice within an ADD. The program
  must contain at least 2 CALLs to ABS. Tests reuse of T1's invention.

Adversary-designed family (C0-C):
  A sixth family (T6) is RESERVED for the independent adversary (A1)
  after mechanism freeze. The adversary will design a sealed world
  requiring a materially different structure. This wave's BUILD-PASS
  covers T0-T5 only. Full C0-C satisfaction requires the adversary step
  in the promotion pipeline. This prereg explicitly does not claim C0-C
  is complete.

## 6. Kill bars (numbered; all must pass for BUILD-PASS)

C0-A (runtime-defined semantics):
- K-A1 (source audit): an auditor searches the committed source for
  identifiers ABS, STEP, DOUBLE, COUPLED, COND (as semantic cases),
  and for switch/if-chains dispatching on invented-object type with
  task-specific semantics. Must find none. The only conditional
  control is the generic JZ/JNZ/JMP. PASS if clean.
- K-A2 (state residence): the committed trace shows STEP and ABS as
  lib entries with their full instruction sequences, created at
  runtime (with timestamps/phase logs). Their semantics are not in
  source. PASS if demonstrated.

C0-B (open structural form):
- K-B1 (growth): T1's assembled program length exceeds the P1 max
  length (12), proving it was not selected from the bounded P1 menu
  but assembled. PASS if len(T1_prog) > 12.
- K-B2 (incremental topology): the trace shows T1's program was built
  by splicing three separately synthesized parts (probe, body_T,
  body_F), not chosen whole. PASS if trace shows three-part assembly.

C0-C (multiple unforeseen forms; partial this wave):
- K-C1: T1 (conditional), T2 (periodic), T3 (relational) each solved
  exactly by the SAME frozen machinery with no source edits between
  tasks. PASS if all three exact.
- K-C2: T4 (repeated) and T5 (hierarchical) each solved exactly, with
  the required CALL counts (see K-D1). PASS if both exact.
- Note: full C0-C (adversary-designed T6) is deferred to promotion
  step 9. This bar is marked PARTIAL in the result.

C0-D (cognitive reuse):
- K-D1 (reuse constructed): T4's program contains >= 2 CALLs to the
  ABS fragment; T5's program contains >= 2 CALLs to the ABS fragment.
  PASS if both hold (verified from committed program dumps).
- K-D2 (ablation): with CALL disabled (lib present but CALL ops
  removed from P2), re-run T4 and T5. Both must FAIL to reach exact
  (or the best accuracy must drop by >= 30 percentage points).
  This proves the invented structures are load-bearing, not
  decorative. PASS if ablation destroys the advantage.

Persistence:
- K-P1: lib entry for ABS (from T1) is the same entry used by T5
  (verified by fragment bytes, not re-synthesized). PASS if byte-match.

Correctness:
- K-T0 through K-T5: each task solved exactly on train episodes
  (100%). T1 additionally exact on held-out extrapolation set.
  PASS if all exact.

Determinism and purity:
- K-DET: 3 full runs, byte-identical stdout (cmp), exit 0.
- K-PURE: pure Zag (build, runs, analysis via shell tools only);
  no Python at any stage including /tmp scratch; no em dash bytes
  in committed docs (byte check).

BUILD-PASS iff all kill bars pass, except K-C1/K-C2 note the PARTIAL
scope for full C0-C (adversary T6 pending). Any other failure is
BUILD-FAIL with the failing bar named.

## 7. Honest limitations (frozen)

- Programs are linear instruction sequences with CALL; not general
  graphs. The call structure forms a DAG. True cyclic graphs and
  self-recursive fragments are future work.
- T4 tests repeated application (STEP^4), not true recursion.
- Probes are input-only; probes on intermediates are future work.
- P1 is bounded synthesis; the open-endedness comes from P2/P3
  assembly and library growth.
- T2 (periodic via MOD) is generic synthesis; the L3 weight rests on
  T1, T4, T5.
- C0-C is PARTIAL until the independent adversary designs T6.
- Classification target: L3 candidate. SURVIVES requires the full
  11-step pipeline including adversary T6, OOD, transfer, and
  integration checks.
