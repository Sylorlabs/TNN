# Q4 Reuse Redesign Result: BUILD-PASS (KB3 clears with deep shared structure)

Date: 2026-09-30. Author: Q4 Reuse Redesign Worker.
Prereg: 2954b4da2 (committed before implementation).
Implementation: q4_reuse.zag (pure Zag, no Python).

## Verdict: BUILD-PASS

All three kill bars pass. The deep shared structure (5-op D1) separates
the reuse and scratch intervention curves decisively.

## Kill bar results

### K1 deeper Phase 2: PASS

Phase 1 on F-THRESH (C = majority(X1, X2, X3)):
- Kept D1: node 1079, 5 operator nodes, 32/32 on evidence
- True accuracy: 64/64 = 1.00 >= 0.95
- Best single observable: 48/64 = 0.75 <= 0.80
- Keep margin: 32/32 vs 25/32 on evidence (1.00 vs 0.78, margin 0.22 >= 0.15)
- Growth trace: 3594 events logged, 3602 nodes created
- Shared structure depth: 5 ops (>= 4 required)

The beam discovered the 5-op sum-of-products within the 24-intervention
budget. This answers the design's open question affirmatively: beam-32
suffices for F-THRESH.

### K2 reuse ratio <= 0.5 (C0-D): PASS

Phase 2 on F-THRESH-XOR (C' = D1 XOR X4):
- Reuse (D1 as atomic terminal): hit_iv = 0, final_true = 64/64
- Scratch (no library): hit_iv = 24 (never reached), final_true = 48/64
- Ratio: 0/24 = 0.0 <= 0.5. KB3 = 1.

Reuse composes XOR(D1, X4) as 1 operator over the atomic D1 and reaches
64/64 true accuracy from the 8 passive samples alone. Scratch must
re-derive the 6-op expression from base terminals; the beam generates one
operator level per round, so the 6-op target cannot even appear before 5
interventions, and within the 24 budget scratch never ranks it top
(final true 48/64 = 0.75, no better than the best single observable).

### K3 purity and determinism: PASS

- 3/3 byte-identical: md5 e17a19cbbc97e530ed3ee3b13384c469
- Zero stderr on all runs
- Pure Zag at every stage (implementation, compilation, execution)
- Zero Python invocations
- Zero em dash bytes in all committed docs

## Falsification criteria

- F1 (Phase 1 fails to keep D1): does NOT fire. D1 kept with 5 ops,
  64/64 true, margin 0.22.
- F2 (reuse ratio > 0.5): does NOT fire. Ratio 0.0.
- F3 (treadmill): does NOT fire. Composition language unchanged:
  {AND, OR, NOT, XOR} over {X1..X6, 0, 1} plus the kept D1 as a
  learner-created atomic terminal. No operators, terminals, or cases
  added.

## C0 assessment

- C0-A (runtime-defined semantics): PARTIAL, unchanged. D1 lives in
  learner-created persistent state as an expression tree with its growth
  trace; semantics come from the generic interpreter. The beam search
  machinery and scoring remain researcher-authored.
- C0-B (open structural form): STRENGTHENED. Growth is incremental and
  traced (3594 events). Phase 2 uses the kept D1 as an atomic terminal
  for a strictly larger expression, so the reachable structure class
  grows with learner history. The beam space remains bounded, honestly
  noted.
- C0-C (unforeseen forms): NOT TESTED. This is the implementer's own
  pairing, not an adversary-selected family. Recorded as future work.
- C0-D (cognitive reuse): PASS. The kept variable decisively improves
  later cognition: reuse solves from passive evidence alone (0
  interventions) what scratch cannot solve in 24 interventions.

## Honest scope

This is bounded L2 discovery with demonstrated reuse (C0-D satisfied).
It is not a full L3 claim: C0-C (adversary-selected families) is
untested, and the promotion pipeline (reproduction, baselines beyond
B-SCRATCH, OOD, ablation, transfer, red team, governance audit) has not
been run on this pairing.

The key advance over the prior BUILD-FAIL: the prior Phase 2 shared only
a 1-op subexpression, letting scratch re-derive as fast as reuse
composed. With a 5-op shared subexpression, re-derivation is
structurally costlier (one operator level per beam round) while reuse
stays at 1 operator over the atomic kept variable. The intervention
curves separate: 0 vs 24.

## Files

- PREREG_Q4REUSE.md: redesign prereg (2954b4da2)
- q4_reuse.zag: implementation (pure Zag)
- q4_reuse: compiled binary (untracked, not committed)
- Q4REUSE_RAW_1/2/3.txt: 3/3 byte-identical raw outputs
- Q4REUSE_RAW_1/2/3.err: empty stderr logs
- Q4REUSE_RESULT.md: this file

## Recommendation

Report as BUILD-PASS on all kill bars. C0-D is now satisfied for this
architecture and pairing. Next steps for the L3 claim: adversary-selected
Phase 1/Phase 2 families (C0-C), then the remaining promotion pipeline
steps.
