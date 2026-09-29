# Next Frontier Design: Procedure Invention (Phase 8)

**Date:** 2026-09-29 04:15 PDT
**Status:** DESIGN (not implemented)
**Priority:** Highest-information next experiment

## Why Procedure Invention?

SEM-L3 (clustering) is exhausted as an L3 candidate. It is L2+.

Procedure invention requires genuine algorithmic creativity:
- The learner must compose primitives into a novel algorithm.
- The algorithm must not exist in source.
- This is undeniable L3 if achieved.

## Minimal Viable Test: String Reversal

**Domain:** String transformation.

**Teaching:**
- ("abc" → "cba")
- ("def" → "fed")
- ("xy" → "yx")
- ("hello" → "olleh")

**Target procedure:** REVERSE (not in source).

**Learner primitives (allowed):**
- `len(s)`: string length
- `at(s, i)`: character at index i
- `concat(a, b)`: concatenate strings
- `loop`: iteration construct

**Not allowed:**
- A `reverse` primitive.
- A menu containing "reverse" as an option.
- Hardcoded transformation rules.

**Success criteria (L3):**
1. Procedure did not exist before learning (not in source).
2. Construction trace exists (shows how primitives were composed).
3. Solves training cases (4/4).
4. Solves hidden instances (e.g., "zag" → "gaz", "12345" → "54321").
5. Reused later (applied to new strings without reteaching).
6. Ablation removes advantage (without the invented procedure, fails).
7. Surface changes don't destroy it (works on different alphabets).
8. Red team cannot explain as memorization (hidden strings not in training).

## Why This Is Hard

The learner must:
1. Notice the pattern (output is input backwards).
2. Invent the algorithm (iterate from end to start, accumulate).
3. Represent the algorithm as reusable procedure.
4. Apply it to novel inputs.

This requires:
- Pattern recognition (L2)
- Algorithm synthesis (L3)
- Procedure representation (L3)
- Generalization (L3)

## Simpler Alternative (if reversal is too hard)

**Copy procedure:**
- Teach: ("abc" → "abc"), ("xy" → "xy").
- Target: IDENTITY (output = input).
- This is trivial and does NOT test invention. Do NOT use.

**Swap procedure:**
- Teach: ("ab" → "ba"), ("cd" → "dc").
- Target: SWAP first two chars.
- Simpler than reverse, but still requires invention.
- Might be a stepping stone.

## Architecture Sketch

**Components needed:**
1. **Primitive library:** Small set of string ops (len, at, concat).
2. **Composer:** Searches combinations of primitives.
3. **Verifier:** Tests candidate procedures on training data.
4. **Selector:** Picks procedure that generalizes (not just memorizes).

**This is a big build.** Estimated 4-6 hours for minimal version.

## Fallback: Causal Structure (Phase 9)

If procedure invention is too hard, try causal learning:

**Domain:** Synthetic machine with hidden "safety valve" rule.
- States: (temp: cold/warm/hot, pressure: low/high)
- Actions: heat, cool, pressurize, depressurize
- Hidden rule: pressurize FAILS if temp==hot (safety valve).
- Learner observes (state, action, next_state), invents the rule.
- Test: Predict (hot, low, pressurize) → (hot, low), not (hot, high).

This tests model invention (L3) without requiring full procedure synthesis.

## Recommendation

Attempt **String Reversal** as the primary frontier. If blocked after 2 hours,
pivot to **Causal Safety Valve** as fallback. Both target genuine L3.
