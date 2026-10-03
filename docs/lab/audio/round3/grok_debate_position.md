The no-synth law is an origin constraint, not a timbre recipe. The three forks below are three different ways of spending recorded samples and no other samples. They are designed so a reviewer can reject them with preregistered numbers, not taste.

---

## 0. Reviewer gate (apply this before any fork)

**Synthesis** = any output sample that is not a deterministic linear combination of samples physically stored in a named source WAV, with coefficients drawn only from a preregistered, input-independent family (fade curves, Hann windows, windowed-sinc kernels) or from a grid computed from those source files.

**Manipulation** = every output sample `y[n]` satisfies

```
y[n] = G * Σ_k  c_k(n) * x_{f_k}[i_k(n)]
```

where `x_f` is a file on disk, `i_k` is an index into that file (or a windowed-sinc interpolant at a fractional index between two such samples), `c_k` is from the allowed coefficient family, and `G` is a constant fixed before the render from **input** peaks only.

Delete the WAVs. If the program can still emit the artifact, it is synthesis. That test is the gate. Analyzer numbers are not a substitute: Round 2 already showed a source-filter cartoon can land inside HNR / periodicity / rolloff.

**Allowed coefficient family (closed):** rectangular cut, linear or equal-power crossfade of length declared in samples, Hann/Hamming analysis window, Blackman-windowed sinc of declared half-width, overlap-add division by the **window-grid** envelope `W[n]` (a function of hop positions and windows only, not of `x` and not of `y`). Analysis-only FIRs (epoch picking, MFCC) may exist and must not be written into `y`.

**Wavetable clause (the hard case):** copying one recorded cycle and looping it at audio rate to manufacture pitch is an oscillator whose table was filled from a microphone. Forbidden, even though the table is “real.” A design is on the manipulation side only if analysis time **progresses** through the recording so cycle-to-cycle jitter, shimmer, and breath noise in the source actually reach the output.

**PASS**

1. Cut `[a,b)` from `vowel_real.wav`, equal-power crossfade 10 ms onto a cut from `breath.wav`.
2. TD-PSOLA that copies successive real epoch grains and overlap-adds them on a new grid, grain interiors not resampled, epoch index advancing.
3. WSOLA that duplicates or skips correlation-aligned **source** segments to change duration.

**FAIL**

1. Band-limited saw or LF pulse through formant biquads, even with F1/F2 measured from the child.
2. LPC (or any source-filter) whose excitation is an impulse train, noise, or LF model, even if the coefficients were fit to a real vowel.
3. A noise-burst “transient,” a Hann-windowed sine grain, or a phase vocoder that keeps magnitudes but replaces phases with a harmonic phase rule.
4. (Boundary, also FAIL) one 5 ms fossil cycle looped for 2 s. Real table, oscillator mechanism.

Gray zone, **not used in any fork below:** phase vocoder with the recording’s own phases, hop changed, bins otherwise untouched. Lineage is real, but the IFFT path is where Round-2-style “resynthesis” hides. Stay in the time domain until that gray zone is separately legislated.

**Round 2 failed the law while passing gates** because the gates measure spectral shape and periodicity, and a parametric glottal model is built to hit those. Provenance is not identifiable from HNR. LF pulses, formant filters, and band-limited saws still generate every sample from equations. Measuring the child and then driving a synth is fitting a cartoon, not editing a recording. 3/6 gate passes are evidence the gates are necessary and not sufficient. The origin test is the missing gate.

**“No output-derived normalization”** is honored as: no measure-the-render-then-scale step. `G` comes from the input file’s peak, logged before any overlap-add. Division by `W[n]` is allowed only because `W` does not depend on sample values.

**Determinism (all three forks):** single thread, accumulation in increasing segment index only, `float64` with round-to-nearest-even, no `rand`, no clock seed, every stage buffer hashed SHA-256, three byte-identical reruns required. Epoch and Viterbi tie-breaks are lowest index, never a coin flip.

