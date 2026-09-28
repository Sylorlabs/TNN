# TNN Byte-Generation Tournament: Deep Review

## Q1. Necessity Gating Design

**Core question**: Does gating preserve the servo's continuous wins (N=16 self-limiting, corruption response) while eliminating unnecessary flux?

### Analysis of the continuous servo's mechanisms

The three proven wins operate on different timescales:

1. **RT-LONG octave correction** (+0.1¢ vs +1200.1¢): discrete error, correctable in ~10 blocks after detection
2. **N=16 chord self-limiting**: *continuous* regulation — the servo isn't correcting an error; it's providing real-time headroom management that the plan cannot encode (the plan specifies N=16 equal-amplitude tones; the servo dynamically attenuates to prevent clipping)
3. **Sustained corruption vetoing**: 1295/1295 blocks vetoed — this is continuous *suppression*, not correction

**The gating problem**: N=16 self-limiting requires the servo *before* clipping occurs. A threshold-triggered gate arrives too late (you detect clipping → engage servo, but the damage is done). The servo's value here is *preventive*, not corrective.

### Proposed necessity criterion (two-tier)

**Tier 1 (always-on preventive monitoring, zero cost when inactive)**:
```
ENGAGE if any:
  - Plan requests N ≥ 4 simultaneous voices AND sum(planned_RMS) > 0.7 FS
    → Pre-engage headroom servo before rendering begins
  
  - Measured block_RMS deviates from plan_target by >15% for 3+ consecutive blocks
    → Pitch/gain correction servo
    
  - Pitch inference (any method) disagrees with plan f0 by >50¢ sustained over 5 blocks
    → Pitch correction servo
    
  - Corruption detector fires (existing rail-pin or model-error >50%)
    → Suppression servo
```

**Tier 2 (hysteresis)**:
Once engaged, servo remains active for 20 blocks minimum OR until all trigger conditions clear + 10-block grace period, whichever is longer. Prevents flapping on threshold boundaries.

**Justification**:
- **N ≥ 4 + RMS >0.7**: Catches N=16 case *before* rendering. The plan is inspectable; we know summed amplitude will clip. Cost: ~5 ms plan analysis, one-time per region.
- **15% / 3-block**: Current 10% deadband is design intent. 15% is the "something is actually wrong" threshold (octave error produces ~50% RMS deviation within 2 blocks in the RT-LONG test). 3-block persistence filters measurement noise.
- **50¢ / 5-block**: Half-octave is the "clearly not vibrato" threshold. 5 blocks = 50–100 ms depending on block size, long enough to distinguish sustained error from transient.
- **Corruption detector**: Existing logic, proven. No change.

**What this loses**: 
- Continuous micro-adjustments for model errors in the 10–15% range. Evidence needed: does PAR's 10% deadband already handle these silently? If C's continuous servo is correcting 11–14% errors that PAR ignores, and those corrections are inaudible, then the gating is correct and the continuous behavior was wasteful.

**Measurement needed**: Run PAR and continuous-C on the same battery. For every block where C's servo is active but error <15%, measure: (a) what correction was applied, (b) difference in output spectrogram. If (b) is below JND (perceptual threshold), the correction was unnecessary.

---

## Q2. Choppiness Standard

**Micah's concern**: "choppiness when unnecessary" — implies perceptible discontinuity artifacts that serve no functional purpose.

### Proposed operational definition

**Choppiness** = presence of flux spikes that:
1. Exceed the 95th percentile of flux magnitude in a plan-matched PAR baseline (i.e., "louder than typical PAR transients"), AND
2. Are NOT coincident (±5 ms) with plan-specified events (note attacks, releases, explicit glides), AND  
3. Cluster (≥3 within a 50 ms window) OR repeat periodically (same Δf, Δt pattern ≥3 times in one region)

**Rationale**:
- Condition 1: If C's flux is within PAR's envelope, it's "as choppy as the plan asked for" — not a regression.
- Condition 2: Servo-induced transients at planned event times are indistinguishable from rendering artifacts (which PAR also has). The problem is *unplanned* transients.
- Condition 3: Isolated spikes are common in digital audio (quantization, phase discontinuities at block boundaries). Perceptible choppiness requires *pattern* — either clustered (a "rattle") or periodic (a rhythmic artifact).

### Applying to the 41-vs-29 question

