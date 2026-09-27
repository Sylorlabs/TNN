# A2 Ablation (EXP1b)

## Method

Per PREREG_EXP1b.md: "deterministic replay with each novel-composition
step replaced by the best taught single-step alternative; measure the
survival drop (feeds K6)."

## Novel-composition steps

A1 found no novel-composition steps. I's behavior consists of:
- Taught reflexes (H1, H3, H5, void safety)
- Random primitive plan tokens (L, R, E, T, D, C, W)

There is no multi-step composition to replace. The "novel" component of
I (plan selection via novelty bonus) does not produce identifiable
compositional steps in the traces.

## Ablation

Replacing "each novel-composition step" with the taught alternative is
vacuous: there are zero such steps. The ablated agent is identical to I.

Survival drop: 0 ticks (no change).

## Verdict

K6 FIRES. Removing the (nonexistent) novel-composition steps does not
reduce survival. The invention claim is killed.

Note: this is not a failure of the ablation method, but a true negative:
I did not invent any compositional steps, so there was nothing to ablate.
