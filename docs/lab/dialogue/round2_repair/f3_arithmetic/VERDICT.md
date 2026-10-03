# VERDICT.md — F3-ARITHMETIC guided-release repair

Plain-language verdict on the round-2 turn-6 failure ("how much taller is
it?" → "The Eiffel Tower is in Paris." instead of 120).

## What was done

The machine had no subtraction anywhere and no way to carry the compared
pair across turns, plus "taller" never stemmed to "tall". The repair adds a
small general difference engine: it recognizes how-much-difference questions
("how much taller…", "how many years between…", "what is the difference in
height between…"), finds the two things being compared (named directly, or
the pair from the previous comparison turn), looks up each one's number from
the knowledge base **at answer time**, subtracts, and says the number. It
also teaches the stemmer that "taller" is just the comparative of "tall"
(and older/old, longer/long, etc.) — comparatives are grammar, not new
words, so this doesn't cross the line the morphology crew drew around
word-pairs like tall/height.

## Verdict per kill bar

| bar | result |
|-----|--------|
| 1. Acquisition — turn 6 → `120` | **PASS** (round-2 conversation re-run: turn 6 now answers `120`) |
| 2. Release — held-out probes H2–H8 correct | **PASS** (8/8; new phrasings, new entity pairs, never seen in development) |
| 3. No gaming — computes, doesn't memorize | **PASS** (no answer constants in the code; values looked up live from the KB; only entity ids carried across turns) |
| 4. No regressions — 5 good round-2 turns keep working | **PASS** (turns 1, 2, 5, 10, 12 byte-identical) |
| 4. No regressions — full round-1 battery, no section drops | **PASS** (all 8 sections identical: 45/45, 45/45, 60/60, 30/30, 30/30, 60/60, 72/72, 28/28; full output identical except the digest line) |
| 5. Determinism — byte-identical reruns, zero RNG | **PASS** (`cmp` clean on held-out and battery reruns) |
| 6. Cleanroom — canonical `dialogue/` tree untouched | **PASS** (frozen `dialogue.zag` sha256 unchanged: `acda81ac…8231f`) |

**Overall: PASS on all 6 bars.**

## What worked

- First-try scaffold: all 5 scaffold probes passed on the initial build, and
  all 8 frozen held-out probes passed on the first released run — the general
  machinery (not per-case hacks) carried over.
- The follow-up path ("it" → the just-compared pair) worked for both the
  original turn-6 wording and the paraphrase "by how much is it taller?".
- Per-entity event selection ("the louvre opening … the eiffel tower being
  built") correctly picked different year-markers for the two entities.

## What didn't / limits

- The difference engine only covers height and years — the only dimensions
  the KB has paired values for. "How much older" maps to birth-year
  difference; anything without two KB values falls through to the old
  pipeline (that's F2's withholding problem, not this family's).
- The carried pair expires after one turn by design; "how much taller is it?"
  asked three turns later won't resolve. That's deliberate — a stale referent
  is worse than a miss.
- Output is a bare number (`120`, not "120 meters"). The bar demanded `120`;
  units would be a presentation-layer decision.

## Follow-ups for the integration pass

- None blocking. The fork is merge-ready: the diff is additive (new branch +
  new pv slots + 7 stemmer mappings) with zero measured drift on the frozen
  battery and conversation.
