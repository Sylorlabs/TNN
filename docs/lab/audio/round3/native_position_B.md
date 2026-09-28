# NATIVE POSITION B — the skeptic-engineer: the no-synth law is right, and almost every "manipulation" proposal violates it

**Debate:** no-synth audio for TNN, round 3. **Position:** SKEPTIC-ENGINEER (native).
**Date:** 2026-09-24. **Author:** native subagent B (independent position; no coordination with native voice A).

## 0. Where I stand

Micah's law — NO SYNTHESIZERS, PERIOD — is correct, and the round-1/round-2 history vindicates it: 10 synth forks scored 0/10 on human ears, and the only thing that ever sounded organic was resynthesis of real recordings (the vowel fossils). Where I break with the permissive camp is on what the law's own vocabulary smuggles in. The law as written allows "cut, splice, stretch, grain-resample, layer, crossfade, reverse, granular-of-real-audio, waveform surgery, concatenative real units." That list contains at least three operations — **resampling pitch-shift, crossfading, and additive layering** — that are synthesis with a real recording as the alibi. If we allow them, we have not banned synthesis; we have banned only the oscillator, which was never the load-bearing part of a synthesizer anyway.

This paper proposes two fork designs that survive the strictest defensible reading of the law, states that reading as a razor, attacks the weakest points of typical manipulation proposals, and answers where novelty comes from when you are not allowed to generate a single sample.

A note on honesty before the designs: **under my strict reading, the vowel-fossil approach — our only organic success — does not comply.** It used Q32 time-warp resampling (interpolation: new samples) and overlap-add (weighted sums of two grains: new samples). I am not asking to retract its ear verdict; I am saying it succeeded by doing exactly what the law forbids, and we should stop citing it as proof that manipulation works. Either the strict reading is wrong, or our one success cheated. I take the latter. The two forks below are what "manipulation" looks like when it doesn't cheat.

---

## 1. The razor (strictest defensible reading)

**RAZOR: Every output sample must be a function of exactly one recorded sample — a verbatim copy, or a verbatim copy through fixed-point gain. Any output sample computed from two or more source samples — interpolation, resampling, crossfading, overlap-add, additive layering, convolution/filtering — is a generated sample, i.e. synthesis, regardless of how real the inputs were.**

Two rules, both load-bearing; either alone is launderable:

- **R1 — operation arity.** One input sample per output sample = manipulation (copy, delete, reorder, reverse, repeat, truncate, butt-splice, fixed-point gain). Two or more input samples per output sample = generation = synthesis. This is not a metaphor: a crossfade's output sample is a weighted average that no microphone ever captured; a resampler's output sample is an interpolated value that existed in no recording; a layer-sum is a sum no air pressure ever produced. The operation's *inputs* being real does not make its *outputs* real.
- **R2 — source provenance.** "Real waveform" means an acoustic recording of a real-world event (field anchor, child utterance), never the output of a synthesizer captured to disk. Without R2, the arity rule is launderable: record a DX7 once, then "manipulate" it with pure copies and claim compliance. Without R1, the provenance rule is launderable: take a real child vowel and resample/crossfade/layer it into a synth pad. The law needs both jaws of the trap.

Corollaries I will defend in §4:

