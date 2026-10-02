# INTRINSIC SURFACE AUDIT — znc_linux_x86_64_abed8aa1 (one-time, 2026-09-20)

Method (authoritative: the compiler itself, not strings-guessing):
1. Extracted all `_zag_[A-Za-z_0-9]+` runs from the znc binary's string table;
   split concatenated symbol runs at every `_zag_` boundary (intrinsic names
   never contain `_zag_` internally — verified: every intrinsic actually used
   by committed Zag sources was recovered exactly).
2. Unioned with every `_zag_*` token appearing in committed Zag sources
   (those necessarily compiled, so they are real).
3. 319 candidates. Each probed against the frozen compiler with call shapes
   `()`, `(0)`, `(0,0)`, `("s")`, `(0,0,0,0,0,0)`: a candidate is REAL iff at
   least one shape avoids `native: call to unknown function` (unknown names
   fail before arity/type checking — validated with `_zag_print()` giving an
   arity error vs `_zag_nonexistent_xyz()` giving unknown-function).
4. Cross-check: all 9 `_zag_*` tokens actually used by committed sources
   probed REAL (`_zag_cstr_ptr` was string-literal-only in the v2 checker,
   correctly UNKNOWN).

Result: **98 REAL intrinsics** on this toolchain build. Probe scripts:
ephemeral (/tmp/probe_one.sh, /tmp/candidates.txt, /tmp/probe_results.txt);
the classification below is the frozen record.

## Classification

**TIER M — allowed in module (trial-build) source** (deterministic, pure or
fixed-IO-channel; minimal set the representative build needs):
- `_zag_arg`, `_zag_argc` — argv; the trial's declared inputs.
- `_zag_print`, `_zag_println` — stdout; the trial's declared output channel.
- `_zag_i64_to_str`, `_zag_strcmp` — pure functions, no entropy channel.

**TIER S — substrate-only** (allowed ONLY in manifest-pinned substrate files;
any occurrence in module source is a FAIL):
- `_zag_malloc`, `_zag_free` — raw allocation; module code must use
  `nio_alloc`/`nio_free` (which zero-fill on alloc).
- `_zag_slice_ptr` — address materialization (ASLR-leak primitive, v2
  dirty5 class); confined to the hash-pinned substrate where its call sites
  are fixed and reviewed.
- `_zag_raw_syscall` — general syscall primitive (v2 dirty2 class); allowed
  ONLY with a first argument that is an integer literal in SYSCALLS below.

**SYSCALLS — allowlisted first-argument literals for `_zag_raw_syscall`**
(Linux x86-64; audited from the frozen substrate
`R33_NATIVE_IO_V1.zag` e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8,
which uses exactly these 13, all as literals):
0 read, 1 write, 2 open, 3 close, 5 fstat, 8 lseek, 23 select, 72 flock,
74 fsync, 83 mkdir, 160 setrlimit, 257 openat, 265 linkat.
Computed first arguments (e.g. `200+28`) FAIL even if the value would be
listed (v2 red-team class: computed syscall immediate).

**BANNED-EXPLICIT — named nondeterminism channels** (any occurrence in the
build's module source is a FAIL naming the token; also FAIL by the
fail-closed rule even if renamed here):
- Clock: `_zag_clock_monotonic_ms` (banned outright per the v2 lessons).
- Syscall escape hatches: `_zag_linux_syscall`, `_zag_darwin_syscall`
  (probed UNKNOWN on this toolchain — listed anyway; fail-closed covers).
- Environment: `_zag_getenv`, `_zag_script_env_get`.
- Process: `_zag_exec_cmd`, `_zag_exec_capture`, `_zag_process_result_abi_new`,
  `_zag_process_result_output`, `_zag_process_result_state`,
  `_zag_process_result_status`, all `_zag_script_*`.
- FD/file IO outside the substrate: `_zag_read_fd`, `_zag_read_file`,
  `_zag_write_file`, `_zag_write_exec`, `_zag_file_exists`, `_zag_write_stdout`,
  `_zag_write_stderr`, `_zag_flush`.
- Privileged/hardware: `_zag_cli`, `_zag_sti`, `_zag_hlt`, `_zag_pause`,
  `_zag_wbinvd`, `_zag_inb`, `_zag_inw`, `_zag_inl`, `_zag_outb`, `_zag_outw`,
  `_zag_outl`, `_zag_rdmsr`, `_zag_wrmsr`, `_zag_read_cr0`, `_zag_read_cr2`,
  `_zag_read_cr3`, `_zag_read_cr4`, `_zag_write_cr0`, `_zag_write_cr3`,
  `_zag_write_cr4`, `_zag_lgdt`, `_zag_lidt`, `_zag_ltr`, `_zag_invlpg`,
  `_zag_x86_cpuid_eax`, `_zag_x86_cpuid_ebx`, `_zag_x86_cpuid_ecx`,
  `_zag_x86_cpuid_edx`.
