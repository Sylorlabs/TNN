# Contender C — red-team report (frozen §5 + Attacks 4/9/11)

All attacks run against the final source
(SHA-256 `0640f28fe1496d614d45c7480ea0dd211bb76fc24d4549a2433fc07a26c6d3db`).
Fixtures: `tests/plan_*.txt`. Key: every attack either fails to break C or
breaks it in a documented, bounded way.

## Attack 4 — rail-pin / 2-cycle attempts (the servo's kill zone)

**Verdict: SURVIVED.** Four settling traces:

1. **Slow RMS ramp through the old rail-pin point** (`plan_ramp.txt`:
   dense slow amplitude ramp, one active region): 23 adaptations, 951
   plan-silence holds, gain 1.0000–1.3734, zero vetoes, zero rail pins.
   The gain tracks the ramp and parks — no runaway.
2. **Alternating loud/quiet regions** (`plan_alt.txt`): the loud region's
   first update reconstructs exactly from the unity reset; the quiet
   region's entry holds exact unity because the plan target is below the
   silence floor. Region reset proven, not assumed.
3. **Contraction proof (stationary target):** for constant plan content
   (`S` = plan-pure block RMS, `T` = target), the update is
   `g_{n+1} = (g_n + T/S)/2` — Lipschitz 1/2 toward the unique fixed point
   `T/S`. Empirically (`plan_rail1.txt`): T/m = 1.191 → g 1.0000 → 1.0957
   (exactly halfway); T/m = 1.121 → 1.0957 → 1.1619 (exactly halfway).
   Banach forbids 2-cycles for stationary targets; the 10 % deadband parks
   the orbit inside ±10 %; the [0.5, 2.0] clamp is a convex projection.
4. **Settling after corruption stops** (`sus5`: first 5 s corrupted, then
   clean): 0 output diffs after 5 s, 0 gain-trajectory diffs from clean —
   the servo re-settles, it does not 2-cycle.

**Plan-text rail pins** (`plan_rail1.txt` extreme amplitude,
`plan_rail2.txt` rapid loud/quiet alternation in one region): gain
1.0000–1.1856 (5 adapts) and 1.0000–1.3572 (7 adapts). No pin — the
clamp + deadband + plan-derived target (not measured-output chasing) make
rail text inert.

## Sustained 1292-block corruption (frozen §5, literal)

`sus1292` corrupts exactly 1292 flat 1024-sample blocks
(1292×1024 = 1,323,008 ≥ 1,323,000 fixture samples — the whole fixture):
1295/1295 region-split blocks vetoed, 82,880 corrupted samples differ,
**gain trajectory 1295/1295 blocks bit-identical to clean**,
gain range under attack 0.8763–1.1574 (never pinned, never railed).
The veto remeasures from an exact plan-pure re-render (same integer
arithmetic as the clean path); corrupted bytes stay corrupted, only servo
state is protected.

## Polyphonic RESPOND

`plan_long_poly.txt` (two simultaneous cue voices): `nvoice=2` → latch
refuses (`rsn=0`), renders the plan nominal. No hallucinated pitch.

## Sub-octave nominal lies

- Nominal 220 Hz, true cue 440 Hz: `k=+1 → LATCHED f0=440Hz`, renders
  **440.02 Hz (+0.1¢)**. The lie is corrected UP.
- Nominal 1760 Hz, true cue 440 Hz: `k=−2 → LATCHED f0=440Hz`, renders
  **440.02 Hz (+0.1¢)**. Two octaves corrected DOWN.

## Vibrato / glide vs the ZCR sensor

- Heavy vibrato cue (100-cent 8 Hz): measured 454 Hz, `k=−1 → LATCHED`,
  renders 440.02 Hz (+0.1¢). Vibrato does not fool the octave detector.
- Glide cue (200-cent glide across the window): ZCR halves disagree
  (`rsn=1`) → keeps the nominal 880 Hz, renders 880.04 Hz (+0.1¢).
  Honest abstention, not a guess.

## Silence-as-memory

`plan_silmem.txt` (loud event @ 1 s, 12 s gap, quiet event @ 14 s):
the quiet event lands in a new region (gap ≥ 0.5 s) whose gain resets to
exact unity — entry gain 1.0000, max 1.0000. Stale gain cannot cross the
boundary; within a region, plan-silence blocks HOLD (never adapt), so
silence carries no memory either. Structurally impossible, verified.

## Cross-region leakage

Fixture + injected loud event in region 0: 66,093 sample diffs before the
2.0 s boundary, **0 diffs after**. The reset is real, not a comment.

## No-plan-mutation audit

Post-parse `evs` calls: zero (verified by inspection). The old latch's
plan rewrite and the dead hybrid `render_events` path were deleted
2026-09-24; the octave correction lives in the separate `ovr` arena.
RT-LONG re-verified after the repair: 440.02 Hz (+0.1¢) — unchanged.

## Remaining §5 items

- **Parallel-order permutation**: N/A — C is block-sequential by design
  (contender A's attack, not C's).
- **NATIVE under the same attacks**: NATIVE/PAR have no servo and no
  latch; rail text, sustained corruption, and polyphonic cues are inert
  against them by construction (nothing to pin, nothing to latch).
  Documented as not-applicable rather than tested.

## Scorecard

| Attack | Result |
|---|---|
| rail-pin text (×2) | survived, gain ≤ 1.36 |
| slow ramp / alternating regions | settles, resets |
| stationary-target contraction | 1/2-contraction, empirical exact |
| post-corruption settling | 0 diffs after recovery |
| sustained 1292-block | 1295/1295 vetoed, trajectory = clean |
| polyphonic RESPOND | refused, nominal kept |
| sub-octave lies (220/1760) | both corrected to 440.02 Hz |
| vibrato vs ZCR | latched correctly |
| glide vs ZCR | abstained honestly |
| silence-as-memory | structurally impossible |
| cross-region leakage | 0 post-boundary diffs |
| plan mutation | zero post-parse writes |
