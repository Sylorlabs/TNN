# Q4 Design Prereg: Learner-Constructed Explanatory Variables

Date: 2026-09-30. Author: A1 Frontier Architect.
Parent mandate: L3 via Q4, after DDES was ruled terminal L2 (analysis 678ea4162):
DDES fails C0-A at five independent loci, C0-B, C0-C, and C0-D. The L3 path
runs through F2 (hypothesis construction), Q3 (operator recruitment), or Q4
(explanatory variables). This prereg freezes what the Q4 design must specify
and what the future Q4 implementation will be judged by. It is committed
alone before the design document is finalized. Nothing here may be weakened
after the design lands.

## Problem

DDES is causal Stage 1: authored hypothesis language plus guided synthesis.
F2's contextual law used a researcher-supplied K variable. No current TNN
lane constructs an explanatory variable the researchers did not supply and
then reuses it. Q4 tests exactly that: sealed worlds where the true cause
is a hidden function of observables; the learner must posit a derived
variable, test it by intervention, keep it in persistent state, and reuse
it on a later world.

## K1: sealed world family specified (design completeness bar)

The design must specify: observable count and type, intervention operators,
outcome type, hidden-function families as functional descriptions (not
code), the passive confounded sample, the independent adversary's
post-freeze role, and the harness scoring method.

Frozen numbers: 6 binary observables (X1..X6); 8 passive samples drawn with
selection bias (adversary realizes the bias with a fixed seed); 24 adaptive
interventions in Phase 1; harness scores true accuracy over all 64 input
combinations (the harness may query the sealed function exhaustively; the
learner may not).

## K2: posit, test, keep protocol specified (design completeness bar)

The design must specify: the generic composition language (fixed terminals
and operators, no per-family cases), incremental candidate growth (beam
width, scoring with complexity penalty), adaptive intervention selection,
the keep and discard rule with frozen margin and simplicity epsilon, the
persistent state format for kept variables, the construction trace format,
and the Phase 2 reuse protocol with its ablation.

Frozen numbers: terminals {X1..X6, 0, 1}; operators {AND, OR, NOT, XOR};
maximum 7 operator nodes per kept variable; beam width 32; complexity
penalty lambda 0.02 per operator node; keep margin +0.15 over the best
single observable; simplicity epsilon 0.02.

## K3: falsification criteria defined (design completeness bar)

The design must define F1..F5 below so unambiguously that a future worker
can judge BUILD-PASS or BUILD-FAIL without interpretation. These criteria
are frozen here and may not be altered after the design is finalized.

## Frozen implementation kill bars (for the future Q4 build)

- KB1 discovery: on the sealed Phase 1 family, the kept derived variable D
  reaches true accuracy >= 0.95 over all 64 combinations, while the best
  single observable scores <= 0.80 on the same 64 combinations.
- KB2 non-memorization: D has at most 7 operator nodes, was grown
  incrementally (growth trace logged per operator addition), and the
  truth-table memorizer baseline cannot transfer (it restarts from scratch
  by construction; the bar is that the learner's Phase 2 beats it via the
  reuse ratio in KB3).
- KB3 reuse (C0-D): Phase 2 interventions needed to reach true accuracy
  >= 0.95 with the kept-variable library is at most 0.5x the interventions
  needed by the from-scratch ablation. If either side fails to reach 0.95
  within the 24-intervention budget, its count is recorded as 24.
- KB4 determinism and purity: 3/3 byte-identical runs, pure Zag, zero
  Python at every stage including analysis, zero em dash bytes.

## Frozen falsification criteria

- F1: no kept D beats the best single observable by the +0.15 margin on
  sealed Phase 1. Discovery fails. Verdict: BUILD-FAIL.
- F2: D exceeds 7 operator nodes, or no incremental growth trace exists.
  The construction claim fails (this is menu selection or memorization,
  not construction). Verdict: BUILD-FAIL.
- F3: reuse ratio exceeds 0.5. C0-D fails. Verdict: BUILD-FAIL on the L3
  claim (discovery alone may still be reported as bounded L2).
- F4 treadmill guard: any hidden function required adding an operator, a
  terminal, or a dedicated source case to the composition language. The
  run is VOID, the design is revised, and no rescue cases are permitted
  (this is the standing ban on SUB, DIV, PARITY style rescues, applied to
  Q4).
- F5: the best-single-observable baseline or the memorizer baseline
  matches the learner on KB1..KB3. The explanatory variable adds nothing.
  The hypothesis is falsified for this architecture.

## C0 mapping (design intent, to be honored by the design)

- C0-A runtime-defined semantics: D lives in learner-created persistent
  state as an expression tree the learner built. Its semantics come only
  from the generic interpreter over the fixed operator set. No dedicated
  source case per hidden function (F4 enforces this).
- C0-B open structural form: D is grown incrementally, one operator at a
  time, with the growth trace logged. Phase 2 must compose a kept D into
  a strictly larger expression, which a frozen finite menu cannot do.
  (Known risk: beam search over bounded trees is a finite space; the
  design must carry an explicit risk note and the Phase 2 composition
  requirement as the counter-evidence.)
- C0-C unforeseen solutions: an independent adversary (not the
  implementing worker) designs at least one Phase 1 family and the Phase
  2 family after the implementation is frozen. Families must be
  materially different representations (the five example families in the
  design are examples only, not an exhaustive list).
- C0-D reuse: KB3.

## Adversary role (frozen)

An independent adversary, distinct from the implementing worker, selects
the Phase 1 hidden-function family and the Phase 2 hidden-function family
after the implementation freeze, realizes the 8 passive samples with a
fixed seed, verifies F4 (no operator or case was added for the sealed
functions), and scores KB1..KB3 from the harness logs.

## Scope of this prereg

Design only. No implementation is authorized by this prereg. The
implementing worker will file its own prereg referencing these frozen
bars before writing any Zag.
