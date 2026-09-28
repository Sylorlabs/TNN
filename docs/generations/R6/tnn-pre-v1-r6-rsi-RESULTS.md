# TNN pre-v1 R6 results

## Release decision

R6 promotes a **research candidate**, not production TNN v1. The promoted
change is Grounded Contrastive Schema Memory with support-gap recruitment and a
protected fast path. The candidate passed calibration and hidden regression
checks in the generated multimodal world.

```text
BOUNDED_SAR_RESEARCH_GATE               PASS
OPEN_ENDED_RSI                           NOT_MET
HUMAN_SUPERIORITY                        NOT_EVALUATED
TEENAGER_ENGLISH                         NOT_MET
ADULT_ENGLISH                            NOT_MET
PRODUCTION_TNN_V1                        NOT_PROMOTED
```

## 1. Failure-triggered revision and rollback

R5's strongest unresolved language-memory failure was cross-construction use of
a genuinely new grounded label. The unchanged R5 branch reached only 0.2813 on
calibration and 0.3438 on hidden target-role accuracy.

The first schema branch substantially improved new-label binding but updated too
much familiar structure during continuing learning. On the first hidden run it
reached 0.8594 one-shot target accuracy while established-language exactness
fell from 0.9911 to 0.9291. It was rejected and is preserved under
`attempts/r6_unprotected_revision/`.

The revised mechanism made two generic changes:

1. **Support-gap recruitment:** only the unsupported captured raw-byte span is
   eligible for one-shot growth; familiar grounded spans are not rewritten.
2. **Protected fast path:** a new surface label enters shadow memory after the
   brain's own video/audio/action state estimate; competent sensory and
   established-language maps are not globally retrained merely because the
   surface label is new.

## 2. Hidden bounded-SAR result

Four calibration seeds selected the mechanism and four untouched seeds evaluated
promotion.

| Metric | R5 unchanged | Promoted R6 | Change |
|---|---:|---:|---:|
| Cross-frame one-shot target | 0.343750 | **0.828125** | +0.484375 |
| Cross-frame whole meaning | 0.281250 | **0.828125** | +0.546875 |
| Shared-fragment target | 0.250000 | **0.822917** | +0.572917 |
| Delayed target | 0.306250 | **0.818750** | +0.512500 |
| Contradiction target | 0.500000 | **0.750000** | +0.250000 |
| Established exact, before | 0.854536 | 0.991135 | — |
| Established exact, after | 0.899970 | **0.991135** | 0.000000 R6 regression |
| Sensory clean/stress mean, before | 0.802083 | 0.802083 | — |
| Sensory clean/stress mean, after | 0.770833 | **0.796875** | -0.005208 R6 regression |
| Snapshot reload parity | 1.000000 | **1.000000** | unchanged |

The broad novelty branch was correctly rolled back. It produced some immediate
new-label hits but reduced hidden established-language exactness to 0.0696 and
whole-meaning fragment exactness to 0.0625.

## 3. What the promoted mechanism learns

The new memory does not receive words, spaces, parts of speech, or English
rules. It:

- measures recurring raw-byte spans over grounded episodes;
- contrasts alternatives within each latent factor to remove shared
  construction material;
- derives reversible construction skeletons from recurring fixed segments and
  grounded variable spans;
- identifies a single unsupported span in an otherwise grounded construction;
- attaches that span to the brain's own cross-modal state estimate;
- retains the baseline pathway when schema evidence is absent or weak.

This is Contextual Architecture Revision in a limited sense: the old path remains
available, and the new path is used only when its evidence is locally relevant.

## 4. Independent one/few-shot efficiency curve

A second hidden seed set introduced 24 new concepts per seed and varied exposure
count. Each test changed the construction and surrounding latent factors.

| Learner | 1 example | 2 | 4 | 8 |
|---|---:|---:|---:|---:|
| R6 grounded schema | **0.885417** | **0.916667** | **0.927083** | **0.937500** |
| R6 compact schema | 0.854167 | 0.916667 | 0.927083 | 0.937500 |
| R5 unchanged | 0.312500 | 0.354167 | 0.447917 | 0.458333 |
| Nearest-surface control | 0.312500 | 0.343750 | 0.385417 | 0.427083 |
| Hardcoded prosthesis control | 1.000000 | 1.000000 | 1.000000 | 1.000000 |

The hardcoded branch is artificial and excluded from TNN promotion. It receives
human-authored templates plus explicit lexicon insertion for every novel label.

R6's one-example update added about 960 bytes of persistent memory and consumed
about 15.5 million counted operations. R5 used about 749 bytes but approximately
20.3 million operations while scoring only 0.3125. Thus R6 is substantially more
accurate and uses fewer counted operations in this bounded task, at a modest
memory cost.

## 5. Exposure Goldilocks boundary

Immediate accuracy rose with more examples, but delayed target accuracy peaked
at two examples:

```text
1 example   0.885417 delayed
2 examples  0.927083 delayed
4 examples  0.895833 delayed
8 examples  0.864583 delayed
```

This is a real negative result. The current learner does not yet know when
additional teaching has stopped adding information. Saturation detection and
self-chosen consolidation are next-stage architecture problems.

## 6. Persistence

A selected seed-13 brain is included under `state/`. With
`PYTHONHASHSEED=0`, two independent builds produced byte-identical pickle state
SHA-256:

```text
49c6aa2108b12421a4918948847601d4441ae3696bd5ebc55337565351daecca
```

Reloaded predictions matched the pre-save predictions. The format is a Python
research snapshot, not a portable production state format.
