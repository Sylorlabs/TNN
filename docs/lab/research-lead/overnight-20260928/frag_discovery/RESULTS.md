# Fragment Discovery (Hypothesis B) Results

Deterministic run of `frag_discovery.zag` on Battery v2 (T0..T5).
Program output is byte-identical across 3 runs (md5-verified; see run7.log).
No PVM_TRAP, no VERIFY-FAIL, no F-TRICK in the log. All eval budgets < 1M.

## Main phase (carried library)

| Task | Route | Verdict | Train | Held-out | Ops | Evals | Prediction | Match |
|------|-------|---------|-------|----------|-----|-------|------------|-------|
| T0 2x+1 | base | SOLVE | 9/9 | NA | 5 | 69 | SOLVE | yes |
| T1 |x| | assembler | SOLVE | 17/17 | 4/8 | 35 | 7 | SOLVE, 35 ops, 4/8 heldout | yes |
| T2 x mod 3 | base | SOLVE | 17/17 | NA | 3 | 36 | SOLVE | yes |
| T3 parity | base | SOLVE | 25/25 | NA | 8 | 9747 | SOLVE | yes |
| T4 ||x|-2| | composer | SOLVE | 13/13 | 6/8 | 38 | 2515 | SOLVE, 38 ops | yes |
| T5 |x|+|x-2| | composer | SOLVE | 13/13 | 4/8 | 40 | 27661 | SOLVE, 40 ops | yes |

- T1: assembler emitted the 33-op ABS fragment (7x [DUP,PUSH(-v),ADD,JZ] +
  [DUP,PUSH(-8),ADD,JZ] + [NEG]); main rewritten to [IN0,CALL0]; total 35.
  Fragment induced TRAIN-SCOPED, kink set {0}, P-VM-valid.
- T4: 1-CALL exhausted (2380 candidates, none exact); 2-CALL found
  [IN0,CALL0,PUSH2,SUB,CALL0] (5 + 33 = 38 ops). 3 RETRIEVE events for
  fragment 0 with kink-subset {0} <= {-2,0,2}; 2 RETRIEVE-CALL-SITE events.
- T5: 1-CALL exhausted (2380); 2-CALL found
  [IN0,CALL0,IN0,PUSH2,SUB,CALL0,ADD] (7 + 33 = 40 ops, exactly at cap).
  3 RETRIEVE events ({0} <= {0,2}); 2 RETRIEVE-CALL-SITE events.
- Held-out (8 episodes each, outside train range): T1 4/8 (as predicted,
  disclosed limitation of the finite chain); T4 6/8; T5 4/8. The ABS
  fragment is train-scoped by construction; held-out scores are reported,
  not claimed.

## Ablation (library disabled, composer skipped, no induction)

| Task | Verdict | Prediction | Match |
|------|---------|------------|-------|
| T0 | SOLVE | SOLVE | yes |
| T1 | SOLVE (assembler) | SOLVE | yes |
| T2 | SOLVE (base) | SOLVE | yes |
| T3 | SOLVE (base) | SOLVE | yes |
| T4 | FAIL | FAIL | yes |
| T5 | FAIL | FAIL | yes |

T4/T5 FAIL because the assembler declines (3 and 2 kinks; single-kink
scope) and the base exhausts sizes 1..8 on the P-VM without success.
The fragment library is the causal difference-maker.

## Fresh state (empty library, T4/T5 only; battery metric 12)

- T4 fresh: FAIL (2515 evals carried SOLVE vs 669 evals fresh FAIL)
- T5 fresh: FAIL (27661 evals carried SOLVE vs 669 evals fresh FAIL)

## Kill bars

- K1: prereg `ce6d3b1a7` (plus amendment `a709777a6`) strictly precedes the
  implementation commit (verified with git merge-base --is-ancestor).
- K2: genuine fragment-reuse SOLVE on P-VM kinked tasks the base cannot
  solve: T4 AND T5 both SOLVE via composer reuse of the induced ABS
  fragment; ablation destroys both. PASS.
- K3: pure Zag (no Python in implementation, harness, or analysis);
  no em/en dashes (shell-verified); VM cores byte-identical to frozen
  sources; all eval budgets < 1M. PASS.

## Falsifier watch

- F-TRICK: not tripped. The base never solved a P-VM kinked task
  (R2-base fallback exhausted on T1/T4/T5 in ablation/fresh).
- F-SMUG: pvm_valid = 1 on the ABS fragment and all composed mains;
  the fragment uses only JZ/JNZ/JMP + stack ops (no DIV/MOD/LT/EQ/GT).
- F-MEM: 40-op cap respected (T5 exactly at 40; T4 at 38; T1 at 35).
- B-F1/B-F2/B-F3: no hardcoded ABS (the chain is assembled from region
  repair); no train-only overfit claimed (held-out reported);
  no duplicate fragments (dedup by signature; 3 distinct fragments).

## Deviations and notes

- The prereg section 3c T1 instance describes the partition as
  R_lo = -8..-1 / R_hi = 0..8, but the numbered rule (3c.1) specifies
  R_lo = x <= kink. The implementation follows the numbered rule
  (R_lo = -8..0, A = R_hi). The emitted fragment is still 33 ops and the
  total still 35, matching the prediction; the difference is which region
  supplies the chain values. No kill bar affected.
- T5's kink set is {0,2} (|x|+|x-2| on -4..8); the ABS kink set {0} is a
  subset, so retrieval succeeds. (An earlier draft summary misrecorded
  T5 as |x|+||x|-2|; the prereg and implementation agree on |x|+|x-2|.)
- Two implementation bugs were found and fixed before the committed run:
  (1) mode-1 verify did not simulate the chain's stack context;
  (2) the inducer's inline probe mis-executed jump-containing fragments
  (now probed via CALL in the composer-identical context).
  Both fixes are pre-commit; the frozen design is unchanged.
