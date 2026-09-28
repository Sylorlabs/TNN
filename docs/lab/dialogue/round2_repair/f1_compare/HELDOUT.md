# F1-COMPARE — held-out release test

Date: 2026-09-23. Prereg: `PREREG_F1.md` (frozen, commit `1d826c7` — held-out
probes §4 written before any implementation).

## What "release" means here

The repair was developed against the scaffold probes (`scaffold_battery.txt`:
round-2 turns 3/4/7 verbatim + 5 dev paraphrases). The mechanism in
`dialogue.zag` contains no scaffold-keyed branches — verified by inspection:
no multi-word literal from any scaffold or held-out probe appears in the
source; only the prereg-allowed grammatical classes (single comparison words,
the anaphora word list `those two / these two / the two / either`, aux verbs)
and the fixed KB-shape marker list. The test below uses ONLY the frozen
held-out phrasings, each in a fresh DIALOGUE block (fresh state), run on the
final binary with no scaffold present.

## Held-out results (binary `dialogue_bin`, sha256 `4cd89f22…`, log `heldout_run1.log`)

| Probe | Input | Expected | Got | Verdict |
|---|---|---|---|---|
| H1 | was jane austen born before herman melville? | yes. | yes. | PASS |
| H2 | who was born earlier, marie curie or andy weir? | marie curie was born first. | marie curie was born first. | PASS |
| H3 | which was built later, the eiffel tower or the montparnasse tower? | the montparnasse tower was built last. | the montparnasse tower was built last. | PASS |
| H4 | was the statue of liberty dedicated before the eiffel tower was built? | yes. | yes. | PASS |
| H5 | who is older, jane austen or charles darwin? | jane austen was born first. | jane austen was born first. | PASS |
| H6t1 | which is taller, the statue of liberty or big ben? | big ben is taller. | big ben is taller. | PASS |
| H6t2 | which of these two was built first? | engine declines (no comparison-shaped answer) | The Eiffel Tower was built in 1889. (retrieval fallback; Big Ben has no year fact, so no comparison is possible) | PASS |
| H7 | was the colosseum completed before the louvre opened? | yes. | yes. | PASS |

**Release score: 7/7** (bar was ≥6/7). Two full runs byte-identical
(sha256 `2809475a…` both runs, `cmp` clean).

## What the held-out set exercised (beyond the scaffold)

- Novel comparison words never used in dev: `earlier` (H2), `later` (H3),
  `older` (H5) — the direction mapping (min vs max) generalized to unseen words.
- Novel value markers never used in dev: `dedicated` (H4, statue of liberty),
  `completed` (H7, colosseum), `opened` (H7, louvre) — the marker list is
  KB-shape-driven, not probe-driven.
- Mixed markers in one question (H4: dedicated vs built).
- Anaphora to a pair across a two-turn block (H6) and honest decline when a
  value is missing (H6t2) rather than a confabulated comparison.

## Scaffold vs released (for the record)

Scaffold battery on the final binary (`scaffold_final.log`): 20/20 real probes
PASS (5 additional lines are intentional `<sentinel>` placeholders for turns
belonging to other families — F2/F3/F4 territory — and are not scored).
Round-2 turns 3/4/7 all produce the prereg-specified outputs, including turn 7
with turn 6 (F3's arithmetic turn) intervening — the compared pair survives
non-comparison turns by design.
