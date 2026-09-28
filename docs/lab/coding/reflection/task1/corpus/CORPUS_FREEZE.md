# Prior-art corpus — freeze record (2026-09-22)

**Status:** FROZEN. Installed only through the learner's `teach` (with audit
entries) in the INFORMED arm. Any change needs a dated amendment with
Micah's re-approval.

- File: `corpus/records.txt`
- sha256: `3ff512a3367350374c19e6c26615fd4f5547d1bb2353098e2f37bcb30d71c2c7`
- 12 records, format `@ID / T:ARCH / K:keywords / prose / @end`
  (same record format the KB installer accepts).

## Content rule (verified by inspection at freeze)

Each record describes ONE architectural idea in prose: compositional
planning, recursion, nested loops, sentinel scans, char-class filtering,
multi-accumulators, modular dispatch, run grouping, bitwise walking,
deliberate revision, plan-then-emit, teaching audit. **No Zag code, no code
sketches, no full solutions to any T4x item.** C-ARCH-02 states the
factorial recurrence as mathematics (`fact(n) = n * fact(n-1)`), which is
the idea of recursion, not a Zag program — the learner must still write
the function form, argument handling, and output itself.

## What the corpus is FOR (INFORMED arm hypothesis)

The coding KB (69 entries) contains no entry whose keywords name the T4x
constructs (verified: no KB keyword matches recursion/nested/sentinel/
filter/fizzbuzz/run-length/popcount). The corpus supplies the semantic
bridge: its keywords overlap the T4x spec words, so the learner's recall
can map a novel spec to composable mechanisms. The FROM-SCRATCH arm does
not receive it; the arm gap measures the bridge's value.