- **Pitch-shifting by resampling is synthesis**, full stop. The output samples never existed in any recording. (Consequence: under the strict reading there is honest pitch control and dishonest pitch control; §2.1 shows the honest kind.)
- **Crossfading is synthesis.** A 50/50 crossfade midpoint is a sample that appears in neither input.
- **Additive layering is synthesis.** The sum of two real samples is a sample no recording contains — and it is exactly how every synth pad since the 1970s is built (two detuned saws into a mixer). Banning the oscillator while permitting the mixer bans nothing.
- **Gain is manipulation** (one-input function; the sample's information is preserved up to quantization), and **deletion is manipulation**, but **insertion is not** — not even digital silence. A zero sample is a function of zero source samples. The strict reading's only lawful silence is *recorded* silence (room tone from a real take).
- **Reversal, reordering, repetition, truncation, and butt-splicing are manipulation**: every output position maps to exactly one source position. A butt-splice is a choice of *which* source sample goes *where*, not the computation of a new one.

The strict reading's price is real and I will not hide it: pitch range collapses to what the source actually contains, durations quantize to real unit lengths, and some things simply become impossible — in which case the honest fork **refuses** rather than resamples. Refusal is a feature. A fork that cannot do something without generating samples should say so, loudly, and die on its kill bars instead of quietly becoming a synthesizer.

---

## 2. Fork designs

Both forks are specified to be buildable in pure Zag, zero RNG, deterministic given inputs, with every artifact SHA-256 logged. Both perform **zero arithmetic on sample values** — Fork 1 uses no gain at all (natural levels are consistent); Fork 2 is a pure permutation, bit-identical samples. Fixed-point gain is *permitted* by my razor but neither fork *needs* it, which makes the laundering probe (§2.1.K2, §2.2.K1) airtight: the output multiset of samples must equal a sub-multiset of the source.

### 2.1 FORK 1 — "SUTURE": pitch-controllable vowels by period-butt concatenative surgery

**Concept.** PSOLA minus its two sins. Classic PSOLA gets pitch control by (a) resampling grains to a common pitch and (b) overlap-adding them — both generation under R1. SUTURE keeps only the honest skeleton: cut the source vowel into its real pitch periods, then *select* (never warp, never blend) periods whose natural lengths trace a target F0 contour, joined by butt-splices at phase-matched landmarks. Pitch control becomes a *selection* problem over a real inventory, not a *warping* problem over fake samples. The F0 contour you hear is new; every sample you hear is old.

**Exact source excerpt.** `~/workspace/aud_v11/diag/vowel_real.wav` — SHA-256 `8ba3b42708a8bab2bb8152d392d4425c5c248591d545f3bd1b24070e264e5d1d`, mono 16-bit 44.1 kHz, 88,200 samples (2.00 s). Measured 2026-09-24: F0 stable at 390–455 Hz across all twenty 100 ms frames (autocorrelation; dominant 401–405 Hz), RMS ≈ 12,000 ± 3% per frame, DC = +1.1 LSB (negligible — no DC step needed, and none is taken: verbatim means verbatim), peak 26,213 (−4.7 dBFS headroom). Excerpt used: the **full file** — it is one stable field-anchor vowel, and using all of it maximizes inventory.

**Inventory (analysis only, logged, never searched at render time beyond a linear scan).** Period boundaries are cut at the **rising zero-crossing immediately preceding the main positive peak** of each glottal cycle — a deterministic landmark (peak-pick threshold > 8,000, then walk back to the sign change). Measured inventory: **799 periods**, lengths 97–113 samples (distribution: 108:142, 109:165, 110:119, 111:122, 112:180, 113:62; tails 97–99 and 107: 9 total). Natural F0 coverage: 44100/113 ≈ **390 Hz** to 44100/97 ≈ **455 Hz**. Each inventory entry is stored as (start, length) — the samples are never copied at build time; the renderer indexes the source.

**Exact manipulation chain** (every step defended):

1. **Target contour → target period length.** A 1 s render takes a target F0 contour (e.g. 400→450→410 Hz linear sweep). Per output step, L_target = 44100 / F0_target, rounded to integer. *Defense: arithmetic on the contour, not on samples.*
2. **Greedy phase-corrected selection.** Maintain cumulative output length C and cumulative target length T (T advances by L_target each step). At each step, linear-scan the inventory (fixed order, deterministic) and pick the *admissible* period minimizing |(C + L) − (T + L_target)|; ties broken by lowest inventory index. *Defense: pure selection. The "synthesis" is in the choice rule, which is metadata, not samples.*
3. **Admissibility filter (the suture).** A period may follow the previous one only if the butt-splice satisfies |last_sample(prev) − first_sample(next)| ≤ **4 LSB** AND the endpoint slope signs agree (sign of (last − second_last) vs (second − first)). Because every period is cut at the same landmark class (rising zero-crossing), values near the boundary are near zero with matched slope by construction; the filter rejects the rare bad pairs and the selector takes the next-best. *Defense: a splice chooses which source sample goes where (arity 1). No average is computed; no sample is created. This is "waveform surgery" in the literal sense — suture, not blend.*
4. **Verbatim copy concatenation.** Output[n] = source[inventory_start + k], pure index mapping. **Zero arithmetic on samples: no gain** (inventory RMS is uniform to ±3%), no DC removal (DC = 1.1 LSB), no fades, no dither.
5. **WAV write.** Header rewritten (container metadata, not audio); sample bytes copied.

**Law-compliance argument (strict reading).** Every output sample is a verbatim copy of exactly one recorded sample (R1 satisfied with the strongest possible margin — not even gain is used). The source is an acoustic field recording of a real child vowel (R2). No resampling, no interpolation, no crossfade, no overlap-add, no layering, no filtering, no inserted silence. The only "new" thing is the *order* of periods and hence the F0 contour — arrangement novelty, which §5 argues is the strict reading's legitimate source of novelty. The renderer's refusal behavior (§K1) is the compliance backstop: where the inventory has no coverage, it exits non-zero instead of warping.

**Preregistered kill bars (all measured with the round-2/3 analyzer; hum check = 50/60 Hz + harmonics per standing lesson):**

- **K1 — F0 tracking (and the refusal probe).** Render: 1.0 s, target contour 400→450→410 Hz linear. Bar: per-20 ms-frame autocorrelation F0 within **±3%** of target on **≥95%** of frames; HNR 3.7±3 dB; PERIODICITY ≥ 0.5; HF_ROLLOFF in [−40,−12] dB; hum check clean. **Self-kill experiment:** request a 300 Hz target (outside the 390–455 Hz inventory). The renderer must exit non-zero *refusing*. If it renders anything — by resampling, by stretching periods, by any warp — the fork is dead by its own hand, because rendering would prove a generative path exists in the binary.
- **K2 — splice honesty (the laundering probe).** Bar: max |Δ| over all butt-splices ≤ 4 LSB; slope-sign agreement ≥ 98% of splices; **sample-provenance count = 0**: every output sample must be bit-equal to some source sample (verify by multiset comparison against the source). **Self-kill experiment:** instrument the renderer with a debug counter for "samples written that match no source sample." If the counter is ever nonzero on any render, kill the fork — it means a generative code path fired.
- **K3 — determinism.** Three renders of the sweep, byte-identical SHA-256. (Trivially satisfiable — no RNG, no search — but the bar stays; determinism is law.)
- **K4 — prosody/level gates.** PROSODY variation of the rendered F0 contour within [0.3%, 3%] of the target contour's own variation (the contour is the message; the fork must not flatten or exaggerate it beyond ±10% relative error); peak < −1 dBFS; TRANSIENT [3,20] dB.
- **K5 — inventory coverage honesty.** Log the per-step |L_chosen − L_target| residual; bar: mean residual ≤ 1.5 samples, max ≤ 4 samples. If the inventory cannot track the contour, the bar fails *instead of* the renderer cheating — quantization error is reported, not hidden.

**Honest failure mode.** The F0 range is locked to **390–455 Hz** — the child's actual production, nothing more. No adult male vowels, no 300 Hz targets, no 800 Hz squeals: those renders *refuse*. Fast sweeps quantize audibly to the 17 available period lengths (period inventory is sparse at the tails: only 9 periods outside 108–113). Butt-splices at zero-crossings are clean by construction, but slope-sign mismatches on the rejected pairs mean the selector sometimes takes a length-suboptimal period — trading F0 accuracy for splice cleanliness, visibly in the K5 residual log. There are no consonants, no onsets, no offsets — SUTURE renders sustained vowels only; anything else is a different fork. This is the price of the strict reading, paid openly: **range is what the recording contains, and the fork says no to everything else.**

### 2.2 FORK 2 — "PALINDROME": novel utterances by pure permutation of real child speech

**Concept.** If every output sample must be a verbatim source sample, the largest lawful novelty space is the **permutation group**: reorder and reverse real units. PALINDROME segments real child utterances into syllable-scale units, reverses each unit (time-reversal is a pure sample permutation — autocorrelation, HNR, and spectral envelope magnitude are preserved exactly), reorders units by a deterministic rule, and butt-splices them at precomputed low-energy boundaries. The output is a genuinely novel utterance — a babble no child ever spoke, with a prosody contour no recording contains — and **zero arithmetic is performed on any sample**. The output file is, bit-for-bit at the sample level, a rearrangement of the input. This is the strict reading's existence proof that novelty does not require generation.

**Exact source excerpt.** `~/workspace/v5work/kide.wav` — SHA-256 `5d69f49dd6653c4bbd1fe5c0296b4240ff52224ce47e7062b0a12c05ba40c701`, mono 16-bit 44.1 kHz, 1,323,000 samples (30.0 s), DC = −0.8 LSB, peak 22,288. Segmentation (deterministic, logged): 50 ms frames, voiced/active threshold RMS > 800, gaps < 150 ms merged. Measured 2026-09-24: **11 units, 22.95 s total**, boundaries (s): (0.60,3.55), (4.50,10.80), (11.00,14.35), (14.50,14.55), (14.70,14.95), (15.30,16.05), (16.20,16.30), (16.45,20.20), plus 3 further units to 27 s. (kida.wav measured as near-silence throughout, RMS ≈ 100 — the mic-noise floor — and is *not* used as content; see the recorded-silence note in §4.)

**Exact manipulation chain** (every step defended):

1. **Segment** per the rule above; write the unit table (start, end) to the run log with the source SHA. *Defense: analysis, not synthesis — no samples are touched.*
2. **Boundary refine (no fades, ever).** Each unit edge is snapped to the lowest-RMS 5 ms window within ±100 ms of the energy-gated edge (deterministic scan; tie-break: earliest). If no window under RMS 300 exists in the search range, the unit is **dropped** and the drop is logged. *Defense: choosing where to cut is selection. Dropping instead of fading is the strict reading's signature move — a gap is honest, a fade is generation.*
3. **Reverse every unit.** Output position i of a unit maps to source position (end − i). *Defense: reversal is a permutation — arity 1, every output sample is exactly one input sample. It preserves HNR, periodicity, and the magnitude spectrum; it mirrors the prosody contour, which is precisely what makes the result novel rather than replayed.*
4. **Reorder by descending duration** (deterministic; ties broken by original source order). *Defense: ordering is metadata. The unit sequence (durations: 6.30, 3.75, 3.35, 2.95 s, …) is fully determined by the audio.*
5. **Verbatim concatenation** of the reversed units in the new order; **WAV write**. No gain (natural unit levels are kept — loudness steps between units are honest), no normalization (the law bans output-derived normalization anyway), no dither, no inserted silence between units — units butt directly.

**Law-compliance argument (strict reading).** This fork is the strict reading's clean room: the entire pipeline is a permutation, so R1 holds trivially — the output sample multiset *equals* the input sample multiset (minus dropped units), provable by sort-and-compare. R2 holds: kide.wav is an acoustic recording of real child utterances. There is no resampling, no crossfade, no layering, no gain, no filtering, no silence insertion. The K1 identity-control (below) proves the pipeline adds nothing; the K4 novelty bar proves the result is not replay.

**Preregistered kill bars:**

- **K1 — provenance (the permutation proof).** Bar: 100% of output samples bit-equal to source samples; multiset-equality between output samples and the kept source excerpts (sort-and-compare; mismatch count = 0). **Self-kill experiment (identity control):** render with the identity permutation (units in source order, *not* reversed). The output must be bit-identical to the plain concatenation of the source excerpts. This proves the pipeline contributes zero — no hidden gain, no dither, no DC step. Then the novelty render's SHA must differ from the identity render's *only* by permutation (verified by the same multiset check). If the identity control is not bit-exact, the fork dies: something in the pipeline touches samples.
- **K2 — harmonicity preservation.** Bar: |HNR_render − duration-weighted mean HNR_units| ≤ **1.0 dB**; PERIODICITY ≥ 0.5; frac_static ≥ 0.25. Rationale: reversal and reordering are spectrum-preserving, so any HNR loss would indict the splices (the only joints in the pipeline).
- **K3 — boundary clicks.** Bar: max |Δ| at unit junctions ≤ **16 LSB**; TRANSIENT gate [3,20] dB; peak < −1 dBFS; hum check clean. The low-energy snap (step 2) is what makes this passable without fades; the drop rule is what keeps it honest.
- **K4 — genuine novelty.** Bar: the output unit-ID sequence contains **zero contiguous 3-unit matches** with the source order (edit check on the ID sequence), AND the reversed-then-reordered prosody contour has ≥ 30% of its 100 ms frames differing by > 5% F0 from every source unit's contour (nearest-neighbor contour distance). The fork must prove it made something new, not a reshuffled replay a listener could map back 1:1.
- **K5 — determinism.** Three renders, byte-identical SHA-256.

**Honest failure mode.** PALINDROME's novelty is **combinatorial, not directed**: it produces babble, not target utterances. You cannot ask it for a specific phoneme sequence, a target F0 contour, or an emotional arc — there is no control interface beyond the permutation rule, because every control interface beyond selection is a generative act wearing a trench coat. Reversed prosody reads as uncanny as often as charming; some units will drop at step 2 (audible gaps where low-energy windows don't exist), and the fork logs the drops rather than hiding them. If the listener's verdict is "interesting babble, not speech," that is the *correct* verdict for this fork — it is a proof about the strict reading's novelty space, not a voice.

