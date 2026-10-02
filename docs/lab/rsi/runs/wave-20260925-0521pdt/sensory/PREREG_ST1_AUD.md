# PREREG ST-1 - frozen preregistration, committed BEFORE any ST-1 code exists

Wave: wave-20260925-0521pdt. Slot: sensory headspace candidate (audio).
Branch: tnn-native-lab. Working copy: ~/workspace/tnn-rsi.
Run dir: docs/lab/rsi/runs/wave-20260925-0521pdt/sensory/
Frozen: 2026-09-25 05:40 PDT. Status: PREREG ONLY. No ST-1 generator,
verifier, stem file, or render exists. Implementation is explicitly
deferred until after this prereg is committed. The prereg commit must
strictly precede the first implementation commit (commit-order
self-check); a failure is UNVERIFIABLE ORDERING and cannot be adopted
this wave.

## Candidate: ST-1 STEREO FIELD [NEW]

The D-AUD-3 planetvoice score is rendered mono. Every element of the
Kethra world is synthesized, then summed into one channel, yet the
world doc (docs/lab/imagination_discovery/aud/PLANETVOICE.md) places
the mic at a specific point in a specific geography: on a basalt slab
at the edge of the glass-sand dunes, at the foot of the lavender
range, the rift vents behind it, Ilyra climbing above, the ring plane
arcing overhead. Human ears judge realism largely from space: a mono
render of a world that performs around the listener is the biggest
remaining "not real life" tell in the audio line. S11-AUD (queued,
unjudged) added mono propagation (early reflections plus a Schroeder
late field, still one channel). No wave has ever rendered a stereo
field: grep over docs/lab and all run dirs for stereo, binaural, and
two-channel finds zero prior art in the loop.

ST-1 renders each of the ten world elements of score_aud3 to its own
stem buffer (byte-identical element renders, only the accumulation
target changes), then places each stem in a stereo field with
constant-power amplitude panning whose pan positions are frozen from
the Kethra geography. This is not a widener, not a decorrelator, not
a post-hoc stereo-izer on the mono mix: every source keeps its
world-derived position, and the mix is rebuilt from positioned stems.
No new samples, no IR files, no RNG. Deterministic by construction.

This honors the standing line directly:
- Big lever, not a micro-lever: mono to spatial is one of the largest
  perceptual steps in audio realism. It changes every second of the
  21 second piece, not one dab or one band.
- Free lunch: same synthesis cost per element (the stems are the same
  render calls), plus one positioning pass. Frozen cost bar KB8.
- E3 honored: nothing high frequency is added. Panning is pure gain;
  no grain, no static, no hash anywhere in the mechanism.
- Untried audio lever: the image substrate's big levers are exhausted
  or queued (survey below). Audio has had exactly one loop lever
  (S11-AUD, mono space). Stereo is new territory.

## Survey evidence (why this is genuinely new, not a re-litigation)

Image levers on the r8c substrate, with dispositions:
- S11-IMG sun-conditioned dusk sky gradient: QUEUED-UNJUDGED.
- Moon phase/terminator: already substrate (pass 3 shades the moon
  from the same sun vector).
- Giant terminator plus limb darkening: already substrate (pass 3).
- S14 atmospheric limb scattering on the giant: QUEUED-UNJUDGED.
- Whirlpool surface planform on the giant: QUEUED-UNJUDGED.
- Aerial perspective wash by tier: already substrate (pass 3 L7);
  the 1121pdt survey explicitly rejected re-proposing it.
- D13 haze dabs: substrate micro-lever.
- R9 contact occlusion: QUEUED-UNJUDGED.
- S13 warm tone: QUEUED-UNJUDGED.
- E3 film grain: REJECTED by Micah's eyes 2026-09-23.
- G1 sunshafts: lane STANDS DOWN until a genuinely new design idea.
- D15/D17/D18 giant dab patches, D19 focus-plane dabs: micro-levers.
Audio levers: S11-AUD mono propagation, QUEUED-UNJUDGED (a pull
ruling awaits Micah; ST-1 does not stack it, see lineage). b_alpha
V11 is Micah's own frontier: untouched. Nothing stereo exists.

