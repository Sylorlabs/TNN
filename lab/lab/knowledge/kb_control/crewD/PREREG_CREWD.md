# PREREG — KB-Control Crew D: Silent-Overwrite Red Team (frozen)

**Date:** 2026-09-23. **Crew:** D (red team vs the silent-overwrite battery).
**Status:** FROZEN. Committed alone before any attack runs.
**Branch:** `tnn-native-lab`. **Work dir:** `~/workspace/kb_control/crewD/`.
**Commit path:** `docs/lab/knowledge/kb_control/crewD/`.
**Kill bar (Micah):** zero cross-slot clobbers. The conscious fork (Crew B)
ships only if it survives this battery.

## 1. Background (quoted from `knowledge/ingest_1gb/FINDINGS.md` §2.4 / RT-G3)

> `igb_append` never counts inter-chunk zero-padding in `b.*.total`. Each
> 33,488,896-byte blob chunk ends with 40–467 bytes of padding that `total`
> ignores → slot→blob offsets wrong for **92.4% of slots**; the red team's
> independent census on a 260k-slot store found **100% of post-first-chunk
> slots wrong**. … G3: 5/5 pre-boundary revises SUCCEED but silently destroy an
> unrelated fact (`rtg:0259999` → NOTFOUND) — padding-blind `bb.used`
> overwrites the last 126 data bytes of the final blob chunk.

Precise mechanism: `ig_revise` reconstructs append state as
`bb.used = (btotal % IG_BLOB_CHUNK)`. Because `btotal` never counted padding,
`bb.used` understates the true tail position by the accumulated padding of
all prior chunks. The revised record is written at `cur[used]` — on top of
live bytes of an unrelated fact near the chunk tail. The write "succeeds";
the victim fact is silently destroyed. Crew A root-causes in parallel; if
`ROOTCAUSE_A.md` lands it is advisory only — this battery is defined against
the frozen FINDINGS.md above and needs nothing from Crew A.

## 2. Targets

- **T-FAST (current fast path):** the genuine current store code
  (`knowledge/ingest_1gb/build/ingest.zag` at commit `118251c5`, SHA recorded
  in the build manifest), wrapped in a `kbctl`-compatible CLI. Only change:
  `IG_BLOB_CHUNK` is a build-time constant per geometry variant (source SHA +
  substituted line recorded; the write-path logic is untouched). This is the
  code that produced the 126-byte clobber.
- **T-CONSCIOUS (Crew B fork):** Crew B's `kbctl --mode=conscious` when their
  handoff lands (their prereg §6 freezes the interface; this battery drives
  that exact interface). Until it lands, only T-FAST runs — and T-FAST must
  die first (see §8, battery-validity gate).

Crew B's fork was not built at prereg time. The battery is proven against
T-FAST; the T-CONSCIOUS leg is PENDING their handoff and re-runs the identical
battery unmodified.

## 3. Binary interface (frozen — mirrors Crew B prereg §6 verbatim)

Single binary `kbctl` (pure Zag, deterministic — logical op clock only, no
wall time, no RNG). T-FAST's binary accepts `--mode=fast` and rejects
`--mode=conscious` (usage error); the driver always passes `--mode=<target>`.

```
kbctl init <dir> [--mode=fast]
kbctl put <dir> <id> <key> <textfile> --mode=fast|conscious
kbctl revise <dir> <id> <textfile> --mode=fast|conscious
kbctl delete <dir> <id>
kbctl get <dir> <id>                 # OK line + raw key + raw text, or NOTFOUND
kbctl verify <dir>                   # OK n=<n> mismatches=0 digest=<hex> | FAIL
kbctl recover <dir>                  # RECOVERED n (T-FAST: no journal, no-op verify)
kbctl crashput <dir> <id> <key> <textfile> --mode=fast|conscious --fail-after=data|meta
kbctl crashrevise <dir> <id> <textfile> --mode=fast|conscious --fail-after=data|ovr|meta
```

Exit codes: 0 ok · 1 usage/argument error · 2 integrity/verify failure ·
3 write-protocol abort (fail-closed) · 99 simulated crash (partial state left
for `recover`+`verify`).

`get` output (frozen, byte-exact):
```
OK kind=<k> id=<id> keylen=<kl> textlen=<tl> sha256=<hex64>
<key raw bytes>\n<text raw bytes>
```
`sha256` = sha256 over the stored record bytes (`[1B kind][4B id LE][2B klen
BE][4B tlen LE][key][text]`). Deleted/unknown id → `NOTFOUND`, rc=1.

