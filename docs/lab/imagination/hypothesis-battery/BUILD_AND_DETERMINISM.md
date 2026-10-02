# BUILD AND DETERMINISM

## Toolchain

- **Compiler:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)
- **Build script:** `src/build_probe.sh`
- **Assembly:** `head -1582 composer_base.zag` + `fz1.zag`…`fz4.zag` + `v4a.zag`…`v4e.zag` + `probe.zag`
  (see `build_probe.sh` for exact composition)

## Source integrity

| File | SHA-256 |
|---|---|
| `src/probe.zag` | `3933f07027acd5f7040a3dddf925d5ac290ea65a5bc98c7d24b15a987f30ab2d` |
| `src/build_probe.sh` | `e6a10b6b056d412d8e7f76c4bae5e9a5e878e6b5a0cff7b0804984e6f3fb06a3` |
| `src/probe_bin` (built) | `602a65ff43ed970cfad8d8bbc8d22238e55e2e7eaa255564ca027c2028904d17` |

The binary is **not committed** (repo holds code + docs + evidence, not build artifacts).

## Determinism: byte-identical reruns

Every probe mode was run **twice**. All pairs are byte-identical (verified by `sha256sum` and `cmp`).

| Mode | Run 1 SHA-256 | Run 2 | Identical? |
|---|---|---|---|
| `anatomies` | `df08e44ffb622ef9cb3a834527ee1fbb9948168d1b17f4085bae217b1943aeac` | same | **YES** |
| `neckplace` | `15542fd4c1c919d16c3c74e918f198267aa1ef35d4d7c501811b692c0b5c6f1d` | same | **YES** |
| `slotvar` | `8a58637afae52fe6181e735576b93aa5b9211d0f6ff676709e5733df78820b73` | same | **YES** |
| `shake` | `139bac7526db2bc5702cf78d0c977b7d2f1e4d2654dbdcee8c799f66a626bcd2` | same | **YES** |
| `parts` | `d7c59af1d84daf91311743d9bcb32e5cb2f3560777e567061663` | same | **YES** |
| `viewcov` | `8d4d9c2b49a8788bf003e6fdec3052535b8d986f6cf0fe5d27c1cf4941590795` | same | **YES** |
| `oracle` | `9d67275ee029304fbeccddf4007bf9e5a5c4eb6955311e9d9a15305480644125` | same | **YES** |

**Zero RNG.** All mechanisms are deterministic given inputs. The `anatomies` output hash (`df08e44f…`) matches the pre-correction run, confirming the source fixes did not alter the anatomy code path.

## znc hazard audit (H2d)

| Hazard | Check | Result |
|---|---|---|
| `as []i32/u32/u16` indexed casts | `grep -c` | **0** (all tables on `[]u8` arenas with `h_get64`/`h_put64`) |
| `nio_free` on `_zag_arg()` (non-owned) | `grep -n` | **0** |
| `_zag_strcmp` equality | `== 1` | Correct (7 usages) |
| Slice > 2^25 bytes indexed | largest `nio_alloc` | 614,400 bytes (well under 33,554,432) |
| Large-struct field indexing | — | No structs used; flat byte arenas only |

**Independent cross-check:** `xcheck_neck.py` (pure Python, integer arithmetic) recomputes frame-12 anatomy from the mask dumps. Results match Zag **exactly**:

| Measurement | Python | Zag |
|---|---|---|
| snout | (63, 220) | (63, 220) |
| d_neck | 154 | 154 |
| d_skull | 126 | 126 |
| skull width | 83 | 83 |
| neck width | 15 | 15 |
| prominence ×1024 | 5666 | 5666 |

The toolchain is **exonerated** (H2d). Computation is correct; the failure is in the design, not the compiler.
