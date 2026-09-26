# M3 taint-propagation unit-test vectors (committed pre-test, FROZEN)

Byte-cell taint: every tracked heap byte carries (init, taint) bits in the
tracer meta arena. Taint sources: `m3_getrandom`, `m3_clock_gettime`,
`m3_argv_read`, `/proc/self/environ` reads, `m3_taint_range` (test/manual).
Propagation: `m3_memcpy` copies taint bit per byte; `m3_w8` sets the taint bit
of the written byte (overwrites clear taint when written with taint=0).
Sinks (checker FAIL): any emitted event with taint=1 (R/B/O), or R with
region ∈ {UNINIT-HEAP, ENV, CLOCK}.

| ID | Operation | Expectation |
|---|---|---|
| V1 | `m3_taint_range(b,2,4)` on 8-byte clean buf | `m3_taint_of(b,0,8)==1`, `m3_taint_of(b,0,2)==0`, `m3_taint_of(b,6,2)==0` |
| V2 | `m3_memcpy(dst,0,src,0,8)` src fully tainted | `m3_taint_of(dst,0,8)==1` |
| V3 | byte 3 of 8 tainted | `m3_taint_of(b,0,3)==0`, `m3_taint_of(b,3,1)==1`, `m3_taint_of(b,4,4)==0` |
| V4 | `m3_r8` on tainted cell | `m3_last_taint()==1`; emitted R line ends ` 1` |
| V5 | `m3_r8` on fresh `m3_alloc` (no init) | `m3_last_region()==2` (UNINIT-HEAP) |
| V6 | `m3_r8` after `m3_w8` | `m3_last_region()==1` (INIT-HEAP), `m3_last_taint()==0` |
| V7 | alloc A,B adjacent; taint all of A | `m3_taint_of(B,0,n)==0` (no bleed) |
| V8 | taint A → memcpy A→B → memcpy B→C | `m3_taint_of(C,0,n)==1` (chain) |
| V9 | taint then `m3_w8(...,taint=0)` | `m3_taint_of(b,0,n)==0` (overwrite clears) |
| V10 | `m3_r8` on untracked buffer (`m3_raw_alloc`) | `m3_last_region()==0` (UNTRACKED) |
| V11 | `m3_getrandom` into buf | `m3_taint_of(buf,0,n)==1` afterwards |
| V12 | `m3_argv_read` into buf | `m3_taint_of(buf,0,n)==1` afterwards |

All assertions are value-deterministic (taint BITS, not tainted values), so
the test is byte-stable across reruns. The test binary is
`tracer/m3_taint_test.zag`; it prints `Vn PASS/FAIL` lines and exits nonzero
on any failure.