T-FAST store layout = the current layout (`blob_NNNNNN.dat` × C bytes,
`store.dat`, `overrides.dat`); `sparse.idx` is not built (this battery tests
the write path; key lookup is out of scope). T-FAST-only test subcommand
`bulkfill <dir> <n> <maxtextlen>` builds an n-record store in one process
(fixture setup for the genuine-geometry leg; NOT part of the per-op protocol).

Crash-stage definitions, T-FAST (frozen — stages of the CURRENT protocol):
- `crashput --fail-after=data`: chunk file flushed with the new record bytes,
  then exit 99 BEFORE `store.dat` is saved (slot not added).
- `crashput --fail-after=meta`: `store.dat` saved (slot added), then exit 99
  (no later stage exists for put; exercises the post-commit path).
- `crashrevise --fail-after=data`: chunk flushed with new record, exit 99
  BEFORE `overrides.dat` (override still points at old record).
- `crashrevise --fail-after=ovr`: `overrides.dat` saved (override points at
  new record), exit 99 BEFORE `store.dat` (flags/seal not updated).
- `crashrevise --fail-after=meta`: `store.dat` saved, exit 99 (post-commit).
T-CONSCIOUS stages are defined by Crew B's `INTERFACE.md` (`journal`,
`data`, `commit` per their prereg §2.4); the driver passes the same
`--fail-after=` values through and the oracle (§6) is identical.

## 4. Fixtures (deterministic — zero RNG anywhere)

- `key(id)` = `k%06d` (7 bytes, e.g. `k000042`).
- `text(id, seq, tlen)`: byte `j` = `65 + ((id*31 + seq*17 + j*7) % 26)`
  (A–Z pattern; fully determined by `(id, seq, tlen)`).
- Storm lengths: `tlen(n) = 1 + ((n*7919 + 13) % 1500)` (1..1500).
- Boundary lengths: computed exactly per attack (see §5 F2).
- All schedules enumerated explicitly in `battery.py`; no randomness source
  exists in any tool (`grep -r rand` gate over `src/`).

## 5. Attack families (frozen)

Chunk-size variants: **4096, 8192, 65536, 1048576** (small, fast legs) plus
**33488896** (genuine geometry, bulk-filled, revise-only leg). Default
battery variant is 8192. Padding is MEASURED per leg (scan each chunk file
for the last non-zero byte); every leg must observe padding intersecting the
[40,467]-byte range seen in the 1GB audit, or the leg is VOID.

- **F1 — adversarial revise sequences** (the G3 pattern). Fill N=600
  (storm lengths; ≥2 chunks at C=8192). Then:
  - A1: 40 revises of ids whose records END within 256 bytes of a chunk end
    (pre-boundary). New-text lengths: longer (2×), shorter (½), same (⅓ each).
  - A2: 20 revises of ids whose record IS the last record of a chunk.
  - A3: 20 revises of ids whose record IS the first record of chunks ≥1.
  - A4: 20 revises at arbitrary mid-chunk offsets.
  - A5: 20 double-revises (revise, then revise again — override replace-in-place).
  - A6: revise-then-delete (10), delete-then-revise (10, must fail closed with
    `revise: fact is deleted`, rc=3).
  - After EVERY single revise: get-check of the revised id AND its physical
    chunk neighbors. After each batch A1–A6: full oracle (§6).
- **F2 — boundary-size facts.** Fresh store per sub-attack, then oracle:
  - B1: record sized so `used+reclen == C` exactly (ends at chunk end, zero padding).
  - B2: `used+reclen == C+1` (forces rollover), then a 1-byte-text record.
  - B3: text lengths exactly 4096 (`IG_MAX_TEXT`) and exactly C−11−7
    (single record fills a chunk exactly).
  - B4: records engineered so chunk padding is exactly 40, 200, and 467
    bytes; then revise a chunk-0 fact and census the tail.
  - B5: 1-byte-text facts (minimum records) × 200.
- **F3 — concurrent (interleaved) writes.** 12 deterministic schedules over
  12 ids, each a fixed op list mixing put/revise/delete, including:
  revise-of-just-revised, delete-of-just-revised, put-after-delete-of-other,
  revise deleted id (must fail closed), put duplicate id (must fail closed,
  `sc_add` dupe path), delete unknown id (must fail), revise unknown id
  (must fail). Oracle after each schedule. (Ops are sequential CLI
  invocations; "concurrent" = adversarial op interleaving — the store has no
  threads, and neither does the battery.)
