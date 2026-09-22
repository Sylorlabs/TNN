# GROK47 FALLBACK LOG

## 2026-09-21 ~23:25 PDT — grok-4.7 completion truncation (COORDINATOR direct probe)
- **What grok did wrong:** grok-4.7 via ExperientialLabs `chat.py` truncates completions at ~50–90 bytes, mid-word/mid-sentence, on 4 consecutive substantive prompts (23:16–23:25 PDT). Short prompts (PONG, 2-line labeled) return fine. Longer generation is cut: "The 58/58 native pass is suite-over" (46B), "…still fails to" (92B), "Testable weakness hypotheses" (91B, list never came), "attack the" (71B).
- **Control:** identical prompt to gpt-5.6-sol via UnoRouter returned a complete, high-quality ~1100-byte red-team answer.
- **Replacement:** substantive hypothesis/attack generation moves to (b) gpt-5.6-sol via `python3 ~/workspace/skills/unorouter/bin/unorouter.py chat "<prompt>" --model gpt-5.6-sol` (wrap in `timeout 120`; the CLI can hang after printing — capture output, don't wait on exit). grok-4.7 retained ONLY for short structured outputs (single lines, PONG-style, ≤2 labeled lines). Native workers cover the rest per original briefs.
- **Recovery watch:** re-probe grok-4.7 with a substantive prompt every ~60 min; if full completions return, restore it as primary engine and log recovery here.
- **Blast radius:** all 7 sector workers were briefed grok-first; broadcast sent 23:26 PDT switching their substantive generation to sol, grok-4.7 to short outputs only. Teacher-showdown corpus CAPTURE via grok-4.7 is unaffected in principle (capture uses many small completions) but the worker must verify no truncation in captured values — any truncated capture value = void batch, recapture.

## 2026-09-21 ~23:35 PDT — CORRECTION + escalation (senses worker diagnosis, coordinator verified)
- CORRECTION: the ~50-90-byte "truncations" were a TOOLING artifact, not model degradation: stock `chat.py` line 26 hard-codes `"max_tokens": 16`. Worker-built wrapper `~/workspace/grok47/senses/grokchat.py` (default max_tokens 1500, override via argv[3]) fixes it. All workers: use the wrapper for grok-4.7, not stock chat.py.
- ESCALATION: grok-4.7 gateway now returns `HTTP 429 insufficient_credits — org out of platform credits (balance: $-0.02)` on every call (worker re-probe ~23:30 PDT). Full outage. Credit top-up is external/irreversible — needs Micah. Until then: substantive generation on gpt-5.6-sol (short prompts, `timeout 120`, capture stdout) or native.
- Hourly grok-4.7 re-probe moved to coordinator cron (workers exempt).

## 2026-09-21 ~23:46 PDT — parent-verified: gpt-5.6-sol ALSO down (timeouts)
- Direct probe by parent: gpt-5.6-sol via UnoRouter timing out. grok-4.7 still 429 insufficient_credits (balance $-0.02).
- New rule: max ONE API retry per hour per API to detect recovery. No retry-burning.
- All work proceeds NATIVELY (analysis/build/verification by the agents themselves, as the senses track did). No new Muse workers unless truly needed (Micah's tonight rule).
- Governing rule: "do what you can when you can". Manifest sweep, bars, deliverables unchanged.
