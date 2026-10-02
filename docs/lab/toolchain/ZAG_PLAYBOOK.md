# ZAG Playbook — TNN Native Lab (Linux)

Proven behavior of the Zag compiler `znc` on this Linux VM, recorded
2026-09-19. Everything below was executed on this machine unless marked
**historical** (repository evidence, not re-executed here).

Rule of the lab: document and test what components **actually are**, not
what they resemble. Three kinds of claim appear in this file and they are
never mixed:

- **compile proof** — `znc` produced a target artifact without error.
- **runtime proof** — the artifact was executed and its output observed.
- **historical** — the repository contains logs/binaries for it, but it was
  not executed on this VM.

## 1. The compiler

- Path (lab-local): `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Origin: `sylorlabs/TNN` repo, branch `tnn-native-lab`,
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
- Size: 8,337,204 bytes (matches the repo listing byte-for-byte)
- Format: ELF 64-bit x86-64, **statically linked, no section headers**
- SHA-256: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
  — exactly matches `R32_ZNC_PROVENANCE_2026-08-23.json` in the repo.
- Version string: `znc 2026.07.0-dev (edition 2026)`
- `znc --help` works. Default native output is x86-64 ELF and the
  compiler needs **no external toolchain** (no cc/ld installed or invoked).

### Recommended flags

```
znc prog.zag --no-zagd --no-analyze --no-foreground-cache -o prog
```

- `--no-zagd`: the `zagd` daemon is unavailable on this VM; without this
  flag builds warn about it.
- `--no-analyze`, `--no-foreground-cache`: skip auxiliary passes; faster,
  deterministic CLI behavior for lab work.

### check / script modes

- `znc check prog.zag` type-checks. Emits a warning that `zagd` is
  unavailable, then `znc: OK — all capability claims proven` on success.
- `znc script prog.zag --run` generates **its own entry point**. A file
  with a user-defined `fn main()` fails in script mode (entry-point
  conflict). Use script mode only for entry-point-less snippets.

## 2. Minimal Zag (all syntax below compiled AND ran on Linux x86-64)

```zag
fn main()i32 {
    _zag_println("HELLO_FROM_LINUX_X86_64");
    return 0;
}
```

```bash
znc hello.zag --no-zagd --no-analyze --no-foreground-cache -o hello_linux
./hello_linux   # -> HELLO_FROM_LINUX_X86_64, exit 0
```

Observed: `znc: wrote native binary hello_linux (127 bytes main, 0 external tools)`.
Binary: 4,120-byte statically linked x86-64 ELF.

Language notes (observed, not from docs):

- Functions: `fn name(args)rettype { ... }`, e.g. `fn add(a: i32, b: i32) i32`.
- Bindings: `let x:i32 = 0;` `let s:i64 = ...;`
- Structs: `struct CLUsage {status:i32,cpu_us:i64,rss_bytes:i64}`,
  constructed `CLUsage{.status=0,.cpu_us=-1,.rss_bytes=-1}`, fields `u.status`.
- Slices: `[]u8`; pointer slices `p[0..n]`; `_zag_slice_ptr(s) as i64`.
- Raw pointers: `*i64`, `*u8`; null: `null as *i64`; indexing `p[0]`.
- Casts: `expr as i64`, `(b[at+i] as i64)<<(i*8)`.
- Strings: double quotes; `\"` is an accepted escape for a quote inside a
  string (the R34 sources mix `"..."` and `\"...\"` forms).
- Intrinsics seen working: `_zag_print`, `_zag_println`, `_zag_i64_to_str`,
  `_zag_strcmp`, `_zag_arg(n)`, `_zag_malloc(n)`, `_zag_free(ptr)`,
  `_zag_raw_syscall(num,a1..a6)`.
- Panics exist: out-of-bounds slice access aborts with
  `panic: slice index out of bounds`.

## 3. Cross-target table

`--help` on the Linux compiler advertises these `--target` values:

