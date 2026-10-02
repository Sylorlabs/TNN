# CALIBRATION_5100_REPAIR.md - repair-signature calibration on training data

Lane F1-REPAIR, wave wave-20261001-2321pdt. Calibration performed
2026-10-02 ~00:05 PDT on the 24 committed 5100-series train traces
(F1-FOLLOWUP runs2/1, read-only inspection with grep; no fresh
fixture generated, no fresh learner run executed, no probe built
yet). This calibration informed the frozen signature definition in
PREREG_REPAIR.md; the sealed test uses fresh 6100-series worlds.

No em-dashes are used in this document.

## Trace grammar (observed, all 24 traces)

- `TRIGGER <ep> winfail=<f> win=<w> buf=<b>`
- `CONSTRUCT <ep> <k> NODE id=<id> op=ADD p1=<a> p2=<b> p3=<c> err_before=<e0> err_after=<e1>`
- `STALL <ep> nodes=<n> buf_err=<e>`
- `EXEC main 24`, `SUMMARY ...`

Operand codes observed: 0 = accumulator r0, 8 = feature f0, 9 =
feature f1. Every first construct doubles one feature
(ADD r0,f,f with p2 == p3).

## Degenerate second construct (trace-mechanical)

c0 = first CONSTRUCT of the first-trigger burst: op=ADD, p2 == p3
(call it f). c1 = second CONSTRUCT of the first-trigger burst.
c1 is degenerate iff op=ADD, p1 == 0, and neither c1.p2 nor c1.p3
equals COMP(f), where COMP swaps 8 and 9. This covers both
observed degenerate forms: re-add of the same feature
(ADD r0,r0,f) and accumulator doubling (ADD r0,r0,r0). The
complementary add (ADD r0,r0,COMP(f)) is not degenerate.

5100-series classification:

| seed | c0 doubles | c1 form | degenerate? | label |
|---|---|---|---|---|
| 0 | f1 | r0+r0 | yes | CORRECT |
| 1 | f0 | +f1 (complement) | no | CORRECT |
| 2 | f0 | +f0 (re-add) | yes | OVERFIT |
| 3 | f0 | +f0 (re-add) | yes | OVERFIT |
| 4 | f1 | +f0 (complement) | no | CORRECT |
| 5 | f0 | r0+r0, burst to err 0 | yes | OVERFIT |
| 6 | f1 | +f1 (re-add) | yes | CORRECT |
| 7 | f0 | +f1 (complement) | no | CORRECT |
| 8 | f0 | +f1 (complement) | no | CORRECT |
| 9 | f1 | (single construct, err 0) | no | CORRECT |
| 10 | f1 | +f0 (complement) | no | CORRECT |
| 11 | f1 | +f0 (complement) | no | CORRECT |
| 12 | f0 | r0+r0 | yes | CORRECT |
| 13 | f1 | +f1 (re-add) | yes | OVERFIT |
| 14 | f0 | +f1 (complement) | no | CORRECT |
| 15 | f0 | +f1 (complement) | no | CORRECT |
| 16 | f1 | +f0 (complement) | no | CORRECT |
| 17 | f1 | r0+r0 | yes | OVERFIT |
| 18 | f1 | +f1 (re-add) | yes | OVERFIT |
| 19 | f1 | (single construct, err 0) | no | CORRECT |
| 20 | f1 | +f0 (complement) | no | CORRECT |
| 21 | f0 | +f1 (complement) | no | CORRECT |
| 22 | f0 | +f1 (complement) | no | CORRECT |
| 23 | f0 | +f1 (complement) | no | CORRECT |

D (degenerate-path) seeds: 0, 2, 3, 5, 6, 12, 13, 17, 18 (9 seeds).

## Repair-burst signature on the D subset (training)

REPAIR-BURST event: TRIGGER at t > T1 with buf=8, burst with >= 1
CONSTRUCT, last CONSTRUCT of the burst with err_after=0.

| seed | repair episodes (buf=8, to err 0) | S | label | hit |
|---|---|---|---|---|
| 0 | 23 | 1 | CORRECT | yes |
| 2 | none (later bursts stall or partial) | 0 | OVERFIT | yes |
| 3 | none (TRIGGER 5 has buf=6) | 0 | OVERFIT | yes |
| 5 | none (TRIGGER 9: 1 construct 26->25, stall) | 0 | OVERFIT | yes |
| 6 | 12 | 1 | CORRECT | yes |
| 12 | 7 | 1 | CORRECT | yes |
| 13 | none (TRIGGER 20: 1 construct 13->12, stall) | 0 | OVERFIT | yes |
| 17 | none (TRIGGER 23: 1 construct 30->28, stall) | 0 | OVERFIT | yes |
| 18 | none (TRIGGER 21: 1 construct 14->12, stall) | 0 | OVERFIT | yes |

Conditioned rule (S=1 predicts CORRECT): 9/9, zero counterexample
pairs within D. The full-buffer requirement (buf=8) is load
bearing: seed 3's TRIGGER 5 (buf=6) does not count. The
to-zero requirement is load bearing: partial constructs that
stall (seeds 5, 13, 17, 18) do not count.

## What this calibration does and does not establish

It establishes that the frozen signature definition is
mechanically applicable and perfectly separates the training
D subset. It does not establish out-of-sample predictive power;
that is the sealed 6100-series test. The definition was not
tuned beyond the task's wording ("a later full-buffer trigger
that revises the degenerate construct", operationalized as
buf=8 plus burst-to-zero in pure buffer-error terms).
