# ROUND 3 PREREGISTRATION — no-synth audio (FROZEN)

Date frozen: 2026-09-24 PDT. Branch: `tnn-native-lab` (repo `sylorlabs/TNN`).
Debate inputs: `grok_debate_position.md`, `native_position_A.md`,
`native_position_B.md`. Judging rubric: `JUDGING_RUBRIC.md`.

## 0. Binding direction from Micah

- NO SYNTHESIZERS, PERIOD. No oscillators, no formant synths, no LF
  models, no parametric excitation, no physical models acting as
  synthesizers. Forbidden set is exactly this.
- Permitted (his words): "cut, splice, stretch, layer, crossfade,
  reverse, resynthesize from recordings, granularly manipulate real
  audio, waveform surgery, concatenative real units."
- Round-2 ear verdicts: CLIP_A glottal_formant = BEST (notation correct,
  NO STATIC); CLIP_B skeleton_refine = middle; CLIP_C prosody_ab = WORST
  (lots of static). **STATIC IS THE KILLER.** "No audible static" is a
  hard gate for anything reaching Micah's ears. glottal_formant's
  clarity is the bar to beat — without synths.
- Round 2's synth forks are RETIRED, not retroactively wrong.
- Pure Zag. Zero RNG in decision paths. Byte-identical reruns.
- Preregister kill bars before building. Analyzer-first: no ear claim
  before waveform analysis.
- Commit incrementally. Report measured deltas vs Round 2 + SHA-256.
- Stage survivors under neutral `CLIP_X` labels; attribution revealed
  only after Micah's numbered ear verdicts. Micah's ears outrank metrics.

## 1. Debate verdict (judge's ruling)

### 1.1 The strict/permissive boundary — RULED

Native-B's razor (one recorded sample per output sample; no crossfade,
no resample, no layering) is intellectually sharp but OVERSTRICT:
it deletes operations Micah explicitly named as permitted
("grain-resample", "crossfade", "layer", "stretch"). The user outranks
the debate. RULING: the permitted set is Micah's vocabulary; the
forbidden set is his forbidden list. Resampling-as-reconstruction,
equal-power crossfades of real streams, and layering of real streams
are LEGAL. What stays forbidden: any designed excitation (oscillator,
LF pulse, noise burst, PRNG/hash evaluated at output index), any
filter that creates phonetic identity (formant filters turning
excitation into vowels), wavetable looping of a single cycle.

### 1.2 Adopted mechanisms (4)

| # | Name | Source | Verdict |
|---|------|--------|---------|
| F1 | `epoch_graft` | grok A + native-A F1 merged | ADOPT |
| F2 | `inventory_splice` | grok B + native-A F2 merged | ADOPT |
| F3 | `onset_graft` | grok C | ADOPT |
| F4 | conscious-KB audio editor | `KB_FORK_DESIGN.md` (mandatory) | ADOPT |

REJECTED as standalone forks (kept as controls/audit standards):
- native-A F3 `surgery_collage`: pure arrangement adds nothing over
  F4's deliberate planning + F2's selection; its ladder argument is kept
  as an ablation, not a product.
