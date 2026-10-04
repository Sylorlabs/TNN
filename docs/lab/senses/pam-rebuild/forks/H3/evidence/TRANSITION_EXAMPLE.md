# H3 Transition Example (human-readable)

## What a StateTransition is

H3 does not just output a label. For every fixture it emits a **StateTransition**:
what it saw (T0), what it *predicted* would be true if each possible claim held
(the counterfactual branches), which predictions confirmed or broke, and the
resulting memory disposition. Transitions are hash-chained into an append-only
ledger, so the full reasoning trace is replayable.

## Worked example: the "tab" adversarial fixture

Fixture: `h3a_t3_000.img` — a white circle (r=28) with a 10×40 rectangular tab
attached to its right side. Truth: CIRCLE.

Raw H3 output (verified against the built binary, 2026-09-22):

```text
t0=SQUARE
judgment=SQUARE
disposition=WITHDRAWN
confidence=298
ops=138240
transition=H3|task=shapetrans|fx=.../fixtures/h3adv/h3a_t3_000.img|t0=SQUARE|br=0:0:3;1:2:1;2:0:3;|inst=NONE|disp=WITHDRAWN|judge=SQUARE|dur=0|
chain=7c84bc683810106199ba8091874eddaf309e97c5c89090878db25e38026ff7e1
```

(truth=CIRCLE, from `h3a_t3_000.img.truth`.)

What happened, in plain language:

1. **T0 (the fast perceiver)** saw the shape and said **SQUARE**. The tab adds
   enough area that the circle's area/R² ratio looks square-like. T0 was fooled.
2. **Counterfactual branches**: H3 spun up one branch per possible claim
   (CIRCLE, SQUARE, TRIANGLE). Each branch made testable predictions:
   - P1: the shape classifies the same at two nearby brightness thresholds
   - P2: the shape classifies the same at a third threshold
   - P3: the shape's rotational symmetry matches its claimed class
3. **SQUARE's branch** confirmed P1 and P2 (the tab doesn't change threshold
   behavior) but **broke P3**: a square rotated 90° should overlap itself
   almost perfectly (≤120 differing pixels per mille), but the tabbed circle
   differs by far more. **One broken prediction is enough to kill the branch.**
4. **Disposition: WITHDRAWN.** H3 did not install the false SQUARE claim.
   The judgment falls back to T0 (SQUARE) but the memory system records that
   this claim was tested and withdrawn — it will not be acted on, and the
   negative evidence is retained.

The transition string encodes all of this compactly:

```
H3|task=shapetrans|fx=<path>|t0=SQUARE|br=0:0:3;1:2:1;2:0:3;|inst=NONE|disp=WITHDRAWN|judge=SQUARE|dur=0|
```

- `br=0:0:3` — CIRCLE: 0 confirmed, 3 broken
- `br=1:2:1` — SQUARE: 2 confirmed, 1 broken (P3)
- `br=2:0:3` — TRIANGLE: 0 confirmed, 3 broken
- `inst=NONE|disp=WITHDRAWN` — no claim installed; T0's claim withdrawn
- `chain=<sha256>` — this transition's hash-chained ledger entry

## Why this matters

A traditional classifier would have output "SQUARE" with some confidence and
moved on. H3 output "SQUARE" too — but then *tested* the SQUARE hypothesis
against its own predictions, found it wanting, and refused to commit it to
memory. The false percept was caught by H3's own counterfactual machinery,
not by an external oracle.