**Gate tension to preregister before claiming ears:** HNR `3.7 ± 3 dB` is breathy, not sung-choir clean. Do not denoise; do not average cycles together (averaging raises HNR and also invents a cycle that never occurred). PROSODY CV `[0.3%, 3%]` is narrower than ordinary child speech (a semitone is already ~6% in frequency ratio). First logged act of every fork: measure the anchor and the donor. If the anchor itself sits outside a gate, that gate is not a realness test; report it and do not “fix” the audio to satisfy a broken interval. Affine compression of a measured F0 contour to force the CV into band is legal under the origin test and scientifically dirty. It is not in these designs.

---

## 1. Fork A — `epoch_graft`

**Concept.** TD-PSOLA of successive real glottal cycles from a vowel fossil, placed on epoch times measured from a different real utterance, grain interiors copied, not resynthesized.

**Sources.**

- Timbre: one vowel-core excerpt from the fossil set, the same family as the `vowel_fossils` fork that actually sounded organic. Prefer the core cut from `vowel_real.wav` if its logged SHA matches the anchor; otherwise the fossil whose offset is logged against the 134 s field tape. Use ≥ 400 ms of voiced audio so the cycle inventory is not a single period.
- Prosody donor: one short voiced region of `kida.wav` … `kide.wav`, chosen **before** listening to the render, by the rule “longest contiguous voiced run whose measured F0 CV already lies in `[0.3%, 3%]`.” If none do, take the run with CV closest to the anchor’s CV and report the gate conflict. Do not warp the contour.
- No playground bed, no breath layer. One mechanism only.

**Chain.**

1. SHA-256 the two slices. Record `G = min(1, 10^(-1/20) / peak_input)` from the fossil slice peak so a full-scale input cannot clip at −1 dBFS under a two-window overlap. `G` is logged and frozen.
2. Epoch track (analysis only, discarded after marks exist), identical settings on both files. Frame 40 ms, hop 5 ms, Hann. Normalized autocorrelation, lag search `[⌊fs/800⌋, ⌈fs/80⌉]` → F0 ∈ `[80, 800]` Hz at 44.1 kHz. Voiced iff peak `r ≥ 0.5`. Parabolic refine, then **snap to nearest sample**. Unvoiced gaps stay unvoiced; do not fill them with noise.
3. Analysis grain for epoch `s_i` with period `τ_i = s_i − s_{i−1}`: samples `[s_i − τ_i, s_i + τ_i)`, multiplied by a Hann of that length. The payload before the Hann must be bit-identical to the file. Grain length is two local periods, the standard TD-PSOLA choice (Moulines & Charpentier).
4. Synthesis grid = the donor’s snapped epoch times `d_j` and nowhere else. Mapping `i(j) = clamp(round(j * (N_s−1)/(N_d−1)), 0, N_s−1)`. Monotonic. A source epoch may be reused at most **twice** (the time-stretch case). At least 50% of synthesis epochs must point at unique source epochs. If the donor is longer than that policy allows, truncate the donor; do not start looping the fossil.
5. Place grain `i(j)` so its center sample lands on `d_j`. No resampling of the grain interior. Pitch change is **only** the change in spacing between centers. Formants stay because the cycle shape is the recorded shape.
6. Overlap-add in increasing `j`. `W[n] = Σ Hann_j[n − d_j]`. `y[n] = G * Σ (windowed grain)_j / W[n]` where `W[n] > 0`, else `0`. Unvoiced donor intervals: copy the corresponding mapped fossil samples raw, 5 ms equal-power crossfade at each voiced edge, coefficients from the allowed family.
7. Do not lowpass, do not add noise, do not normalize to the output peak. Hum check and the global gates on `y`. Emit the provenance table `(n-range → file, source index, epoch id)`.

**Why this is not a synth.** No sample is computed from a glottal formula. Autocorrelation only **selects indices**. The Hann is a coefficient, not a source. Changing the hop is editing the clock of real cycles, which is what the earlier fossil fork already did. It becomes a synth at the moment step 4 is replaced by “repeat grain 0.” That version is the kill condition, not the fork.

Time-stretch here is duplication or deletion of recorded cycles. Granular resampling is not used. The line is the wavetable clause above, and this design stays on the legal side by the 50% / max-reuse-2 rule.

