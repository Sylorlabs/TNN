# V91 semantic-generator evidence recovery report

Date: 2026-09-14

## Scope

This report records the V91 evidence-recovery findings for the retained R23 semantic generator. Historical Python, pickle, Torch, NumPy, and foreign evaluator code was not executed. Canonical R27 was not mutated.

## Exact admitted identities

- R23 accepted state: 7,028,883 bytes, SHA-256 `fc24881f104052c09a4cb6e596b01ae5c107d9ae0356c8799ec97eff3edf440b`.
- Exact R23 source: 63,069 bytes, SHA-256 `517eb325096d5ae71ebb3bf659da77eac4266129136b888b469a99e366d4b642`.
- Original R23 release ZIP SHA-256: `3eda7e90fde2d4e5be1c7f44362c9018af85a945624f0e56e4c0cefe0000afad`.
- Original R23 release TAR.GZ SHA-256: `c3162ec8620a9b6c5464fcd1c2c4962a11ea46d79d9df521d7c2d21d33bb186c`.
- Frozen R25 lineage independently carries the same R23 accepted-state identity and includes `lineage/r23_summary.json` in its verified manifest.

## Historical semantic-generation contract recovered

The exact R23 source defines `semantic_roundtrip_generation_experiment(seed=23101)` and establishes:

- held-out membership: `stable_u64('r23hold', a, o, l, kind) % 7 == 0`;
- train and test lists are shuffled by the experiment's `random.Random(seed)` instance after `_build_semantic_dataset(seed)` returns;
- deterministic caps: train = first 1,800 shuffled rows; test = first 72 shuffled rows;
- for each test row `i`, the naive candidate is generated with `generate(c, seed+i, n=1, semantic_weight=0.0)`;
- only the first 16 test examples are stored in the accepted evidence under `semantic_generation.examples`;
- because `n=1`, each stored `naive` string is a direct seeded sampler outcome, not a best-of-N semantic reranking result.

The accepted evidence is then inserted into R23 state as `evidence['semantic_generation']` and serialized separately to `results/r23_summary.json`.

## Current V91 16-string oracle

The current V91 KAT binds these expected `naive` strings in order:

1. `lena moved the key so it would not risk falling.`
2. `ana acted because the folder might face being lost.`
3. `jon thinks the folder is in the desk.`
4. `lena left it in the desk.`
5. `ravi promised to send the folder to the shelf.`
6. `ana moved the glass so it would not risk falling.`
7. `mira believes the folder is located in the room.`
8. `ravi acted because the notebook might face breaking.`
9. `ana thinks the book is in the shelf.`
10. `mira put the notebook to the box.`
11. `omar promised to send the glass to the box.`
12. `sam carried the key to the shelf.`
13. `nora thinks the glass is in the box.`
14. `sam thinks the folder is in the room.`
15. `jon believes the glass is located in the bag.`
16. `nora believes the book is located in the desk.`

These remain oracle constants until independently re-extracted from exact admitted historical bytes by native Zag.

## Exact retained generator storage envelope

Existing native custody work establishes:

- `semantic_generator` key text at byte 5,600,377 in the admitted R23 state;
- semantic-generator value span `[5,600,396, 6,357,638)`, 757,242 bytes;
- semantic value SHA-256 `74fe104f87511aac5d847625f5de003921e32ed27213986f2134df324402800f`;
- `MotifGenerator` marker at byte 5,603,408;
- 11 retained semantic model tensor storages totaling 619,544 raw float32 bytes;
- interpreter payload begins at byte 6,228,538, length 129,024 bytes;
- interpreter raw SHA-256 `3f5c806cfa243f9fc5de398101d93a9fc59b8ea1d4cb55cbe08165d940e3e5c3`;
- interpreter shape is 768 x 42 and the retained condition dimension is 42.

## Current summary identity carried by V91

The current V91 lane records `results/r23_summary.json` as 29,242 bytes with SHA-256 `74cdb944e1037e92100d0dee2eca6ffaebcabe53346bb114c4bd09b035e3a495`.

This identity is not promoted here as independently re-admitted evidence until the exact summary bytes are hash-checked by the native V91 runner.

## Remaining exact unknowns

V91 must remain fail-closed until native Zag independently establishes:

1. the protocol-5 traversal path and exact byte offsets for `evidence -> semantic_generation -> examples -> naive[0..15]` in the admitted R23 state;
2. for each of the 16 strings: opcode form, text offset, byte length, and native SHA-256;
3. exact native admission of the 29,242-byte `r23_summary.json` and JSON lexical offsets for the same 16 `naive` values;
4. state-vs-summary byte equality for all 16 strings;
5. one framed 16-row receipt digest binding index, string bytes, state offsets, summary offsets, and source identities;
6. any memo references encountered by the bounded protocol-5 extractor must resolve exactly; unsupported or ambiguous opcodes must refuse rather than guess.

## Gate state

`FAIL_CLOSED_PENDING_NATIVE_EXACT_EXTRACTOR_EXECUTION`

No learner authority, promotion credit, semantic-generator behavior closure, scientific exposure, or canonical mutation is granted by this evidence report.
