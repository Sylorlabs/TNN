# Q4 Adversary Test Preregistration: F-PARCOND

Date: 2026-09-30. Worker: Q4 Adversary Test Worker.

## Objective

Test the Q4 learner (beam-search explanatory variable discovery) on the
adversary-designed F-PARCOND family (ADV_SPEC.md, sealed, b4e9b6a14).

F-PARCOND: D = IF X1 THEN (X2 XOR X3) ELSE (X2 AND X3). 6 operators.
Context-dependent operation: the correct operation on (X2, X3) depends
on X1. Materially different from CONJ, XOR, THRESH, MUX.

## Method

Adapt q4_reuse.zag (commit b719bb54b) with two new sealed families:

- fam 5: F-PARCOND. D = (x1 & (x2^x3)) | ((x1^1) & (x2&x3)).
- fam 6: F-PARCOND-XOR. C' = D XOR X4 (Phase 2 reuse target).

Phase 1: discovery on fam 5 (8 biased passive + 24 adaptive interventions).
Phase 2: reuse D as atomic terminal for fam 6 vs scratch.

Pure Zag. Fixed seeds. 3/3 byte-identical runs.

## Frozen Kill Bars

### K1: F-PARCOND implemented per spec

- Sealed fam 5 computes D per ADV_SPEC.md truth table.
- Verified: all 8 rows of (X1,X2,X3) match the spec table.

### K2: Discovery tested

- True accuracy >= 0.95 (61/64) on held-out.
- Beats best observable by >= 0.15 margin.
- Operator count <= 7.
- Growth trace shows incremental construction.

PASS if all hold. FAIL (F1) if accuracy < 0.95 or margin < 0.15.
FAIL (F2) if operator count > 7 or no growth trace.

### K3: Reuse tested

- Reuse interventions to criterion (hit_iv) vs scratch interventions.
- Ratio <= 0.5 (reuse at least 2x more efficient).

PASS if ratio <= 0.5. FAIL (F3) if ratio > 0.5.

### K4: Purity and determinism

- Pure Zag at every stage. Zero Python invocations.
- 3/3 byte-identical runs (same md5).
- Zero stderr on all runs.
- Zero em dash bytes in committed docs.

## Falsifiers

- F1: Discovery fails (accuracy < 0.95 or margin < 0.15).
- F2: Memorization (operator count > 7 or no growth trace).
- F3: Reuse fails (ratio > 0.5).
- F4: Language violation (operators outside {AND, OR, NOT, XOR} or > 7 ops).
- F5: Not better than baseline (learner <= best observable + 0.15).

## C0 Assessment Plan

- C0-A: Runtime-defined semantics (partial, as before).
- C0-B: Open structural form (incremental traced growth).
- C0-C: TESTED HERE. Adversary-designed family post-freeze.
- C0-D: Cognitive reuse (Phase 2 ratio).

## Verdict Labels

- BUILD-PASS: All kill bars pass. F-PARCOND discovered and reused.
- BUILD-FAIL: Any kill bar fails. Report which falsifier fired.

## Governance

- Prereg committed alone before implementation.
- Implementation references this prereg.
- Owned path: docs/lab/research-lead/overnight-20260928/q4_parcond/ only.
- Commits use pathspec to avoid sweeping.
- No Python. No em dashes.
