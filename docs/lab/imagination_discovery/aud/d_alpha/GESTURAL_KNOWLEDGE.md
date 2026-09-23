# GESTURAL_KNOWLEDGE.md — FORK D-α (direct waveform dreaming)

What position (d) claims to know about sound, committed BEFORE listening to
its own renders. This is the deliberation's knowledge base: everything the
expansion is allowed to use must be traceable to a line below. The expansion
(dream.zag, Section E) contains no opinions of its own — only arithmetic.

## 1. The position

Sound is what happens when bodies do things. A laugh is not a waveform; it
is a small human losing control of their breath in a particular way. If you
deliberate the *gesture* — the effort, the airway, the timing, the
irregularity — faithfully enough, and your expansion adds no opinions of its
own, the waveform takes care of itself. Synths fail not because they use
math, but because the math has opinions: an oscillator wants to be periodic,
a resonator wants to ring at its frequency, a filter wants to shape. Our
expansion wants nothing.

## 2. What we studied (public-domain recordings, local only, never committed)

Five Wikimedia Commons recordings (all reported Public Domain by the
Wikimedia API), analyzed with `study/analyze_laugh.py` (analysis only —
no audio from these files enters any render):

| file | what it taught |
|---|---|
| `Baby_5_months_old_gabbling_laughing_practising_voice.ogg` | Voiced infant pulses: F0 ~485–1225 Hz, ~5.3% successive-period jitter on clean pulses. Real baby laughter is wildly pitch-unstable. |
| `Bursting_out_laughing.ogg` | Adult burst laughter: pulses 30–158 ms, F0 ~306–959 Hz, centroids 1.7–4.2 kHz. Pulse-to-pulse pitch changes are LARGE; repeated "ha"s are never identical. |
| `Indoor_swimming_pool_children.ogg` | Children in a reverberant space: overlapping voices, no clean solo lines — the benchmark texture is dense overlap, not sequential giggles. |
| `Laughter.ogg` | Ensemble laughter: the laugh "bout" is the unit, not the pulse; bouts vary in length, spacing, and breathlessness. |
| `Weird_cartoonish_laughs.ogg` | Negative example: exaggerated regularity reads as cartoon/synth. |

### Committed gestural facts (used in the scores)

1. **A laugh pulse is 30–160 ms** of voiced sound with a fast attack and a
   ragged decay. Not an ADSR — the decay has deliberate asymmetry (mid-pulse
   dips where the breath catches).
2. **F0 moves within and between pulses.** Child F0 300–600 Hz for giggles,
   up to ~900+ in shrieks. No two successive pulses share a contour unless
   the breath forces it — and then something else differs.
3. **Period jitter is ~5%** on clean voiced pulses. Below ~2% it starts to
   sound sung; above ~10% it sounds distressed. (The monster uses 12–14%
   deliberately — it is not a child.)
4. **Spectral emphasis MOVES within the pulse.** The vocal tract never sits
   still: measured pulse centroids in real laughter span 1.7–4.2 kHz with
   large pulse-to-pulse SD. A static formant is the synth smell.
5. **Breath is part of the voice.** Laughs are 2–10% breath noise; the
   breathiness is modulated by the same envelope as the voice (it catches
   when the voice catches).
6. **Feet are impacts, not drums.** A running child's footstep is a short
   (~25 ms) irregular thud with a noisy attack and a fast, uneven decay —
   drawn, not synthesized. No two steps share rate, gain, or timing.
7. **Real ambience breathes.** Room tone/air is never flat: it swells and
   recedes on 5–15 s scales. A stationary bed is a synth; a slowly-varying
   wash is air.

## 3. The three child voices (deliberated characters, not presets)

| voice | age | character | F0 range | jitter | breath | signature |
|---|---|---|---|---|---|---|
| Mara | 6 | bright, tumbling laugh | 330–580 Hz | 5% | 6% | 12-pulse tumble after the trip; pitch falls as breath runs out |
| Joss | 4 | high, staccato, shrieky | 420–900+ Hz | 6% | 8% | short 40–90 ms bursts; occasional 25–50% shriek lift mid-bout |
| Tari | 7 | deeper guffaw | 300–420 Hz | 4% | 10% | longer 100–260 ms pulses; the "laugh-leader" |

Nobody is the "lead": at any moment 1–3 voices overlap (the pool recording
taught us the texture is overlap). The score has 8 laugh bouts across 30 s,
deliberately varied in length (4–12 pulses), spacing, pitch contour, and
breathlessness.