**Kill bars.**

1. Provenance: 100% of non-zero `y[n]` rows in the table point into the fossil slice. One sample without a source index kills the fork.
2. Progress: unique-epoch fraction ≥ 0.50 and max reuse ≤ 2. Fail → reclassify as wavetable, kill.
3. Inherited gates, all of them, on the real-source render: `frac_static ≥ 0.25`, HNR in `[0.7, 6.7]` dB, autocorr at the **donor** period ≥ 0.5, HF band in `[−40, −12]` dB, F0 CV in `[0.3%, 3%]` or the documented anchor exception, onset peak-to-RMS in `[3, 20]` dB, peak `< −1` dBFS.
4. Grain integrity: before the Hann, each extracted cycle matches the file bytes at that index. After the full chain, a cycle placed with no overlap (isolated) correlates with its source cycle at ≥ 0.999. Fail → the implementation resampled or filtered the grain.
5. Donor tracking: synthesis F0 median within 3% of the donor’s measured median, and within 15% of the fossil’s median only if the donor happened to sit there. Pitch error > 5% against the donor kills the “transplant” claim.
6. Three renders, identical SHA-256. Any mismatch kills the fork regardless of sound.

**Kill experiment.** Freeze: build `epoch_graft_freeze` by forcing `i(j) = i(0)` for every `j`, same grid, same window, same `G`. If freeze still passes every numeric bar in (3) **and** a fixed A/B script does not separate it from the progressing fork on cycle-to-cycle spectral flux (flux std of freeze ≥ 0.5× flux std of the real fork), then progressing through the fossil is not load-bearing and the fork is a wavetable. Kill it. Second arm, run only as a negative control, never as a candidate: same grid fed by an LF pulse train with F0 copied from the donor. If HNR and HF do **not** leave the anchor box relative to the real-source fork, the metrics cannot see provenance. That kills the evaluation, and the fork may not claim a gate pass as evidence of realness until a provenance audit is mandatory.

**Honest failure.** Most likely a clean but dead sampler vowel: organic cycle, correct-ish pitch, comb or chorus from the overlap, prosody that is a few hertz of wobble and nothing like a person changing their mind. Listener line: “edited sample, not a take.” That tells us one fossil plus a foreign clock is not speech. It does not license a return to LF. It licenses Fork B (longer real units) or a longer real performance as the donor. Metallic buzz with HNR above 6.7 dB means the overlap-add averaged the breath out of the cycles; the upper HNR bar is there to catch that. Epoch snaps locking onto formant peaks instead of closure will sound like the Round-1 alien; the kill is bar 4 plus periodicity, and the fix is a better **measurement**, not an excitation model.

---

## 2. Fork B — `inventory_splice`

**Concept.** Concatenative assembly of real diphones and vowel nuclei. Deterministic Viterbi. Joins are short crossfades of the two recorded waveforms. No residual, no filter, no excitation.

**Sources.**

- Inventory, exclusive of the donor take: hand-specified or energy-and-delta-MFCC cuts from `kidb.wav` … `kide.wav`, plus fossil vowel cores **other than** the anchor slice used as the spectral target. Each unit is a row `(file, start, end, left_phone, right_phone, sha256_of_slice)`. Minimum unit length 40 ms (one phoneme or a diphone, not a single glottal cycle — that would collapse into Fork A’s wavetable failure).
- Target specification, not a generative model: a phonetic string that is actually attested in `kida.wav`, plus duration and voiced/unvoiced labels measured from `kida.wav`. `kida.wav` is then **banned from the inventory** so the solver cannot win by handing the take back unchanged.
- Spectral target vectors: MFCCs measured on `kida.wav`. They are a cost function, not a filter that is later excited.

**Chain.**

