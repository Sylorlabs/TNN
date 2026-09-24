# PAR_DIVE RED TEAM — Contender D2 (PAR render, plan-referential cue + integrity gate) attack sheet

Date: 2026-09-24. Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Binary: `contender_d/src/render_d2`. Output int32 LE.
Fixture: `~/workspace/bytegen/fixture/plan_v1.txt`.

D2's confirmed behavior: RESPOND latches to the PLAN's cue pitch (no sensor);
an integrity byte-compare gate on the cue path abstains (code 3) when the cue
bytes are tampered. General output has no detector.

## A2 — RT-CASCADE

`faultmix`: built-in fault injects 64 gross samples (not a true single bit —
strict variant not built; flagged). vs clean: exactly **64 differing
samples**, no downstream propagation. Verdict: **DEFENDED** against cascade;
the 64 fault samples persist.

## Sustained corruption

`susfaultmix` vs `seq+mix` clean: **82,688 differing samples, 1292/1292
blocks differ, exactly 64 diffs/block**, peak 43337→2147483648. D2's
integrity gate covers only the RESPOND cue path — general output corruption
is not detected or healed. Verdict: **ATTACK_WORKS** (output recovery).

## A3 — parser rail-pins

14-plan fuzz corpus: all rc=0, no rejections. Same fail-open family:
200 events capped at 64 (peak=1963119), 1e9 amplitude → rail
(peak=2147483648), non-numeric coerced, short dropped, negative/extreme
accepted. Verdict: **ATTACK_WORKS**.

## A4 — RESPOND attacks (plan-referential cue + integrity gate)

| Plan | Cue / nominal | Log | Verdict |
|---|---|---|---|
| octlie | 440 / 880 | LATCHED 440 | DEFENDED |
| octlie_low | 440 / 220 | LATCHED 440 | DEFENDED |
| 2oct | 220 / 880 | LATCHED 220 | DEFENDED |
| nearmiss (cue 460) | 460 / 460 | LATCHED 460 | DEFENDED |
| nearmiss2 (cue 440) | 440 / 460 | LATCHED 440 (cue, not nominal) | DEFENDED |
| poly | 440+554 / 880 | ABSTAIN code=1 | DEFENDED |
| vibdeep | 440 / 880 | LATCHED 440 | DEFENDED |
| glide | 440 / 880 | LATCHED 440 | DEFENDED |
| cue30 | 30 / 880 | LATCHED 30 (plan's cue) | DEFENDED — no sensor to trap |
| cue5000 | 5000 / 880 | LATCHED 5000 (plan's cue) | DEFENDED — plan obedience |
| harm13 | 110 / 220 | LATCHED 110 | DEFENDED |

D2 has no pitch sensor, so vibrato/glide/harmonic/30 Hz sensor attacks cannot
bite — it renders the plan's cue pitch. The integrity gate (code 3) fires
only on cue-byte tampering, which the plan corpus never triggers. Note: D2
will render a 30 Hz or 5000 Hz "response" if the plan says so — that is plan
obedience, not a vulnerability, but it means D2's safety rests entirely on
plan provenance.

## A5 — cross-region leakage

`xr_base` vs `xr_alt` (extra EVENT at t=0.5 s), raw `seq+mix`:
`postcut` cut=132300: **prediff=17499, postdiff=0**. Verdict: **DEFENDED**.

## A6 — order permutation

`rev` / `stride` modes write peak-normalized WAV; compared byte-for-byte
against a clean WAV (empty mode → order 0 + WAV): **rev identical, stride
identical** (`cmp` clean). Verdict: **DEFENDED**.

## A7 — long-horizon t=1→t=28

`lh_cue{440,220,460}`, response window [28 s, 29 s] ZCR:
- cue 440 → ~425 Hz (440)
- cue 220 → ~217 Hz (220)
- cue 460 → ~446 Hz (460)
The t=28 response follows the plan's t=1 cue pitch exactly.
Verdict: **DEFENDED** (long-horizon relation honored via plan reference).

## A8 — silence as memory

`sil_a` (440 @0.5 s, 880 @20 s) vs `sil_b` (220 @0.5 s, 880 @20 s) vs
`sil_c` (880 @20 s only), raw `seq+mix`, `postcut` cut=882000 (t=20 s):
- sil_a vs sil_b: prediff=44049, **postdiff=0**
- sil_a vs sil_c: prediff=43913, **postdiff=0**
Verdict: **DEFENDED** — no state survives the silence.

## Byte-identical reruns

All attack outputs re-rendered; `cmp` clean.

## Headline

D2's plan-referential design makes it immune to every sensor attack —
including the 30 Hz trap — but its safety is plan-provenance all the way
down: it renders whatever pitch the plan's cue says, and its integrity gate
does not cover general output corruption (sustained fault persists
untouched). Fail-open parser like the rest.
