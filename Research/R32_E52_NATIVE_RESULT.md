# R32 E52 — Native Joint Decision Foundry Result

Date: 2026-08-29  
Status: `EXECUTED_NATIVE_DIAGNOSTIC NEGATIVE — CANDIDATE-COEFFICIENT FIT DEFECT EXPOSED`  
Canonical: R27 step 60,423

## Question

Can a generic learner-owned sparse pairwise feature Foundry improve the three grounded terminal commit values jointly with learned continuation value, while `UNKNOWN` remains the immutable neutral value `0`?

## Integrity

- E50 parent integrity: PASS
- fresh seed assignments: 7,020; failures: 0
- development: 3,240 episodes / 55,080 terminal records
- validation: 2,700 episodes
- sealed confirmation: 1,080 allocated, 0 executed
- source SHA-256: `3d0776e7c5a1d8c42f3ad446382ffe7f0c377267a8882253b2a2a97cc4df25b0`
- two byte-identical native binaries: `9f9ff2402e881224f2f230fae9c86e26fe0138c4624f06cf22ff1d0513706775`
- raw ledger SHA-256: `edacd398a823c41e77f87aac1bb0ac30488e077a1b9693fffdd3c01b59e993bd`
- runtime: 85.65 seconds; expected qualification exit: 1

## Validation

| Arm | Terminal geometry | Continuation | Success | UNKNOWN | Wrong | Known success | Known wrong | No-unique UNKNOWN | No-unique wrong | Observations | Net utility |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | frozen E50 | none | 1,133 | 1,399 | 452 | 849 | 136 | 284 | 316 | 0 | 197,800 |
| B | frozen E50 | learned | 1,148 | 1,475 | 400 | 825 | 123 | 323 | 277 | 1,358 | 80,188 |
| C | Foundry | none | 1,133 | 1,399 | 452 | 849 | 136 | 284 | 316 | 0 | 197,800 |
| D | Foundry | learned | 1,148 | 1,475 | 400 | 825 | 123 | 323 | 277 | 1,358 | 80,188 |

## Finding

The Foundry selected zero interactions. C exactly equaled A and D exactly equaled B. Inspection showed that proposal coefficients were estimated from a sample and then rejected by the full-development acceptance test; therefore the intended joint capacity was not actually exercised.

E52 is a valid native fitting diagnostic, not evidence that joint terminal/continuation learning lacks value. It preregistered the exact-coefficient repair E52A before any new validation execution. Confirmation remained sealed.
