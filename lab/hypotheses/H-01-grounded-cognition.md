---
id: H-01
title: "Grounded cognition over symbol prediction"
status: PROVISIONAL
hypotheses: [H-01]
updated: 2026-09-19
---

# H-01 — Grounded cognition over symbol prediction

## Claim
Intelligence needs a high-fidelity episodic route, learner-created reusable
abstractions, and the ability to act for evidence — not next-token prediction
over fixed tokens.

## Why it matters
This is the founding bet and the reason the program is deliberately not a
transformer, LLM, BPE/tokenizer pipeline, next-token objective, fixed knowledge
graph, or confidence-threshold classifier. Externally supplied word, phoneme,
VAD, or chunk boundaries are not to be treated as cognition.

## Evidence
| Experiment / source | Result | Status |
|---|---|---|
| R31 shadow program (dual-route ablation, support-gap recruitment) | Direction-setting quantitative support in shadow runtime | REFERENCE_ONLY |
| Program architecture docs (`docs/program/`) | Position stated, never experimentally established natively | PROVISIONAL |

The repo is explicit: this is a research direction, not a result. Nothing
natively qualifies a full grounded learner.

## Open questions
- Does any shadow architecture (dual route, support-gap recruitment,
  split/merge) survive native quantification once the sensory gate is real?
- Sensor qualification (audio, vision) is NOT_QUALIFIED; only
  synthetic-temporal evidence is partial.