| target | compile proof | runtime proof | notes |
|---|---|---|---|
| (default) x86-64 ELF | yes | **yes** — hello + full R34 campaign | primary lab target |
| `arm64` | yes — 65,576-byte AArch64 ELF | **no** — no QEMU aarch64 on this VM | Linux AArch64 ELF, not Mach-O |
| `wasm` | yes — valid `00 61 73 6d` magic | **yes** — Node v24, `main()` returned 42 | see §4 |
| `macos-arm64` | **no** — rejected as unsupported | n/a | historical macOS logs used this name, but on a *different* compiler binary |
| `gpu-nvidia`, `gpu-amd`, `gpu-vulkan`, `amdgpu-gfx1010`, `vulkan-compat`, `opencl-compat`, `metal-compat`, `opengl-compat`, `cuda-compat`, `x86_64`, `arm64`, `i686` | not tested | not tested | advertised only |

**macOS is not producible from this compiler.** Historical repo logs invoke
`--target macos-arm64`, but that belongs to the separate macOS binary
`znc_macos_arm64_7cacbfc0`. The Linux compiler accepts `--target arm64` and
emits **Linux AArch64 ELF** — a different OS object format. Document
"macOS status" only from the macOS compiler.

## 4. WASM backend surface (proven)

- `_zag_println("...")` **fails** to compile for wasm:
  `wasm codegen error: call to unknown function`.
- A computation-only program (no string printing) compiles and runs:

```zag
fn add(a: i32, b: i32) i32 { return a + b; }
fn main()i32 { let s: i32 = add(40, 2); return s; }
```

- Only `main` is exported (`add` is internal to the module).
- The module **requires host imports** or instantiation fails:
  `env.print_i32`, `env.print_u64`, `env.print_i64` (functions).
- Under Node v24 with those imports stubbed: `main()` returned `42`.
- Rule: keep WASM programs computation-only; provide the three `env.print_*`
  imports at instantiation.

## 5. Syscall intrinsics on Linux x86-64

- `_zag_raw_syscall(num, a1, a2, a3, a4, a5, a6)` — **supported** (proven via
  strace: issues the real syscall with args in the Linux calling convention).
- `_zag_linux_syscall` — **does not exist** (compile error).
- `_zag_darwin_syscall` — **does not exist** on this compiler (compile
  error: `call to unknown function`). Any source using it must be ported.

### Porting Darwin -> Linux: the verified map

