# Q4 Design: Learner-Constructed Explanatory Variables (Causal Stage 2)

Status: DESIGN ONLY. No implementation authorized. Prereg 1b72fdf45 frozen
before this design was finalized; all numbers and falsification criteria
below honor it. A future implementing worker files its own prereg
referencing these bars before writing any Zag.

## 1. Problem and L3 context

DDES is causal Stage 1: an authored hypothesis language plus guided
synthesis, and the DDES L3 gap analysis (678ea4162) ruled the lineage
terminal L2: it fails C0-A at five independent loci, plus C0-B, C0-C, and
C0-D. F2 constructs hypotheses but its contextual law used a
researcher-supplied K variable. No current TNN lane constructs an
explanatory variable the researchers did not supply and then reuses it.

Q4 tests exactly that. Sealed worlds hide the true cause as a function of
observables. The learner must posit a derived variable D, test it by
intervention, keep it in persistent state only if it earns its place, and
reuse it as a building block on a later world. If it can, that is
representational invention with reuse: the L3 core. If it cannot under
these frozen bars, the hypothesis is falsified for the tested
architecture (F1..F5 in the prereg).

## 2. World model

Each world exposes 6 binary observables X1..X6 and one binary outcome Y.
A hidden cause C = f(X1..X6) is computed by the sealed world; the learner
never observes C or f, only (x, y) pairs. Y = C deterministically.

The learner has two evidence channels:

- Passive: 8 samples (x, y) drawn with selection bias (see section 4).
- Interventional: SET Xi to 0 or 1 (do-operator) in any combination, then
  read Y. Phase 1 budget: 24 adaptive interventions. The learner chooses
  each intervention based on prior evidence.

The harness (not the learner) may query the sealed f on all 64 input
combinations to score true accuracy. The learner's data is limited to its
8 passive samples plus its 24 interventions.

## 3. Sealed families (functional descriptions, not code)

The independent adversary selects the Phase 1 family and the Phase 2
family after the implementation freeze. The five families below are
examples only; the adversary may invent new ones provided each is
expressible in the frozen composition language (section 5) with at most 7
operator nodes, and provided at least one family is materially different
in representational form from the others (per C0-C, functional test
descriptions, never implemented as dedicated cases):

- F-CONJ (conjunctive): C = X1 AND X2. Distractors X3..X6 carry no signal
  except the confounded X6 (section 4).
- F-XOR (exclusive): C = X1 XOR X2. Single observables carry zero signal;
  this family kills pure correlational positing.
- F-THRESH (thresholded sum): C = 1 iff (X1 + X2 + X3) >= 2. Expressible
  as (X1 AND X2) OR (X2 AND X3) OR (X1 AND X3): 5 operator nodes.
- F-MUX (conditional): C = X1 if X4 = 0 else X2. Expressible as
  (X1 AND NOT X4) OR (X2 AND X4): 4 operator nodes. Tests conditional
  structure, a representational form absent from the other families.
- F-NEST (hierarchical composition): C = (X1 AND X2) OR (X3 AND X4):
  3 operator nodes. Tests multi-component structure.

Expected baseline ceilings (the adversary verifies these on the sealed
realization before launch; they are properties of the families, not
tunable parameters):

- F-CONJ: best single observable true accuracy 0.75; D = X1 AND X2: 1.00.
- F-XOR: best single observable 0.50; D = X1 XOR X2: 1.00.
- F-THRESH: best single observable 0.75; sum-of-products D: 1.00.
- F-MUX: best single observable 0.75; multiplexer D: 1.00.
- F-NEST: best single observable 0.50; nested D: 1.00.

All satisfy KB1's requirement (D >= 0.95, best single <= 0.80).

Phase 2 family constraint: the Phase 2 hidden function must share a
subexpression with the Phase 1 true function (so reuse is possible in
principle) while being materially different overall. Example: Phase 1
F-CONJ with D1 = X1 AND X2 kept, Phase 2 C' = (X1 AND X2) OR X5, i.e.
D' = D1 OR X5. The adversary chooses the actual pairing post-freeze.

## 4. Passive confounded sample

Before interventions begin, the harness supplies 8 passive (x, y) pairs
with selection bias: 6 of the 8 satisfy X6 = Y, the remaining 2 are drawn
uniformly. X6 is a genuine observable; the sealed f never depends on X6;
over all 64 combinations X6 predicts Y at roughly chance. This tests that
positing is driven by interventional evidence, not by passive
correlation. A learner that posits D = X6 must discard it once
interventions dissociate X6 from Y (SET X6 = 1 with X1..X5 = 0 yields
Y = 0 on every family above).

## 5. Composition language (generic machinery, frozen)

