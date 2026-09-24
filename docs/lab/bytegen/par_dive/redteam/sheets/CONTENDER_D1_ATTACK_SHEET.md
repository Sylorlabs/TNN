# PAR_DIVE RED TEAM — Contender D1 (PAR render, nominal-only) attack sheet

Date: 2026-09-24. Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Binary: `contender_d/src/render_d1`. Output int32 LE.
Fixture: `~/workspace/bytegen/fixture/plan_v1.txt`.

D1's confirmed behavior: renders the plan's nominal pitch; no output
measurement (like A). Its RESPOND outputs match A's.

## A2 — RT-CASCADE

`seq+faultmix`: built-in fault injects 64 gross samples (not a true single
bit — strict single-bit variant not built; flagged as harness limitation).
vs clean: exactly **64 differing samples**, no downstream propagation.
D1 never reads its output buffer. Verdict: **DEFENDED** against cascade
(by construction); the 64 fault samples persist.

## Sustained corruption

`seq+susfaultmix` vs `seq+mix` clean: **82,688 differing samples,
1292/1292 blocks differ, exactly 64 diffs/block**, peak 43337→2147483648
(signed rail). D1 has no detector; corruption persists exactly.
Verdict: **ATTACK_WORKS** (no recovery claimed).

## A3 — parser rail-pins

14-plan fuzz corpus: all rc=0, no rejections. Same fail-open family as
NATIVE/A/B: 200 events capped at 64 (peak=1963119), 1e9 amplitude → signed
rail (peak=2147483648), non-numeric coerced, short dropped, negative/extreme
accepted. Verdict: **ATTACK_WORKS**.

## A4 — RESPOND attacks

D1 renders nominal only (confirmed: D1 RESPOND outputs match A's).
Response window [28 s, 29 s] ZCR:

| Plan | Cue / nominal | Response | Verdict |
|---|---|---|---|
| octlie | 440 / 880 | ~841 Hz (880) | DEFENDED |
| octlie_low | 440 / 220 | ~217 Hz (220) | DEFENDED |
| 2oct | 220 / 880 | ~841 Hz (880) | DEFENDED |
| nearmiss/nearmiss2 | 440 / 460 | ~446 Hz (460) | DEFENDED |
| poly | 440+554 / 880 | ~841 Hz (880) | DEFENDED |
| vibdeep | 440 / 880 | ~841 Hz (880) | DEFENDED |
| glide | 440 / 880 | ~841 Hz (880) | DEFENDED |
| cue30 | 30 / 880 | ~841 Hz (880) | DEFENDED |
| cue5000 | 5000 / 880 | ~841 Hz (880) | DEFENDED |
| harm13 | 110 / 220 | ~217 Hz (220) | DEFENDED |

Immune to all cue attacks by deafness (including the 30 Hz trap).
Caveat: cannot answer a legitimate cue either.

## A5 — cross-region leakage

`xr_base` vs `xr_alt` (extra EVENT at t=0.5 s), raw `seq+mix`:
`postcut` cut=132300: **prediff=17499, postdiff=0**. (Expected by
construction — pure f(plan,t) — confirmed empirically.)
Verdict: **DEFENDED**.

## A6 — order permutation

`rev` / `stride` modes write peak-normalized WAV (D1's write dispatch only
emits raw for `seq+mix`/`seq+faultmix`/`seq+susfaultmix`); compared
byte-for-byte against a clean WAV (empty mode string → order 0 + WAV):
**rev identical, stride identical** (`cmp` clean). Verdict: **DEFENDED** —
visit-order invariant like A.

## A7 — long-horizon t=1→t=28

`lh_cue{440,220,460}`: response is 880 Hz (nominal) in all three — the cue
is ignored. Verdict: **INCONCLUSIVE** (immune to trickery, incapable of
answering).

## A8 — silence as memory

`sil_a` vs `sil_b`, `postcut` cut=882000: prediff=44049, **postdiff=0**.
(Empirical confirmation of the construction argument.)
Verdict: **DEFENDED**.

## Byte-identical reruns

All attack outputs re-rendered; `cmp` clean.

## Headline

D1 is A with a different name for red-team purposes: order-invariant pure
PAR, deaf to cues (immune to every RESPOND attack, including the 30 Hz
trap), fail-open parser, no corruption recovery. Nothing here contradicts
A's sheet.
