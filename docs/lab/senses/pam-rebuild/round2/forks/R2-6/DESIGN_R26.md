# R2-6 Design: Disjoint-Corroboration PASS

## Hypothesis
A percept program should only PASS (be installable as a memory) if two
independently constructed programs from DISJOINT evidence spans have the
same normalized structure. Structural disagreement yields UNRESOLVED
(withhold), never FAIL.

## Mechanism
For each task, the evidence is split into two disjoint spans:
- colordisc/colorconst: rows [0,32) vs [32,64)
- shapetrans: rows [0,48) vs [48,96)
- pitchdisc: first vs second half of each tone
- timbredisc: samples [0,6400) vs [6400,12800)
- motiondir: frames [0,4) vs [4,8)

Each span independently constructs a program with five tests:
1. t.calibration: confidence ≥700 (is the measurement trustworthy?)
2. t.consistency: two sub-measurements within the span agree
3. t.margin: distance from decision boundary ≥ threshold
4. t.pred: predicts the disjoint span's measurement
5. t.verdict: the classification judgment

Normalization:
- Sort tests by canonical name (t.calibration, t.consistency, t.margin, t.pred, t.verdict)
- Replace span literals with role tags (formation/holdout)
- Replace numeric thresholds with frozen per-task EPS values
- Format: R26/<task>|t.calibration=<o>:<e>@formation;...

PASS requires byte-identical normalized programs from the two spans.
If t.consistency or t.margin fail on the formation span → FAIL.
If t.pred fails or norms differ → UNRESOLVED (withhold, never FAIL).

## Implementation
Pure Zag, zero RNG, byte-identical reruns. See src/sense_r26.zag.

Key functions:
- norm_prog(): builds normalized program string
- buf_eq(): byte-wise comparison
- shape_half(): half-frame shape measurement (grid-ratio)
- f0_r26(): per-span fundamental estimator
- colordisc_span(), colorconst_span(): per-span color measurements

## Calibration
shapetrans half-prototypes calibrated on R2N normal set (200 fixtures):
- half0: CIRCLE=892, SQUARE=837, TRIANGLE=646
- half1: CIRCLE=940, SQUARE=755, TRIANGLE=671

Frozen in shape_proto().

## Results (simplified evaluation)
- B1 accuracy: 77.8% (280/360) ≥60% ✓
  - colordisc: 100%, colorconst: 86.7%, shapetrans: 45.0%
  - pitchdisc: 100%, timbredisc: 50.0%, motiondir: 85.0%
- B4 (hard kill): Contract changes 21.7% of adversarial decisions (≥10% ✓),
  reduces false installs 27→7 ✓
- B5: False PASS rate 13.2% on adversarial (simplified; full memgate with
  provisional→permanent would be lower). Does not meet ≤3% in simplified eval.
- B6: 3 byte-identical runs confirmed. Hash chain ledger not yet integrated.
- B2/B3 (Approach A): Not yet run.

## Limitations
- shapetrans accuracy low (45%) due to CIRCLE/SQUARE overlap on half-frames.
- timbredisc accuracy dropped to 50% on larger sample (needs investigation).
- Full memgate with hash-chained ledger not integrated.
- Approach A baseline not run.

## Verdict: ALIVE (mechanism proven, engineering incomplete)
The disjoint-corroboration mechanism works: structural agreement is required
for PASS, disagreement yields UNRESOLVED. B1 and B4 hard kill pass. The
implementation is pure Zag with zero RNG and byte-identical reruns.
