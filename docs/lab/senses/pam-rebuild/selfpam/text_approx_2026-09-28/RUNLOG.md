# RUNLOG.md — dev-only determinism runs (2026-09-28)

**Scope:** Builder determinism check on OPEN dev set only. NOT the sealed corpus.
The builder never scores the sealed corpus (tester crew does).

## ta1_derive — edge derivation from dev episodes

**Binary:** `/tmp/ta1_derive` (built from `src/ta1_derive.zag` via znc)
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Input:** `dev/dev_episodes.tsv` (3 episodes)
**Command:** `ta1_derive dev/dev_episodes.tsv <out.tsv>`

| Run | Env | stdout SHA-256 | stderr SHA-256 | edges.tsv SHA-256 | rc |
|---|---|---|---|---|---|
| 1 | normal | cc32246498c4ca08614d3a5e32935a1e39869a77560ddde5980dc8f96bbbd9de | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | d3db0eecf3035e8d54ac6e273e903bbdf62d0fe7ad481e5cc75f543258be5591 | 0 |
| 2 | normal | cc32246498c4ca08614d3a5e32935a1e39869a77560ddde5980dc8f96bbbd9de | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | d3db0eecf3035e8d54ac6e273e903bbdf62d0fe7ad481e5cc75f543258be5591 | 0 |
| 3 | MALLOC_PERTURB_=1 | cc32246498c4ca08614d3a5e32935a1e39869a77560ddde5980dc8f96bbbd9de | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | d3db0eecf3035e8d54ac6e273e903bbdf62d0fe7ad481e5cc75f543258be5591 | 0 |

**Result:** 3/3 byte-identical (stdout, stderr, edges.tsv) including allocator perturbation.
**Output:** 3 edges, 0 refused:
- `keeps the tide ledger` ↔ `maintains the tide log` (0.9, DEVEP-01)
- `maintains the tide log` ↔ `holds the tide records` (0.9, DEVEP-02)
- `delayed` ↔ `held up` (0.6, DEVEP-03)

## Source/binary SHAs
- `src/ta1_derive.zag`: (see commit)
- `src/text.zag`, `src/lists.zag`, `src/io.zag`: (see commit)
- Binary `/tmp/ta1_derive`: 35324 bytes

## Note
KB-TA-5 requires 3/3 byte-identical FULL runs. This log covers the derivation
component on the dev set. The full-corpus gate determinism run is the tester's
responsibility per protocol (builder must not score the sealed battery).