`R33_NATIVE_IO_V1.zag` was a macOS/ARM64 substrate ("Darwin ABI constants
checked against the installed SDK, not Linux numbers"). The lab-local copy
at `~/workspace/tnn-lab/toolchain/R33_NATIVE_IO_V1.zag` is now a **Linux
x86-64 port** (Darwin original kept as `R33_NATIVE_IO_V1.zag.darwin.orig`).
Same for `R33_CONTINUING_LIFE_V1/storage.zag`
(Darwin original: `storage.zag.darwin.orig`).

Syscall numbers (Darwin -> Linux x86-64):

| op | Darwin | Linux |
|---|---|---|
| open | 5 | 2 |
| close | 6 | 3 |
| read | 3 | 0 |
| write | 4 | 1 |
| lseek | 199 | 8 |
| mkdir | 136 | 83 |
| fsync | 95 | 74 |
| flock | 131 | 72 |
| openat | 463 | 257 |
| linkat | 471 | 265 |
| fstatat | 339 | — (port uses fstat = 5) |
| setrlimit | 195 | 160 |
| select | 83 | 23 |
| getuid | 24 | 102 |
| getrusage | 98 | 98 (same number, different struct notes) |

Flag constants (verified against `/usr/include/.../bits/fcntl-linux.h`
on this machine — **do not hand-convert octal**; the first port attempt
confused O_DIRECT (16384) with O_DIRECTORY (65536) and `open` returned
EINVAL, caught only by strace):

| use | Darwin | Linux x86-64 |
|---|---|---|
| open_root: O_DIRECTORY\|O_NOFOLLOW\|O_CLOEXEC | 554696704 | **720896** |
| open_child: O_NOFOLLOW\|O_CLOEXEC\|O_NONBLOCK | 16777476 | **657408** |
| open_child create: + O_RDWR\|O_CREAT\|O_EXCL | 16780038 | **657602** |
| flock LOCK_EX\|LOCK_NB | 6 | 6 (same) |
| mkdir mode 0700 / creat mode 0600 | 448 / 384 | 448 / 384 (same) |
| setrlimit RLIMIT_NOFILE resource id | 8 | **7** (0 CPU, 1 FSIZE, 4 CORE same) |

ABI layout notes:

- Linux `struct stat` (x86-64): `st_mode` is u16 at **offset 24**
  (Darwin: offset 4); `st_nlink` u64 at **offset 16**; `st_uid` u32 at
  **offset 28**. A `st_u64` little-endian helper was added to storage.zag
  (common.zag only had `cl_u32`).
- `getrusage` struct: `ru_utime`/`ru_stime` timevals at 0/16 (same formula
  works), but **`ru_maxrss` is KiB on Linux vs bytes on Darwin** — the port
  multiplies `p[4]` by 1024 to keep `rss_bytes` semantics.
- `select` arg order and the zeroed-fdset no-op behavior port unchanged.
- `EINTR` is `-4` on both; retry logic ports unchanged.
- errno map: Linux `ENAMETOOLONG` is 36 (Darwin 63) — added `-36` to the
  path-error set; `-40` is ELOOP on Linux (already mapped to path error).

Porting discipline (white-box, per Micah's direction): every changed
constant carries a comment naming both sides; struct offsets were checked
against the installed headers, not memory; behavior was verified at
runtime (strace + real file operations), not just compilation.

## 6. R34 v3 continual learner — Linux port (runtime proof, 2026-09-19)

### Import graph

`r34v3/r34_continuing_harness_v3.zag` imports (paths relative to the
importing file's directory):

```
r34_continuing_harness_v3.zag
├── r34_learner_core.zag            (isolated learner; see §7)
├── ../R33_CONTINUING_LIFE_V1/world.zag
├── ../R33_CONTINUING_LIFE_V1/checkpoint.zag
│     ├── observation.zag, common.zag, storage.zag (Linux-ported)
│     └── ../../R33_NATIVE_SHA256_V2.zag
└── ../R33_NATIVE_IO_V1.zag         (Linux-ported)
```

The repo's reorganized generation hierarchy breaks the original
`../R33_CONTINUING_LIFE_V1/...` relative layout; the lab-local tree
reconstructs it. Future agents: copy the whole `toolchain/` subtree or
fix the relative paths — copying just `r34v3/` is not enough.

### Result

Compiled with the Linux compiler, default target:

```
znc: wrote native binary r34_v3_linux (172719 bytes main, 0 external tools)
```

The **full native protocol passes on Linux** via
`r34v3/run_native_linux.sh` (bash port of `run_native.zsh`; takes `ZNC`
from env or first arg, portable `sha256sum`, no macOS-isms):

```
failures=0
learner_core_isolation=true
exact_match=true
```

- `campaign`: `R34V3_FAILURES,0` — 24/24 CL_CHECK lines pass, including
  `train_updates,48,48` (48 learner updates), `deterministic_learner,1,1`,
  `deterministic_world,1,1`, `inner_state_corrupt_refused,2005,2005`.
- `R34V3_STATE,campaign,fp=397063,active=0,contexts=3,updates=48,switches=2,pending=0`
- `R34V3_RESOURCE,cpu_us=398749,rss_bytes=2027520` (getrusage port works).
- `write-mid` → `checkpoint-1.bin` (548 bytes, mode 0600), exit 0.
- `reload-mid` output **byte-identical** to `reference-mid`
  (`R34V3_STATE,continued,fp=915581,...,updates=57,...,pending=0` +
  `R34V3_CONTINUE_POSITIVE,4`).
- `refuse-inner-corrupt` → `R34V3_REFUSAL,2005` (CL_CORRUPT).
- `refuse-torn` → `R34V3_REFUSAL,2001` (CL_IO).
- Full evidence bundle: `r34v3/EVIDENCE_20260919T221033Z/` (commands,
  stdouts, exits, SHA256SUMS, RECEIPT.txt, isolation proof).

This is the first execution of the R34 v3 experiment outside macOS. No
learner/world logic was changed — only the syscall substrate (§5).

### Darwin coupling (why a port was needed at all)

The harness is a white-box sandwich:

1. **Portable**: learner core, evaluator, world stepping logic.
2. **Adapter boundary**: `nio_*` functions in `R33_NATIVE_IO_V1.zag`,
   `cl_*` in `storage.zag`.
3. **Darwin-only implementation**: 13 `_zag_darwin_syscall` sites
   (open/openat/read/write/close/fsync/flock/mkdir/linkat/lseek/setrlimit/
   select/fstatat) plus fstat/getuid/getrusage in storage.zag, with Darwin
   syscall numbers, flags, and struct layouts baked in.

The failure mode before the port was precise: learner logic lowered fine,
then `znc: error in nio_regular: native: call to unknown function
'_zag_darwin_syscall'` — the adapter boundary, not the science.

## 7. Learner-core isolation (static check, part of the runner)

`r34_learner_core.zag` must not import `world.zag`/`checkpoint.zag` and
must not reference `cw_`/`CWOutcome`. The runner greps for
`@import\([^)]*(world\.zag|checkpoint\.zag)` and `\bcw_|CWOutcome` and
fails the run if found. Currently: `learner_core_isolation=true`.

## 8. Common errors and fixes

| error | cause | fix |
|---|---|---|
| `call to unknown function '_zag_darwin_syscall'` | Darwin substrate source on Linux compiler | port per §5, or use macOS compiler |
| `call to unknown function '_zag_linux_syscall'` | no such intrinsic | use `_zag_raw_syscall` |
| `--target macos-arm64` rejected | Linux compiler has no macOS backend | use macOS `znc` binary for macOS |
| `wasm codegen error: call to unknown function` on `_zag_println` | no string printing in wasm backend | computation-only; `env.print_*` host imports |
| script mode conflicts with `fn main()` | script generates its own entry point | compile normally, or drop `main` |
| `open(...) = -1 EINVAL` with O flags | wrong octal→decimal constant (e.g. O_DIRECT vs O_DIRECTORY) | check against installed headers; strace to see actual flags |
| `panic: slice index out of bounds` | `_zag_malloc(n) as []u8` leaves length 0 | form the slice: `p[0..n]` (see `nio_alloc`) |
| harness `write-mid` exits 2, no files | `cl_root` failed (bad open flags/numbers) | strace the binary; verify §5 map |
| imports fail after copying one folder | relative `@import("../R33_...")` layout | reconstruct the full relative tree |

## 9. What is NOT proven (do not claim)

- ARM64 **runtime** behavior (no QEMU; compile-only).
- macOS builds from this Linux compiler (impossible by design).
- GPU/compat/driver targets (advertised, untested).
- Malicious same-user mutation resistance or power-loss durability of the
  checkpoint store (explicitly not claimed by the original authors either).
- Anything about the R34 science beyond what the harness asserts: the lab
  proves the **apparatus runs**; interpreting results is separate work.

## 10. Files

- Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Playbook: `~/workspace/tnn-lab/toolchain/ZAG_PLAYBOOK.md` (this file)
- Hello/cross-target: `~/workspace/tnn-lab/toolchain/hello/` (`hello.zag`,
  `add.zag`, `add.wasm`, `hello_linux`, `hello_arm64`)
- Linux-ported IO substrate: `~/workspace/tnn-lab/toolchain/R33_NATIVE_IO_V1.zag`
  (Darwin original: `R33_NATIVE_IO_V1.zag.darwin.orig`)
- Linux-ported storage adapter:
  `~/workspace/tnn-lab/toolchain/R33_CONTINUING_LIFE_V1/storage.zag`
  (Darwin original: `storage.zag.darwin.orig`)
- R34 v3 lab tree: `~/workspace/tnn-lab/toolchain/r34v3/`
  (binary `r34_v3_linux`, runner `run_native_linux.sh`,
  evidence `EVIDENCE_20260919T221033Z/`)
- Note: `r34v3/r34_continual_harness_v3.zag` was a 0-byte fetch artifact;
  removed 2026-09-19. The real harness is `r34_continuing_harness_v3.zag`.

## 11. Guidance for future agents

- Prefer longer developmental runs; test long-term learning, not just
  compile-and-exit.
- Keep the white box open: when something fails, find the exact layer
  (learner logic vs adapter vs compiler backend) before changing anything.
- Never substitute ABI constants from memory — verify against installed
  headers and confirm with strace/runtime behavior.
- Record negative results (this file's §9 exists because someone checked).
- No Python in lab work going forward — Zag only (this playbook used the
  system python3 once, purely as an octal calculator for header constants;
  the lab artifacts themselves are all Zag).
- Nothing in this task pushes to Git; the repo branch `tnn-native-lab`
  was read-only for this work.

## 12. Zag testing notes (added 2026-09-19, Agent D)

Proven while building the white-box suite
(`toolchain/r34v3/wb_whitebox_tests.zag`, runner
`../wave2/whitebox/run_whitebox.sh` — 43/43 checks pass):

- **Check macro pattern:** `cl_check(name, actual, expected)` from common.zag
  prints `CL_CHECK,<name>,<actual>,<expected>` and returns 1 on mismatch.
  Accumulate `f=f+cl_check(...)`; end with `WB_FAILURES,<f>` and
  `return (f!=0) as i32`. The runner greps `^CL_CHECK,` and requires
  `actual==expected` on every line — keep this output contract.
- **Driving the learner core in tests:** `r34v3_init(seed)` returns the
  struct by value; pass `&s` to take `*R34V3State`. Set `pending` fields
  directly (`s.*.pending=1; s.*.pending_action=...;`) to drive
  `r34v3_accept` without the world harness. `r34v3_equal(&a,&b)` compares
  all 21 fields — the whole learnable state.
- **`nio_alloc` is NOT zeroed.** Every buffer the tests depend on is
  explicitly initialized (the suite zeroes its `restarts` array by hand;
  `r34v3_encode` does the same). Never assume zeroed memory.
- **No `[]i32` allocator observed.** Pack small ints into `[]u8` with
  little-endian helpers (`wb_i32_get`/`wb_i32_set`); values must stay
  non-negative and < 2^31.
- **Bool-to-int:** `(expr) as i32` works on comparisons
  (e.g. `(r1.rng!=r2.rng) as i32`), same idiom as the R34 harness.
- **Static checks belong in the runner, not the binary:** the
  learner-core isolation rule (no `world.zag`/`checkpoint.zag` import, no
  `cw_`/`CWOutcome` reference) is a grep in `run_whitebox.sh`, mirroring
  the R34 runner. Runtime tests can't see imports.
- **Negative tests need negative cases:** every invariant check in the
  suite is paired with a tampered input that must fail (broken lineage
  link, regressed steps, orphan ledger entry). An invariant test without
  its negative case proves nothing.
- **Documented assumptions beat silent ones:** the suite's FILTER_GT/MAP_MUL
  numeric semantics and the revision PROMOTE rule are assumptions recorded
  in `WHITEBOX_TESTS.md`. If an assumption changes, the tests AND the doc
  change together — a passing suite against stale semantics is worse than
  a failing one.

## ⚠️ Contamination notice — 2026-09-20 (R34 hidden-randomness remediation)

This document cites results that are **QUARANTINED**: the §6 R34 v3 Linux-port campaign results (24/24 CL_CHECK pass, `failures=0`, `fp=397063`, `updates=48`).
The cited runs trained with `explore_enabled=1`, engaging a hidden seeded LCG
(`r34v3_rng` in `r34_learner_core.zag`) in the learner's action-choice path —
a violation of the no-randomness law (r34 RNG probe, workstream 2/8, commits
`072f25aa` / `4976cbf5` on branch `tnn-native-lab`; Micah's ruling: REMEDIATE).
Treat the cited numbers as recorded-but-uncertified until clean reruns exist.
The original text above is left intact for the record.
