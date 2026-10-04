# B6 RESULTS — the interpreter scratch bound

Claim IDs **C570-C576**. Prereg: `PREREG.md` K1-K7.

## THE HEADLINE

**The documented one-line fix `z_alloc(128)` is NOT a fix. It is a bigger
magic number that fails silently at program length 12.** The tight bound is
**`scr_bytes(L) = 12L - 8`**, a function of program length, derived from the
instruction set's maximum stack effect.

And a correction to the ledger: **on this host the overflow does not panic.
It silently corrupts the heap.** See K5.

---

## K1 — the derivation is EXACT for valid programs

`b6_sweep.zag` runs **all 5^L digit strings** for L=1..10 through an
instrumented copy of `learner_interp` that records the highest scratch cell
touched (12,721,240 programs total; `out/b6sweep.log`).

| L | max cell, VALID | predicted 3L-3 | max cell, ALL strings |
|---|---|---|---|
| 1 | 0 | 0 | 2 |
| 2 | 3 | 3 | 5 |
| 3 | 6 | 6 | 8 |
| 4 | 9 | 9 | 11 |
| 5 | 12 | 12 | 14 |
| 6 | **15** | 15 | 17 |
| 7 | **18** | 18 | 20 |
| 8 | 21 | 21 | 23 |
| 9 | 24 | 24 | 26 |
| 10 | 27 | 27 | 29 |

`K1_VALIDPASS=1`: `max_sp(L) = 3L-3` for valid programs at **every** L.

**`K1_ALLPASS=0`, reported as the prereg requires.** Over *all* digit strings
the maximum is `3L-1`, two cells above my prediction. The cause is fully
identified: a program ending in `loo3` reaches `3L-1`, but `valid_prog`
requires the last instruction to be 0/3/4, so such programs are rejected and
**never reach the interpreter**. The load-bearing bound is the valid-program
one, and it matches exactly. The `all` column is reported because the prereg
said it would be.

The worst-case valid program is `[loo3 x (L-1), fit]`: `loo3` contributes +3,
`fit` +1, `exm` 0, and `med`/`avg` *reset* sp to 1.

## K3/K4 — `12L-8` is the TIGHT bound, verified to the byte

`b6_canary.zag` allocates the scratch and the canary as **two slices of one
allocation**, so the canary begins at exactly byte S with no malloc padding
(a first attempt with two separate `z_alloc` calls let small overflows hide in
allocator padding and under-reported).

| L | need = 12L-8 | S = 12L-9 | S = 12L-8 | S = 64 | S = 128 |
|---|---|---|---|---|---|
| 6 | 64 | 1 corrupt | **0** | 0 | 0 |
| 7 | 76 | 1 corrupt | **0** | 12 | 0 |
| 8 | 88 | 1 corrupt | **0** | 24 | 0 |
| 11 | 124 | 1 corrupt | **0** | 60 | 0 |
| 12 | **136** | 1 corrupt | **0** | 72 | **8** |

At `S = 12L-8` there is **zero** corruption; at `S = 12L-9` exactly **one**
byte. The bound is tight, not merely sufficient. Every result also matches a
4096-byte reference run (`match=YES`), so the tight allocation changes no
answer.

**`z_alloc(64)` was exactly the tight bound for L=6** (`12*6-8 = 64`). The
frozen constant was therefore not a magic number — it was a correct derivation
that was frozen as a literal and never re-derived when the length moved 6->7.

## K5 — THE LEDGER'S STATED MECHANISM IS WRONG ON THIS HOST

Prereg K5 predicted `set32(scr,64,...)` on a 64-byte buffer would reproduce
`panic: slice index out of bounds`. **It does not.** `b6_verify.zag` mode 0
runs the ledger's exact crashing program `[fit,loo3,loo3,loo3,loo3,loo3,fit]`
at L=7 with `z_alloc(64)` and it **completes, rc=0**.

`b6_probe.zag` isolates this with no interpreter in the way
(`out/b6probe.log`):

```
B6P z_alloc(64).len=64
B6P set32(b,64) SURVIVED readback=12345
B6P wrote_through_offset=4096 SURVIVED
B6P neighbour_corrupt_bytes=16
```

**This host's compiler emits no slice bounds checks.** Writing 4 KB past the
end of a 64-byte allocation survives and silently corrupts a neighbouring
live allocation (16 bytes).

**Why the ledger saw a panic:** the DEEP7 lane was built with the pinned
Linux binary `src/tools/toolchain/znc_linux_x86_64_abed8aa1`; this host uses
`znc 2026.07.0-dev` targeting macos-arm64. Different compilers, different
bounds-checking behaviour.

**Consequence: B6 is real but WORSE than documented, not better.** It is not
a loud crash that stops the run. It is a **silent heap corruption**, the same
silent-wrong-answer class as B1. Under this toolchain the 5k-scale runs that
"passed" would not have been stopped by it.

## K2 — 128 is insufficient, confirmed by corruption not by panic

`need_bytes(12) = 136 > 128`. At L=12 with `scr=128` the canary shows
**8 corrupted bytes** (`out/b6d_12_128.log`). At L=12 with `scr=136`,
zero.

## K6 — the honest new ceiling

| allocation | safe for | status |
|---|---|---|
| `z_alloc(64)` (frozen) | L <= 6 | **exact** at L=6; breaks at L=7 |
| `z_alloc(128)` (documented fix) | L <= 11 | **still a magic number** |
| `z_alloc(12*L-8)` (derived) | **no ceiling** | function of L, charter 37 satisfied |

128 is not the tight bound for *any* integer L (`12L-8 = 128` has no integer
solution). It is a rounded-up literal. The principled form is
`scr = z_alloc(12*qlen - 8)`.

## K7 — a larger scratch costs nothing measurable

`b6_cost.zag`, **9,765,600 programs** per run, identical work at every size:

| S | checksum | elapsed (3 reps) |
|---|---|---|
| 64 | 104834560 | 25, 23, 22 s |
| 128 | 104834560 | 19, 22, 20 s |
| 512 | 104834560 | 23, 18, 21 s |
| 4096 | 104834560 | 23, 28, 23 s |
| 65536 | 104834560 | 22, 23, 24 s |

Checksums identical across a **1024x** range of buffer size; no timing trend.
The interpreter touches only cells `0..max_sp` regardless of allocation size,
so the only cost of a larger buffer is the one-time `z_alloc` zero-fill,
O(bytes), once per run.

**The preregistered expectation holds: there is no speed ceiling here.** The
trade-off is therefore **zero** and the correct allocation is simply the
sufficient one. Sizing the scratch defensively costs nothing.

## Incidental finding (not preregistered, reported)

`learner_interp` computes `s/sp` with no `sp>0` guard, and `stack_med`
dereferences `((sp-1)/2)` likewise. Any program whose first instruction is
`exm` (which pushes nothing) followed by `avg`/`med` **panics with division
by zero** in the frozen source. `valid_prog` rejects exactly those programs
(an aggregate before any push sets `vok=0`), so the frozen lane never reaches
it: **latent, not live**. The sweep binary guards it so that all `5^L` strings
can be executed; the guard does not affect the sp high-water mark.

## VERDICT

**B6 is closed as a derived bound, and the documented fix is rejected.**
The correct allocation is `z_alloc(12*qlen - 8)`. `z_alloc(128)` is rejected:
it is not derived, it is not tight for any L, and it silently corrupts 8 bytes
at L=12. The frozen `z_alloc(64)` is vindicated as an exact L=6 bound.
Separately, the ledger's `panic` mechanism is corrected: on this toolchain the
defect is silent heap corruption.