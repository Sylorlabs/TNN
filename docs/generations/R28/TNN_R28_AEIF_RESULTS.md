# R28 AEIF No-Graph Rebuild — Results

## Decision

**Status:** `SHADOW_RESEARCH_CHECKPOINT / NATIVE_ZAG_BLOCKED_ENV`.

R28 is **not** promoted over R27. The accepted parent remains step **60,423**, zero newborn restarts, digest `562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04`. The parent verifier reran **33/33 PASS**, R26 **47/47 PASS**, and R25 lineage **68/68 PASS**.

Candidate Zag source SHA-256: `61fe5ffb41e1d3e02f8139d57128af1f4c9f3216c206afe6b3eb86fed1f2e0ea`. Static/source-contract audit: **18/18 PASS**. Native execution is blocked because no executable pinned `znc` is materialized in the active cloud terminal.

## Architecture change

R28 retires graph state as identity authority. The candidate identity architecture is **AEIF — Associative Episodic Identity Fabric**: exact/multi-view episodic retrieval + live identity hypotheses + learned evidence reliability + temporal prediction + active reinspection. Graphs remain optional derived relation indexes only. Destroying a relation index must not destroy identity, memory, language grounding, or action history.

### Matched deep-training evidence

At dose 1,024, the best no-graph `AE_ACTIVE` condition reached **93.57%** overall (balanced training; floor 50.00%). `AE_ACTIVE + MIXED` reached **92.86%** with the stronger **60.00%** worst-condition floor.

The strongest graph-authority control under adaptive-Master training (`G_ACTIVE/G_ALL`) reached **80.71%** overall with a **30%** floor and was classified as plateauing. This supports removing graph authority, but does not prove graphs are useless: relation graphs remain a valid derived representation and some active graph controls converge toward no-graph performance when given the same helpers.

## Training is independent from architecture

The continuous-life AEIF dose sweep, with architecture held fixed, was:

| Dose per entity | Identity | True switch | Full nominal | Extra observation |
|---:|---:|---:|---:|---:|
| 64 | 96.67% | 89.58% | 85.83% | 9.58% |
| 128 | 95.83% | 92.50% | 88.33% | 12.50% |
| 256 | 98.75% | 94.17% | 92.92% | 7.50% |
| 512 | 95.83% | 86.67% | 82.92% | 21.25% |
| 1024 | 96.25% | 85.83% | 82.50% | 19.58% |

The peak is **256 examples/entity**. Increasing to 512/1,024 caused interference/overconsolidation rather than further learning. This is evidence against treating low scores as automatically undertraining.

## Continuous-life integrated qualification

Five-seed nominal means at the 256-example peak:

- persistent identity: **98.75%**
- true identity switching: **94.17%**
- bounded speech path: **100.00%**
- name / affordance / sibling / memory / provenance / save-reload in this nominal harness: **100% each**
- all-or-nothing integrated success: **92.92%**

Hard five-seed means:

- identity: **97.92%**
- true switch: **90.00%**
- hard connected speech: **22.08%**
- full integrated success: **20.42%**
- active reinspection used: **100.00%**

The hard integrated failure is now dominated by connected speech rather than a diffuse system-wide collapse.

## Memory — default heuristic under TNN authority

The user-selected default is the privileged generic heuristic, but it is **not immutable and not credited as learned memory competence**. TNN owns the actual storage choices and may override/mutate/replace it. LRU is eviction mechanics only.

| Policy | Overall | Exact | Semantic | Project utility | TNN override |
|---|---:|---:|---:|---:|---:|
| HEURISTIC_DEFAULT_TNN_OVERRIDE_LRU | 73.80% | 72.30% | 74.09% | 0.6670 | 39.49% |
| HEURISTIC_LOCKED_LRU_EVICT | 73.64% | 58.69% | 78.43% | 0.6358 | 0.00% |
| LRU_REPRESENTATION_CONTROL | 82.14% | 19.48% | 98.41% | 0.6196 | 0.00% |
| STRUCTURED_ALL_CONTROL | 79.04% | 0.00% | 100.00% | 0.5632 | 0.00% |