- **F4 — power-loss mid-write.** `crashput` × 20 trials per stage
  (`data`, `meta`); `crashrevise` × 20 trials per stage (`data`, `ovr`,
  `meta`); target ids and texts deterministic and distinct per trial.
  After each trial: `recover` (rc 0) → `verify` (OK) → crash oracle (§6 O5).
  100 crash trials per target per geometry variant (8192 + genuine leg).
- **F5 — padding-geometry fuzz.** Per chunk-size variant: fill with storm
  lengths, measure padding distribution, run F1-lite (20 pre-boundary
  revises), full oracle. Genuine-geometry leg (C=33488896): `bulkfill`
  ~16.3K records (2 chunks), then 20 CLI revises of chunk-0 pre-boundary
  ids — the direct RT-G3 reproduction at real geometry — plus full oracle.

## 6. Oracle (frozen — runs after every attack batch, and per-op where noted)

- O1 model: Python dict `id → (live|deleted, key, text)`. Updated ONLY when
  the CLI reports success (rc=0); expected-fail ops leave the model unchanged.
- O2 get-check: every live id → `get` → kind/id/key/text/sha256 all equal
  model (sha256 recomputed by the driver over the canonical record bytes).
  Every deleted id → `NOTFOUND`. ANY mismatch/missing/resurrected = clobber.
- O3 verify: `kbctl verify` → rc 0 and `OK ... mismatches=0`.
- O4 deep census (slot→blob offsets): every slot's EFFECTIVE offset
  (override-aware) → parse record header at that offset → header id == slot
  id. Report mismatch count. (Adapted from the RT-G1 census walker.)
- O5 crash oracle: after `recover`: O3 passes; `get(target)` is byte-exactly
  the OLD bytes or byte-exactly the NEW bytes (never partial/torn); every
  other id matches the model (no collateral).
- O6 byte-identity: full battery × 2 reruns → SHA256 of every store file +
  sorted dir digest identical across reruns.

## 7. Kill criteria (frozen)

- **K1 — zero clobber (hard):** any O1/O2/O3/O5/O6 failure → **KILL**.
  One clobbered byte = KILL. This is Micah's bar.
- **K2 — offset correctness:** O4 mismatch count > 0 → criterion FAIL.
  T-FAST: EXPECTED FAIL (the known 92.4% G1 defect; documents it, not a
  surprise). T-CONSCIOUS: FAIL = **KILL**.
- **K3 — crash fail-closed:** any O5 failure → **KILL**.
- **K4 — determinism:** any O6 divergence → **KILL** (then investigate).
- **Verdict per target: SURVIVE** iff K1 ∧ K3 ∧ K4 pass (K2 reported
  separately per target).

## 8. Battery-validity gate (frozen)

Before ANY verdict on T-CONSCIOUS: the battery must reproduce the known G3
clobber on T-FAST — a revise that reports success while destroying an
unrelated fact (victim id, byte offset, and clobber size recorded
byte-identically). A battery that cannot catch the known bug is decoration:
if F1 does not KILL T-FAST, the battery is VOID and must be repaired, never
worked around.

## 9. Evidence (frozen)

Per phase: phase id, op list, store-dir SHA digest (sorted file list +
SHA256 per file), oracle result, `prev_hash` chain
(`phase_hash = sha256(prev_hash ‖ phase_bytes)`; genesis prev = 32 zero
bytes). Deliverables: `RUNLOG.md`, `evidence/` (per-phase JSONL,
`BYTE_IDENTITY.txt` with rerun SHAs), `VERDICT.md`. No binaries, no `.zagd`
in commits. All reruns ≥ 2.

## 10. Commit plan (frozen)

1. This prereg — committed ALONE (this commit).
2. `src/` (kbctl.zag, battery.py, oracle.py, gen fixtures) + `INTERFACE_FAST.md`
   + build manifest (source SHA, chunk-const substitution, binary SHAs).
3. `RUNLOG.md` + `VERDICT.md` + `evidence/` (T-FAST verdict; T-CONSCIOUS leg
   appended as its own commit when Crew B's handoff lands).

## 11. Open questions (not blockers)

- Crew B handoff timing/path for their `kbctl` binary (T-CONSCIOUS leg pending).
- `ROOTCAUSE_A.md` (Crew A) not landed at prereg time — advisory only if it lands.
