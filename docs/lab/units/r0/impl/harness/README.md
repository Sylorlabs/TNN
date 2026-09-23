# R0 Measurement Harness (native Zag)

Track R0, prereg FROZEN (Micah signed 2026-09-21). **HARD LAWS: pure Zag; zero RNG
in AI decision paths; byte-identical reruns.**

## What this is

The measurement infrastructure for the R31 native redo: audit ledger, probe/episode
framework, R-1 consequence-labeling reference, corpora pipeline, metrics-v1
evidence emitter, and the M8 determinism-gate armor + runner.

**What this is NOT:** it does not run the batteries. Battery crews build their own
binaries against these modules. This directory's `driver.zag` exposes only harness
selftests (`selftest`, `r1test`), a sample scorecard (`scorecard`), and deterministic
corpus ingest (`ingest`).

## Build

```sh
./build.sh            # compiles driver.zag -> /tmp/harness_bin
./build.sh /tmp/x     # custom output path
```

Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(flags: `--no-zagd --no-analyze --no-foreground-cache`).
Build outputs go to `/tmp` only — **never commit binaries, `.zagd`,
`.zag-cache`, or corpora.**

## Driver configs

One binary, `argv[1]` selects the config; `argv[2]` is the M8 perturb flag
`{0..4}` (default 0). Diff two runs per config for byte-identical verification.

| config | what it does |
|---|---|
| `selftest` | audit ledger (packed 64-byte layout) roundtrip + byte-spot check, episode mapping, STORESEQ store-pattern probe, probe-framework smoke, M8 captures |
| `r1test` | R-1 aggregation test: deterministic span grouping + label/purity math on hand-checked cases |
| `scorecard` | emits one sample metrics-v1 JSON scorecard (schema-validated) |
| `ingest <corpora_dir> <evidence_dir>` | fixed-order corpus ingest (prose first, code second) + hash records to the evidence log |

## M8 gate

```sh
./m8_gate.sh /tmp/harness_bin selftest   # 5 runs, perturbations 0..4
./m8_gate.sh /tmp/harness_bin r1test
```

PASS = all 5 runs exit 0, normalized stdout byte-identical, stderr
byte-identical, and `M8_STORE_IMAGE` / `M8_LEDGER` / `M8_ALLOC_TRACE` capture
lines identical. Any divergence = FAIL = DISQUALIFIED (fail-closed). See `M8.md`.

## Corpora (fetch on demand, never commit)

```sh
./fetch_corpora.sh /tmp/corpora
```

Fetches Gutenberg #100 (`pg100.txt`) and the pinned sqlite amalgamation
(`3530400`), verifies SHA-256. The committed hash record is
`units/r0/evidence/corpora.json` (the M-30 commitment); the files themselves are
never committed.

## Modules

| file | contents |
|---|---|
| `harness_common.zag` | env stream (fixed logged seed `20260921`, environment-input-only), `[]u8` LE cell helpers, allocators, IO |
| `audit.zag` | packed 64-byte audit entries, episode mapping, rolling ledger hash |
| `probes.zag` | episode kinds/routes, dose schedule, support-gap battery, near-twin probe, split/merge scenario |
| `r1_label.zag` | R-1 aggregation API (grouping + label/purity over battery-supplied observations) |
| `corpus.zag` | fixed-order ingest, 2²⁴ striping, hash records |
| `evidence.zag` | metrics-v1 scorecard emitter (exact normative keys, flags as strings) |
| `m8_armor.zag` | M8 armor: perturbations 0–4, allocator trace, captures |
| `driver.zag` | the four configs above |

Docs: `R1.md` (R-1 operational definition), `M8.md` (gate protocol).
Evidence: `units/r0/evidence/` (build, selftest, M8, scorecard, compiler bugs).

## Toolchain bugs this harness works around

- **ZNC-2026-09-19-001** (re-derived by the EXPLORE crew): 3+ sequential `[]i32`
  stores corrupt (deterministically wrong), in `[]i32` **and** `[]i64` multi-store
  contexts. `[]u8` stores are fully reliable.
- **ZNC-2026-09-21-004**: znc miscompiles indexed stores to `[]i32` heap slices at
  large indices (≥ ~61440); loads fine; `[]i64`/`[]u8` unaffected at the same indices.

Policy: every table with 3+ sequential indexed stores uses `[]u8`-backed
little-endian cells (`hc_le32_set/get`, `hc_le64_set/get`); the `STORESEQ` probe in
`driver.zag` readback-verifies every remaining store pattern against expected
values. Details in `units/r0/evidence/znc_bugs.md`.

## Frozen-bar notes (flagged, not silently resolved)

1. Local `PREREG_FREEZE.md` still says "PROPOSED — NOT FROZEN" and "Micah must
   approve/amend" on R-1; the parent/coordinator instruction is that Micah signed
   the freeze on 2026-09-21. The prereg file is not edited; the discrepancy is
   recorded in the verdict sheet.
2. The frozen R-1 text does not specify the concrete probe task or outcome
   encoding. This harness implements R-1 as an aggregation API over
   battery-supplied, preregistered probe observations — the battery manifest
   defines the probe before execution. An earlier draft's invented reference
   predictor / downstream predicate were removed.
3. `METRICS.md` ("flags as strings") and `ARM_INTERFACE.md` (JSON booleans, wider
   `m2_etc`) disagree on the scorecard schema. The emitter follows `METRICS.md`
   exactly; the divergence is recorded in the verdict sheet.
