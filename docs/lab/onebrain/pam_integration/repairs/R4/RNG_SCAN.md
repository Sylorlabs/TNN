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

## Rescan 2026-09-25 (no-stupid-limits repair: chunked revision storage)

Scope: all three trees — `build/src/`, `longhorizon/src/`, `redteam/src/`
(the R4 repair lands identically in all three).

```
grep -rniE "rand|srand|random|lcg|entropy|_zag_random" build/src/ longhorizon/src/ redteam/src/ --include="*.zag"
```

**Result: PASS — zero hits** (no output at all; `.zag-cache` semantic
records excluded). The new revision machinery (`sp_rev_g64/sp_rev_s64`,
`sp_rev_chunk`, `sp_rev_get`, `sp_rev_append`, rewritten `sp_rev_newest` /
`sp_rev_cycle` / `sp_revise_one`) and the new `rt_r4_uncapped` probe use only
deterministic arithmetic, counters, and chunk allocation — no randomness in
any decision path.

Empirical backstop: smoke 3/3, redteam 3/3, long-horizon 3/3+3/3 — all
byte-identical across runs (SHAs in `evidence/`).
