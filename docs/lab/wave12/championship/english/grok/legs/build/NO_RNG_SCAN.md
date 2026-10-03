# Static no-RNG scan — grok English-box legs

files scanned: 37 .zag files

## 1. Randomness-source tokens
none found (PASS): no urandom/rand/srand/rdtsc/clock_gettime/
gettimeofday/time(/getpid/RDRAND/_zag_time/_zag_clock/_zag_rand tokens.

## 2. `_zag_*` intrinsic inventory (per file)
- legA/src/grok_trial.zag: _zag_arg, _zag_argc, _zag_i64_to_str, _zag_print, _zag_println
- legA/src/substrate/R33_NATIVE_IO_V1.zag: _zag_free, _zag_i64_to_str, _zag_malloc, _zag_print, _zag_println, _zag_raw_syscall, _zag_slice_ptr, _zag_strcmp
- legA/src/substrate/R33_NATIVE_SHA256_V2.zag: _zag_free, _zag_malloc
- legA/src/substrate/cl/common.zag: _zag_i64_to_str, _zag_print, _zag_println, _zag_slice_ptr
- legA/src/t5_arms.zag: _zag_i64_to_str, _zag_print, _zag_println
- legA/src/t5_traps.zag: _zag_print, _zag_println
- legB/src/grok_b7_direct.zag: _zag_print, _zag_println
- legB/src/q1_types.zag: _zag_print
- legB/src/substrate/R33_NATIVE_IO_V1.zag: _zag_free, _zag_i64_to_str, _zag_malloc, _zag_print, _zag_println, _zag_raw_syscall, _zag_slice_ptr, _zag_strcmp
- legB/src/substrate/R33_NATIVE_SHA256_V2.zag: _zag_free, _zag_malloc
- legB/src/substrate/cl/common.zag: _zag_i64_to_str, _zag_print, _zag_println, _zag_slice_ptr
- legC/src/grok_teacher_leg.zag: _zag_print, _zag_println
- legC/src/q1_types.zag: _zag_print
- legC/src/substrate/R33_NATIVE_IO_V1.zag: _zag_free, _zag_i64_to_str, _zag_malloc, _zag_print, _zag_println, _zag_raw_syscall, _zag_slice_ptr, _zag_strcmp
- legC/src/substrate/R33_NATIVE_SHA256_V2.zag: _zag_free, _zag_malloc
- legC/src/substrate/cl/common.zag: _zag_i64_to_str, _zag_print, _zag_println, _zag_slice_ptr

## 3. Identifiers containing 'rand'
none (PASS).

## Verdict
STATIC SCAN PASS: no randomness/nondeterminism sources in the leg sources.
