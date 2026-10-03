# E51AJ — Complete fixed-comparison tables

Source `9ea141b050599854783258d82cfa3ee02efb1fad`; run `33952427608`; artifact `9965575939`.

Replica identifiers 0–2 match the native log. Each panel contains 2,160 probes: 1,680 known and 480 no-unique. Counts are not independent replications across checkpoints.

## Primary retention comparison

| Replica | Shared successes | Final loss: sequential | Final loss: replay | Ever lost: seq / replay | Worst loss: seq / replay | Retention direction |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2091 | 1 | 14 | 31 / 24 | 16 / 15 | no |
| 1 | 2081 | 9 | 11 | 35 / 26 | 17 / 15 | no |
| 2 | 2082 | 17 | 6 | 48 / 28 | 20 / 12 | yes |

The rule requires all three replicas. These are fixed checkpoint-0 anchors and checkpoint-32 final losses; no favorable checkpoint is substituted.

## Hybrid and shared learned baselines

| Replica | Baseline | Reachable | Known | No-unique | t=0 success | t=0 wrong commitment |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | Hybrid before residual fitting | 2086 | 1616 | 470 | 1395 | 113 |
| 0 | Shared learned fork | 2091 | 1627 | 464 | 1395 | 118 |
| 1 | Hybrid before residual fitting | 2081 | 1620 | 461 | 1385 | 102 |
| 1 | Shared learned fork | 2081 | 1618 | 463 | 1384 | 105 |
| 2 | Hybrid before residual fitting | 2088 | 1617 | 471 | 1406 | 77 |
| 2 | Shared learned fork | 2082 | 1619 | 463 | 1382 | 168 |

## Every arm at checkpoint 32

| Replica | Arm | Name | Reachable | Known | No-unique | Hybrid lost | Hybrid rescued | t=0 success | t=0 wrong commitment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | sequential | 2098 | 1632 | 466 | 8 | 20 | 1393 | 133 |
| 0 | 1 | replay | 2090 | 1629 | 461 | 18 | 22 | 1393 | 125 |
| 0 | 2 | balanced_mixture | 2091 | 1628 | 463 | 14 | 19 | 1392 | 120 |
| 0 | 3 | continued_A | 2081 | 1625 | 456 | 21 | 16 | 1392 | 118 |
| 0 | 4 | frozen_fork | 2091 | 1627 | 464 | 9 | 14 | 1395 | 118 |
| 1 | 0 | sequential | 2076 | 1618 | 458 | 14 | 9 | 1369 | 151 |
| 1 | 1 | replay | 2074 | 1617 | 457 | 14 | 7 | 1382 | 110 |
| 1 | 2 | balanced_mixture | 2074 | 1617 | 457 | 16 | 9 | 1374 | 132 |
| 1 | 3 | continued_A | 2073 | 1618 | 455 | 21 | 13 | 1388 | 96 |
| 1 | 4 | frozen_fork | 2081 | 1618 | 463 | 7 | 7 | 1384 | 105 |
| 2 | 0 | sequential | 2091 | 1634 | 457 | 26 | 29 | 1312 | 517 |
| 2 | 1 | replay | 2091 | 1626 | 465 | 11 | 14 | 1390 | 167 |
| 2 | 2 | balanced_mixture | 2086 | 1622 | 464 | 9 | 7 | 1394 | 117 |
| 2 | 3 | continued_A | 2103 | 1638 | 465 | 15 | 30 | 1344 | 360 |
| 2 | 4 | frozen_fork | 2082 | 1619 | 463 | 10 | 4 | 1382 | 168 |

Hybrid losses and rescues concern the zero-residual deployable controller, not the learned shared-fork anchor or the evaluator-only union.

## Pointwise retention and actual continued parameter changes

| Replica | Arm | Anchor successes | Ever lost | Regained at final | Missing at final | Never lost | Worst simultaneous loss | Changing blocks | Accepted updates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 2091 | 31 | 30 | 1 | 2060 | 16 | 32 | 12282 |
| 0 | 1 | 2091 | 24 | 10 | 14 | 2067 | 15 | 32 | 10792 |
| 0 | 2 | 2091 | 19 | 9 | 10 | 2072 | 14 | 32 | 10894 |
| 0 | 3 | 2091 | 21 | 2 | 19 | 2070 | 19 | 27 | 2818 |
| 0 | 4 | 2091 | 0 | 0 | 0 | 2091 | 0 | 0 | 0 |
| 1 | 0 | 2081 | 35 | 26 | 9 | 2046 | 17 | 32 | 12232 |
| 1 | 1 | 2081 | 26 | 15 | 11 | 2055 | 15 | 32 | 10857 |
| 1 | 2 | 2081 | 22 | 9 | 13 | 2059 | 15 | 32 | 10902 |
| 1 | 3 | 2081 | 19 | 0 | 19 | 2062 | 19 | 14 | 1604 |
| 1 | 4 | 2081 | 0 | 0 | 0 | 2081 | 0 | 0 | 0 |
| 2 | 0 | 2082 | 48 | 31 | 17 | 2034 | 20 | 32 | 12209 |
| 2 | 1 | 2082 | 28 | 22 | 6 | 2054 | 12 | 32 | 10789 |
| 2 | 2 | 2082 | 15 | 9 | 6 | 2067 | 8 | 32 | 10518 |
| 2 | 3 | 2082 | 17 | 6 | 11 | 2065 | 15 | 32 | 2877 |
| 2 | 4 | 2082 | 0 | 0 | 0 | 2082 | 0 | 0 | 0 |

