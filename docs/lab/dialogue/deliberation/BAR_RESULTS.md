# Deliberation v1 — Bar Results

**Frozen source SHA:** d433bd06a102df5842b09318b86caa4e0d4e0ae075e3516bae8c9f85f5403c64
**Date:** 2026-09-27

## Validity
- Byte-identical reruns: PASS (R4 stdout+stderr, B20 stdout+stderr)

## K1 — Order Invariance
- 77 turns (29 R4 + 28 B20 + 20 heldout), 0 A-line diffs: PASS

## K4 — Accuracy
- Round4: 27/29 turns (2 known-unachievable): PASS
- Trace-trial: 28/28 turns: PASS

## K2, K3, K5
- K2: NOT RUN (requires red-team flips)
- K3: NOT RUN (requires independent parser)
- K5: Out of scope (independent red team only)

## Close-Call
- Mechanism implemented, scoring allows <5 margins: PARTIAL
- Natural trigger not observed; synthetic demonstration pending
