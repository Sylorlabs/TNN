# CALIBRATION_5100_6100_POLICY.md - repair-time burst regularity

Lane F1-REPAIR2, wave wave-20261001-2321pdt. Read-only inspection
(grep/awk; no probe built, no fresh fixture, no fresh run) of the
20 degenerate-path train traces available before PREREG_REPAIR2:
9 from the 5100-series (F1-FOLLOWUP runs2/1) and 11 from the
6100-series (F1-REPAIR runs4/1). This calibration motivates the
frozen POLICY-R in PREREG_REPAIR2.md section 2; the sealed test
uses fresh 7300-series worlds.

No em-dashes are used in this document.

## Method

Per-trace burst dump: for each TRIGGER line, the episode, buf,
construct count, and the construct list
(op:p1,p2,p3,err_before>err_after). Later bursts are those with
episode > T1 (T1 is 1 or 2 in all 20 traces) and at least one
CONSTRUCT. DOUBLING first construct = op=ADD, p1=0, p2==p3 in
{8,9}.

## Later bursts with at least one construct (28 total)

Complete = last construct err_after=0. Partial = last construct
err_after>0.

| series | seed | ep | buf | first construct | ncon | last err_after | outcome |
|---|---|---|---|---|---|---|---|
| 5100 | 0 | 14 | 8 | ADD r0,r0,f0 | 1 | 27 | partial |
| 5100 | 0 | 23 | 8 | ADD r0,f1,f1 (dbl) | 3 | 0 | complete |
| 5100 | 2 | 4 | 5 | ADD r0,r0,f1 | 1 | 5 | partial |
| 5100 | 3 | 5 | 6 | ADD r0,r0,f1 | 1 | 13 | partial |
| 5100 | 5 | 9 | 8 | ADD r0,r0,f1 | 1 | 25 | partial |
| 5100 | 6 | 3 | 4 | ADD r0,r0,f0 | 1 | 5 | partial |
| 5100 | 6 | 12 | 8 | ADD r0,f1,f1 (dbl) | 3 | 0 | complete |
| 5100 | 12 | 7 | 8 | ADD r0,f0,f0 (dbl) | 3 | 0 | complete |
| 5100 | 13 | 20 | 8 | ADD r0,r0,f0 | 1 | 12 | partial |
| 5100 | 17 | 23 | 8 | ADD r0,r0,f0 | 1 | 28 | partial |
| 5100 | 18 | 3 | 4 | ADD r0,r0,f0 | 1 | 8 | partial |
| 5100 | 18 | 21 | 8 | ADD r0,r0,f0 | 1 | 12 | partial |
| 6100 | 3 | 8 | 8 | ADD r0,r0,f1 | 1 | 29 | partial |
| 6100 | 3 | 18 | 8 | ADD r0,r0,f1 | 1 | 14 | partial |
| 6100 | 4 | 5 | 6 | ADD r0,r0,f0 | 1 | 15 | partial |
| 6100 | 4 | 23 | 8 | ADD r0,r0,f0 | 1 | 16 | partial |
| 6100 | 10 | 3 | 4 | ADD r0,f0,f0 (dbl) | 3 | 0 | complete |
| 6100 | 11 | 12 | 8 | ADD r0,r0,f0 | 1 | 14 | partial |
| 6100 | 12 | 7 | 8 | ADD r0,f1,f1 (dbl) | 3 | 0 | complete |
| 6100 | 13 | 3 | 4 | ADD r0,r0,f0 | 1 | 5 | partial |
| 6100 | 13 | 20 | 8 | ADD r0,r0,f0 | 1 | 12 | partial |
| 6100 | 15 | 3 | 4 | ADD r0,r0,f1 | 1 | 14 | partial |
| 6100 | 15 | 5 | 6 | ADD r0,r0,f1 | 1 | 16 | partial |
| 6100 | 15 | 23 | 8 | ADD r0,f0,f0 (dbl) | 3 | 0 | complete |
| 6100 | 17 | 9 | 8 | ADD r0,r0,f0 | 1 | 17 | partial |
| 6100 | 17 | 14 | 8 | ADD r0,f1,f1 (dbl) | 3 | 0 | complete |
| 6100 | 20 | 12 | 8 | ADD r0,f1,f1 (dbl) | 3 | 0 | complete |
| 6100 | 22 | 10 | 8 | ADD r0,r0,f1 | 1 | 25 | partial |

## Regularity (training knowledge)

- 8/8 complete bursts start with a DOUBLING first construct.
- 20/20 partial bursts start with an accumulator-preserving
  first construct (ADD r0,r0,*), commit exactly one construct,
  and stall with err_after > 0.
- Zero violations of POLICY-R (complete iff doubling-first) on
  all 28 later bursts.
- Per-seed polok = 1 on all 20 D-seeds (6100 seed 5 has no
  later firing burst; vacuously polok=1).
- Corollary (descriptive, not scored): every complete burst has
  exactly the form [double f | ADD r0,r0,COMP(f) |
  ADD r0,r0,COMP(f)] with ncon=3; every partial burst has
  ncon=1.

## Mechanistic gloss (trace-grounded)

The F1 burst loop commits the single best strictly-improving
move per round (up to 4 rounds; F1 IMPLEMENTATION.md /
f1_learn_proto.zag `burst`/`trial_move`, read-only). A
doubling first construct overwrites r0 with f+f, discarding
the degenerate accumulator chain; greedy descent from the
clean doubled base then reaches zero via two complementary
adds (the same 3-construct form that solves non-degenerate
seeds at first trigger). An accumulator-preserving first
construct keeps the degenerate chain; greedy depth-1 then has
no strictly-improving single move (the residual needs a
two-step correction no single ADD achieves), so the burst
ends after one construct. First-trigger bursts are a
different regime (empty graph) and are excluded from
POLICY-R, which covers only t > T1.

## What this calibration does and does not establish

It establishes that POLICY-R is mechanically applicable and
holds 28/28 on the available D-seed later bursts. It does not
establish out-of-sample predictive power; that is the sealed
7300-series test in PREREG_REPAIR2.md Part B.
