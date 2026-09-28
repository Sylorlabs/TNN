# Arm Q — Build Log

**Date:** 2026-09-21
**Compiler (frozen toolchain):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Source:** `cl/arm.zag` (71,847 bytes)
**Substrate:** `substrate/R33_NATIVE_SHA256_V1.zag` imported via
`@import("../substrate/R33_NATIVE_SHA256_V2.zag")` (relative to `cl/`), with
`R33_NATIVE_IO_V1.zag` alongside (required by `substrate/cl/common.zag`).

## Build command

```
cd ~/workspace/tnn-lab/units/arms/q/cl
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 arm.zag -o ~/workspace/q_test_bin
```

The compiler ran in foreground mode (`zagd` unavailable; background planning
disabled — warning only, build proceeds). Compilation completed with
diagnostics only:

- `warning[L0010]` (possible string buffer leak, `p_i64` at line 125):
  advisory; the `_zag_i64_to_str` buffer is used transiently and does not
  affect output correctness.
- `warning[E0101]` (adding 0 has no effect) at lines 293 and 446: advisory,
  dead arithmetic in hot paths.
- `warning[A0102]` (ignored `nio_close` return) in `read_file`, `file_size`,
  `write_file`: advisory; file I/O return checks handled inline.
- `warning[A0107]` (dead loop, `write_file` at line 530): the compiler flags
  the decrement loop; it executes correctly (all write tests byte-exact).

No errors. Binary: `~/workspace/q_test_bin` (258,412 bytes, executable).
**The binary is NOT committed** (per hygiene rules); it lives only on the VM
for the evaluation runs.

## Evaluation runs (prior crew, carried over)

- M1 (prose/code × hybrid/taught-only), M2 (T1/T2/T3), M3, M4, M5, M6 — run
  against the frozen battery corpora under
  `~/workspace/tnn-lab/units/arms/harness/corpora/r1/`.
- M8 determinism battery: `./q_test_bin m8-1x <croot> <outdir> <perturbation>`
  with `<croot>` = `harness/corpora/r1/` (contains `t1_prose.bin`,
  `t1_code.bin`), `<outdir>` per-run under `~/workspace/qwork/m8/<pert>/run<N>`.
- M8 perturbations: `clean`, `frag` (256 nio_alloc/nio_free churn pre-pass),
  `aslr` (1,234,567-byte allocation pad), `starve` (LD_PRELOAD'd shim
  `qwork/m8/shim.so` that fails getrandom/getentropy and zeroes
  clock_gettime), `freelist` (arm-internal no-op: id-derived placement, no
  clock/entropy use).
- Completion crew (this run) re-ran the full M8 matrix ×2 per perturbation and
  verified byte-identity; results recorded in `VERDICT.md`.

## Hygiene

Before commit: deleted `cl/.zag-cache/` and `cl/.zagd.semantic-ready`.
Not committed: `~/workspace/q_test_bin`, `~/workspace/qwork/`,
`~/workspace/q_build.log`.