From the evidence: 41 C spikes vs 29 PAR spikes, all within the "complete-event-list explanation window" (meaning: every spike coincides with a planned event). BUT: 6 of the 12 *extra* C spikes sit within 12 ms of servo-adapt block boundaries, and the rest are "servo-amplified vibrato extrema."

**My judgment**:
- The 6 boundary-adjacent spikes are **choppiness** under the definition. They are servo artifacts (boundary effects), not planned events. However, if their magnitude is <95th percentile of PAR's transients, they are *inaudible* choppiness.
- The servo-amplified vibrato extrema are **not choppiness** IF: (a) the vibrato is in the plan, and (b) the servo is amplifying existing transients rather than creating new ones. This is arguable: if PAR renders vibrato with 5 flux spikes and C renders it with 8, but all 8 are at vibrato zero-crossings, is that "amplification" or "new artifacts"?

**What this misses**:
- **Phase discontinuities**: Flux measures frequency changes, not phase jumps. A servo that maintains perfect f0 but introduces π phase jumps at block boundaries would pass this test but sound terrible.
- **Perceptual masking**: A spike during a loud chord is inaudible; the same spike during a sustained tone is obvious. This metric doesn't weight by context.
- **Stereo imaging**: If the servo creates L/R channel phase differences, it could produce spatial "wobble" with zero mono flux.

**Minimum additional test**: Measure inter-block phase continuity. For any block boundary, compute: `|phase_end(block_n) - phase_start(block_n+1)| mod 2π`. Threshold: >0.2 radians unexplained by f0 change is a discontinuity.

---

## Q3. Red-Team Adversarial Plans

### Adversarial Plan 1: Sub-Threshold Drift
**Design**: 1000-block region, f0 starts at 440 Hz, drifts linearly to 430 Hz over 950 blocks (−10 Hz / 950 blocks = −0.0105 Hz/block), then snaps back to 440 Hz in block 951.

**Per-block deviation**: −0.0105 Hz = −0.04¢/block. Over 5 blocks: −0.2¢, well under the 50¢ threshold.

**Expected behavior**:
- **Stock-C (continuous)**: Tracks the drift immediately (servo sees plan target, renders it). Snap at block 951 produces one correction spike.
- **Gated-C**: Servo stays off for 950 blocks (no 50¢ / 5-block trigger). At block 951, sudden −10 Hz error trips threshold; servo engages and corrects over ~10 blocks with visible transient.
- **Servo-off (PAR)**: Renders the plan exactly. Snap at 951 is in the plan; no artifact.

**Verdict**: Gated-C produces a **10-block correction transient** that servo-off avoids. This is choppiness-when-unnecessary IF the snap is a plan error (user intended smooth drift, plan encoder quantized it). If the snap is *intentional* (percussive effect), then gated-C's correction is wrong.

**Kill condition**: If plan metadata includes "smooth" vs "discrete" event tags, gated-C should read them. If no tags exist, the 10-block transient is a design flaw.

---

### Adversarial Plan 2: Gate Flapping
**Design**: 200-block region, f0 oscillates: 440 Hz (10 blocks) → 465 Hz (10 blocks) → 440 Hz (10 blocks)... (20 cycles).

**Deviation**: ±25 Hz = ±98¢, but only for 10 blocks at a time. The 5-block persistence requirement means: blocks 1–5 see 440 Hz (no trigger), blocks 6–10 see 465 Hz (no trigger yet — only 5 blocks observed), blocks 11–15 see 440 Hz again (trigger never fires).

**Gated-C behavior**: Servo never engages (no 5-block persistence). Renders the plan exactly like PAR.

**Modified attack** (to force flapping): f0 = 440 Hz (6 blocks) → 465 Hz (6 blocks) → repeat.

Now: blocks 1–6 = 440, blocks 7–12 = 465 (triggers at block 11), servo engages. Blocks 13–18 = 440 (error clears at block 17), but hysteresis keeps servo on until block 21 minimum. Blocks 19–24 = 465 again... servo re-engages.

**With 20-block minimum active duration**: Servo engages at block 11, stays on until block 31 (20 blocks), even though error cleared at block 17. If the oscillation continues, servo stays continuously active — **effectively reverting to stock-C** for this pattern.

**Verdict**: Hysteresis prevents flapping but also defeats gating for periodic errors. This is **correct behavior** (the plan is pathological; continuous servo is the right response).

