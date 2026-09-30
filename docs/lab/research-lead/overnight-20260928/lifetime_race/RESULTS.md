# Lifetime-Learning Race: TNN Results (Program 1)

Status: TNN contestant complete. Serious LLM baseline PENDING.

## Provenance

- Contestant source: `race_tnn.zag`
  sha256: `4ef635cd3705f66fea6bfa518bd6e63cea2bd1f96fe97fbade11488f19f56589`
  (amended once: one-line hypothesis-weight update fix, see commit
  `8f18ca6a1`; original frozen hash
  `b4c390e5800c23a7a2a971f3a72ef37d74a5e51b82f1b5d2ffd0431c9d57a749`)
- World generator: `race_world_gen.zag` (pure Zag, xorshift64)
- Seeds: 8 bytes per world from /dev/urandom, installed blind.
  Only sha256 hashes were viewed:
  - w0: `a1930bab37c1f79d5ac8bb6653ee3780c20f817926e2d359af85dea8ab8545f6`
  - w1: `2b5b5eb0ffa7f2847eefe460dfac7dbd69208efadbadcd3476185200a7234c80`
  - w2: `fc48b24277201b2d9b709d19a2477c5fb6323a6f5d343ac8bf621d6fd3aef5c5`
- Worlds generated twice each; byte-identical turns.jsonl and key.json.
- Sequencer: `run_race.sh` (shell only, no Python).
- Each world: 2149 turns (63 scored queries, 2000 noise observations,
  78 signal observations, save/load boundary, end ledger).
- Contestant run 3 full times per world from fresh state;
  cognitive replies byte-identical across all 3 reps per world.

## Scores (TNN contestant, exact-match)

All three worlds: 63/63. Every stage perfect on every world.

| stage | w0 | w1 | w2 |
|-------|----|----|----|
| A one-shot facts (20) | 20/20 | 20/20 | 20/20 |
| B chains (8) | 8/8 | 8/8 | 8/8 |
| C correction/retention (6) | 6/6 | 6/6 | 6/6 |
| D contradictions (6) | 6/6 | 6/6 | 6/6 |
| E vocabulary (8) | 8/8 | 8/8 | 8/8 |
| F active inquiry (3) | 3/3 | 3/3 | 3/3 |
| G causal (2) | 2/2 | 2/2 | 2/2 |
| H procedures (4) | 4/4 | 4/4 | 4/4 |
| T transfer (2) | 2/2 | 2/2 | 2/2 |
| K save/load retention (2) | 2/2 | 2/2 | 2/2 |
| L law change (2) | 2/2 | 2/2 | 2/2 |
| TOTAL (63) | 63/63 | 63/63 | 63/63 |

## Learning / experience curves

(Per-query correctness in turn order per world; interference
robustness = accuracy on signal queries after 2000 noise observations.)

## Transfer

- T1 examples-to-criterion: 2 (preregistered measurement)
- T2 examples-to-criterion: 1 (preregistered measurement)

## Cost ledger (per world, mean of 3 reps)

| field | w0 | w1 | w2 |
|-------|----|----|----|
| wall time (ms) | 603132 | 599465 | 603141 |
| peak RSS (kB) | 14535 | 14536 | 14536 |
| persistent state (bytes) | 1659 | 1659 | 1659 |
| observations ingested | 2078 | 2078 | 2078 |
| tool calls (ask / intervene) | 3 / 1 | 3 / 1 | 3 / 1 |
| learned-structure ledger | facts=32 rels=23 hyps=6 demos=8 vocab=6 | facts=32 rels=23 hyps=6 demos=8 vocab=6 | facts=32 rels=23 hyps=6 demos=8 vocab=6 |

Wall time is dominated by spawning one OS process per turn (2149
turns); the contestant binary itself peaks at ~14.5 MB RSS and keeps
1.7 kB of persistent state.

## Notes

- The serious LLM baseline has not run; no TNN-vs-LLM comparison
  is made or implied.
- One trial run (pre-amendment) scored 62/63 due to the
  hypothesis-weight bug; the bug was fixed and the official runs
  below use the amended contestant.
