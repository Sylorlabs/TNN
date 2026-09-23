# Portable Runtime — Wave-3 Investigation (slug: portable-runtime)

Date: 2026-09-19. VM: Ubuntu 24.04 x86-64. Compiler: `znc 2026.07.0-dev`
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
All work on this VM; Zag-first; no git pushes.

Program law in force: (1) scaling is allowed — mechanisms must carry an
explicit scale dimension (survive 10x/100x: traces, partitions, memory,
horizons); "bigger table" stays dead. (2) **No RNG in the AI** — no random
exploration, tie-breaks, or stochastic policies anywhere in the system's
decision paths; deterministic given state. Seeded RNG tolerated only as
harness scaffolding, never in the system. (3) Test adversity as designed
curricula; verdicts must distinguish "system is deterministic" from
"test was adversarial".

## 1. Verdicts per target

| Target | Verdict | Basis |
|---|---|---|
| Linux x86-64 | **POSITIVE — lead target** | hello + full R34 v3 protocol + all wave-2 trials, runtime-proven (§playbook) |
| WASM | **NEGATIVE — blocked by compiler backend** | Not a missing host import, not a language limit: the wasm codegen is broken for everything the mechanisms need (§2) |
| Linux AArch64 | **MIXED — runs under QEMU, but `_zag_raw_syscall` miscompiles** | hello/println/malloc/strcmp runtime-proven via qemu-aarch64-static 7.2.0; raw-syscall number dropped by backend (§3) |
| macOS (arm64) | **BLOCKED from this VM by design** | Linux `znc` rejects `--target macos-arm64`; macOS output needs the separate `znc_macos_arm64_7cacbfc0` binary on a macOS host. Nothing verifiable here. |

**Overall: MIXED.** AArch64 now executes (QEMU user-mode works), but two
compiler-backend bugs block the mechanism stack: wasm lowering is broken
across the board (§2) and arm64 `_zag_raw_syscall` drops the syscall number
(§3). The path to one portable runtime is clear in design (§4); it needs
backend repairs, not a new architecture.

## 2. WASM: precise characterization (reproduced 2026-09-19)

**Category: compiler backend defects — a missing/broken lowering, not a
host-import problem and not a language limitation.** Every failure below is
at `znc` compile time or as invalid/wrong machine code; instantiation-time
host imports are never the blocker (they are declared unconditionally and
are unreachable from Zag source anyway).

### 2a. No `_zag_*` builtin lowers for wasm
Each of these fails with `znc: wasm codegen error: call to unknown function`:
`_zag_print`, `_zag_println`, `_zag_print_i32`, `_zag_print_u64`,
`_zag_print_i64`, `_zag_i64_to_str`, `_zag_malloc`, `_zag_free`,
`_zag_strcmp`, `_zag_argc`, `_zag_raw_syscall`. The wasm backend's
known-function table covers only user-defined `fn` calls; string literals
themselves compile (as inert data) — so strings are legal Zag for wasm,
just unusable.

### 2b. No control flow lowers
`if` and `while` — even trivial (`if a == 5 { return 1; }`) — fail with
`znc: wasm codegen error: unknown variable`.

### 2c. Widening casts silently dropped → invalid modules
`(a as i64) * b` and `let s: i64 = a as i64;` compile **without error** but
emit the unconverted i32 where i64 is expected; Node rejects the module:
`Compiling function #3 failed: i64.mul[0] expected type i64, found local.get
of type i32`. Silent miscompile, caught only at instantiation.

### 2d. Bitwise/shift ops silently miscompiled (wrong results, no error)
Observed under Node v24: `1 & 2` → 3 (expected 0); `1 << 3` → 4
(expected 8); `6 | 3` → 9 (expected 7); `16 >> 2` → 18 (expected 4).
Any mechanism using bit-packing (`<< (i*8)` byte assembly, flags) would
compute garbage on wasm with no diagnostic.