Ever lost equals regained at final plus missing at final. Regaining a case does not erase its earlier loss. Frozen arm 4 intentionally has zero continued fitting.

## All eight cycle endpoints, with shared fork

| Replica | Checkpoint | Sequential | Replay | Balanced mixture | Continued A | Frozen fork |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 2091 | 2091 | 2091 | 2091 | 2091 |
| 0 | 4 | 2095 | 2095 | 2096 | 2085 | 2091 |
| 0 | 8 | 2097 | 2096 | 2091 | 2086 | 2091 |
| 0 | 12 | 2097 | 2092 | 2093 | 2083 | 2091 |
| 0 | 16 | 2098 | 2094 | 2096 | 2083 | 2091 |
| 0 | 20 | 2098 | 2092 | 2092 | 2083 | 2091 |
| 0 | 24 | 2097 | 2091 | 2089 | 2081 | 2091 |
| 0 | 28 | 2098 | 2087 | 2090 | 2081 | 2091 |
| 0 | 32 | 2098 | 2090 | 2091 | 2081 | 2091 |
| 1 | 0 | 2081 | 2081 | 2081 | 2081 | 2081 |
| 1 | 4 | 2081 | 2080 | 2080 | 2077 | 2081 |
| 1 | 8 | 2082 | 2084 | 2078 | 2073 | 2081 |
| 1 | 12 | 2080 | 2077 | 2074 | 2073 | 2081 |
| 1 | 16 | 2080 | 2078 | 2076 | 2073 | 2081 |
| 1 | 20 | 2079 | 2081 | 2081 | 2073 | 2081 |
| 1 | 24 | 2080 | 2084 | 2075 | 2073 | 2081 |
| 1 | 28 | 2078 | 2077 | 2075 | 2073 | 2081 |
| 1 | 32 | 2076 | 2074 | 2074 | 2073 | 2081 |
| 2 | 0 | 2082 | 2082 | 2082 | 2082 | 2082 |
| 2 | 4 | 2094 | 2089 | 2087 | 2097 | 2082 |
| 2 | 8 | 2091 | 2096 | 2090 | 2099 | 2082 |
| 2 | 12 | 2090 | 2088 | 2087 | 2100 | 2082 |
| 2 | 16 | 2091 | 2089 | 2086 | 2099 | 2082 |
| 2 | 20 | 2090 | 2093 | 2090 | 2099 | 2082 |
| 2 | 24 | 2090 | 2089 | 2091 | 2099 | 2082 |
| 2 | 28 | 2088 | 2086 | 2088 | 2102 | 2082 |
| 2 | 32 | 2091 | 2091 | 2086 | 2103 | 2082 |

The full intervening checkpoints are retained in CURVE.csv; endpoints are not selected winners.

## Fixed final pointwise contrasts

| Replica | Treatment minus control | Paired lost | Paired rescued | Net reachable | Delta known | Delta no-unique | Delta t=0 success | Delta t=0 wrong |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 minus 0 | 13 | 5 | -8 | -3 | -5 | 0 | -8 |
| 0 | 2 minus 0 | 9 | 2 | -7 | -4 | -3 | -1 | -13 |
| 0 | 1 minus 2 | 5 | 4 | -1 | 1 | -2 | 1 | 5 |
| 0 | 3 minus 4 | 19 | 9 | -10 | -2 | -8 | -3 | 0 |
| 1 | 1 minus 0 | 9 | 7 | -2 | -1 | -1 | 13 | -41 |
| 1 | 2 minus 0 | 9 | 7 | -2 | -1 | -1 | 5 | -19 |
| 1 | 1 minus 2 | 3 | 3 | 0 | 0 | 0 | 8 | -22 |
| 1 | 3 minus 4 | 19 | 11 | -8 | 0 | -8 | 4 | -9 |
| 2 | 1 minus 0 | 19 | 19 | 0 | -8 | 8 | 78 | -350 |
| 2 | 2 minus 0 | 27 | 22 | -5 | -12 | 7 | 82 | -400 |
| 2 | 1 minus 2 | 3 | 8 | 5 | 4 | 1 | -4 | 50 |
| 2 | 3 minus 4 | 11 | 32 | 21 | 19 | 2 | -38 | 192 |

The contrasts are replay vs sequential, mixture vs sequential, replay vs mixture, and A-only vs frozen. Pointwise decompositions are descriptive; the primary rule is unchanged.

Correct UNKNOWN choices are included in t=0 success. The separate t0unknown field in CSVs counts unsuccessful UNKNOWN choices. Feasible-state reachability does not establish a learned online stopping policy.
