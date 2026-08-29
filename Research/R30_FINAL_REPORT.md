# R30 Big Boom — Final Shadow Research Report

## Executive result

R30 strongly validates the decision to run a long developmental training campaign before diagnosing architectural failure. The clearest example is no-VAD speech: the same fixed-acoustic-identity CTC learner progressed from exact **0%** at 1,024 utterances to **96.56% hard exact-sequence accuracy at 100,000 utterances** without changing the core speech architecture. This is direct evidence that the early zeros were undertraining, not proof of architectural failure.

The user-requested extreme-score policy was also empirically useful: exact 0% and 100% repeatedly identified either undertraining, evaluator saturation, trivial controls, or a distribution-specific result that required a harder follow-up. No exact extreme is accepted at face value in this generation.

R30 remains a **shadow** result because the local `znc` compiler could not be materialized and a container reset erased the unpersisted raw R30 workspace. The metrics below were observed in completed execution and were immediately reconstructed into the durable recovery ledger after the reset. They are not being relabeled as native-Zag evidence.

## 1. Lineage

R27 was independently verified again during R30:

- 33/33 verifier checks PASS
- development step: **60,423**
- newborn restarts: **0**
- accepted digest: `562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04`

R27 remains canonical. R30 is a shadow continuation design and experimental evidence set.

## 2. Graph-free architecture

The reconstructed R30 native target passes a static source contract requiring:

- no active graph runtime;
- no graph/node/edge cognitive substrate;
- associative episodic identity;
- TNN-owned memory with heuristic default and learned override;
- LRU not used as semantic memory authority;
- non-graph Foundry;
- causal parent-linked tracing;
- no-VAD CTC core;
- automatic exact-0/exact-100 diagnostic escalation.

Source SHA-256: `2c439aacfca04fae2a940f125af0d255e23e8aae5dddf2985980cbf63221396c`.

## 3. Long no-VAD speech development

Primary seed 30301, hard exact sequence accuracy:

| Connected utterances | Hard exact | Token accuracy | Silence-shift exact | No-gap exact | Long sequence exact |
|---:|---:|---:|---:|---:|---:|
| 1,024 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| 4,096 | 0.00% | 15.01% | 0.00% | 0.00% | 0.00% |
| 9,600 | 0.63% | 41.17% | 3.85% | 0.00% | 0.00% |
| 19,200 | 45.31% | 84.99% | 80.00% | 21.15% | 32.27% |
| 38,400 | 88.13% | 97.45% | 96.54% | 80.38% | 77.27% |
| 57,600 | 94.06% | 98.87% | 99.23% | 92.69% | 90.00% |
| 76,800 | 96.25% | 99.32% | **100.00%*** | 96.15% | 95.00% |
| 100,000 | **96.56%** | **99.38%** | **100.00%*** | **95.38%** | **97.73%** |

`*` Automatically quarantined by the perfect-score suspicion rule.

At the common 57,600-utterance dose, three independent seeds reached 94.06%, 95.31%, and 91.56% hard exact respectively. The later container reset prevented preservation of the two replication seeds' 100k endpoints; they are deliberately not claimed.

A greedy-vs-prefix-beam check at 19,200 utterances showed only modest gains from decoding. The large improvement was therefore primarily training/representation development, not a decoder trick.

### Speech conclusion

The central R30 speech finding is causal: **long training transformed a total-looking failure into high-90s bounded performance without replacing the core CTC architecture.** Remaining work is robustness, not proof that CTC cannot learn.

## 4. Long graph-free developmental life

The reference long-life campaign reached 100k events with a real fresh-process save/reload and was later continued to 120k with corrected global developmental thresholds.

At 100k:

- identity: 94.21%
- true switching: 94.24%
- action choice: 95.67%
- sibling transfer: 98.31%
- active reinspection rate: 13.56%
- hard identity diagnostic: 70.0%
- names: 100% — quarantined as evaluator saturation

Corrected global-threshold continuation at 120k:

- identity: 93.58%
- true switching: 93.56%
- action choice: 95.48%
- sibling: 98.77%
- hard identity diagnostic: 72.5%
- names: 100% — still quarantined

The original resumed segment had a discovered harness flaw: some curriculum thresholds were segment-relative after reload. The underlying state persisted, but the mature curriculum temporarily paused some evaluations. That flaw was fixed by using global developmental step in the later continuation.

## 5. Extreme-score adversarial diagnostics

The clean entity tests often hit 100%, but harder counterfactuals revealed the actual boundary:

- severe occlusion: **70.17%**
- confident wrong view then clean reinspection: **79.83%**
- confident wrong evidence twice: **58.0%**
- half sensory channels removed: **79.17%**
- identity/appearance conflict: **81.17%**

