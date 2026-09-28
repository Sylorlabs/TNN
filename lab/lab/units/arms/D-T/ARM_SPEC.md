# ARM D-T — Curriculum-Taught Seed Vocabulary — Specification

**Family:** CUT+ACQ | **Track:** A | **Status:** Implementation complete, battery in progress

## 1. Mechanism

D-T pre-commits the 500 most frequent content-word (C-W) chunks from the
training split via `CUT_COMMIT` (justification code 3), then runs the standard
D self-cut organ over the curriculum. The organ may revise, split, merge, or
kill taught seeds based on observed evidence. Taught seeds are NOT pinned;
only an explicit audited force-install/force-pin is irreversible (per
`units/TEACHERS.md`).

### 1.1 Vocabulary representation

- **Stable chunk IDs:** never reused; tombstoned on kill.
- **Chunk states:** proposed / committed / taught / demoted / dead.
- **Content index:** FNV-1a 64-bit hash + length, open-addressing tables.
- **ID-referenced memories:** ledger entries reference chunk IDs, not content.

### 1.2 Teaching (stage: TEACH)

`teach_seeds` scans the training corpus, counts C-W token frequencies via
`sc_count` (open-addressing, 65K slots), selects the top 500 by count
(deterministic: higher count wins; ties broken by first-seen order), and mints
each as a `ST_TAUGHT` chunk with `CUT_COMMIT` justification 3.

Repetition counts are saved BEFORE `chunk_mint` (fixing the earlier bug where
`c_rep` received -1).

### 1.3 Self-cut organ (stages: OBSERVE → REVISE)

**OBSERVE** (`observe_pass`): For each C-W token, emits candidates:
- 1-gram (the token itself)
- 2-gram, 3-gram, 4-gram (via forward scan, bounded by `DT_LMAX=64`)
- token + trailing whitespace run

For each candidate:
- If it matches a taught seed (`st_find`): increment `t_rep`, OR the
  continuation byte into `t_cd`, increment `r_refs`.
- Else: `ht_bump` into the counting table (1M slots, 16-probe max, no
  eviction). Stores hash, length, count, 256-bit continuation diversity set,
  and one representative position.

**REVISE** (`revision_pass`): For each taught seed (in teach order):
- `rep < 3` → `CUT_KILL` (insufficient evidence), tombstoned.
- Committed sub-chunk S strictly inside T with `S.rep > 2*T.rep`
  → `CUT_SPLIT` (T tombstoned, remainders minted).
- Committed super-chunk U strictly containing T with `U.rep > 2*T.rep`
  → `CUT_MERGE` (T absorbed into U, tombstoned).
- Stronger evidence ratio wins; split wins ties.

**Note on sub-token candidates:** Prefix/suffix affix candidates were omitted
for feasibility (the organ cuts at token and phrase level; seeds cover frequent
tokens). This is a documented speed/fidelity tradeoff, not a mechanism change.

### 1.4 Determinism

- Zero RNG in any decision path.
- FNV-1a 64-bit hashing (deterministic).
- Fixed-size tables, linear probing, deterministic tie-breaks.
- Byte-identical reruns verified (M8 hard gate).

## 2. Binding kill criterion

> "≥50% of taught seed chunks are revised/killed by end of curriculum AND
> untaught D matches D-T on M1/M2/M3 — teaching adds nothing measurable."

This is a COMPOUND kill. It cannot fully fire without the concurrent untaught
D result. Per assignment: do NOT build D as a substitute; recheck other crews.

**Status:** D-T shows 97.6% seed revision (488/500) on M2 t1-prose. The
untaught-D comparison awaits the official D crew result. A private ablation
(`x-abl-*` modes) is implemented for informative comparison only and MUST NOT
be used to fire the compound kill.

## 3. Frozen metric notes

- **M3 naming:** Frozen §5 calls M3 "retention under churn"; an older alphabet
  used M3 for "reuse". The frozen names are applied literally; the mismatch is
  documented here.
- **M1 provisional A15:** N=64 deterministic remaps; `TRAINER_SWAP_PROBE`
  logging; `PROVISIONAL-PENDING-FREEZE` marked.
- **M7 provisional C′:** first-byte XOR 0xFF; 5,000 lookups via `(l*37)%nunits`.
- **M8 A17:** combined M1+M3 construction; ambiguity documented.

## 4. Performance notes

- `observe_pass` uses a fixed 1M-slot counting table (no per-candidate
  allocation, no sort). 16-probe max, skip on overflow (no eviction).
- 8-bit LSD radix sort was tried and abandoned (16-bit variant exhibited
  pathological slowness; 8-bit worked but sort-based was replaced by
  hash-table for the 2^25 slice limit).
- Single slices >2^25 bytes panic on index; all large structures are kept
  under 32MB per array.
- `DT_KCAP=1,048,576` (1M) for the candidate table.

## 5. Build

```bash
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 \
  cl/arm.zag -o ~/workspace/dt_bin
```

Substrate files (`R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag`) are copied
from B-64 per the frozen harness contract.

## 6. Modes

One binary, `argv[1]` dispatch:
- `m1-1x-prose`, `m1-1x-code`: M1 mastery.
- `m2-t1-prose`, `m2-t1-code`, `m2-t2-prose`, `m2-t2-code`, `m2-t3-1x`: M2 learning.
- `m3-1x`: M3 retention.
- `m4-1x-prose`, `m4-1x-code`: M4 revision.
- `m5-1x`: M5 cost.
- `m6-p2c-1x`, `m6-c2p-1x`: M6 transfer.
- `m7-1x`: M7 reuse.
- `m8-1x <outdir> <perturbation>`: M8 determinism.
- `x-abl-*`: PRIVATE untaught ablation (informative only; NOT the official D).

## 7. Correctness fixes applied

1. **Teaching repetition:** `s_cnt[best]` saved before `chunk_mint` (was -1).
2. **Merge threshold:** `jrep > 2*trep` (was inverted `trep < 2*jrep`).
3. **Candidate counting:** hash-table replaces sort (2^25 limit, performance).
4. **Empty `t.c`:** removed.
5. **Debug prints:** removed before score runs.
