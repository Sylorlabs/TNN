# PAR_DIVE RED TEAM — Contender A (pure PAR end-to-end) attack sheet

Date: 2026-09-24. Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Binary: `contender_a/src/render_a` (rebuilt from `render_a.zag`; i32 mix `.s32`).
Fixture: `~/workspace/bytegen/fixture/plan_v1.txt`.

## A2 — RT-CASCADE

`seq+fault1mix`: true single-bit fault (bit 13 of sample 132300) during
generation. `postcut` cut=132300: **prediff=0, postdiff=1** (sample 132300
only). Generation never reads the mix, so no cascade is possible by
construction. Verdict: **DEFENDED**.

## Sustained 1292-block corruption

`sustain+mix`: per-block XOR with a deterministic block-indexed pattern during
generation. vs clean: **1,322,969 differing samples, 1292/1292 blocks differ**
(31 samples where pattern XOR is identity). A has no exception detector by
design (pure PAR); corruption persists exactly. Verdict: **ATTACK_WORKS**
trivially — but A claims no recovery story, so this is documented as
out-of-scope-by-design rather than a broken promise.

## A3 — parser rail-pins

Same 14-plan fuzz corpus as NATIVE: all rc=0, no rejections. 1e9 amplitude
accepted (peak=2147483648, signed rail); 1e18 frequency accepted; negative
fields accepted; non-numeric coerced; short EVENT dropped; 200 EVENTs capped
at 64 (peak=1963119, no clipping protection). Verdict: **ATTACK_WORKS**
(fail-open parser, same as NATIVE).

## A4 — RESPOND attacks

A renders the plan's nominal pitch; it cannot measure output (pure f(plan,t)).
Response window [28 s, 29 s] ZCR on all 11 plans:

| Plan | Cue / nominal | Response | Verdict |
|---|---|---|---|
| octlie | 440 / 880 | ~841 Hz (880) | DEFENDED (nominal) |
| octlie_low | 440 / 220 | ~220 Hz | DEFENDED |
| 2oct | 220 / 880 | ~841 Hz (880) | DEFENDED |
| nearmiss/nearmiss2 | 440 / 460 | ~446 Hz (460) | DEFENDED |
| poly | 440+554 / 880 | ~841 Hz (880) | DEFENDED |
| vibdeep | 440 / 880 | ~841 Hz (880) | DEFENDED |
| glide | 440 / 880 | ~841 Hz (880) | DEFENDED |
| cue30 | 30 / 880 | ~841 Hz (880) | DEFENDED |
| cue5000 | 5000 / 880 | ~841 Hz (880) | DEFENDED |
| harm13 | 110 / 220 | ~217 Hz (220) | DEFENDED |

A is immune to every cue attack by deafness — including the 30 Hz harmonic
trap (no sensor to fool). Caveat: it also cannot answer a legitimate cue;
"defended" here means "cannot be tricked", not "responds correctly".

## A5 — cross-region leakage

`xr_base` vs `xr_alt` (extra EVENT at t=0.5 s), `seq+mix`:
`postcut` cut=132300: **prediff=17499, postdiff=0**.
Verdict: **DEFENDED** (pure f(plan,t) — no regions to leak across).

## A6 — order permutation (§5 required: A scrambled-order identity)

All vs `seq+mix` clean, byte-for-byte:
- `evperm+mix` (deterministic event permutation): **bit-identical** (`cmp` clean)
- `blocked+mix` (1024-sample block tiling): **bit-identical**
- `rev` (reverse event order): WAV **identical** to `seq` WAV
- `stride` (strided event order): WAV **identical** to `seq` WAV
Verdict: **DEFENDED** — pure PAR is visit-order invariant, as claimed.

## A7 — long-horizon t=1→t=28

`lh_cue{440,220,460}`: response at t=28 is the nominal 880 Hz in all three
cases (A ignores the cue). The long-horizon call→response relation is NOT
honored — A cannot hear the call. Verdict: **INCONCLUSIVE** as a response
mechanism (immune to trickery, incapable of answering).

## A8 — silence as memory

N/A by construction (no state). The t=20 event renders identically regardless
of history — trivially, since nothing is carried.

## Byte-identical reruns

All attack outputs re-rendered; `cmp` clean. (11/11 B-clean runs are the only
divergence observed in the whole campaign, and that was contender B.)

## Headline

A's core claim (order-invariant pure PAR) holds under every permutation
tested. It is immune to all sensor/cue attacks by construction, at the cost
of never answering. Its parser fails open exactly like NATIVE's. It promises
no corruption recovery and delivers none.