---

### Adversarial Plan 3: Corruption Bomb
**Design**: 1000-block region, clean plan for 500 blocks, then inject model error: force block 501's plan_target to 0.95 FS (near clipping) while actual acoustic model predicts 0.4 FS. This is a 138% error, trips the 15% / 3-block threshold immediately.

**But**: Inject errors in a sawtooth pattern: block 501 = +138%, block 502 = +5%, block 503 = +138%, block 504 = +5%...

**Stock-C**: Continuous servo vetoes blocks 501, 503, 505... (every high-error block). Renders blocks 502, 504, 506... (low-error blocks). Output has 2-block periodic "holes."

**Gated-C**: Threshold trips at block 501 (138% error). Servo engages, stays on for 20 blocks minimum (hysteresis). During those 20 blocks, vetoes all high-error blocks (501, 503, 505..., 519). Blocks 521+ (post-hysteresis): servo disengages if error <15%. Next high-error block (521 if pattern continues) re-triggers.

**Servo-off (PAR)**: Renders block 501 at 0.95 FS → **clipping**. Renders block 502 at plan target (0.4 FS, clean). Clipping artifacts propagate via codec state or auditory masking effects.

**Verdict**: Both servos survive; servo-off fails (clipping). Gated-C produces the same veto pattern as stock-C here because hysteresis keeps it engaged. **No difference** between stock and gated for this attack.

**Insight**: The gating design is conservatively safe. It's hard to construct a plan where gated-C fails but stock-C succeeds, because the thresholds are set to "obvious error." The risk is the opposite: gated-C *passes* when stock-C passes, but gated-C *also* passes when stock-C was doing unnecessary work.

---

## Q4. Contender Map Attack

Current map:
- Audio → B (plan-seeded region state)
- Image → PAR
- Generative video → PAR  
- Predictive video → state demanded
- Dialogue → state demanded

### Most likely wrong: Generative video → PAR

**Hypothesis**: Generative video has temporal coherence requirements (frame-to-frame motion smoothness, object persistence) that PAR cannot satisfy without inter-frame state. If PAR is winning here, it's because:

1. The battery's 9 quality bars don't include a temporal coherence metric specific to video, OR
2. The test videos are short enough (<30 frames?) that intra-region coherence suffices, OR
3. PAR's plan is so detailed (per-pixel, per-frame targets) that it encodes all necessary coherence, making carried state redundant.

**Counter-evidence needed**: B (plan-seeded region state) should beat PAR on generative video if inter-frame state improves coherence. But the map says PAR won — meaning either:
- B wasn't tested on generative video (oversight), OR  
- B was tested and tied/lost (in which case the plan is encoding everything, and PAR is correct).

**Falsification experiment**:

**Test**: "TEMPO-1: Object Tracking Coherence"
- **Plan**: Generate a 300-frame (10-second) video of a red ball moving left-to-right across the frame at constant velocity. Plan specifies: ball position per frame (linear interpolation), ball radius = 50 pixels, background = static white.
- **Metric**: Object centroid jitter. For each frame, detect red region centroid. Measure deviation from the linear trajectory: `jitter = mean(|actual_x - expected_x|)` over all frames.
- **Bar**: PAR and B must achieve jitter <2 pixels (sub-pixel due to rendering interpolation). If B achieves <1 pixel and PAR achieves >2, **B overthrows PAR on generative video**.
- **Kill condition**: If PAR renders frames 50–51 with a 10-pixel discontinuity (ball "jumps"), PAR has failed temporal coherence despite the plan being correct.

**Why this works**: Constant-velocity motion is the simplest temporal coherence test. If PAR's per-frame rendering (even with a perfect plan) cannot maintain sub-2-pixel trajectory smoothness, it proves inter-frame state is necessary. If PAR *does* maintain smoothness, it proves the plan is sufficient (and the map is correct).

---

### Is there a path where gated-C beats B?

**Candidate**: Audio, specifically the RT-LONG overthrowing criterion.

**B's win**: RT-LONG 440 Hz at 0¢ (octave latch at region boundary reseeds from plan). Coherence 1.0, no cascade.

**C's performance**: RT-LONG 440.02 Hz at +0.1¢ (servo correction within region). Coherence ~1.0, no cascade, but 12 extra flux spikes.

