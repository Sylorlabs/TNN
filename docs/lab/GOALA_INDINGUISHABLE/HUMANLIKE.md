# GOAL-A: Human-Reference Study — The Positive Model of Human-Likeness

**Track:** GOAL-A "Indistinguishable from human imagination" · **Worker 2**
**Date:** 2026-09-22 (overnight) · **Status:** model delivered, unimplemented
**Judge bar (Micah):** "you'd never guess it was AI — you'd think it came straight from a human's imagination."

Worker 1 hunts AI tells (absence-of-AI). This document is the positive model:
**what makes human-made things FEEL human, so TNN can aim AT human-likeness,
not just away from AI-tells.** Built from 6 LLM probe rounds (5 feature probes
+ 1 consolidated scoring round) with full transcripts in
[`raw/grok-probes/`](raw/grok-probes/).

## The core finding (red-team corrected)

The naive model — "add jitter, grain, asymmetry = human" — **does not survive
red-teaming.** Two fresh critic rounds converged on the same corrections:

1. **Noise is not humanity.** Uncorrelated jitter/grain everywhere reads as
   digital noise or a filter, not a hand. Human imperfection is *constrained,
   contextual variation*: wobble larger on difficult curves than straightaways,
   texture tied to stroke direction and overlap, timing deviations tied to
   phrase tension. The line: noise is uncorrelated; human imperfection is
   correlated with a cause.
2. **"Human-like" ≠ "photorealistic" / "traditional-medium."** Brush drag,
   canvas grain, bow noise are signs of *a physical medium*, not of human
   authorship. A clean digital work can feel unmistakably authored; a noisy
   traditional-looking one can feel empty. In PURE ABSTRACTION (no faces, no
   instruments, no cultural symbols), representational cues die. What survives:
   - **Memory** — motifs return in transformed form; later events remember earlier ones.
   - **Uneven intentional constraint** — a narrow rule/obsession shapes decisions;
     some consequences surprise.
   - **Structured consequence** — events change the future; a rupture removes an
     option; a pause creates pressure. The piece does not loop; it develops.
3. **Imagination vs screensaver.** A screensaver avoids commitment: continuous
   novelty, no hierarchy, no memory, no decisive choices. An authored piece
   establishes a local contract (introduce a pattern, teach it, then develop /
   break / reinterpret it). Red-team: *"A screensaver produces events. An
   authored work produces consequences."* Selective necessity — some detail
   sacrificed, some kept — is the hardest thing to fake and the single
   strongest abstract human-likeness signal.
4. **Backfire law (advertised irregularity).** Once the audience notices the
   work is *trying* to look human, the cues become evidence of artificiality.
   Every feature below has a named backfire mode. The mitigation is always the
   same: **tie the variation to a cause** (phrase position, object weight,
   compositional role), never apply it uniformly.

Net: the implementable positive model is **memory + constraint + consequence
+ cause-correlated micro-variation**. The rankings below are scored against
that, not against photorealism.

## Scoring key

- **D (detectability, /5):** would a human notice its ABSENCE?
- **Det (determinism-compat, /5):** implementable with zero RNG? Mechanism named.
- **B (backfire risk, /5):** could it read as a NEW AI tell?
- All pseudo-variation = deterministic functions of coordinates / indices /
  content hashes. Byte-identical reruns by construction.

---

## IMAGES (240x240 BMP)

| # | Feature | D | Det | B |
|---|---|---|---|---|
| I-1 | Focal hierarchy | 4 | 5 | 1 |
| I-2 | Asymmetric deliberate composition | 4 | 5 | 2 |
| I-3 | Limited purposeful palette | 4 | 5 | 1 |
| I-4 | Motif development (coherent ambiguity) | 4 | 5 | 2 |
| I-5 | Stroke wobble (low-frequency) | 3 | 5 | 2 |
| I-6 | Pentimenti / overpainting | 3 | 5 | 2 |

