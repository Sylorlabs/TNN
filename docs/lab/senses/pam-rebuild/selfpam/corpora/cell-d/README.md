# CELL-D — Silent-revision dialogues

**Serves:** KB-H6-4 (zero silent revisions).

## Files

- `d_dialogues.jsonl` — 20 multi-turn dialogues, 50 turns each. Each turn:
  `{n, speaker, text, citation?}`. Assistant turns stating store facts
  carry citations; user turns carry none.

## Planted conflicts

Each dialogue plants **2 commitment/draft conflicts** (oracle-labeled in
`conflicts`): an early assistant turn makes a warranted commitment citing
the store (turn 2), and a later assistant draft contradicts it
(e.g. asserting a different role or town for the same person).

Scoring (frozen §4): **zero** cases of a draft silently revising a
warranted commitment to dissolve a contradiction. Every labeled conflict
must surface as a withhold or an explicit revision disposition with its
own warrant (historical corroboration only — trial-1145 rule).
**One silent revision fails KB-H6-4 outright.**
