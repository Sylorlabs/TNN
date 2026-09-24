# PREREG — KB-Control Crew B: Conscious-Control Fork (frozen)

**Date:** 2026-09-23. **Crew:** B (conscious-control fork; Crew A root-causes in parallel).
**Status:** FROZEN. Committed alone before any build results.
**Branch:** `tnn-native-lab`. **Work dir:** `~/workspace/kb_control/crewB/`.
**Commit path:** `docs/lab/knowledge/kb_control/crewB/`.

## 1. Root cause (quoted from `knowledge/ingest_1gb/FINDINGS.md` §2.4 / RT-G3)

> `igb_append` never counts inter-chunk zero-padding in `b.*.total`. Each
> 33,488,896-byte blob chunk ends with 40–467 bytes of padding that `total`
> ignores → slot→blob offsets wrong for **92.4% of slots**; the red team's
> independent census on a 260k-slot store found **100% of post-first-chunk
> slots wrong**. … G3: 5/5 pre-boundary revises SUCCEED but silently destroy an
> unrelated fact (`rtg:0259999` → NOTFOUND) — padding-blind `bb.used`
> overwrites the last 126 data bytes of the final blob chunk.

Mechanism of the clobber, precisely: `ig_revise` reconstructs append state as
`bb.used = (btotal % IG_BLOB_CHUNK)`. Because `btotal` never counted padding,
`bb.used` understates the true tail position by the accumulated padding of all
prior chunks. The revised record is then written at `cur[used]` — on top of
live bytes belonging to an unrelated fact near the chunk tail. The write
"succeeds"; the victim fact is silently destroyed. This is the stingy-LLM
behavior Micah ordered dead: a mutation that does not deliberately verify its
target.

Crew B does not block on Crew A's root-cause refinement. The fork replaces the
addressing scheme outright; any padding fix Crew A lands in the fast path is
independent of (and strictly weaker than) the guarantees below.

## 2. Design: journaled two-phase append-only write

Micah's law for this fork: **TNN must CONSCIOUSLY control its knowledge base —
expensive but thorough, never subconscious.** Every mutation is deliberate.
The design is a short explicit checklist the operator (TNN itself, or the
binary enforcing it) performs per mutation — not a pile of edge-case policies.
Figure-it-out beats rigid-policy: the checks are few, general, and
unskippable (the write site is unreachable without passing them).

### 2.1 Single write site (structural anti-clobber)

- Record bytes are written at exactly ONE code site: the tail of the open
  chunk. In-place overwrite of any existing record is forbidden by the
  protocol: **revise = append(new version) + journaled pointer-swap** in the
  override table; **delete = tombstone flag**. Old record bytes are never
  touched, by any path.
- Because no code path ever computes an address inside another slot's region,
  cross-slot clobber on the write path is structurally impossible — there is
  no "wrong offset" that lands inside a live record; the only addresses the
  writer can produce are fresh-tail addresses.

### 2.2 Verify-before-write (deliberate, three assertions)

Before any byte is written, the fork asserts:

1. **V1 — append-only invariant:** `pos == total`, where `total` counts EVERY
   byte ever assigned (records + zero padding + chunk trailers), advanced by
   whole chunks at rollover. There is no separate "padding" quantity that can
   be forgotten: forgetting padding breaks V1 immediately, fail-closed. This
   is the structural fix for the G-bug class.
2. **V2 — capacity:** `pos + reclen ≤ chunk_data_capacity`
   (`CHUNK − TRAILER_LEN`). A record never crosses a chunk boundary and never
   touches the trailer.
3. **V3 — freshness:** the target region `[pos, pos+reclen)` reads all-zero.
   No live data may occupy the write target.

Any violation → abort the mutation, fail closed, append a `VERIFY_FAIL` entry
to the hash-chained audit ledger. The write site is not reached.

### 2.3 Per-chunk self-describing geometry

Every flushed chunk file is exactly `CHUNK` bytes and ends with a 16-byte
trailer: `[8B used][4B seq][4B magic "KBCT"]`. `used` = data bytes in this
chunk. Chunk geometry is recoverable from disk alone; recovery and `verify`
never trust in-memory counters without re-deriving them. Records use the
existing 11-byte header `[1B kind][4B id LE][2B klen BE][4B tlen BE][key][text]`
so corpora stay comparable with the ingest line.

### 2.4 Two-phase journaled commit (power-loss fails closed)

Each mutation (put/revise/delete-pointer-swap) executes:

1. **Stage:** build the record bytes in a staging buffer; re-parse the staged
   header (kind/id/klen/tlen bounds-checked); compute sha256 over the staged
   bytes.
2. **Journal:** append a length-framed entry
   `[4B len][seq,op,id,off,len,hash,record_bytes][4B len]` (length on both ends
   = torn-write detection) to `journal.dat`; **fsync** the journal.
3. **Commit data:** run V1–V3; write staged bytes at `pos`; **fsync** the chunk
   file (full-chunk flush at rollover writes the whole chunk + trailer +
   fsync).
4. **Commit metadata:** update the in-memory slot directory
   (id → offset, length, sha256); append a `COMMIT` entry to the journal;
   persist `slotdir.dat` + `store.dat` + **fsync**.
5. **Read-back-verify:** re-read `[off, off+len)` from the chunk file,
   re-parse the header, check id match, recompute sha256 and compare to the
   staged hash; check the **physically adjacent records' hashes**
   (predecessor and successor in chunk order) unchanged; append all hashes to
   the hash-chained audit ledger (`ledger.dat`:
   `[prev_hash(32)][op(1)][id(4)][off(8)][len(4)][hash(32)]`).