Terminals: {X1, X2, X3, X4, X5, X6, 0, 1}.
Operators: {AND, OR, NOT, XOR} with standard Boolean semantics, evaluated
by a generic interpreter.

This set is fixed before the adversary selects families and may not be
extended (F4 treadmill guard). Every example family in section 3 is
expressible within it; the adversary must confirm expressibility of any
invented family within the 7-operator-node bound before launch. The
operators are generic machinery in the same sense as GENEXEC2 VM ops;
the specific combination, the decision to posit, and the reuse are the
learner's. No operator exists to rescue a particular family.

## 6. Phase 1 protocol: posit, test, keep

Step 1, baseline: compute B-OBS, the best single-observable predictor,
scored by accuracy on all evidence gathered so far (8 passive + k
interventions).

Step 2, candidate growth (incremental, generic): maintain a beam of at
most 32 candidate expression trees. Initialize with the 8 terminals.
Repeatedly extend: apply NOT to each candidate; apply AND, OR, XOR to
each ordered pair of candidates (with hash-consing to suppress
duplicates). Score each candidate by (accuracy on all evidence so far)
minus (0.02 per operator node). Keep the top 32. Record every operator
addition in the growth trace: parent expression ids, operator, resulting
id, and the evidence count at the time.

Step 3, adaptive intervention selection: after each growth round, score
each not-yet-used input combination by disagreement among the top 8
candidates (fraction predicting Y = 1, distance from 0.5 maximized... in
concrete terms: prefer combinations where the top candidates split most
evenly). Ties broken by lowest combination index. Execute the chosen
intervention, append (x, y) to the evidence, repeat until the 24 budget
is spent. This is uncertainty sampling with a deterministic tie-break;
the full sequence is reproducible.

Step 4, keep or discard: after the budget is spent, let BEST be the
argmax of (accuracy minus 0.02 per operator node) over the beam.
Let ACC-OBS be B-OBS accuracy on the same evidence. Keep BEST as a
derived variable D1 iff all of the following hold:

- accuracy(BEST) >= accuracy(B-OBS) + 0.15 (frozen keep margin);
- operator nodes in BEST <= 7;
- minimality: no other beam candidate is within 0.02 accuracy of BEST
  with fewer operator nodes.

Otherwise discard all candidates and record KEEP = 0. If kept, persist
D1 as an expression tree in learner state together with its growth
trace (section 7). The trace is the white-box record of D1's creation:
which interventions confirmed each subexpression.

## 7. Persistent state and construction trace format

Kept variables persist across phases in a variable library: each entry
holds an id, the expression tree (operator nodes with child pointers,
terminals as leaves), the Phase 1 accuracy, the evidence count, and the
growth trace. The growth trace is a chronological list of construction
events: (event index, operator, child ids, resulting id, evidence size
at construction, accuracy delta contributed). In Phase 2, kept variables
are available as atomic terminals for new candidate growth (section 8).
The library is learner-created persistent state; its contents are never
written by researcher code after initialization (initialization creates
an empty library only).

## 8. Phase 2 protocol: reuse and transfer (C0-D)

