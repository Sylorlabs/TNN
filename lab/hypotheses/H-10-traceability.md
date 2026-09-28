---
id: H-10
title: "White-box causal traceability as a protected feature"
status: PROVISIONAL
hypotheses: [H-10]
updated: 2026-09-19
---

# H-10 — White-box causal traceability as a protected feature

## Claim
Promotion-eligible state must be serializable, provenance-linked,
integrity-checked, and inspectable; every consequential mutable decision needs
a parent-linked causal trace (evidence → hypothesis revision → memory change →
action → observed consequence → delayed regret). Explanations must reconstruct
from durable state.

## Why it matters
It's what makes the autonomy position (H-06) auditable rather than rhetorical.

## Evidence
| Experiment / source | Result | Status |
|---|---|---|
| Native infrastructure | Full ledgers, SHA-pinned sources/binaries/outputs, independent recomputation (E51AJ: 21 analysis + 11 verifier tests); byte-identical native builds; 33/33 verifier reruns; 24,601-check engineering passes (N13A) | PROVISIONAL — infrastructure-strong, cognition-unproven |
| R33-B000 audit | The prototype trace helper **silently drops an event at saturation** (8,193 attempts → 8,192 records) — a concrete defect in the very machinery meant to guarantee traceability, now a specified B001 gate | NEGATIVE (as a measurement of the helper) |

Trace *mechanisms* exist in Zag sources; the cognitive side (traces that
actually explain decisions) is unproven.

## Open questions
- B000's five confirmed boundary defects (substrate transform loses channel
  order; acoustic window misses unsampled detail; trace helper drops a record
  at saturation; output limits silently omit tails) — corrective
  implementation is an active workstream.
- Whether reconstructed explanations from durable state can pass the
  anti-facade tests.
