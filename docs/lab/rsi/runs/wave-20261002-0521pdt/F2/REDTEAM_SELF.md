# SELF RED TEAM: F2 v6 (wave-20261002-0521pdt)

Date: 2026-10-02. Builder self red-team for PREREG_F2V6.md (frozen,
amended once transparently for NC5). Verdict: (to be recorded).

## Attack axes

### 1. Knowledge-vs-architecture confounds

Q: Does the learner contain shift-specific knowledge?
A: No. The revision loop is regime-agnostic: it triggers on
prediction-vs-observation contradiction under a converged single
survivor, with no representation of "regime", "shift", or "latch".
The latch thresholds (setup calls #1, #23) are world-side hidden state;
the learner never reads the setup counter or regime flag (packed cell
is world-internal). Source audit: no S2_* references in the learner;
the learner calls only the w_* interface. The fixed-point stop compares
canonical rule bytes, not regime labels.

Q: Is the world tuned for the learner?
A: NC3 guards this: the pristine v5-base (one-revision cap) must FAIL
on SHIFT2. If v5-base passed, the world would not be a genuine
double-shift test (VOID). (Result below.)

### 2. Metric gaming

Q: Could the learner pass the bars without genuine revision?
A: K6-R4 requires: wave-1 conv=1 AND wave-1 plan fails for real with
logged contradiction AND exactly two revisions AND wave-2 conv=2 AND
wave-2 plan fails with contradiction AND wave-3 conv=3. Each revision
is gated on a logged PRED_VS_ACTUAL mismatch. A learner that "games"
by revising without contradiction would fail K6-R3 (revision without
logged contradiction). A learner that gets lucky would fail K6-R5's
0/20 random control or the 3-wave conv sequence.

Q: Could the fixed-point stop be gamed?
A: The stop triggers only when re-converged laws byte-match a previous
wave's. This is a safety terminator, construction-validated; it was not
hit in eval (each wave converged to new laws).

### 3. Goal-weakness (is the goal actually sustained/hard?)

Q: Is double-shift genuinely harder than single-shift?
A: Yes, structurally: v5's fixed one-revision cap provably cannot
survive two shifts (NC3). The goal requires THREE outcome-linked waves
over a horizon, each caused by the previous wave's failed execution.
This is sustained multi-wave experiment construction, not a longer
single wave.

Q: Are the shifts "the same trick twice"?
A: Both lengthen Y2's delay progressively (2->3->4). Same-type shifts
isolate the tested variable (revision count); varying shift type
simultaneously would confound. The hardness is in the loop, not the
shift variety.

### 4. Presentation fabrication

Q: Are the numbers real?
A: 3/3 byte-identical runs per world (cmp-verified). No RNG in decision
paths. Binary exit codes (not just logs) adjudicate PASS/FAIL. All
binaries built from committed source via build.sh (pure Zag, safebin).

### 5. Implementation risks

- Packed t-cell overflow: t<1000, sc<1000, reg<=3; tc<3.1M<2^31. Safe.
- Latch miscount: assumes 22 setups/wave (2 goal-phase + 20 control).
  Verified in logs (setup counts). If a wave found no plan, the count
  would differ, but plans are found in all waves (verified).
- 11-action planning cost: inherent to maxd=4; wall-clock reported.

## Results

- NC3 (v5-base on SHIFT2): PROGRAM_FAIL (exit=1), m2=59, w1disc=35.
  VOID CONDITION SATISFIED. The world is a genuine double-shift test.
- NC4 (v6 on SHIFT1): PASS (PROGRAM_ALL_BARS_PASS, nrev=1, mask 63).
  Exactly one revision; no over-revision.
- NC5 (v6 on OSC): PASS (PROGRAM_ALL_BARS_PASS, nrev=1, mask 63).
  Amended expectation confirmed.
- NC2: RESULT 0. PASS.
- K6-R8: PASS on A-prime and C2-prime (mask 63, nrev=0). No spurious revision.
- Sealed SHIFT2: PARTIAL. Wave 1 (conv=1, plan fails, revision),
  Wave 2 (conv=2, plan fails, revision), Wave 3 (conv=3).
  Wave-3 11-action planning incomplete due to CPU contention.
  K6-R4: conv 1/2/3 YES, 2 revisions YES, wave-3 goal UNVERIFIED.