A new sealed world is presented (adversary-chosen family sharing a
subexpression with Phase 1's true function). The learner runs the same
posit/test/keep protocol with a fresh 8 passive samples and a fresh 24
intervention budget, except candidate growth may use kept library
variables as atomic terminals. This is the reuse mechanism: D1 can
appear as a building block inside a strictly larger expression
(e.g. OR(D1, X5)), which a frozen finite menu of Phase 1 candidates
cannot supply.

Ablation B-SCRATCH: the identical learner with the library disabled
(empty at Phase 2 start) runs the same Phase 2 world with the same
budget. Metric for each side: number of interventions until the current
best candidate's harness-scored true accuracy first reaches >= 0.95.
KB3 requires reuse_count <= 0.5 * scratch_count, with 24 recorded for any
side that never reaches 0.95 within budget.

## 9. Baselines

- B-OBS: best single observable predictor, scored by the harness over
  all 64 combinations. Expected ceilings per family are listed in
  section 3. This is the "no construction" control.
- B-MEM: truth-table memorizer. Records every observed (x, y) and
  predicts by exact match, defaulting to the majority label on unseen
  combinations. It has no compressed representation and no library, so
  it restarts from scratch in Phase 2 by construction. It controls for
  "the learner just memorized the interventions."
- B-SCRATCH: the learner itself with the Phase 2 library disabled
  (section 8). This isolates the causal contribution of reuse: same
  machinery, minus the kept variable.

## 10. Harness and scoring

The harness owns the sealed functions and the intervention counter. It
provides: the 8 passive samples per phase, intervention execution
((x) -> y), the full-64 truth table for scoring only (never shown to
the learner), and the run logs. Scoring:

- KB1: harness computes true accuracy of kept D1 over all 64
  combinations (>= 0.95 required) and of each single Xi (<= 0.80
  required for the max).
- KB2: harness-independent checks on the committed artifacts: operator
  node count <= 7, growth trace present with one event per operator
  addition, B-MEM Phase 2 behavior confirmed as restart-from-scratch.
- KB3: intervention counts from the run logs as defined in section 8.
- KB4: 3/3 byte-identical stdout, pure Zag at every stage, zero Python
  invocations, zero em dash bytes in all committed docs.

## 11. Worked example (F-CONJ, hypothetical run)

Phase 1 true function: C = X1 AND X2. Passive samples show X6 = Y in 6
of 8. B-OBS on passive evidence: X6 at 0.75. Growth begins from
terminals. Early interventions: the disagreement criterion favors
combinations splitting the beam; SET (X6=1, rest 0) returns Y = 0,
dissociating X6. Candidates containing X6 decay. By intervention 10 the
beam leaders involve X1, X2. Candidate X1 AND X2 reaches accuracy 1.0
on all evidence gathered; B-OBS (X1) sits near 0.75. At budget end:
accuracy(BEST) = 1.0 >= 0.75 + 0.15; operator nodes = 1 <= 7;
minimality holds (no 0-operator candidate within 0.02). KEEP = 1; D1 =
AND(X1, X2) persisted with its trace.

Phase 2 true function: C' = (X1 AND X2) OR X5. Reuse side grows
OR(D1, X5): 1 operator node over the atomic D1, found within a few
interventions once X5's relevance is sampled. Scratch side must
re-derive AND(X1, X2) before composing the OR, costing strictly more
interventions. KB3 compares the counts.

## 12. C0-B risk note (explicit, honest)

Beam search over expression trees bounded at 7 operator nodes is a
finite space, and a strict reader could call the beam a menu of
complete answers. Three counter-considerations are built into the
protocol, and the implementing worker must log evidence for each:

- Growth is incremental and traced: D1 is assembled one operator at a
  time, each addition scored and logged, not selected whole from a
  pre-enumerated list.
- Phase 2 open-ended composition: kept variables become atomic
  terminals for strictly larger expressions across phases, so the
  reachable structure class grows with the learner's history rather
  than being fixed at compile time.
- Adversary-selected families: at least one family is designed
  post-freeze with a representational form (e.g. conditional) the
  implementer did not optimize for.

If the implementing worker cannot produce the growth trace or the
Phase 2 strictly-larger composition, C0-B is not met and the L3 claim
fails even if KB1..KB3 pass numerically.

## 13. Integration notes

- Q2 (compression-driven invention): the keep score (accuracy minus
  0.02 per operator node) is a description-length criterion in
  miniature. If Q2's MDL work matures, Q4 should adopt its scoring.
- Q3 (operator recruitment): a kept D1 is a natural candidate for
  ALLOCATE_OP recruitment: freeze the expression tree as new opcode
  semantics stored in learner state. Q4 discovery followed by Q3
  recruitment would demonstrate the full invent, persist, reuse loop.
- F2 (experiment construction): the adaptive intervention selection in
  section 6 step 3 is a small active-learning loop; F2's
  disagreement-driven experiment machinery is the natural
  generalization if 24 fixed-budget interventions prove insufficient.

## 14. Open questions for the implementing worker

- Is beam width 32 sufficient for F-THRESH's 5-operator sum-of-products
  under the 24-intervention budget, or does the search need staged
  deepening? Report beam utilization from the run logs.
- Does uncertainty sampling degenerate on F-XOR (where all
  low-order candidates sit at chance)? If the first several
  interventions are uninformative ties, document the tie-break
  behavior explicitly.
- What is the smallest Phase 2 budget at which the reuse ratio still
  clears 0.5? An ablation over budgets (24, 16, 8) is recommended as
  exploratory analysis alongside the frozen 24.
- If no D is kept in Phase 1 (KEEP = 0), Phase 2 still runs with an
  empty library: report the scratch-equivalent result and judge F1.

## 15. Design completeness check against the prereg

- K1: sections 2, 3, 4, 10 specify the sealed world family, with
  frozen numbers (6 observables, 8 passive, 24 interventions,
  full-64 harness scoring). Satisfied.
- K2: sections 5, 6, 7, 8 specify the composition language, the
  posit/test/keep protocol, persistent state and trace formats, and
  the Phase 2 reuse protocol with ablation, with frozen numbers
  (operators, terminals, 7 nodes, beam 32, lambda 0.02, margin
  +0.15, epsilon 0.02). Satisfied.
- K3: the prereg froze F1..F5; section 10 operationalizes them into
  harness checks. Satisfied with no alteration.

No em dashes were used in this document. No implementation was
performed. Pure design.
