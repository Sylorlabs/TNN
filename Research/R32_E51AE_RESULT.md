# R32 E51AE — Trajectory-Critical Candidate Residual Result

**Status:** Corrected authoritative native result for frozen implementation commit `0b7dab35a256541be3e854ab64a2eddcc759ef3b`.

**Correction note:** This file supersedes the stale result text committed at `b0a0f2d06861685569fb7fb064b5378ac05d80ed`. That text was assembled from stale handoff numbers and did not match the preserved Actions artifact. The evidence below is taken directly from GitHub Actions run `33452596868`, job `99685597571`, and artifact `9780663363`.

## Executive verdict

E51AE is a valid negative learned-treatment result. The frozen union control reached `5260/5400`; each learned residual arm reached `5132/5400`; the evaluator direct-action oracle reached `5400/5400`.

More importantly, all three learned treatments already failed the frozen development-preservation gate before validation: each preserved `12135` of `12644` frozen-union development episodes while rescuing `230`, so each development gate was `0`. Sealed stage-98 validation was still executed for reporting under the preregistered implementation, but no learned arm was eligible to win. Confirmation remained sealed.

Outcome: `TRAJECTORY_CANDIDATE_RESIDUAL_NO_RESCUE`.

## Execution identity

- implementation commit: `0b7dab35a256541be3e854ab64a2eddcc759ef3b`
- Actions run: `33452596868`
- job: `99685597571`
- workflow conclusion: `success`
- native runtime: `905` seconds
- exit code: `0`
- deterministic double-build byte identity: `1`
- artifact ID: `9780663363`
- artifact name: `r32-e51ae-native-0b7dab35a256541be3e854ab64a2eddcc759ef3b`

## Evidence hashes

| Evidence object | SHA-256 |
| --- | --- |
| E51AE assembled fragment | `9d4ecc675e0c57e50c07deef22a2e86f57810110c588a8833a24a4192cf291c8` |
| assembled native Zag source | `dea2368cc3795b8e547a454f8d10f5f7db9613107753fb443e57f7e70484ecf1` |
| native binary build 1/2 | `4a562e967341f8b14fd3f5ef8e1b76b8517856dd08f3f81bca4a79ffbf026b94` |
| `RAW.log` | `ae1b5fe4b5cf3f8b610fe6da1c095a5cd2a9da51757978334836dedb21c87389` |
| `SUMMARY.log` | `0a8c8fd16f8ce30b88a6357641a285c0666f2bd5a10d44512b7a90a3eb308b0e` |
| preserved artifact ZIP | `307f79e7013630cbef0560e0e47bf55a4f47e0073d73be97b2f4cf2f31718e97` |

The workflow also recorded the source-file SHA-256 values before compilation, including `01a=d176e733…`, `01b=d7873c9a…`, `01c=d8c708a4…`, `02a=340281d1…`, `02b=71562055…`, `02c=34c767b6…`, `02d=e1c05da1…`, and main injection `7ae7f792…`.

## Integrity and frozen-model gates

- E50 seed preflight: `1`
- E50 batch statistics: `1`
- E50 forward/reverse identity: `1`
- E50 convergence: `1`
- E50 auxiliary frozen: `1`
- E51Y parent integrity: `1`
- E51Y terminal reproduction: `4200,4200,1200,1200,1`
- E51AE world partition gate: `1`
- E51AE domain gate: `1`
- direct reconstruction episodes: `12960`
- direct global identity: `1`
- direct local identity: `1`
- direct target support: `1`
- direct integrity: `1`
- direct hash before training: `1790306570`
- terminal hash before training: `238967492`
- terminal hash after training: `238967492`
- direct hash after training: `1790306570`
- frozen training gate: `1`
- pre-validation integrity gate: `1`
- frozen validation gate: `1`
- validation integrity gate: `1`
- frozen final gate: `1`
- final integrity gate: `1`

## Stage-97 development ledger

- episodes: `12960`
- states: `220320`
- slot-covered: `12355`
- direct-required: `289`
- union-neither-known: `315`
- union-neither-no-unique: `1`
- frozen-union development: `12644`
- neither replication factor: `1`
- expected critical count: `605`
- support gate: `1`

Critical set:

- count: `605`
- selection trace: `354012291`
- critical record/target hash: `841951745`
- isolation gate: `1`
- candidate-0 support: `297 positive / 308 negative / 0 neutral`
- candidate-1 support: `302 positive / 303 negative / 0 neutral`

Global residual fits:

- candidate 0: `32,2,547504260,254939881,identity=1`
- candidate 1: `32,2,444148704,274963742,identity=1`
- global identity gate: `1`

Development treatment outcomes:

| Arm | Treatment | Preserved frozen union | Rescued neither | Margin loss | Development gate |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | global residual | `12135/12644` | `230` | `6272814` | `0` |
| 2 | local-96 residual | `12135/12644` | `230` | `6272814` | `0` |
| 3 | local-384 residual | `12135/12644` | `230` | `6272814` | `0` |

The local forward/reverse identity gate was `1`. The local fits made no accepted rescue-improving round and converged to the same deployed behavior as the global residual treatment.

## Sealed stage-98 validation

| Arm | Frozen policy | Reachable | Known reachable | No-unique reachable |
| ---: | --- | ---: | ---: | ---: |
| 0 | frozen slot+direct union control | **5260/5400** | `4061/4200` | `1199/1200` |
| 1 | global residual | `5132/5400` | `4160/4200` | `972/1200` |
| 2 | local-96 residual | `5132/5400` | `4160/4200` | `972/1200` |
| 3 | local-384 residual | `5132/5400` | `4160/4200` | `972/1200` |
| 4 | evaluator direct-action oracle | **5400/5400** | **4200/4200** | **1200/1200** |

Thus the learned residual treatment shifts errors rather than monotonically repairing them: it improves known reachability relative to arm 0 (`4160` vs `4061`) but loses much more no-unique reachability (`972` vs `1199`), producing a net regression of `128` total episodes.

Validation gates for arms 1–3 were all `0`; winner was `-1`. Stage-99 confirmation allocation was declared but execution was `0` and confirmation exact gate was `0`.

## Interpretation

The oracle result shows that the candidate action interface can express a perfect solution on this partition. The failure is therefore not candidate-action expressivity. The residual learner's evaluator-blind features and fitted value correction fail to preserve the mature union behavior, especially on no-unique cases, while improving some known cases.

This is evidence against this specific trajectory-critical additive residual geometry as a promotable repair. It does not justify choosing the oracle, using stage-98 labels to retune the residuals, or changing the frozen development rule after seeing validation.

## Claim boundary

R27 remains canonical and R32 remains experimental. E51AE does not demonstrate AGI, proto-AGI, consciousness, or inevitability. It is one falsifying discriminator inside the broader architecture search.

## Authoritative conclusion

E51AE executed validly and failed as a learned treatment. The correct causal follow-up is a no-parameter-change replication/generalization audit on fresh partitions or a separately preregistered escalation—not post-hoc tuning on stage 98.
