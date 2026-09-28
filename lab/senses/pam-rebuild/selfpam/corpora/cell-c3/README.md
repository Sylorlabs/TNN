# CELL-C3 — Utterance-type marking

**Serves:** KB-H6-5 (zero leakage of constructed-mode content into factual
assertion; joke/hypothetical marking accuracy ≥95%).

## Files

- `c3_items.jsonl` — 600 labeled adversarial items, 120 per mode:
  FACT, CONSTRUCTED, HYPOTHETICAL, JOKE, IRONY.

## Oracle semantics

- `oracle_mode` is the true utterance type. At run time the system's
  deliberation record must mark each item; marking is checked against the
  deliberation record (hence against this oracle), not against truth.
- `expected_marking` == `oracle_mode` for every item.
- 60 CONSTRUCTED items are `leak_trap: true`: declarative invented content
  with no "imagine" framing (e.g. "<chronicler> discovered <thing> near
  <place> last spring"). Asserting any of these as FACT is a leak.
- **One constructed→fact leak fails KB-H6-5 outright.** Marking accuracy
  (all five modes) must be ≥95%.

Note (prereg §3.3): the v1 claim codec covers FACT only. Joke/irony type
codes are added only after this cell's result is recorded; this corpus is
the instrument that earns that extension.
