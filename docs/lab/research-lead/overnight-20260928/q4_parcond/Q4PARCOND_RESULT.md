# Q4 F-PARCOND Adversary Test Result: BUILD-PASS

Date: 2026-09-30. Worker: Q4 Adversary Test Worker.
Prereg: ad4284269 (committed before implementation).
Implementation: q4_parcond.zag (pure Zag, no Python).
Adversary spec: b4e9b6a14 (F-PARCOND, sealed post-freeze).

## Verdict: BUILD-PASS

All four kill bars pass. The learner discovers the adversary-designed
conditional-computation structure and reuses it.

## The Adversary Family

F-PARCOND: D = IF X1 THEN (X2 XOR X3) ELSE (X2 AND X3). 6 operators.
Implemented as: D = (x1 & (x2^x3)) | ((x1^1) & (x2&x3)).

Truth table verified against ADV_SPEC.md: TABLE_MATCH 1 (all 8 rows).

Structural difference from training families:
- vs CONJ/XOR: 4 operator types coordinated (AND, OR, NOT, XOR), not 1.
- vs THRESH: asymmetric (X1 is condition, not symmetric participant).
- vs MUX: selects between computations (XOR vs AND), not variables.
- Key test: context-dependent operation.

## Kill Bar Results (3/3 byte-identical, md5 e9be97dd8a0c8428ce4f616e087a6433)

### K1: F-PARCOND implemented per spec: PASS

Sealed fam 5 computes D per the spec truth table (verified TABLE_MATCH 1).
Phase 2 target fam 6 = D XOR X4.

### K2: Discovery tested: PASS

Phase 1 on F-PARCOND:
- Kept D1: node 1105, 7 operator nodes, 32/32 on evidence
- True accuracy: 64/64 = 1.00 >= 0.95
- Best observable true: 40/64 = 0.625
- Margin: 0.375 >= 0.15
- Growth trace: 3860 events, 3868 nodes created
- Operator count: 7 <= 7

The beam discovered the conditional structure within the 24-intervention
budget. The 7-op solution (vs 6-op reference) is the minimal found;
keep=1 confirms no simpler within-0.02 alternative.

### K3: Reuse tested (C0-D): PASS

Phase 2 on F-PARCOND-XOR (C' = D XOR X4):
- Reuse (D as atomic terminal): hit_iv = 0, final_true = 64/64
- Scratch (no library): hit_iv = 24 (never reached), final_true = 52/64
- Ratio: 0/24 = 0.0 <= 0.5

Reuse composes XOR(D, X4) as 1 operator over the atomic D and reaches
64/64 from the 8 passive samples alone. Scratch must re-derive the 7-op
expression; the beam generates one operator level per round, so the
target cannot appear before 6 interventions, and scratch never ranks it
top within budget (final 52/64 = 0.81).

### K4: Purity and determinism: PASS

- 3/3 byte-identical: md5 e9be97dd8a0c8428ce4f616e087a6433
- Zero stderr on all runs
- Pure Zag at every stage (implementation, compilation, execution)
- Zero Python invocations
- Zero em dash bytes in committed docs

## Falsification Criteria

- F1 (discovery fails): does NOT fire. 64/64 true, margin 0.375.
- F2 (memorization): does NOT fire. 7 ops, 3860 trace events.
- F3 (reuse fails): does NOT fire. Ratio 0.0.
- F4 (language violation): does NOT fire. Operators in {AND, OR, NOT, XOR}.
- F5 (not better than baseline): does NOT fire. 1.00 vs 0.625.

## C0 Assessment

- C0-A (runtime-defined semantics): PARTIAL, unchanged. D lives in
  learner-created persistent state; beam machinery researcher-authored.
- C0-B (open structural form): STRENGTHENED. Incremental traced growth
  (3860 events). The 7-op conditional structure was not in the training
  families.
- C0-C (unforeseen forms): PASS. F-PARCOND was designed by independent
  adversary post-freeze (b4e9b6a14). The learner had never seen
  conditional-computation structure. It discovered it.
- C0-D (cognitive reuse): PASS. Reuse solves from passive evidence alone
  what scratch cannot solve in 24 interventions.

## Honest Scope

This is bounded L2 discovery with demonstrated reuse on an
adversary-selected family (C0-C and C0-D satisfied for this pairing).
It is not a full L3 claim: C0-A remains partial (beam is
researcher-authored), and the remaining promotion pipeline steps
(reproduction, OOD, ablation, transfer, red team, governance audit)
have not been run on F-PARCOND.

The key advance: the discovery mechanism generalizes to a materially
different structural form (conditional computation) that was not in its
training distribution. This is the first C0-C data point for the Q4
architecture.

## Files

- PREREG_Q4PARCOND.md: test prereg (ad4284269)
- q4_parcond.zag: implementation (pure Zag)
- q4_parcond: compiled binary (untracked, not committed)
- Q4PARCOND_RAW_1/2/3.txt: 3/3 byte-identical raw outputs
- Q4PARCOND_RAW_1/2/3.err: empty stderr logs
- Q4PARCOND_RESULT.md: this file
