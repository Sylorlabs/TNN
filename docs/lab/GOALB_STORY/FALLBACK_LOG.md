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

## 2026-09-22 ~06:47 UTC: BOTH LLM APIs HARD-DOWN — track goes native
- ExperientialLabs grok-4.7: HTTP 429 insufficient_credits, balance -$0.02 (verified by direct probe). Needs Micah's top-up. NOT transient.
- gpt-5.6-sol via UnoRouter: timing out on direct probe (was working ~06:33-06:43 UTC for B2-sol + red-team; now timing out).
- grok-4.6 via UnoRouter: 3x HTTP 524 on full B2 prompt, 3x 524 on batched (9-item) prompts. Origin not responding.
- Parent directive: max ONE API retry per hour to detect recovery. No retry loops. Proceed NATIVELY.
- B2 impact: single blind LLM judge completed (gpt-5.6-sol, 2 runs, pre-outage). Second judge UNEVALUATED tonight; bar reported honestly as partial. Experimenter native rating added as clearly-labeled SUPPLEMENT (blind, frozen rubric), not bar evidence.
- No new Muse workers spawned for this; analysis done directly.

## 2026-09-22 ~07:20 PDT: B2 second judge COMPLETED (grok-4.7 via ExperientialLabs)
- API verified recovered with substantive probe; wrapper `grokchat.py` path (max_tokens 1500), single call.
- Method: same frozen prompt `evidence/b2_prompt.txt` (md5 7e79199cadb2e08367376750445c7357), same blind TIDs T01-T17. Substitution vs A1 (grok-4.6 via UnoRouter) documented in VERDICT.md §7.1; one-call success, no retries.
- Result: 17/17 scores parsed from clean 17-line response → `evidence/b2_raw_grok-4_7.txt`.
- grok-4.7: all POS=1, DEL 2-3 (odd sets 2, even sets 3), CTRL=5. Two-judge means >=3.5: DEL 4/8, POS 0/8 → preregistered two-judge bar NOT MET. B2 final = FAIL. Positive control 5/5 both judges (apparatus valid); max inter-rater |diff|=2.
