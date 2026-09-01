# R32 E51AE — Trajectory-Critical Candidate Residual Result

**Status:** Authoritative native result for the frozen E51AE reimplementation at commit `0b7dab35a256541be3e854ab64a2eddcc759ef3b`.

**Claim boundary:** This is a fresh preregistered native reimplementation of E51AE. It is **not** a byte-identical reconstruction of the earlier local/historical E51AE source.

## Executive verdict

E51AE is a negative learned-treatment result. The frozen E51AB direct-candidate baseline scored `5260/5400`. Each preregistered learned residual treatment scored `5132/5400`, so all three learned treatments regressed by 128 cases relative to the frozen baseline. The oracle candidate control scored `5400/5400`, showing that candidate expressivity remains sufficient when the correct candidate is supplied.

No learned treatment passed the frozen validation gates. The frozen winner is `-1`; confirmation was not required and was not executed; `final_commit=0`; `outcome_code=3`; `final_native_result=0`.

This experiment therefore does **not** support the hypothesis that the preregistered local/global trajectory-critical residual support geometry provides a generalizing rescue on the sealed validation set.

## Frozen lineage and execution

- Frozen E51AE implementation commit: `0b7dab35a256541be3e854ab64a2eddcc759ef3b`
- GitHub Actions run: `33452596868`
- GitHub Actions job: `99685597571`
- Workflow conclusion: `success`
- Native runtime: `891` seconds
- Exit code: `0`
- Assembly: success
- Deterministic double compilation: success
- Native execution: success
- Evidence preservation: success

The treatment was frozen before native validation execution. No post-validation treatment edits were made.

## Native implementation and evidence identities

| Evidence object | SHA-256 |
| --- | --- |
| E51AE fragment | `311e0992cd9691747b2a217c3b8bedbdf95666897040d93e1751e5083068c3ab` |
| Assembled Zag source | `a39ed1c07844f50516080f7a296357a5012e3d388ca2fcf86aa818e4fd94fafb` |
| Native binary | `fcab5b168012f024b62f97dbdb42ba1c9be3ac8acf9eca9d509a24de9913eb2f` |
| `RAW.log` | `74c5b15381bdaf6e2ecc1cbad86364a61e3bed3efdfe6fb2c5347448ed9c4fc5` |
| `SUMMARY.log` | `c9886300308b20840dffcd094388a56cd494464c75da0c6b6a42bff251b92d68` |
| Preserved evidence ZIP | `307f365453c4d70c35a139624720c5e582fbee0b4eb34654812d52b69010954b` |

GitHub Actions artifact: `r32-e51ae-native-evidence`, artifact ID `9780663363`.

## Frozen parent/integrity hashes

The native run reported the following frozen lineage and integrity values before interpretation:

- `E50B=11527908921913446389`
- `E51W=1360523492`
- `E51W_CTRL=1062603631`
- `E51AB=1045718324`
- `E51AC=350784385`
- `validation_pre=426392224`
- `pre_validation_integrity=917467028`

These gates passed in the successful native run.

## Development-stage trajectory-critical ledger

The independently executed native reimplementation fixed the following development-stage partition before sealed validation interpretation:

- critical records: `605`
- direct-required records: `289`
- union-neither-dominance records: `315`
- no-unique diagnostic records: `1`
- critical ledger hash: `354012291`
- global fit 1 hash: `547504260`
- global fit 2 hash: `444148704`
- ledger hash: `15562201`

## Sealed validation result

| Arm | Frozen policy | Total | Known | No-unique | Gate |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0 | E51AB direct-candidate baseline | **5260/5400** | **4064/4200** | **1196/1200** | control |
| 1 | local residual-1 candidate support | 5132/5400 | 3936/4200 | 1196/1200 | 0 |
| 2 | local residual-2 candidate support | 5132/5400 | 3936/4200 | 1196/1200 | 0 |
| 3 | global residual-2 candidate support | 5132/5400 | 3936/4200 | 1196/1200 | 0 |
| 4 | oracle candidate control | **5400/5400** | **4200/4200** | **1200/1200** | 1 |

Frozen terminal ledger:

- `winner=-1`
- local residual modes enabled: `0`
- global residual-2 enabled: `0`
- `confirmation_required=0`
- `confirmation_executed=0`
- `final_commit=0`
- `outcome_code=3`
- `final_native_result=0`

## Interpretation

The oracle candidate arm closes an important alternative explanation: the remaining errors are not caused by an inability of the candidate action set to represent the correct answer. Correct candidate selection can reach `5400/5400` on the sealed validation set.

However, the preregistered learned residual mechanisms do not recover that candidate selection. All three learned residual arms collapse to the same `5132/5400` result, below the frozen E51AB baseline. The evidence therefore points away from this specific residual-support geometry as a generalizing repair and toward a harder candidate-selection/provenance problem.

The result must not be converted into a positive claim by selecting the oracle arm. Arm 4 is diagnostic only and is not a learnable treatment.

## Historical E51AE reconciliation

The earlier historical E51AE workflow is not an independent native result:

- historical run: `33419267570`
- historical head: `50ef5e59e1121036a0e2abc8838b5607073b845a`
- conclusion: `failure`
- failure point: `Assemble historical E51AE native source`
- error: missing `.github/scripts/e51ae_assemble.py`

That run failed before historical E51AE source assembly and before native E51AE execution. Its preserved artifact therefore cannot establish an independent Actions reproduction of the earlier local result.

The historical preregistered identities also differ from this reimplementation. Historical expected identities begin with fragment `311b8583…`, assembled source `d3b00387…`, and binary `8438b724…`; this native reimplementation produced `311e0992…`, `a39ed1c0…`, and `fcab5b16…`, respectively. Accordingly, this result is authoritative for the new frozen reimplementation lineage only.

## Retained invariants

This result does not alter the project claim boundary. R27 remains canonical; R32 remains experimental. E51AE does not demonstrate AGI, proto-AGI, consciousness, or inevitability of an AGI path.

## Next causal question

The frozen E51AF experiment already preregistered a prerequisite source-and-ledger replication gate. The independent native E51AE result above disagrees with that historical prerequisite, so E51AF must be resolved by its fail-closed rule rather than executed as though replication succeeded. Any future attempt to recover the historical residual result must be a separately preregistered provenance/source reconstruction or a clearly new experimental lineage; the sealed E51AE validation result must not be used to tune the frozen treatment.

## Authoritative conclusion

E51AE executed successfully and produced a valid negative learned-treatment result. The oracle control establishes available candidate expressivity, while all preregistered learned residual treatments regress relative to the frozen E51AB baseline. There is no validation winner and no confirmation execution.