# PAR_DIVE RED TEAM — Contender C (PAR render, exception-veto servo) attack sheet

Date: 2026-09-24. Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Binary: `contender_c/src/render_c`. Output int32 LE via `mix_write`.
**Format trap found and fixed mid-campaign:** C's mode dispatch writes raw
`.s32` ONLY for `seqmix`/`faultmix`/`susfaultmix`/`dropoutmix`/`sus5mix`/
`sus1292mix` (no `+`); any other mode string (e.g. `seq+mix`) silently writes
**WAV** (44-byte RIFF header + int16) to the `.s32` path. Early fuzz/lh/xr
runs used `seq+mix` and were re-run as `seqmix`; all numbers below are from
raw-mode outputs. The RESPOND latch logs are format-independent.
Fixture: `~/workspace/bytegen/fixture/plan_v1.txt`. Clean peak: 49752.

## A2 — RT-CASCADE

`faultmix`: built-in fault injects 64 gross samples (NOT a true single bit —
a strict single-bit source variant was not built for C; this is a
red-team-harness limitation, flagged). vs clean: exactly **64 differing
samples**, no downstream propagation (`postcut`: prediff=0, postdiff=64
within the fault block, 0 after). C rerenders clean blocks for servo
measurement but never heals output bytes. Verdict: **DEFENDED** against
cascade; the 64 fault samples persist by design.

## Sustained 1292-block corruption

`susfaultmix` (per-block fault injection, all 1292 meter blocks):
- all 1295 internal C blocks vetoed by the servo
- vs clean: **198,529 differing samples, 1292/1292 blocks differ**,
  max 714 diffs/block, corrupted peak hit signed-rail magnitude 2147483648
- C protects its servo state by rerendering clean blocks for measurement,
  but explicitly does NOT heal output bytes.
Verdict: **ATTACK_WORKS** for output recovery; **DEFENDED** against
feedback-state cascade (servo state untainted).

## A3 — parser rail-pins

14-plan fuzz corpus, raw `seqmix` mode, all rc=0, no rejections:

| Plan | Peak | Note |
|---|---|---|
| fz_base | 46065 | baseline |
| fz_many (200 events) | 1125195 | silently capped at 64, no clip guard |
| fz_rail_amp (1e9) | 2147483648 | signed rail hit, accepted |
| fz_rail_freq (1e18) | 31326 | accepted, rendered |
| fz_rail_dur | 46154 | accepted |
| fz_neg | 12919 | negative fields accepted |
| fz_nonnum | 12919 | non-numeric coerced, bed-only-like |
| fz_short | 12919 | short EVENT silently dropped |
| fz_empty | 0 | silence emitted, rc=0 |
| fz_bed_bad | 33399 | accepted |
| fz_glide / fz_vib / fz_timbre | 45700 / 38558 / 46953 | extreme values accepted |
| fz_resp_bad | 46085 | malformed RESPOND accepted |

Verdict: **ATTACK_WORKS** — fail-open parser, same family as NATIVE.

## A4 — RESPOND attacks (NATIVE-like sensor latch)

| Plan | Cue / nominal | Sensor → latch | Verdict |
|---|---|---|---|
| octlie | 440 / 880 | fm=456 k=-1 → 440 | DEFENDED |
| octlie_low | 440 / 220 | fm=456 k=+1 → 440 | DEFENDED |
| 2oct | 220 / 880 | fm=215 k=-2 → 220 | DEFENDED |
| nearmiss/nearmiss2 | 440 / 460 | fm=456/457 k=0 → nominal | DEFENDED |
| poly | 440+554 / 880 | nvoice=2 → abstain | DEFENDED |
| vibdeep | 440 / 880 | fm=578 k=-1 → 440 | DEFENDED |
| glide | 440 / 880 | fm=0 rsn=1 → abstain | DEFENDED |
| **cue30** | 30 / 880 | **fm=79 k=-3 → 110 Hz** | **ATTACK_WORKS** |
| cue5000 | 5000 / 880 | fm=4683 rsn=2 → reject | DEFENDED |
| harm13 | 110 / 220 | fm=109 k=-1 → 110 | DEFENDED |

C inherits NATIVE's sensor verbatim, including the **30 Hz harmonic trap**:
false in-range 79 Hz estimate → wrong octave latch 880→110 Hz.
Verdict: **ATTACK_WORKS** on cue30; DEFENDED on the other 9.

## A5 — cross-region leakage

`xr_base` vs `xr_alt` (extra EVENT at t=0.5 s, region 0), raw `seqmix`:
`postcut` cut=132300: **prediff=66076, postdiff=0**. C's region-boundary
reset holds. Verdict: **DEFENDED**.

## A6 — order permutation

Not separately run for C (C's region renderer is plan-order driven like A's
within-region event list; the §5 order-permutation requirement names A
explicitly). Verdict: **INCONCLUSIVE** (untested).

## A7 — long-horizon t=1→t=28

`lh_cue{440,220,460}`, response window [28 s, 29 s] ZCR:
- cue 440 → ~425 Hz (440 latched, k=-1)
- cue 220 → ~217 Hz (220 latched, k=-2)
- cue 460 → ~425 Hz (440 latched, k=-1)
The t=28 response tracks the t=1 cue through the sensor latch.
Verdict: **DEFENDED**.

## A8 — silence as memory

Covered by A5's boundary reset (state is per-region; silence carries nothing
across regions). Verdict: **DEFENDED** (by the reset mechanism).

## Byte-identical reruns

All attack outputs re-rendered; `cmp` clean. No B-style divergence observed.

## Headline

C's servo defends its internal state (vetoes + boundary reset hold), but it
**inherits both of NATIVE's headline failures**: the fail-open parser and
the 30 Hz harmonic-trap latch. Output recovery is explicitly not attempted —
sustained corruption persists in the bytes. Separately: C's silent WAV
fallback on unrecognized mode strings is a footgun (bytes change format
without error), found and worked around during this campaign.
