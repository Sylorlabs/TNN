# R32 E51AF — Frozen Global Residual Partition Replication Result

**Status:** Invalidated before execution by the frozen replication/integrity gate.

**Execution:** `0`

## Executive verdict

E51AF must not execute or be interpreted as a partition-sensitivity experiment. Its preregistration required an independent GitHub-native reproduction of the earlier E51AE source identities and development ledger before E51AF validation could become interpretable. The independently executed native E51AE reimplementation disagrees with both the historical source/build identities and the historical development ledger.

The frozen E51AF rule is explicit: **any source or ledger disagreement invalidates E51AF before interpretation.** That condition is met. Therefore the scientifically valid E51AF result is a prerequisite-integrity failure with zero E51AF treatment execution, not a negative or positive partition-replication result.

## Frozen prerequisite

The historical/local E51AE evidence embedded in the E51AF preregistration fixed the following prerequisite target:

| Preregistered historical E51AE prerequisite | Frozen value |
| --- | --- |
| fragment/source identity | `311b8583…` |
| assembled source identity | `d3b00387…` |
| native binary identity | `8438b724…` |
| global residual validation total | `5395/5400` |
| global residual known | `4195/4200` |
| global residual no-unique | `1200/1200` |
| critical records | `639` |
| direct-required | `272` |
| union-neither | `234` |
| no-unique | `133` |
| critical hash | `1498336702` |
| global model hash | `133555290` |

The preregistration does not permit these values to be replaced after observing an independent reproduction.

## Independent GitHub-native E51AE reproduction

The frozen independent native E51AE reimplementation executed successfully in GitHub Actions:

- frozen commit: `0b7dab35a256541be3e854ab64a2eddcc759ef3b`
- Actions run: `33452596868`
- job: `99685597571`
- workflow conclusion: `success`
- runtime: `891` seconds

Its source/build identities are:

| Identity | Independent native value | Agreement with frozen E51AF prerequisite |
| --- | --- | --- |
| fragment SHA-256 | `311e0992cd9691747b2a217c3b8bedbdf95666897040d93e1751e5083068c3ab` | **no** |
| assembled source SHA-256 | `a39ed1c07844f50516080f7a296357a5012e3d388ca2fcf86aa818e4fd94fafb` | **no** |
| native binary SHA-256 | `fcab5b168012f024b62f97dbdb42ba1c9be3ac8acf9eca9d509a24de9913eb2f` | **no** |

Its development-stage ledger is:

| Ledger field | Frozen E51AF prerequisite | Independent native E51AE | Agreement |
| --- | ---: | ---: | --- |
| critical records | 639 | 605 | **no** |
| direct-required | 272 | 289 | **no** |
| union-neither | 234 | 315 | **no** |
| no-unique | 133 | 1 | **no** |
| critical hash | 1498336702 | 354012291 | **no** |

The independent native learned residual arms also scored `5132/5400`, not the historical local global-residual value `5395/5400`.

These are substantive source/provenance and ledger disagreements, not harmless byte-level packaging differences.

## Historical Actions run does not satisfy the prerequisite

The historical E51AE GitHub Actions run cannot be used to claim that the historical local result was independently reproduced:

- run: `33419267570`
- head: `50ef5e59e1121036a0e2abc8838b5607073b845a`
- conclusion: `failure`
- failure step: `Assemble historical E51AE native source`
- error: `.github/scripts/e51ae_assemble.py` was missing

The historical job failed before source assembly and before native E51AE execution. Its evidence artifact preserved transport/preregistration material but did not contain a successfully executed historical native result.

Accordingly, the earlier local `5395/5400` residual ledger remains unreproduced by the frozen GitHub-native pathway required by E51AF.

## Frozen gate resolution

Because the source/build identities and development ledger disagree:

- prerequisite source-agreement gate: **fail**
- prerequisite ledger-agreement gate: **fail**
- E51AF execution permitted: **0**
- E51AF sealed validation interpretation permitted: **0**
- E51AF confirmation permitted: **0**
- partition-sensitivity conclusion: **not defined / not interpretable**

No E51AF treatment is executed after this failed prerequisite. Doing so would violate the preregistered causal ordering and convert a fail-closed replication audit into a post-hoc experiment.

## Interpretation

This result does **not** show that the proposed E51AF partition scheme succeeds or fails. It shows that the historical E51AE premise on which E51AF was conditioned is not independently reproduced under the required source/provenance constraints.

The large development-ledger disagreement is scientifically material. The independent native implementation identifies `605` trajectory-critical records with a `289/315/1` class split, whereas the historical prerequisite fixed `639` records with a `272/234/133` split. In particular, the no-unique class changes from `133` to `1`. That changes the population E51AF was supposed to repartition, so proceeding would no longer test the preregistered question.

## Consequence for the research frontier

The frozen E51AF instance is permanently closed by its own integrity rule. It must not be repaired by weakening the gate after observing E51AE evidence.

A future experiment can proceed only as a new, separately preregistered lineage, for example by:

1. recovering and hash-verifying the exact historical E51AE source/assembler/provenance and independently reproducing its ledger before proposing a new partition replication; or
2. accepting the successful current E51AE reimplementation as the new experimental parent and preregistering a new causal experiment from its `605`-record ledger without borrowing the historical `639`-record claims.

The existing E51AE sealed validation results must not be used to tune such a future treatment.

## Claim boundary

R27 remains canonical and R32 remains experimental. This integrity failure neither establishes nor refutes AGI. TNN remains a research pathway under evaluation, not demonstrated AGI, proto-AGI, consciousness, or an inevitable route to AGI.

## Authoritative conclusion

E51AF is **invalidated before execution**. The frozen prerequisite replication gate fails because the independent GitHub-native E51AE source/build identities and development ledger disagree with the historical values preregistered by E51AF, while the historical Actions run failed before native execution. The correct terminal state is `execution=0` with no E51AF partition-sensitivity interpretation.