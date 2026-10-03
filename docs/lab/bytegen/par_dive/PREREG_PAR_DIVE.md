# PAR_DIVE — frozen prereg (2026-09-24)

Micah: dig super deep into PAR; test everything, forks, red teams; see if
anything overthrows native stateful-sequential generation.

## 0. Settled forensics (do NOT re-litigate; verify independently, then build on)

- **CHOP-3 14 spikes ROOT-CAUSED 2026-09-24:** measurement artifact. The
  audit's `events.txt` held only note *onsets*; the 14 "unexplained" flux
  spikes are vibrato-cycle extrema (5.5 Hz) and 150 ms release onsets, all
  plan-scripted. Re-running `aud_v10/chop.py` on `fork_par/src/par_seq1.wav`
  with the complete event list (onsets + offsets + release tails + predicted
  vibrato extrema, 321 timestamps) → **29 spikes, 0 unexplained**. PAR's
  CHOP-3 record is clean.
- **Standalone-vs-in-context motif:** motif-only plan render vs full-plan
  render (`render_par`, `seq+mix` mode): motif region 2.0–5.3 s is
  **bit-identical, 0/145,530 samples differ**. Zero cross-context
  contamination, as pure f(plan,t) predicts.

## 1. Contenders (each: pure-Zag build, pinned
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, zero RNG,
byte-identical reruns proven by `cmp`)

- **NATIVE (champion):** stateful-sequential as surveyed (plan → carried
  deterministic state → bytes, no output feedback). Reference: v2 hybrid
  piece 1 for audio; `imagination/src/field.zag::f3_synth`,
  `dialogue/dialogue.zag::do_compose`, `imagination/design/render.zag`.
- **A — pure-PAR end to end:** plan formation AND render both parallel
  (every plan event computed independently, no sequential elaboration;
  every sample f(plan,t), zero carried state).
- **B — PAR render, plan-seeded state:** carried state allowed but seeded
  ONLY from the plan at region boundaries (never from prior output).
  Region = plan-defined segment; state wiped + reseeded per region.
- **C — bounded-feedback AR (grok's H3, never built):** region-scoped
  servo with plan-derived targets and boundary state reset, per
  `grok47/ATTACKS.md` Attacks 9/11. Continuous feedback allowed ONLY
  intra-region; no cross-region carry; no plan mutation.
- **D — novel (crew's choice, ≥2 schemes):** e.g. bidirectional two-pass
  render (forward plan pass + backward smoothing, no output→content
  feedback), multi-resolution plan→render, plan-parallel formation +
  sequential render. Crew proposes, preregisters each scheme's claim,
  builds the two most promising.

## 2. Frozen battery (every contender, same fixture
`bytegen/fixture/plan_v1.txt`, 30 s / 44.1 kHz / mono)

- **DET:** two renders, `cmp` clean (mix level — WAV mastering is global,
  per standing house rule).
- **QUALITY:** 9 V10 bars (G-PER, G-STA, G-LURCH, G-DRIFT, G-FLUXm,
  G-SIL1, G-SIL2, G-CLIP, G-CREST) + CHOP-1/2/3 with the COMPLETE event
  list (§0).
- **COHERENCE:** motif recurrence, zero-lag normalized xcorr (motif
  2.0–5.4 s vs 24.0–27.4 s) + max-lag ±50 ms xcorr + pitch/IOI contour
  correlation (Attack 5/8: decompose the number).
- **COST:** wall-clock + peak RSS, same machine.
- **RT-LONG:** cue 440 Hz @ t=1 s, RESPOND @ t=28 s nominal 880 Hz;
  report cents error of the response (honest: octave detector vs pitch
  meter). Near-miss variant: nominal 460 Hz.
- **RT-CASCADE:** single-bit fault in mix @ t=3 s; count differing
  post-cut samples vs clean (mix level).
- **RT-EDGE:** plan truncated @ 15 s; discontinuities at cut + legitimate
  vs illegitimate diffs vs full plan.
- **FAILURE MODES:** documented per contender — where it breaks that
  others don't.

## 3. Forensics extension (PAR characterization)

Beyond §0: polyphony behavior (ZCR-of-sum, voice masking), long-horizon
drift (render ≥5 min plan; does pure f(plan,t) drift in phase/tuning vs
carried-phase native?), fault behavior vs native (fault models beyond
single-bit: burst, dropout, DC shift), per-path notes (audio/video/
dialogue/image — where does PAR's argument hold and where does the path's
nature demand state?).

## 4. Plan-formation parallelism (Micah's framing)

"Left to right but it first plans parallelly" — test explicitly:
instrument where plans come from in each modality (audio plan formation
in `imagination/`, dialogue `do_compose` inputs, image `render.zag`
theme→plan). Questions: are plan events computed independently (any
order, parallelizable) or does formation itself carry sequential state?
Build a plan-formation prototype that forms plans both ways and diff the
plans byte-for-byte. If plan formation is parallel, quantify the
end-to-end win of A.

## 5. Red team (every contender + NATIVE — no sacred cows)

Blind where possible. Must include: sustained 1292-block corruption vs
each contender's recovery story; plan-text adversarial inputs
(rail-pin attempts per Attack 4/7); polyphonic RESPOND cues;
sub-octave nominal lies; vibrato/glide cues vs the ZCR sensor;
cross-region leakage probes for B/C (does region state REALLY reset?);
parallel-order permutation for A (render events in scrambled order —
must be bit-identical).

## 6. Kill / adoption bars

- A contender **overthrows** NATIVE on a path iff: ≥ all 9 quality bars,
  coherence ≥ NATIVE (xcorr + contour decomposition), strictly better on
  ≥1 of {RT-LONG honest-cents, RT-CASCADE, RT-EDGE, COST} with no
  regression elsewhere, byte-identical reruns, and survives §5 red team.
- Verdicts are **per path** (audio/video/dialogue/image): PAR may win
  audio and lose dialogue — report the matrix, not a single crown.
- Partial wins are reported as partial. A TIE keeps NATIVE (incumbent).

## 7. Laws

Pure Zag. Zero RNG in decision/render paths. This prereg frozen before
builds — any change needs a dated amendment. Byte-identical reruns.
Commit to `tnn-native-lab` under `docs/lab/bytegen/par_dive/` (use
`~/workspace/commit_racefree.py`, lab-relative paths, TMPDIR=
`~/workspace/tmp_commit`, never commit binaries or `.zagd`, verify via
GitHub API). No branch surgery. Micah's ears outrank metrics on quality
— render excerpts for every contender into `par_dive/excerpts/` labeled
NEW. Do not stop until the matrix is filled or Micah says stop.