1. Freeze the inventory table and the phone string in the preregistration. Hash both.
2. Analysis (not audio): 25 ms window, 10 ms hop, 12 MFCCs + log energy, same code on every unit and on the donor. Also store, for each unit, the raw edge vectors: first and last 10 ms of samples, and the unit’s measured median F0 if voiced.
3. Costs, all deterministic:
   - Target cost = L2 distance between the unit’s mean MFCC and the donor frame-average MFCC for that phone, plus `0.5 * |log(dur_unit/dur_target)|`, plus a large constant (1000) if phone labels disagree.
   - Join cost between unit `p` ending and unit `q` starting = RMS of the difference of their 10 ms edges after an equal-power crossfade of length `C` samples, plus L2 of the edge MFCCs. `C` is frozen at 10 ms (441 samples). It is not increased after listening.
   - Transition forbidden (infinite cost) unless `right_phone(p) == left_phone(q)` or either side is a declared boundary phone.
4. Viterbi. Standard DP, best predecessor on ties = lowest unit index. No pruning that depends on a random beam. Path is a list of `(unit_id, source range)`.
5. Render: concatenate the raw slices. At each join, overlap `C` samples with equal-power weights `cos(πn/2C)`, `sin(πn/2C)` applied to the **recorded** edge samples. No waveform interpolation between interiors, no PSOLA, no micro-pitch shift. If two adjacent units disagree in F0 by more than 5%, that is a bad join and the cost function is supposed to avoid it; do not “correct” it with an oscillator.
6. Single declared gain from the **maximum input-slice peak** across the chosen units, same −1 dBFS headroom rule as Fork A. No output peak normalize.
7. Write the path and the sample-index map. Global gates. Hum check.

**Why this is not a synth.** Unit-selection speech (the pre-neural Festival / AT&T kind) was concatenation plus a search. The failure mode of commercial systems was the join, and the industry “fixed” it by adding parametric smoothing and then neural vocoders. Those fixes are exactly what the law now forbids. This fork keeps the part that was real and drops the part that was a synth. Viterbi does not create samples; it picks intervals. A crossfade is the “layer / crossfade” clause with both parents on disk.

It is synthesis if a join is replaced by an LPC residual, a diphone-model interpolator, or any filter whose impulse response is not just the crossfade ramp. It is a synth if units shrink to one cycle and the path repeats a favorite cycle. Bar 2 blocks that.

**Kill bars.**

1. Donor exclusion: zero samples with provenance in `kida.wav`. The reference take appearing in `y` kills the fork (trivial copy).
2. Unit length: every selected unit ≥ 40 ms and ≥ 2 measured periods if voiced. Single-cycle units kill the fork.
3. Join click: at each boundary, after the crossfade, sample-to-sample first difference peak ≤ 4× the median first difference of the two unit interiors, and spectral flux in the join frame ≤ 2× the median interior flux. Any join failing this, **at the frozen `C = 10 ms`**, kills the fork. Widening `C` past 30 ms to hide a click also kills it (the crossfade has eaten the units).
4. Inherited analyzer gates, same numbers as Fork A. Plus path stability: Viterbi run three times, identical unit-id sequence, identical output SHA.
5. Inventory coverage sanity: no unit used more than twice. A two-unit loop is a sampler phrase, not a concatenation. Kill.

**Kill experiment.** Ablate the join cost: set it to 0 and take the Viterbi path that optimizes target cost only (still deterministic). If the click bar (3) still passes, join cost is not load-bearing and the fork’s distinctive claim is dead; ship dumb phone-matched concatenation or kill the machinery. Negative control, not a candidate: render the **same path** with every unit replaced by an LF-plus-formant diphone of matched duration and median F0. The fork’s approach is killed as a realness claim if this cartoon stays inside the HNR box **and** inside 3 dB of the real-unit fork’s HNR. (Expected outcome: the cartoon leaves the box. If it does not, stop citing gates as evidence and require the provenance audit, same as Fork A.)

**Honest failure.** Ransom-note speech. Each fragment is a real child, the sequence is correct, and every join is a tiny cut, a level jump, or a vowel that changes mouth mid-phone. Metrics can pass while the ear says “doll.” That tells us this inventory is too small and too inconsistent for unit selection, which is the known corpus-size failure of concatenative TTS, not a secret lack of oscillators. The legal response is more real diphones of the same speaker, recorded on purpose, or shorter utterances that need fewer joins. The illegal response is a smoothing vocoder. If the unedited donor is obviously better than the assembly, the fork has not earned its complexity; say so and keep it only as a recombination test, not as a product.

