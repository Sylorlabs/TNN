# PREREG — KB-CONTROL CREW A: root-cause audit + write-path map

**Crew:** KB-Control Crew A. **Date:** 2026-09-23. **Status:** FROZEN (committed before any reproduction results).
**Branch:** `tnn-native-lab` (sylorlabs/TNN). **Workdir:** `~/workspace/kb_control/crewA/`.
**Deliverables:** `ROOTCAUSE_A.md` + pure-Zag reproducer, under `docs/lab/knowledge/kb_control/crewA/`.

## 1. Background (from the frozen 1GB-ingestion FINDINGS, commit `118251c5`)

Two defects, both in the blob writer of the ingest port (`knowledge/ingest_1gb/build/ingest.zag`):

- **D1 — padding miscount.** `igb_append` never counts inter-chunk zero-padding in `b.*.total`. Each 33,488,896-byte blob chunk ends with 40–467 bytes of padding that `total` ignores → slot→blob offsets wrong for 92.4% of slots (2,398,865, chunks 1–11) on the 1GB store; the red team's independent 260k-slot census found 100% of post-first-chunk slots wrong.
- **D2 — silent cross-fact destruction (RT-G3).** A pre-boundary `revise` "succeeds" but silently destroys an unrelated fact (`rtg:0259999` → NOTFOUND) — padding-blind `bb.used` overwrites the last 126 data bytes of the final blob chunk.

Micah's ruling: silent cross-fact destruction is stingy-LLM behavior and must be killed by construction. TNN must consciously control its knowledge base.

## 2. Committed hypotheses (falsifiable, stated before reproduction)

- **H1 (D1 mechanism).** In `igb_append`, the returned/stored global offset is `off = b.*.total`, and `b.*.total` is advanced by `reclen` only. On chunk rollover the branch zero-pads `IG_BLOB_CHUNK - used` bytes and flushes, but never adds the padding to `total`. Therefore `total` lags the true on-disk end by the accumulated inter-chunk padding, and every slot offset recorded after the first rollover is short by exactly that accumulated padding.
  - *Falsifier:* a reproducer using the verbatim `igb_append` formulas shows any post-first-boundary slot whose recorded offset matches true on-disk geometry.
- **H2 (D2 mechanism).** In `ig_revise`, the blob tail state is reconstructed as `bb.used = (btotal % IG_BLOB_CHUNK) as i32`. Because `btotal` excludes all inter-chunk padding, this undercounts the true tail usage of the final chunk by `(accumulated_padding mod IG_BLOB_CHUNK)` bytes (126 in the red-team run: computed 1,499,994 vs true 1,500,120). `igb_append` then writes the revised record at that too-small `used`, overwriting the last 126 real data bytes of the final chunk — destroying the tail fact while reporting success.
  - *Falsifier:* revising a pre-boundary slot leaves every other fact's bytes bit-identical (chunk-image diff empty in the real-data region).
- **H3 (blast-radius asymmetry).** The same padding-blindness makes post-boundary revises fail closed (`revise: old parse failed`, store untouched), pre-boundary revises succeed-but-destroy, and deletes always succeed (delete never reads a blob offset). Query is unaffected because `ig_sindex` writes geometric offsets (`ci*CHUNK + off`).
  - *Falsifier:* any of those three behaviors inverts in the reproducer.

## 3. Reproduction method (pre-committed)