- Termination: `_zag_exit`.
- Allocator introspection: `_zag_allocation_free`, `_zag_allocation_register`,
  `_zag_allocation_validate`, `_zag_allocator_allocation_count`,
  `_zag_allocator_live_bytes`, `_zag_allocator_peak_live_bytes`,
  `_zag_fixed_buffer_*` (all 12).
- RNG-named: `_zag_rand` (probed UNKNOWN on this toolchain — the name alone
  is banned; any future toolchain introducing it fails closed).

**UNLISTED — everything else** (deterministic but unneeded: `_zag_realloc`,
`_zag_memcpy`, `_zag_memcmp`, `_zag_strdup`, `_zag_str_concat`,
`_zag_str_free`, `_zag_strlen`, `_zag_str_len`, `_zag_str_eq`,
`_zag_strcmp_ord`, `_zag_str_index_of_byte`, `_zag_str_to_i64`,
`_zag_u64_to_str`, `_zag_print_i32`, `_zag_print_i64`, `_zag_print_u64`,
`_zag_print_f32`, `_zag_print_f64`, `_zag_eprintln`, `_zag_panic`, ...):
FAIL by the fail-closed rule. Deterministic-but-unlisted is not a
nondeterminism risk; it is banned to keep the certified idiom narrow.

## Full REAL list (98)

_zag_allocation_free _zag_allocation_register _zag_allocation_validate
_zag_allocator_allocation_count _zag_allocator_live_bytes
_zag_allocator_peak_live_bytes _zag_arg _zag_argc _zag_cli
_zag_clock_monotonic_ms _zag_eprintln _zag_exec_capture _zag_exec_cmd _zag_exit
_zag_file_exists _zag_fixed_buffer_allocate _zag_fixed_buffer_capacity
_zag_fixed_buffer_deinit _zag_fixed_buffer_generation _zag_fixed_buffer_high_water
_zag_fixed_buffer_init _zag_fixed_buffer_read_u8 _zag_fixed_buffer_remaining
_zag_fixed_buffer_reset _zag_fixed_buffer_used _zag_fixed_buffer_write_u8
_zag_flush _zag_free _zag_getenv _zag_hlt _zag_i64_to_str _zag_inb _zag_inl
_zag_invlpg _zag_inw _zag_lgdt _zag_lidt _zag_ltr _zag_malloc _zag_memcmp
_zag_memcpy _zag_outb _zag_outl _zag_outw _zag_pause _zag_print _zag_print_f32
_zag_print_f64 _zag_print_i32 _zag_print_i64 _zag_print_u64 _zag_println
_zag_process_result_abi_new _zag_process_result_output _zag_process_result_state
_zag_process_result_status _zag_raw_syscall _zag_rdmsr _zag_read_cr0 _zag_read_cr2
_zag_read_cr3 _zag_read_cr4 _zag_read_fd _zag_read_file _zag_realloc
_zag_script_alloc _zag_script_alloc_used _zag_script_context_init
_zag_script_context_shutdown _zag_script_env_get _zag_script_file_size
_zag_script_new _zag_script_process_result_abi_new _zag_script_read_file_into
_zag_slice_ptr _zag_sti _zag_str_concat _zag_str_eq _zag_str_free
_zag_str_index_of_byte _zag_str_len _zag_str_to_i64 _zag_strcmp _zag_strcmp_ord
_zag_strdup _zag_strlen _zag_u64_to_str _zag_wbinvd _zag_write_cr0 _zag_write_cr3
_zag_write_cr4 _zag_write_exec _zag_write_file _zag_wrmsr _zag_x86_cpuid_eax
_zag_x86_cpuid_ebx _zag_x86_cpuid_ecx _zag_x86_cpuid_edx

## Audit limits (stated honestly)

1. This audits the intrinsic surface of exactly
   `znc_linux_x86_64_abed8aa1`. A different toolchain build needs a new audit
   (the probe is re-runnable; the method is the durable part).
2. Non-`_zag_` language surface (operators, casts, slicing, `@import`) is
   covered by the prescriptive rules R3–R6, not by this audit.
3. `@import` can only name files inside the build tree (R1 manifest pins the
   full file set; there is no stdlib import beyond the vendored substrate).