**Gated-C's potential**: If the 12 extra flux spikes are eliminated by gating (servo only engages when the octave error is detected, then disengages after correction), gated-C could match B's 0¢ performance *and* beat B on smoothness (no region-boundary reseed discontinuity).

**B's vulnerability**: Plan-seeded region state means B has a **discontinuity at every region boundary** (state resets to plan-derived value). If the plan's region boundaries are audible (e.g., every 5 seconds in a 60-second piece), B has 12 resets. C (even gated) has zero resets — it's continuous within a region, servo or not.

**Experiment**: "REGION-1: Boundary Discontinuity"
- **Plan**: 60-second sustained 440 Hz tone, region boundaries every 5 seconds (12 regions). Introduce a slow drift: f0 = 440 Hz in region 1, 441 Hz in region 2, ..., 451 Hz in region 12.
- **Metric**: Phase continuity at region boundaries. Measure `|phase_end(region_n) - phase_start(region_n+1)|` for all 11 boundaries.
- **Bar**: Mean phase discontinuity <0.1 radians.
- **Expected**: B reseeds from the plan at each boundary → 11 phase jumps (each ~2π * 1 Hz / 44100 Hz * boundary_duration, but plan-derived, so potentially large). Gated-C has continuous phase (servo off, rendering plan targets directly, no reseed needed).

**Verdict**: **Gated-C could beat B on audio** if boundary discontinuities are perceptible and the battery adds a phase-continuity test.

---

## Q5. Blind Spots

### Blind Spot 1: Latency and Real-Time Performance Under Load

**What's missing**: All tests measure *quality* (accuracy, coherence, artifacts) but not *latency* or *throughput* under constrained resources. The RT-* tests measure pitch accuracy ("honest-cents"), not wall-clock render time or CPU utilization.