## Baseline (frozen)

- Source: docs/lab/imagination_discovery/aud/synth.zag, score_aud3
  (D-AUD-3 planetvoice v1, the same base S11-AUD used), sha256
  f76293f6061812aaaedeac59ae67440bf949b23c1bf9ebc7e60211df1c58f055.
- Vendored copy: sensory/st1/sub/synth_base.zag, byte-identical to
  the committed file (hash re-verified at build time).
- Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1, sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  verified with sha256sum before use.
- Dry rebuild gate: the vendored copy compiled with the pinned
  toolchain and run as `synth_base aud3 dry_ref.wav` must produce a
  WAV with sha256
  7728fbee2d00ec0d1f791c379dd0430b37aae86fa86e00bba25f90fe42d0612c,
  identical to the committed d_aud3_planetvoice.wav. If the rebuild
  ever fails to reproduce this hash, the wave stops and files a dated
  pre-change addendum; no baseline substitution is permitted.
- Reference render: the dry score renders 926100 samples (21 s at
  44.1 kHz).

## The lever: ST-1 stereo field (frozen mechanism)

Slot: a new positioning stage between the score and the WAV writer,
in sensory/st1/st1_stereo.zag, which is a copy of the vendored
synth_base.zag modified ONLY as follows (diff-verified at evidence
time): each element group of score_aud3 renders into a private stem
buffer instead of the shared mix; the stems are positioned into L/R
accumulators per the frozen pan table; a stereo WAV writer emits the
result. All render calls keep their exact arguments, seeds, and
order; accumulation is integer-linear, so the unpanned stem sum is
bit-exact with the dry mix (asserted by the verifier).

All arithmetic for positioning is f64 gain multiply on the i64 Q24
stem samples, rounded to nearest i64. Zero RNG anywhere. Every
constant below is frozen; the implementation may not tune them
against renders or listening.

Pan law (constant power): for pan p in [-1, 1],
gL = cos((p+1)*PI/4), gR = sin((p+1)*PI/4).
No interaural time delay: ILD only, a disclosed simplification. ITD
is a named follow-up, not smuggled in.

Frozen pan table (azimuth story from PLANETVOICE.md; mic faces the
lavender range at 0 degrees):
- hum (argon standing waves, 3 struck calls): p = 0.00. The air
  itself; omnipresent, centered.
- moon-breath (2 LP beds): p = 0.00. Ilyra overhead.
- ridge wind (resbed 280->950 Hz): p = 0.00. The range spans the
  horizon ahead; stereo collapses it to center, disclosed.
- spire whistle (resbed 1500->2350 Hz): p = +0.15. The tall central
  spire, near center.
- air/shimmer/white bed (HP bed + white bed): p = 0.00. On the mic
  diaphragm.
- gusts (4 geyser events, foothills): p = -0.45, -0.15, +0.15,
  +0.45 in event order. A weather front passes left to right;
  disclosed as a frozen story choice.
- rift vents (3 geysers + 3 bursts, behind the mic): p = -0.10,
  0.00, +0.10. Stereo folds rear to near-center; disclosed as the
  known front/back collapse of two-channel.
- seismic groans (3 struck): p = 0.00. Crust underfoot.
- ice cracks (18 burst+ping pairs, scattered craters):
  p_c = (h01(3961,c)*2-1)*0.8, the frozen golden-walk hash already
  used for crack timing. Spread +/-0.8, deterministic.
- chorus (9 rising tones, ring plane overhead):
  p_e = (h01(3991,e)*2-1)*0.6, the frozen hash used for chorus
  timing. Spread +/-0.6, deterministic.

The binary writes ST-1 decision lines (element, stem index, pan,
gL, gR) to the trace. The verifier asserts every line against this
frozen table.

Stereo WAV writer: 16-bit stereo, 44100 Hz. Peak is taken over both
channels; the same 0.89 headroom norm, the same 1323-sample attack
fade, the same 35280-sample release fade, and the same soft clip
x/(1+0.35*|x|) as the mono writer apply per channel. No new
processing.

