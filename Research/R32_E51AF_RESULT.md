# R32 E51AF — Frozen Global Residual Partition Replication Result

**Status:** Invalidated before execution by the frozen prerequisite/integrity gate.

**Execution:** `0`

**Evidence correction:** This document supersedes stale independent-E51AE identity/runtime values in the earlier result text. The correction uses the preserved artifact from E51AE run `33452596868`, job `99685597571`. It does not change the E51AF verdict: the preregistered historical prerequisite still fails decisively.

## Executive verdict

E51AF must not execute or be interpreted as a partition-sensitivity experiment. Its preregistration required an independent GitHub-native reproduction of the earlier historical/local E51AE source identities and development ledger before E51AF validation could become interpretable. The successfully executed current E51AE lineage disagrees with those frozen historical prerequisites.

The E51AF rule was explicit: **any source or ledger disagreement invalidates E51AF before interpretation.** Therefore the valid terminal state is a prerequisite-integrity failure with zero E51AF treatment execution.

## Frozen historical prerequisite

| Historical E51AE prerequisite | Frozen value |
| --- | --- |
| fragment/source identity | `311b8583…` |
| assembled source identity | `d3b00387…` |
| native binary identity | `8438b724…` |
| global residual validation | `5395/5400` |
| global residual known | `4195/4200` |
| global residual no-unique | `1200/1200` |
| critical records | `639` |
| direct-required | `272` |
| union-neither | `234` |
| no-unique | `133` |
| historical critical hash | `1498336702` |
| historical global model hash | `133555290` |

These frozen values cannot be replaced after observing a different reproduction.

## Independent current E51AE execution

- implementation commit: `0b7dab35a256541be3e854ab64a2eddcc759ef3b`
- Actions run: `33452596868`
- job: `99685597571`
- conclusion: `success`
- runtime: `905` seconds
- artifact: `9780663363`

Executed identities:

| Identity | Current E51AE value | Historical prerequisite agreement |
| --- | --- | --- |
| assembled fragment SHA-256 | `9d4ecc675e0c57e50c07deef22a2e86f57810110c588a8833a24a4192cf291c8` | **no** |
| assembled source SHA-256 | `dea2368cc3795b8e547a454f8d10f5f7db9613107753fb443e57f7e70484ecf1` | **no** |
| native binary SHA-256 | `4a562e967341f8b14fd3f5ef8e1b76b8517856dd08f3f81bca4a79ffbf026b94` | **no** |

Development-ledger comparison:

| Field | Historical prerequisite | Current native E51AE | Agreement |
| --- | ---: | ---: | --- |
| critical records | `639` | `605` | **no** |
| direct-required | `272` | `289` | **no** |
| union-neither-known | part of historical `234` union-neither | `315` | **no** |
| no-unique | `133` | `1` | **no** |
| current selection trace | n/a | `354012291` | n/a |
| critical record/target hash | `1498336702` historical value | `841951745` current | **no** |

The current learned residual arms reached `5132/5400` on stage 98, not the historical `5395/5400`. Their actual stage-98 decomposition was `4160/4200` known and `972/1200` no-unique. The current frozen union control reached `5260/5400`.

These are substantive source, support-population, and behavior disagreements.

## Historical Actions run does not satisfy the prerequisite

Historical E51AE run `33419267570` at head `50ef5e59e1121036a0e2abc8838b5607073b845a` concluded `failure` during historical E51AE source assembly because `.github/scripts/e51ae_assemble.py` was missing. It failed before native historical E51AE execution.

Therefore the historical local `5395/5400` ledger remains unreproduced by the frozen GitHub-native pathway E51AF required.

## Frozen gate resolution

- source-agreement gate: **fail**
- development-ledger agreement gate: **fail**
- E51AF execution permitted: `0`
- E51AF validation interpretation permitted: `0`
- E51AF confirmation permitted: `0`
- partition-sensitivity conclusion: **not defined**

No E51AF treatment may be executed after this failed prerequisite. Weakening the prerequisite after observing current E51AE evidence would be post-hoc redesign.

## Consequence

The frozen E51AF instance is permanently closed. A valid follow-up must be a new preregistered lineage either recovering the exact historical source or accepting the successfully executed current E51AE lineage as a new parent. E51AG takes the second route without borrowing historical `639`-record claims or reusing stage-98 validation for tuning.

## Claim boundary

R27 remains canonical and R32 experimental. This integrity failure neither establishes nor refutes AGI. It only closes one preregistered replication instance.

## Authoritative conclusion

`INVALID_E51AF_INTEGRITY_FAILURE`, `execution=0`. The historical prerequisite was not independently reproduced, so E51AF is not a valid partition-replication experiment and was correctly not run.
