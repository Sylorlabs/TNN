# V91 exact R23 recovery — 2026-09-17

## Scope

This note records a new historical-input recovery for V91. It does not alter or
supersede the frozen 2026-09-15 V91 evidence directories. It grants no learning,
authority, promotion, exposure, or canonical-R27 mutation.

## Recovered release

The original release archive `tnn-pre-v1-r27-general-learning.zip` was recovered
from the user's existing ChatGPT Library artifact and inspected as an inert
archive. The release archive had already been identified by the R27 recovery
record as the original recovered release.

The archive contains all three exact inputs that the 2026-09-15 V91 record
listed as missing:

| role | archive member | bytes | SHA-256 | status |
| --- | --- | ---: | --- | --- |
| original R23 source | `src/r23_experiments.py` | 63,069 | `517eb325096d5ae71ebb3bf659da77eac4266129136b888b469a99e366d4b642` | exact match recovered |
| standalone R23 state | `lineage/r23-accepted-state.pkl` | 7,028,883 | `fc24881f104052c09a4cb6e596b01ae5c107d9ae0356c8799ec97eff3edf440b` | exact match recovered |
| original R23 summary | `lineage/r23_summary.json` | 29,242 | `74cdb944e1037e92100d0dee2eca6ffaebcabe53346bb114c4bd09b035e3a495` | exact match recovered |

The exact source text is quarantined locally at
`recovery_exact_20260917/r23_experiments.py`. It is read-only and is historical
source evidence, not a runtime dependency for native qualification.

## Generator semantics resolved from the exact source

The recovered source resolves the previously unknown historical contract:

- condition width is 42, with one-hot groups of 8 names, 8 objects, 8
  locations, 6 motives, 8 actions, and 4 kinds;
- `_build_semantic_dataset(seed=23101, n_extra=2200)` produces 2,048 balanced
  combinatorial rows followed by 2,200 random rows using `random.Random(seed)`;
- each balanced row consumes random motive, action, and one of four surface
  forms; each extra row consumes name, object, location, motive, action, kind,
  and form choices;
- the holdout decision is `stable_u64('r23hold', a, o, l, kind) % 7 == 0`;
- train and test are independently shuffled by a fresh `random.Random(23101)`
  and then capped to 1,800 train rows and 72 test rows;
- byte BPE is trained only on the 1,800 training texts, starting with 256 byte
  tokens and greedily adding the most-common adjacent pair until vocabulary
  340 or pair count below four;
- special tokens are `start=bpe.vocab_size` and `end=start+1`; training sequence
  length is 54, while generation samples at most 48 tokens;
- `MotifGenerator` is a 48-dimensional token embedding, 42→128 condition
  hidden projection, 42→48 condition embedding projection, one-layer GRU with
  input 96 and hidden 128, and a 342-way output projection;
- generation initializes hidden state with `tanh(ch(c))` and concatenates token
  embedding with `tanh(ce(c))` at every step;
- sampling uses `torch.Generator().manual_seed(seed)`, temperature 0.72,
  top-k 7, softmax over the top-k logits, and `torch.multinomial`;
- generation tracks model log probability only while each sample is alive and
  stops appending after the end token;
- semantic reranking uses the separately learned 768×42 interpreter, negative
  mean squared error, model log-probability divided by decoded text length,
  and a `-.001 * abs(len(text)-48)` length penalty;
- the historical R23 evaluation calls `n=1, semantic_weight=0` at seed
  `23101+i` for the naive lane, and `n=128, semantic_weight=20` at seed
  `33101+i` for the round-trip lane.

## Remaining V91 work

The historical algorithm is no longer blocked by absent source semantics.
Native generator parity still requires an independently implemented pure-Zag
equivalent of the admitted runtime behavior, including the exact CPython seeded
row/shuffle order and the PyTorch float32 GRU, top-k, softmax, and seeded
multinomial behavior. Until those native outputs reproduce the bound 16-string
oracle, the V91 generation gate remains closed.