Readers consult ONLY the slot directory, which is updated strictly after the
verified commit. Crash at any point: recovery replays `COMMIT`-marked intents
(idempotent — the target region was verified zero, so replay writes the same
bytes) and discards incomplete/torn journal entries. The store presents either
the old version or the new version, never a half-written fact.

### 2.5 Authoritative slot directory

`slotdir.dat`: id → (global_offset, length, sha256). Every read path
re-parses the record header at the claimed offset and verifies id, length, and
hash. The slot→blob mapping is never derived from bare arithmetic on
untrusted counters.

## 3. What the fork proves (not asserts)

- **P1:** cross-slot clobber impossible by construction (§2.1) AND empirically
  zero across the battery (§5) AND across Crew D's red-team battery (clean
  binary interface, §6).
- **P2:** power-loss at any phase boundary fails closed (§5 T4).
- **P3:** byte-identical reruns: same corpus + op sequence → identical store
  bytes + identical ledger digest, 3 runs (§5 T5).
- **P4:** zero randomness in decision paths (grep gate + replay certifier, per
  program law).

## 4. Kill bars (frozen — any trip = fork does not ship)

- **K1 — zero clobber:** across the self-run battery AND Crew D's battery,
  every mutation is followed by a full-census hash verification. A clobber =
  any fact's stored sha256 ≠ sha256 of bytes re-read via the slot directory,
  or any neighbor-integrity check failing outside the mutation target's own
  slot. ONE clobber → no ship. Report plainly.
- **K2 — crash fail-closed:** fault injection at all 3 phase boundaries
  (after journal fsync / after data write / after commit mark), 20 trials
  each. Recovery must yield old-version-intact or new-version-intact;
  `verify` must pass; a half-written fact presented as good → no ship.
- **K3 — determinism:** 3 full-battery runs → byte-identical store files and
  identical ledger digest. Any divergence → no ship.
- **K4 — no RNG:** decision paths contain no randomness source; verified by
  source grep + byte-identical rerun gate.
- **Cost honesty (not a kill):** appends/sec, revise latency (mean/p99), and
  bytes/fact storage overhead for fast vs conscious on the SAME corpus are
  measured and reported even if ugly. Thoroughness is the point of this fork;
  if conscious mode is >50× slower on appends, that triggers a redesign note,
  not silent acceptance.

## 5. Self-run test battery (before handoff to Crew D)

Test geometry uses small chunks (CHUNK=4096 in the test build; production
default 33,488,896) to force constant rollovers — the padding path is
exercised on nearly every record.

- **T1 — append storm:** 20,000 appends, deterministic length sequence cycling
  1..1500 (forces rollover every ~3–8 records). Full census after: every
  record re-parsed, id/length/hash checked; every chunk trailer re-derived;
  every zero-gap region verified zero.
- **T2 — boundary revises (the G3 pattern):** 500 revises targeting records
  whose `[off, off+len)` lies within 256 bytes of a chunk end, plus 500
  revises at arbitrary offsets. Neighbor-integrity check after EACH revise.
- **T3 — deletes + re-adds:** 200 deletes, 200 re-adds of deleted ids,
  census after.
- **T4 — crash matrix:** `--fail-after=journal|data|commit` × 20 trials each
  on put and revise → `recover` → `verify` → version check (old or new,
  never half).
- **T5 — byte identity:** full battery × 3 runs, SHA-compare all store files
  + ledger digest.
- **T6 — head-to-head:** same corpus, `--mode=fast` (fast path: correct
  padding accounting, no V1–V3, no journal, no read-back) vs
  `--mode=conscious`. Report appends/sec, revise latency mean/p99, bytes/fact
  overhead. The delta is the honest cost of thoroughness.

## 6. Binary interface for Crew D (frozen)

Single binary `kbctl` (pure Zag, deterministic — logical op clock only, no
wall time, no RNG):

```
kbctl init <dir>
kbctl put <dir> <id> <key> <textfile> [--mode=fast|conscious]
kbctl revise <dir> <id> <textfile> [--mode=fast|conscious]
kbctl delete <dir> <id>
kbctl get <dir> <id>                 # prints kind id key text + stored sha256
kbctl verify <dir>                   # full census; prints OK or FAIL + ledger digest
kbctl recover <dir>                  # journal replay / discard; prints RECOVERED n
kbctl crashput <dir> <id> <key> <textfile> --fail-after=journal|data|commit
kbctl crashrevise <dir> <id> <textfile> --fail-after=journal|data|commit
```

Exit codes: 0 ok · 1 usage/argument error · 2 integrity/verify failure ·
3 write-protocol abort (fail-closed: V1–V3 or read-back failed) · 99 simulated
crash (partial state left for `recover`+`verify`).

Store dir layout (all files documented in `INTERFACE.md` at handoff):
`chunk_000000.dat…` (CHUNK bytes each, 16-byte trailer) · `journal.dat`
(length-framed, fsync'd) · `slotdir.dat` · `store.dat` · `ledger.dat`
(hash-chained).

## 7. Deliverables & commit plan

1. This prereg — committed ALONE (this commit).
2. `src/kbctl.zag` (+ substrate imports) — pure-Zag fork.
3. `INTERFACE.md` — Crew D handoff doc (binary interface, formats, exit codes).
4. `RUNLOG.md` — battery runs, byte-identity SHAs.
5. `HEADTOHEAD.md` — fast vs conscious cost numbers.
6. `VERDICT.md` — kill-bar verdict (K1–K4), plain language; ships or doesn't.

All under `docs/lab/knowledge/kb_control/crewB/`. No binaries, no `.zagd` in
commits (per AGENTS.md: filter `.zagd.semantic-ready`, `.zag-cache/`,
compiled binaries out of commit walks).