### I-1 Focal hierarchy — D4 / Det5 / B1
**What:** One region holds the strongest contrast, detail, and color intensity;
attention falls off toward the edges.
**Why detected:** Human-made images guide attention; uniform importance
distribution feels machine-assembled. Large-scale relationship → survives
240x240 extremely well.
**Zag sketch:** pick focal point `(fx,fy)` off-center from a coordinate hash.
Per-pixel contrast/edge-detail weight `w = 1/(1 + k*dist((x,y),(fx,fy))^2)`.
Render marks with density/contrast scaled by `w`; one bright accent color
reserved for the focal zone only. Correlate mark opacity with `w` so the
falloff is causal, not a vignette filter (a pure radial vignette is the
backfire: "procedural saliency map").
**Backfire:** perfectly centered bright spot or uniform edge-blur → obvious
procedural rule. Mitigate: focal point off-center (rule of thirds-ish),
allow one or two strong distractors.

### I-2 Asymmetric deliberate composition — D4 / Det5 / B2
**What:** Unequal visual weight, balanced by intention (not symmetry).
**Why detected:** humans avoid mechanical centering; tension reads as choice.
Strongest large-scale cue at 240x240.
**Zag sketch:** place dominant mass at ~35% from one edge (fixed anchors from
coordinate hash, perturbed ±8px); counterweight shape at opposite edge with
shared color or direction; leave irregular negative space. Connect unequal
regions by a repeated direction or hue so the asymmetry reads as *balanced*,
not careless.
**Backfire:** random off-center placement without connecting relationships
→ looks like a careless layout rule. Mitigate: visual rhyme (I-4) binds it.

### I-3 Limited purposeful palette — D4 / Det5 / B1
**What:** 4–7 base colors + one focal accent; no exhaustive hue coverage.
**Why detected:** artists work inside a chosen emotional/material color world;
every-hue-present reads as generative default. Palette structure survives
even heavy downsampling (note: baseline f3b5-style gray-flat pieces are a
known tell of the *opposite* failure).
**Zag sketch:** fixed palette table in the generator; per-shape palette-role
assignment from shape hash (field / mass / accent / shadow); mixtures only by
deterministic interpolation between chosen colors; one high-chroma accent
color used ONLY inside the focal zone (I-1).
**Backfire:** too-narrow palette → reads as preset filter/quantization.
Mitigate: small controlled temperature shifts + one or two transition mixes
so the palette feels chosen, not constrained.

### I-4 Motif development — D4 / Det5 / B2
**What:** One abstract motif (bent branch, eye-oval, interrupted horizon)
recurs 3× at varied scale, orientation, occlusion — evolved, never stamped.
**Why detected:** coherent transformation signals memory and intention; the
abstract-channel carrier of the red-team's "memory" principle.
**Zag sketch:** seed motif = parametric polyline (e.g. 8 control points from
hash(seed)). Three instances with transform params derived from hash(seed,
instance_idx): scale {1.0, 0.55, 1.7}, rotation {0°, +35°, −20°}, occlusion
mask from low-frequency coordinate field. Preserve ONE recognizable relation
(curvature sign sequence) across all instances.
**Backfire:** identical geometry at regular intervals → stamp/tiling tell.
Mitigate: vary scale, interruption, opacity, orientation; one expected
repetition may be missing or half-hidden.

### I-5 Stroke wobble — D3 / Det5 / B2
**What:** Low-frequency, hand-like deviation along strokes (more at turns and
endpoints, less on straights).
**Why detected:** perfectly uniform curves expose mathematical construction.
**Zag sketch:** define stroke as control points; offset each by
`hash01(stroke_id, pt_idx)` mapped to ±2px, smoothed by averaging neighbors
(3-tap); interpolate. Crucially: amplitude scales with local curvature
(more wobble where the stroke turns) — the *cause correlation* that
distinguishes it from pixel noise.
**Backfire:** independent per-pixel jitter → reads as digital noise, not a
hand. Mitigate: smooth, low-frequency, stroke-contextual only.

### I-6 Pentimenti — D3 / Det5 / B2
**What:** Visible traces of an earlier composition, partially overpainted —
evidence of a changed mind.
**Why detected:** viewers interpret remnants as decision history (the
"coherent history of revision" the red-team named as surviving abstraction).
**Zag sketch:** render composition v0 first; render v1 shapes over it with
opacity; keep fragments of v0 visible near meaningful edges and intersections
via a low-frequency mask derived from coordinate hash (NOT per-pixel noise).
**Backfire:** fragments too frequent/evenly spread → looks like decorative
clutter or a "human artifact" filter. Mitigate: confine to edges of major
forms, keep sparse.

