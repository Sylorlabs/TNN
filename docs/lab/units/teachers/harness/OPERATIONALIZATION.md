# Track B Teacher Harness — Operationalization

**Date:** 2026-09-21  
**Status:** All 13 modes PASS; N=5 byte-identical; M8 perturbations byte-identical.

## What this is

The Track B teacher harness (`harness.zag`) is a deterministic, self-contained
test rig for the teacher/student protocol defined in `TEACHERS.md`. It exercises
the §P proposal codec, ingress validation, deliberation, verdicts, appeals,
hints, oracles, deferrals, tripwires, replay verification, and cost accounting
— all in pure Zag with zero RNG and no wallclock.

## Building and running

```bash
./run_harness.sh              # build + run all 13 modes
./run_harness.sh <mode...>    # build + run specific modes
./run_harness.sh --build-only # compile only
```

The build uses the lab znc toolchain:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## The 13 modes

| Mode      | What it proves |
|-----------|----------------|
| smoke     | Basic codec round-trip (§P encode/decode) |
| codec     | §P edge cases (bad magic/version/teacher/kind/span/checksum) |
| malformed | Malformed proposals rejected and logged (INGRESS_REJECT) |
| seq       | Seq gaps/duplicates detected (protocol violation) |
| tripwire  | Coverage/acceptance/maxconf tripwires fire correctly |
| replay    | Closed tapes replay bit-identically; tampered tapes fail |
| defer     | Deferral budget and forced deliberation work |
| hint      | Hints cite correctly; bad hints rejected |
| oracle    | Oracle queries and suspension work |
| det       | Determinism: two runs byte-identical (internal det5) |
| pertA     | Perturbation leg A (footer present) |
| pertB     | Perturbation leg B |
| cost      | Cost accounting (ledger/teacher/delib/appeal/defer words) |

## Determinism

- **N=5:** Five process-level `det` runs produce byte-identical output
  (sha256 `e43fc3c8...`, see `evidence/determinism_n5.txt`).
- **M8:** `MALLOC_PERTURB_=165`, env filler, and `setarch -R` all produce
  output byte-identical to baseline (see `evidence/m8_perturbations.txt`).

## Checksums

FNV-1a-64 is implemented identically in three places and verified to agree
bit-for-bit (see `evidence/fnv_checksum.txt`):
- Learner `pcodec.zag` (`p_fnv`)
- Fixtures345 `tape345.zag` (`t345_fnv`)
- Harness `harness.zag` (`fnv1a64`)

## Static guarantees

- **No RNG:** No `random`/`rand`/`srand` in code (see `evidence/static_scans.txt`).
- **No wallclock:** Tape uses logical ticks only.
- **No forbidden payloads:** §P proposals carry byte spans only (TEACHERS.md §P).

## Known compiler workarounds

The harness works around znc codegen bugs documented in `~/AGENTS.md`:
- **ZNC-007:** No consecutive same-size `as []i32`/`[]u32`/`[]u16` casts; use
  `[]u8` arenas with explicit little-endian accessors.
- **ZNC-012:** Never chain field access through a struct-stored pointer
  (`s.field.subfield`); copy to a local first.

## Session lifecycle

1. `sess_new()` — allocate arenas (ZNC-007-clean order).
2. `st_init()` + `st_set_stage()` — create the audit ledger.
3. `t_begin()` / `session_begin()` — write CONFIG/HEADER/STIMULUS events.
4. `gate_ingress()` — ingest proposals (validates §P, runs deliberation).
5. `session_turn()` — advance turn (for multi-turn tests).
6. `session_close()` — write TAPE_FOOTER (SHA-256 over unit records and
   ledger bytes, plus six verdict counters).
7. `replay_verify()` — re-run from the closed tape; must be bit-identical.

## Evidence

See `evidence/` for mode results, determinism, M8, checksums, and scans.