---

## 3. Attack: the weakest points of typical "manipulation" proposals

This section is the skeptic's core contribution. Each attack is aimed at a proposal pattern that recurs in round-2/round-3 discussions and in the law's own permissive vocabulary. I name the pattern, show the laundering, and state the strict verdict.

### 3.1 "Pitch-shifting by resampling" — the output samples never existed

The proposal: take a real vowel, resample it at 1.2× with interpolation, call the result a pitch-shifted real vowel. The defense usually offered: "the *information* came from a real recording." The attack: **name one output sample and point to the recording it came from.** You cannot — every output sample of a fractional resampler is an interpolated value computed from two or more input samples. It existed in no recording, passed through no microphone, moved no air. Under R1 it is generated, full stop. The honest alternative exists and is well-known: **integer-ratio varispeed** (repeat each sample k times, or keep every k-th sample) — every output sample is verbatim, pitch and speed move together, and that coupling is not a limitation to be engineered away but the *truth* about what pitch means when you refuse to invent samples. Anyone who promises pitch control without time change under the no-synth law is promising interpolation with better PR. SUTURE (§2.1) shows the actual honest route to decoupled pitch: don't warp one period — *select among many real ones*, and refuse when the inventory runs out.

### 3.2 "Crossfading" — the mixer is where the synthesis happens

