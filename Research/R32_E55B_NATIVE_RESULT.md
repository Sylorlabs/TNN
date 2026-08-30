# R32 E55B — Native Coordinate-Separable Joint Validation Result

Date: 2026-08-30  
Status: `EXECUTED_VALID_NATIVE PARTIAL POSITIVE — COORDINATE JOINT GENERALIZES; STRICT NO-UNIQUE SAFETY REMAINS`  
Canonical: **R27 step 60,423**  
Confirmation executed: **0**

## Native authority

- full native Zag v2 source SHA-256: `a99b4eef0a2870ea0aff9278900b302048492deb56c0c19e158ee8a13761161a`
- persisted compiler SHA-256: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- byte-identical build SHA-256: `6c0cf4c5183aa4db18929d1e0a6db91b7b2e0afa6161ded74a1f45c9f9db6e9c`
- raw ledger SHA-256: `ec644241933dfb9c9fa5600f3c7110ac854e9e1f857986a9b0508156aeb1a8cf`
- stderr empty
- wall time: 375.219910283 s
- exit code: 1 because strict validation gate failed
- fresh namespace modulus: 2,140,001
- allocator failures: 0
- namespace manifest hash: 1349907567
- terminal fit forward/reverse identity: PASS
- frozen E55A fit vector reproduction: PASS
- frozen 1/4 coefficient vector reproduction: PASS
- C stability/fit: PASS
- overall integrity: PASS

## Frozen coordinate policy

C continuation reproduced with development utility 421,543. E55A's terminal fit and selected 1/4 vector reproduced exactly:

`[-1221, 51, 288, 28, -55, 461, -210, 9]`

D development utility reproduced at 496,943 with 1,071 known successes, 18 known wrong, and 334 no-unique wrong.

## Fresh validation

| Arm | Net utility | Continued | Observations | Opportunity loss | Known success | Known wrong | No-unique UNKNOWN | No-unique wrong |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A terminal control | 224,600 | 0 | 0 | 0 | 855 | 140 | 308 | 292 |
| B naive on-policy | -147,940 | 1,507 | 6,312 | 951,540 | 1,148 | 27 | 358 | 242 |
| C conservative continuation | 340,130 | 656 | 1,100 | 126,670 | 898 | 53 | 329 | 271 |
| D coordinate joint | **409,730** | 656 | 1,100 | 126,670 | **896** | **16** | 327 | 273 |

D versus A:

- +185,130 net utility;
- +41 known successes;
- -124 known wrong commitments;
- -19 no-unique wrong commitments;
- 656 episodes use continuation, so behavior is selective rather than always-stop/always-continue.

D versus C:

- +69,600 net utility at exactly the same observation/opportunity cost;
- -37 known wrong commitments;
- known success changes by -2;
- no-unique wrong changes by +2.

Thus the terminal coordinate adds substantial general value after the continuation policy is stabilized.

## Reachability and gates

- A no-reachable UNKNOWN: 33
- D no-reachable UNKNOWN: 29
- A no-reachable correct: 1
- D no-reachable correct: 2
- combined terminal reachability gate: PASS
- net utility superiority over A/B/C: PASS
- known non-inferiority: PASS
- aggregate no-unique improvement versus A: PASS
- nontrivial continuation: PASS
- integrity: PASS
- **strict every-populated-no-unique-cell safety: FAIL**
- all 60 populated no-unique cells still contained at least one wrong commitment
- confirmation earned/executed: 0/0

Native outcome: `NO_VALIDATED_COORDINATE_SEPARABLE_JOINT_RESCUE` only because the strict full validation conjunction was not satisfied.

## Scientific interpretation

E55B establishes that the coordinate-separable architecture is materially better than the coupled E53/E54 optimizer and generalizes to a fresh evaluator namespace. The remaining dominant failure is selective stopping under no-unique evidence: 273/600 no-unique validation episodes still end in wrong commitments even though UNKNOWN is reachable in most trajectories.

That residual is large enough that another tiny hand-selected interaction is not justified. The next phase should let TNN grow a substantially larger **generic sparse continuation connectivity graph** from its own delayed-value residuals, while full-development utility/safety decides which connections survive. This is the first controlled step toward learner-owned structural plasticity; it should be development-only before any fresh validation is consumed.

R27 remains canonical and confirmation remains sealed.
