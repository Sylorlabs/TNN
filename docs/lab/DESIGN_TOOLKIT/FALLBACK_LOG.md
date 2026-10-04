# Fallback / API log — design track, 2026-09-21/22

## Grok 4.7 (preferred per Micah) — BLOCKED

2026-09-21 ~23:35 PDT: stock `chat.py` used `max_tokens: 16` (one-line answers).
Built `~/workspace/skills/experientiallabs/bin/g47.py` with proper budget.
First full request failed: HTTP 429 `insufficient_quota`, org balance
**$-0.02**; provider suggested $5 top-up or BYOK.

Status: Grok hammering is blocked. NO top-up without Micah's approval.
Surfaced to parent/Micah.

## gpt-5.6-sol via UnoRouter — DEGRADED, then DOWN

Operational 2026-09-21/22 for short prompts (V2 theme values, red-team).
Long prompts intermittently returned `choices: null` / zero tokens / HTTP 524.
`temperature` param removed after correlating with failures (length, not
temperature, looked causal).

**2026-09-22 ~00:47 PDT update: sol is now timing out on direct probe too.**
Both APIs hard-down. Standing rule from parent: max ONE retry per hour to
detect recovery; do not burn the night retrying. All design-track work
proceeds natively — the toolkit, scorer, renders, and verification are
100% Zag-native already; Sol only ever supplied numbers (theme tokens) and
prose critiques, never pixels or mechanisms.

## Purity statement (unchanged)

Every pixel, glyph, component, and layout decision in the renders was
produced by Zag code. No LLM-generated imagery, no copied assets. The font
is a hand-entered 5x7 bitmap table.
