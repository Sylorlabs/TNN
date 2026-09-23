# AMBIGUITIES-B16.md — literal-reading log for the B-16 build

Standing rule (inherited from the harness): where the frozen prereg
(`units/PREREG_FREEZE.md`, commit `b0b9140c0eda`) is ambiguous, implement the
**literal reading** and log it here. Nothing below reinterprets a bar.
Micah decides.

## B16-A1. M3 fresh-unit byte size for 16-byte chunks (IMPLEMENTED)

ARM_INTERFACE.md §10 M3 says: "steps 1–3,000 ingest 3,000 fresh units
(`churn_fresh.bin[0:192000]`, 64B each)". That byte range is literal for the
b64 validator (chunk = 64B) but cannot be literal for B-16: B-16's unit IS its
16-byte chunk (design doc §B: "a 64-byte probe = … four B-16" IDs; the
validator's code path, which this arm ports literally, ingests one chunk per
unit).

Literal reading adopted: a "unit" in the M3 schedule is the arm's unit = one
16-byte chunk. The 3,000/3,000/4,000 unit counts, the V=1,000 every-k-th
schedule, C_M3=4,000, the 50-weaken timing, and the last-500-fresh sample are
all unchanged; only the fresh byte range becomes `[0:48000]` (3,000 × 16B) and
`[48000:112000]` for phase 3. Rationale: the protocol's invariants are the
unit counts and the pressure structure, not the byte range — the byte range is
a consequence of the validator's chunk size, and porting it verbatim would
require B-16 to ingest 64B "units" in M3 while ingesting 16B units in M1, an
inconsistency the prereg never asks for. If the coordinator rules that M3
fresh units must be 64B spans for all B sizes, this arm re-runs with a
4-chunk-per-unit M3 path (the slot record already carries arbitrary
`(offset, len)`; the change is mechanical).

## B16-A2. Ledger sharding vs the single-slice ledger (IMPLEMENTED, forced)

The interface fixes the ledger as "16-word entries = 64 bytes" and the
validator keeps one slice. B-16's M8 ledger needs ~950k entries ≈ 60MB, and
znc cannot index any slice larger than 2^25 bytes. The ledger is therefore
8 × 262144-entry shards (16MB each); entries remain 64B 16-word little-endian
records in the identical field layout, addressed by
`(led_n >> 18, (led_n & 0x3FFFF) * 64)`. The audit *content* is unchanged;
only the container is sharded. `LEDGER-BOUND` semantics preserved (drop
silently past capacity; sized so it never fires).

## B16-A3. M8 artifact hashing for >2^25 regions (IMPLEMENTED, forced)

- `store_hashes.txt`: per slot-array ≤2^20 windows, chunk indices sequential
  across the 8 arrays in fixed order (ids, offs, lens, corps, flags, shifts,
  pidx, ins). Chain = `sha256(concat of chunk digests)`, exactly the
  validator's construction.
- `ledger_chain.txt`: `sha256(concat of per-shard sha256(used bytes))`
  instead of `sha256(whole ledger bytes)`.
Both are deterministic, order-preserving, and M8 compares each arm only
against itself (C13), so the gate's meaning is unchanged.

## B16-A4. ID-layer classification (CONFIRMED, no swap probe)

Per ARM_INTERFACE.md §9's provisional classification, `b16` is a non-ID-layer
arm: recall resolves the unit ID through pure arithmetic (`id = f(offset)`)
plus the slot hash — no persistent ID→storage mapping the arm maintains.
Therefore `m1_id_probe = "N/A (no ID layer)"`, M7 = `N/A (no ID layer)` with
the informational re-read-bytes footnote, and the A15 swap probe does not
apply. No provisional cell to mark.

## B16-A5. M9 shape for a null-control arm (NOTED)

B-16 reaches criterion in episode 1 by construction (ingest = memorization),
so M9's shape is degenerate ("fast-then-flat", takeoff 1, steepness 100.0,
late gain 0.0) — same as the validator. Informational only; never scored.