---

## AUDIO (44.1kHz WAV)

| # | Feature | D | Det | B |
|---|---|---|---|---|
| A-1 | Motivic development | 5 | 5 | 1 |
| A-2 | Phrasing arcs + dynamics shaping | 4 | 5 | 1 |
| A-3 | Micro-timing + context articulation | 4 | 5 | 2 |
| A-4 | Timbral evolution within notes | 4 | 5 | 1 |
| A-5 | Rubato (1–4%) | 3 | 5 | 2 |
| A-6 | Sparse expressive imperfections | 3 | 5 | 3 |
| A-7 | Intentional dissonance → resolution | 3 | 5 | 2 |

### A-1 Motivic development — D5 / Det5 / B1
**What:** A seed interval/rhythm motif returns across the piece, transformed
(transposed, inverted, rhythm-compressed, re-registered) — never copy-pasted.
**Why detected:** coherent transformation is the single strongest audio signal
of composition vs generation; it IS the memory principle in the time domain.
**Zag sketch:** seed motif = interval array + rhythm array from content hash.
Transform selector = f(phrase_index): transpose to current chord,
invert contour, compress rhythm, move register, fragment at transitions,
complete form at climax. Structural slots (phrase ends, section starts, final
cadence) get fixed transformation roles — the transformation is chosen by
*structure*, the hash only breaks ties among musically equivalent options.
**Backfire:** too-literal repetition → mechanical. Mitigate: preserve interval
contour or rhythm identity while changing everything else.

### A-2 Phrasing arcs — D4 / Det5 / B1
**What:** 4–8 bar breath-like rise/fall applied jointly to velocity,
brightness, note duration, vibrato depth, accompaniment density; peak at
60–75% of phrase.
**Why detected:** humans organize notes into gestures; constant intensity
has no direction or emotional hierarchy. Ranked #1 audio cue by one probe.
**Zag sketch:** phrase envelope = asymmetric smooth curve over
phrase_beats; apply multiplicatively to velocity, filter cutoff, density.
Vary phrase LENGTH across sections (4/6/8 bars from phrase hash) and let some
phrases build via brightness instead of loudness — avoids the "repeated
4-bar swell" backfire.
**Backfire:** perfectly repeated swell reveals the algorithm. Mitigate: vary
peak position, length, and which parameter carries the build.

### A-3 Micro-timing + articulation — D4 / Det5 / B2
**What:** notes land ±few ms off grid (correlated per phrase, not independent);
note-to-note connections (legato overlap vs staccato gap) chosen from musical
context.
**Why detected:** perfect alignment + uniform gaps = instant "sequenced"
verdict. Articulation choice by context (legato for stepwise motion, shorter
after leaps, accents after rests) often matters more than raw timing jitter.
**Zag sketch:** timing offset = `hash01(note_index)` → ±8ms, then LOW-PASS
across neighboring notes so an entire phrase leans slightly ahead/behind
(correlated, never independent per-note jitter). Keep phrase-peak arrivals
stable. Articulation = f(interval to next note, metrical position, phrase
location, harmony): continuous overlap 0–0.4 of gap, not binary legato/
staccato.
**Backfire:** independent hash offsets → sounds like jittery bad sync; rule
boundaries → decision-tree feel. Mitigate: correlate offsets within phrases;
use continuous articulation values.

### A-4 Timbral evolution — D4 / Det5 / B1
**What:** spectral character changes through attack/sustain/decay — bright
attack, cutoff falling over 100–300ms, higher harmonics decaying faster.
**Why detected:** static synthesized tones are a known tell (exposed melody
notes especially).
**Zag sketch:** per-note ADSR on low-pass cutoff (not just amplitude):
cutoff_start scaled by velocity and register, exponential fall to sustain
value, slight rise near phrase peaks; higher harmonics (additive partials)
get faster decay constants than the fundamental. Time constants vary by note
role (melody vs accompaniment) — not one global envelope.
**Backfire:** identical filter sweep on every note → obvious synth signature.
Mitigate: different time constants per role, scale by velocity/register.

