# Fallback log — GOAL-B story track

## 2026-09-22 ~06:30 UTC: grok-4.7 (ExperimentalLabs) DOWN — out of platform credits
- First call: read timeout at 90s (long prompt).
- Retry: HTTP 429 `insufficient_credits`: "Your organization is out of platform credits
  (balance: $-0.02). Add credits at https://platform.experientiallabs.ai/credits."
- Per Micah's fallback chain (grok-4.7 weird → muse native or gpt-5.6-sol via UnoRouter):
  this track now uses **gpt-5.6-sol via UnoRouter** for all LLM reasoning
  (red-teaming, B2 rating, autopsy, intelligence verdict).
- NOTE FOR PARENT: this credit exhaustion affects the whole grok-4.7 overnight
  coordinator, not just this track. Topping up is a spending decision — needs Micah's word.
