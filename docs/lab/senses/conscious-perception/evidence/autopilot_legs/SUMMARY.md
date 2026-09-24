# Autopilot legs S1-S4 — measured 2026-09-23

Binary: `tnn-lab/senses/rebuild/a_raw/sense` (Approach A, the current pipeline).
Episodes: 384 (370 primary + 14 new fair-fight fixtures). Byte-identical reruns: 288/288 PASS.

## S1 raw throughput (episodes/sec, bulk clear stimuli)

| task | n | eps/sec |
|---|---|---|
| colorconst | 42 | 1.274 |
| colordisc | 62 | 1.29 |
| motiondir | 62 | 2.367 |
| pitchdisc | 66 | 0.321 |
| shapetrans | 90 | 3.666 |
| timbredisc | 62 | 0.377 |
| **overall** | 384 | **0.765** |

## S2 latency floor (per-episode wall time)

| task | p50 (s) | p95 (s) | max (s) |
|---|---|---|---|
| colorconst | 0.805 | 1.06 | 1.229 |
| colordisc | 0.887 | 1.212 | 1.316 |
| motiondir | 0.402 | 0.679 | 1.108 |
| pitchdisc | 2.983 | 5.531 | 7.6 |
| shapetrans | 0.247 | 0.529 | 0.807 |
| timbredisc | 2.635 | 4.167 | 4.931 |

## S3 no-uncertainty cases (deliberation adds nothing but latency)

Fraction of episodes with autopilot confidence >= 950 AND correct:

| task | conf>=950 frac | conf>=950 & correct frac | accuracy |
|---|---|---|---|
| colorconst | 0.0% | 0.0% | 83.3% |
| colordisc | 0.0% | 0.0% | 48.4% |
| motiondir | 0.0% | 0.0% | 41.9% |
| pitchdisc | 1.5% | 1.5% | 80.3% |
| shapetrans | 0.0% | 0.0% | 100.0% |
| timbredisc | 0.0% | 0.0% | 74.2% |

## S4 compute per episode (ops, deterministic instrumented counter)

| task | ops median | ops min | ops max |
|---|---|---|---|
| colorconst | 8,193 | 4,097 | 8,193 |
| colordisc | 8,193 | 4,097 | 8,193 |
| motiondir | 28,674 | 28,674 | 28,674 |
| pitchdisc | 4,521,065 | 4,521,065 | 5,583,041 |
| shapetrans | 27,651 | 27,651 | 27,651 |
| timbredisc | 2,293,308 | 2,293,308 | 2,824,296 |

## New-fixture baseline (autopilot on the frozen conscious-leg battery)

| fixture | task | judgment | conf | truth | correct | ops |
|---|---|---|---|---|---|---|
| am_c1.img | colordisc | DIFFERENT | 16 | DIFFERENT | True | 4,097 |
| am_p1.pcm | pitchdisc | HIGHER | 19 | HIGHER | True | 5,583,041 |
| il_c1.img | colorconst | DIFFERENT | 90 | SAME_SURFACE | False | 4,097 |
| il_c2.img | colorconst | SAME_SURFACE | 555 | DIFFERENT | False | 4,097 |
| ib_m1.vid | motiondir | E | 500 | W | False | 28,674 |
| ib_m2.vid | motiondir | W | 789 | W | True | 28,674 |
| om_p1.pcm | pitchdisc | SAME | 285 | HIGHER | False | 5,583,041 |
| om_p2.pcm | pitchdisc | SAME | 285 | LOWER | False | 5,583,041 |
| om_p3.pcm | pitchdisc | SAME | 285 | SAME | True | 5,583,041 |
| om_p4.pcm | pitchdisc | HIGHER | 951 | HIGHER | True | 5,583,041 |
| om_t1.pcm | timbredisc | PURE | 272 | BRIGHT | False | 2,824,296 |
| om_t2.pcm | timbredisc | BRIGHT | 491 | BRIGHT | True | 2,824,296 |
| rt_c1.img | colordisc | SAME | 16 | DIFFERENT | False | 4,097 |
| rt_p1.pcm | pitchdisc | SAME | 2 | HIGHER | False | 5,583,041 |

