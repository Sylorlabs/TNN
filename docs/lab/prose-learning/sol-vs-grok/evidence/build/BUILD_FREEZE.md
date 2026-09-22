# Build freeze evidence — commit B (2026-09-22)

Both contender implementations are frozen as source in `src/`. Binaries are
NOT committed (repo policy); the coordinator rebuilt from the frozen sources
with the pinned toolchain and verified behavior byte-identical to the
builders' accepted binaries.

## Frozen sources

| file | bytes | SHA256 |
|---|---|---|
| `src/sg_sol.zag` | 14699 | `1fcc3d37a997a502a050db56de5888dadf5b91c0aea737f60ec7f248f2d36850` |
| `src/sg_grok.zag` | 15280 | `4e8bba20d5eb9b370fe83f09ace0c22c2b848ecdcfda3160685cef29a362155e` |

Front end reused read-only in both builds: `frozen/sg_parse.zag`
(plus `R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag`).

## Rebuild verification (2026-09-22, coordinator, pinned toolchain)

`znc_linux_x86_64_abed8aa1` rebuilt both sources from `src/`:

| binary | bytes | matches builder's binary |
|---|---|---|
| sg_sol (rebuild) | 186630 | yes, byte size identical |
| sg_grok (rebuild) | 186770 | yes, byte size identical |

Stdout on the fixed calibration battery (`gen/calib/`, 384 teach / 432 probes)
is **byte-identical** between the builders' binaries and the rebuilds
(`cmp` clean on both).

## Determinism: 5 runs each on fixed calib

| run | Sol stdout SHA256 | Sol proof SHA256 |
|---|---|---|
| 1–5 | `d0a4cd6ec986153ca068ba383b39ee019c8ee433f877bd4aa5239837756b8e59` (all 5) | `2fe3366abb5a11a70f2a0e08cc8076531015bc187db935a5d6b3b8734aafbca3` (all 5) |

| run | Grok stdout SHA256 | Grok proof SHA256 |
|---|---|---|
| 1–5 | `c9076b4388fdf2ebcaabec2951051f424f5e03ffae7dd6677ad9979150898183` (all 5) | `999ac28fd318cb394157ce3b6149c9e214d260949dc730514e3e7545257f19da` (all 5) |

## Calibration scores on the fixed battery (frozen binaries)

| metric | Sol | Grok | hybrid |
|---|---|---|---|
| SG_PARA | 0.5000 | 0.9583 | 0.9583 |
| SG_CANON | 1.0000 | 1.0000 | 1.0000 |
| SG_SAFE | 1.0000 | 0.9167 | 0.9167 |
| SG_PREC | 1.0000 | 0.5000 | 0.5000 |
| SG_COMP | 0.0000 | 0.1667 | 0.1667 |
| SG_WRONG | 0.0000 | 0.2315 | 0.2315 |

Per-slice: canon 96/96 both; heldout 96/96 both; extra 0/48 Sol, 48/48 Grok;
typo 0/48 Sol, 40/48 Grok; neg 24/24 Sol, 21/24 Grok; hedge 24/24 Sol, 21/24
Grok; contr 24/24 both; distr 48/48 Sol, 24/48 Grok; multi 0/24 Sol, 4/24 Grok.

Calibration is not decisive; the scored battery is sealed until commit C.
