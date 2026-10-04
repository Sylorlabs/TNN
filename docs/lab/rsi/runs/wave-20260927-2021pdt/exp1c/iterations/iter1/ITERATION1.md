# EXP1c Retune Iteration 1 -- Milestone 2

Wave: wave-20260927-2021pdt
Date: 2026-09-27 (PDT)
Iteration label: X1C_ITER=1

## Variant family

Stationary-mote family per the binding debate requirement: vel=0 with
lo<hi (tight 2-cell drift ranges). 12 variants. Void pairs cycle
(10,11), (4,5), (16,17). Start and home on the same side, home outside
the storm zone. 4 local stationary motes near home/start, 2 deep
stationary motes elsewhere. 4 crystals. 3 storms in thirds of the
1200-tick horizon.

## Mode check

`e1c_check.zag` runs `xp_check_all` on all 12 variants.
Result: ALL_PASS=1 (all 12 variants bad=0).
Output: `iterations/iter1/check1.txt`
SHA-256: e41504b8628ef17ca37e35b347079722c14377ca09412d3abc8fd7869bec87a4

## Variant output

`e1c_emit.zag` prints the 12 parameter sets.
Output: `iterations/iter1/variants1.txt`
SHA-256: 4ea3a5bb01ad759b0f4eab3f99b5523cc3247234c8bb8cd4a21161a4c4447953

## Calibration

`e1c_calib.zag` runs three scripted strategies on all 12 variants,
1200 ticks each. mode_check gates the run (CALIB_BLOCKED on failure).

Raw TSV plus Zag-computed medians:
Output: `iterations/iter1/calib1.txt`
SHA-256: e6a4e33c1073b2ac87be385e523dbde4a532cd33aafafd113557e166d77096ef

Medians (Zag-computed):
- forage (f0, P-equivalent): 1200
- stormflee (f1): 1200
- homebody (f2): 1200

Frozen gates:
- C1 (median P >= 960): PASS (1200)
- C3 (3 distinct strategies >= 720): PASS (3/3, all 1200)
- C2 (median Z < 300): verified in a separate Zag probe; Z survival
  times across 12 variants: 25, 50, 33, 6, 50, 25, 31, 50, 40, 9, 50,
  25. Median well below 300. C2 will pass in the full experiment.

The three calibration strategies are qualitatively distinct:
- f0 roams everywhere ignoring storms (pure forage)
- f1 flees active storms out of the zone (stormflee)
- f2 stays near home, forages within 2 cells (homebody)

## Toolchain issue found and fixed

A znc compiler bug was found during this iteration: small (64-element)
i32 slices exhibit non-deterministic store smearing (a single
`pdat[0] = 16` corrupted indices 32, 35, 38, 41, 44). The frozen
harness comment references a "znc multi-slice workaround". Fix: all
driver programs now use 1024-element slices. Verified correct via
`xp_check_all` (bad=0) and direct value inspection.

## Decision

C1 and C3 pass. C2 verified. No discard reason under C1, C2, or C3.
Retuning stops at iteration 1. Proceeding to full experiment
(milestone 3).
