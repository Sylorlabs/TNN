# Blind inputs for Attempt 3 (clean-room)

- `train_blind.tsv`: 448 train items. Columns: `id` (opaque T0001–T0448), `text`.
- `heldout_blind.tsv`: 192 held-out items. Columns: `id` (opaque H0001–H0192), `text`.

Both files are deterministically shuffled (seed 1545793672, documented in the
coordinator's build log) so item position carries no information. Opaque IDs
carry no class information. There is no class column. These files contain zero
label information.

The original-ID ↔ opaque-ID ↔ class mapping is sealed with the coordinator
(`~/workspace/epi_a3/_coordinator/MAPPING.sealed`). The implementer must NOT
read it. LOO verdicts are emitted by opaque train ID; the coordinator scores
them one-shot after the parser/build freeze.