The proposal: butt-splices click, so blend units with 5–20 ms crossfades; the inputs are real, so the output is "manipulated real audio." The attack is arithmetic: a 50/50 crossfade midpoint sample is 0.5·a + 0.5·b — a value present in *neither* input. With a 10 ms raised-cosine fade at 44.1 kHz, that is **441 consecutive generated samples per splice**, every one of them a two-input function. Calling this "editing" is a category error: editing selects; crossfading *computes*. And the laundering consequence is fatal to the permissive reading: **two detuned recorded saw waves through a crossfading layer engine is a synth pad.** Every subtractive synth since the 1970s is oscillators into a mixer; if the mixer is lawful "manipulation," then banning the oscillator banned nothing — you just record the oscillator once (R2's provenance rule is the only thing stopping this, and the permissive camp rarely states it). The strict verdict: crossfading is synthesis regardless of input provenance. The honest alternative is the suture: phase-matched landmarks, admissibility filters, and the discipline to *drop* unjoinable units instead of blending them (§2.1 step 3, §2.2 step 2).

### 3.3 "Any interpolation is generation" — fractional delays, "grain-resample," time-warp

This is the general form of 3.1, and it kills the most beloved technique in the building: **PSOLA with overlap-add and time-warp resampling** — i.e., the vowel fossils, the only approach that ever sounded organic. The fossils' Q32 phase warp interpolated between real samples (new samples), and the overlap-add summed windowed grains (new samples). I want to be explicit about the blast radius: **under the strict reading, our single organic success was synthesis by another name.** I am not relitigating its ear verdict — listeners heard what they heard — but we may not cite it as evidence that manipulation works, because it wasn't manipulation. It was high-quality synthesis *from* real recordings, which is exactly what Micah's law was written to forbid. (Note the asymmetry the permissive camp never answers: if overlap-add of real grains is "manipulation," then granular synthesis — literally invented as a synthesis technique — becomes lawful the moment its grain source is a recording. The law would then permit every granular synth ever built, provided you sample its input. That is not a reading; it is a repeal.)

### 3.4 "Additive layering" — sums no air ever produced

Layering is in the law's allowed list, so this attack needs care: I am arguing the list is wrong here, not that I am above it. Take two real samples a and b from two real recordings. The layered output a+b is a sample value that **no single recording contains** — it is the digital equivalent of two sounds occurring in the same air, except no air was involved; the sum was computed. Under R1 this is a two-input function: generation. The practical bite: layering *forces* renormalization (two full-scale recordings sum past 0 dBFS), and the law independently bans output-derived normalization — so the permissive layering proposal either clips (dishonest) or normalizes (unlawful). The strict reading's answer: if you want two sounds together, record them together. Neither fork layers anything.

### 3.5 The provenance loophole — "real waveform" must mean a real event

R1 without R2 launders in the other direction: record a synthesizer's output to disk once, then apply only arity-1 operations (copy, reorder, reverse, integer varispeed) and claim every sample is "real" because it came from a WAV file. A WAV file is not a provenance. **"Real waveform" must mean an acoustic recording of a real-world event** — field anchor, child utterance, room tone — with the recording chain logged (source file SHA-256, excerpt offsets in seconds and samples, as this paper does for both forks). Anything else lets the entire synth catalog back in through the sample-library door. I state this as a separate rule because operation-purity and source-purity are independent axes, and the debate keeps collapsing them.

### 3.6 The silence smuggle — even zeros are generated

A small one, because it shows how far the strict reading goes: proposals routinely "pad with silence" or "insert 50 ms of silence between units." A digital zero is a sample value computed from *zero* source samples — it fails R1 more cleanly than a crossfade does. The strict reading permits **deletion** (truncation) but not **insertion** — not even of silence. Lawful silence is *recorded* silence: kida.wav's near-silent stretches (RMS ≈ 100, the actual mic-noise floor of the session, SHA logged above) are real recordings of a real room and may be cut and placed like any other unit. This sounds pedantic until you notice that every "clean" demo with suspiciously perfect gaps got them from generated zeros.

**Summary of the attack.** The permissive reading of the law bans oscillators and permits everything a modern synth actually *is*: resamplers, mixers, crossfaders, granular overlap-adders, interpolation. The strict reading (R1 arity + R2 provenance) draws the line where the samples change: one input per output, and the input must be a recording of something that happened. The two forks in §2 live inside that line. Everything in this section lives outside it, no matter how real its inputs were.

---

## 4. The razor, restated as build rules

For the crew that has to implement under the strict reading, the razor compiles to five build rules:

1. **Name every output sample's source.** The renderer must be able to print, for any output index, the exact (file, sample_offset) it was copied from. If it can't — if the answer is "a weighted combination" or "an interpolated value" — the operation is synthesis. (Both forks satisfy this; the §2.1.K2 and §2.2.K1 laundering probes mechanize it.)
2. **One input, one output.** Gain (fixed-point, per-unit or global) and verbatim copy are the only value operations. No sums, no averages, no filters, no resamplers.
3. **Cut, don't blend.** Joins are butt-splices at precomputed landmarks with admissibility filters; unjoinable units are dropped, never faded.
4. **Recorded silence only.** No inserted zeros; room tone is a unit like any other.
5. **Refuse, don't warp.** When the source inventory lacks the needed pitch, duration, or unit, the fork exits non-zero and logs the refusal. A fork that cannot refuse will eventually synthesize.

---

## 5. Where novelty comes from under the strict reading

The permissive camp's unspoken premise is that novelty requires new samples — that without generation you can only replay. The strict reading rejects the premise: **novelty lives in arrangement and selection, not in samples.** Three sources, all exercised by the forks:

1. **Combinatorial recombination.** Eleven units admit 11! ≈ 4×10⁷ orderings; with per-unit reversal the space doubles per unit. PALINDROME's output is an utterance no child ever spoke, with a prosody contour no recording contains — every sample old, the *sequence* new. The mosaic analogy: nobody claims a mosaic isn't new art because the stones are old. Grinding the stones into pigment and painting with it is a different medium — that medium is synthesis.
2. **Selection under novel constraints.** SUTURE's period inventory is fixed and real, but the F0 contour it traces — 400→450→410 Hz, or any contour within 390–455 Hz — is chosen by the composer, not the child. The contour is the novelty; the samples are the palette. This is also the honest answer to "expressive control": control lives in the *selection rule*, which is metadata and may be as sophisticated as we like (phase-corrected greedy search, contour quantizers, deterministic traversals), because metadata never becomes a sample.
3. **Context and juxtaposition.** A real laugh placed after a real gasp in a new scene is a new event. Concatenative assembly of real one-shots (the fossil log's T1/T2/S1 event pieces were already lawful one-shot *playback* — the sin was only ever in the vowel warping) composes scenes no recording captured, from pieces every recording contains.

What the strict reading *cannot* give you — and this is the honest failure mode of the whole position — is **directed parametric control**: "make *this* vowel, at *this* pitch, with *this* exact prosody, regardless of what was recorded." That request is a synthesizer request. Under the strict reading you get the pitch the child sang, the units the child uttered, arranged by your rules. If Micah's ear demands a 300 Hz vowel and no 300 Hz vowel was ever recorded, the strict reading's answer is: go record one. That is not a limitation of the technique. It is the law, taken seriously.

---

## 6. Closing: what I am actually claiming

1. The no-synth law is right, and the permissive reading of its vocabulary (resample, crossfade, layer) repeals it while pretending to obey it.
2. The strict reading — **one recorded sample per output sample; sources must be acoustic records of real events** — is the strongest defensible line, and it is buildable: SUTURE and PALINDROME are fully specified above, grounded in measured sources (SHAs, offsets, inventory distributions all logged from today's analyzer runs).
3. Our one organic success (vowel fossils) does not survive the strict reading — it used interpolation and overlap-add — and intellectual honesty requires saying so rather than citing it as manipulation evidence.
4. Novelty under the strict reading is real but bounded: arrangement, selection, and context — not parametric control. The forks' kill bars are designed so that the *first* resort to generation kills the fork, by its own instrumentation, before any ear is involved.

The grok side will argue, I expect, that the strict reading strangles expressivity and that resampling/crossfading "preserve" the real recording's character. My reply in advance: character is not the criterion — *samples* are. A photocopy of a painting preserves its character too; a photocopier is still not the painter, and a crossfader is not an editor. If we want TNN's audio to be *real* in the sense the law means, then every sample in the output must have passed through a microphone. Everything else is negotiation, and I am not negotiating.

---

### Appendix: measured source facts (2026-09-24, analyzer-first)

| file | SHA-256 | format | length | measured |
|---|---|---|---|---|
| `aud_v11/diag/vowel_real.wav` | `8ba3b42708a8bab2bb8152d392d4425c5c248591d545f3bd1b24070e264e5d1d` | mono 16/44.1k | 88,200 samp / 2.00 s | F0 390–455 Hz stable (20/20 frames), RMS ≈12,000 ±3%, DC +1.1 LSB, peak 26,213 |
| `v5work/kide.wav` | `5d69f49dd6653c4bbd1fe5c0296b4240ff52224ce47e7062b0a12c05ba40c701` | mono 16/44.1k | 1,323,000 samp / 30.0 s | 11 energy-gated units (RMS>800/50ms, gaps<150ms merged), 22.95 s voiced; DC −0.8 LSB, peak 22,288 |
| `v5work/kida.wav` | `b8ad8e1a1f4f70b01a602fd1848db8aacd9f4857311a19b72757f1af570cfd6e` | mono 16/44.1k | 1,323,000 samp / 30.0 s | near-silence throughout (RMS ≈ 100, mic-noise floor) — candidate recorded-silence source, not content |

Period inventory (vowel_real.wav, rising-zero-crossing-before-main-peak landmarks, peak threshold 8,000): 799 periods; lengths 97–113 samples (108:142, 109:165, 110:119, 111:122, 112:180, 113:62; 9 outliers at 97–99/107); natural F0 coverage 390–455 Hz.

kide.wav unit boundaries in seconds (energy-gated, §2.2): (0.60,3.55), (4.50,10.80), (11.00,14.35), (14.50,14.55), (14.70,14.95), (15.30,16.05), (16.20,16.30), (16.45,20.20), +3 units to 27 s (22.95 s total over 11 units).