## 4. Feet, breath, air (the non-voice gestures)

- **Footsteps**: two drawn tables (1024 samples each, zero-meaned), played at
  deliberated rates (0.92–1.08×) and gains. Runs at 15.2–19.4 s ("chase"),
  23.5–26 s (receding). The two tables are drawn by the same deterministic
  procedure — documented limitation, see §7.
- **The trip** (19.62 s): a drawn 2048-sample landing thud at 0.8× rate,
  gain 0.7 — bigger, lower, messier than a footstep.
- **Breaths**: inhales/gasps as the deliberated air grain under a 4-key
  envelope. The trip gasp (19.45 s) precedes the thud — the body reacts
  before it lands.
- **Distant air**: three 10–11 s grain gestures, gains 0.014–0.020, slowly
  swelling envelopes starting at 0.55 (air is always there). Non-stationary
  by design — NOT a bed.
- **Swing creaks**: low (90–140 Hz) voiced gestures with sagging F0 and
  deliberately irregular period — the playground furniture.

## 5. Beyond experience: Kethra, the ocean, the monster

The monster objection says: humans imagined things they'd never heard.
Position (d) answers: you don't need to have heard it if you understand the
*gestures* it's made of. Committed translations:

- **Kethra planet voice** (anti-v2): a planet's voice is slow geology, not a
  synth pad. Tidal crust breathing (10–20 s swells, f0 30–45 Hz), rift-vent
  exhalations (breath grain, long), cryo-cracks (drawn impacts at 2–3× rate
  — the same impact tables as footsteps, pitched up by playback rate, which
  is honest: a crack IS a tiny impact), magnetospheric chorus (high,
  wandering voiced gestures 600–1200 Hz). Nothing periodic; nothing that
  rings.
- **Alien ocean at dawn**: breakers are DRAWN (3 s tables: slow rise, ragged
  crest with sub-crests, heavy fall — deliberated, frozen), played at
  0.9–1.1× every 7–11 s. The "sky hums": a low voiced drone (55–82 Hz) that
  never sits still (F0 wanders ±8%). Distant roar: low voiced gestures
  (28–41 Hz). Glass singing far away: inharmonic partials (1, 1.71, 2.63…)
  — the alien color. Spindrift: breath grain, gusting.
- **The monster** (committed description in MONSTER.md): a cavernous throat,
  f0 51–68 Hz sagging, INHARMONIC partials (a throat that big is not a pipe:
  1, 1.62, 2.71, 3.83…), 12% jitter, ragged sub-crested roar envelopes,
  subsonic swells (33–38 Hz) underneath, cavernous exhales between roars.
  Dreamed from gestural knowledge of largeness, roughness, and breath —
  never heard, only understood.

## 6. The synth-smell table (what we check our renders against)

| smell | what it is | our guard |
|---|---|---|
| periodicity | exact repetition | max pairwise pulse xcorr < 0.90; no two pulses alike |
| stationarity | unchanging texture | centroid SD > 250 Hz across pulses; air swells, never flat |
| symmetry | clean ADSR, exact envelopes | ragged decays, mid-pulse dips, irregular keyframes |
| ringing | fixed resonances | harmonic emphasis MOVES within every pulse (3 keyframes) |
| hiss bed | constant white noise | exposed-hiss gate = 0.000; breath uses falling-spectrum grain |
| clicks | digital edges | all envelopes start/end at 0; max jump < real field recording |
| DC offset | asymmetric math | zero-meaned tables; per-partial phase (see audit); \|DC\| < 0.005 |

## 7. Known limitations (committed honestly)

1. The two footstep tables are drawn by the same deterministic procedure —
   they differ only by hash seed, not by a deliberated left/right character.
   Rate/gain/timing vary per step, but the source tables are cousins.
2. The laugh is built from pulses the deliberation fully specifies — but the
   *phonetic* content (vowel color "ha" vs "hee") is carried only by the
   harmonic weights, not by a vocal-tract model. A linguist would hear the
   simplification.
3. The monster was never heard by anyone; its gestural knowledge is analogy
   (large + rough + breathy). If it sounds like a synth, the position
   concedes Test 3's monster leg honestly (see MONSTER.md).
4. The expansion sums Fourier partials per gesture — the audit (EXPANSION_AUDIT.md)
   addresses head-on whether this is "additive synthesis in a wig."
