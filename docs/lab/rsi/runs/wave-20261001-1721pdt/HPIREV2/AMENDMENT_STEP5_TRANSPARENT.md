# TRANSPARENT AMENDMENT: H-PI-REV2 step 5 (drafted wave-20261001-1721pdt, AMENDED)

This document is an AMENDMENT to a frozen prereg, drafted in full before
any re-execution. It is flagged explicitly as AMENDED; it is not a silent
revision. Per the wave-20261001-1421pdt judge ruling (DEBATE_1421PDT.md),
the amendment (a) is drafted in full here, naming a concrete replacement
comparison that remains discriminating, (b) must be committed alone by the
coordinator before any re-execution (commit-order self-check), and
(c) preserves the run matrix and determinism requirements. Execution under
the amended prereg is next wave's work, not this wave's.

## What was wrong (the flawed clause, quoted verbatim)

The frozen step-5 prereg
(docs/lab/rsi/runs/wave-20261001-1121pdt/pi_rev2/PREREG_PI_REV2_STEP5_BASELINE.md)
states:

"- K-SB4 (correctness parity): the revised procedure is correct on all
of T (with updated expectations per the frozen conflict rule),
F1r, and F1r-reuse. B1's fitted program is correct on T+F1r.
Kill: any misprediction by the revised procedure on T/F1r/F1r-reuse,
or any misprediction by B1's fit on T+F1r."

The clause "B1's fitted program is correct on T+F1r" presupposes that
B1's full 1055-program enumeration returns a fitted program. It does
not: B1 evaluated all 1055 programs and returned first-fit -1 on 3/3
byte-identical runs. K-RV2-1b, verified against the frozen code in
K_RV2_1B_VERIFICATION.md (this lane), proves that no program in the
frozen evaluator's semantics can fit T+F1r: output position (k=0, n=3)
requires index 2 from "abc"->"ccc" and index 0 from "rab"->"rrr"
simultaneously, and eval_prog is a deterministic pure function of
(prog, k, n). So "B1's fitted program" names an object that cannot
exist under the frozen definitions, and the kill condition is
unsatisfiable as written. The step-5 execution therefore recorded
BASELINE-FAIL on a design flaw in the frozen prereg, not on a defect
in the revision machinery.

## Minimal correction preserving the bar's original intent

K-SB4's original intent is correctness parity: hold the revision
machinery and the re-search baseline to a common correctness standard
on the same data, so a PASS means the revision is genuinely correct
and the baseline comparison is genuinely informative. The correction
keeps that intent but stops demanding the impossible:

- K-SB4a (revised procedure correctness, unchanged in substance):
  the revised procedure is correct on all of T (with updated
  expectations per the frozen conflict rule: "xy"->"xx" is the
  expected update), F1r, and F1r-reuse. Numerically: fails=0 across
  the 5 prediction checks ("abc"->"ccc", "xy"->"xx", "defg"->"gggg",
  "rab"->"rrr", "rqw"->"rrr").
- K-SB4b (baseline competence, the discriminating replacement for
  "B1's fitted program is correct on T+F1r"): B1 run over T alone
  (the set the frozen v1 discovery fit) returns first_fit >= 0, and
  the fitted program is correct on all of T (fails=0). This pins B1
  as a working re-search baseline rather than a broken one: if B1
  cannot fit T, the comparison is void and the bar kills. Kill:
  first_fit < 0 on T, or any misprediction by the T-fitted program
  on T.
- K-SB4c (verified-impossibility recheck, pins K-RV2-1b as a live
  claim): B1's full 1055-program enumeration over T+F1r returns
  first_fit = -1. This is the verified impossibility restated as a
  numeric bar: if B1 ever finds a fit on T+F1r, the verified
  impossibility is falsified (evaluator or proof bug) and the bar
  kills. This keeps the amendment honest: it does not become a
  vacuous "B1 cannot fit, so parity is vacuous, PASS".

Together the three sub-bars keep the bar discriminating: the revised
procedure must be fully correct (4a), the baseline must be a working
fit on the pre-counterexample data (4b), and the impossibility that
explains the original failure must hold as a checked numeric fact
(4c). No bar is weakened to force a pass; each has a real kill
condition.

All other frozen bars (K-SB1, K-SB2, K-SB3, K-SB5, K-SB6) are
re-frozen unchanged, with the same numeric thresholds as the frozen
step-5 prereg. K-SB2's threshold remains strict inequality:
revision_evals < b1_enumerated. K-SB3, K-SB5, K-SB6 are unchanged
verbatim.

Run-matrix note (transparent): the amended K-SB4b requires B1
executions over T alone in addition to the frozen 12-run matrix.
The amended matrix is 15 runs total (revision x3, B0 x3, B1-on-T+F1r
x3, B1-on-T x3, B2 x3), each binary 3/3 byte-identical, exit 0, zero
stderr bytes. Determinism requirements are preserved; the matrix
change is stated here so the coordinator can rule on it.

## What this amendment does NOT do

- The original step-5 verdict stays BASELINE-FAIL and is NOT
  retroactively changed by this amendment. Step 5 of the 11-step
  frontier pipeline remains failed as executed. The amended prereg
  governs only a future re-execution; a step-5 PASS under the amended
  prereg would be a new result with its own provenance, never an
  edit of the BASELINE-FAIL record.
- This amendment does not weaken any bar to force a pass, does not
  add protected-core operations, and does not change the bounded L2
  ceiling: a PASS under the amended prereg is not evidence toward L3.
- This wave performs re-freeze only. No re-execution is performed
  under the amended text.

## Provenance

- Frozen step-5 prereg: docs/lab/rsi/runs/wave-20261001-1121pdt/pi_rev2/PREREG_PI_REV2_STEP5_BASELINE.md
- Step-5 result record: docs/lab/rsi/runs/wave-20261001-1421pdt/pi_rev2_exec/RESULT_PI_REV2_STEP5.md (verdict BASELINE-FAIL)
- Debate ruling: docs/lab/rsi/runs/wave-20261001-1421pdt/debate/DEBATE_1421PDT.md (attribution upheld; amendment approved only with conditions)
- K-RV2-1b verification: K_RV2_1B_VERIFICATION.md (this lane)
- Amended re-frozen prereg: PREREG_PI_REV2_STEP5_BASELINE_AMENDED.md (this lane)
