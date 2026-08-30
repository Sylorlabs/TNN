# R32 E53A — Native Learner-Owned Meta-Control Result

Date: 2026-08-30  
Status: `EXECUTED_NATIVE DIAGNOSTIC PASS — BOUNDED META-CONTROL OWNERSHIP DEMONSTRATED`  
Canonical: R27 step 60,423  
Promotion: none

## Question

Can update-rate / replay / trust-region selection move from a caller-supplied schedule into learner-valued state without evaluator family identity entering the selector?

E53A is a bounded ownership-pressure test, not the full E53 behavioral discriminator.

## Integrity

- preregistration SHA-256: `f3e98c19f90ab16f37bd36539b7a9590d90f168ef441ba9e96a2ff3404aaa34d`
- ownership-audit SHA-256: `aa336c32ae2634cc2465635fe8db6da7071d8916058cea30eb4bf1b9678eb9e8`
- source SHA-256: `0e6c886f6a221f543056f0d8a7c012b23c3a19f90c3c6c360fea00063b6ee1d8`
- parent E53 core SHA-256: `8d54f62b18514a2dafc6468e985abb6d048ca71fc0d6ccca8ef0046d40ebfa83`
- two native binaries: byte-identical
- native binary SHA-256: `d81fefb7d0aa4e9b7f21cd97334d79a11403da6d90a2d82be0b9b0e0524f4196`
- workflow run: `33330396775`
- evidence artifact ID: `9737466021`
- evidence artifact digest: `sha256:bd46b7a7b2702455ac8891be16ef081a5f2765d9b0ead254ca783346e42cfd07`
- native exit: 0

The source contract verifies that the selector inputs are only `qvalues, context`, while the context is derived only from `policy_value, replay_anchor`. Evaluator family is confined to world/case generation and is not a selector input.

## Learned meta-values

Each learner-visible context received exactly 40 development experiences for each of the six candidate update geometries.

| Context | Action 0 | Action 1 | Action 2 | Action 3 | Action 4 | Action 5 | Selected |
|---|---:|---:|---:|---:|---:|---:|---:|
| low discrepancy | -5 | -8 | -82 | -206 | -409 | -977 | **0** |
| medium discrepancy | 20 | 72 | 210 | 397 | **543** | 470 | **4** |
| large discrepancy | 20 | 72 | 210 | 550 | 1200 | **2540** | **5** |

Selected update geometries:

| Context | Update rate | Replay mass | Residual clip |
|---|---:|---:|---:|
| low discrepancy | 100 | 7 | 100 |
| medium discrepancy | 750 | 1 | 800 |
| large discrepancy | 1000 | 0 | 1400 |

The learner therefore did not collapse onto one global schedule. It learned a conservative/high-replay geometry near an established replay anchor and progressively more aggressive geometries as endogenous discrepancy increased.

## Fresh validation

Validation contained 480 records: exactly 160 in each learner-visible context. No validation record updated the learned meta-values.

| Policy | Validation objective |
|---|---:|
| fixed action 0 | 5,516 |
| fixed action 1 | 20,344 |
| fixed action 2 | 57,092 |
| fixed action 3 | 117,548 |
| fixed action 4 | 190,904 |
| fixed action 5 | **208,320** |
| **learner-selected adaptive meta-control** | **545,356** |

The adaptive selector used three distinct meta-actions and changed action 8 times as learner-visible context changed.

Gates:

- balanced development: PASS
- three distinct learned meta-actions: PASS
- adaptive action switching: PASS
- adaptive objective > best of all six fixed controls: PASS
- validation context balance: PASS
- UNKNOWN value protected at zero: PASS
- evaluator family inside selector: NO
- graph substrate required: NO
- final native gate: `TNN_R32_E53A_META_CONTROL_OWNERSHIP_GATE=PASS`

## Interpretation

This is a meaningful but narrow ownership transfer.

Before E53A, the E53 core could consume rate/replay/clip values, but native evidence did not establish that TNN itself selected them. E53A demonstrates that a learner can assign grounded delayed value to generic update geometries and select different geometries from its own visible state, outperforming every fixed candidate in the bounded validation.

What E53A **does not** establish:

- the six candidate geometries are still researcher supplied;
- the three-region discrepancy representation is still researcher supplied;
- TNN does not yet invent arbitrary update rules;
- TNN does not yet create new meta-actions;
- the mechanism is not yet integrated into the full E53 sequential terminal/continuation discriminator;
- arbitrary connection/routing rewrites are not demonstrated;
- hypothesis/action ontology ownership is unchanged;
- no R32 promotion is earned.

The scientifically correct status is therefore **partial learner ownership of meta-control selection**, not full ownership of learning itself.

## Preregistration boundary and next ownership work

The full E53 treatment was preregistered before E53A executed. E53A therefore must **not** be inserted retroactively into frozen E53 and then described as part of the original E53 treatment. Frozen E53 should execute exactly as frozen. If E53A-style learner-selected meta-control is integrated into the full sequential controller, that integration requires a distinct preregistered successor/extension with fresh evaluation data.

The highest-value remaining ownership tests are:

1. learner-created hypothesis split/merge/retirement;
2. learner-selected discriminating observation/action, not only continue/terminate;
3. first-class introspection and write authority over every non-core causal connection/influence;
4. learner-expanded Foundry representation/mechanism grammar;
5. learner-owned memory and compute scheduling.

R27 remains canonical.