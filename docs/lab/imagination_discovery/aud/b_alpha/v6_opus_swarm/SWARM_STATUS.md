# SWARM_STATUS.md — opus-5.5 investigation swarm, 2026-09-23

## What was dispatched

Three parallel claude-opus-5.5 calls via the ExperientialLabs gateway
(`custom.experientiallabs`), each with a different failure angle and Micah's
verbatim quotes + the actual render source code pasted in:

1. `prompt_bed.txt` → diagnose the bed's "sloppy DJ mix" + write bed-analysis Python
2. `prompt_events.txt` → diagnose the events' "randomly stops" + write event-analysis Python
3. `prompt_master.txt` → diagnose the mastering chain + bed/events interaction + write audit Python

Each was to return a mechanical diagnosis plus runnable code; the coordinator
would execute the code against the real WAVs and verify.

## What happened — swarm produced NO model output (hard stop)

- Calls 1–3 (max_tokens=8000): all returned HTTP 200 with
  `finish_reason=length` and **null content** — opus-5.5 burned the entire
  8000-token budget on hidden reasoning and emitted nothing. The known
  "use 2000+" caveat was insufficient for these long analytical prompts.
- Call 4 (retry of #2 at max_tokens=16000): **HTTP 429 `insufficient_credits`** —
  `Your organization is out of platform credits (balance: $-0.02)`.
  The three empty 8000-token calls consumed the last of the balance.

So: no verbatim model diagnosis exists, and no model-written code exists. The
gateway account needs a top-up (Micah's call — no spending without him) AND
future opus-5.5 analytical prompts need max_tokens ≥16000 (8000 is not enough
when the prompt itself is long; the model reasons first and answers with
whatever budget remains).

## What was done instead

The coordinator performed the investigation independently and verified every
claim by measurement against the committed WAVs (`measure_v6.py`,
`DIAGNOSIS.md`). This is analysis, not model output — labeled as such. The
three prompts are kept in this directory for re-dispatch after a top-up.

## Lessons

- opus-5.5 via this gateway is a reasoning-heavy model: token budget must
  cover hidden reasoning PLUS the answer. For code-writing prompts with large
  pasted context, budget 16000+.
- Check the credits balance BEFORE a multi-call swarm, not after. Three
  burned empty calls zeroed the account.
- A blocked swarm must still deliver: the diagnosis in DIAGNOSIS.md stands on
  measured evidence from the actual artifacts, independent of any model.
