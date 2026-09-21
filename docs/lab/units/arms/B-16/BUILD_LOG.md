# BUILD_LOG.md — B-16 build & test log

## 2026-09-20 — build

- Read frozen spec: prereg §3 mechanism ("Aligned blocks of size 16; chunk ID =
  index (no table)"), ALPHABET_A-F.md §B, ARM_INTERFACE.md, HARNESS_SPEC.md,
  AMBIGUITIES.md (A1–A17), PREREG §5/§6 via the interface.
- Classification: **non-ID layer** (ARM_INTERFACE.md §9 lists `b16` explicitly).
  No M1 swap probe (A15 N/A); M7 = N/A + re-read-bytes footnote.
- Verified corpora against `corpora/r1/MANIFEST.json` hashes: all 8 files
  match (prose.bin `a023115c…`, code.bin `b1dd5d74…`, churn/t1/t2/t3 all match).
- Implementation strategy: literal parameter port of the frozen b64 harness
  validator (`harness/b64/cl/arm.zag`, 1287 lines): `s/b64/b16/`, `s/B64/B16/`,
  `B16_CHUNK` 64 → 16, patch stride and all `bout`/`patch`/`ep2` buffers
  parameterized. Two structural changes forced by the znc 2^25 per-slice
  indexing limit (documented in ARM_SPEC.md §5 and AMBIGUITIES-B16.md):
  1. Audit ledger sharded: 8 × 262144 entries × 64B (16MB/shard), routed by
     `(led_n >> 18, (led_n & 0x3FFFF) * 64)`. New helpers: `led_base`,
     `led_op`, `write_led_file` (streams shards through one fd, ≤1MB writes),
     `led_chain` (sha256 of concatenated per-shard digests — documented
     deviation from the validator's sha256(whole ledger)).
  2. M8 store image: per slot-array ≤2^20 chunk digests (`hash_chunks`
     helper), chunk indices sequential across the 8 arrays in fixed order;
     chain = sha256(concat of digests) exactly as the validator.
- M8 ledger sized 2,097,152 entries (8 shards); measured need ≈ 950k.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (frozen). Build: `znc cl/arm.zag -o work/b16_bin` → 189,658 bytes, exit 0
  (71 analyzer warnings, all pre-existing style warnings also present in the
  validator's build; `--analyze-strict` not used, matching validator practice).
- Substrate: verbatim copies of `R33_NATIVE_SHA256_V2.zag`,
  `R33_NATIVE_IO_V1.zag` from `harness/b64/substrate/`.
- Memorizer control built from `harness/memorizer/cl/memorizer.zag` →
  `work/memorizer_bin` (46,574 bytes) for the M6 validity gate.

## 2026-09-20 — smoke tests

- `m1-1x-prose`: 100.0 / 100.0, 338,921 units, rc=0. Two-run diff: IDENTICAL.
- `run_battery.sh` first attempt: ALL legs rc=127 — root cause: harness
  `run_metric.sh` cds into per-run subdirs and execs the binary path verbatim,
  so relative paths fail. Re-ran with absolute paths. (Harness-usage lesson,
  not an arm bug.)

## 2026-09-20 — full 1x battery (round r1)

- Command: `run_battery.sh <abs>/work/b16_bin <abs>/work/memorizer_bin
  <abs>/corpora/r1 work/battery_r1`
- Result: **18/18 legs pass, BATTERY_RC=0.** Every leg rc1=rc2=0, stdout
  IDENTICAL across the two reruns (run_metric.sh diff gate).
- M8 gate: **M8GATE PASS** — 5 perturbations (clean/frag/aslr/starve/freelist)
  × 2 reruns, all rc=0. Independently verified: store_hashes.txt,
  store_chain.txt, ledger_chain.txt, alloc_trace.txt byte-identical across all
  10 runs (sha256 in docs/logs/m8_artifact_hashes.txt: each artifact hash
  appears exactly 10×). M8 stdout `M8,100.0,100.0,945680`; ledger.bin =
  60,523,520 bytes = 945,680 × 64B — complete ledger, zero truncation
  (8-shard capacity 2,097,152 entries was sufficient).
- Scorecard: assembled with a mechanical b16-labeled copy of the frozen
  `scorecard_assemble.py` (only the `"arm"` literal changed; byte-identical
  output to the harness assembler except the label — verified). Written to
  `docs/lab/units/arms/B-16/scorecard_r1_1x.json`.
- 10x: **not attempted.** The frozen r1 battery defines only 1x legs — no
  `corpora/r10` exists and no arm (including the validator) has a 10x row.
  Per C15, status is "not attempted (10x undefined in frozen r1 harness)",
  not "ATTEMPTED — FAILED". Forward caveat: the current binary's M8 ledger
  (2,097,152 entries) cannot hold a 10x M8 ledger (~9.5M entries); a 10x leg
  would need a shard-count bump + re-validation.
