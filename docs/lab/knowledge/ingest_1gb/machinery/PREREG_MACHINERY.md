# PREREG — Machinery forks: sindex fix + S5 integration

Date: 2026-09-23. Frozen BEFORE any new battery runs.
Task: close the two machinery gaps in the 1GB ingestion stack (REPORT.md §7),
then characterize scaling toward the 10GB program (measure, don't run 10GB).

Toolchain (pinned): `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Zero RNG everywhere: splitmix64-of-index draws only. Every battery runs twice;
outputs must be byte-identical (SHA256 compared).

## Fork 1 — Zag sindex chunk-boundary bug

**Background.** Commit `b4d2852c` fixed `ig_lookup` in `build/ingest.zag`
(`rl==0` now advances to the next blob chunk instead of returning NOTFOUND —
the 999/1000 E1 failure: a key in chunk 8 missed when its sparse entry
pointed at chunk 7) but the binary was never rebuilt; the 1GB run used the
Python fallback `extract/build_sparse.py`, which emits every-1024th entries
PLUS the first key of each chunk. The shipped `run/store_full/sparse.idx`
has 2548 entries = 2537 every-1024th + 12 chunk-firsts − 1 overlap.

**Fix (Zag only).** In `build/ingest.zag::ig_sindex`:
1. Emit an entry when `id % IG_SPARSE_EVERY == 0` OR the record is the first
   of its chunk (mirrors the Python entry set exactly).
2. Guard: emitted keys must be non-decreasing in id order (the pipeline
   installs facts in globally sorted key order); fail loudly otherwise.
3. Entry-count bound becomes `(n+1023)/1024 + bnchunk`; the written count is
   the actual emitted count (Python writes its actual count too).
4. `ig_lookup` is NOT changed: the `rl==0 → next chunk` fix was audited —
   a missing chunk file makes `ig_blob_read_chunk` return −1, so the scan
   terminates (no infinite loop); records never straddle chunks.

**Equivalence proofs (bars F1.1–F1.5).**
- F1.1 (builder, live store): rebuild `ingest_bin` from the fixed source;
  `ingest_bin sindex run/store_full` → `cmp` byte-identical with the shipped
  Python-built `run/store_full/sparse.idx` (2548 entries).
- F1.2 (builder, second store): same on `run/store_e23` (if it carries a
  Python-built index; otherwise on a fresh synthetic store) — guards against
  a one-store fluke.
- F1.3 (lookup fix, isolated): strip the 12 chunk-first entries from a copy
  of the shipped index (pure every-1024); query a real boundary key (a key in
  chunk 8 whose greatest pure entry ≤ key sits in chunk 7) with the NEW
  binary → FOUND with byte-correct text. With a pure index, chunk crossing
  is the ONLY way to find it — this proves the `rl==0` fix itself.
  (Best-effort: also run the STALE `build/ingest_bin` on the same query;
  if it returns NOTFOUND, the before/after is demonstrated on the real bug.)
- F1.4 (behavioral, 1GB): 1,000 deterministic E1 keys via `bquery` against
  the Zag-built index → 1,000/1,000 FOUND, texts byte-identical to the
  Python-index run.
- F1.5 (determinism): `sindex` twice → identical SHA256.

**Cutover.** After F1.1–F1.5 pass: delete `extract/build_sparse.py` from the
branch (API tree deletion, race-free) and update `RUNBOOK_INGEST1GB.md` so
`ingest_bin sindex` is the sole index path. No Python in the final pipeline.

**Kill criteria.** Any F1 bar fails → the "fixed in source" claim does not
hold: find the real bug in Zag, fix, re-prove. The Python fallback is NOT
reinstated.

## Fork 2 — S5 into the scale learner

**Background.** Commit `2f61ed6a` delivered the canonical S5 store
(`ops/storage-compression/adopt/s5_store.zag`, incl. the `sc_seal_tail`
idempotency guard from `7303b6db`) and `s5_merge.zag` (merge-on-ingest gate,
proven byte-identical to the one-copy baseline in dedup/r2). The live scale
learner (`scale/driver/scale_learner.zag`) still uses a bespoke 24B-slot
store + dense index + write-only 16-word audit chunks (92 B/fact).

**Integration design (frozen).**
- ADOPT (not port): `@import("../../ops/storage-compression/adopt/s5_merge.zag")`
  at the top of `scale_learner.zag` (file-relative imports, proven pattern
  from `dedup/r2/dd_r2.zag`; pulls in `s5_store.zag` → R33 sha256/io).
- DELETE the learner's colliding bespoke storage: `ScStore`, `sc_store_init`,
  `sc_slot_chunk`, `sc_id2slot_get/set`, `sc_add`, `sc_recall`, and the
  `sc_alloc/sc_g32/sc_s32/sc_g64/sc_s64` copies (S5's are behavior-identical;
  the one signature widening `sc_g64(o:i32→i64)` was proven benign in
  PORT_EQUIV.md; the S1 parity run below re-proves it on the corpus path).
- KEEP, untouched in logic: the decision core (`sc_teach_value`: evidence →
  `sc_verify` → deliberate add), the 16-word deliberation audit (moved to a
  standalone struct — S5's `ScStore` has no audit fields), corpus handling,
  all measures. The learner's `sc_episode` is renamed `sc_audit_episode`
  (S5 owns `sc_episode`).
- Main teach path uses raw S5 `sc_add` (identity id==slot). Rationale: the
  learner's unit of knowledge is the (id → value) fact; duplicate VALUES
  across ids are distinct facts (e.g. two words of length 5). Routing the
  main path through the merge gate would fold them and break learning-read
  by id. The gate is compiled in and is the sanctioned ingest path for
  duplicate-bearing streams; the `chain` mode proves it.
- New argv mode `scale_learner chain <small|big>` (no corpus needed):
  - `small`: R2-B5 parity — 600 claims, cslots=64, merge ingest → 50 deletes
    → 30 revises → 20 re-adds (fresh) → 20 re-adds (folded) → `sc_seal_tail`
    ×2 → `sc_seal_final` → full verification. Must reproduce the R2 ok=1
    behavior on the integrated binary.
  - `big`: 1GB-scale — 40 lessons × 65,536 claims = 2,621,440 claims with a
    12.7% exact-duplicate profile (mirrors the 1GB pipeline's measured
    539,418/4,247,408 wiki-overlap rate); per-lesson merge gate (hmbits=17);
    one-copy baseline built in the same run (same stream, first-occurrence
    dedup, raw `sc_add`). Bars: per-lesson `sc_written_bytes` equal,
    end-of-ingest `sc_digest` equal, `events_n`==0 both, then mutations
    (delete/revise/re-add), double seal, and learning-read verification
    (every deleted id fails recall; every live id recalls ground truth;
    `sc_replay_check`==0, `sc_manifest_verify`==0, all 40 `mg_replay_check`==0,
    live-count arithmetic exact).

**Proofs (bars F2.1–F2.4).**
- F2.1 (no learning regression): S1 train run (N=2,400, P=1) with the
  integrated binary vs the committed `runs/s1_r*.log` outputs — every
  measure line identical (mastery, flaw 96/96, absorption, ops, digest);
  ONLY the `SCALE_MEM` line may differ (new S5 accounting, reported honestly).
- F2.2 (chain parity): `chain small` → ok=1 with the R2-expected counts.
- F2.3 (1GB-scale byte-identity): `chain big` → merged vs baseline
  byte-identity bars hold; full mutation chain verifies.
- F2.4 (determinism): every chain mode run twice → stdout SHA256 identical.

**Kill criteria.** Any F2 bar fails → integration is wrong: fix in Zag,
re-prove. No behavior change to the decision core is acceptable (F2.1 is
the tripwire).

## Scaling characterization (toward the 10GB program)

Measure on this VM (8 GB RAM, 2 vCPU); PROJECT to 10GB, do not run it.
The 10GB program is a separate running crew — its data/workdirs are untouched.

- **Throughput/fact and /GB**: wall time of `chain big` (timed, no timestamps
  in artifacts) + the 1GB ingest's measured window (blob_000000→blob_000011:
  131 s for 2,597,057 installs).
- **Memory headroom**: peak RSS sampler (`/proc/<pid>/status` VmHWM) during
  `chain big`; per-tier bytes from the 1GB report (blob 146 B/fact logical,
  S5 slot tier 5.53 B/fact, 16-word audit 64 B/fact write-only).
- **Chunk-count scaling**: S5 chunks = ⌈N/4096⌉, blob chunks = bytes/32 MiB,
  sparse entries = ⌈N/1024⌉ + chunks, seal cost O(chunks).
- **First-break projection**: evaluate each hard limit at 10× the 1GB
  numbers — znc 2^25 slice cap (merge-gate table ≤ ~20 MiB ⇒ hmbits ≤ 19 ⇒
  ≤ ~367K distinct values per gate instance ⇒ lesson-chunked gating is
  MANDATORY at 1GB+), the write-only 16-word audit (64 B/fact, 2×
  over-allocated), i32 id space (fine to 2.1B), sparse.idx streaming load
  (fine). Name the binding constraint with numbers.

## Commit plan

1. This prereg, alone.
2. Fork 1: `build/ingest.zag` fix + `RUNBOOK_INGEST1GB.md` update +
   `extract/build_sparse.py` deletion (+ proof logs under
   `knowledge/ingest_1gb/machinery/`).
3. Fork 2: `scale/driver/scale_learner.zag` integration (+ `BUILD.md` note).
4. `knowledge/ingest_1gb/machinery/MACHINERY_VERDICT.md` with all proofs.

All commits to `tnn-native-lab` via `~/workspace/commit_racefree.py`
(`TMPDIR=~/workspace/tmp_commit`); lab-relative paths not starting with
`docs/lab/`; never commit binaries or `.zagd`; never tree-replace.

## Out of scope (stated)

- The 1GB ingest's ported `sc_seal_tail` (build/ingest.zag:521) is UNGUARDED
  (predates the `7303b6db` port) — found during recon; flagged in the
  verdict for the 1GB track, not fixed here.
- E2/E3 eval ID remap, wiktionary completion, CAL-reject root cause: 1GB
  track's open items, untouched.
- 10GB data/workdirs: untouched.
