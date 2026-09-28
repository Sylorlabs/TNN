# Arm E — Build Log (Track A, Round 1)

Date: 2026-09-21. Author: Arm E crew. All work in
`~/workspace/tnn-lab/units/arms/E/`; docs in `~/workspace/docs/lab/units/arms/E/`.

## Source provenance

- `cl/arm.zag`: single-file arm, written fresh for E (STORE family, ephemeral
  chunks). No B-64 code was copied into the arm itself.
- `substrate/`: the two R33 substrate files (`R33_NATIVE_IO_V1.zag`,
  `R33_NATIVE_SHA256_V2.zag`) copied verbatim from B-64 and MD5-verified
  equal (IO `19bdcc5212998682ed733b43c09a23d0`, SHA256
  `70e1be7d0c7caf2f9f037112ce3b2f03`).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## Build sequence

1. **Initial build** — compiled clean (warnings only). 1x battery: first
   invocation used relative binary paths and was invalid (every leg rc=127);
   rerun with absolute paths → 18/18 legs, M8GATE PASS.
2. **Four-shard arena patch** — the arena (`ar0/ar1`) was clamped to 2 shards
   and the 10x M5 run needed 3 (panic at 95MB code corpus). Extended to
   `ar0..ar3` with a shared `ar_shard()` selector; rebuilt `work/e_bin`.
3. **Four-shard ledger patch** — same latent bug in the audit ledger
   (`led0/led1`, clamped to 2 shards): a 71MB 3-shard ingest panicked when
   ledger entries spilled past shard 1. Extended to `led0..led3` with a
   `led_shard()` selector; applied to `e_led`, `led_op`, `write_ledger`, the
   t_m8 ledger hash loop, and the M5-baseline touch code. Both patches are
   behavior-preserving for ≤2-shard cases (shard 0/1 selection logic
   unchanged; shards 2/3 empty).
4. **Final binary** — rebuilt after both patches; the full 1x battery was
   rerun against it (18/18, M8GATE PASS) so all evidence is from one binary.
   A transient `e_bin` write hiccup during one rebuild was resolved by
   building to a fresh path and moving it over; MD5/size checked before use.

## 10x corpora

Built with the frozen `build_10x.py` under `work/r10`:
- prose 10x: 54,227,210 bytes (tile SHA matches builder expectation)
- code 10x: 95,153,410 bytes (tile SHA matches builder expectation)

## Evidence runs (final binary, each 10x leg ×2, byte-identical stdout)

| leg | run 1 | run 2 | stdout |
|---|---|---|---|
| E m1-10x-prose | 100.0/100.0, 847,301 u | 100.0/100.0, 847,301 u | IDENTICAL |
| E m1-10x-code | 100.0/100.0, 1,486,773 u | 100.0/100.0, 1,486,773 u | IDENTICAL |
| E m5-10x | slot_table 91,679,710 B | slot_table 91,679,710 B | IDENTICAL |
| E m5-baseline-10x | ok | — | — |
| B-64 m1-10x-prose | 100.0/100.0, 847,301 u | 100.0/100.0, 847,301 u | IDENTICAL |
| B-64 m1-10x-code | 100.0/100.0, 1,486,773 u | 100.0/100.0, 1,486,773 u | IDENTICAL |
| B-64 m5-10x | slot_table 33,167,612 B | slot_table 33,167,612 B | IDENTICAL |

B-64 10x measurements were made with a measurement-only B-64 variant
(`work/b64_10x/`, uncommitted) that preserves B-64's reference/re-read
semantics while adding large-file/sharded support; the variant's own ledger
received the same 4-shard fix. It is evidence tooling, not a new arm.

## Kill calculation

- Stored bytes (M5 `m5_slot_table_bytes`, arm store region per A16):
  E = 91,679,710 B; B-64 = 33,167,612 B.
- Ratio = 91,679,710 / 33,167,612 = **2.764×** ≥ 2×.
- Equal M1 at 10x: both arms 100.0% recall / 100.0% boundary on BOTH corpora
  (prose 847,301 units, code 1,486,773 units).
- Per-source-byte (prereg §5 C1 comparison column): E 1.69 B/B vs B-64
  0.61 B/B — same 2.764× ratio. E also exceeds the M5 bar (≤1.5× source).
- The audit ledger is excluded from "stored bytes" per prereg §5 M5 (audit
  entries/bytes are a separate cost column); both arms' ledgers are byte-
  comparable anyway (same entry count, 848,301).

**Criterion fires → VERDICT: KILLED.**

## Determinism

- 1x battery: all 18 standard legs ran twice with byte-identical stdout;
  M8 gate (5 perturbations) PASS on the final binary.
- 10x legs: each ran twice, stdout byte-identical (table above).

## Known notes

- The 1x M8 gate passes; the M8 ledger-hash implementation was reviewed
  during the ledger-shard patch (hash loop walks all ledger shards).
- `work/shardtest/` holds the 71MB 3-shard reproducer used to isolate the
  ledger-shard panic (not evidence, kept for the record).
- Same-key re-ingest revives the existing entry (documented in ARM_SPEC §5
  as same-provenance revival, not dedup); 10x tiled ingests use distinct
  keys and are independent copies — the kill number is unaffected.