### 2e. Module shape (fixed, unconditional)
Every wasm module imports `env.print_i32`, `env.print_u64`, `env.print_i64`
(functions) — required at instantiation even for programs that never print —
and exports only `main`. **No linear memory is exported**, so there is no
host-readable string/byte output path at all.

### 2f. The actually-sound subset (observed, Node v24)
Straight-line code only: i32/i64 `+ - * / %`, comparisons as values
(`(3 < 4) as i32` → 1), struct construction/field access, user fn calls,
`return` of small ints from `main`. Everything else is broken or missing.

**Consequence:** the new mechanisms (deliberate memory ops need malloc,
slices, prints; verified switching needs branches and loops; audit ledgers
need string/byte I/O) cannot run on wasm today. Making wasm viable requires
compiler-backend repair (control flow, builtin lowering incl. a byte-sink
host import + exported memory, correct casts and bitwise ops) — not a
different host shim. Do not route around this with a hand-rolled WAT
post-pass; the failure is in `znc`'s lowering tables.

### Minimal repro (all compile/run commands verified this session)
```zag
// repro_print.zag — string printing
fn main()i32 {
    _zag_println("HELLO");
    return 0;
}
// znc repro_print.zag --target wasm --no-zagd --no-analyze --no-foreground-cache -o repro_print.wasm
// → znc: wasm codegen error: call to unknown function   (exit 1)

// repro_branch.zag — control flow
fn main()i32 {
    let a: i32 = 5;
    if a == 5 {
        return 1;
    }
    return 0;
}
// → znc: wasm codegen error: unknown variable   (exit 1)

// repro_cast.zag — widening cast (compiles, then Node rejects the module)
fn main()i32 {
    let a: i32 = 3;
    let s: i64 = a as i64;
    return s as i32;
}
// → znc: [wasm] wrote WASM repro_cast.wasm, then
//   WebAssembly.instantiate(): Compiling function #3 failed:
//   local.set[0] expected type i64, found local.get of type i32

// repro_bitops.zag — silent wrong code (compiles, instantiates, wrong answer)
fn main()i32 { return 1 & 2; }   // Node: main() → 3, expected 0
```

## 3. AArch64: runtime verification ACHIEVED via QEMU (2026-09-19)

`--target arm64` emits **Linux AArch64 ELF** (verified: `ELF 64-bit LSB
executable, ARM aarch64, version 1 (SYSV), statically linked`) — correct
input for `qemu-aarch64` user-mode. The "no QEMU on this VM" blocker is
resolved: `qemu-aarch64-static` 7.2.0 (multiarch static build, x86-64)
runs the binaries; a copy is kept at
`~/workspace/tnn-lab/toolchain/bin/qemu-aarch64-static` (apt's `qemu-user`
was abandoned — mirror too slow; static binary sufficed).

**Runtime proof (all under qemu-aarch64-static, exit codes observed):**
- `hello_arm64` (from `hello.zag`): prints `HELLO_FROM_LINUX_X86_64`,
  exit 0. strace: `write, write, exit(0)` — clean.
- `_zag_println`, `_zag_malloc`/`_zag_free` (64MB mmap arena),
  `_zag_i64_to_str`, `_zag_strcmp` (returns 1 on equality — matches the
  `nio_name_valid` lesson), struct ops: all execute correctly.

**But — compiler backend bug: arm64 `_zag_raw_syscall` drops the syscall
number.** Minimal repro:
```zag
fn main()i32 {
    let r = _zag_raw_syscall(172, 0, 0, 0, 0, 0, 0);  // 172 = getpid on aarch64
    return 7;
}
```
qemu strace: `Unknown syscall 2147483647` then `exit(7)`. The requested
number (172, or 64=`write` in another probe) never reaches x8 — the backend
emits 0x7FFFFFFF (INT32_MAX, a sentinel/poison value) instead, in both
literal and variable forms. QEMU tolerates it (ENOSYS, execution continues,
exit code correct), so it is benign for verification but fatal for real
use: **every adapter in the R33/R34 substrate issues file I/O through
`_zag_raw_syscall`, so no file-touching Zag program can work on AArch64
until this lowering is fixed.** (In one larger program the correct number
happened to go through — stale x8 from the preceding `println`'s write —
confirming a register/slot bug, not a deliberate trap.)

