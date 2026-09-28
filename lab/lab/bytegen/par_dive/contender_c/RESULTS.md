# Contender C — results (frozen §2 battery + §5 red team)

Source: `src/render_c.zag`
(SHA-256 `0640f28fe1496d614d45c7480ea0dd211bb76fc24d4549a2433fc07a26c6d3db`,
2026-09-24 final — includes the no-plan-mutation repair and the `sus1292`
mode). All renders below are from this source unless noted.

## DET

Two fixture renders byte-identical (`cmp` clean, WAV level).

## QUALITY — 9 V10 gates (final binary, `c_final.wav`)

| Gate | C | Bar | Verdict |
|---|---|---|---|
| G-PER | 0.333 | — | PASS |
| G-STA | 2.020 | 3.000 | PASS |
| G-LURCH | 2.518 | 5.000 | PASS |
| G-DRIFT | 477.143 | 800.000 | PASS |
| G-FLUXm | 242.649 | 350.000 | PASS |
| G-SIL1 | 0.000 | 0.020 | PASS |
| G-SIL2 | 0.000 | 0.500 | PASS |
| G-CLIP | 0.849 | 0.950 | PASS |
| G-CREST | 4.324 | 14.000 | PASS |

GATE: PASS (9/9).

## QUALITY — CHOP-1/2/3 (`aud_v10/chop.py`, complete 271-event list)

| Check | C | PAR | Verdict |
|---|---|---|---|
| CHOP-1 hard discontinuities | 0 | 0 | PASS |
| CHOP-2 silent gaps ≥150 ms | none | none | PASS |
| CHOP-3 flux spikes | 41 total, **0 unexplained** | 29 total, 0 unexplained | PASS with caveat |

Caveat (honest): C has 12 extra supra-threshold flux spikes vs PAR, all
within the explanation window of complete-list timestamps (attack/release/
vibrato transients). 6 of the 14 C-only spikes sit within 12 ms of a
servo-adapt block boundary; the rest are servo-amplified vibrato extrema.
The servo is not sonically transparent at the flux level — its gain steps
are sub-threshold individually (CHOP-1 clean) but add detectable flux.
Whether this counts as a "regression" under §6's "no regression elsewhere"
is a judgment call; the frozen CHOP-3 bar (0 unexplained) passes.

## COHERENCE (motif 2.0–5.4 s vs 24.0–27.4 s)

| Metric | C | NATIVE/PAR |
|---|---|---|
| zero-lag normalized xcorr | 1.000000 | ~1.0 |
| max-lag ±50 ms xcorr | 0.999999 @ lag 0 | ~1.0 |
| pitch-contour correlation | 1.000000 | — |
| centroid-proxy correlation | 1.000000 | — |
| IOI correlation | 1.000000 | — |
| onsets w1/w2 | 10 / 10 | — |

Coherence ≥ NATIVE: satisfied (tie at 1.000000). Note: the two motif
instances sit in different regions (1 and 5) with independent servo state,
yet correlate at 1.000000 — the servo is plan-deterministic.

## COST (same VM, interleaved, 5 runs each)

| | C | PAR |
|---|---|---|
| wall clock median | 8.15 s | 7.24 s |
| wall clock min | 7.00 s | 5.06 s |
| peak RSS | 13,056 KB | 12,928 KB |

VM noise dominates (5.06–11.64 s spread). No strict cost win claimable —
COST is a tie / no-win for C (+12 % median, +1 % RSS, both inside noise).

## RT-LONG (cue 440 Hz @ t=1 s, RESPOND @ t=28 s)

| Case | C response | PAR response |
|---|---|---|
| nominal 880 Hz (octave lie) | **440.02 Hz → +0.1 cents** | 880.04 Hz → +1200.1 cents |
| nominal 460 Hz (near-miss) | 460.05 Hz → +0.1 cents (kept nominal, correct) | 460.x (renders nominal) |

Latch trace (880 case): `fm=456Hz nom=880Hz k=-1 -> LATCHED f0=440Hz`.
**Strict C win on RT-LONG honest-cents.**

## RT-CASCADE (64-sample XOR @ t=3 s, mix level)

C: 64 in-window diffs, **0 post-cut diffs** (exact plan-pure remeasurement
after the veto). PAR: 0 post-cut diffs (no feedback at all). Tie — no
regression: C's servo does not propagate the fault.

## RT-EDGE (plan truncated @ 15 s)

- C cut vs C full first differs at **14.900 s** — identical to PAR cut vs
  PAR full (14.900 s). The 0.1 s lead is a release tail of a note starting
  before 15 s: legitimate in both.
- C cut vs PAR cut: max abs diff 0.13 FS (servo gain only), no
  edge-specific artifacts.
- CHOP-1 on cut renders: 0 discontinuities for both C and PAR.
- Tie — no regression.

## FAILURE MODES (where C breaks that others don't)

1. **Flux-level non-transparency** (see CHOP-3 caveat): 12 extra explained
   flux spikes from servo gain steps. PAR has none.
2. **Model-error deadband blindness**: block RMS errors ≤ 10 % vs the
   analytic target are never corrected (by design — the deadband is the
   rail-pin defense). A plan whose true level sits 9 % off the analytic
   model keeps that offset forever.
3. **Analytic-target pitch approximation**: the target uses nominal pitch,
   not latched override pitch (RMS-level effect, inside deadband).
4. **Dropout floor**: a 64-sample full dropout moves block RMS ×0.97 —
   below the veto detection floor (documented; full-block dropout @ t=3 s
   tested separately).
5. **RESPOND abstains are silent**: polyphonic cues, gliding cues, and
   out-of-range measurements keep the nominal with only a trace line —
   no in-band signal.

## §6 ADOPTION MATRIX

| §6 condition | Result |
|---|---|
| ≥ all 9 quality bars | 9/9 PASS |
| coherence ≥ NATIVE | 1.000000, tie |
| strict win ≥1 of {RT-LONG, cascade, edge, cost} | **RT-LONG: +0.1¢ vs +1200.1¢** |
| no regression elsewhere | cascade tie, edge tie, cost tie, DET pass, §5 survives; CHOP-3 spike-count delta disclosed as caveat |
| determinism | byte-identical reruns |
| §5 survival | all attacks survived (see REDTEAM_C.md) |

**Verdict: C satisfies the letter of the §6 overthrow clause** — strict
win on RT-LONG honest-cents, all bars pass, coherence ≥ NATIVE, no bar
failed, deterministic, §5 survived. One disclosed caveat (CHOP-3
41-vs-29 flux spikes, all explained) for the "no regression" judgment.
A tie retains NATIVE; on the letter this is not a tie.