- native-B `PALINDROME`: produces babble by design ("interesting babble,
  not speech" is its own honest verdict); not a product. Its
  permutation-proof (multiset equality) is adopted as the provenance
  audit gold standard.
- native-B `SUTURE`: kept as a CONTROL ARM inside F1 (butt-splice-only
  variant vs overlap-add variant) — head-to-head tests whether OLA is
  load-bearing for quality, which is exactly the permissive/strict
  boundary, tested empirically instead of argued.

### 1.3 Why these four

- F1 inherits the only organic success in program history
  (vowel_fossils' real-cycle PSOLA) with the wavetable failure mode
  fenced by hard numbers (max reuse 2, ≥50% unique epochs, freeze
  control).
- F2 is the strictest mechanism that still targets directed speech
  (novel utterance, zero resampling, donor banned).
- F3 tests the transient/air hypothesis: must the attack and the room
  be recorded? With necessity ablations that can kill the graft claim.
- F4 is Micah's explicit order: the conscious KB must finish and
  autonomously activate — it operates F1/F2 mechanisms, makes the
  deliberate choices itself, gates itself, revises or withholds.

## 2. Global kill bars (all forks, no exceptions)

- G1 PROVENANCE: 100% of non-zero output samples map to
  (source SHA-256, source offset). Spot-check ≥1000 indices; multiset
  check where the mechanism is a pure permutation/copy.
- G2 DETERMINISM: 3 renders, byte-identical SHA-256. Any mismatch kills.
- G3 SHARED ANALYZER GATES (`audio_round2/shared/analyze.py`):
  frac_static ≥ 0.25; HNR ∈ [0.7, 6.7] dB; periodicity (autocorr peak)
  ≥ 0.5; HF band ∈ [−40, −12] dB rel peak; prosody CV ∈ [0.3%, 3%]
  (documented anchor exception allowed, never silent); transient crest
  ∈ [3, 20] dB; peak < −1 dBFS; hum check clean (50/60 Hz + harmonics).
- G4 NO-STATIC AUDIT (hard gate, from Micah's verdicts):
  (a) max boundary discontinuity ≤ −40 dB rel peak;
  (b) no 50 ms frame with crest > 20 dB outside catalogued real
      transients;
  (c) voiced-region 8–16 kHz energy ≤ −30 dB rel peak;
  (d) no sub-period grains in the audio path.
  Fail any → repair once, then kill. Nothing reaches ears failing G4.
- G5 SILENCE TEST: zeroed sources → bit-exact zero output. Automated.
- G6 NO OUTPUT-DERIVED NORMALIZATION. No denoise. No cycle averaging.
  Gains from input peaks only, logged before render. Over-peak =
  failed render → replan with lower fixed gains, never renormalize.
- G7 EAR STAGING: only after G1–G6 pass. Neutral `CLIP_X` labels.
  M4A for ears, WAV masters for measurement. Delivery note carries
  measured delta vs Round 2. Micah's ears outrank every metric.

## 3. F1 — epoch_graft (TD-PSOLA of real glottal cycles on a donor clock)

Sources: vowel-core excerpt (fossil set or `vowel_real.wav`,
SHA `8ba3b427…5d1d`, ≥400 ms voiced); prosody donor = longest
contiguous voiced run in `kida.wav`…`kide.wav` whose measured F0 CV
already lies in [0.3%, 3%] (else closest-to-anchor CV + documented
gate conflict). No beds in primary render.

Chain: epoch-track both files (40 ms frame, 5 ms hop, Hann,
normalized autocorr, lag [⌊fs/800⌋, ⌈fs/80⌉], voiced iff r ≥ 0.5,
parabolic refine, snap to sample). Analysis grain per epoch
`[s_i − τ_i, s_i + τ_i)` × Hann (payload bit-identical to file).
Synthesis grid = donor's snapped epochs. Mapping monotonic;
max reuse 2; ≥50% unique source epochs; truncate donor rather than
loop fossil. Overlap-add in increasing j; divide by window-grid W[n]
only. Unvoiced donor intervals: raw mapped fossil samples, 5 ms
equal-power crossfades at voiced edges. Gain G from fossil-slice
input peak, −1 dBFS headroom, frozen. No lowpass, no added noise.

Variants (head-to-head, same gates):
- (a) no-resample grain interiors (grok primary);
- (b) windowed-sinc resample per grain, r ∈ [0.75, 1.33] (native-A);
- (c) SUTURE-style butt-splice-only, no OLA (strict control).
No vibrato in primary. One vibrato-as-time-map variant allowed as
secondary, same bars, clearly labeled.

Kill bars:
- F1.1 unique-epoch fraction ≥ 0.50 AND max reuse ≤ 2, else reclassify
  as wavetable and kill.
- F1.2 grain integrity: pre-Hann cycle bit-identical to file bytes;
  isolated placed cycle correlates ≥ 0.999 with source cycle.
- F1.3 donor tracking: rendered F0 median within 3% of donor median.
- F1.4 FREEZE CONTROL: `i(j) = i(0)` for all j. If freeze passes all
  G-bars AND flux-std(freeze) ≥ 0.5 × flux-std(real), the fork is a
  wavetable → kill.
- F1.5 NEGATIVE CONTROL: LF pulse train on same grid. If it stays in
  the HNR box AND within 3 dB of real-fork HNR, metrics can't see
  provenance → gates may not be cited as realness evidence.
- F1.6 variant comparison reported; ear staging picks the
  best-on-gates variant only (one CLIP_X per fork, not three).

## 4. F2 — inventory_splice (deterministic concatenative unit selection)

Sources: inventory from `kidb.wav`…`kide.wav` + fossil vowel cores
EXCLUDING the donor take. Target: phonetic string + durations +
voiced/unvoiced labels measured from `kida.wav`; `kida.wav` BANNED
from inventory. Min unit 40 ms (≥2 periods if voiced).

Chain: freeze inventory table + phone string in prereg, hash both.
25 ms/10 ms 12-MFCC + log-energy analysis. Target cost = L2(unit
mean MFCC, donor phone-avg MFCC) + 0.5·|log(dur_u/dur_t)| + 1000 if
phones disagree. Join cost = RMS edge difference after frozen
C = 10 ms (441 samples) equal-power crossfade + L2 edge MFCCs.
Forbidden transitions = infinite cost. Viterbi, ties → lowest unit
index. Render: raw slices, equal-power crossfades at joins only.
No PSOLA, no micro-pitch shift, no time-stretch (resample call
count = 0, code-asserted). Gain from max input-slice peak, −1 dBFS
headroom. Path + sample-index map written.

Kill bars:
- F2.1 zero samples with provenance in `kida.wav` (donor exclusion).
- F2.2 every unit ≥ 40 ms, ≥ 2 periods if voiced; no unit used > 2×.
- F2.3 join click: boundary first-difference peak ≤ 4× interior
  median; join-frame flux ≤ 2× interior median; at frozen C = 10 ms.
  Widening C past 30 ms kills.
- F2.4 Viterbi 3× identical unit-id sequence + identical output SHA.
- F2.5 ABLATION: join cost = 0 path must degrade (join-cost total
  rises ≥ 50% AND ≥ 2 gates fail), else the join machinery is
  decorative.
- F2.6 NEGATIVE CONTROL: LF-plus-formant diphones of matched
  duration/F0 on the same path must fail ≥ 3 gates, else realness
  claim is vacuous.

## 5. F3 — onset_graft (WSOLA nucleus + real transient + reversed breath)

Sources: nucleus = fossil vowel core or `vowel_real.wav`, ≥300 ms
voiced; onset = real percussive transient (playground bed or mouth
onset in kidc–kide), cut [t0, t0+30 ms] at max |slope| in a
preregistered 200 ms neighborhood; release = 80 ms real breath,
reversed. No pitch shift. If no usable onset exists in real sources,
fork dies for lack of source — never synthesized.

Chain: frozen gains (nucleus G_n from its peak; transient 0.2·G_n;
breath 0.35·G_n). Source-side WSOLA: L = 1024, Ha = 512,
Hs = round(512·T_target/T_source), stretch ∈ [0.85, 1.25],
R = 128, correlation of previous source frame tail vs candidate
head, ties → δ = 0 then lowest δ. Hann OLA, divide by window grid
only. Transient at sample 0; nucleus starts sample 441 (10 ms
equal-power crossfade); reversed breath starts 40 ms before nucleus
end. Sum at frozen gains. No compressor/saturator/EQ.

Kill bars:
- F3.1 stretch ∈ [0.85, 1.25]; repeated-block fraction < 0.5.
- F3.2 every WSOLA frame correlates ≥ 0.98 with claimed source
  interval (pre-Hann raw samples).
- F3.3 TRANSIENT NECESSITY: G_t = 0 ablation must fall below 3 dB
  onset crest while full mix sits in [3, 20] dB, else the graft
  claim dies.
- F3.4 HF NECESSITY: full-mix HF ∈ [−40, −12] dB; nucleus-only must
  drop ≥ 6 dB OR write-up admits the air came from the vowel and
  the breath layer is not the HF story (claiming otherwise kills
  the claim).
- F3.5 NAIVE-SPLICE CONTROL: δ* = 0 always. If boundary flux is not
  ≥ 6 dB worse than aligned WSOLA, WSOLA dies as the mechanism.

## 6. F4 — conscious-KB audio editor (autonomous)

Per `KB_FORK_DESIGN.md`, now binding: the KB fork operates the F1
and F2 mechanisms (its render backends). It consciously installs
real-audio units into the KB (source SHA, offsets, measurements,
provenance), deliberately writes an edit plan (target + selection
rule + fixed gains), renders, runs G1–G6 gates itself, and either
commits the passing result with full provenance or revises the plan
(≤ 2 replans, each naming the failed bar and the exact delta) or
withholds. The full cycle completes with ZERO human decisions.

Kill bars:
- F4.1 silent overwrites refused; 100% provenance; shared gates;
  3× byte-identical reruns.
- F4.2 bounded revision: after 2 failed replans it withholds —
  no infinite loop, no silent parameter drift.
- F4.3 SELF-KILL: replace real sources with synthetic sources
  carrying matching descriptors. If quality does not collapse
  (gates still pass / no withhold), the real-source claim is
  vacuous → kill.
- F4.4 autonomy audit: every decision in the loop logged with a
  reason; any human decision inside the loop (beyond the initial
  tasking) fails activation.

## 7. Analyzer-first protocol (standing)

Every render: HNR, spectrum, hum, transients, periodicity, prosody,
spectral drift, G4 static audit — BEFORE any listening claim.
Measured delta vs Round 2 in every delivery note. SHA-256 on every
file. Agents describe measurements, never how anything "sounds."

## 8. Build + staging

- Build all four in parallel, pure Zag, pinned toolchain.
- Prereg (this file) committed BEFORE code.
- Deliverables per fork: WAV master, provenance table, analyzer
  report, SHA log, RUNLOG.md.
- Ear staging: at most one CLIP_X per fork, only G1–G7 survivors.
  NEW labels (all Round-3 material is new). Attribution revealed
  only after Micah's numbered verdicts.

## 9. What kills the program direction (not just a fork)

- All four forks pass G1–G7 yet score below the retired
  glottal_formant line on Micah's ears across two judgment rounds →
  real provenance is not sufficient; the LAW becomes the variable.
- F1.5/F2.6 negative controls show metrics can't see provenance →
  gates lose their evidence status; provenance audit becomes the
  only admissible evidence.

---
*Frozen 2026-09-24 PDT. Amendments need Micah's word.*