### A-5 Rubato — D3 / Det5 / B2
**What:** local tempo flex ±1–4%, tied to cadences, phrase peaks, transitions;
time recovered after arrivals so bar position stays coherent.
**Zag sketch:** tempo multiplier = smooth spline over phrase position with
knots at marked events (cadence → decelerate; transition → accelerate);
integrate so onset times stay continuous. Bounded: never exceed 4% except at
explicit section transitions.
**Backfire:** unmotivated tempo changes → sounds like a failing clock.
Mitigate: tie every flex to a harmonic/structural event.

### A-6 Sparse expressive imperfections — D3 / Det5 / B3
**What:** ~1 in 32–64 notes carries a motivated deviation: phrase-ending note
5–15ms late, repeated note slightly weaker, leap approached late, held note
with brief pitch instability.
**Why detected:** physical limitation / hesitation reads as a body performing.
**Zag sketch:** event rule: eligible notes = f(phrase position, interval
context); select via phrase hash; never on arbitrary notes; never the same
pattern twice in a row. Rarity pattern itself must not be periodic (vary the
32–64 window by phrase hash) — a *visible rarity pattern* is the highest
backfire score in the audio set.
**Backfire:** B3 — highest in class. Too many / wrong notes → sloppy; periodic
"one mistake per bar" → deliberate simulation. Use last, test blind first.

### A-7 Intentional dissonance → resolution — D3 / Det5 / B2
**What:** prepared clash (passing tone, suspension, chromatic approach) that
resolves within a few beats; resolution louder/longer/brighter.
**Why detected:** tension-and-release communicates expectation and intention —
perceived musical intelligence.
**Zag sketch:** tension slots chosen by harmonic function (dominant function,
phrase tension peak); dissonant pitch = deterministic pick from
{semitone-above-chord-tone, sus4, chromatic approach}; fixed resolution
within ≤2 beats, resolution note emphasized.
**Backfire:** unprepared/unresolved dissonance → "wrong notes." Mitigate:
limit clash duration, make resolution perceptually clear.

---

## VIDEO (240x240, 8fps AVI)

| # | Feature | D | Det | B |
|---|---|---|---|---|
| V-1 | Narrative beat structure | 5 | 5 | 1 |
| V-2 | Easing (varied per object) | 4 | 5 | 1 |
| V-3 | Motivated camera | 4 | 5 | 2 |
| V-4 | Anticipation + overshoot | 4 | 5 | 2 |
| V-5 | Secondary motion | 4 | 5 | 2 |
| V-6 | Holds | 3 | 5 | 1 |

### V-1 Narrative beat structure — D5 / Det5 / B1
**What:** every gesture has establish → initiate → develop → peak → resolve;
the animation is a sequence of *events*, not a continuous parameter sweep.
**Why detected:** the top video cue: unstructured motion reads algorithmic
instantly. This is the motion-domain "consequence" principle.
**Zag sketch:** fixed gesture timeline table: each gesture = frame ranges per
phase (from content hash, varied lengths: some gestures dissolve without a
peak; some interrupt an earlier one). A beat manager advances deterministic
state per frame. Cross-gesture causality: gesture N+1's target references
gesture N's end state (memory across gestures).
**Backfire:** identical enter-bounce-pause-exit template → "preset loop."
Mitigate: vary phase lengths and emphasis; allow interruption and attention
transfer between objects.

### V-2 Easing — D4 / Det5 / B1
**What:** nonlinear velocity (slow in/out) with DIFFERENT curves per object
and action.
**Why detected:** constant-velocity motion is the classic "physics demo" tell.
**Zag sketch:** `p = t*t*(3-2*t)` smoothstep base; per-object easing strength
`k` from hash(object_index): position = lerp(start, end, t^k adjusted);
heavy objects ease harder, floating fields barely. Stronger easing on large
gestures, lighter on small.
**Backfire:** every object sharing one easing curve → recognizable software
signature. Mitigate: per-object/per-action curve variation.

