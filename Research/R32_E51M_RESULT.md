# R32 E51M — Calibration Dose × Capacity Curve Result

Date executed: 2026-08-30 PDT
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Status

`VALID DEVELOPMENT/VALIDATION RESULT — CALIBRATION_DOSE_SIGNAL; NO EXACT RESCUE`

E51M was rerun in full native Zag v2 after repairing the exhausted *unexecuted confirmation-reservation* path. Development and validation stayed in the historical effective-state namespace. The sealed confirmation partition received deterministic nominal IDs, remained inaccessible to cognition, and was not executed. Because no arm reached the exact validation gate, no confirmation or promotion claim is available.

The earlier run at GitHub Actions `33343784134` remains retired as an invalid seed-namespace-exhaustion run. Its grid is not evidence. The authority for this result is the successful run below.

## Native authority

- GitHub Actions run: `33364230156`
- source head: `bda86ce93c1084d77c22b5414d8d76aff17f3ab9`
- artifact ID: `9747784574`
- artifact ZIP SHA-256: `683a3293e8af000f13be1b763b7fef1afffdfcf42cc45921d1dfcb011de71795`
- patched E51M fragment SHA-256: `b47e1505e2fef8d0a3c9d3cd0c0bb262a76adadc58849ab939b3409639750bc6`
- retained `01_calibration_curve.zagfrag` SHA-256: `9de7792008f0f4f3a3f6ba14bf23bc02b57324b61b7576ab26b029fb92fc798f`
- retained main-injection SHA-256: `e0ea517b1e7876e77070a4c1a13dacd6f386690df3063a15a78b3d5cfed99d85`
- assembled complete native source SHA-256: `b80ec443e95b4c600576dda95f96b1abeb00312b9969761ed3779f0ca20f6bee`
- frozen E45 core SHA-256: `6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0`
- native binary SHA-256: `0eb57ff0080cdc5dfb706f2e82ad111a5b1322f53e8a732d500de4f47bec17e9`
- two native builds byte-identical: PASS
- native runtime: 175 seconds
- native exit code: 0

## Integrity

Parent E50 gates:

- seed preflight: PASS
- batch statistics: PASS
- batch forward/reverse identity: PASS
- batch convergence: PASS
- frozen auxiliary-state gate: PASS

Learner and experiment isolation:

- full native Zag v2 path: yes
- evaluator truth exposed to learner: no
- ambiguity label exposed: no
- validation membership exposed: no
- UNKNOWN positive target: none
- topology changed: no
- graph privileged: no
- base UNKNOWN nonzero targets: 0
- base UNKNOWN nonzero parameters: 0
- base terminal fit identity: PASS
- scalar forward/reverse identity for every dose: PASS
- hinge forward/reverse identity for every dose: PASS
- 16 learner-selected hinge terms recruited at every dose

Partitions:

- maximum development: 12,960 episodes / 220,320 sequential states
- untouched validation: 5,400 episodes / 91,800 sequential states
- validation composition: 4,200 known / 1,200 no-unique
- sealed confirmation: 10,800 nominal IDs allocated / 0 executed
- development + validation effective-seed assignment failures: 0
- confirmation effective streams reserved: 0

The confirmation namespace amendment is documented in `Research/R32_E51M_NATIVE/ASSEMBLY_INTEGRITY_NOTE.md`. Nominal confirmation IDs cannot be opened. An exact validation rescue would require a separately preregistered expanded executable confirmation namespace.

## Training support

| Development dose | States | Positive top-commit sign targets | Negative top-commit sign targets | Neutral |
|---|---:|---:|---:|---:|
| 1× | 55,080 | 37,156 | 17,924 | 0 |
| 2× | 110,160 | 74,461 | 35,699 | 0 |
| 4× | 220,320 | 148,908 | 71,412 | 0 |

The base commit-ordering head was frozen after the first 1× development prefix. Increasing dose changed only the rank-preserving scalar commit-calibration learner.

## Validation frontier

Uncalibrated frozen-base reachability:

- known: **4,199 / 4,200**
- no-unique UNKNOWN: **1,124 / 1,200**

| Dose | Hinge capacity | Known reachable | No-unique UNKNOWN reachable |
|---:|---:|---:|---:|
| 1× | 0 | 4,193 / 4,200 | 1,144 / 1,200 |
| 1× | 4 | 4,194 / 4,200 | 1,147 / 1,200 |
| 1× | 8 | 4,189 / 4,200 | 1,159 / 1,200 |
| 1× | 16 | 4,192 / 4,200 | 1,161 / 1,200 |
| 2× | 0 | 4,193 / 4,200 | 1,149 / 1,200 |
| 2× | 4 | 4,196 / 4,200 | 1,156 / 1,200 |
| 2× | 8 | 4,196 / 4,200 | 1,152 / 1,200 |
| 2× | 16 | 4,192 / 4,200 | **1,162 / 1,200** |
| 4× | 0 | 4,192 / 4,200 | 1,148 / 1,200 |
| 4× | 4 | 4,194 / 4,200 | 1,154 / 1,200 |
| 4× | 8 | 4,188 / 4,200 | 1,159 / 1,200 |
| 4× | 16 | 4,190 / 4,200 | 1,158 / 1,200 |

## Frozen outcome

- exact validation rescue: **FAIL**
- preregistered dose signal: **PASS**
- preregistered capacity signal: **PASS**
- winning exact arm: none
- sealed confirmation executed: 0
- native outcome: `CALIBRATION_DOSE_SIGNAL`

The cleanest dose contrast is 1× linear to 2× linear: known reachability remains 4,193 while no-unique reachability improves from 1,144 to 1,149. The cleanest capacity contrasts are the 0-to-4-hinge moves at every dose; each improves both measured reachability dimensions on this validation partition.

The curve is nevertheless non-monotonic beyond those local contrasts. More data or more hinge terms do not uniformly improve the controller, and no calibrated arm Pareto-dominates the uncalibrated base. The best no-unique arm still misses 38 ambiguous episodes and loses seven known episodes relative to exact known reachability.

## Interpretation

E51M rejects a strict claim that the tested scalar decision boundary has already reached a hard data/capacity plateau. The same learner-visible state can support measurable Pareto movement when either development exposure or learner-selected boundary capacity increases.

E51M does **not** show that continued scaling of this exact scalar mechanism will reach the exact gate. It also does not justify a graph/topology rewrite. The next binding question is replication: do the preregistered low-capacity Pareto contrasts survive independent fresh world tuples, or were they specific to this validation partition?

The next experiment is E51N, a native Zag v2 replication using an expanded tuple-disjoint evaluator namespace. It must hold the learner-visible state, grounded consequence targets, frozen commit ordering, UNKNOWN geometry, optimizer, and capacity definitions fixed. No seed/domain identifiers may enter cognition.

No E51M result promotes R32, defeats R27, or establishes consciousness or AGI.
