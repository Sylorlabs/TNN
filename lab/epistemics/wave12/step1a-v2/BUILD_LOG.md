# BUILD_LOG — Step 1a v2 (RNGSCAN-2026-09-20-v2) rebuild

Date: 2026-09-20. Rebuilder: step-1a-rebuilder subagent (this session).
Prereg: `PREREG_NO_RNG_AUDIT_V2.md`, frozen and committed BEFORE any checker
code at `0b29c17d834f22873fdb78d11ac04f094fe5952c`
(branch `tnn-native-lab`, path `docs/lab/wave12/step1a-v2/`).
v1 (`rngscan.c`) is dead: 19/20 plants caught; plant20 (`get_env_flag`)
passed only because v1's checker omitted frozen rule 4.5's `env_` match.

## Purity accounting (prereg §10)

- Checker, modules, harness: pure native Zag. No RNG anywhere.
- Shell: `runner/run_audit.sh` is the preregistered deterministic runner
  (§7.5) — byte-compare replay glue + checker invocation, not checker logic.
- Python use (allowed only as GitHub commit glue / log analysis):
  1. `/tmp/prereg_blob.py` — encoded the prereg blob for the GitHub API
     commit (ephemeral, /tmp only).
  2. Python one-liners to parse GitHub API JSON responses during commit.
  3. Python `json.load` one-liners to verify attestation JSON fields in the
     dirty/clean rounds (log analysis, read-only; did not touch the audit).

## Capability spike (/tmp/spike, NOT committed)

Verified before writing the checker: native Zag file reading, direct
binary-byte scanning, `ns_sha256` == `sha256sum`, slice syntax `[0..end]`,
`nio_alloc` returns `[]u8` only (casts needed for typed tables, whose `.len`
stays byte-sized — capacities tracked manually), `_zag_arg` non-owned,
`ns_hex` allocates fresh (must free). Spike binary sha256 observed:
`e2f67e4d54df2ff4700f43dc7ffa3564555ab9dfe5c9b21c4fec6583014b1627`.

## Substrate (copied, unmodified)

- `substrate/R33_NATIVE_SHA256_V2.zag` sha256
  `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf`
- `substrate/R33_NATIVE_IO_V1.zag` sha256
  `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`

## Pre-freeze bugs found and fixed (checker was editable at this point)

1. `index_lines` dropped the end sentinel `loff[nlines]=b1`; `get_line(k)`
   reads `loff[k+1]` for the last line → "line read error", RC=2.
   Fixed by writing the sentinel inside `index_lines`.
2. `write_file` fail-closed on bare filenames (no `/`); `read_file` already
   fell back to `"."`. Fixed `write_file` with the same fallback.
3. Arity: `scan_uninit` called with 16 args, takes 15 (stray `raw1`).
4. Cast-slice capacity audit: `loff.len` is byte count; all `[]i32` table
   guards use element counts (e.g. cap 200001 for the 800004-byte line
   table). One real overflow risk caught in review of `build_lines`
   (superseded by `index_lines` with explicit cap param).

All fixes pre-date the scored rounds and the freeze.

## Dirty round (checker unfrozen→ then frozen; rounds run on final source)

Modules: `modules/dirty{1..5}_*.zag` + `modules/harness.zag` (shared clean
main). Fixtures: `fixtures/state1.bin` (1 MiB `S`), `fixtures/state2.bin`
(1 MiB `T`), `fixtures/input.bin` (64 KiB `I`) — fixed patterns, no RNG.
Runner: `runner/run_audit.sh` (RUNAUDIT-2026-09-20-v1).

| module | verdict | hits | rules named |
|---|---|---|---|
| dirty1_urandom | FAIL (RC=1) | 4 | 4.1/4.6 literal + binary bytes; 4.6 object open(2)+openat(257) with /dev/urandom |
| dirty2_clock | FAIL (RC=1) | 2 | 4.2 `_zag_raw_syscall(clock_gettime=228)`; 4.6/4.2 object imm 228 |
| dirty3_uninit | FAIL (RC=1) | 1 | 4.3 read of `s[uninit]` before init |
| dirty4_hash | FAIL (RC=1) | 6 | 4.4 `hashmap` ×6, no 4.3 false positives |
| dirty5_aslr | FAIL (RC=1) | 3 | 4.5 `_zag_slice_ptr` + pointer cast; REPLAY divergence (genuine: ASLR bits in output) |

5/5 dirty plants caught, each naming the expected rule family. Attestations
in the round logs (ephemeral /tmp; verdicts above are the record).

## Clean round

`modules/variation.zag` (adapted from v1's clean module, imports vendored
`R33_NATIVE_IO_V1.zag`):
- verdict PASS (RC=0), 0 banned hits, object_byte_scan clean,
  replay byte_identical=true, varies_with_state=true (S-state vs T-state
  outputs differ — genuine state variation), ops_checked=92, callees=0,
  `lookup_table_sha256` pinned (1 entry), module_sha256 recorded.
- Rerun determinism: two full audits → attestations byte-identical.

## Freeze

After the clean round, the checker source was frozen. Any further edit
restarts both rounds. Frozen hashes:

- checker source `checker/rngscan_v2.zag`:
  `ee962e53817c81721996a8086c5e42530da07316250b1a4906ab74a56a3d9e5d`
- checker binary (build artifact, NOT committed):
  `9bbaf5390f140a88516d6f1912bc060610bd773af32406f7fd935c5281c41943`
  built with `toolchain/bin/znc_linux_x86_64_abed8aa1`.

## Status

READY FOR RED TEAM. The 20 blind plants must be authored by a separate
agent; this builder will run the frozen checker unmodified against them.
K1/K2/K3 are binding: any replay divergence on a PASS build, any blind
miss, or any banned construct found post hoc on a PASS path kills v2.