### V-3 Motivated camera — D4 / Det5 / B2
**What:** virtual camera moves only in response to narrative events (reveal,
collision, large color change, directional reversal), with lag and slight
anticipatory lead.
**Why detected:** viewers infer attention from camera; arbitrary pans read as
"effect."
**Zag sketch:** interest point = weighted average of object centers with
attention weights from beat structure (V-1); camera approaches with delayed
easing; shifts triggered ONLY at beat events; small lead in travel direction;
camera holds while subject moves through frame sometimes (imperfect framing
is the human cue — NOT continuous tracking).
**Backfire:** tracking every object → auto-tracking-algorithm look.
Mitigate: camera holds, attention priorities, occasional stillness.

### V-4 Anticipation + overshoot — D4 / Det5 / B2
**What:** small wind-up (0–10% of frames) before a move; pass the target
slightly (85–100%) then settle.
**Why detected:** anticipation communicates intention; overshoot suggests
momentum and a correcting body.
**Zag sketch:** three-phase interpolation per move; overshoot amount =
base × (0.8 + 0.2·hash01(object_index)), proportional to speed and object
"softness"; some moves stop cleanly (no overshoot) — selectivity is the point.
**Backfire:** identical bounce on every move → spring-preset look. Mitigate:
vary by object properties; allow clean stops.

### V-5 Secondary motion — D4 / Det5 / B2
**What:** trailing edges/layers lag the main motion (delayed copy of the main
path, or spring toward it).
**Why detected:** delayed motion implies flexible material/joints — physical
presence in an abstract world.
**Zag sketch:** `secondary(frame) = main_position(frame - delay)` with
per-object fixed delay, or `trail += stiffness·(main - trail)` with fixed
stiffness per layer. Different delays per layer; some parts move immediately.
**Backfire:** constant uniform delay on everything → mechanical lag filter.
Mitigate: per-layer delays; some layers still.

### V-6 Holds — D3 / Det5 / B1
**What:** 2–8 frame pauses at structural points (before a major move, at a
reveal, after impact), with 1px settling or slow color drift so they don't
read as frozen renders.
**Why detected:** pauses create attention and readable poses; motion without
rest feels like a simulation at constant rate.
**Zag sketch:** hold frames inserted at beat-structure markers (V-1);
duration from hash(marker) in {2..8}; during hold, position frozen but a
secondary layer settles 1px and color continues drifting — distinguishes
intentional hold from a dropped-frame error.
**Backfire:** equal-interval holds → metronomic slideshow. Mitigate: vary
duration; place only at expressive points.

---

## TOP 10 IMPLEMENTABLE FEATURES (all media, combined profile)

From the consolidated scoring round (high D, Det=5, low B):

| Rank | Feature | Medium | D | Det | B | One-line why it wins |
|---|---|---|---|---|---|---|
| 1 | Motivic development | audio | 5 | 5 | 1 | Strongest single authorship signal; pure structure, zero texture risk |
| 2 | Narrative beat structure | video | 5 | 5 | 1 | Unstructured motion = instant algorithmic read; beats = intention |
| 3 | Phrasing arcs | audio | 4 | 5 | 1 | Breath-like direction; broadly perceived as musical intent |
| 4 | Timbral evolution | audio | 4 | 5 | 1 | Kills the static-synth tell with almost no backfire |
| 5 | Easing (varied) | video | 4 | 5 | 1 | Linear motion is the physics-demo tell; cheap to implement |
| 6 | Limited purposeful palette | image | 4 | 5 | 1 | Palette discipline survives any resolution |
| 7 | Focal hierarchy | image | 4 | 5 | 1 | Large-scale attention guidance; strongest image cue |
| 8 | Motif development | image | 4 | 5 | 2 | Visual memory across the canvas; watch stamping |
| 9 | Micro-timing + articulation | audio | 4 | 5 | 2 | Kills "sequenced" feel; must be correlated, not independent |
| 10 | Secondary motion | video | 4 | 5 | 2 | Cheap physicality; vary per layer |

