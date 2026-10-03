# Vendoring note — G1 registration sources in `R2-3/src/`

Under self-PAM prereg amendment 2026-09-27-A
(`../../selfpam/amendments/AMENDMENT_2026-09-27_G1_ID2.md`), the R2-3
admission instrument registers candidate id 2 (`selfpam-fact-gate`).

## Vendored files (byte-identical copies)

| File in this dir | Canonical source | SHA-256 at vendoring |
|---|---|---|
| `g1_candidate.zag` | `../../selfpam/src/g1_candidate.zag` | `6ba9ea447387db4e47f13ea2295ea7da4ba735c27c8d41c638ca0fefa8abdecb` |
| `codec.zag` | `../../selfpam/src/codec.zag` | `ca9d1fd1cd10b164e95a2ca2f4b2a96c7944ba7452958cb0d1156db9643ccd4c` |

`build_g1.py` refuses to build if these differ from the canonical files —
the amendment freezes the `sp_gate_*` implementations as vendored, and any
semantic change needs its own amendment.

## Build assembly (why the substrates are staged, not vendored)

znc resolves `@import` relative to the current working directory, so the
build stages every imported file into one build dir:

- From this dir: `sense.zag`, `r2p_gates.zag`, `r2p_front.zag`,
  `r2p_protos.zag`, `g1_candidate.zag`, `codec.zag`.
- From `../../selfpam/src/`: `R33_NATIVE_IO_V1.zag`
  (`e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`),
  `R33_NATIVE_SHA256_V2.zag`
  (`9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf`).

The substrates are referenced from their canonical location, not copied
into the repo a second time. `build_g1.py` records the substrate SHAs it
actually staged in its build log.

Build: `python3 build_g1.py` → pinned znc
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`)
compiles `sense.zag` to `sense_bin` in the build dir. **Binaries are never
committed.**
