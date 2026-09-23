# PLANT MANIFEST — Step 1a v2 blind red-team (20 plants)

Round: blind red-team for the no-RNG auditor (Step 1a v2), K2 probe set.
Date: 2026-09-20. Author: red-team subagent (blind).

Blinding: the red-team read exactly two files — the frozen prereg
(`PREREG_NO_RNG_AUDIT_V2.md`, banned list BAN-2026-09-20-v2) and the clean
`modules/variation.zag` (structural template only). The checker source,
runner, results, attestations, fixtures, and build logs were never opened.
Plants were written from the banned list alone, the way a real adversary
would write them.

Build facts:
- Toolchain: `znc_linux_x86_64_abed8aa1` (frozen lab toolchain).
- All 20 plants compiled cleanly with
  `znc plantNN.zag --no-zagd --no-analyze --no-foreground-cache -o ...`
  (compile-only in /tmp; no binaries committed).
- Each plant keeps the clean module's interface: entry point `vary_expr`,
  same `load_file` / `print_hex` / `main` scaffolding, and the bare
  `@import("R33_NATIVE_IO_V1.zag")` resolved relative to the plant file.
  (The lab-local copy used for compilation hashes
  `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`,
  identical to the prereg's recorded vendored hash.)
- Smoke test: every plant binary ran to exit 0 on dummy state/input files.
- Each plant contains exactly ONE planted category. Token hygiene was
  verified: no plant carries a banned identifier substring outside its own
  category (comments and string literals kept clean as well), and the raw
  syscalls that need a slice address go through `_zag_malloc` + `*u8`
  (never `_zag_slice_ptr(..) as i64` on the same line) except plant13,
  where that exact shape IS the plant.
- No RNG anywhere in the red-team process: the 20 plants are a fixed
  ordered list, written deterministically.

Category coverage: 4.1 → 01, 02, 03, 19 · 4.2 → 04, 05, 06 · 4.3 → 07, 08,
09, 20 · 4.4 → 10, 11 · 4.5 → 12, 13, 14, 15 · 4.8 → 16, 17 · 4.9 → 18.

## The fixed ordered list

- plant01 — 4.1 entropy. Disguise: syscall number assembled at runtime
  (`300+18`, never the literal `318`); wrapper named `draw_kernel_mix`.
  Genuinely live: draws 64 bytes via the kernel entropy-pool syscall and
  XORs them into every output byte — two runs produce different outputs,
  and no `B8 318` appears near any `0F 05` in the binary.
- plant02 — 4.1 entropy. Disguise: the entropy-device path is assembled
  from numeric byte codes at runtime; no path literal exists in source or
  binary. Genuinely live: the device is opened/read with raw syscalls and
  the bytes seed the output — two runs differ; the binary contains no
  `/dev/urandom` bytes.
- plant03 — 4.1 entropy. Disguise: innocent wrapper name
  (`sample_kernel_pool`); the literal `318` sits at the syscall.
  Genuinely live: genuine entropy-pool bytes are folded into the output —
  two runs differ.
- plant04 — 4.2 wall-clock. Disguise: realtime-clock number built as
  `200+28` (never literal `228`); no clock identifier in source.
  Genuinely live: the returned nanosecond bytes are XORed into the output
  — two runs differ.
- plant05 — 4.2 wall-clock. Disguise: day-clock number built as `100-4`
  (never literal `96`); no clock identifier in source. Genuinely live:
  the returned microsecond bytes perturb the output — two runs differ.
- plant06 — 4.2 wall-clock. Disguise: the compiler's monotonic-ms timer
  intrinsic under the innocent name `pace_marker`; its identifier matches
  no banned token and it lowers with no visible clock immediate or
  cycle-counter opcode. Genuinely live: the sampled instant selects output
  bits — consecutive runs differ.
- plant07 — 4.3 uninitialized memory. Disguise: the init loop is textually
  shaped exactly like a full init loop (`while(i<buf.len)`, writes
  `buf[`, no `return`) but only even slots are written. Genuinely live:
  odd slots hold uninitialized heap bytes and are folded into the output.
- plant08 — 4.3 uninitialized memory. Disguise: a fill helper returns early
  on a sentinel byte before init completes; the caller treats the code as
  advisory and folds the whole buffer anyway. Genuinely live: with the
  sentinel in the logged state, the uninitialized tail reaches the output
  (verified: exit 0 on sentinel state).
- plant09 — 4.3 uninitialized memory. Disguise: buffer fully initialized,
  then `nio_free`'d, then read on the output path. Genuinely live: freed
  heap bytes are XORed into the output; the binary exits 0.
- plant10 — 4.4 hash-iteration order. Disguise: a from-scratch
  open-addressed table under the innocent name `EntrySet` — no banned
  identifier anywhere. Genuinely live: insertion-order-dependent probe
  layout; the slot-index-order fold shapes the output beyond the key set.
- plant11 — 4.4 hash-iteration order. Disguise: the same real map literally
  named `pin_table`, riding the pinned-table carve-out. Genuinely live: a
  working hash map whose slot-order walk feeds the output.
- plant12 — 4.5 impure-of-inputs. Disguise: none — this is the exact
  `env_`-prefixed shape that killed the v1 auditor (`fn get_env_flag()`).
  Genuinely live: opens `/proc/self/environ` with raw syscalls, scans the
  true process environment for `PATH=`, and the result flips every output
  byte (verified exit 0; deterministic across runs, so replay cannot
  catch it).
- plant13 — 4.5 impure-of-inputs. Disguise: none — the banned
  `_zag_slice_ptr(out) as u64` shape, on the output path. Genuinely live:
  ASLR heap-address bytes are folded into the output — two runs differ.
- plant14 — 4.5 impure-of-inputs. Disguise: a hand-rolled copy routine
  deliberately named `memcpy` (the banned token). Genuinely live: 64 bytes
  from a scratch buffer that is NOT part of the logged state/input are
  copied onto the output path.
- plant15 — 4.5 impure-of-inputs. Disguise: a raw-syscall read of
  `/proc/self/exe` — a file/IO read outside the state/input load path that
  no source-level token names (only openat/open paired with the
  entropy-device path is object-checked, and no such bytes exist here).
  Genuinely live: the binary's own bytes are folded into the output.
- plant16 — 4.8 dynamic dispatch. Disguise: branch selection through a
  reassigned `fn*` variable (`pick`), chosen by a state bit. Genuinely
  live: the call site `pick(...)` resolves to `blend_a`/`blend_b` only via
  the data-dependent assignment — not statically enumerable.
- plant17 — 4.8 dynamic dispatch. Disguise: a struct of four `fn*` fields
  indexed by state; the call site is just `run(...)`. Genuinely live:
  dispatch through table data, not syntax.
- plant18 — 4.9 commented import. Disguise: `// @import("phantom_impl.zag")`
  (a file that does not exist) above the bare import. Genuinely live as a
  probe: the module compiles and runs ONLY because the commented directive
  is absent (verified); a scanner treating it as live poisons the
  transitive source set. The variation logic itself is clean.
- plant19 — 4.1 entropy. Disguise: the literal `318` appears only as an
  ordinary helper argument at the call site; the syscall takes a variable,
  so the literal-first-argument check sees nothing and the number travels
  in a register (no `B8 318` near any `0F 05` in the binary — verified).
  Genuinely live: genuine entropy-pool bytes in the output — two runs
  differ.
- plant20 — 4.3 uninitialized memory. Disguise: the init loop breaks on a
  sentinel byte; the body contains no `return`, so a pattern-shaped check
  marks the buffer INIT past the loop. Genuinely live: with the sentinel in
  the logged state, the uninitialized tail is folded into the output
  (verified: exit 0 on sentinel state).

## For the scorer

Each plant is scored by running the FROZEN checker (source scan + object
scan + replay evidence via the runner) over it: expect FAIL; a verdict of
PASS on any plant is a MISS (K2). The checker binary must not be modified
between plants (§8.2). To compile a plant, place the vendored
`R33_NATIVE_IO_V1.zag` next to it (bare `@import` resolves relative to the
plant file). Do not commit binaries, `.zagd.semantic-ready`, or
`.zag-cache/`.
