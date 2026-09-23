# PORT_EQUIV.md — S5 storage core port equivalence

The ingest binary (`build/ingest.zag`) ports the S5 decision/storage core
from `ops/storage-compression/src/s5_learner.zag`. This file records the
equivalence proof required by the prereg before the full run.

## Method

1. **Textual**: extracted all 21 ported functions from both files, applied
   the mechanical rename map (t_* → sc_*, TStore → ScStore), stripped
   comments, normalized whitespace, and diffed. Script:
   `build/port_diff.py`.
2. **Behavioral**: the small-scale end-to-end run (2,000 facts through the
   full path: gate → install → compact → chain → seal → persist → sindex →
   query) exercises every ported function; the seal is deterministic across
   reruns (byte-identical store.dat/blob/sparse.idx/manifest/audit.log).

## Result

- 15 of 21 functions: code-identical after rename/comment normalization.
- 6 of 21 functions: differences, each reviewed and benign:

| function | difference | verdict |
|---|---|---|
| sc_g64 | offset param widened i32→i64, converted back internally | benign: identical for all offsets < 2^31 (all real offsets) |
| sc_store_init | drops s5's `ovr_*` in-RAM override fields and `ops_verify` counter | benign: `ovr_*` lived in s5's non-ported override fns (replaced by persistent overrides.dat); `ops_verify` is only incremented in s5's non-ported `sc_teach_value` |
| sc_pick_width | trailing whitespace only | benign |
| sc_compact_and_seal | removes dead `signed`/`voff` locals (voff was 0); slice-field aliased to local per ZNC codegen rules | benign: `sc_wval(cc,0+k*w,…)` ≡ `sc_wval(cc,k*w,…)`; slice aliases share memory |
| sc_add | trailing whitespace only | benign |
| sc_seal_tail | trailing whitespace only | benign |

- New functions (not ports, ingest additions): `sc_flags_get`,
  `sc_flags_set` (tombstone/revised meta bits), `sc_chain_recompute_all`
  (re-chain after legitimate meta changes), the blob tier, the judgment
  gate (G1–G4 + CAL), sparse index, revise/delete, persistence.

## Semantic note (carried from the prereg)

The ported S5 core stores i64 slot values (here: blob offsets). The 5.53
B/fact figure from the S5 benchmark is the slot-tier cost only. Text blobs,
keys, the sparse index, audit events, and overrides are separate tiers with
their own measured B/fact, reported in the final run report.
