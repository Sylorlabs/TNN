# L5 evidence — vDSO clock_gettime bypasses the M1 seccomp filter

- `vdso_test2.c`: installs the exact 72 M1 filter bytes via seccomp(2);
  direct `__vdso_clock_gettime` (resolved via dlopen) SURVIVES, rc=0, real timestamp.
- `vdso_test3.c`: same filter; glibc `clock_gettime(CLOCK_REALTIME)` SURVIVES
  (vDSO path), while the raw `syscall(228, ...)` in the same process dies
  SIGSYS — proving the filter was live for real syscalls throughout.

Conclusion: any plant reaching the clock through the vDSO is invisible to
the M1 filter. Recorded as verdict limitation L5.
