# H2 M8 Report — five-regime adversarial-heap gate

**Date:** 2026-09-21
**Binary:** `work/h2` (rebuilt 10:17 UTC after the t_m8 store-image fix;
post-rebuild smoke `m1-1x-prose` byte-identical — see BUILD_NOTES.md)
**Corpus:** `~/workspace/tnn-lab/corpora/r1/`
**Evidence:** `evidence/r1/m8-{clean,frag,aslr,starve,freelist-rev}/`

## What M8 does

`t_m8` runs a full M1 (ingest + full recall of both corpora) plus an M3
churn sequence (fresh ingest, kills, weakens, second fresh ingest) on ONE
session, then writes artifacts:

- `stdout.txt` — `M8,<m1p recall>,<m1c recall>,<ledger entries>`
- `store_hashes.txt` — per-1MB-chunk SHA-256 of the store image
  (slot table + dedup maps + ID maps)
- `store_chain.txt` — SHA-256 chain over the chunk hashes
- `ledger.bin` — retained audit ledger (73,922 entries × 64 B = 4,731,008 B;
  under the 300,000-entry cap — complete, not truncated)
- `ledger_chain.txt` — SHA-256 of the ledger bytes
- `alloc_trace.txt` — allocator trace (sizes only, perturbation-agnostic)

## Regimes

| Regime | Perturbation | Rationale |
|--------|--------------|-----------|
| clean | none | baseline |
| frag | 256 mixed-size allocs/frees before the run | fragmented heap |
| aslr | 1,234,567-byte pad allocation before the run | shifted heap base |
| starve | accepted no-op (no entropy/clock reads anywhere) | — |
| freelist-rev | accepted no-op (slot placement is a pure function of chunk ID) | — |

starve/freelist-rev are documented no-ops (AMBIGUITIES.md A8) but still run
as full regimes with byte-identical comparison.

## Results

| Regime | exit | stdout | artifacts vs clean |
|--------|------|--------|-------------------|
| clean | 0 | `M8,100.0,100.0,73922` | — (reference) |
| frag | 0 | byte-identical | byte-identical (all 6 files) |
| aslr | 0 | byte-identical | byte-identical (all 6 files) |
| starve | 0 | byte-identical | byte-identical (all 6 files) |
| freelist-rev | 0 | byte-identical | byte-identical (all 6 files) |

**M8-GATE: PASS.** All five regimes byte-identical on stdout, store hashes,
store chain, ledger bytes, ledger chain, and allocator trace.

## Bugs found during M8 (fixed, documented)

1. The runner invoked nonexistent `m8-<pert>` modes; fixed to
   `h2 m8-1x CORPUS OUTDIR PERT` (the first attempt's "unknown mode" runs
   were runner failures, deleted, not arm evidence).
2. `_zag_argc()` is always 0 in this znc build, so outdir/perturbation were
   silently ignored; dispatcher now reads `_zag_arg(3)`/`_zag_arg(4)`
   unconditionally.
3. Store-image OOB: `img_append` read `dcap*8` from the `dcap*4` ID maps →
   `panic: slice index out of bounds` after all ingests. Fixed to
   `cap*28+dcap*20` with `dcap*4` ID-map appends. Pre-fix code never
   produced artifacts, so no baseline is invalidated.

See BUILD_NOTES.md. The post-fix binary's non-M8 modes are byte-identical
to the 1x evidence (smoke-verified).
