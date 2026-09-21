---
id: H-03
title: "Endogenous self-chunking with support-gap recruitment"
status: PROVISIONAL
hypotheses: [H-03]
updated: 2026-09-19
---

# H-03 — Endogenous self-chunking with support-gap recruitment

## Claim
The learner should recruit its own reversible spans over raw input — motifs that
often cross human-visible boundaries rather than reproduce a human tokenizer —
and should be able to ground an unsupported raw span inside otherwise
established constructions without being handed a human chunk boundary.

## Why it matters
It operationalizes learner-owned representation (H-06) at the perceptual level;
CTC-like machinery may remain only as a generic alignment primitive *after*
chunks exist.

## Evidence
| Experiment / source | Result | Status |
|---|---|---|
| R31 support-gap recruitment | Held ~0.89–0.92 on harder battery across seeds/doses (clean 1.0 scores treated as suspicious) | REFERENCE_ONLY |
| R31 context specialization | 2.0 specializations avg, 0.9423, purity ~0.94 — beat blind chunk/consequence mapping (0.5081) for polysemous spans | REFERENCE_ONLY |
| R31/R32 Zag sources | Learner-driven split/merge exists in Zag source | PROVISIONAL — lacks native quantitative validation |

This lineage traces to the user's correction of R30 — the program explicitly
pivoted away from fixed-token/transformer framing at user direction.

## Open questions
- Native quantitative validation of split/merge and support-gap recruitment.
- Natural continuous speech/video self-chunking is unqualified (R31 speech
  tests were synthetic eSpeak research only).
