# R32 E54 — Native Feasible-Root Joint Policy Result

Date: 2026-08-30  
Status: `EXECUTED_VALID_NATIVE_NEGATIVE — ZERO-ROOT DOES NOT UNBLOCK JOINT UPDATES`  
Canonical: **R27 step 60,423**

## Causal change

E54 changed only the joint-arm initialization from the full E52A terminal coefficients to zero coefficients on the same E52A learner-selected pair identities. This started D exactly at the frozen safe terminal control. Validation used the fresh preregistered evaluator namespace modulus 2,100,001.

## Native authority

- maintained cognition/experiment: full native Zag v2
- compiler SHA-256: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- source SHA-256: `17c1aa0d4d336ee23fc64d22acf17c05af44d8abaa24dec7e3a7c206d03ec500`
- build 1 SHA-256: `a1bf59a7c8b89327bd9815ed1c5a276974df5a66fc958ed67b246dd2b161d200`
- build 2 SHA-256: `a1bf59a7c8b89327bd9815ed1c5a276974df5a66fc958ed67b246dd2b161d200`
- byte-identical binaries: PASS
- raw ledger SHA-256: `d8b12a3952de09fc7173cff6dd55745327d82dbcc5838d7d3c1d6414eb9f9e76`
- stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty)
- wall time: 387.146358638 s
- exit code: 1, expected failed validation gate

## Integrity

- E50 parent integrity: PASS
- expanded allocator failures: 0
- E54 namespace manifest hash: 1179930065
- validation allocated: 2,700
- sealed confirmation allocated: 5,400
- confirmation executed: 0
- C/D fit identity and deterministic stability: PASS
- overall integrity: PASS

## Development

E54 reproduced E53's conservative continuation result exactly:

- A utility: 254,600
- B naive utility: -150,058
- C conservative utility: **421,543**, 1,242 observations, 137,257 opportunity loss, 1,062 known successes, 50 known wrong, 336 no-unique wrong.

The key E54 result is D:

- feasible-root joint initial utility: 254,600
- terminal coefficients at start: all zero
- accepted conservative rounds: **0**
- final terminal coefficients: all zero
- continuation Foundry: empty
- D development state remained exactly the terminal control.

Therefore E53's zero-update joint failure was **not caused by starting outside the safety-feasible set**.

## Fresh validation

| Arm | Utility | Continued | Observations | Opportunity loss | Known success | Known wrong | No-unique UNKNOWN | No-unique wrong |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A terminal | 230,200 | 0 | 0 | 0 | 869 | 140 | 301 | 299 |
| B naive | -106,773 | 1,484 | 6,309 | 932,973 | 1,169 | 16 | 341 | 259 |
| C conservative continuation | **345,063** | 657 | 1,079 | 120,137 | **898** | **46** | 316 | **284** |
| D feasible-root joint | 230,200 | 0 | 0 | 0 | 869 | 140 | 301 | 299 |

C again generalized: +114,863 utility versus A, +29 known successes, -94 known wrong commitments, and -15 no-unique wrong commitments, with far less cost than naive B.

D remained exactly A and therefore failed to add any joint behavior.

## Reachability / gates

- A no-reachable UNKNOWN: 36
- D no-reachable UNKNOWN: 36
- A no-reachable correct: 4
- D no-reachable correct: 4
- integrity: PASS
- known non-inferiority: PASS (identity with A)
- net-utility superiority: FAIL
- no-unique improvement: FAIL
- strict every-cell safety: FAIL; all 60 populated no-unique cells retained wrong commitments
- nontrivial joint behavior: FAIL
- terminal reachability improvement: FAIL
- confirmation earned/executed: 0/0

Native outcome: `NO_VALIDATED_FEASIBLE_ROOT_JOINT_RESCUE`.

## Interpretation

The joint optimizer's failure is now more specific: it is not an unsafe-incumbent problem. E53/E54's conservative continuation coordinate is useful and stable, but coupling terminal refitting into every D candidate prevents D from inheriting that useful continuation update. The next preregistered E55A audit freezes the learned continuation policy first and asks whether the fixed E52A terminal basis has any safe marginal value on the reached states. If it does not, the fixed basis should be retired and the next frontier should be learner-owned sparse structural connectivity rather than another researcher-selected uncertainty rule.

R27 remains canonical. No confirmation was opened.