Thus the nominal 100s were not treated as solved identity. The remaining entity challenge is largely confidence reliability and evidence arbitration under missing or confidently misleading input.

## 6. Training versus architecture: changed physics

When the physical action rules changed abruptly, performance initially collapsed. Instead of redesigning the world model immediately, R30 ran a dose curve with architecture held fixed:

| Changed experiences | Accuracy |
|---:|---:|
| 0 | 0.75% |
| 300 | 1.17% |
| 1,000 | 2.75% |
| 3,000 | 5.17% |
| 10,000 | 62.17% |
| 30,000 | **96.33%** |

This is another strong R30 result: a near-zero post-change score was predominantly a **training/history replacement problem**, not immediate evidence that the architecture could not adapt.

## 7. Master teacher

The experiments show two seemingly conflicting facts that resolve cleanly:

1. A diagnostic Master can materially improve hard performance when targeting learner failures.
2. Over-fine targeting can fill finite episodic capacity with repeated hard cases and damage broad coverage.

The correct direction is therefore a **capacity-aware diagnostic Master with explicit diversity protection**, not purely random teaching and not hard-example-only teaching.

## 8. Memory

Under severe resource pressure, exact recall falls sharply even with the default heuristic. Increasing memory budget restores it, confirming that resource envelope is a major causal variable.

At a 50k budget:

- locked heuristic exact recall: 70.78%
- conservative regret override: **73.77%**
- aggressive override: **99.74%***
- LRU-as-representation: **0%*** exact recall

Both extremes were quarantined. The aggressive policy appears to exploit abundant budget by nearly storing everything exactly and does not generalize to tighter budgets. LRU representation destroys exact detail and remains rejected.

R30 therefore retains:

> privileged heuristic at birth → TNN authority → conservative learned regret overrides → LRU for physical eviction only.

## 9. Architecture Foundry

A first longitudinal Foundry history learner failed badly because it pooled experience across unrelated phase landscapes. That was diagnosed as stale credit transfer.

After adding observable failure-context keys, the contextual hybrid became the best mean strategy:

- random: 5.7711
- evolution: 7.0366
- contextual retrieval: 6.4331
- contextual learned mutation: 6.8494
- **contextual hybrid: 7.1522**

Contextual hybrid beat random in **212/240** comparisons and evolution in **148/240**.

This supports a specific mechanism: architectural experience should transfer only when current failure telemetry resembles the prior experimental regime.

## 10. Active perception and episodic memory

Matched entity ablation:

- full episodic + active reinspection: 79.78%
- full episodic passive: 56.05%
- one-view + active: 75.60%
- centroid + active: 89.95%
- centroid passive: 54.0%

Active reinspection is clearly causal. A centroid helped on the unimodal synthetic denoising battery, so a deliberately multimodal identity battery was then run:

- exact episodic population: **99.49%***
- centroid: 95.79%

The near-100 episodic result is itself considered suspiciously easy, but the comparison demonstrates why R30 should not discard exact episodic populations simply because centroid compression works on a unimodal benchmark.

## 11. Name grounding

The clean one-shot name task saturated at 100%, so harder teaching-time uncertainty was introduced:

- occluded teaching: 77.70%
- confidently corrupted teaching: 82.86%
- near-twin teaching: 92.21%

This converts a saturated metric into a meaningful grounding problem.

## 12. Traceability

Before reset, the 100k life trace contained:

- 7,415 records
- 7,415 unique IDs
- 0 duplicate IDs
- 0 broken parent links
- steps 1–100,000
- newborn restarts: 0
- state SHA-256: `6c4e5036cad5dbadb7470434227a73db6546332c483a10cac9770fc49f7be655`

A later continuation expanded tracing for action/name/sibling decisions, but its raw file was lost in the container reset. This is explicitly part of the release boundary.

## 13. Native evidence boundary

The official Zag repository and compiler provenance were repeatedly confirmed, but the active terminal could neither clone GitHub nor materialize the committed compiler binary. Therefore:

- graph-free R30 Zag target exists and passes the static source contract;
- generic no-VAD CTC forward logic is represented in Zag;
- native quantitative R30 execution is **not established**;
- Python/reference R30 measurements are **non-promotable**.

## 14. Decision

**R27 remains canonical. R30 is a strong shadow developmental checkpoint.**

The highest-value discoveries are:

1. long CTC training is decisively effective;
2. 0/100 suspicion diagnostics catch real evaluator/training problems;
3. abrupt world changes require large adaptation dose before architecture blame;
4. active reinspection is a major identity capability;
5. memory performance is resource-sensitive;
6. teacher targeting must be capacity/diversity aware;
7. learned architecture history requires context-aware credit transfer;
8. adversarial confidence under ambiguous/corrupted perception remains an open entity bottleneck.
