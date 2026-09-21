# BUILD_LOG.md — Z1: Witness-bound cuts

## Procedural disclosure (2026-09-21)

ARM_SPEC.md was drafted AFTER the initial compilation, not before. The
spec-first requirement was not met. This is disclosed here; the document's
contents are reconciled with the implementation as of the 2026-09-21
correction pass (v2 probe claim removed; see §6).

## 2026-09-21 — Source construction

Built `cl/arm.zag` (1,639 lines, pure Zag) implementing the frozen Z1 mechanism:
witness-bound cuts with an eliminative challenge window (C1 word-split, C2
no-whitespace ±8, C3 uniform 16-byte neighborhood). One binary, `argv[1]` mode
dispatch. Persistent dense rows; row index == unit ID (ID arm).

Key structures: 28-field Z1 store (row arrays, 32B SHA-256 witnesses, version
stamps, challenge bits, 64B audit ledger entries, insertion queue, FNV
dedup table, allocation trace).

Modes: m1-1x-prose/code, m2-t1/t2/t3 (5), m3-1x, m4-1x-prose/code, m5-baseline,
m5-1x, m6-p2c/c2p-1x, m7-1x, m8-1x.

## 2026-09-21 — Compiler issues and fixes

Frozen toolchain: `znc_linux_x86_64_abed8aa1`.

1. **t_m8 "unknown struct field" (×9):** t_m8 used stale field names from a
   summary (`pidx`, `cbits`, `dtab`, `dval`, `atrace`); actual struct fields
   are `poff`, `witv`, `dedup` (single array), `trace`. Fixed to actual names.
2. **M8 ledger 38.4MB > 2^25:** reduced 600k→500k entries (32.0MB). z_led
   drops beyond capacity (LEDGER-BOUND).
3. **Row size 68B not 64B:** 7×u32 + 32B witness + 2×u32 (witv/witc). Fixed
   M5 slot accounting and M8 image capacity.
4. **Trace is text:** `alloc_trace.txt` writes the trace buffer verbatim
   ("A <n>"/"F <n>" lines, no addresses), not binary 12B entries.
5. **ZNC-2026-09-21-004:** `let s:T;` uninitialized struct rejected; z1_new
   uses a struct-literal initializer `Z1{...}` then `z1_init(&s)`.
6. Dedup table explicitly initialized to -1 (sentinel), per uninitialized-
   memory lesson.

All other ledgers audited: max is M8 at 32.0MB < 33,554,432.

## 2026-09-21 — Smoke tests

- `m1-1x-prose`: 100.0% recall, 100.0% boundary, 36,404 units, ID probe PASS
  (A15 provisional). 36k units vs 84k grid positions — the challenge window
  regretted ~57% of proposed cuts.
- `m1-1x-code`: 100.0% recall, 100.0% boundary, 68,491 units, ID probe PASS.

## 2026-09-21 — Bug fixes during 1x battery

1. **M2 ETC off-by-two:** `etc=e-2` reported 1 instead of 3 (criterion needs
   3 consecutive episodes). Fixed to `etc=e`. Battery restarted.
2. **M3 ID exhaustion (critical):** `next_id` was monotonic with no reuse;
   after 4,000 inserts the 4,000-cap store was permanently full, causing 0%
   fresh recall. Implemented freelist (`free_head`/`free_next` in Z1 struct):
   `z1_kill` and `z1_evict_oldest_unpinned` push killed IDs; `z1_insert`
   pops freelist first. Added `is_new` out-param to `z1_insert` so
   `z1_ingest` logs OP_ADD for freelist-reused fresh inserts (not just
   `id>=before`). Added liveness check in dedup-hit path (stale killed
   entries are ignored). M3 fresh recall went 0% → 100%.
3. **ARM_SPEC.md correction:** the v2 challenge-revision probe was documented
   as implemented but was absent from the source. Document corrected 2026-09-21;
   probe remains unimplemented (kill cell 2 BLOCKED).

## 2026-09-21 — Full 1x battery

Launched `run_battery.sh` in `~/workspace/z1_battery/` covering all 16 modes
plus M8 ×10 (5 perturbations × 2 runs). (Results appended below as they
complete.)

## znc warnings

71 analyzer warnings (A0102 ignored return values, A0107 false-positive dead-
loop notes on incrementing loops, L0010 string buffer notes). No errors.
Binary: 237KB.
