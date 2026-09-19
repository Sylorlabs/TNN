# R5 results

## 1. Broad developmental screen

The initial screen executed 240 runs: five sensory architectures, sixteen
training histories, and three independent generated worlds. It established two
separate facts:

- temporal/local sensory processing can improve identity and robustness;
- sensory grounding does not repair a weak language-memory architecture by
  itself.

The earliest flat/prototype language designs stayed near chance-to-low accuracy
on held-out meaning even when perception improved. This triggered architectural
revision rather than indefinite data scaling.

## 2. Language architecture revisions

The retained sequence was:

1. flat fast/slow prototypes — poor held-out transfer;
2. feature-local evidence and provenance-aware repetition — improved but
   plateaued;
3. position-invariant lexical motifs plus position-sensitive construction
   motifs — approximately 76–79% held-out component accuracy;
4. contrastive raw-byte motif discovery — strong controlled compositional
   meaning without a parser;
5. hybrid audio PAM — retained stable global frequency identity while adding
   recurrent local temporal detail;
6. motif-gated temporal discourse workspace — preserved earlier explicit
   entities while later byte windows updated only factors with direct motif
   evidence.

A broad surprise-span memory was rejected: it improved some one-shot cases but
regressed established meaning and consumed excessive compute. A more selective
version remained inconsistent and was not promoted.

## 3. Training-mixture confirmation

### Medium budget: 512 developmental exposures

Five new worlds, recurrent PAM architecture:

| History | Goldilocks score | Fused exact | Stress exact | Held-out text component | Video component | Audio component |
|---|---:|---:|---:|---:|---:|---:|
| noisy → clean, all modalities | **0.9580** | **1.0000** | **1.0000** | **1.0000** | 0.6758 | 0.9650 |
| clean → noisy, all modalities | 0.9483 | 0.9933 | 0.9933 | 1.0000 | 0.6700 | 0.9638 |
| text first → all modalities | 0.9430 | 1.0000 | 1.0000 | 1.0000 | 0.6546 | 0.9629 |
| mixed from birth | 0.9422 | 0.9733 | 0.9733 | 0.9958 | **0.6892** | **0.9717** |
| text only | 0.9242 | 0.9950 | 0.9950 | 1.0000 | 0.0000 | 0.0000 |
| video+audio+action, then text | 0.8879 | 0.8317 | 0.8300 | 0.9521 | **0.7050** | 0.9708 |

Text-only scores well on the bounded text metric but has no grounded senses. It
therefore cannot be the integrated Goldilocks solution. The delayed-language
condition has the best isolated video score here but substantially worse fused
meaning, which is why “video first” is not the winner.

### Larger budget: 1,024 exposures

Three additional worlds:

| History | Goldilocks score | Fused exact | Stress exact | Video | Audio |
|---|---:|---:|---:|---:|---:|
| noisy → clean | **0.97225** | 1.0000 | 1.0000 | 0.7444 | 0.9819 |
| mixed from birth | 0.97192 | 1.0000 | 1.0000 | 0.7382 | **0.9840** |
| text first → all | 0.96067 | 1.0000 | 1.0000 | **0.7486** | 0.9792 |
| clean → noisy | 0.95996 | 1.0000 | 1.0000 | 0.7354 | 0.9833 |

The order advantage narrows with more experience. The current interpretation is
not that noise is inherently good; moderate variation followed by clean
correction helps the current substrate establish invariance without leaving the
final state dominated by corruption.

## 4. Architecture and compute

At 512 exposures under `noisy_then_clean`, three new worlds:

| Architecture | Goldilocks | Fused exact | Stress exact | Video | Mean operations | Mean memory bytes |
|---|---:|---:|---:|---:|---:|---:|
| recurrent PAM + hybrid audio | **0.9553** | **1.0000** | **1.0000** | 0.6694 | 176,131,176 | 688,315 |
| cross-modal PAM | 0.9544 | 0.9583 | 0.9583 | **0.6979** | 176,269,804 | 688,786 |
| shallow PAM | 0.9514 | 0.9806 | 0.9806 | 0.5090 | **165,835,432** | **614,795** |
| central raw | 0.9412 | 0.9528 | 0.9528 | 0.6090 | 169,522,148 | 640,069 |

The recurrent design is the balanced winner, but shallow PAM remains a valid
Contextual Architecture Revision (CAR) alternative when compute/memory limits
matter more than video performance. It uses about 5.8% fewer recorded operations
and about 10.7% less memory than recurrent PAM in this confirmation.

## 5. Promoted discourse revision

Five-world shadow comparison:

| Mechanism | Controlled exact | Stress component | Multi-sentence reference exact |
|---|---:|---:|---:|
| previous whole-text decoder | 1.0000 | 1.0000 | 0.2000 |
| motif-gated temporal workspace | 1.0000 | 1.0000 | **1.0000** |

The candidate preserved prior explicit entities and allowed later local windows
to update event/object/state evidence. It used byte windows and motif confidence,
not punctuation, sentence labels, pronoun rules, or English grammar.

## 6. Hard teenager boundary

Five independent worlds after the promoted discourse revision:

| Capability | Result |
|---|---:|
| controlled held-out exact meaning | 0.9700 |
| novel paraphrase-frame exact meaning | 0.9617 |
| bounded internal tuple retrieval from question context | 0.9667 |
| simple multi-sentence reference exact | 0.9708 |
| one-shot new label, transferred to another construction | **0.3125 target role** |
| explicit uncertainty/abstention | NOT_MET |
| negation and polarity | NOT_MET |
| conditionals/counterfactuals | NOT_MET |
| ambiguity resolution | NOT_MET |
| metaphor/humor/pragmatics | NOT_MET |
| long documents | NOT_MET |
| natural-language explanation/generation | NOT_MET |
| spoken English | NOT_MET |

Therefore:

```text
TEENAGER_ENGLISH=0
ADULT_ENGLISH=0
PRODUCTION_TNN_V1=NOT_PROMOTED
```
