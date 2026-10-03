# BUILD_LOG.md — B-8 (Arm B-8: fixed 8-byte chunks)

## 2026-09-21 — setup
- Created `units/arms/B-8/{cl,substrate,run,docs}`.
- Copied frozen substrate verbatim from `harness/b64/substrate/`
  (`R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag`).
- Copied `harness/b64/cl/arm.zag` → `B-8/cl/arm.zag` as the starting point.
- Verified all 8 corpus files against `corpora/r1/MANIFEST.json` sha256 — all OK.
- Read: ALPHABET_A-F.md (B section), ARM_INTERFACE.md, HARNESS_SPEC.md,
  CORPORA.md, AMBIGUITIES.md (A1–A17), b64 scorecard, B-8.json brief.

## Design decisions (all literal-reading; ambiguities logged, never reinterpreted)
1. **Unit = 8B chunk everywhere** (M1/M2/M3/M4/M5/M6/M8). Chunk ID = index,
   unit ID = `(corpus<<24)|chunk_index`. Rationale: minimal faithful adaptation
   of the validated reference; the alternative (64B span entries with 8-ID
   lists) would make B-8 metrically indistinguishable from B-64 and void the
   granularity experiment the arm exists to run.
2. **Non-ID-layer classification confirmed** (§9): pure arithmetic resolution,
   no ID table. M1 swap probe N/A; M7 N/A + re-read bytes.
3. **M3 (A-B8-1):** rig's 64B fixture spans ingested as 8 chunk units each;
   C_M3=4000 slots → eviction pressure in phases 1 and 3 (FIFO-oldest-unpinned,
   V pinned/safe). Freeze flag expected to fire mechanically → M3 cell 0.
   Logged in ARM_SPEC §6; shared AMBIGUITIES.md NOT edited (frozen harness
   file — flagged for the coordinator instead).
4. **Sharded ledger** (524288-entry shards, 8 max) — B-8's ADD volume exceeds
   2^25 per slice. `ledger.bin` = shard concatenation; M8 `ledger_chain` =
   sha256 of concatenated per-shard sha256s (self-comparison only, C13).
5. **M8 store hashing streamed** in 1MB chunks over the region concatenation
   (image ~73MB > 2^25) — same chunk boundaries as a materialized image.
6. M2 ledger cap kept at 64 entries exactly as the reference (unscored mode).
7. No stats/use_count array (drives no decisions; M3 reported from ledger+probes).

## 2026-09-21 — build
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (frozen).
- `znc cl/arm.zag -o run/b8_bin` → OK (analyzer warnings only, same classes
  as the reference: A0102 ignored return values, no errors).
  - Note: first attempt with a relative `-o run/b8_bin` produced no binary
    (rc=0, no error); absolute `-o` path worked. Build note, not an arm issue.
- Built memorizer for the M6 gate: `znc harness/memorizer/cl/memorizer.zag
  -o run/memorizer_bin` → OK.
- Smoke tests: `m2-t3-1x` → ETC=1, ep0=0.0, final 100.0/100.0, rc=0.
  `m1-1x-prose` → 100.0/100.0, 677,841 units, 14.4s, rc=0.

## 2026-09-21 — M3 adjudication (follow-up crew)

Question: is the r1 M3 result (67.6, FROZEN-UNDER-PRESSURE) real or a build defect?

- **Protocol verified against the frozen prereg** (PREREG_FREEZE.md, commit
  b0b9140c0eda): the churn fixture is exactly 7,000 64B spans (3,000 + 4,000),
  so the prereg's churn-phase "units" are the fixture's 64B spans; the
  500-span fresh sample implements the spec literally. No protocol defect.
- **Rebuilt** `cl/arm.zag` with the frozen toolchain
  (`znc_linux_x86_64_abed8aa1`); **two independent M3 runs, byte-identical**:
  `M3,100.0,67.6,64050,50,FROZEN-UNDER-PRESSURE`.
- **Eviction-victim trace** (50,000 victims, debug build only): block-level
  FIFO confirmed — phase-3 victims are chunks 24000–50999 + 2,000
  hash-scattered in 51000–53999; live set 51001–55999. The 67.6 vs the
  insertion-order ideal 75.0 is a within-block hash-scattering wart (stale
  slot-queue entries) — verdict-irrelevant, since both sit below the 80% bar.
- **Adjudication: REAL.** The freeze is genuine granularity/capacity pressure
  (4,000 slots, 1,000 pinned V, 4,000 fresh chunks demanded by the sample).
  Production source left untouched. Evidence: `run/adjudication_m3.md`.
- **Retirement fires:** B-16 strictly dominates B-8 on M1/M2/M3 both corpora
  (verified from B-16's scorecard: M1/M2 ceiling, M3 100.0/100.0 CLEAR).
  **Verdict: RETIRED (KILLED at size level).** Death certificate:
  `docs/RETIREMENT.md`.

## 2026-09-21 — full 1x battery (prior crew; resumed, not redone)

- Driver: `run/run_battery_b8.sh` (frozen `run_metric.sh` + `m8_gate.sh`;
  assembler = frozen `scorecard_assemble.py` with only `"arm":"b64"`→`"b8"`
  patched, kept at `run/scorecard_assemble_b8.py`).
- Workdir: `run/battery_r1/` (binaries, `.zagd`, workdirs never committed).

### Results

18/18 legs passing; M8 gate PASS. Scorecard: `run/battery_r1/scorecard_r1_1x.json`.
M1 100/100 both corpora (677,841 / 1,189,418 units). M2 ETC=1 every tier ×
corpus, final 100/100, ep0=0.0. M3: survival 100.0, fresh 67.6,
FROZEN-UNDER-PRESSURE → cell 0 (adjudicated real, see above). M4 100/100 both
classes both corpora, kill 0. M5: memory 6.065 B/B (bar 1.5× FAIL), audit
128.2 entries/KB (bar 10 FAIL) — honest granularity cost. M6 100/100/100 both
directions, validity gate PASS. M7 N/A (no ID layer). M8: M8GATE PASS.
