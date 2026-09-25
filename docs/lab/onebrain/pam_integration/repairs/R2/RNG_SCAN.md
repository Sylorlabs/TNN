# RNG_SCAN — zero-randomness source scan

Date: 2026-09-24. Scope: `src/*.zag` (the integration build tree).

## Method

Case-insensitive grep over all build sources for randomness/clock/seed
primitives:

```
grep -rniE "rand|rdrand|getrandom|/dev/urandom|clock_gettime|time\(|seed" --include="*.zag" src/
```

with comment lines (`//`) excluded, plus a manual review of every hit.

## Result: PASS — zero RNG in any decision path

Hits (all benign, reviewed):

| file:line | hit | disposition |
|---|---|---|
| `sp_gate.zag:104` | `// 512 bytes: source organ id (255=seed)` | comment; "seed" = the pinned trust-root store, not a PRNG seed |
| `sp_gate.zag:233,254` | `sp_seed_store` | function name; plants the pinned EXT trust root, deterministic |
| `sp_gate.zag:675` | `// pinned seed: independent of every organ` | comment |
| `ob_test_integration.zag:531` | `"seed_independent"` | check name |

No `rand`, `rng`, `rdrand`, `getrandom`, `/dev/urandom`, `clock_gettime`,
`time(`, or PRNG-seeding constructs anywhere in the tree. The fork-D kernel
files were already certified no-RNG by their own build script; the
integration adds no randomness (the N-AUTH content hash is FNV-1a,
deterministic; nonces are monotonic counters, not random).

The 3x byte-identical smoke runs (SHA-256
`6855928854e38255e7275a18c5b07c82675fe1bc0752a616ba9ca90ba2e6d2e0`)
are the empirical backstop: any randomness in a decision path would break
byte-identity and fail `run_smoke.sh`.

## Re-scan 2026-09-25 (after perf fixes)

New hits from the Bloom filter (`prover.zag:95-96`):
| file:line | hit | disposition |
|---|---|---|
| `prover.zag:95` | `fn bf_fnv(s:[]u8, seed:i32)i32` | benign; `seed` is the FNV-1a initial hash constant (-2128831035 or 16777619), not a PRNG seed. Deterministic given input. |
| `prover.zag:96` | `let h:i32=seed;` | benign; copies the deterministic hash seed. |

Result: PASS — zero RNG in any decision path. The Bloom filter uses
deterministic FNV-1a hashing; no randomness, no clock, no entropy source.
