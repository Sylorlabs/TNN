# R32 E53 — Native Conservative Average-Cost Joint Policy Result

Date: 2026-08-30  
Status: `EXECUTED_VALID_NATIVE_NEGATIVE — CONSERVATIVE CONTINUATION WORKS, JOINT FEASIBILITY/CAPACITY BLOCKED`  
Canonical: **R27 step 60,423**  
Preregistration: `R32_E53_CONSERVATIVE_AVERAGE_COST_PREREG.md`, frozen in GitHub before execution at branch commit `191f10feac1e08cfcdde0b90f2c797e5c1788a24` (prereg blob `a9d8d648c2fb47de607f71dd22e8aa95173cdbaf`).

## Native authority and reproducibility

- maintained experiment/cognition language: **Zag v2 native**
- official persisted Linux x86-64 compiler SHA-256: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- assembled source SHA-256: `c07446f1b7dbe823facc77e0dac68cafbb8a2b8e4a43a06d1a047dcc8ca45f9f`
- core SHA-256: `6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0`
- independent build 1 SHA-256: `d1b5ad0cd9c0a123ee65d75088670c1e6995b4959bd80223071f7bc6d3caa77a`
- independent build 2 SHA-256: `d1b5ad0cd9c0a123ee65d75088670c1e6995b4959bd80223071f7bc6d3caa77a`
- binaries byte-identical: **PASS**
- native raw ledger SHA-256: `ceb7b288ae8dc7bb55d970d4ffafecb6c199ef594aae67066828ac2435a00da5`
- independent native rerun raw ledger SHA-256: `ceb7b288ae8dc7bb55d970d4ffafecb6c199ef594aae67066828ac2435a00da5`
- full raw outputs byte-identical: **PASS** (124,345 lines each)
- rerun wall time: **395.187769827 s**
- rerun exit code: **1**, expected because the preregistered validation gate failed
- stderr: empty

## Integrity / allocator

- E50 parent integrity: PASS
- legacy E51B development seed assignment failures: 0
- E53 expanded RNG namespace modulus: 2,000,003
- expanded allocator failures: 0
- expanded manifest hash: 719401809
- validation allocated: 2,700
- sealed confirmation allocated: 5,400
- sealed confirmation executed: **0**
- naive fit identity: PASS
- conservative C fit/stability: PASS/PASS
- conservative D fit/stability: PASS/PASS
- overall integrity gate: **PASS**

## Development behavior

Aggregate columns are: episodes, success, UNKNOWN, wrong, known, no-unique, observations, opportunity loss, utility, continued episodes, known success, known wrong, no-unique UNKNOWN, no-unique wrong.

| Arm | Utility | Observations | Opportunity loss | Known success | Known wrong | No-unique UNKNOWN | No-unique wrong |
|---|---:|---:|---:|---:|---:|---:|---:|
| A terminal control | 254,600 | 0 | 0 | 1,015 | 166 | 363 | 357 |
| B naive on-policy | -150,058 | 7,390 | 1,096,458 | 1,360 | 28 | 422 | 298 |
| C conservative continuation | **421,543** | 1,242 | 137,257 | **1,062** | **50** | 384 | 336 |
| D conservative joint, E52A initialization | 284,600 | 0 | 0 | 997 | 142 | 363 | 357 |

C accepted three learner-selected conservative updates:

1. utility 355,166; 1,694 observations; damping 1/2; shadow 0;
2. utility 415,937; 1,126 observations; damping 1/4; learned shadow 268;
3. utility 421,543; 1,242 observations; prior-replay weight 7; damping 1/8; learned shadow 212.

This directly falsifies the E52B conclusion that on-policy continuation necessarily causes cost explosion: conservative replay/rollback plus learner-updated resource price recovered substantial positive development utility.

D accepted **zero** updates. Its E52A-initialized terminal incumbent began with only 997 known successes versus the frozen safety baseline's 1,015, so it began outside the optimizer's own feasible non-inferiority set.

## Fresh validation

| Arm | Net utility | Continued episodes | Observations | Opportunity loss | Known success | Known wrong | No-unique UNKNOWN | No-unique wrong |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A terminal control | 169,400 | 0 | 0 | 0 | 833 | 153 | 302 | 298 |
| B naive on-policy | -146,047 | 1,467 | 6,323 | 915,847 | 1,121 | 25 | 349 | 251 |
| C conservative continuation | **321,320** | 649 | 1,103 | 119,280 | **875** | **48** | 318 | **282** |
| D conservative joint | 198,000 | 0 | 0 | 0 | 820 | 134 | 305 | 295 |

C is the strongest behavioral result in E53: versus A it gained **+151,920 net utility**, +42 known successes, removed 105 known wrong commits, and reduced no-unique wrong commits by 16 while using 1,103 observations. It did so without the oscillation/cost explosion of B.

However C is not the preregistered primary joint treatment and still leaves 282/600 no-unique episodes as wrong commitments.

D beat A and B on net utility and reduced no-unique wrong commitments slightly, but failed known-success non-inferiority (820 < 833) and made no continuation decisions.

## Reachability / safety

- A no-unique episodes with no reachable UNKNOWN: 30
- D no-unique episodes with no reachable UNKNOWN: 28
- A known episodes with no reachable correct terminal action: 1
- D known episodes with no reachable correct terminal action: 1
- terminal reachability gate: PASS
- no-unique improvement gate: PASS
- strict every-cell no-unique safety: **FAIL**
- all 60 populated no-unique cells retained at least one wrong commitment in D
- nontrivial D continuation behavior: **FAIL**
- known non-inferiority: **FAIL**

## Gate outcome

- integrity: PASS
- positive/net-superior utility: PASS
- known non-inferiority: FAIL
- aggregate no-unique improvement: PASS
- strict every-populated-cell no-unique safety: FAIL
- nontrivial D continuation: FAIL
- terminal reachability improvement: PASS
- confirmation earned: **NO**
- confirmation executed: **0**

Native outcome: `NO_VALIDATED_CONSERVATIVE_AVERAGE_COST_RESCUE`.

## Scientific interpretation

E53 establishes two things simultaneously:

1. **The E52B oscillation/cost problem is tractable.** A generic conservative learner can use replay, rollback, damping, and a learned observation shadow price to produce a stable, cost-effective continuation policy.
2. **The tested joint terminal+continuation optimizer is confounded by its incumbent geometry.** It starts from the E52A terminal coefficients even though that incumbent already violates the frozen known-success safety floor, and no local joint update crosses back into the feasible set.

The result does **not** justify adding a researcher-authored ambiguity rule. It justifies the already-preregistered E54 feasible-root discriminator: start the same E52A learner-selected terminal basis at zero coefficients (the safe control point), then let TNN grow terminal and continuation value conservatively from that feasible root.

R27 remains canonical. No confirmation or R27 dominance test was earned.
