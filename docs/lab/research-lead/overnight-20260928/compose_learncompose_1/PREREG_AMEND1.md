# PREREG_AMEND1.md -- COMPOSE-LEARNCOMPOSE-1 prereg amendment

Date: 2026-10-03. Worker: COMPOSE-LEARNCOMPOSE-1. Committed BEFORE
any implementation commit (the implementation exists as uncommitted
files; this amendment corrects hand-trace errors against the frozen
mechanism spec, Section 1.3).

## Cause

Two hand-trace errors in PREREG.md Section 3. The frozen similarity
rule (1.3) assigns sim=2 when "one code multiset is a subset of the
other". I traced sim=1 (kind-match-only) for FANIN and CHAIN10, but:

- FANIN: skF = [1001002,1001002,2002022] is a multiset-subset of
  skD = [1001001,1001002,1001002,2002022] (two 1001002 <= two
  1001002; 2002022 <= 2002022). sim=2, not 1.
- CHAIN10: skC3 = [1001001,1001001,1001002] is a multiset-subset
  of skC10 = [1001001 x9, 1001002] (two <= nine; one <= one).
  sim=2, not 1.

The implementation follows the frozen spec (retrieves on sim>=2).
The spec (Section 1) is UNCHANGED. Only the predicted Section 3
values below are corrected to match the spec.

## Corrected bars

- FANIN: ANS=9, TRIES=4, WIDEN=0, MODE=REVISE, SIM=2, NEGREC=1.
  Trace (per spec): sim-2 retrieval of the diamond entry; X
  unmapped (no (arity1,{1},{1}) in FANIN); DROP_UNMAPPED ->
  [f1(C),f1(C),g(i0,i1)] (2 execs) -> 8 != 9; R1 skipped (no -2s);
  R2 TRUNCATE fails (0 new execs); R3 SUBST i0 -> f2 ->
  [f2(C),f1(C),g] (2 execs) -> 9. Total 4. This is cross-shape
  transfer via memory (a positive result for the hypothesis),
  not a cold-start.
- CHAIN10: ANS=4, TRIES=108, WIDEN=0, MODE=COLD, SIM=-1,
  NEGREC=0, ESEL=-1. Trace (per spec): sim-2 retrieval of the
  CHAIN3 entry (3-chain program); adaptation maps to
  [20(C),20(i0),29(i1)]; execution -> -2 != 4; R1/R2/R3/R4
  revision fails (~53 tries); fallback cold-start (55 tries).
  Total 108. The memory misfires (a 3-chain does not extend to
  a 10-chain via the frozen operators) and the mechanism pays
  the cost, then falls back. Honest negative result for
  retrieval precision; reported as-is.

All other Section 3 bars are unchanged. No mechanism rule, no
threshold, and no other predicted value is altered by this
amendment.