**Why it matters**: 
- PAR is embarrassingly parallel (every sample is independent). If the system has 8 cores, PAR renders 8× faster than serial methods.
- B (plan-seeded state) is parallelizable within regions but requires sequential region boundaries.
- C (servo) has a feedback loop — it cannot parallelize *within* a block (block N+1 depends on block N's correction). If blocks are small (1024 samples = 23 ms), servo serialization could be a 10× throughput penalty on multi-core systems.

**Missing test 1**: "LATENCY-1: Real-Time Render Throughput"

**Design**:
- **Task**: Render 60 seconds of audio (RT-LONG test case) on a 4-core system with CPU governor set to "performance."
- **Metric**: Wall-clock time to render (seconds).
- **Bar**: 
  - All contenders must render in <60 seconds (1× real-time minimum for "real-time" claims).
  - Contenders that render in <15 seconds (4× real-time, exploiting all cores) are marked "RT-capable."
  - Contenders that render in >60 seconds are marked "offline-only."
- **Expected results**:
  - PAR: ~7.5 seconds (8× speedup on 4 cores with hyperthreading, assuming negligible overhead).
  - B: ~15–20 seconds (parallelizes within regions; 12 regions in RT-LONG = 12 sequential boundaries).
  - Stock-C: ~45–55 seconds (feedback loop serializes most rendering; only plan analysis parallelizes).
  - Gated-C: ~10–15 seconds if servo engagement is <10% of blocks (mostly PAR-like), ~45 seconds if servo is always-on.
- **Kill condition**: If gated-C renders in >60 seconds on the RT-LONG test (which stock-C already handles), the gating has failed to reduce computational cost, and the "only when necessary" claim is false.

**What this catches**: Gated-C could win all quality bars but be unusable in production due to latency. The servo's cost isn't just "12 extra flux spikes" — it's "10× slower rendering" if the gate doesn't work.

---

### Blind Spot 2: Cross-Path Contamination and State Bleed

**What's missing**: Each path (audio/image/video/dialogue) is tested *independently*. But production systems often mix paths — e.g., a video with audio, a dialogue agent that plays sound effects, an image gallery with background music. If contenders use different state management strategies per path (audio→B, image→PAR), how do they handle *shared state* at the boundary between paths?

**Why it matters**:
- B (plan-seeded region state) on audio + PAR (stateless) on image: What happens if the audio plan depends on image content (e.g., "play a sound when the image transitions")? Does the audio renderer need to read image output (creating a cross-path dependency), or is the plan rich enough to encode the sync?
- Dialogue→state + audio→B: Dialogue state is carried across turns (conversation history). Audio state is region-reset. If the dialogue says "play this soundbite," does the audio renderer start fresh (losing dialogue context), or does it inherit state (violating B's design)?

**Missing test 2**: "SYNC-1: Cross-Path State Boundary"

**Design**:
- **Task**: Generate a 30-second video with synchronized audio. Video: a bouncing ball (generative video path). Audio: a "boing" sound every time the ball hits the ground (audio path). The plan specifies: ball position per frame (60 fps = 1800 frames) and "boing" events at frames 30, 90, 150, ... (every 60 frames = 1 second intervals).
- **Metric**: Audio-visual sync accuracy. Measure time difference between:
  - Ball's Y-position minimum (ground contact, per frame) 
  - "Boing" sound onset (via onset detector, ±5 ms tolerance).
- **Bar**: All "boing" events must occur within ±50 ms of the corresponding ball-ground contact. Mean sync error <10 ms.
- **Cross-path scenarios**:
  - **PAR video + PAR audio**: Both stateless. Sync is plan-derived. Expected: perfect sync if plan is correct.
  - **PAR video + B audio**: Audio has region state (reset every 5 seconds?). If a boing event occurs 10 ms after a region boundary, does B's reseed cause a delay? Expected: potential 1-block (~23 ms) desync at boundaries.
  - **Servo video + B audio**: If video servo corrects ball trajectory mid-flight (to fix a plan error), but audio plan still has the boing at the original frame, they desync. Expected: worst case (servo fights the plan).
- **Kill condition**: If PAR video + B audio produces >50 ms desync at any boing event, the per-path contender map is incompatible — you cannot mix PAR and B in production without cross-path coordination.

**What this catches**: The tournament verdict could be "audio→B, video→PAR" but the *combination* is incoherent. A production system must use a single state-management strategy across all paths, or implement explicit cross-path sync (adding complexity cost not measured in the battery).

---

## Summary of Judgments (Adversarial Stance)

1. **Gating design (Q1)**: The two-tier criterion is defensible but **not optimal**. The N≥4 pre-engagement is smart, but the 15%/3-block threshold is arbitrary (why 15? why 3? no perceptual justification given). The real risk: gating converts continuous regulation (N=16 self-limiting) into threshold-triggered response, which *changes the sonic character* even if it prevents clipping. The servo is no longer transparent.

2. **Choppiness standard (Q2)**: The 95th-percentile + clustering definition is testable but **misses phase discontinuities**, the most common cause of perceptible digital choppiness. The 41-vs-29 question cannot be answered without magnitude data. If the 12 extra spikes are all below PAR's 95th percentile, there is no regression. If any exceed it, the regression exists but may be inaudible (needs listening tests, which Micah will do anyway).

3. **Red-team (Q3)**: The gating design is **conservatively safe but not minimal**. It's hard to break because the thresholds are set to "obvious error." But this means it also engages on errors that PAR would handle silently (e.g., 16% deviation for 3 blocks — is that audible?). The adversarial plans show: gating mostly replicates stock-C's behavior (good for correctness, bad for cost reduction).

4. **Contender map (Q4)**: **Generative video → PAR is the weakest cell**. Either the test videos are too short for temporal coherence to matter, or the battery is missing a frame-to-frame jitter test. The TEMPO-1 experiment (object tracking coherence) would expose this. **Gated-C could beat B on audio** if boundary discontinuities are measured (REGION-1 test).

5. **Blind spots (Q5)**: **Latency (LATENCY-1) is the biggest gap**. The tournament measures quality, not production viability. If gated-C's engagement is >10% of blocks, it will be too slow for real-time use, even if it wins all quality bars. **Cross-path sync (SYNC-1) is the second-biggest gap**. The per-path map assumes paths are independent, but production systems mix them. If PAR + B is incoherent at path boundaries, the entire map collapses.

---

**Final adversarial take**: The gated servo is a good idea but the **execution is underspecified**. The necessity criterion needs perceptual grounding (why these thresholds?), and the latency cost must be measured before declaring victory. The choppiness standard is testable but incomplete (add phase continuity). The contender map has one likely-wrong cell (generative video) and two missing tests (latency, cross-path sync) that could overturn multiple verdicts. **The tournament is rigorous on what it measures, but it's not measuring production-readiness**.
