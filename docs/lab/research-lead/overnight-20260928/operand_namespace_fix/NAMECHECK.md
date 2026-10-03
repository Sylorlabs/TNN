# NAMECHECK.md -- Operand Namespace Fix Worker (rev1 workstream)

## Step 0: Toolchain guard (2026-10-02)

Executed at worker start, before any other work:

```
bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
which python3; which python
```

Result: safebin linked 36 tools; znc OK
(`src/tools/toolchain/znc_linux_x86_64_abed8aa1`); `which python3` and
`which python` both returned NOTHING (exit 1, empty output). PATH is
`$HOME/safebin` only for all worker commands.

No forbidden executable invoked in this wave. PROCESS-PASS on toolchain.

Compiler-defect workarounds (all four, mandatory for new Zag code):
- no `as *i32` + `q[0..n]` slice construction inside functions (u8 cells
  with little-endian helpers instead)
- no `_zag_print` for dynamic content (single preallocated buffer + one
  `_zag_raw_syscall` write; base `emit`/`e64` helpers reused as-is)
- no `.len` trust on `as []f64` / `as []i64` casts
- if-nesting at most 3 with hoisted flag lets
- never `!(... && ...)` in a `while` condition (De Morgan rewrite; grep for
  `while.*!(` before compiling new drivers)

## Reuse verification

- Frozen base: `../scaling_5000_fixed/s6_base.zag`, sha256
  `6797e6aeb7e642a5c3ce5875831bff31afb5691e03df96abcc248b9235a4a5bd`,
  verified byte-identical to lines 1..1495 of committed
  `../scaling_5000/s5_full.zag` (`cmp` clean). Read-only; never modified.
- `op_patch.zag` will be a byte-identical copy of the frozen
  `../scaling_5000_fixed/s6_patch.zag` (sha256 verified at copy time).
- `op_base.zag` will be `s6_base.zag` with exactly the PREREG.md section-3
  line changes; verified by `diff` inventory against the prereg (K2).

## Determinism

3/3 byte-identical runs per experiment (sha256 recorded in REPORT.md).
