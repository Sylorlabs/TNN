# KB-CONTROL CREW B — Interface Documentation

Conscious-control fork of the TNN knowledge base. Pure Zag, zero RNG,
expensive-but-thorough. Every mutation deliberately verifies target geometry
(including padding), reads back writes, and proves adjacent facts' hashes
remain unchanged.

## Mechanism

**Journaled two-phase append-only writes with pointer-swap revisions.**

- **One conscious record-byte write site**, only at the fresh tail. All
  record bytes flow through `kb_conscious_write_record`, which enforces:
  - **V1**: `off == total == nchunks*CHUNK + cur_used` (write only at the
    verified fresh tail; cross-slot clobber is structurally impossible
    because no write site addresses any other offset).
  - **V2**: the record fits in the chunk's data capacity.
  - **V3**: every target byte is zero before the write (no silent overwrite).
- **Revisions** append a new version at the tail; the slot pointer swaps to
  the new offset. The old version remains as history. **Deletes** are
  tombstones (slot flag set, data retained).
- **Rollover** advances by the full chunk, including padding and the 16-byte
  trailer (used length, sequence, `KBCT` magic). Flushed chunks are
  self-describing. On load, the journal replay adopts flushed chunks on
  demand via trailer-checked synthesis, driven by each intent's (nb,tb).
  A chunk file without a journal intent is uncommitted crash debris and is
  ignored (the journal is the source of truth).
- **Intent framing**: every mutation stages a journal intent
  `[4B len][8B seq][1B op][payload][4B len]` with duplicated lengths,
  fsynced before the data commit. Readers expose only committed directory
  entries.
- **Post-write verification**: the staged record is read back from the
  journal and from the chunk; header, hash, and predecessor integrity are
  checked. The predecessor's hash is re-verified to prove no adjacent
  clobber.
- **Hash-chained ledger**: every committed mutation and every failure
  appends an 81-byte entry `[32B prev][1B op][4B id][8B off][4B len][32B hash]`.
- **Recovery**: on load, the journal is scanned. Torn entries are truncated
  (fail closed). Intact uncommitted intents are reported DIRTY by `verify`;
  `recover` replays them idempotently and appends the commit. Only old or
  new complete versions are ever visible.
- **Journal<->ledger completeness** (K2 fix, streaming validator 2026-09-24):
  every committed journal mutation (commit frame op 2/4/6) must have exactly
  one ledger entry (op 1/2/3) with the same (id,off,len,hash), in exact
  journal-commit order, one-to-one. The validator streams: the ledger is read
  through a 1 MiB window and the journal frame-by-frame, retaining at most one
  pending intent — O(1) memory, no whole-ledger load, no size cap (the former
  32 MiB ceiling and 500,000-entry tables are removed). Strict `verify` fails
  closed (`CENSUS FAIL journal-ledger-gap`, rc=2) on any omission, duplicate,
  reorder, removal, extra entry, or content mismatch — including
  attacker-rechained ledgers whose hash chain alone verifies. `recover`
  reconciles ONLY an exact ledger prefix: it appends the missing deterministic
  suffix in journal order, hash-chained from the current head. Any non-prefix
  divergence (gap in the middle, reordered, forged) is corruption (rc=-2):
  recover refuses to rewrite, skip, or reorder. Reconciliation is idempotent
  and resumable: a crash mid-reconciliation leaves a partial suffix that the
  next recover completes; a fully-reconciled ledger is reconstructed
  byte-identically. Torn ledger tails (size % 81 != 0) are truncated on
  recover, then audit/reconcile runs, so a crash mid-ledger-append heals.
  Verified 2026-09-24: 3× 9/9 crash batteries (27/27), 7/7 adversary matrix
  (duplicate/reorder/removed/extra/forged rejected; missing-suffix repaired;
  missing-middle rejected), mid-reconciliation crash resumability, torn-tail
  truncation.
- **Staging buffers** (2026-09-24 fix): `kb_do_put`/`kb_do_revise` stage
  records in a buffer sized proportionally to the actual record
  (`11+key.len+text.len`), not a full `KB_CHUNK`. The prior full-chunk
  staging leaked ~1 MB per mutation at 1 MiB geometry (850 MiB RSS observed
  in batch); proportional staging bounds the leak to record size.
- **Checkpoint**: `store.dat` is written via temp+fsync+rename+dir-fsync.
  On load, the authoritative state is rebuilt from zero by adopting
  trailer-backed chunks and replaying the journal; the checkpoint is
  informational only.

## CLI

```
kbctl init <dir> [--mode=conscious|fast]
kbctl put <dir> <id> <key> <textfile> [--mode=...]
kbctl revise <dir> <id> <textfile> [--mode=...]
kbctl delete <dir> <id> [--mode=...]
kbctl get <dir> <id> [--mode=...]
kbctl verify <dir> [--mode=...]        # full census; DIRTY if uncommitted work
kbctl recover <dir> [--fail-after=N]  # replay uncommitted intents + reconcile
                                      # journal<->ledger; N>0 crashes after N
                                      # reconcile appends (test hook, rc=99)
kbctl batch <dir> <batchfile> [--mode=...]
kbctl dump <dir>                      # slot table dump
kbctl stats <dir>                     # chunks/total/slots/live/jsize/jseq
kbctl crashput <dir> <id> <key> <textfile> <point>    # point: 1,2,3
kbctl crashrevise <dir> <id> <textfile> <point>       # point: 1,2,3
```

Crash points: 1=after-journal, 2=after-data, 3=after-commit. Exits 99 on
simulated crash. `delete` also honors `--fail-after=1|2|3` (1=after intent,
2=after in-memory tombstone, 3=after commit).

Modes:
- `conscious` (default): the full mechanism above. Every op is a separate
  process invocation; each does journal+data+commit+ledger+checkpoint.
- `fast`: the baseline. Minimal framing, batched persistence, no journal,
  no ledger, no read-back. Used for head-to-head benchmarking only; it is
  NOT crash-safe and does NOT meet the kill bars.

## Invariants

- `total == nchunks*CHUNK + cur_used` (tripwire checked on every load).
- No record byte is ever written except at the verified tail via the single
  conscious write site.
- `verify` returns DIRTY (rc=3) iff the journal holds an intact uncommitted
  intent. Clean stores verify OK (rc=0). Corrupt stores fail closed (rc=2).
- Three byte-identical runs produce byte-identical stores (chunk files,
  journal, ledger, slotdir, store.dat).

## Kill bars

- **K1**: zero cross-slot clobbers across T1–T4. Any clobber → DOES NOT SHIP.
- **K2**: all 120 T4 crash trials fail closed (DIRTY→recover→OK, data intact).
- **K3**: three full runs byte-identical (SHA-256 of every store file).
- **K4**: zero RNG in the codebase (grep-verified) and in decision paths.