Pure LRU has higher headline recall but destroys most exact-detail retention (19.48%). The heuristic-default + TNN-override policy has the highest defined project utility (**0.6670**) and preserves **72.30%** exact-detail queries.

## Innate System Fluency

System-operation semantics were tested separately from task knowledge. Mean development regret:

- innate system fluency: **0.230**
- Master-taught fluency: **0.359**
- schema-only: **14.134**
- learn everything from scratch: **18.855**

The strong early advantage supports treating generic self-operation semantics as a core bootstrap capability, not as task/world knowledge. Schema-only learning can largely catch up on transfer.

## Substrate-agnostic Foundry

Whole-substrate meta search treats graph authority as one optional gene rather than the search space itself.

| Search | Hidden score | Overall | Floor | Graph authority selected |
|---|---:|---:|---:|---:|
| META_HYBRID | 1.1696 | 89.84% | 49.31% | 16.67% |
| META_MUTATION | 1.1658 | 89.84% | 48.61% | 16.67% |
| META_RETRIEVAL | 1.1457 | 88.98% | 46.53% | 33.33% |
| RANDOM | 1.0984 | 86.55% | 42.36% | 16.67% |

`META_HYBRID` ties-or-beats random on all six hidden profiles and strictly beats it on half; graph authority is selected only **16.67%** of the time. This is positive evidence for substrate-agnostic self-design, but the six-profile reference suite is too small for a broad autonomous-architecture claim.

## Grounded affordance/world model

A fixed-context scalar baseline collapses to ~28%. A context-sensitive entity × action → effect learner reaches **95.23% clean / 88.92% noisy**. With 40 grounded training contexts it reaches **98.01% clean / 90.74% noisy**. This is learned consequence prediction, not category→action lookup.

## One-shot arbitrary names

Hard five-seed arbitrary-name grounding:

- raw resampling: **90.50%**
- normalized learned shape: **99.50%**
- target beats closest-name distractor: **99.50%**

This is robust-near-solved for the bounded one-shot name task, not a broad natural-speech claim.

## Independent sibling teaching

The nominal 100% sibling result did not survive an adversarial receiver test:

- passive: **50.83%**
- one grounded discriminating action question: **93.54%**
- same mechanism under heavy action noise: **78.96%**

The interactive grounded mechanism is retained; the 100% nominal claim is explicitly narrowed.

## Master curriculum

The Master remains valuable for development, but permanent Master control is not optimal. At dose 512, mixed/diversified training reaches **93.81%**, competence-withdrawal **90.00%**, staged **91.43%**, and permanent Master **88.57%** in the reference curriculum suite. Teacher knowledge is always withdrawn from qualification and never counted as learner cognition.

## Connected speech — unresolved boundary

This remains the main capability blocker. Important diagnostics:

1. Earlier CTC 0% contained an invalid split: train/validation/test regenerated different acoustic identities while reusing class IDs. That result was discarded.
2. After fixing acoustic identity across splits, CTC still produced **0%** because it collapsed to blank outputs despite falling loss.
3. Negative blank bias removed the empty-output collapse but produced only **2.9%** token accuracy.
4. Isolated acoustic pretraining reached **91.81%**, yet connected CTC fine-tuning reached only **5.14%**. CTC remains rejected in its current formulation.
5. On the exact hard distribution, a discriminative acoustic learner with evaluator boundary context tops out around **87.17%**. Thus the deliberately severe hard waveform world is partly information-limited at the current signal representation, not merely a segmentation bug.
6. Hard continuous-life speech remains **22.08%**, so broad natural connected-speech competence is not established.

## Release conclusion

R28 materially improves the architectural understanding of identity, memory policy, training interference, system fluency, substrate search, affordance learning, one-shot names, and sibling teaching. **It does not earn canonical promotion** because the new Zag source has not been natively compiled/executed in this environment and hard connected speech remains unsolved.
