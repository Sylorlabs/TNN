# Q4 Implementation Result: BUILD-FAIL on L3 (F3 fires)

Date: 2026-09-30. Author: Q4 Implementer.
Prereg: 5a6613bc3 (committed before implementation).
Implementation: q4.zag (pure Zag, no Python).

## Verdict: BUILD-FAIL

F3 fires: reuse ratio 1.0 exceeds the 0.5 bar. C0-D fails. Per the frozen
prereg, this is BUILD-FAIL on the L3 claim. Discovery alone (KB1, KB2)
passes and may be reported as bounded L2.

## Kill bar results

### KB1 discovery: PASS (both families)

Phase 1a (F-CONJ, C = X1 AND X2):
- Kept D: node 14, 1 operator, 32/32 on evidence
- True accuracy: 64/64 = 1.00 >= 0.95
- Best single observable: 48/64 = 0.75 <= 0.80
- Keep margin: 32/32 vs 24/32 on evidence (1.00 vs 0.75, margin 0.25 >= 0.15)

Phase 1b (F-XOR, C = X1 XOR X2):
- Kept D: node 16, 1 operator, 32/32 on evidence
- True accuracy: 64/64 = 1.00 >= 0.95
- Best single observable: 32/64 = 0.50 <= 0.80
- Keep margin: 32/32 vs 17/32 on evidence (1.00 vs 0.53, margin 0.47 >= 0.15)

### KB2 non-memorization: PASS (both families)

- P1A: 1 operator node <= 7; growth trace 4012 events logged
- P1B: 1 operator node <= 7; growth trace 4091 events logged
- D1 = AND(X1, X2); D2 = XOR(X1, X2). Both grown incrementally via beam
  search, not selected from a menu. The X6 confound (6/8 passive with
  X6=Y) was dissociated by interventions; neither kept D uses X6.

### KB3 reuse (C0-D): FAIL

Phase 2 (F-NEST-PAIR, C' = (X1 AND X2) OR X5):
- Reuse (D1 as atomic terminal): hit_iv = 1
- Scratch (no library): hit_iv = 1
- Ratio: 1.0 > 0.5. F3 fires.

Both sides reach 0.95 true accuracy after 1 intervention. The beam search
is powerful enough that scratch re-derives the 2-operator solution
almost as fast as reuse composes the 1-operator solution. The shared
subexpression (X1 AND X2) is too easy to re-derive for the 0.5x bar.

### KB4 determinism and purity: PASS

- 3/3 byte-identical: md5 976a9875358ed0ccd1d1bfa5d2d5e9e2
- Zero stderr on all runs
- Pure Zag at every stage (implementation, compilation, execution)
- Zero Python invocations
- Zero em dash bytes in all committed docs

## Falsification criteria

- F1 (no discovery): does NOT fire. Both families discovered with 1.00
  true accuracy, beating observables by > 0.15.
- F2 (no construction trace or > 7 ops): does NOT fire. Both D1 and D2
  have 1 operator and full growth traces.
- F3 (reuse ratio > 0.5): FIRES. Ratio 1.0.
- F4 (treadmill: added operator/case): does NOT fire. Composition
  language fixed at {AND, OR, NOT, XOR} over {X1..X6, 0, 1}. No additions.
- F5 (baselines match learner): does NOT fire. B-OBS gets 0.75/0.50 vs
  learner 1.00. B-MEM (truth-table) cannot reach 0.95 within 32 evidence
  (needs 56 observations by calculation); it restarts from scratch in
  Phase 2 by construction.

## Honest analysis

The learner CAN construct explanatory variables. On two sealed families
(F-CONJ and F-XOR), it grew the correct 1-operator expression
incrementally, logged the construction trace, dissociated the X6
confound via intervention, and kept the variable in persistent state.
This is genuine Stage 2 causal discovery, bounded L2.

The L3 claim fails on C0-D (reuse). The Phase 2 task does not
demonstrate that the kept variable improves later cognition enough to
clear the 0.5x bar. Two factors:

1. The beam search is too strong relative to the task. Scratch finds
   the 2-op Phase 2 solution in the same number of interventions as
   reuse finds the 1-op solution.

2. The shared subexpression is shallow (1 op). A deeper shared
   structure (e.g. 3-op D1) would make re-derivation costlier and give
   reuse more room to demonstrate savings.

The design's open question ("smallest Phase 2 budget at which the reuse
ratio still clears 0.5") is answered: at budget 24 with this pairing,
it does not clear. A harder Phase 2 pairing or a weaker beam (fewer
extensions per round) might separate the curves.

## C0 assessment

- C0-A (runtime-defined semantics): PARTIAL. D lives in learner-created
  state as an expression tree; semantics come from the generic
  interpreter. But the beam search machinery and scoring are
  researcher-authored.
- C0-B (open structural form): WEAK. Beam search over bounded trees is a
  finite space. The incremental traced growth and Phase 2 composition
  are present, but the space is bounded at 7 ops.
- C0-C (unforeseen forms): NOT TESTED. Only 2 of 5 example families
  tested; adversary has not selected post-freeze families.
- C0-D (cognitive reuse): FAIL. KB3 not met.

## Files

- PREREG_Q4IMPL.md: implementation prereg (5a6613bc3)
- q4.zag: implementation (pure Zag)
- q4: compiled binary
- Q4_RAW_1/2/3.txt: 3/3 byte-identical raw outputs
- Q4_RAW_1/2/3.err: empty stderr logs

## Recommendation

Report as bounded L2 discovery (KB1+KB2 pass). Do not claim L3. For a
future L3 attempt: use a deeper shared subexpression in Phase 2, or
constrain the beam to make re-derivation costlier, or test on
adversary-selected families with materially different forms.
