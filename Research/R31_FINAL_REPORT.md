# R31 Endogenous Chunking — Final Shadow Research Report

## Executive decision

R31 answers the user's correction to R30: TNN should not be evaluated or architected as a fixed-token/transformer-style sequence model. The forward architecture is **endogenous self-chunking over raw experience plus a high-fidelity raw/episodic bypass**. CTC-like alignment may remain a generic alignment primitive after chunks exist, but it does not define the units.

R31 remains **SHADOW / REFERENCE_ONLY** for quantitative claims because this runtime could not materialize or execute a usable `znc` compiler. The graph-free native Zag target exists and passes its static source contract. R27 therefore remains canonical.

## Binding architecture

```text
raw sensory / episodic evidence ------------------------------+
      |                                                        |
      +-> learner-recruited reversible chunks                  |
            -> support-gap recruitment                         |
            -> grounded/consequence utility                    |
            -> hierarchy / split / merge / specialization      |
            -> compressed reusable route                       |
                                                               |
raw high-fidelity bypass <-------------------------------------+
      |
      +-> evidence arbitration / active reinspection
            -> discriminating action/consequence probe
            -> learned commit / continue / UNKNOWN
```

No graph cognition. No transformer. No LLM. No BPE/fixed tokenizer. No next-token objective. No supplied VAD/phoneme/word/chunk boundary.

## 1. Recovered self-chunking lineage

The earlier Adaptive Motif lineage already established the relevant mechanism class:
- reversible learned spans over raw input;
- motifs often cross human-visible boundaries rather than reproduce a human tokenizer;
- 33,450 raw held-out units were represented by 2,789 adaptive motif units with exact round-trip in the prior tournament;
- motif-gated temporal workspace and support-gap recruitment improved grounded multi-event and one/few-shot behavior without English grammar or word labels.

R31 carried that lineage into the graph-free associative/episodic architecture rather than treating R30's fixed anonymous motif IDs as the final representation.

## 2. Support-gap recruitment survives

`R31_SUPPORT_GAP_ACOUSTIC_REFERENCE_ONLY.json` shows clean evaluation saturated at 1.0 and is therefore suspicious, but the harder battery remained roughly **0.89–0.92** across seeds and doses from 1 to 16 grounded exposures. The important mechanism is not the clean perfect score: the learner can identify and ground an unsupported raw span inside otherwise established constructions without receiving a human chunk boundary.

Support-gap recruitment is retained.

## 3. Compression alone is not intelligence

Several early chunk objectives exploited compression by constructing very long spans. That produced impressive compression while grounded discrimination stayed mediocre. Those objectives are not promoted merely because they reduce sequence length.

The decisive causal ablation used identical active context/evidence machinery:

| Route | Hard grounding | Near-twin | Confidently wrong | Compression gain |
|---|---:|---:|---:|---:|
| Raw active | **0.9213** | 0.8186 | 0.7510 | 0.0000 |
| Chunk-only active | 0.7533 | 0.7155 | 0.6621 | **0.8525** |
| Dual raw + chunk active | **0.9209** | **0.8363** | **0.7600** | **0.8525** |

This is the central R31 architecture result.

**Decision:** self-chunking is retained as a compression/indexing/grounded-construction/memory route, but it must not erase or replace raw episodic evidence. The dual route preserves essentially all raw hard capability while keeping ~85% compression gain and slightly improving near-twin discrimination.

## 4. Rich chunk identity is useful but not sufficient

Opaque chunk IDs lose internal evidence under speaker/noise/near-twin transformations. R31 added chunk signatures containing intrinsic microstate and transition statistics. These help some transfer conditions, but rich chunks alone do not solve confidently misleading evidence.

The architecture therefore keeps:
- reusable chunk identity;
- intrinsic chunk microstructure;
- literal/raw fallback;
- exact episodic retrieval.

A chunk is not an opaque vocabulary symbol.

## 5. Context and cross-modal disagreement are major evidence

The first post-repair comparison:

- acoustic-only active route hard mean: **0.6668**
- context-disagreement active route hard mean: **0.9017**
- always-reinspect hard mean: **0.8439**

Context-aware active route:
- near-twin: **0.7852**
- confidently-wrong: **0.6906**
- correlated-wrong safe: **0.7454**

Always asking again is not the answer. The value comes from detecting that independent grounded context disagrees with the first acoustic/chunk hypothesis.

## 6. Active physical consequences close much of the remaining gap

TNN was then allowed to choose the action/observation whose *learned predicted physical consequences* most separated its top competing hypotheses. The evaluator does not provide the identity or a speech boundary.

Result:
- hard acoustic mean: **0.9523**
- near-twin: **0.9149**
- confidently-wrong: **0.8776**
- hard-noise: **0.9923***
- onset damage: **0.9914***

The near-1 scores remain suspicious and are not treated as solved. The causal finding is that difficult self-chunk ambiguities can often be resolved by interacting with the grounded world rather than redesigning the chunker.

## 7. Sequential evidence and learned stopping

The best retained stopping policy uses internal evidence and delayed correctness/stability to decide when to commit, gather another physical observation, or return UNKNOWN.

