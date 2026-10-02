# znc compiler bugs — R0 harness record (2026-09-21)

Two distinct miscompiles of indexed stores are characterized. Both are
deterministic (byte-identical reruns), so determinism alone cannot detect them;
only readback against expected values can.

## ZNC-2026-09-19-001 — multi-store []i32/[]i64 corruption (EXPLORE crew)

- **Re-derived independently** by the EXPLORE crew within its first hour (see
  `docs/lab/units/r0/explore/02_ADVERSARIAL_PROBES.md`).
- **Symptom:** 3+ sequential indexed stores to `[]i32` corrupt — values read back
  deterministically wrong. Also observed in `[]i64` multi-store contexts.
- **`[]u8` indexed stores are fully reliable**, verified over 500 sequential cells
  (negatives and extremes exact).
- **Workaround (adopted):** `[]u8`-backed little-endian i32 cells
  (`a32_set`/`a32_get` pattern); all EXPLORE probes rebuilt on it, passing
  byte-identical.

## ZNC-2026-09-21-004 — large-index []i32 store fault (harness crew)

- **Symptom:** indexed stores to heap-backed `[]i32` fault near high indices
  (>= ~61440); the same-index **loads** work; `[]i64`/`[]u8` stores at the same
  indices are unaffected.
- **Workaround (adopted):** large tables moved to `[]i64`; 10MB `[]u8` indexed
  store/load verified passing.

## This harness's audit outcome (coordinator hardening, 2026-09-21)

The harness sources were audited for 3+ sequential `[]i32`/`[]i64` stores:

| Site | Pattern found | Disposition |
|---|---|---|
| `audit_append` (3 scalar + 2×5-loop + 3 scalar `[]i64` stores) | 3+ sequential `[]i64` stores | **Rewritten** to `[]u8` LE cells (also fixes the 64-byte packed layout) |
| `audit_get` readback loop (16 sequential `[]i32` stores) | 3+ sequential `[]i32` stores | **Caught live**: selftest failed with `e0[12]=65536` instead of `204`; **rewritten** to `[]u8` LE cells; selftest now `fails=0` |
| `r1_enumerate` slot insert (4 sequential `[]i64` stores) | 3+ sequential `[]i64` stores | **Rewritten** to `[]u8` LE cells (slot stride 24 B) |
| `r1_test` manifest arrays (`[]i32`, 4 sequential stores) | 3+ sequential `[]i32` stores | **Rewritten** to `[]u8` LE cells; `r1_aggregate` takes cell arrays |
| `m8_armor` trace/block-header writes (2 sequential `[]i64` stores) | 2 sequential (under threshold) | **Kept + proven**: STORESEQ probe readback-verifies the exact pattern |
| `hc_alloc_*` zeroing loops (1 store/iteration) | single-store loops | **Kept + proven**: STORESEQ probe verifies at large index |
| `chunk_addrs`/`ep_bounds` (`[]i64`, single accesses) | no sequential pattern | Kept |

**Policy going forward:** every table with 3+ sequential indexed stores uses
`[]u8`-backed little-endian cells (`hc_le32_set/get`, `hc_le64_set/get` in
`harness_common.zag`). The `STORESEQ` probe in `driver.zag` readback-verifies
every remaining store pattern (LE roundtrips incl. extremes, 500 sequential
cells, 2-sequential `[]i64`, large-index single-store loop) against expected
values on every `selftest` run — currently `STORESEQ,fails=0`.

Note: during this work `/tmp` (512MB tmpfs, shared) filled to 100% from other
crews' corpora; the znc binary output stayed byte-identical across builds
(sha256 `da58854f…` reproduced), ruling out build-environment corruption as a
cause of the observed miscompile.
