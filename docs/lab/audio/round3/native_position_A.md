# NATIVE POSITION A — No-Synth Audio, Round 3 (2026-09-24)

**Side:** native (pro no-synth). **Author:** native subagent, TNN program.
**Law under debate:** Micah's law — NO SYNTHESIZERS, PERIOD; audio ONLY via
native wave manipulation and editing of real waveforms.

## 0. Thesis

The no-synth law is not a handicap to be worked around. It is the only
constraint in program history with a non-zero hit rate: Round 1 (10 synth
forks) went 0/10 on human ears; the single approach that ever produced
organic-sounding material was resynthesis of real recordings (vowel_fossils'
PSOLA time-warp of real child vowels). The native position is therefore:
**double down on provenance, and move the entire novelty budget from
waveform generation (forbidden, and historically worthless) into
deliberate compositional choice — selection, arrangement, and
transformation-as-composition — made by TNN itself, verified by analyzer,
iterated against preregistered kill bars.** Three forks below span the
space: pitch-shifting resynthesis (PSOLA), concatenative assembly
(deterministic Viterbi), and pure arrangement (zero resampling). Each is
implementable in pure Zag, deterministic, byte-identical across reruns,
and auditable sample-by-sample back to recorded sources.

---

## 1. The line: "synthesis" vs "manipulation", precisely enough to gate reviews

### 1.1 Definitions

**MANIPULATION** — a process M mapping recorded source buffers to an output
buffer is *manipulation* iff all three hold:

- **(M1) The silence test.** M applied to all-zero sources yields an
  all-zero output, bit-exactly. No exceptions, no epsilon.
- **(M2) Provenance closure.** Every output sample is a documented
  deterministic function of recorded samples, using ONLY these operations:
  copy / reorder / interleave (cut, splice, reverse, interleave); scalar
  gain; summation (layering); convex combination (crossfade); and
  bandlimited resampling (interpolation) under a monotone time-map, with
  pitch-synchronous windowing (Hann) for grain extraction. No other
  operations.
- **(M3) Information origin.** No output sample's value depends on
  evaluating a designed waveform, noise, or excitation equation at output
  coordinates — i.e., no function whose values are defined independently
  of the recorded samples (oscillators, polynomial flow models, PRNG/hash
  evaluated at output index, designed excitation bursts).

**SYNTHESIS** — any process that fails M1 (equivalently: it emits non-silence
when its sources are silence), or that places perceptually load-bearing
information — periodic excitation, spectral envelope identity (vowel
quality), transient identity — into the output via designed equations
rather than recorded samples.

The silence test (M1) is the reviewer's mechanical gate: it is
implementable as an automated unit test (zero the sources, render, assert
all-zero). M2 is the code-audit gate (whitelist of operations). M3 is the
judgment gate for the hard cases below.

### 1.2 Three PASS examples

1. **PSOLA pitch-shift of a real vowel fossil** (788 Hz → 660 Hz):
   pitch-synchronous Hann grains, windowed-sinc resampling per grain,
   overlap-add on the target period grid. M1: silent fossil → silent
   output. M2: every output sample is an interpolation of recorded grain
   samples under a monotone time-map. The sinc kernel is a *reconstruction
   filter* — the digital equivalent of a DAC's reconstruction stage: it
   recovers values of the already-recorded continuous waveform between
   sample instants (subject to the bandlimit the ADC already imposed). It
   adds no information; it cannot invent a formant.
2. **Concatenative assembly of real syllables** with 8 ms equal-power
   crossfades at energy minima. Output = recorded samples, plus convex
   combinations of two recorded segments at joins. Silent inventory →
   silent clip. Every sample traces to a source offset logged in the unit
   manifest.
3. **Reversal + layering of a real breath onset under a real vowel unit**,
   fixed scalar gains. Reverse is index inversion; layering is summation;
   gain is scalar multiply. All in the M2 whitelist; M1 trivially holds.

### 1.3 Three FAIL examples

1. **LF-model glottal pulse + 6 designed formant filters** (Round-2 fork 1,
   `glottal_formant`). Zero the sources: the LF polynomial still emits
   pulses, the filters still ring. The vowel quality — the entire
   perceptual identity — originates in the filter coefficients, which were
   *designed*, not recorded. Fails M1 and M3.
