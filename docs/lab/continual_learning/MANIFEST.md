# MANIFEST.md — Committed file inventory with SHA-256

All SHAs computed 2026-09-27 from the exact committed bytes.

## Frozen authority (untouched)

| File | SHA-256 |
|---|---|
| `PREREG.md` | `2e94b2e7feb8179052af3d9ac18a85d8f9086433c6db3b4899d3ded15c75d909` |

Frozen 2026-09-27, commit `8c22ffb9bbde02c4dae1fc59ac73068509742696`.
Never modified by this crew.

## Teaching manifest

| File | SHA-256 |
|---|---|
| `TEACH.md` | `9b7e4f5fa2ee8e95ef07f839e3800663731f5867870dbc6b460ca27edb4dd9d5` |

## Implementation (pure Zag, zero randomness in decision paths)

| File | SHA-256 | Notes |
|---|---|---|
| `build/battery.zag` | `7d9e75ec9dbc260a5ca47f5bbb2d12a126881de4b941483ae96a6a474fdf27a4` | Battery driver: teach → probe → consolidate → formation → phase-4 → provenance → consequence |
| `build/bridge.zag` | `a2ac11728a693b1a00bc6062bbaa2665bd29818ddb68cb89c0d85a30cbdd9971` | Native bridge: lowercase/strip-punct/collapse-ws, FNV-1a over runtime bytes, dense registry, collision detection |
| `build/scorer.zag` | `4210bd4ace143716698b5fcd5bf7e52510b1ae9e16fbb0ba7044bd2975e90c8b` | Strict scorer; the ONLY module that reads expected-answer/synonym fields |
| `build/psm.zag` | `ec1adcc7f74696594e57c25da8588055dcadb8d2c1379b31ed16270ff664f067` | Vendored PSM + read-only `psm_fast_inspect` (see deviation D1) |
| `build/substrate/st_memory_core.zag` | `474ac0bb2417f26e531450a4fa406662aa733138eeaf622f454222509834da8d` | Vendored substrate, unmodified |
| `build/substrate/cl/common.zag` | `8aec83cb4feb83a20bc91c8179d7055d691c155414a359f7014386271aa6168b` | Vendored, unmodified |
| `build/substrate/R33_NATIVE_SHA256_V2.zag` | `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf` | Vendored, unmodified |
| `build/substrate/R33_NATIVE_IO_V1.zag` | `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8` | Vendored, unmodified |

**Deviation D1 (implementation):** `build/psm.zag` was modified from the
vendored original to add a read-only `psm_fast_inspect` helper (the
vendored PSM exposes no fast-tier reader; the battery needs it for the
deliberate consolidation pass). The original copied file's SHA-256 was
`a17f7e755f93bbd4e31cf4108ea879775b972a91cdd4733c41e6219289e04f9b`.
The first version of the helper incorrectly called a nonexistent
`f3_get32`; corrected 2026-09-27 to use native `fget`. The helper is
read-only (no state mutation). Final SHA above.

## Fixtures (frozen, verified against prereg + sources)

| File | SHA-256 |
|---|---|
| `build/fixtures/facts.tsv` | `5fbc710c65176ca19de754fdd0c5153ac0fcb2458e796e62f296740161afd98a` |
| `build/fixtures/phase4.tsv` | `a473651291ad010834e9951377d0570ebe6ed2ca84264703cab1e07ec9891609` |
| `build/fixtures/probes.tsv` | `a3740024cc8875775eae1e175576b1b80fdca9009bcd88a4b3737f6e11920231` |
| `build/fixtures/prov.tsv` | `509caab1fdff39135bbedceea2c3e49562d42ae1ede25ee3da7f0b1e9c190359` |
| `build/fixtures/conseq.tsv` | `20fb816f133a46174a22d2f5dfa86164625a6e0561b514ef57e410e1aaa08a1a` |

Fixture layouts: `facts.tsv` 6 fields (episode, phase, family, section,
source, fact); `phase4.tsv` 6 fields (id, subject, source, context,
question, expected); `probes.tsv` 4 fields (id, question, expected,
synonyms); `prov.tsv` 3 fields; `conseq.tsv` 3 fields.
`build/tools/make_fixtures.py` (`09b6a2a00e7ef7559878ba13627ce7b23055f347c4f1a668ae853db71f2d70b7`)
verifies fixtures against the frozen prereg and fetched sources:
`ALL CHECKS PASSED`.

## Evidence and logs

| File | SHA-256 |
|---|---|
| `RUNLOG.md` | `ffd8796df238912424de9e68e148bf3a3ad8021dfc25d2f42c596dc39cc82108` |
| `RESULTS.md` | `8edd71e10aa7cc7a8603ef0f98f86879d1ac4f1662a1eb5f59cbe5c9e56a2836` |

## Explicitly NOT committed

Binaries (`cl_bin`, `cl_scorer`), `.zagd` caches, build logs, downloaded
Gutenberg source texts (`build/sources/*.txt`), regenerable battery
outputs, `/tmp` material. The footprint stays under 200 MB; all temp
material lives under `~/workspace/tmp_commit` with `cl_*` prefixes.
