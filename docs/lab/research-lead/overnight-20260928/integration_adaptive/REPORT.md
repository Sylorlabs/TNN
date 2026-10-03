# REPORT: consequence-learned decision policy (integration_adaptive)

Verdict: **INTEGRATION-ADAPTIVE-COMPLETE**. All four frozen kill bars pass on
all 3 seeds. Pure Zag, safebin toolchain, zero forbidden executables.

## What was built

`adapt.zag` (271 lines): three decision-making arms run on paired world
draws (identical random streams per arm per run), 5 regimes x 400 rounds =
2000 rounds per arm. Each round presents an observable stake cue (HIGH/LOW)
plus learner-maintained reliability records (sliding 40-window per channel);
the arm chooses TRUST_SOURCE, TRUST_PREDICTOR, or WITHHOLD; the evaluator
then reveals both channels and applies the frozen consequence schedule
(correct +10; wrong -20 HIGH / -5 LOW; withhold when an answer would have
been correct -4 missed opportunity; withhold when both would have been
wrong +2 saved error).

- ADAPT: learner-owned Q-table (6 context cells x 3 actions, fixed-point),
  context = (stake, sign(pred_rate - src_rate)) with exact-equality tie and
  no threshold constant anywhere in the decision path; epsilon-greedy argmax
  (epsilon 0.05, deterministic xorshift); delta update Q += 0.1*(r-Q).
- AND: fixed gate, answer iff both rates > 0.70. OR: fixed gate, answer iff
  either rate > 0.70. Baselines only.

## Results (3/3 seeds)

| Seed | ADAPT | AND | OR | K1 | K2 diff | K3 TP frac |
|------|-------|-----|----|----|---------|------------|
| 11 | 8588 | -1771 | 7346 | PASS | 313/400 (0.78) PASS | 191/200 (0.955) PASS |
| 22 | 8827 | -1946 | 7435 | PASS | 334/400 (0.84) PASS | 189/200 (0.945) PASS |
| 33 | 9352 | -1466 | 7485 | PASS | 306/400 (0.77) PASS | 195/200 (0.975) PASS |

- K1: adaptive total beats both fixed gates on every seed.
- K2 (stake adaptivity): identical accuracy regimes R4 (HIGH) and R5 (LOW,
  both 0.55/0.55) produce opposite policies: R4 withholds (319/400 in seed
  11), R5 answers (394/400). Fixed gates score exactly 0 on this contrast
  (AND: 0/0; OR: 54/1) because they cannot condition on stakes.
- K3 (RSV redteam scenario, R3: perfect predictor + adversarial source):
  adaptive learns TRUST_PREDICTOR at 0.95 in the second half, where the AND
  gate withholds all 400 rounds (score -1600 vs adaptive +3310 in seed 11).
- K4 (audit): the adaptive decision path (`ctx_cell`, `adapt_decide`)
  contains no threshold constant and no AND/OR combination of signals; the
  only comparisons are the order relation sign(pred_ones - src_ones).
  Gates exist solely in the baseline arms and in the evaluator's frozen
  consequence schedule, never in the learner's decision.

Adaptation across regime shifts is visible in the behavior table (seed 11):
R1 answers (379 TS), R2 trusts source (345 TS), R3 trusts predictor
(369 TP), R4 withholds (319 W), R5 answers again (394 answered). The
(HIGH,TIE) cell is even trained toward ANSWER by the R1->R2 transition and
later revised toward WITHHOLD by R4 consequences: revision, not just
accumulation.

## Implementation notes (transparent)

1. Memory-layout bug, caught before any verdict: the first build overlapped
   arm 2's state block with arm 0's stats block (garbage totals). Fixed by
   re-laying blocks disjointly; all reported runs use the fixed binary.
2. K3 denominator bug, corrected to match the frozen prereg text: the code
   checked count >= 280 (0.70 of 400) but the prereg specifies the fraction
   over R3 rounds 200..399 (200 rounds), i.e. count >= 140. The frozen bar
   (fraction >= 0.70) is unchanged; the implementation now computes exactly
   what the prereg says. Raw counts are in the run files for verification.
3. Determinism: rerun of the seed-11 binary is byte-identical
   (`run1b.txt`, cmp clean).

## Architecture accounting

- Cognition lines added: 271 (one self-contained file; no TNN-2 source touched).
- New modes / bridges / handlers / semantic cases: 0.
- Researcher-owned: consequence schedule, regime schedule, action set,
  delta update rule, epsilon, window length, context features, stake cue.
- Learner-owned: all Q values, window contents, derived rates, context
  computation, every decision, and the regime-shift revisions.
- This is an UNFROZEN precursor experiment: the world is synthetic Bernoulli
  streams, not live TNN subsystems. It establishes that consequence-driven
  policy learning can replace hardcoded gates in principle; integration into
  the continuing learner is follow-up work.

## Bounds and next steps

- The update rule and exploration schedule are researcher-authored (same
  standing as C182's update rule); only the policy content is learned.
- Counterfactual feedback (would-be correctness when withholding) is
  evaluator-provided; a deployed learner needs a real delayed-truth path.
- Next: replace epsilon-greedy with uncertainty from the consequence
  substrate itself; merge this policy table into the shared tag-61 substrate
  (compression with C185/RSV); test misleading-stake cues and adversarial
  consequence delay.

## Files

- `adapt.zag` (canonical source), `adapt_s2.zag`, `adapt_s3.zag`
  (seed variants, sed-generated), binaries `adapt_s1/2/3`
- `run1.txt`, `run2.txt`, `run3.txt`, `run1b.txt` (determinism evidence)
- `compile.log`, `PREREG.md`, `NAMECHECK.md`, `REPORT.md`
