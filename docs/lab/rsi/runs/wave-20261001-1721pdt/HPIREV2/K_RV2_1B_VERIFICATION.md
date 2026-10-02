# Verification record: K-RV2-1b against the frozen code (H-PI-REV2 step-5 amendment)

Lane: H-PI-REV2, wave-20261001-1721pdt. Pure analysis of frozen records and
frozen code; no execution, no implementation, no re-run.

## The frozen definitions (quoted verbatim, not reinterpreted)

1. K-RV2-1b (from the wave-20260929-2321pdt judge record, JUDGE_2321.md
   line 19, enumerating the frozen K-RV2-1 sub-bars): "K-RV2-1(b):
   dsearch over T+F1 returns -1 on the port."
2. K-SB4 (from the frozen step-5 prereg,
   docs/lab/rsi/runs/wave-20261001-1121pdt/pi_rev2/PREREG_PI_REV2_STEP5_BASELINE.md):
   "K-SB4 (correctness parity): the revised procedure is correct on all
   of T (with updated expectations per the frozen conflict rule),
   F1r, and F1r-reuse. B1's fitted program is correct on T+F1r.
   Kill: any misprediction by the revised procedure on T/F1r/F1r-reuse,
   or any misprediction by B1's fit on T+F1r."
3. The frozen code under test: proc_revise2.zag, committed at 847a8f10f,
   file sha256 dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12.
   Extracted from the committed blob and byte-checked identical to that
   sha256 for this verification (written to /tmp, not the working copy).

## What the frozen code does (read directly from the committed source)

- `benum` (lines 179-225) enumerates exactly 1055 programs: 5 terminals
  (t=0..4: K, N, C0, C1, C2), then for each op in {ADD, SUB}: 25 programs
  from (terminal, terminal) pairs, 250 from (terminal, size3) pairs, and
  250 from (size3, terminal) pairs. Total: 5 + 2*(25+250+250) = 1055.
- `dsearch` (lines 252-270) iterates pi=0..pcount-1, checks `prog_fits`
  against every staged sequence, returns the first pi fitting all of them,
  and returns -1 only after all pcount programs have been checked. A -1
  is therefore an exhaustive negative: every enumerated program failed at
  least one staged example. There is no early exit that could produce a
  false -1.
- `eval_prog`/`eval_node` (lines 55-73): each program evaluates to a single
  index per output position, deterministically, as a pure function of the
  program nodes, the output position k, and the input length n. Node
  semantics: K returns k, N returns n, C0/C1/C2 return 0/1/2, ADD/SUB add
  or subtract child values. The evaluator never reads input byte content;
  the output byte at position k is always input[eval_prog(prog, nn, k, n)].
- `prog_fits` (lines 88-94) requires eval_prog(prog, nn, k, n) to equal
  the expected index (the unique input position holding the output byte,
  per `extract_seq`) for every output position k.

## Verification of the impossibility claim (the skeptic's required check)

The wave-20261001-1421pdt debate (DEBATE_1421PDT.md) upheld the
BASELINE-FAIL attribution but recorded a required check: confirm the
inherited K-RV2-1b impossibility claim against the frozen dsearch/benum
code rather than assuming it from a citation, because the whole
attribution rests on it.

Verified against the frozen code:

- For T+F1r, "abc"->"ccc" (n=3) requires eval_prog(prog, nn, 0, 3) = 2
  (the output byte 'c' sits at input index 2, exactly once).
- "rab"->"rrr" (n=3) requires eval_prog(prog, nn, 0, 3) = 0
  (the output byte 'r' sits at input index 0, exactly once).
- Both requirements call eval_prog with identical arguments
  (prog, nn, k=0, n=3). By the frozen eval_node semantics this call
  returns one deterministic value; it cannot be both 2 and 0.
- Therefore no program evaluated by this evaluator can fit both
  examples, regardless of which 1055 programs benum enumerates. The
  impossibility is structural to the frozen evaluator semantics, not an
  artifact of the enumeration, its order, or its instrumentation.

## Verification outcome

K-RV2-1b is VERIFIED against the frozen code. The frozen definition
("dsearch over T+F1 returns -1 on the port") is exactly what the frozen
code produces under the frozen evaluator semantics, and the frozen
evidence (RESULT_PI_REV2.md P3: "no program fits T+F1 (search returned
-1)") matches the frozen definition. The skeptic's attribution challenge
is answered: the -1 is not a baseline implementation bug; it is what the
frozen definitions entail.

Consequence for K-SB4: with K-RV2-1b verified, the frozen step-5 prereg's
K-SB4 clause "B1's fitted program is correct on T+F1r" refers to an
object that provably does not exist under the frozen definitions. The
bar is unsatisfiable as written. This is a design flaw in the frozen
step-5 prereg (it presupposed a B1 fit that the frozen K-RV2-1b
impossibility rules out), not a defect in the revision machinery, which
met every behavioral requirement placed on it (K-SB1/2/3/5/6 PASS per
the step-5 result record). The BASELINE-FAIL verdict of the frozen step-5
execution stands on that attribution and is not changed by this
verification.
