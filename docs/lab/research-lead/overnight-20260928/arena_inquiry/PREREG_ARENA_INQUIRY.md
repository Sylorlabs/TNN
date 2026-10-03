# Prereg: Arena Active Inquiry (C8)

Date: 2026-09-30 UTC
Worker: Arena Inquiry Worker
Parent: Arena Conflict (ARENA-CONFLICT, 0.676, 9211de19e)

## Diagnosis

### C8 active inquiry (0.000): Two missing pieces

The arena tests C8 with 4 items. Each item runs a 3-turn sequence:
1. Test turn: `fact|<entity>|<attr>` (cap=8). The fact was never
   exposed during learning (world_gen comment: "C8 oracle facts
   (never exposed)").
2. `observe_result` turn: `{"vals":[{"e":"...","a":"...","v":"..."}]}`
   providing the oracle fact.
3. Re-ask: same `fact|<entity>|<attr>` test turn.

The scorer (arena.zag) awards 1000 iff BOTH hold:
- The LAST test-turn reply equals the answer, AND
- The FIRST test-turn reply line contains `"observe":[`
  (i.e., the contestant emitted an observation request on the
  first ask, signaling active inquiry).

The contestant v4 fails both:
- Test handler: on unknown `fact|` lookup, answers "UNKNOWN" with
  no observe request. So `first_obs=0` for all C8 items.
- `observe_result` handler: just calls `tick(W)`. The oracle fact
  is received but never learned. So the re-ask also answers
  "UNKNOWN".

This is a missing capability (active inquiry: recognizing a
knowledge gap, requesting the missing fact, learning from the
result), not a bug.

## Planned changes

Built on devint1_contestant_v4.zag as v5.

### Change 1: Emit observe request on unknown fact (test handler)

In the test handler, for `fact|`/`fact2|` questions: when
`fact_get` fails (fact unknown), add an observe request to the
reply JSON:
`,"observe":[{"e":"<entity>","a":"<attr>"}]`

This is general active-inquiry behavior: whenever the learner
cannot answer a fact query, it asks to observe the missing fact.
It is not gated on cap==8; for other caps the facts are known so
the branch never triggers, and where it could trigger (C7
unknown entities, expected answer "UNKNOWN") the reply field
still says "UNKNOWN" so scoring is unaffected.

No hardcoded entities, attrs, or values. The request echoes the
question's own entity/attr.

### Change 2: Learn from observe_result (expo-equivalent handler)

In the `observe_result` handler: parse `e`, `a`, `v` from the
`vals` array (via jval, same pattern as expo parsing) and call
`learn_fact(W,e,a,v)` (the standard DEVINT1 learning path:
lexicon feed, concept touches, rule touch, fact store). If the
fields are absent, fall back to `tick(W)`.

State persistence carries the learned fact to the re-ask turn
(state.bin is saved/loaded per turn, same as expo learning).

## Kill bars

K1: After changes, C8 must score above 0.000 (was 0/4).
     Target: 1.000 (4/4). If C8 remains at 0.000, FAIL.

K2: Total must exceed 0.676 (was 46/68).
     Expected: 46 + 4 (C8) = 50/68 = 0.735.
     If total does not exceed 0.676, FAIL.

K3: No regression. C1, C2, C3, C4, C5, C6, C7, C11, C13, C14 must
     remain at 1.000. If any drop, the changes broke existing
     functionality.

K4: Pure Zag. Zero Python. Zero em dashes.
     If any Python is used, the wave is void.

K5: Arena world and scoring unmodified. Sealed seed not viewed.
     If world_gen.zag or arena.zag are modified, or the seed is
     viewed, the run is invalid.

K6: Determinism. 3/3 full arena runs must produce identical scores
     and byte-identical cognitive outputs (excluding rss_kb/ms).
     If not deterministic, FAIL.

K7: Generality. The inquiry handler must not contain hardcoded
     entity names, attribute names, or values from the C8 test
     items. Verification: grep the committed source for the
     specific test entity/attr/value strings; the observe logic
     must echo question fields only.

## What is NOT being done

- C9 causal, C10 procedure, C12 transfer, C15 goal, C16 language:
  out of scope. These require new mechanisms.

## Honest scope

This adds genuine active inquiry in the arena's tested sense: the
learner detects a knowledge gap at query time, requests the
missing fact, learns it from the observation result, and answers
correctly on re-ask. It is bounded: the inquiry is a single
observe request for the queried fact; it does not plan multi-step
information gathering, prioritize among gaps, or decide when not
to ask. Still 0 on causal, procedure, transfer, goal, language.

## Success criteria

BUILD-PASS if K1 through K7 all pass.
BUILD-FAIL if any kill bar fails.