2. **"Deterministic breath" = lowpassed hash/PRNG evaluated at output
   coordinates** (Round-2 fork 2's HNR filler). Deterministic ≠ recorded.
   Zero the sources: it still emits noise, because the hash is a function
   of the output index, not of any recording. Fails M1 and M3. This is the
   honest correction to fork 2: its breath filler was synthesis, and under
   the law it must be replaced by *real* breath segments. (Fork 1 of this
   round does exactly that.)
3. **Noise-burst transient "synthesizer"** (burst envelope × PRNG, cf.
   Round-2 fork 5's KS-decay elements). Zero the sources: the burst still
   fires. The transient's identity comes from the envelope equation. Fails
   M1/M3. Transients must be *cut* from real recordings (park claps, stop
   bursts), never *fired* from equations.

### 1.4 Hard cases, ruled

- **Time-stretch (WSOLA/phase-vocoder-free duplication):** MANIPULATION.
  It is reordering/duplication of real samples under a time-map. Silent
  in → silent out. The "new" duration contains no new information; it is
  the same information, re-timed.
- **Granular resampling / windowed-sinc interpolation:** MANIPULATION
  (see PASS 1). The kernel reconstructs; it does not compose. Reviewer
  check: the kernel must be a fixed reconstruction kernel (sinc/Kaiser),
  not a designed timbral filter, and its output must vanish on zero input.
- **Crossfade:** MANIPULATION — convex combination of recorded samples.
- **Filtering/EQ:** MIXED, decided by M3. Convolution with a *measured*
  impulse response (a recorded room, a measured microphone) is
  manipulation — the kernel is itself recorded. Filtering that *creates*
  sonic identity — formant filters turning a saw into /a/, a designed
  "vocal tract" — is synthesis: the phonetic information originates in the
  design. Reviewer test: **does the filter's design determine the output's
  phonetic/sonic identity?** If yes → synth. If it only corrects or
  places already-recorded identity (measured room, fixed gentle
  high-shelf from a measured chain) → manipulation. When in doubt, the
  fork must prove the identity survives with the filter bypassed.
- **Pitch detection, autocorrelation, formant tracking:** not audio
  generation at all. Measurement is always allowed; the analyzer is not
  the synthesizer.
- **Scalar gain:** MANIPULATION — but with the standing law **no
  output-derived normalization**: gains are fixed a priori or derived from
  *source* measurements, never from the rendered output's peak/RMS.
  A peak over −1 dBFS is a *failed render* (gate), not a signal to
  renormalize; the agent replans with lower fixed gains.
- **Vibrato via time-varying resample ratio:** MANIPULATION — the ratio
  is a time-map applied to recorded grains, not an oscillator mixed into
  the output. The LFO never appears as samples; it only steers the map.

---

## 2. Why the Round-2 synth forks failed the law despite passing gates

Three of six Round-2 forks passed the analyzer gates. They still fail the
law, and the reason is structural, not a matter of degree:

1. **The gates measure acoustic correlates; the law constrains
   provenance.** HNR, prosody, periodicity, rolloff — these are necessary
   conditions for plausibility, not certificates of origin. A well-fitted
   LF model plus designed formants produces correct F0, correct HNR, and
   correct formant peaks *because the equations were fitted to those
   targets*. The meters cannot distinguish harmonic energy from a real
   glottis from harmonic energy from a polynomial. The law asks a question
   the analyzer cannot ask: *where did this information come from?*
2. **Passing gates never earned synthesis a pass.** The Round-2 crews
   operated under the old rules (research-informed synthesis was legal
   then); their work was valid under those rules and is now *retired*, not
   retroactively "wrong." But the information-origin test is orthogonal to
   every meter: fork 1's voice never existed as a recording. Every sample
   traces to equations. That is the definition of what the law forbids.
3. **Round 1 is the empirical base rate.** Ten synth forks, 0/10 on human
   ears ("shitty synth", "earrape", "video-game character", "gunshots with
   static", "alien"). Meters that pass while ears fail mean the meters
   were measuring the wrong thing — exactly Micah's standing
   analyzer-first correction. The law is the program-level response to
   that base rate: stop optimizing equations against meters; start from
   the only material that ever cleared the ear.
4. **Fork 2 (`grain_unit`) is the counter-proof, honestly qualified.**
   It passed all 7 shared gates (HNR 5.43, prosody 1.99%, periodicity
   0.71, frac_static 0.61, crest 8.7 dB, peak −3.2 dBFS, HF −18.2) using a
   *real* vowel fossil — real-source resynthesis clears the gates. It was
   killed on a kill-bar technicality (a backwards hypothesis about grain
   size vs formant smear: larger PSOLA grains give *better* frequency
   resolution, not worse — the bar, not the engine, was wrong). And under
   the new law it needs one repair: its "deterministic breath (LP'd hash)"
   filler fails the silence test (§1.3, FAIL 2) and must be replaced by
   real breath. Round-3 Fork 1 is that repair, upgraded to agentic
   operation.

---

## 3. The crux: where does novelty come from if every sample traces to a recording?

Head-on, because this is where the other side will attack:

**Novelty was never in the samples.** A violinist's novelty is not in
inventing new atoms of rosin and horsehair; it is in which notes, in which
order, with what timing, against what silence. Chemistry does not
synthesize new elements; it makes new molecules from the existing ones —
and nobody calls chemistry uncreative for it. The compelling thing a
listener hears was *always* a compositional fact: selection (which moment
of the voice), arrangement (order, rhythm, juxtaposition), and
transformation-as-composition (time-stretch as a microscope on a vowel's
interior; PSOLA pitch moves putting a child's /i/ on a melody she never
sang; reversal revealing the breath inside a syllable).

Concretely, what is *new* in each fork below:
- Fork 1: a melody the child never sang, in a voice that is recognizably a
  real child's — the pitch contour, the phrasing, the breath placement are
  composed; the atoms are recorded.
- Fork 2: a phrase never spoken, assembled from ~200 real diphones — the
  *utterance* is new; the phonemes are fossils.
- Fork 3: a rhythmic piece from found sound — the *arrangement* is new;
  every transient happened in a real park, every chop left a real mouth.

Second: **the constraint has the only non-zero hit rate in program
history.** Every equation-first attempt at "novel" waveforms produced
novelty of the wrong kind — novel *ugliness* (0/10). The ear is
exquisitely tuned to exactly what recordings carry for free and equations
cannot fake: breath noise with the right statistics, F0 wobble with the
right correlation structure, a room. Constraining the atoms to reality
does not shrink the design space that matters; it deletes the region of
the space where all historical failures live.

Third: **the novelty budget moves to where TNN's deliberation actually
lives.** Under synthesis, the "intelligence" sits in parameter choices
for equations — a space where TNN has no advantage over a grad student
with a DSP textbook. Under the law, the intelligence sits in *listening
to an inventory, planning edits against targets, verifying by analyzer,
and iterating* — deliberate choice over real material, which is precisely
the program's main line (deliberate memory agency, deliberate
consolidation). That is why the native position favors **agentic editing**
over fixed pipelines (§4).

Fourth, the falsifiable concession: **if the real-source line cannot beat
the retired synth line on Micah's ears within a bounded number of rounds,
the law itself becomes the variable to revisit.** But not before the
native position gets a fair, well-resourced run — three forks, real
inventories, agentic operation, preregistered kill bars — because the
only organic result in six days of audio work came from this line, and it
would be irrational to abandon the single working approach before
testing it properly.

---

## 4. The native method: agentic editing

Fixed pipelines are allowed under the law, but the native position argues
for **agentic editing** as the primary mode, for three reasons:

1. **The law leaves choice unlimited.** It bans generators; it does not
   cap decisions. Unit selection, edit sequencing, gain staging, replan
   logic — all are pure deliberation, zero RNG, fully logged. A fixed
   pipeline spends none of this budget; an agent spends all of it.
2. **Real material is irregular; plans must adapt.** A fixed pipeline
   breaks on the first bad join or thin inventory region. An agent
   *listens first* (measures F0, formants, HNR, crest per unit), plans
   against gate targets, renders, measures, and replans — with every
   decision logged as a deliberate action with a reason (unit id, cost
   terms, why this unit and not the runner-up).
3. **Agency is testable.** Fork 3's kill experiment (§7.5) directly tests
   whether agentic arrangement beats a fixed chronological rule. If it
   doesn't, the native position drops the agency claim for that fork and
   keeps the pipeline. Claims earn their keep or die.

**The agentic loop (shared by all three forks):**
1. *Inventory listen* — load sources (SHA-verified), run
   `audio_round2/shared/analyze.py` frame metrics, catalog units with
   measured features. Write `inventory_manifest.md` (unit id → source
   file, byte offset, source SHA-256).
2. *Plan* — agent writes `edit_plan.md`: the target (notes / syllables /
   grid), the selection rule, fixed gains, and the predicted gate values
   with reasons.
3. *Render* — pure-Zag renderer executes the plan. Operations restricted
   to the §1.2 whitelist; the renderer also emits a *provenance sidecar*
   (for a sampled subset of output indices: source id + source range +
   transform applied).
4. *Verify* — analyzer gates + fork kill bars + silence test + provenance
   spot-check. 3× byte-identical reruns (SHA-256 match).
5. *Iterate* — at most 2 logged replans, each naming the failed bar and
   the exact plan delta. A third failure kills the fork; no silent
   parameter drift.

All decisions deterministic: ties broken by lowest unit id, no RNG
anywhere, no output-derived normalization (gains fixed in the plan;
over-peak renders fail the gate and trigger replan, never
renormalization).

---

## 5. FORK 1 — `fossil_choir`: agentic PSOLA resynthesis of a real child's voice singing a new melody

**One-line concept:** A real child sings a melody she never sang — pitch-
synchronous grains of real child vowels, pitch-shifted by resampling,
selected and arranged by an agentic edit plan.

### 5.1 Real source material

| Role | File | SHA-256 (full) | Measured properties |
|---|---|---|---|
| Primary vowel unit | `aud_v11/diag/vowel_real.wav` | `8ba3b42708a8bab2bb8152d392d4425c5c248591d545f3bd1b24070e264e5d1d` | 2.0 s, 44.1 kHz mono 16-bit; field anchor child vowel; F0 ≈ 400.9 Hz, autocorr peak 0.985 |
| High vowel unit | `audio_round2/grain_unit/fossil_hi.bin` | `9439c067ee9a01841f702fec49571475336eb47318bbd999948617d8746a4622` | 4816 int16 (122.42–122.57 s of Aporee source below); F0 ~788 Hz, F1 ~2371, F2 ~4725; /i/-like |
| Mid vowel pool | `v5work/kidb.wav`, `kidc.wav` | `13285a0d…`, `5a1b1f7b…` (full in §9) | 30 s each; RMS ≈ −20 dBFS, peak −3.3 dBFS; ~600 voiced frames each, median voiced F0 558–565 Hz |
| Breath bed | segments of `v5work/kida.wav` | `b8ad8e1a…` | 30 s, quiet (RMS −48.4 dBFS): agent hunts 200 ms low-energy / high-zero-crossing breath segments |
| Room bed | `tnn-lab/…/calibration/garry_point_park_30s.wav` | (manifest §9) | real park ambience, fixed −30 dB |

The Aporee field source (`aporee_kids_play_area.wav`,
`24981f77ff52acb701f3e6957ece9c5b5ab8d53857887d7bc69bc0d717c79b77`)
is the fossil's provenance root; the fossil's logged offsets (122.42–
122.57 s) are re-verified by the agent against the source SHA before use.

### 5.2 Exact manipulation chain

1. **Inventory listen.** Agent loads sources, runs the shared analyzer per
   25 ms frame, catalogs voiced-stable segments: autocorr peak ≥ 0.6,
   F0 ∈ [200, 950] Hz, F1/F2 frame-to-frame movement < 120 Hz over ≥ 12
   frames. Breath candidates: RMS < −40 dBFS, zero-crossing rate >
   0.25. Writes `inventory_manifest.md`.
2. **Target plan** (`edit_plan.md`): 8 notes — C5 D5 E5 G5 A5 G5 E5 D5
   (523.25, 587.33, 659.25, 783.99, 880.00, 783.99, 659.25, 587.33 Hz),
   0.55 s/note, 80 ms breath gaps. Per-note F0 contour: 30 ms attack
   ramp, then ±0.8% 5.5 Hz vibrato on notes 3–5 only (vibrato realized as
   a *time-varying resample ratio* — a time-map, §1.4 — the LFO never
   becomes samples). All phases deterministic.
3. **Unit selection (agentic, logged).** Per note, cost =
   2·|log2(F0_unit/F0_target)| + vowel_mismatch(0/1 from F1/F2 class) +
   |HNR_unit − 3.7|/3.7. Deterministic tie-break: lowest unit id. The
   plan logs chosen unit, runner-up, and cost terms — a deliberate choice
   with a reason, auditable.
4. **Pitch marking.** Autocorrelation peak-picking on the lowpassed unit
   (measurement, allowed). Marks at glottal-pulse spacing.
5. **PSOLA resynthesis.** Extract 2-period Hann-windowed grains at marks;
   resample each grain by r = F0_unit/F0_target_inst via windowed-sinc
   (Kaiser β=6, 16 taps — reconstruction kernel, §1.4); overlap-add on
   the target period grid at 50% overlap. **Ratio bound: r ∈ [0.75,
   1.33].** If the best unit violates the bound, the agent must replan
   (pick next-best unit); exceeding the bound is a plan failure, not a
   parameter to stretch.
6. **Breath gaps.** The 80 ms gaps are filled by *real breath segments*
   from kida (cut to length by agent choice among candidates), joined to
   note tails with 10 ms equal-power crossfades. No generated noise
   anywhere — this is the §2 repair of fork 2's hash-breath.
7. **Master.** Fixed gains in the plan: vowel layer 0.5, breath 0.25
   (−12 dB rel), room bed 0.06 (−30 dB). **No output-derived
   normalization** (standing law): if rendered peak ≥ −1 dBFS the render
   FAILS the transient gate and the agent replans with lower fixed gains.
8. **Verify + iterate.** Analyzer gates (§8), fork kill bars (§5.5),
   silence test, provenance spot-check, 3× byte-identical reruns. Max 2
   logged replans.

### 5.3 Law-compliance argument

- The only pitch-changing operation is PSOLA resampling = interpolation
  under a monotone time-map: PASS example 1 of §1.2. Silent vowel unit →
  silent note. The formants are never touched by design — they ride along
  inside the recorded grains (kill bar 3 verifies this empirically).
- Vibrato is a time-varying resample ratio, not a mixed oscillator
  (§1.4): the LFO value never appears in the output buffer; it only
  steers which recorded sample the interpolator reads.
- Breath and room are recorded segments, selected and placed — the
  replacement for fork 2's illegal hash-breath.
- The "hard case" the other side will press: *isn't choosing r per note
  "parametric"?* Parameters steer *which recorded samples are read and
  when* — they never generate values. A parameter that indexes into
  reality is manipulation; a parameter that evaluates sin() is synthesis.
  The silence test decides it mechanically.

### 5.4 Why agentic (not a fixed pipeline)

The unit inventory is irregular: F0s cluster at 401/558/788 Hz, vowel
coverage is whatever the field recordings happened to contain. A fixed
pipeline with a fixed unit per note either violates the ratio bound or
accepts bad matches silently. The agent's job is exactly the native
claim: listen to what's there, pick the least-bad match by a stated cost,
replan when bounds fail, and log every choice. The plan is the
deliverable as much as the audio.

### 5.5 Preregistered kill bars

1. **All 7 shared gates pass** on the final render: frac_static ≥ 0.25;
   HNR ∈ [0.7, 6.7] dB; periodicity (autocorr peak at target F0) ≥ 0.5;
   HF rolloff ∈ [−40, −12] dB rel peak; prosody (voiced F0 std/median) ∈
   [0.3%, 3%]; transient crest ∈ [3, 20] dB with peak < −1 dBFS; hum
   check clean. (Gate definitions: `audio_round2/shared/analyze.py`.)
2. **3× byte-identical reruns** — SHA-256 of the WAV master identical
   across three runs on the pinned toolchain.
3. **Formant preservation:** per held note, |F1_render − F1_unit| ≤ 8%
   and |F2_render − F2_unit| ≤ 8% (median across notes, analyzer formant
   tracker). PSOLA must move pitch, not vowel identity. Failure means the
   resampling is dragging the spectrum — a synthesis-like artifact.
4. **Silence-source test:** all sources replaced by zeros → output
   bit-exact zeros. Automated; failure = law violation, fork dead on the
   spot.
5. **Provenance audit:** 1000 random output indices spot-checked against
   the provenance sidecar — each must map to a recorded range inside a
   SHA-verified source. Any unmapped sample kills the fork.

**KILL EXPERIMENT (kills the approach itself):** substitute a *synthetic*
unit inventory (sawtooth + designed formant filters at the same F0s, same
chain otherwise) and rerun. The fork's claim is that its quality comes
from *realness*. Kill condition: if the synth-inventory render passes
kill bars 1–3 as well as (or better than) the real-inventory render —
i.e., realness buys nothing measurable — the "real-source resynthesis"
approach claim is vacuous and the fork dies. Conversely the fork must show
the real inventory beating the synth inventory on ≥2 of the 7 gates
(predicted: HNR and frac_static, where recorded breath/wobble statistics
cannot be faked by the saw).

### 5.6 Honest failure mode

Most likely: **chipmunk choir** — audible "sped-up/slowed-down" quality
where the ratio bound was respected but the ear still hears time-scaling
rather than singing, or vowel identity wobbles between notes because the
inventory's vowel coverage is thin. What it tells us: PSOLA alone cannot
carry melody without a denser multi-F0, multi-vowel inventory — the
selection cost's F0 term dominates, and the fix is *more recording* (wider
inventory), not a better equation. That is a knowledge problem
("improper knowledge" — Micah's default attribution), not a machinery
ceiling, and it is solvable inside the law.

---

## 6. FORK 2 — `concat_native`: deterministic concatenative unit selection — a real child "says" a new phrase

**One-line concept:** A novel utterance assembled from ~200 real diphone
units via deterministic Viterbi selection — **zero pitch shifting, zero
resampling**: formants are untouched by construction.

### 6.1 Real source material

- Unit inventory: `v5work/kidb.wav`, `kidc.wav`, `kidd.wav`
  (SHAs `13285a0d…`, `5a1b1f7b…`, `ab22c5e4…`, full in §9) — 30 s each,
  ~600 voiced frames each, median voiced F0 558–565 Hz. Agent cuts
  CV/diphone segments at energy minima flanking voiced cores (min
  120 ms), pitch-marks by autocorrelation; target N ≥ 200 units.
- Transient units: real stop-burst onsets (/b d g/ attacks) cut from the
  same files — onset crest ≥ 10 dB, 30–80 ms.
- No beds, no breath filler: this fork tests whether selection + joins
  alone carry an utterance.

### 6.2 Exact manipulation chain

1. **Inventory listen.** Segment, measure per unit: F0 median, F0 slope,
   F1/F2, RMS, HNR, duration. Write `inventory_manifest.md` (unit id →
   file, offset, source SHA).
2. **Target plan** (`edit_plan.md`): a fixed 6-syllable sequence with
   per-syllable constraints — e.g. /la ba du gi ma la/ with a target F0
   arc 560→620→560 Hz and per-syllable duration targets. The target is a
   *sequence of constraints*, not audio: (vowel class, F0 target,
   duration target) per syllable.
3. **Deterministic Viterbi.** States = top-20 candidate units per
   syllable by target cost; target cost = w1·|log2(F0u/F0t)| +
   w2·|dur_u − dur_t|/dur_t + w3·vowel_dist (F1/F2 Euclidean, z-scored
   from *inventory* statistics — source-derived, legal); join cost =
   boundary RMS discontinuity + 20 ms edge spectral distance;
   deterministic tie-break by lowest unit id; backtrace yields the unit
   sequence. Weights (w1..w3) from a preregistered set of 3, tried in
   fixed order.
4. **No time-stretch, by design.** Units play at natural duration;
   duration mismatch is absorbed by *selection among candidates*. If no
   candidate lies within ±25% of the duration target, the agent drops to
   the next-best vowel class and logs the substitution. Resample call
   count for the whole fork: **0** (asserted in code).
5. **Joins.** 8 ms equal-power crossfades placed at energy minima (convex
   combination of two recorded segments — §1.2 PASS 2). Onset transients
   prepended for stops with 5 ms crossfades.
6. **Master.** Fixed a priori gains: vowel layer 0.5, transient layer
   0.35. No output-derived normalization; peak ≥ −1 dBFS fails the
   render → replan with lower fixed gains.
7. **Verify + iterate.** Gates, kill bars, silence test, provenance
   audit, 3× byte-identical. Max 2 logged replans (weight-set rotation
   only).

### 6.3 Law-compliance argument

This is the *strictest* fork on paper: no resampling, no interpolation,
no time-maps at all — only copy, crossfade (convex combination), and
scalar gain. The silence test is trivially satisfied; provenance is
exact (output samples *are* source samples except in ≤8 ms join regions,
which are convex combinations). The hard case it answers: *is Viterbi
selection "generating" the utterance?* No — selection chooses among
recorded realities; it creates an *order*, not samples. Ordering is
composition, and composition was never the banned thing (cf. §3).

### 6.4 Why agentic

The inventory is whatever the children happened to say; the target
phrase was never spoken. Some syllable slots will have 30 candidates,
some will have 3, and the agent must trade vowel match against F0 match
against join smoothness — a genuine multi-objective deliberation with
logged reasons. A fixed pipeline (e.g. "always take lowest target cost")
cannot explain or revise its tradeoffs; the agent can, and its replan
rule (rotate the preregistered weight set, log which bar failed) is
itself deterministic.

### 6.5 Preregistered kill bars

1. **All 7 shared gates pass** (same definitions as §5.5.1).
2. **3× byte-identical reruns** (SHA-256 match).
3. **Join quality by meter:** median boundary RMS discontinuity ≤ 3 dB
   across joins; zero frames with crest > 20 dB at join locations (no
   clicks by construction — measured, not asserted).
4. **Selection-not-shifting:** resample call count = 0 (code assertion);
   mean |log2(F0_unit/F0_target)| ≤ 0.15 across selected units — the F0
   arc must be achieved by *choosing* units near the targets, proving the
   inventory (not hidden pitch-shifting) does the work.
5. **Silence-source test:** zeroed inventory → bit-exact zero output.

**KILL EXPERIMENT (kills the approach itself):** the *shuffled-inventory*
control — rerun selection with the inventory mapping deterministically
permuted (documented fixed permutation: reversed unit order; no RNG).
Kill condition: if the shuffled run does NOT degrade — join-cost total
must rise ≥ 50% and ≥ 2 gates must fail (predicted: frac_static and
prosody) — then selection is vacuous (any unit works as well as the
chosen one) and the approach claim dies. Companion check: a synthetic
diphone inventory (formant-synthesized at matched F0s) through the same
chain must fail ≥ 3 gates; if it passes equally, realness is vacuous
(same logic as Fork 1's kill experiment).

### 6.6 Honest failure mode

Most likely: **ransom-note voice** — audible choppiness, vowel quality
jumping between syllables, joins the ear catches despite the meters.
What it tells us: the inventory is too sparse (one session, ~200 units)
for the join cost to hide — a *density* problem, solvable by recording
more (denser inventory), or by admitting that some minimal smoothing
(Fork 1's PSOLA) is load-bearing for musicality. Either way the lesson is
inside the law: record more, or borrow Fork 1's time-map — never an
oscillator.

---

## 7. FORK 3 — `surgery_collage`: arrangement-only composition — zero pitch manipulation, zero resampling

**One-line concept:** Prove composition alone can be compelling: a rhythmic
vocal-percussive piece from real chops, real transients, and real beds,
using ONLY cut / splice / reverse / layer / crossfade / gain.

### 7.1 Real source material

- Voiced chops: syllable-length voiced segments from `v5work/kidd.wav`,
  `kide.wav` (SHAs `ab22c5e4…`, `5d69f49d…`), cut at zero-crossings near
  energy minima.
- Real percussive transients: agent hunts `garry_point_park.wav`
  (`e286e604…`, 134 s) for onset crest ≥ 12 dB with 30–80 ms decays
  (claps, taps, real-world hits).
- Breath bed: quiet segments of `v5work/kida.wav` (`b8ad8e1a…`).
- Room bed: `garry_point_park_30s.wav` at fixed −30 dB throughout.

### 7.2 Exact manipulation chain

1. **Inventory listen.** Catalog chops (duration, F0, RMS, vowel class),
   transients (crest, decay time), beds. `inventory_manifest.md`.
2. **Target plan** (`edit_plan.md`): 12 s piece on a deterministic rhythm
   grid — 100 BPM ⇒ 600 ms beats = exactly 26,460 samples/beat (integer;
   no rounding drift). The agent places chops on grid slots by *matching
   chop duration to slot* (±10% tolerance; no time-stretch — if no chop
   fits, the agent picks another chop, logged); transients on off-beats;
   exactly one reversed chop per 4 bars (reversal = index inversion,
   §1.2 PASS 3); breath bed under gaps; room bed throughout.
3. **Assembly.** Hard cuts at zero-crossings (search ±50 samples for a
   sign change); 3 ms crossfades ONLY where a cut misses a zero-crossing
   (logged per cut); layering = sample addition at fixed gains
   (chops 0.5, transients 0.3, breath 0.2, room 0.06); final fixed gain
   0.5. **Resample call count: 0 — asserted in code and audited.**
4. **Sample accounting.** Output sample count must equal the sum of
   placed source sample counts, exactly; crossfade regions (convex
   combos) counted separately and must be ≤ 5% of total samples. Every
   non-crossfade output sample is a *copied* source sample — the
   strongest provenance claim of the three forks.
5. **Verify + iterate.** Gates, kill bars, silence test, 3×
   byte-identical. Replan = deterministic placement-rule change, logged.

### 7.3 Law-compliance argument

Nothing in this chain is even adjacent to synthesis: no resampling, no
interpolation, no time-maps, no filters. It is cut, splice, reverse,
layer, crossfade, gain — the operations the law names explicitly
("cut, splice… layer, crossfade, reverse… waveform surgery"). The silence
test passes trivially. If *this* fork were ruled synthesis, the law's own
examples would be illegal — it is the definitional anchor of the
permitted set.

### 7.4 Why agentic — and the experiment that tests it

This fork carries the native position's core claim — that *deliberate
choice* is where the value lives — so it also carries the experiment
that could kill that claim (§7.5, kill experiment). The agent listens to
the chop catalog and places chops for rhythmic fit, vowel contrast
across bars, and transient/chop call-and-response; a fixed pipeline
cannot do any of this.

### 7.5 Preregistered kill bars

1. **All 7 shared gates pass** — note this is a *real* bar here: the
   prosody gate (voiced F0 std ∈ [0.3%, 3%]) requires the chops' natural
   F0 variation to land in range; a too-percussive arrangement fails it
   honestly.
2. **3× byte-identical reruns** (SHA-256 match).
3. **Zero-resample audit:** code attestation + sample accounting (§7.2.4)
   — output length exactly equals placed source lengths; crossfade
   samples ≤ 5%.
4. **Click audit:** zero frames with crest > 20 dB outside the catalogued
   real transients — no cut artifacts masquerading as transients.
5. **Silence-source test:** zeroed sources → bit-exact zero output.

**KILL EXPERIMENT (kills the agentic claim itself):** the *chronological
control* — render the SAME chops on the SAME grid in *source order* (a
fixed, non-agentic rule: earliest-recorded chop goes in the earliest
slot). Kill condition: if the agent-arranged version does not beat the
chronological control on ≥ 2 of the 7 gates AND does not use a more
diverse chop set (distinct chops used), then agentic arrangement adds
nothing measurable — the agency claim dies, the fork reduces to its fixed
pipeline (which may continue without the agent). This is the honest,
preregistered test of §4's thesis. (Ear judgment, when Micah listens,
is the second oracle; the gate comparison is the agent-measurable one.)

### 7.6 Honest failure mode

Most likely: **collage, not music** — audible seams, rhythm that feels
pasted rather than played, the ear catching every edit. What it tells
us: zero-resample arrangement cannot smooth real discontinuities, and
some minimal time-alignment (Fork 1's PSOLA) is load-bearing for
musicality — i.e., the forks compose a ladder (Fork 3 ⊂ Fork 2 ⊂ Fork 1
in transform power), and the failure of Fork 3 bounds *how little*
transformation suffices. That is still a win for the law: it maps the
minimum, rather than assuming the maximum.

---

## 8. Shared infrastructure (all forks)

- **Language/toolchain:** pure Zag; pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
  Zero RNG in any decision path; deterministic tie-breaks (lowest unit
  id); fixed preregistered weight/parameter sets tried in fixed order.
- **Gates:** `audio_round2/shared/analyze.py` — frac_static (voiced frames
  within 5% of local median F0) ≥ 0.25; HNR ∈ [0.7, 6.7] dB; HF rolloff
  ∈ [−40, −12] dB; prosody ∈ [0.3%, 3%]; transient crest median ∈ [3, 20]
  dB; plus periodicity ≥ 0.5, peak < −1 dBFS, hum check (50/60 Hz +
  harmonics), spectral drift. Analyzer-first: no ear claim before gates.
- **Identity:** SHA-256 of every source (manifest §9), every inventory,
  every plan, every render. 3× byte-identical reruns required.
  Per `audio_predelivery_gate.md`: NEW / PREVIOUSLY SHOWN / REFERENCE
  labels; M4A for ear clips, WAV masters for measurement; measured
  delta vs previous version in every delivery note; agents describe
  measurements, never how anything "sounds."
- **No output-derived normalization** (standing law): gains fixed in the
  plan or derived from source measurements; over-peak renders fail the
  gate and trigger replan, never renormalization.
- **Compliance automation:** the silence test (M1) and the resample-call
  counter are unit tests in the renderer, run on every render. The
  provenance sidecar + spot-check is the audit trail.

## 9. Source manifest (SHA-256, verified 2026-09-24)

| File | SHA-256 |
|---|---|
| `aud_v11/diag/vowel_real.wav` | `8ba3b42708a8bab2bb8152d392d4425c5c248591d545f3bd1b24070e264e5d1d` |
| `v5work/kida.wav` | `b8ad8e1a1f4f70b01a602fd1848db8aacd9f4857311a19b72757f1af570cfd6e` |
| `v5work/kidb.wav` | `13285a0da02de5a830e289924ba4c9e5b831ac86bbd7de0002f033d7046682a3` |
| `v5work/kidc.wav` | `5a1b1f7b1f359f4fa6fff40580e72be5c34f33f300dc4b2f9a6140c78eb4ab44` |
| `v5work/kidd.wav` | `ab22c5e400c26c1693020317526f6bff69661b5a48fc7e58efdb085549c3e9dd` |
| `v5work/kide.wav` | `5d69f49dd6653c4bbd1fe5c0296b4240ff52224ce47e7062b0a12c05ba40c701` |
| `audio_round2/grain_unit/fossil_hi.bin` | `9439c067ee9a01841f702fec49571475336eb47318bbd999948617d8746a4622` |
| `tnn-lab/…/calibration/aporee_kids_play_area.wav` | `24981f77ff52acb701f3e6957ece9c5b5ab8d53857887d7bc69bc0d717c79b77` |
| `tnn-lab/…/calibration/garry_point_park.wav` | `e286e604ab0bcdb6fd944d48005fc7e57952ae0cab30fcda9d44cd4993100ba1` |
| `audio_round2/shared/smoke.wav` (calibration ref) | `a0e913dc2677d6cfa3dc8102be02b84c55e4013cd1a5bb25c06eab6024ace78a` |

Measured anchors: vowel_real F0 ≈ 400.9 Hz (autocorr 0.985); kidb–kide
median voiced F0 558–565 Hz, RMS ≈ −20 dBFS; kida quiet (RMS −48.4
dBFS — breath-bed source); fossil_hi F0 ~788 Hz, F1 ~2371, F2 ~4725.

## 10. What would change our mind

The native position is falsifiable, and we state the conditions plainly:

1. If all three forks pass every gate and kill bar yet score 0/3 (or
   worse than the retired synth line) on Micah's ears across two
   judgment rounds, the *sufficient* claim fails: real provenance is not
   sufficient for compelling audio, and something beyond manipulation is
   needed. The law, not the forks, becomes the variable.
2. If Fork 3's chronological control matches the agent arrangement
   (kill experiment fails), the *agency* claim fails for arrangement —
   we keep the pipeline, drop the agent, and say so.
3. If either kill experiment shows synthetic inventories passing gates
   as well as real ones, the *realness* claim is vacuous — the meters,
   not the law, are the problem, and we will say that too.

What would NOT change our mind: a fork failing its own kill bars. That
is the system working — preregistration doing its job, exactly as
Round-2 fork 2's (incorrect) kill bar did. A dead fork is evidence the
method is honest, not that the law is wrong.

---

*End of Native Position A. Three forks, one law, zero oscillators.*