---

## 3. Fork C — `onset_graft`

**Concept.** A single voiced nucleus time-stretched by source-side WSOLA, with the attack and the release cut from other real files. Tests whether the transient and the air have to be recorded rather than noised in. No pitch shift at all, so it cannot be accused of hiding an oscillator in the transpose.

**Sources.**

- Nucleus: fossil vowel core or `vowel_real.wav`, ≥ 300 ms voiced, SHA logged. This is the only pitched material.
- Onset: a real percussive transient from the playground/percussion bed, or, if a logged mouth-onset exists inside `kidc.wav`–`kide.wav`, that onset. Cut is `[t0, t0+30 ms]` with `t0` at the sample of maximum absolute slope inside a preregistered 200 ms neighborhood. Fixed rule, not a fader move after listening.
- Release: a real breath recording, **reversed** (reversal is an allowed permutation), 80 ms, equal-power into the tail.
- No noise generator for the consonant. If the beds do not contain a usable onset, the fork is killed for lack of source, not “fixed” with a burst.

**Chain.**

1. Input gains, frozen: nucleus `G_n` from its own peak, transient `G_t = 0.2 * G_n`, breath `G_b = 0.35 * G_n`. Constants in the preregistration, not fit to the mixdown.
2. WSOLA, **source-side only**, so the search never reads `y` and cannot be called output-derived normalization. Segment length `L = 1024` (~23.2 ms). Analysis hop `Ha = 512`. Synthesis hop `Hs = round(512 * T_target / T_source)`, integer. Stretch factor restricted to `[0.85, 1.25]`. Target duration = the preregistered nucleus length times that factor; pick the factor so the **rendered** F0 CV and the held-note fraction have a chance at the gates, but choose it from the input duration, not from a listening pass. Search range `R = 128` samples.
3. Alignment: for frame `m`, expected source position `p_m = m * Ha`. Choose
   `δ* = argmax_{δ ∈ [−R, R]}  Σ_{n=0}^{L/2}  x[p_{m−1} + δ*_{m−1} + L/2 + n] * x[p_m + δ + n]`
   i.e. correlation of the **previous source frame’s tail** with the candidate’s head. Tie → `δ = 0`, then lowest `δ`. Copy `x[p_m+δ* : p_m+δ*+L]` into the output on hop `Hs` with a Hann overlap-add, divide by the window grid `W[n]` only. This is duplication and deletion of recorded blocks plus a crossfade. It is not a phase vocoder.
4. Place the transient cut at sample 0. Place the WSOLA nucleus so it starts at sample 441 (10 ms), 10 ms equal-power crossfade, weights on the two **real** streams. Place the reversed breath so it starts 40 ms before the nucleus ends, same crossfade.
5. Sum the three streams with the frozen gains. No bus compressor, no saturator, no EQ. Those would be extra filters in the audio path; they are not in the allowed coefficient family.
6. Provenance map must list, for every output sample, one, two, or three source triples `(file, index, coefficient)`. Coefficients must match the preregistered ramps. Hash the output.

**Why this is not a synth.** WSOLA’s search picks a source index. The copied block is the recording. Reversal is a permutation. Layering is the law’s “layer” clause. Time-stretch of this kind does not invent a waveform shape; past a small stretch it **repeats** one, which is why the stretch factor is capped and why stutter is a kill, not a texture.

It would be synthesis if the transient were a filtered noise burst, if the breath were shaped noise, or if pitch-shifting were done by resampling a grain so hard that a new sample rate clock became the oscillator. Naive resampling of a whole vowel (chipmunk) is still manipulation under the origin test, and it is a bad fork; it is not this one. Granular clouds with grains shorter than one period are legal only in the narrow origin sense and are the Round-1 “static / alien” path. Bar 2 forbids them.

**Kill bars.**

