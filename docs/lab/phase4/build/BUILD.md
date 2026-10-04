# Phase 4 — build notes

## Toolchain (pinned)

- `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Build from `build/` so the bare `@import("R33_NATIVE_IO_V1.zag")` resolves
  (znc `@import` is a bare directive and resolves relative to cwd).

## Source

- `p4.zag`: 27,726-byte pure-Zag person-substrate interpreter. No structs, no
  RNG, no hash tables, no forward references. All state in `[]i64` tables
  (byte-sized `nio_alloc`), 64 person slots keyed by stable `p1`..`p64`
  identities, names as mutable attributes, per-person fact/belief linked
  lists, secret flags with non-enumeration, per-person correction counters,
  person delete/reopen, `L` ledger output, FNV-1a-64 transcript chain.
- `R33_NATIVE_IO_V1.zag`: native I/O substrate from workbuddy round-2
  (crew D lineage `3cd24f11d119a17d14d9637e43ebdc8918b41e92`), unmodified.

## znc issues worked around (from AGENTS.md lessons)

- ZNC-2026-09-21-007: `[]i64`/`[]u64` casts verified clean; no `[]i32`
  indexed tables anywhere (arena/getput accessors instead).
- Forward references: every callee defined before its caller (bus-error
  corruption otherwise).
- 5-deep `else` nesting: flat dispatcher (`op_eq` chain with early return).
- `[]u8` `==` is not content identity: `beq` byte-compare helpers used
  everywhere.
- `_zag_arg(n)` is a non-owned pointer: never freed; argc is 0 regardless —
  read unconditionally.
- u64 shifts/modulo are arithmetic/signed: hex emit uses explicit nibble
  extraction + masking, never `%`/`>>` on values with bit63 set.

## Binary identity

- Clean-room rebuild (fresh dir, same sources) is byte-identical:
  SHA-256 `2cb66f16daccec82ef2c0e75a1c1d003e99a71afa5809b22971031ef147d74e9`.
- All 14 probes (8 battery + 6 red-team): 2× plain + 1× MALLOC_PERTURB_=165
  runs byte-identical (see `../results/SHA256SUMS_RESULTS.txt`).
