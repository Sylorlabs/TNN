# CREW A — fork A-poly: dense-polyphony N=1/2/4/8/16/32. Results 2026-09-24.

## Plans
`plans/plan_chord{N}.txt`: N simultaneous voices, whole-tone stack from A3
(220 Hz), EVENT 2.0–3.0 s, amp 500, all on the 30 s fixture chassis.
`plans/plan_solo32_{k}.txt`: 32 individual voices of the N=32 chord.
`plans/plan_chord32g.txt`: N=32 gain-staged (amp 88 = 500/√32,
power-preserving). All rerendered twice — byte-identical.

## Measurements (raw MIX, chord region 2–5 s; i16FS = 32768)
| N | peak (i16FS) | clipfrac | RMS | ZCR |
|---|---:|---:|---:|---:|
| 1 | 0.664 | 0.0000 | 0.3454 | 716 Hz |
| 2 | 1.325 | 0.0370 | 0.4880 | 930 Hz |
| 4 | 2.442 | 0.1536 | 0.6901 | 1,064 Hz |
| 8 | 3.991 | 0.3567 | 1.0822 | 1,394 Hz |
| 16 | 6.394 | 0.5627 | 1.7741 | 2,606 Hz |
| 32 | 10.309 | 0.7066 | 2.7246 | 8,960 Hz |
Clipping at any i16 output stage from N=2 up. A has **no output-adaptive
behavior** — the plan-exact linear sum is rendered verbatim.

## vs NATIVE servo-AR (actual `render_nat`, frame-1024 output-servo AGC)
| N | nat peak | nat clipfrac | nat RMS | nat ZCR |
|---|---:|---:|---:|---:|
| 16 | 4.476 | 0.3539 | 1.0780 | 1,908 Hz |
| 32 | 5.764 | 0.5331 | 1.5822 | 7,590 Hz |
max|par−nat| N=32 = **4.793 FS**. The servo drives AGC to its 0.5 floor and
darkens timbre during the chord — RMS ≈ halved, ZCR darkened. AR buys
headroom with gain/timbre deviation from the plan; **it does NOT preserve
plan-exactness**. (Note: `render_fn nat` — no servo — matches A to 0.0138 FS;
the self-limiting is the servo's, not carried accumulators'. Also note:
`render_nat` mode string is `seqmix`, NOT `seq+mix` — the latter silently
writes 16-bit WAV; caught during this fork.)

## Structure (A)
- **Linearity**: Σ(32 solos) == chord mix, max|d| = **0** — perfect linear
  superposition, deterministic.
- **Masking**: per-voice↔sum correlation mean 0.2465 (min 0.2045, max
  0.2852) vs 1/√32 = 0.1768 — coherent above the incoherent baseline from
  harmonic overlap in the whole-tone stack; real deterministic masking
  structure.
- **ZCR-of-sum tracks the highest voice**, consistent with the dive.

## Mitigation (plan-level)
Gain-staged N=32 (amp 88): peak 1.814 i16FS, clipfrac 0.0365 (was 0.7066),
RMS 0.4794 — byte-identical on rerun. Clipping is manageable **at plan
level**, but the renderer itself performs no adaptation.

## Fork verdict: CONFIRMED REGRESSION vs native on dense sums.
## PAR preserves the plan bit-exactly and clips downstream; the servo-AR
## halves RMS and darkens to self-limit at the price of 4.79 FS deviation
## from plan-exactness. Neither is "wrong" — they optimize different things.
## This is a genuine tradeoff loss for A, standing against A's coherence/
## statelessness wins.
