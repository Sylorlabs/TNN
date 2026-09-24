# BYTEGEN red-team report

Frozen plan: `fixture/plan_v1.txt` (30 s, 44.1 kHz mono; 110 Hz bed; 8-note
motif at 2.0–5.15 s repeated identically at 24.0–27.15 s; 23 events).
Final binaries built with the pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

All WAV-level comparisons below use `cmp` (byte-identity). Mix-level cascade
comparisons use raw s32 mix dumps (`seq+mix` / `seq+faultmix` / `seqmix` /
`faultmix` modes), because global peak normalization rescales every sample on
any content edit and would mask generation differences (standing house rule).

## Determinism
| check | result |
|---|---|
| PAR seq rerun | `cmp` clean |
| PAR seq vs rev | `cmp` clean |
| PAR seq vs stride | `cmp` clean |
| AR seq rerun | `cmp` clean (trace: 1,292 frames) |

## RT-CASCADE — fault injection at t = 3 s (64-sample bit-flip in mix)
Mix-level, post-cut region (samples 3 s + 64 → 30 s), 1,190,636 samples:

| fork | pre-cut differ | fault window differ | post-cut differ |
|---|---|---|---|
| PAR | 0 | 64 | **0** |
| AR | 0 | 64 | **5,791** (all within t = 3.0–3.14 s) |

- PAR: no cascade possible — generation never reads output. Proven at mix level.
- AR: cascade is real but self-limiting. Control trace: frame 130 (first frame
  analyzing the faulted frame) slams to agc 0.500 / bright +1 / vibmul 1.500;
  frame 131 overshoots (agc 1.697 / bright +3 / vibmul 0.589); damped
  oscillation; **bit-identical reconvergence by frame 137 (~160 ms)**.
  Not tested: sustained or adversarially crafted faults that could keep the
  servo saturated.

## RT-LONG — response dependency across 27 s (`tests/plan_long.txt`)
Cue: EVENT 440 Hz at t = 1.0–2.0 s. Response: RESPOND at t = 28.0–29.0 s with
source window 1.0–2.0 s and deliberately wrong nominal 880 Hz.

| fork | cue zcr (expect 0.0200 = 440 Hz) | response zcr |
|---|---|---|
| PAR | 0.0206 | **0.0378 (≈ 880 Hz)** — renders the wrong nominal |
| AR | 0.0206 | **0.0211 (≈ 440 Hz)** — infers pitch from its own 27 s-old output |

PAR structurally cannot inspect rendered output; a wrong plan renders wrong
forever. AR discovers the fact from generated output and discards the wrong
plan value. This is AR's one unique capability.

## RT-EDGE — unresolved plan cut at 15 s (`tests/plan_edge_cut.txt`)
Bed and events truncated at 15 s (one event clipped mid-note: 14.8 s + 0.2 s).

| fork | CHOP-1 at cut | first-15 s vs full plan |
|---|---|---|
| PAR | 0 discontinuities | 4,393/661,500 differ |
| AR | 0 discontinuities | 4,410/661,500 differ |

Both end the truncated plan cleanly (25 ms bed fade + 150 ms event release).
The first-15 s differences are plan-legitimate: the clipped event's envelope
is a function of its own duration. No causality violation in either fork.
Honest negative result: with envelope-smoothing renderers, a plan-level cut
does not discriminate AR from PAR — both are causal.

## Quality bars (final binaries)
Nine-bar gate: PAR 9/9 PASS, AR 9/9 PASS (closest: PAR G-PER 0.340 vs 0.350).
CHOP: PAR CHOP-1/2 PASS, CHOP-3 14 unexplained spikes (all ≤ 0.35 s from
scripted note boundaries — attack/release/vibrato transients); AR CHOP-1/2
PASS, CHOP-3 0 spikes (servo smooths attacks below threshold).
Motif coherence: PAR 1.000000, AR 0.741083.
Cost: PAR ~9.7 s / 13.0 MB; AR ~9.4 s / 13.1 MB (30 s render).

## Open attacks (not run)
- Sustained/adversarial fault against AR's servo (can it be kept derailed?).
- ZCR pitch inference on non-pure tones (RT-LONG used a clean 440 Hz cue;
  real audio would be harder).
- RT-LONG with multiple traps and with the cue itself corrupted.
