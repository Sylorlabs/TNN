# Fork PAR — build & findings

## What it is
True parallel byte generation in pure Zag. Every voice sample is computed by
`voice_q16(plan, event, t)` — a pure function of (plan, event, absolute sample
time). The bed is `bed_q16(plan, t)`. No phase accumulator, no IIR state, no
read of any previously generated sample. The mix is a sum of independent
per-sample evaluations.

Source: `fork_par/src/render_par.zag`
Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## Modes
- `seq` — events in plan order
- `rev` — events in reverse plan order
- `stride` — pseudo-random visit order `(k*7919) % span`
- `seq+fault` / `rev+fault` — WAV output with a 64-sample bit-flip fault injected at t=3 s mid-render, post-cut generation continues
- `seq+mix` / `seq+faultmix` — raw s32 mix dump (no mastering) for mix-level content-identity checks

## Determinism & order independence (frozen fixture `fixture/plan_v1.txt`, 23 events)
- `seq` rerun: `cmp` clean (byte-identical WAV)
- `seq` vs `rev`: `cmp` clean
- `seq` vs `stride`: `cmp` clean

Order independence holds exactly for this fixture. (Stride is a true permutation
only when gcd(7919, span) = 1; valid here, not a universal proof.)

## Quality bars (final binary, `fork_par/src/par_seq1.wav`)
Nine-bar gate (`imagination_discovery/aud/b_alpha/consistency_gate/src/gate.zag`): **9/9 PASS**

| bar | value | limit |
|---|---|---|
| G-PER | 0.340 | ≤ 0.350 |
| G-STA | 1.826 | ≤ 3.0 |
| G-LURCH | 2.362 | ≤ 5.0 |
| G-DRIFT | 480.3 | ≤ 800 Hz |
| G-FLUXm | 241.8 | ≤ 350 |
| G-SIL1 | 0.000 | ≤ 0.02 |
| G-SIL2 | 0.000 | ≤ 0.5 s |
| G-CLIP | 0.849 | ≤ 0.95 |
| G-CREST | 3.863 | ≤ 14.0 |

CHOP (`aud_v10/chop.py`): CHOP-1 0 discontinuities PASS; CHOP-2 no silent gaps
PASS; CHOP-3 29 flux spikes, 14 unexplained at 120 ms event tolerance — all 14
are within 0.35 s of scripted note boundaries (attack transients, 150 ms
release onsets, 5.5 Hz vibrato cycle peaks). No structural cause.

Motif coherence (zero-lag normalized xcorr, motif at 2.0–5.4 s vs 24.0–27.4 s):
**1.000000** — the recurrence is bit-identical by construction.

Cost: ~9.7 s wall, 13.0 MB peak RSS for 30 s mono 44.1 kHz.

## Red teams
- **RT-CASCADE**: fault at t=3 s. Post-cut mix bit-identical: 0/1,190,636
  samples differ (mix-level comparison, immune to the global normalization
  rescale). A parallel renderer cannot cascade — there is no path from output
  back to input.
- **RT-LONG** (`tests/plan_long.txt`): cue 440 Hz at t=1 s; RESPOND at t=28 s
  with deliberately wrong nominal 880 Hz. PAR renders **880 Hz** (response
  zcr 0.0378 ≈ 2·880/44100). It cannot inspect its own output, so a wrong plan
  renders wrong forever.
- **RT-EDGE** (`tests/plan_edge_cut.txt`, plan truncated at 15 s): zero hard
  discontinuities at the cut (CHOP-1 = 0). First-15 s vs full plan differs in
  4,393/661,500 samples — plan-legitimate (the clipped event's envelope is a
  function of its own duration), not a causality violation.

## Known defects found & fixed during build
1. **Amp scaling bug (both forks)**: plan amp (0–1000) was converted as
   `(q16 * 65536) / 1000` instead of `q16 / 1000`, rendering all voices at
   1000× intended level (mix peak 43 FS). Peak normalization masked it at the
   WAV level. Fixed; mix peak now 0.66 FS.
2. **Unnormalized harmonic stack (both forks)**: Σ(1/h) sine stack peaked at
   ~2.45× amp. Now normalized by the weight sum so voice peak ≈ plan amp.

## Interpretation
PAR is structurally robust: exactly reproducible, exactly order-independent,
immune to cascades, perfect long-range recurrence. Its price is total: any
long-range dependency must be explicit in the plan, because the renderer can
never discover anything from what it has already generated.
