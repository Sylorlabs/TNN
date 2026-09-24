# H5 Resolution runlog

## grok-4.7 round-1: FAILED (provider-side, 11+ attempts)
- Symptom: HTTP 200 with empty content, or HTTP 524 / socket timeouts, on H5 design questions.
- Tried: full 6KB prompt + reasoning_effort=high (4x empty), split per-question + high (524s),
  streaming (died early), compact single-question + high (524), compact single-question plain (socket timeout),
  medium unrelated prompts + high (WORKED), tables-only + high (WORKED), questions-only + high (524),
  focused battery-design prompt plain (3x EMPTY), trivial "UP" (worked, 53s).
- Pattern: trivial/tables/medium prompts work; H5 open-ended design questions consistently fail.
  Backend degraded on this content right now (53s for a 1-word reply).
- Sol: still provider-down (choices:null, 0 completion tokens) — 5th consecutive failure.
- Decision: proceed with native debate on grok's RECORDED proposals (DEBATE_H5.md) + steelmen.
  Round-1 specifics (recalibration formula, bound formalization) deferred; CEILING crew got the
  battery spec from the adjudication + STEELMAN.md which is sufficient.
- Standing-policy note: reasoning_effort=high is NOT the cause (failures occur with and without it).
  grok47.py wrapper kept at high reasoning per policy; failure is provider-side.
