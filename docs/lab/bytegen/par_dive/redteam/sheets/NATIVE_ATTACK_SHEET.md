# PAR_DIVE RED TEAM — NATIVE (hybrid v2) attack sheet

Date: 2026-09-24. Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Harness: `redteam/src/rt_hyb_attack.zag` (extends inherited `work/src/rt_hyb_attack.zag`
with true single-bit `sb1`/`sb1mix` modes). Meter: `redteam/src/meter.zag`
(`blocks`, `postcut`, `zcr`, `peak`; sign-correct `g32s` reads).
Fixture: `~/workspace/bytegen/fixture/plan_v1.txt` (30 s, 44.1 kHz, mono).
All renders byte-identical across reruns (`cmp` clean).

Baseline: 1292 blocks, 0 detector false positives, peak 43337.

## A1 — sustained 1292-block corruption (inherited attacks, independently reproduced)

| Attack | Mode | Result | Verdict |
|---|---|---|---|
| A1a gross XOR 0x7FFFFFFF, 64 samp/block | `susfaultmix` | 1292/1292 flagged+healed, 0 differing samples vs clean | DEFENDED |
| A1b sub-band XOR bit13 (8192), 64 samp/block | `sus5mix`-family | 0/1292 flagged; 82,688 diffs persist; 1292/1292 blocks differ; exactly 64 diffs/block | **ATTACK_WORKS** |
| A1c DC +3277 (~0.05 FS) every sample | `susdcp`-family | 0/1292 flagged; 1,323,000 diffs persist; every block differs; peak 43337→46506 | **ATTACK_WORKS** |
| A1d zero first 512 samp of every 1024-block | `susz`-family | 2/1292 flagged+healed; 660,266 diffs persist; 1290/1292 blocks still differ | **ATTACK_WORKS** |

The exception detector catches only gross rail-scale corruption. In-band
perturbations (single-bit-13, small DC, half-block silence) pass through
untouched and persist in the output.

## A2 — RT-CASCADE (true single-bit fault at t=3 s, sample 132300)

`sb1mix`: flip bit 13 of exactly sample 132300 pre-detector.
`postcut` cut=132300: **prediff=0, postdiff=1** (first=last=132300).
The single corrupt sample persists; zero downstream propagation.
Verdict: **DEFENDED** against cascade (no recovery/heal of the bit itself —
the detector never fires on a single in-band bit).

## A3 — parser rail-pins (fail-open)

14-plan fuzz corpus (`plans/fz_*.txt`): all runs rc=0, **no parser rejection
anywhere**. Extreme amplitude 1e9 accepted (output hits signed rail,
peak=2147483648 abs); frequency 1e18 accepted; negative fields accepted;
non-numeric tokens silently coerced (1 event rendered); short EVENT silently
dropped (0 events); 200 EVENTs silently capped at 64; malformed RESPOND
accepted with overflowed nominal (21 detector fault blocks/heals).
Verdict: **ATTACK_WORKS** — parser has no rail validation and fails open.
(NEW beyond inherited A1b/A1c/A1d.)

## A4 — RESPOND attacks

| Attack | Cue / nominal | Sensor | Latch | Verdict |
|---|---|---|---|---|
| octave lie up | 440 / 880 | fm=456 | k=-1 → 440 | DEFENDED |
| octave lie down | 440 / 220 | fm=456 | k=+1 → 440 | DEFENDED |
| two-octave lie | 220 / 880 | fm=215 | k=-2 → 220 | DEFENDED |
| near-miss 460/460 | 460 / 460 | fm=457 | k=0, nominal kept | DEFENDED (octave-only by design) |
| near-miss 440/460 | 440 / 460 | fm=456 | k=0, nominal 460 kept | DEFENDED (77-cent lie not corrected — documented behavior) |
| polyphonic 440+554 | — / 880 | nvoice=2 | abstain, nominal kept | DEFENDED (fail-safe; no polyphonic pitch) |
| deep vibrato 300¢ | 440 / 880 | fm=578 | k=-1 → 440 | DEFENDED |
| glide +440 Hz | 440 / 880 | fm=0 | stationarity gate fails, nominal kept | DEFENDED (safe abstention) |
| **low cue 30 Hz** | 30 / 880 | **fm=79** | **k=-3 → 110 Hz** | **ATTACK_WORKS** |
| high cue 5000 Hz | 5000 / 880 | fm=4683 | out-of-range, nominal kept | DEFENDED |
| harmonic timbre-13 | 110 / 220 | fm=109 | → 110 | DEFENDED |

The 30 Hz trap: harmonics/ZCR turn an out-of-range 30 Hz cue into a false
in-range 79 Hz estimate; the octave corrector then latches nominal 880 down
to 110 Hz instead of the true 30 Hz. (NEW beyond inherited failures.)

## A5 — cross-region leakage

`xr_alt` adds an EVENT at t=0.5 s (region 0). Full `seqmix` vs fixture clean:
`postcut` cut=132300: **prediff=17499, postdiff=0**. Region 0's extra event
never leaks into regions 1+. Verdict: **DEFENDED**.

## A6 — order permutation

N/A (NATIVE is sequential AR; order is its semantics). Covered on contenders.

## A7 — long-horizon t=1→t=28 call-response

Plans `lh_cue{440,220,460}`: cue EVENT at t=1 s, RESPOND nominal 880 at t=28 s.
Late response window [28 s, 29 s] ZCR:
- cue 440 → ~425 Hz (nominal 880 latched down to 440, k=-1)
- cue 220 → ~217 Hz (latched to 220, k=-2)
- cue 460 → ~425 Hz (latched to 440, k=-1)
The response at t=28 depends on the cue from 27 s earlier. Verdict:
**DEFENDED** (long-horizon constraint honored via sensor latch).

## A8 — silence as memory

`sil_a` (440 @0.5 s, 880 @20 s) vs `sil_b` (220 @0.5 s, 880 @20 s) vs `sil_c`
(no early event, 880 @20 s):
- sil_a vs sil_b: 44,049 diffs, ALL before t=1.5 s (the differing early
  event); **0 diffs** from t=1.5 s through the 18.5 s silence and the t=20
  event (`postcut` cut=882000: postdiff=0).
- sil_a vs sil_c: 43,913 prediffs, 0 postdiffs.
- Silence region ZCR ≈110 Hz = bed only.
Verdict: **DEFENDED** — silence holds no state; the late event is
bit-identical regardless of history.

## Byte-identical reruns

Every attack output re-rendered; `cmp` clean in all cases.

## Headline

NATIVE breaks in **four** places beyond the inherited detector gaps:
three inherited (A1b sub-band, A1c DC, A1d half-zero — detector blind to
in-band corruption) and two NEW: (1) the parser fails open on every
rail-pin/malformed input tested (no rejection, silent coercion/cap/overflow);
(2) the 30 Hz harmonic trap (false in-range ZCR 79 Hz → wrong octave latch
to 110 Hz). RT-CASCADE, cross-region, long-horizon, and silence probes all
hold.