1. Stretch factor inside `[0.85, 1.25]`. Outside, kill, before anyone listens. Inside, repeated-block fraction: fraction of synthesis frames whose source index was already used ≥ 0.5 kills the fork (audible stutter is the failure mode, measured rather than debated).
2. Grain identity: every WSOLA frame correlates at ≥ 0.98 with the source interval it claims, on the raw samples before the Hann. Below that, the implementation drifted into filtering or interpolation that was not specified.
3. Transient necessity: render an ablation with `G_t = 0`. The full mix must sit in onset peak-to-RMS `[3, 20]` dB. The ablation must fall **below 3 dB**. If the ablation still passes, the transient layer is decorative and the fork is just “a vowel with a fade.” Kill the graft claim.
4. HF necessity, same shape: energy above 8 kHz on the full mix inside `[−40, −12]` dB. On the nucleus-only render it must drop by ≥ 6 dB **or** the nucleus alone must already satisfy the HF gate, in which case the write-up must say the air came from the vowel recording and the breath layer is not the HF story. Claiming the breath “added the air” when this delta is < 6 dB kills the claim.
5. Inherited gates on the full mix, plus peak `< −1` dBFS, plus three identical SHAs. Provenance: every sample maps only into the three declared files.

**Kill experiment.** Naive splice: same hops, `δ* = 0` always, no correlation search. If splice-flux at frame boundaries is not at least 6 dB **worse** than aligned WSOLA, the search is not earning its keep. Kill WSOLA as the mechanism and keep plain cuts if the cuts themselves pass. If both fail the ear the same way (“stuttering vowel over a playground click”), the fork’s hypothesis is wrong: recorded beds plus a stretched vowel do not make a voice. That is a useful death. It would mean organic timbre in this program lives in continuous cycle progress (Fork A) or in real phonetic units (Fork B), not in montage.

**Honest failure.** A collage. The vowel is the anchor, the click is a click, the breath is a breath, and nothing in the middle is a consonant produced by a mouth. Listener line from Round 1 that fits: “video-game character,” or a field recording with a sample pasted on. That tells us layering real objects does not create the articulations we never recorded. The missing sound is a missing **take**, not a missing algorithm. If WSOLA stutters inside the allowed stretch range, correlation alignment is not enough at 44.1 kHz on this material, and the legal fallback is to use a take that is already the right length.

---

## Where novelty comes from if nothing is generated

It does not come from new timbre. Under this law a new timbre is a confession that a generator ran. The novelty budget is the same one tape editors and unit-selection systems actually had:

- **Which** recorded interval, **in what order**, **on what clock**, **against which other real interval**.
- Fork A’s novelty is a real cycle sequence on a clock it did not originally have. The organic part (jitter, breath, formant motion inside the cycle) is inherited because the index moves.
- Fork B’s novelty is a sequence that was not a single contiguous take, with the donor banned so the output cannot be the input.
- Fork C’s novelty is a duration and an onset/release the nucleus take did not have, each piece still a recording.

That is composition, not synthesis. Film editing does not become CGI because the cut is new. Musique concrète did not become a subtractive synth because the tape ran backward.

What the law makes impossible, and what the other side will correctly say out loud: a speaker who is not in the corpus, a consonant that was never recorded, a pitch the grains cannot reach without resampling them into a new formant structure, emotional timing that none of the donors contain. Affine “expression curves,” vibrato LFO depths, and jitter drawn from a Gaussian are generators with the serial numbers filed off. They stay out.

“Compelling” therefore cannot mean “a voice that never existed.” It means “a listener classifies it as edited real audio of this child, and the edit does something none of the raw takes did.” If the unedited anchor wins every A/B, the honest program result is: we may only play the recordings. That result is still a result. Round 1’s 0/10 and the “shitty synth / earrape / alien” notes are what generating new samples bought.

The other side’s attack — “then you aren’t making anything” — is half right. We are not making timbre. We are making arrangements of timbre whose origin a reviewer can audit with a sample-index table and a delete-the-WAVs test. After Round 2, a gate pass without that table is not evidence of anything the law cares about.
