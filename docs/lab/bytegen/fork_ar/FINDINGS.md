# Fork AR — build & findings

## What it is
True autoregressive byte generation in pure Zag. Audio is generated in
1024-sample frames. Before rendering frame f > 0, the renderer **analyzes the
previously generated frame** from the mix buffer (RMS and zero-crossing rate)
and uses those measurements of its own output to set:
- **AGC gain** (target mix RMS 0.19; clamps 0.5–2.0),
- **harmonic brightness** (timbre −3…+13 from ZCR vs 0.016 target),
- **vibrato-depth multiplier** (0.5–1.5 from RMS ratio).

This closes a genuine output→input loop: frame f's synthesis parameters are a
function of generated output, not just the plan. RESPOND events infer their
pitch from the ZCR of previously rendered audio (ignoring a wrong nominal).
Oscillator phase is carried for continuity; an optional trace logs per-frame
(frame, agc_q16, bright, vibmul_q16).

Source: `fork_ar/src/render_ar.zag`
Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## Modes
- `seq` — with optional 4th arg = trace file path
- `fault` — WAV output with 64-sample bit-flip fault at t=3 s (servo reacts)
- `faultmix` / `seqmix` — raw s32 mix dump (no mastering) for mix-level checks

## Determinism (frozen fixture `fixture/plan_v1.txt`, 23 events)
- `seq` rerun: `cmp` clean (byte-identical WAV), trace 1,292 frames.

## The servo is alive (not saturated)
Early in the build the servo targets sat far from the plan's operating point
and the controller clamped. After calibrating targets to the plan's measured
medians (mix RMS ≈ 0.19, ZCR ≈ 0.016), the trace shows genuine regulation:
bed-only frames ride agc ≈ 1.6–2.0 / bright +3 / vibmul ≈ 0.55; when the motif
arrives (frame 86) the servo swings to agc ≈ 0.67–0.96 / bright −1…−2 /
vibmul 1.1–1.5. Brightness histogram spans the full −3…+3 range. This is
negative feedback on the renderer's own output, not a clamped constant.

## Quality bars (final binary, `fork_ar/src/ar_seq1.wav`)
Nine-bar gate: **9/9 PASS**

| bar | value | limit |
|---|---|---|
| G-PER | 0.282 | ≤ 0.350 |
| G-STA | 1.772 | ≤ 3.0 |
| G-LURCH | 2.341 | ≤ 5.0 |
| G-DRIFT | 419.3 | ≤ 800 Hz |
| G-FLUXm | 200.8 | ≤ 350 |
| G-SIL1 | 0.000 | ≤ 0.02 |
| G-SIL2 | 0.000 | ≤ 0.5 s |
| G-CLIP | 0.849 | ≤ 0.95 |
| G-CREST | 5.258 | ≤ 14.0 |

CHOP: CHOP-1 0 discontinuities PASS; CHOP-2 no silent gaps PASS; CHOP-3 **0
spikes total** — the servo's gain-riding smooths note attacks below the flux
threshold (a behavioral difference from PAR, not necessarily a virtue).

Motif coherence (motif at 2.0–5.4 s vs 24.0–27.4 s): **0.741083**. The
recurrence is recognizable but measurably altered by 22 s of intervening
output history feeding the servo.

Cost: ~9.4 s wall, 13.1 MB peak RSS — no meaningful difference from PAR.

## Red teams
- **RT-CASCADE**: fault at t=3 s. Post-cut mix: 5,791/1,190,636 samples differ,
  all within t = 3.0–3.14 s. Trace shows the servo slamming (frame 130:
  agc 0.500, bright +1, vibmul 1.500), overshooting (frame 131), then damped
  recovery — **bit-identical reconvergence by frame 137 (~160 ms)**. The
  cascade is real but self-limiting for this fault: the feedback has exactly
  one frame of memory and the integer-quantized servo is contractive here. A
  sustained/adversarial fault was not tested.
- **RT-LONG** (`tests/plan_long.txt`): cue 440 Hz at t=1 s; RESPOND at t=28 s
  with deliberately wrong nominal 880 Hz. AR renders **440 Hz** (response
  zcr 0.0211 ≈ 2·440/44100) — it measured its own 27 s-old output and
  discarded the wrong plan value. This is the one capability PAR structurally
  lacks.
- **RT-EDGE** (plan truncated at 15 s): zero hard discontinuities (CHOP-1 = 0);
  first-15 s differences vs the full plan are envelope-legitimate (4,410/661,500).

## Known defects found & fixed during build
Same two as PAR (shared voice code): the 1000× amp scaling bug and the
unnormalized harmonic stack. Both fixed.

## Interpretation
AR genuinely reasons over its own generated output: the servo loop is live,
the pitch-inference trap is passed, and the cascade test shows feedback
dynamics (slam → overshoot → recovery) rather than a clamped constant. The
costs are real: long-range recurrence degrades (1.0 → 0.74), cascades are
possible in principle, and the servo's authority is currently broad (every
frame's gain/timbre/vibrato). Unbounded output-feedback is a liability;
bounded feedback — authority limited to designated parameters/regions — is
where its one unique capability (reading its own past output) actually pays.