Portability hazard confirmed while compiling for arm64: `_zag_raw_syscall`
numbers are arch-specific (64 = `write` on aarch64-Linux but `semget` on
x86-64-Linux). Any Zag source embedding raw syscall numbers or OS flag
constants is **not portable by construction** — this is exactly what the
R33 Darwin→Linux port had to fix by hand (§5 of the playbook). The spec
(§4) makes this structurally impossible in core code.

## 4. Portability spec: what "one portable runtime" concretely requires

### 4.1 Lead target
**Linux x86-64 is the lead verification target** — the only target with
runtime proof of the full mechanism stack. AArch64-Linux is first follower
for compute-only mechanisms now that QEMU executes the binaries (§3), but
it cannot carry I/O workloads until the `_zag_raw_syscall` lowering bug is
fixed. **WASM is the aspirational universal target but cannot be lead
today** (§2); macOS-arm64 needs its own compiler binary on a macOS host.
Lead-target discipline: every mechanism lands and passes on Linux x86-64
first; portable core code must additionally compile for arm64 from day one
(cheap, catches arch coupling early).

### 4.2 Module/host-import boundary (for wasm, when the backend is repaired)
- Module exports: `main` **plus exported linear memory** (absent today —
  without it no string/byte output path exists).
- Host imports (all under one `env` module, versioned): numeric sinks
  (`print_i32/u64/i64` — keep, but they must become *callable* from Zag,
  not vestigial), and a **byte-sink import** `env.write_bytes(ptr: i32,
  len: i32)` so ledger/audit bytes can leave the module without depending
  on string-printing codegen. No other host surface: the module must not
  import time, randomness, or filesystem — see §4.4.
- Contract: the module is a pure state machine; the host is a dumb byte
  pipe + clock. All mechanism logic lives in the module.

### 4.3 What new Zag code must satisfy (portable-subset rules)
1. **No `_zag_raw_syscall` in core mechanism code.** All OS interaction goes
   through named adapter functions (`nio_*`, `cl_*` — the R33/R34 pattern),
   with per-target implementations carrying per-target constants. The
   adapter boundary is where Darwin/Linux numbers, `struct stat` layouts,
   and `ru_maxrss` units live — never in the learner, switcher, or ledger.
2. **No arch- or OS-specific constants in core** (syscall numbers, flag
   words, struct offsets, page sizes). If a value differs per target, it is
   an adapter parameter.
3. **Core = explicit state + named adapters.** The portable core (learner,
   deliberate memory ops, verified switching, audit ledger) must be
   expressible as pure computation over explicitly-passed state, with I/O
   only through the adapter boundary. This is what makes the wasm
   module/host split (§4.2) and the native per-OS adapters the *same*
   architecture.
4. **WASM-subset hygiene for shared sources** (until the backend is fixed,
   aspirational): shared core code should avoid depending on constructs the
   wasm backend cannot lower — but do NOT contort the lead-target code
   around today's wasm bugs (§2c/§2d are compiler bugs to fix, not dialect
   restrictions to adopt).
5. **Static isolation checks stay in the runner** (playbook §7/§12): the
   adapter boundary is enforced by grep, not by convention.

### 4.4 Determinism (program law, and it serves portability)
- **No RNG anywhere in the system's decision paths**: no random
  exploration, no random tie-breaks, no stochastic policies, no seeded RNG
  inside the learner/memory/switching code. Deterministic given state.
- Seeded RNG is tolerated **only as harness scaffolding** (driving the
  world), never inside the system; prefer explicitly-designed adversarial
  curricula over RNG-driven worlds where feasible.
- Cross-platform payoff: a deterministic core can be **bit-identical across
  targets** — the strongest portability test available (same inputs →
  same ledger bytes on Linux, AArch64, wasm, macOS). Any platform-specific
  entropy (ASLR addresses in output, unseeded clocks in state) breaks this
  and is banned from core state.