## Perceptual metric and cost

- Perceptual metric: human ears (Micah's, as with S11-AUD). The
  machine proxies are KB2 (energy preserved: the piece is the same
  piece, only positioned), KB6 (mono downmix still reads as the dry
  mix), KB7 (crest character unchanged).
- Cost: the synthesis work is unchanged (same render calls); the
  added work is one positioning pass over 42 stems into two
  accumulators. Frozen bar KB8: stereo wall time <= 3x dry wall time
  on this machine.

## Kill bars (frozen before implementation)

- KB1 determinism: 3/3 stereo renders byte-identical (sha256 equal).
  FAIL kills.
- KB2 energy preservation: |10*log10(E_st / E_dry)| <= 0.5 dB,
  E_dry from the gated dry rebuild, E_st = sum(L^2+R^2). FAIL kills.
- KB3 geometry audit: the pure-Zag verifier asserts all 42 stem pan
  positions against the frozen table from the binary's trace. Any
  mismatch FAIL kills.
- KB4 safety: zero samples with |s| >= 32767 in either channel.
  FAIL kills.
- KB5 purity: pinned znc (hash above), zero Python contact with any
  wave artifact (shell and sha256sum only), token grep clean for
  rand/srand/random/time/clock. FAIL kills.
- KB6 mono compatibility: downmix (L+R)/2 vs dry mono: Pearson
  correlation >= 0.95 AND RMS within +/-2 dB. FAIL kills.
- KB7 crest character: |crest_st - crest_dry| <= 1.5 dB (S11-AUD
  precedent bar). FAIL kills.
- KB8 cost: stereo render wall time <= 3x dry render wall time.
  FAIL kills.

Verdict mapping (frozen): ADOPT requires every bar KB1..KB8 PASS as
specified; any bar failed or unevaluable maps to DEAD with killing
evidence. No bar may be weakened, narrowed, or re-interpreted to
force a pass. Audio candidates are not sealed blind pairs; on a
clean pass the deliverable is the stereo WAV plus this evidence for
Micah's ears (S11-AUD precedent: metrics-pass, WAVs to the judge).
No sealed pair is prepared for audio.

## Provenance header (planned, machine-checkable, for the evidence)

RENDER_SHA: <sha256 of the stereo WAV, filled at render time>
FIRST_RENDERED_WAVE: wave-20260925-0521pdt
COMPONENT_LINEAGE: synth.zag-score_aud3(committed,7728fbee); S11-AUD:QUEUED-UNJUDGED (not stacked, independent stem path); R9:QUEUED-UNJUDGED; C1:QUEUED-UNJUDGED; C2v3:QUEUED-UNJUDGED; S11-IMG:QUEUED-UNJUDGED; C12:QUEUED-UNJUDGED; S13:QUEUED-UNJUDGED; S14:QUEUED-UNJUDGED; whirlpool-planform:QUEUED-UNJUDGED
NEW_KNOWLEDGE_CLAIM: World-geometry-conditioned constant-power stereo panning places each D-AUD-3 planetvoice element at its Kethra azimuth, turning the mono render into a spatial field at the same synthesis cost.
Tag: [NEW]. This is not a re-certification. No pending queue item is
re-surfaced or re-presented here; they are listed only as
QUEUED-UNJUDGED lineage so the judge queue stays honest.

## Governance

- Pure Zag, literally: generator, verifier, analysis, and scratch
  are pure Zag compiled with the frozen toolchain. No Python
  anywhere. Any Python touch of a new wave artifact voids that
  wave's evidence on sight; there is no recovery path this wave.
- No em-dashes in loop documentation (standing style rule).
- Commits stay local on tnn-native-lab. Nothing is pushed.
- Red-team: any dropout, artifact, or weirdness in the renders gets
  a knowledge-vs-architecture investigation (data gap in the world
  geometry or substrate flaw), documented before any verdict.
- This worker cannot spawn a child reviewer (depth 2/2, spawning
  disabled); the red-team pass is performed as a structured
  adversarial self-review and the limitation is disclosed in the
  verdict.

## Verdict: PROCEED
