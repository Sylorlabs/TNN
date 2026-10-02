# BUILD_LOG.md — L1: Absolute Position IDs

## Toolchain
- Frozen compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (exact filename; no other znc used).
- Sources: `cl/arm.zag` (+ `substrate/R33_NATIVE_SHA256_V2.zag`,
  `substrate/R33_NATIVE_IO_V1.zag`, imported bare per Zag rules).
- `znc check cl/arm.zag`: passes (warnings only: ignored-return-value
  lints, string-buffer-leak lints on intentional print helpers, one
  dead-loop false positive on the chunked file writer).
- Native build: `znc cl/arm.zag -o <workdir>/l1_arm` (~24 s).

## Build issues and fixes (all in-arm, no harness changes)
1. `ns_hex` arity: the L1 substrate shim exposed 1-arg `ns_hex` (returns a
   fresh slice); the M8 code was written against the 2-arg b64 form. Fixed in
   the shim: `ns_hex(bytes, out)` writes hex into the caller's buffer.
2. Native codegen `unknown struct field`: `img_at` (M8 image cursor) and the
   allocation-trace fields were referenced but not declared. Added
   `img_at:i32` to `struct L1`; the trace fields were misnamed `atrace` /
   `atrace_n` — corrected to the real `trace` / `trace_n`. No silent
   harness or compiler workarounds.
3. t_m8's `alloc_trace.txt` slice was `trace[0..trace_n]` (variable-length
   text log), not a fixed 8-byte record layout.

## Determinism posture
- Zero RNG in any AI decision path: slot placement is a deterministic
  golden-ratio hash of the position ID; eviction is FIFO over the insertion
  queue; the M1 swap-probe schedule is `i % ceil(n/64) == 0` with target
  `(i+1) % n`; M7 lookups use the `(l*37) % n` stride; defect schedules are
  fixed index lists. The only hash used is SHA-256 for M8 artifacts.
- Byte-identical reruns are asserted by the M8 gate (5 perturbations × 2
  runs, every required artifact compared byte-for-byte by `m8_compare.py`).

## znc issues encountered
- None beyond the above (both were arm-source bugs, not compiler bugs).
  The known ZNC-2026-09-21-002/003 constraints were respected from the
  start: no slice→`*u8` casts, no slice larger than 2^25 bytes is indexed
  (the M8 image is ~28 MB < 33,554,432), large-struct array fields are
  aliased to locals before indexing.

## Scorecard assembly (harness gap, documented not patched)
- `units/arms/harness/scorecard_assemble.py` is B-64-specific: it hardcodes
  `"arm": "b64"`, hardcodes the M1 ID probe as N/A, and always assembles M7
  as N/A. The frozen harness was deliberately NOT modified. L1 ships
  `evidence/assemble_l1.py` (evidence-side, outside the frozen tree), which
  parses the arm's own `METRIC_JSON` lines and TAG lines and writes an
  identical-schema `scorecard.json` with the real L1 values, including the
  provisional M7 row and the M1 `m1_id_probe` result.

## Test procedure
1. Targeted smoke: `m1-1x-prose` and `m4-1x-code` on the real corpora;
   verify recall ≥ bar, probe=PASS, eternity holds.
2. Full 1x battery via the frozen `run_battery.sh` (unaltered) in a
   `~/workspace` workdir (never `/tmp`: 512 MB tmpfs).
3. M8 gate via the frozen `m8_gate.sh` (unaltered).
4. 10x only if every 1x bar passes: modes are the 1x names with `1x`→`10x`;
   the binary reports `"scale":"10x"` from the mode string itself.
   (10x corpora are built by the coordinator's `build_10x.py` on demand.)

## 2026-09-21: M8 panic fixes and dispatch corrections

### M8 slice-index panics (three root causes)
1. **Double segment allocation**: `ensure_stream_segs` was called explicitly
   in t_m8 AND internally by `ingest_all`, allocating 33 segments against a
   21-segment arena. `seg_new` returned -1, producing negative segment IDs
   and a slice panic. Fixed by making `ensure_stream_segs` idempotent
   (early return if `seg0[stream] >= 0`).
2. **Undersized image buffer**: `fixed` used `ins*4` (242,409×4) but the
   insertion queue is `ins_cap*4` (262,144×4), leaving the image 78,940 bytes
   short. The final `img_append_seg` wrote past the end. Fixed by using
   `ps.*.ins_cap*4` in the `fixed` computation; also added bounds guards to
   `img_append_seg`.
3. **Artifact file bugs**: the chain hash was written to `store_hashes.txt`
   instead of `store_chain.txt`; `write_hex_line` append mode failed silently,
   leaving only chunk0. Rewrote to accumulate all 27 chunk lines in memory
   and write once; chain now goes to the correct `store_chain.txt`.

### Dispatch corrections
- Updated `main` to the frozen canonical mode names: `m2-t1-prose`,
  `m2-t1-code`, `m2-t2-prose`, `m2-t2-code`, `m2-t3-1x`, `m6-p2c-1x`,
  `m6-c2p-1x`, `m7-1x` (previously used non-canonical `-1x-` infixes and
  omitted the M2 code variants).
- t_m6 now emits the interface fields `rec_tenths`, `bnd_tenths`,
  `rev_tenths`, `tax_tenths` alongside L1-specific kill/pin metrics.

### M8 gate result
- 5 perturbations × 2 reruns = 10 runs, all byte-identical.
- `m8_compare.py`: **M8GATE PASS**.

### M5 dimensional fix (2026-09-21)
- `budget` was `(content_bytes*2)/100` (bytes) while `spent` counts units —
  dimensionally inconsistent comparison. Fixed to `total + total/50` (units
  + 2% headroom). ARM_SPEC.md §3 updated.
- t_m5 now emits all six frozen A16 fields: `m5_units_learned`,
  `m5_source_bytes_learned`, `m5_slot_table_bytes`, `m5_ledger_bytes`,
  `m5_ledger_entries`, `m5_corpus_buffer_bytes`.
- t_m5b rewritten: allocates and fully touches the exact corpus-derived shape
  (cap, ins_cap=262144, ledger, arena segs) — no hardcoded 250000/50000/32,
  no wall-clock in output. Emits `m5_baseline: "ready"` marker.
- t_m6 now emits interface fields `rec_tenths`, `bnd_tenths`, `rev_tenths`,
  `tax_tenths` alongside L1-specific kill/pin metrics.

### M6 stale-buffer leak false positive (2026-09-21)
- The leak probe compared `bout` bytes after a BLOCKED recall (rl==-1) against
  the corpus. `bout` still held stale bytes from the pre-kill verification,
  so all 200 kills falsely reported as leaks (d1=200, tax=0.0).
- Fixed: leak is only checked when recall SUCCEEDS (rl!=-1). Blocked recall
  cannot leak by definition. After fix: d1=0, tax=100.0, all 200 kills
  properly blocked.
