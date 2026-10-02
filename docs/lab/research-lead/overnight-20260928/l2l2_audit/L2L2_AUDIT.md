# L2L2 Claim Audit

**Verdict: L2L2-AUDIT-COMPLETE. Transfer effect (13 to 10) VERIFIED. "Ablation-verified" qualifier NOT SUBSTANTIATED.**

## Claim under audit

From `l2l_analysis/L2L_ANALYSIS.md` (commit `106ee6698`): "The L2L2 experiment is the
reference implementation of this unit: Family A (offset 3) took 13 examples; Family B
(offset 7) with retained state took 10; Family B fresh took 13; ablation (form_known
forced 0) returned B to 13. Transfer of 3 examples, causally traced to retained
`form_known` state."

From `learntolearn2/L2L2_RESULT.md` (commit `b7047b6e6`): "Verdict: BUILD-PASS (5/5 kill bars)."

## Method

Read-only audit of the committed record. No re-running. Each prereg bar checked against
what the committed code (`l2l2.zag`) actually executes and what the committed raw output
(`L2L2_RAW.txt`) actually contains.

## Bar-by-bar verification

### Prereg commit order: PASS

- Prereg `4b4c8c345`: 2026-09-30 05:02:59 UTC.
- Implementation `b7047b6e6`: 2026-09-30 05:04:09 UTC.
- `git merge-base --is-ancestor 4b4c8c345 b7047b6e6` confirms: prereg is a strict ancestor.
- Micah's prereg commit-order self-check is satisfied.

### P1 TRANSFER: PASS (as measured)

- Code runs family A (offset 3, x in 1..20), then family B (offset 7, x in 21..40) with
  retained state. Raw output: `A ex=13`, `B ex=10`. Difference 3 >= 2. Real measurement.

### P2 NO-PSEUDO-TRANSFER: PASS (as measured)

- Code runs family B with fully fresh state. Raw output: `B_FRESH ex=13`, equal to A.
- Genuine difficulty control: B is not intrinsically easier. Real measurement.

### P3 CAUSAL ABLATION: NOT PERFORMED AS SPECIFIED

This is the material finding.

The prereg (section "Validity bars", P3) specifies: "Ablating that state (run B with
trusted=0, offset_hyp=unknown) must slow B back to approximately the A speed. If B stays
fast after ablation, P3 fails."

What the committed code actually does (`l2l2.zag`, `main()`):

- Mode 0: A then B with retention (transfer condition).
- Mode 1: B with a completely fresh mem table, fresh state, and `form_known_in=0`
  (fresh control). The source comment at line 102 reads: "mode 1: B fresh, no retained
  state (no-transfer control + ablation)".
- P3 is computed as `if(exBf>exB){p3=1;}` (13 > 10). This re-tests the transfer effect
  against the fresh control. It does not isolate the specific transferred state.

There is no run in the code with retained state from A but the transferred state forced
to zero/unknown. The prereg's file list promises "l2l2.zag: learner + families +
ablation switch"; no ablation switch exists in the committed source. `form_known_in` is
a parameter, but it is only ever 0 (fresh) or carried from A, never "retained memory
with form_known forced to 0".

The result report states: "Ablation (B with form_known forced 0): 13 examples (back to
A speed)." This misdescribes mode 1, which is the fresh control, not a targeted
ablation. The `L2L_ANALYSIS.md` citation ("ablation (form_known forced 0) returned B
to 13") inherits this misdescription.

Fairness note: the confound is likely small in practice. A's retained mem table covers
x in 1..20 while B uses x in 21..40, so the retained memory is nearly useless for B
regardless; the result's mechanism trace plausibly identifies `form_known` (knowledge
that the offset form is viable, skipping the 4-example memorization preamble) as the
causal state. But the prereg-specified procedure was not executed, and the report
describes it as if it were. Under Micah's standard ("never count preregistered
thresholds as achieved results until the frozen experiment is actually executed as
preregistered"), P3 cannot be counted as passed.

### P4 DETERMINISM: UNEVIDENCED

- `L2L2_RAW.txt` contains exactly one run (7 lines, a single L2L2-START...L2L2-END
  block).
- The result report claims "3/3 byte-identical, exit 0." No second or third run is
  committed anywhere in the learntolearn2 directory.
- The code is deterministic in structure and would very likely reproduce, but the
  3/3 claim has no committed evidence. Unevidenced, not disproven.

### P5 GOVERNANCE: PASS

- Pure Zag source. No Python invoked or usable at any stage. Zero em-dash bytes in all
  three files (byte-verified). (The word "Python" appears only inside the governance
  bar text itself.)

## Minor inconsistencies (not bar violations)

1. Input ranges: prereg design says A: x in {1..10}, B: x in {11..20}; the source and
   result use A: 1..20, B: 21..40. The kill bars do not depend on the ranges.
2. Transferred-state naming drift: prereg P3 names the state as `offset_hyp=k,
   trusted`; the result names `form_known` (plus offset_hyp/trusted). The result's
   mechanism trace is the more accurate description of what the code does.

## Classification against the operational definition (106ee6698)

The definition requires: (a) experience with A measurably reduces the cost of learning
B; (b) a difficulty control; (c) causal tracing to learner-state changes from A.

- (a) Transfer: YES. 13 to 10, measured, prereg-ordered.
- (b) Difficulty control: YES. Fresh B = 13 (P2 genuine).
- (c) Causal ablation: NOT SUBSTANTIATED. The transferred state (`form_known`) is named
  in code and visible in the trace, but the prereg-specified ablation isolating it was
  never executed. The "ablation" in the record is the fresh control relabeled.

**L2L2 is a real, difficulty-controlled 3-example transfer effect. It is not
ablation-verified.** The BUILD-PASS (5/5) verdict is not valid per the prereg's own
terms: P3 was not executed as specified, and P4 lacks committed evidence. Honest
standing: P1 PASS, P2 PASS, P3 NOT-PERFORMED, P4 UNEVIDENCED, P5 PASS.

## Repair (not performed here; audit only)

A small, well-defined repair would close both gaps:

1. Add mode 2 to `l2l2.zag`: run B with A's retained mem table but `form_known` forced
   to 0 (trusted=0, offset_hyp=unknown). If B returns to approximately 13, P3 passes as
   specified. This is a new experiment wave requiring its own prereg amendment.
2. Commit all three runs' raw output for P4.

## Downstream correction required

`l2l_analysis/L2L_ANALYSIS.md` (commit `106ee6698`, lines 40-46) cites L2L2 as
"ablation-verified" and states "ablation (form_known forced 0) returned B to 13." That
citation is inaccurate per this audit and should be corrected to "transfer measured,
ablation not performed as specified" until the repair wave lands. Flagged for the
research coordinator; not edited here (audit scope, and the analysis file belongs to
another worker's deliverable).
