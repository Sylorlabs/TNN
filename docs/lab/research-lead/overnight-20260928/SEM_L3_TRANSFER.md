# SEM-L3 Minimal v3: Transfer Test (L3 Criterion #7)

> **SUPERSEDED (2026-09-29, governance audit).** The "Updated L3 Score: 7/9" in this
> document is superseded. The parent L3 claim was withdrawn after the kill battery
> (see KILL_BATTERY_VERDICT.md). The transfer observation (novel surface joins
> concept, probe correct) reproduces and remains valid as L2+ evidence.

**Date:** 2026-09-29 ~03:45 PDT

## Test

Novel surface `norpal2` (never seen in teaching). Taught with 2 examples:
- (norpal2, sqz_emit, glimx)
- (norpal2, sqz_glow, glowx)

These align with E1 concept (norpal/squeezer) which uses sqz_emit->glimx, sqz_glow->glowx.

## Result

**Unifications:**
- norpal ~ norpal2 (Jaccard 2/3 = 0.67)
- squeezer ~ norpal2 (Jaccard 2/3 = 0.67)
- Concept now: {norpal, squeezer, norpal2}

**Probes:**
- (norpal2, sqz_heat, ?) → velx CORRECT (untaught; via concept)
- (norpal2, sqz_emit, ?) → glimx CORRECT (taught; direct)

**Score:** 2/2

## L3 Criterion #7: Transfer/Reuse - SATISFIED

The learner reused the invented E1 concept for a novel surface with only 2 examples.
The concept was not pre-enumerated; it was invented from prior experience and
extended to cover a new case.

## Updated L3 Score: 7/9

1. ✅ Not pre-enumerated
2. ✅ Created after experience
3. ✅ Visible state
4. ✅ Causal creation trace
5. ✅ Causal ablation
6. ✅ Unseen-case benefit
7. ✅ Transfer/reuse
8. ⏳ Memorization attacks (RT-8 passed; full battery pending)
9. ⏳ Independent red-team survival (pending)
