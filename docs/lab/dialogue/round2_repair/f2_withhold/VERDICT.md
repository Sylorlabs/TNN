# F2-WITHHOLD — verdict

Date: 2026-09-23. Repair for round-2 guided-release dialogue withholding
failures (turns 8, 9, 13, 17 of the 2026-09-23 conversation).

## What was built

A five-part aboutness gate between `retrieve()` and `emit_fact()` in
`do_turn` step 5 of a cleanroom fork of `dialogue.zag`. Any check firing
declines with exactly `I don't know.`; state (salience, topic, pending
correction) updates exactly as for an emitted fact, with fid = -1 so no
wrong-fact entities pollute memory. The mechanism is general: it kills the
confabulation *class* (relation word matches, question is about an entity
the KB doesn't cover, or about nothing the fact covers) rather than the
probe phrasings. No probe literal from scaffold or held-out appears in the
source (verified by grep).

## Kill-bar results

| bar | result |
|-----|--------|
| B1 — all four failed round-2 turns decline | **PASS**: turns 8, 9, 13, 17 emit exactly `I don't know.` in the real 18-turn replay (`run_r2.log`) |
| B2 — frozen held-outs decline | **PASS**: 7/7 (`HELDOUT.md`) |
| B3 — no gaming, ≤5% answerable decline | **PASS**: 25/25 answerable items answered, 0 declines (`run_nogaming.log`) |
| B4 — full round-1 battery, no section drops | **PASS**: all 8 sections byte-identical to the unmodified-fork baseline; response DIGEST `35aaae8a…` identical; every T-line identical (`diff` empty) |
| B5 — determinism, zero RNG | **PASS**: two full runs byte-identical (`cmp` clean); no randomness in any new code |
| B6 — cleanroom, canonical tree untouched | **PASS**: `dialogue.zag`/`kb.txt`/`gaz.txt` shas unchanged; all work under `round2_repair/f2_withhold/` |

## What worked

- The preregistered minimum (entity-aboutness check + Jaccard floor) was
  real but insufficient alone; the relation-demand (G2) and demand-focus
  (G3) checks are what kill the actual failure class, where a relation word
  ("wrote", "capital") matches and the shortest-matching fact wins.
- Scaffold-first discipline caught a real regression: the first gate build
  declined WE-07 ("When was Herman Melvile born?"), a round-1 typo probe.
  The fix — G4 applies only when no demand-focus was identified-and-
  covered — is a general principle (a stray token on an identified subject
  is a typo/variant, not an unknown entity), not a per-case patch. Full
  battery returned to byte-identical baseline.
- Declining at the retrieval boundary keeps composition, correction, and
  assertion machinery untouched — no ripple effects anywhere else.

## What didn't / known interactions

1. Round-2 turns belonging to other families changed in the replay and are
   documented for their crews (their repairs run before step 5, so they are
   not blocked by this gate, but the merged behavior differs from the raw
   round-2 transcript):
   - turn 3 (F1): "was he born before the eiffel tower was built?" was
     "Andy Weir was born in 1972." (bare date) → now "I don't know."
   - turn 11 (F4): "are you sure? i read 1818…" was a non-sequitur
     ("The Louvre opened as a museum in 1793.") → now "I don't know."
   - turn 15 (F5): "do you remember the first thing i asked you?" was a
     confabulated fact → now "I don't know." (F5's history-reading
     dispatch will handle this class before step 5.)
2. Known boundary of this gate: a new relation about a KNOWN entity
   ("what is the population of paris?") still emits a related-but-wrong
   fact — a non-sequitur, not an answer-shaped falsehood. That needs a
   relation vocabulary beyond what the KB supports; it is outside this
   repair's class.
3. Composition of a declined turn (e.g. "who was born first, darwin or
   melville?") goes through the composition path (step 3), not the gated
   default retrieval — unchanged by design.

## Commits

- Prereg frozen before implementation: `b1b6092d793c150cb02e3285b1e67d093b90ff57`
- Implementation + docs + logs: `5e6a3dbd964a48aed6b6139852b546fb5ca12153`
