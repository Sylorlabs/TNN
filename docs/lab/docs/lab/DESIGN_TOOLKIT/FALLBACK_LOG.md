# Fallback / API log — design track, 2026-09-21/22

## Grok 4.7 (preferred per Micah) — BLOCKED

2026-09-21 ~23:35 PDT: stock `chat.py` used `max_tokens: 16` (one-line answers).
Built `~/workspace/skills/experientiallabs/bin/g47.py` with proper budget.
First full request failed: HTTP 429 `insufficient_quota`, org balance
**$-0.02**; provider suggested $5 top-up or BYOK.

Status: Grok hammering is blocked. NO top-up without Micah's approval.
Surfaced to parent/Micah.

## Fallback: gpt-5.6-sol via UnoRouter — OPERATIONAL

`~/workspace/skills/unorouter/bin/sol.py`. Used for:
- V2 human-taste theme values (corner radius 16, spacing 4px, bg 15,16,18,
  surface 30,31,35, accent 255,82,112, text 247,247,245, muted 157,160,168,
  title 24 / body 16 / caption 12, borderless cards w/ shadow, comfortable
  density, 20px h / 24px v screen padding, 16px card padding,
  12px related / 24px section rhythm)
- predicted machine-vs-human differences (confirmed in renders)
- red-team critiques (this track)

Reliability notes: short focused prompts work; long prompts intermittently
return `choices: null` / zero tokens / HTTP 524. `temperature` param removed
after correlating with failures (one long failure persisted without it —
length, not temperature, looks causal).

## Purity statement

Sol supplied NUMBERS (theme tokens). Every pixel, glyph, component, and
layout decision in the renders was produced by Zag code. No LLM-generated
imagery, no copied assets. The font is a hand-entered 5x7 bitmap table.
