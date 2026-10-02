# Q4 Implementation Prereg: Learner-Constructed Explanatory Variables

Date: 2026-09-30. Author: Q4 Implementer (subagent).
Parent mandate: implement Q4 per the frozen design (Q4_DESIGN.md) and
design prereg (PREREG_Q4DESIGN.md, commit 1b72fdf45). This prereg is
committed alone before any Zag is written. All frozen numbers below are
copied from the design; none are weakened.

## What is being tested

A learner that must (1) posit a derived variable D from a fixed generic
composition language, grown incrementally under a beam search with a
complexity penalty; (2) test candidates by adaptive intervention
(uncertainty sampling over a sealed world); (3) keep D in persistent
learner state only if it beats the best single observable by a frozen
margin; and (4) reuse the kept variable as an atomic terminal in a
strictly larger expression on a second sealed world.

## Frozen numbers (from the design, not altered)

- Observables: X1..X6 binary; outcome Y binary; Y = C deterministic.
- Evidence: 8 passive samples with X6 selection bias (6 of 8 with X6=Y);
  24 adaptive interventions per phase.
- Composition: terminals {X1..X6, 0, 1}; operators {AND, OR, NOT, XOR};
  max 7 operator nodes per kept variable; beam width 32; lambda 0.02
  per operator node; keep margin +0.15 over best single observable;
  simplicity epsilon 0.02.
- Harness scores true accuracy over all 64 combinations (harness only;
  the learner never sees the full table).
- Families tested by this implementation: F-CONJ (C = X1 AND X2) and
  F-XOR (C = X1 XOR X2). The independent adversary selects additional
  families post-freeze; these two are the implementer's own sealed test.

## Kill bars

- KB1 discovery: kept D reaches true accuracy >= 0.95 over all 64
  combinations; best single observable <= 0.80 on the same 64.
- KB2 non-memorization: D has at most 7 operator nodes; growth trace
  logged per operator addition; Phase 2 B-SCRATCH comparison isolates
  reuse.
- KB3 reuse (C0-D): Phase 2 interventions to first reach true accuracy
  >= 0.95 with the kept-variable library is at most 0.5x the
  interventions needed by the from-scratch ablation. Count recorded as
  24 for any side that never reaches 0.95 within budget.
- KB4 determinism and purity: 3/3 byte-identical runs; pure Zag at every
  stage including analysis; zero Python invocations; zero em dash bytes
  in all committed docs.

## Falsification (frozen from the design prereg, unaltered)

- F1: no kept D beats best single observable by +0.15. BUILD-FAIL.
- F2: D exceeds 7 operator nodes, or no incremental growth trace exists.
  BUILD-FAIL.
- F3: reuse ratio exceeds 0.5. BUILD-FAIL on the L3 claim (discovery may
  still be reported as bounded L2).
- F4 treadmill guard: if any sealed family required adding an operator,
  terminal, or dedicated case, the run is VOID and the design is
  revised; no rescue cases permitted.
- F5: best-single-observable or memorizer baseline matches the learner
  on KB1..KB3. Hypothesis falsified for this architecture.

## Implementation plan

Single Zag program `q4.zag`:

1. Sealed world module: two frozen hidden functions (F-CONJ, F-XOR) as
   bit-level evaluation; passive sample generator with fixed seed and
   the specified X6 bias; intervention executor (SET Xi values, read Y).
2. Expression module: expression trees as node arrays in a fixed arena;
   node kinds TERM (with terminal id) and OP (AND/OR/NOT/XOR with child
   indices); generic interpreter evaluating an expression on an input
   vector.
3. Beam search: 32 candidate slots; initialize from 8 terminals; extend
   by NOT over each candidate and AND/OR/XOR over each ordered pair,
   with structural hash-consing to suppress duplicates; score =
   accuracy on all evidence minus 0.02 per operator node; keep top 32;
   log every operator addition to the growth trace.
4. Intervention selection: after each growth round, score all 64 input
   combinations by disagreement among the top 8 candidates (fraction
   predicting 1, distance from 0.5); pick the max-disagreement
   combination not yet used; deterministic tie-break on lowest index;
   execute, append evidence, repeat to 24.
5. Keep/discard: after budget, argmax score over beam; keep iff
   accuracy >= B-OBS accuracy + 0.15, operator nodes <= 7, and no other
   candidate within 0.02 accuracy with fewer nodes.
6. Phase 2: fresh passive samples and fresh budget on the second family
   (F-XOR after F-CONJ, or the reverse); library variables usable as
   atomic terminals; B-SCRATCH ablation with the library disabled.
7. Baselines: B-OBS (best single Xi on harness full-64), B-MEM
   (truth-table memorizer, restarts Phase 2 from scratch).
8. Reporting: emit kept D expression, true accuracies, intervention
   counts, growth trace length, keep decision, KB1..KB3 verdicts.

Phase 2 pairing: Phase 1 on F-CONJ keeping D1 = X1 AND X2; Phase 2 on
F-NEST-PAIR C' = (X1 AND X2) OR X5, i.e. D' = OR(D1, X5), which shares
the Phase 1 subexpression and is materially different overall. The
scratch ablation must re-derive the AND before composing the OR.

C0-B evidence logged: incremental growth trace present; Phase 2
strictly-larger composition using D1 as atomic terminal; beam
utilization reported.

## Scope and honesty

This implementation tests 2 of the 5 example families plus one Phase 2
pairing. The independent adversary will select additional families
post-freeze, including at least one materially different
representational form. If F-XOR's uncertainty sampling degenerates
(all low-order candidates at chance), the tie-break behavior will be
documented explicitly per the design's open questions.

Verdict labels: BUILD-PASS only if KB1, KB2, KB3, and KB4 all pass and
none of F1..F5 fires. BUILD-FAIL otherwise, with the firing criterion
named.

No Python at any stage. No em dashes in docs.
