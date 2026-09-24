# VERDICT W7 — laundering-hunter PAM (third generation)

Evidence commit: `caf5d9077387d0a5e1468115e33818237420373c`
(prereg `wild/prereg/PREREG_W7.md`, frozen; fixtures frozen per
`wild/tape/TAPE_W7_ADDENDUM.md`, SHAs verified before build.)

## Observed numbers (instrument + independent scorer agree exactly)

- Entries: 200 (100 laundered GEN->EXT, 100 genuine EXT)
- **TPR: 100/100 = 100%** (bar >= 95%)
- **FPR: 0/100 = 0%** (bar <= 5%)
- Score separation: laundered 675..950, genuine 108..546 (no score overlap;
  the prereg's predicted boundary false-flag at genuine corner (650,450,1)
  did not occur in the actual fixture values — measured max genuine = 546)
- Battery: 2x byte-identical,
  SHA-256 `fa92249940f79b60cdc38f545012bf95baa6d99c0975163f25f724d62401ca76`
- KB-W7-L label-blindness audit: PASS (instrument code reads only argv[1]
  and signals columns 0..3; no truth/label/origin/claimed reference;
  signals file confirmed 4 columns/line, no label column)
- D-W7-2 per-signal ablation (scorer-side):
  - sig_c alone (>=600): TPR 85/100, FPR 9/100 — would NOT pass the bars
  - sig_b alone (>=575): TPR 100/100, FPR 0/100
  - sig_a alone (==0): TPR 100/100, FPR 0/100
  - full model (3/2/1, 600): TPR 100/100, FPR 0/100
- D-W7-3: missed laundered = none; false-flagged genuine = none

## Bar evaluation

- KB-W7-D: PASS (TPR 100% >= 95%, FPR 0% <= 5%)
- KB-W7-L: PASS (precise code audit; naive substring audit would have
  false-fired on prose comments — documented in scorer)
- K1: recorded N/A per frozen prereg (W7's wrong-set analog is the
  laundering fixture set, counted in KB-W7-D)
- K2: PASS (2x byte-identical). K3: N/A as throughput bar (detector, not
  admission gate) — TPR/FPR are the judgment metrics, per frozen prereg.
- K4: PASS (stateless O(1) per entry by construction). K5: PASS (terminated).

## Status: SURVIVE

All bars pass. Note from D-W7-2: on this fixture set the behavioral and
attestation signals each suffice alone; content similarity alone does not
pass — the weights' prior (content strongest) is not what carries the
detection here. The full model passes with margin (score gap 546..675).

## Numeric-cap classification (standing law: no arbitrary hard limits)

- Suspicion threshold (existence): LOAD-BEARING (a detector must decide
  somewhere); the VALUE 600 is calibration to the observed score gap ->
  FLAGGED as calibration (robust here: gap 546..675, but still a constant).
- Weights 3/2/1: design prior, values ARBITRARY -> FLAGGED (ablation shows
  the prior ordering does not match the measured signal contributions).
