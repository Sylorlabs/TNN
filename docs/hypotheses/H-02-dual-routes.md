---
id: H-02
title: "Raw evidence stays first-class; chunks are reversible hypotheses (dual route)"
status: PROVISIONAL
hypotheses: [H-02]
updated: 2026-09-19
---

# H-02 — Raw evidence stays first-class; chunks are reversible hypotheses

## Claim
Compression is not understanding. A compressed chunk may be useful and still be
wrong in exactly the way that matters, so an exact/high-fidelity episodic route
must run alongside learned chunks, with literal/raw retrieval when a chunk loses
needed detail.

## Why it matters
It constrains every representation the learner is allowed to form — chunks get
no authority to destroy raw experience.

## Evidence
R31 decisive causal ablation, identical active context/evidence machinery
(all REFERENCE_ONLY — shadow runtime):

| Route | Hard grounding | Confidently wrong | Compression gain |
|---|---|---|---|
| Raw active | **0.9213** | 0.7510 | 0.0000 |
| Chunk-only active | 0.7533 | 0.6621 | **0.8525** |
| Dual raw + chunk | **0.9209** | **0.7600** | **0.8525** |

Repo's decision: chunk-only sensory representation is **rejected** (compresses
strongly, loses hidden grounding); the dual route is retained — it preserves
essentially all raw hard capability while keeping ~85% compression gain.
Related shadow findings: predictive-surprise/giant-span chunk objectives are
rejected as primary criteria (impressive compression, mediocre grounding);
rich chunk identity (intrinsic microstate/transition statistics) helps transfer
but doesn't solve confidently misleading evidence. None of this is natively
quantified.

## Open questions
- Native quantification of the dual route under real sensory qualification.
- Whether chunk identity statistics transfer to native Zag execution.