Build `kb_repro.zag`: a minimal, self-contained, pure-Zag program implementing the
blob-writer formulas **verbatim** from `build/ingest.zag` (`igb_append` rollover/total
logic; `ig_revise`'s `bb.used` reconstruction; the `[1B kind][4B id LE][2B klen BE][4B tlen BE][key][text]` record layout), parameterized to `CHUNK=4096` so ≥2 boundaries are crossed quickly. Geometry is a parameter, not the mechanism: chunk size changes only the padding magnitudes, not the formulas.

Deterministic records: `N=100`, key 8 bytes, text 90 bytes → `reclen=109`; 37 records/chunk, 63 bytes padding per rollover. Expected: chunk 0 = ids 0–36, chunk 1 = ids 37–73, chunk 2 = ids 74–99; accumulated padding after 2 rollovers = 126.

Protocol:
1. Append 100 records, recording each returned offset.
2. **Offset census:** parse the record header at each recorded offset; count slots whose stored id ≠ expected (predict: ids 0–36 → 0 wrong; ids 37–99 → 63/63 wrong = 100% post-boundary).
3. **Geometric verification (sindex-style walk):** parse all records at true `chunk*CHUNK+in` offsets; all 100 must parse (predict: yes — proves the bytes are fine, only the accounting is wrong).
4. **Revise** a pre-boundary slot (id=5) via the buggy tail reconstruction; expect rc=0.
5. **Post-revise verification:** id=5 returns the new text at its new offset; geometric re-walk of the final chunk; diff the final chunk image before/after in the real-data region (predict: exactly 126 bytes changed, covering the tail fact's header → tail fact id=99 no longer parses = NOTFOUND).
6. Evidence: run the binary twice from clean outdirs; evidence logs must be byte-identical (SHA256 compared); run-2 log embeds the SHA256 of run-1 log (hash chain).

Zero RNG anywhere. No timestamps, no pointers, no ASLR-dependent content in evidence.

## 4. Write-path inventory to map (complete list, each classified)

For each path in `build/ingest.zag`: (a) does offset/length accounting include padding?
(b) is there a bounds check? (c) fail-closed vs silent on violation?

1. `igb_append` (ingest install path via `ig_process_lesson`; revise path via `ig_revise`)
2. `igb_flush_full` (chunk file write)
3. `igb_finish` (final pad + flush)
4. Chunk-rollover branch inside `igb_append`
5. `ig_revise` (tail-state reconstruction, append, chunk rewrite, overrides, flags, rechain, reseal, store save)
6. `ig_delete` (flags-only; blob untouched — verify)
7. `ig_ovr_save` / `ig_ovr_load` (overrides.dat read-modify-write)
8. `ig_store_save` (persists `blob_total`/`blob_nchunk`/`blob_recs`)
9. `ig_store_load` (trusts persisted tail)
10. `sc_seal_tail` / `sc_seal_final` (double-seal idempotency; RT-H OOB)
11. `sc_compact_and_seal` (slot-chunk compaction — does it touch blob bytes?)
12. `ig_sindex` (sparse.idx writer — geometric offsets; verify claim "unaffected")
13. `ig_open_write` (O_TRUNC vs O_EXCL — silent-failure audit per AGENTS.md lesson)
14. Checkpoint/resume: assert presence or absence in the port (the stale-checkpoint incident was in Wiktionary extraction, not this binary — confirm)
15. Oversize-record guard: is there any check that `reclen <= IG_BLOB_CHUNK` before the `cur[used..]` writes?

## 5. Acceptance bars

- **A1.** Reproducer builds with the pinned toolchain (`znc_linux_x86_64_abed8aa1`), runs rc=0.
- **A2.** ≥2 runs byte-identical: SHA256(evidence_run1) == SHA256(evidence_run2); hash chain recorded.
- **A3.** Census: 0/37 pre-boundary slots wrong, 63/63 post-boundary slots wrong.
- **A4.** Pre-boundary revise rc=0; revised fact returns new text; ≥1 previously-intact unrelated fact becomes unparseable (NOTFOUND); chunk-image diff shows exactly the predicted clobber span (126 bytes) in the real-data region.
- **A5.** `ROOTCAUSE_A.md` delivered: exact arithmetic error (which counter, which line of logic), the full classified write-path table from §4, and for each unsafe path whether "count padding in `total`" fixes it or something more is needed.
- **A6.** No binaries, no `.zagd` caches committed; lab-relative paths only.

## 6. Kill criteria

- If A4's destruction check fails (no unrelated fact harmed), H2 is FALSIFIED: report it as falsified, do not declare victory, do not reframe.
- If any §4 path cannot be classified from the source, mark it UNKNOWN with the exact reason — never guess.
- If the reproducer's formulas diverge from `build/ingest.zag`, the reproduction is void: re-verify by diffing the formula blocks.

## 7. Scope limits

- Root-cause audit + write-path map ONLY. No fixes land in this crew's commits (a fix crew consumes `ROOTCAUSE_A.md`).
- The red-team families RT-A–RT-F/RT-H (gate truthlessness, forged provenance, seal) are out of scope except where they share a write path (RT-H double-seal is in §4 because `sc_seal_final` is a write path).
- The `s5_store.zag`/`s5_merge.zag` canonical store (machinery fork 2) is out of scope unless its blob writer is the same code — the shipped CLI path under audit is `build/ingest.zag`.
