# C500 — INDEPENDENT VERIFICATION OF B17 (`[]u8 as *u8` destructive cast)

Lane `b17fix`. Every run through `tnnwatch.sh` (300 s limit), pure-Zag env
asserted `PURE-ZAG-CLEAN` before compiling. Output is non-empty on every run
(no `_zag_raw_syscall` dependence).

## Why re-verify
The brief frames B17 as established, and `lane/tcdefects` filed it REAL. This
lane re-ran the three minimal reproducers from scratch rather than citing them,
because the rest of the mission (blast radius, invalidation, remediation) is
only worth doing if the defect is real.

## Result: DEFECT CONFIRMED, all three axes

| # | file | oracle | observed | runs |
|---|---|---|---|---|
| V1a | `V1_repro_read.zag` | wrote literal **7** into `b[0]`; any correct read-back is 7 | `direct b[0]=7`, `via (b as *u8)=8` | **9/9** |
| V1b | `V1_repro_control.zag` | same, via sanctioned `_zag_slice_ptr` | `direct=7`, `via _zag_slice_ptr=7` | **3/3 CORRECT** |
| V1c | `V1_repro_write.zag` | write 42 through cast-derived slice; `b[0]` must be **42** (aliased) or **7** (disjoint) | `b[0]` 7 -> **0** | **5/5** |

V1b is the load-bearing control: it differs from V1a by exactly one token
(`b as *u8` -> `_zag_slice_ptr(b)`) and is correct, so the wrong answer in V1a
is attributable to the cast and not to the harness, the allocator, or the host.

V1c is the strongest evidence that this is *corruption* rather than a wrong
address: `0` is neither the old value nor the new value, so **no consistent
aliasing semantics produces it**. The victim is the ORIGINAL arena — the
construct damages memory it does not own.

Note the determinism split, which is itself diagnostic: the *wrong-value* read
(V1a) is perfectly reproducible, while `tcdefects` observed run-to-run variance
on a different byte of the same cast-derived slice. A construct whose result is
a fixed-but-wrong descriptor address for one byte and drifting for the next is
reading whatever happens to sit in the slice descriptor's neighbourhood.

## C500
`[]u8 as *u8` yields an address that is NOT the slice's data pointer
(`_zag_slice_ptr(b) != (b as *u8)`), it is non-null, and reads and writes
through it land on unrelated memory. Remediation and the standing detector are
in `PTR_GUARD.md`.
