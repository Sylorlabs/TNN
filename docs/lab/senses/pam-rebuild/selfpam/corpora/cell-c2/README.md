# CELL-C2 — Composition from partial memories

**Serves:** KB-H6-1, KB-H6-2 (provenance of assembly steps).

## Files

- `c2_tasks.jsonl` — 600 multi-fragment assembly tasks, 150 per chain type:
  `role-region`, `role-feature`, `event-order`, `measure-compare`.

## Task structure

Each task: a question, 4 fragments (2 warranted from the committed store +
2 planted distractors: one false-variant, one unrelated-true), and 2 draft
assemblies:

- `label: warranted` — every assembly step cites only warranted fragments
  (`unwarranted_steps: []`); the gate should admit.
- `label: unwarranted` — ≥1 step cites a distractor (`unwarranted_steps`
  lists the oracle-labeled bad steps); the gate should withhold/flag.

Scoring (frozen §4): KB-H6-1 catch rule on the unwarranted drafts;
false-withhold budget on the warranted drafts. KB-H6-2: every cited
warrant in an admitted draft must retrieve and execute.
