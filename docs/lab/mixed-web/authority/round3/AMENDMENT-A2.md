# AMENDMENT-A2 — Source-authority reliability sweep, round 3 (2026-09-22)

Extends the frozen round-1/round-2 source-authority trials. Round 2
(VERDICT-MW-D) left the licensed claim narrow: PRIMARY_LOOSE is licensed
ONLY for the S1A/R03 dispute shape AND only where the primary source's
reliability is independently established — with the crossover reliability,
the self-estimation stress, and the S8 fiat cost all unpriced. This
amendment authorizes pricing them.

## Approval

Micah's message of 2026-09-22, quoted verbatim (same message recorded in
AMENDMENT-A1):

> "Make sure anything stalled or not launched was tested and investigate why
> did kb4 fail what's going wrong bad learning bad arcitecture? Also try the
> runs we did with 4.6 with 4.7 grok that haven't been done yet and yes try
> mixed web source authority who cares about complexity try it take the free
> lunch and investigate the non free lunch free lunch is free lunch"

The relevant instruction: **"investigate the non free lunch"**. AMENDMENT-A1
§2 already authorized synthetic envelope families measuring "where authority
weighting helps, where it is neutral, and where it hurts"; this amendment
extends that authorization to the reliability sweep that prices the hurt.

## What it authorizes

1. **The reliability sweep** — synthetic dispute-shape envelope families at
   preregistered primary-reliability levels (PREREG-MW-R3 §R1), measuring the
   loose rule's expected value delta vs the conservative round-1 rule at
   each level, and locating the crossover reliability where expected value
   goes negative.
2. **The self-estimation stress** — testing whether the S1A win survives
   when the primary's reliability is estimated from the dispute itself
   rather than independently established (PREREG-MW-R3 §R3).
3. **The S8 fiat-cost row** — quantifying wrong-guess rate and
   false-confidence rate of fiat-breaking genuine ties (PREREG-MW-R3 §R4).
4. **No new arms.** Round 3 reuses the frozen arms B (deliberation verbatim),
   C (conservative PRIMARY, PREREG-MW-C M1), D (PRIMARY_LOOSE, PREREG-MW-D
   D1) on new synthetic envelopes. No rule is retuned; nothing from round 1
   or round 2 is rewritten.

## Scope guardrails (unchanged)

Pure Zag, zero RNG, byte-identical reruns (5 per arm), hash-chained ledgers,
independent oracle recomputation of every verdict/citation/chain/ledger
head, kill bars in PREREG-MW-R3 §R5. Synthetic envelopes carry stipulated
golds and are scored for value-mapping, not as kill bars — a stipulated
gold cannot kill a mechanism. The frozen prereg (PREREG-MW-R3) is committed
before any battery is generated or run.

**FROZEN 2026-09-22.**
