# K9 Result: Interference Test

**Date:** 2026-09-29 03:45 PDT
**Test:** K9 Interference (200 unrelated facts)

## Setup

- Base: v3 world (24 facts, 4 true concepts, 8 probes).
- Interference: 200 noise facts (noise1..noise200, each with unique object).
- Total: 224 T facts.

## Results

**Unifications:** All 4 true concepts still form correctly.
- norpal ~ squeezer (jacc 2/4)
- (others confirmed via score)

**Score:** 8/8 (unchanged from baseline 8/8).

**Noise:** 200 noise surfaces do NOT unify (each has unique signature).

## Verdict

**H-KILL WEAKENED (for interference).** The mechanism is robust to 200 unrelated
facts. Noise with unique signatures does not interfere with true concepts.

**Why it works:** Jaccard requires shared (R,O) pairs. Noise facts use unique
objects (onoise1, onoise2...), so Jaccard(noise_i, true_concept) = 0. No false merges.

**Limitation:** This is "easy" interference (unique signatures). Harder interference
would use overlapping vocabularies. Not tested.

**Implication:** The L2+ mechanism is practically robust to irrelevant data, as long
as the irrelevant data doesn't share consequence signatures with true concepts.