Eight-seed aggregate:
- hard correct mean: **0.9698**
- speaker shift correct: 0.9628
- near-twin correct: **0.9421**
- confidently-wrong correct: **0.9162**
- correlated-wrong correct: **0.9331**
- correlated-wrong safe: **0.9610**
- mean physical probes: **1.396**
- genuine ambiguity abstention: **0.5717**

The final number is the important remaining boundary: the system is much better at correcting misleading evidence than at recognizing that *no unique answer exists*.

## 8. Probe-budget policies that failed

R31 preserved two negative results rather than tuning them away.

### Global learned probe budget
- stable/hard correct: ~0.6958
- ambiguous abstention: ~0.5058
- wrong commit: ~0.0029
- mean probes: ~2.07

It became over-conservative and still did not solve ambiguity.

### Generic state-dependent Random Forest policy
- hard correct mean: **0.6758**
- ambiguity abstention: **0.5439**
- near-twin correct: 0.6235
- confidently-wrong correct: 0.5340

It also traded away too much useful commitment for little ambiguity gain.

**Decision:** do not add more generic threshold/budget layers in R31. The open problem is a richer representation of epistemic instability/no-unique-answer over time, not another probe-count heuristic.

## 9. Regime/world-model memory

Naive multi-model consequence memory improved online adaptation but thrashed between models (~2,147 switches in the first bank test). R31 added evidence persistence/hysteresis.

Stable regime result:
- mean online accuracy: **0.8958**
- return first-200 accuracy: 0.6650
- retention regime 0: **1.000***
- retention regime 1: **1.000***
- retention regime 2: 0.8811
- average switches: **13.125**

Exact 1.0 retention is suspicious and remains challenge-worthy, but hysteresis clearly fixes the thrashing pathology.

## 10. Polysemous/context-specialized chunks

A blind chunk/consequence mapping sits near chance (**0.5081**) when the same perceptual span has context-dependent consequences. An unsupervised context specialization model selects **2.0** specializations on average and reaches **0.9423** with specialization purity ~0.94.

This is evidence for context specialization rather than overwriting a chunk's single meaning.

## 11. Chunk dynamics and delayed regret

R31's continuing-learning tests show a familiar pattern:
- new spans are learned rapidly with enough experience;
- unchanged single-history policies eventually overwrite old-world capability under very large shifted exposure;
- explicit contextual/regime memories preserve multiple consequence histories better than one mutable model.

The Zag target now includes actual learner-driven chunk split and merge operations, archival eligibility, delayed-regret utility updates, support-gap recruitment, hierarchy, and context specialization. Those source mechanisms are **not yet natively quantified** because `znc` is unavailable here.

## 12. Integrated reference life

The earlier R31 integrated life reached 120k reference events with zero newborn restarts. Before the regime repair, identity/acoustic/sibling behavior was strong but action performance collapsed after changed physics because one consequence model was overwritten. `R31_INTEGRATED_V2_PART1` then demonstrated the intended repair: after the physics change, the learner recruited a second regime model and action performance recovered strongly by 120k–125k.

Nominal exact 1.0 values in that integrated run are treated as suspicious; the post-repair component batteries above provide the more informative boundaries.

## 13. Native Zag target status

Latest static target:
- file: `tnn_r31_endogenous_chunking.zag`
- SHA-256: `603424bc01ccb37ffff1ded971333b05c7dc75778da3a4bbd0a00cd156604aa7`
- ~1,148 lines
- source contract: PASS

Required mechanisms present:
- graph-free architecture;
- no transformer/tokenizer/next-token path;
- endogenous repeated-span recruitment;
- reversible segmentation + literal fallback;
- rich chunk microstructure;
- support-gap recruitment;
- delayed chunk regret;
- hierarchy;
- learner-driven split/merge;
- context/regime consequence memory;
- regime-switch hysteresis;
- learned reinspection;
- active discriminating physical probes;
- learned commit/continue/abstain reliability;
- dual raw/chunk evidence arbitration;
- raw retrieval when chunks are lossy/uncertain;
- 0/100 extreme-score diagnostic gate;
- episodic memory and causal traces.

**Native quantitative execution is not established.** Multiple attempts to clone/fetch the official `Sylorlabs/zag` compiler failed due runtime DNS/network/binary-materialization constraints. Python/reference numbers above cannot promote the brain.

## 14. Final R31 decision

**R27 remains canonical.**

R31 is a strong shadow architecture/evidence checkpoint with the following promoted *research direction*:

> **raw episodic perception + endogenous reversible chunks + support-gap/hierarchy/context specialization + active grounded evidence + explicit uncertainty**

Not:

> fixed tokens -> transformer/LLM sequence prediction

and not:

> chunk compression replacing raw perception.

## 15. Open boundary

The highest-value unsolved capability is now **epistemic ambiguity over time**: distinguishing a temporarily difficult but resolvable situation from a world state that genuinely does not determine a unique referent/outcome. The best R31 sequential policy is strong on misleading evidence but abstains on only ~57% of deliberately no-unique-answer cases.

That should be attacked with persistent multi-hypothesis world-state uncertainty and longer cross-modal evidence histories, not more tokenization or probe-count tuning.