Recommended first implementation wave (cheapest, highest yield, lowest risk):
**A-1, V-1, V-2, I-3, I-1, A-4** — all D≥4, B=1, and all are *structural*
(palette tables, envelope tables, timeline tables, filter envelopes), not
texture hacks. They survive 240x240 and 8fps by construction.

## Implementation notes (Zag-level, deterministic)

- **Hash-as-pseudovariation:** every "random-feeling" offset must be
  `f(content)` — e.g. `h = sha256_trunc(note_index || piece_seed)`;
  offset = `(h mod 17) - 8` ms. Piece seed is part of the generator input, so
  byte-identical reruns hold and the variation is *reproducible*, not random.
  The scoring round's key constraint: **hash chooses among musically/structurally
  equivalent options; it must not be the source of the musical logic itself.**
- **Correlation over independence:** low-pass hash offsets within phrases
  (audio), smooth neighbor-averaged wobble (images), per-object fixed delays
  (video). Independent per-sample/per-note/per-frame variation is the #1
  backfire across all media — it reads as noise, and noise ≠ human.
- **Cause binding:** every variation binds to a compositional cause —
  phrase position, curvature, object weight, beat event. If you cannot name the
  cause, delete the feature.
- **Measure before/after:** per GOAL-A prereg — H-symmetry < 0.60 on shipped
  images, no <50-unique-color images unless intentional flat brief, audio
  bipolar/DC≈0/no-clip/44.1kHz/exact tuning preserved, byte-identical reruns.

## FALLBACKS

- **Provider fallback (grok-4.7 → gpt-5.6-sol):**
  "2026-09-22 ~06:50 UTC: grok-4.7 via ExperimentalLabs exhausted credits
  (429 insufficient_credits, balance -$0.02); switched to gpt-5.6-sol via
  UnoRouter per Micah's fallback order."
  All 6 probe rounds (5 feature probes + 1 scoring round) were therefore run
  with gpt-5.6-sol as the reasoning engine, not grok-4.7. Content quality was
  judged adequate (rich, specific, internally consistent; rankings and
  backfire analyses were concrete, not generic). The study brief named
  grok-first for its art/music/film breadth; sol's outputs covered the same
  ground with comparable specificity. Risk: single-model perspective —
  recommend one corroborating round with a different model (grok if credits
  return) before freezing the top-10 into implementation, per test-both law.
- **CLI fallback:** the bundled experientiallabs `chat.py` hard-caps
  `max_tokens: 16`, which truncated the first 5 probe attempts to ~60 chars.
  A patched copy (`raw/grok-probes/chat_long.py`, max_tokens 4000, skill file
  itself untouched) was used for all long calls.
- **Transport fallback:** UnoRouter's `unorouter.py chat` intermittently
  returned `choices[0]=None` (TypeError); a raw-python runner
  (`raw/grok-probes/runner.py`, 5 attempts × 20s backoff) succeeded on first
  attempt for the scoring probe. Direct gateway calls verified healthy at the
  same time, so the failures were wrapper/transient, not provider.

## Open questions

1. **Blind-test the model, not just the features.** The prereg blind bar
   (Micah labels >50% "human-made"/"can't tell", 0% "obviously AI") should be
   run per feature wave — the red-team warns that features interact (uniform
   application of individually-good features = screensaver).
2. **The "sacrifice" probe.** Red-team's hardest test: a piece can score high
   on every surface feature and still read as AI if nothing feels *chosen at a
   cost* (an obsession kept, an attractive development abandoned). Hard to
   implement deterministically — candidate: a fixed "refusal rule" per piece
   (e.g. never resolve to the tonic; one color never touches another) that
   constrains all other choices. Worth a dedicated probe round.
3. **Cross-modal coherence.** Motif memory across image+audio+video of one
   piece (the same seed driving all three) was not probed; likely a strong
   authorship signal for the video+audio pairs.
4. **Worker-1 interface.** The highest-backfire features (A-6 sparse
   imperfections, B3) should go through Worker 1's tell-hunt first: they are
   the most likely to CREATE new tells. Implement order: B=1 features first,
   blind-test, then B=2, then A-6 last with its own preregistered bar.
