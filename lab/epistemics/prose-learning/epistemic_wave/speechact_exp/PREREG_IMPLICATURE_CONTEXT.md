# PREREG: Implicature with speaker / situation / goal / indirect-request context (FROZEN 2026-09-22)

## Background
Implicature handling (matches_implicature in delib_sa.zag) is a set of
hardcoded test strings ("cold in here", "trash is getting full") with no
speaker, situation, goal, or indirect-request context. The literal reading
and the intended reading diverge in indirect requests; the current code
cannot tell them apart except by string match.

## Hypothesis under test
H-IM1: A context model (speaker, situation, goal) resolves indirect
requests through deliberation — NOT hardcoded utterance patterns — at or
above the bar on a fresh battery. H-IM1 is killed if the battery misses,
or if any resolution depends on an utterance-string match (K-IM1).

## Mechanism (delib_impl2.zag, pure Zag, zero RNG)
1. INPUT items `ID|speaker|situation|goal|utterance` (new battery
   impl_ctx.txt, authored for this prereg; 12 items, see below).
2. Context model, fixed machinery (no per-item special-casing):
   - situation carries a small set of (object, fixable-state) slots, e.g.
     situation "dinner-table, salt out of reach" -> slots: (salt, out-of-reach).
   - The utterance yields a state descriptor via a GENERAL state-word
     lexicon (fixed word types, not test strings: cold, empty, full,
     blocking, crying, dead, sticky, chirping, long, wobbling, ...).
   - goal yields an end-state class: `change-state` (speaker wants the
     situation fixed) vs `inform` (speaker only reports).
3. Deliberation per item:
   - LITERAL: the utterance as a bare assertion about the world.
   - INTENT: if the state word matches a fixable-state slot of an object
     in the situation AND goal == change-state AND the speaker cannot act
     directly (speaker != the party positioned to act) -> INDIRECT-REQUEST
     naming the target action; the literal is NOT installed as the
     speaker's asserted fact.
   - Otherwise -> literal reading stands.
4. Output: `ID|LITERAL|REQUEST:<target-object>` (one target object name).

## Frozen battery impl_ctx.txt (12 items; literal != intended on all 12)
1. speaker=CAM, situation=dinner table salt out of reach, goal=get-salt,
   utt="This soup could use more salt." -> REQUEST:salt
2. speaker=CAM, situation=dinner table salt in hand, goal=inform,
   utt="This soup could use more salt." -> LITERAL
   (pair with 1: same utterance, situation flips the reading)
3. speaker=LEE, situation=car interior cold, goal=warm-up,
   utt="It's freezing in here." -> REQUEST:heater
4. speaker=LEE, situation=arctic research station, goal=inform,
   utt="It's freezing in here." -> LITERAL
   (pair with 3)
5. speaker=PAT, situation=kitchen trash overflowing, goal=take-out,
   utt="The trash is getting full." -> REQUEST:trash
6. speaker=PAT, situation=garage cleanup day, goal=inform,
   utt="The trash is getting full." -> LITERAL (pair with 5)
7. speaker=SAM, situation=office meeting in five, goal=leave-now,
   utt="The meeting starts in five minutes." -> REQUEST:wrap-up
8. speaker=SAM, situation=hallway chat, goal=inform,
   utt="The meeting starts in five minutes." -> LITERAL (pair with 7)
9. speaker=JO, situation=porch package all afternoon, goal=bring-in,
   utt="That package has been sitting on the porch all afternoon." -> REQUEST:package
10. speaker=JO, situation=porch, goal=inform,
    utt="That package has been sitting on the porch all afternoon." -> LITERAL (pair with 9)
11. speaker=RUE, situation=baby crying since commercial break, goal=soothe,
    utt="The baby's been crying since the commercial break." -> REQUEST:baby
12. speaker=RUE, situation=living room, goal=inform,
    utt="The baby's been crying since the commercial break." -> LITERAL (pair with 11)

## Bars (frozen; ALL must pass)
| Bar | Statement | Kill criterion |
|---|---|---|
| I1 resolution | >= 10/12 on impl_ctx.txt | <10 KILLS H-IM1 |
| I2 pair-discrimination | all 6 same-utterance pairs resolve DIFFERENTLY (request vs literal) via the context model | any pair same = mechanism is pattern-matching, FAIL |
| K-IM1 no-hardcode | no battery utterance string (or >12-char substring of one) appears in delib_impl2.zag; resolution must cite the matched situation slot + goal class in the output line | any hit = automatic FAIL |
| K-IM2 determinism | 3 reruns byte-identical, sha256 logged | any divergence = FAIL |

## Build notes
- Decision path pure Zag; verification plumbing may be Python.
- The state-word lexicon is fixed word TYPES (general), never full
  utterance strings. The anti-hardcode bar enforces this.
- Commit order: this prereg ALONE first, then code+results in a second commit.