- Tie-breaking rule (replaces any random tie-break): a fixed, documented,
  deterministic order (e.g. lowest partition id wins) — logic, not chance.

### 4.5 Scale dimension (program law: design for 10x/100x)
Every mechanism ships with an explicit scale argument in its prereg:
- **10x/100x traces**: ledger append cost must be O(1) amortized per event;
  the host boundary (§4.2) streams bytes, never whole-state dumps.
- **10x/100x partitions**: switching cost must not be O(partitions²);
  partition ids are dense indices, lookup is indexed not scanned.
- **10x/100x memory**: no fixed caps baked into portable core; any bound
  (max partitions, max ledger entries) is an explicit named parameter with
  a defined saturation behavior (refuse-with-code, never silent drop —
  cf. the R33-B000 trace-saturation defect).
- **10x/100x horizons**: state that grows with time must be summarized or
  checkpointed; the audit ledger's replay-to-exact-state property must hold
  at the scaled size, not just the trial size.
- Small-scale trials state the scaling argument and name the next scale
  test explicitly. "Bigger table" remains dead: scaling means more of the
  real workload, never a larger score table.

### 4.6 What must be true of the toolchain (not the Zag code)
1. wasm backend: lower control flow, all `_zag_*` builtins used by the
   adapters (at minimum malloc/free/slice/string ops + byte-sink import),
   correct int casts and bitwise ops, exported memory. Until then, wasm is
   compile-and-pray for toys only.
2. AArch64: runtime execution (QEMU user-mode suffices for verification).
3. macOS: a macOS host (or runner) with the macOS `znc` binary; the Linux
   compiler will never emit Mach-O.
4. None of these change the Zag sources if §4.3 holds — that is the test
   that the spec is right.

## 5. Key evidence inventory (this session)
- `/tmp/wasmrepro/`: `t_println.zag`, `t_print.zag`, `t_strvar.zag`,
  `t_i64str.zag`, `t_numprint*.zag`, `w1..w5.zag`, `w_ok*.zag`,
  `w_cast*.zag`, `w_if*.zag`, `w_while.zag`, `w_and/shl/or/shr/bits.zag`,
  `w_sub/mul/div/mod/cmps.zag`, `a_native.zag` (+ arm64 binaries
  `a_native_arm64`, `a_mf_arm64`, `a_s1`, `a_s2`, `a_c1`, `a_pid1/2`,
  `a_raw`) — minimal cases behind every claim in §2–§3.
- `~/workspace/tnn-lab/toolchain/hello/hello_arm64`: Linux AArch64 ELF,
  **runtime-proven** under qemu-aarch64-static (prints, exit 0).
- `~/workspace/tnn-lab/toolchain/bin/qemu-aarch64-static`: qemu-aarch64
  7.2.0 static build (multiarch), persistent copy for future agents.

## 6. Next steps
1. **AArch64 runtime: DONE this session** (`qemu-aarch64-static` 7.2.0 at
   `~/workspace/tnn-lab/toolchain/bin/qemu-aarch64-static`). Remaining:
   file the `_zag_raw_syscall` number-dropping bug against the arm64
   backend; re-run the R34 Linux-ported substrate under QEMU once fixed
   (it cannot work until then — all its I/O goes through raw syscalls).
2. **WASM**: file the §2 characterization against the `znc` wasm backend
   (control flow, builtin table, cast lowering, bitwise opcodes, exported
   memory + byte-sink import). No host-shim workaround can fix §2b–§2d.
3. **macOS**: needs a macOS host + `znc_macos_arm64_7cacbfc0` (repo:
   `src/tools/toolchain/`); out of scope for this VM.
4. **Spec adoption**: new mechanism preregs cite §4.3–§4.5 (portable subset,
   determinism, scale argument) as acceptance gates; the R34 adapter
   pattern (`nio_*`/`cl_*`) is the template for all new OS-touching code.
