# SENSES REBUILD — Preregistration 2026-09-21

Micah's directive: rebuild TNN's senses from scratch in pure Zag. The old Drive
senses material is Python, was never wired into TNN memory, and is not reused.
Test BOTH approaches head-to-head. Do not assume the human-style approach wins.

## The two approaches

- **APPROACH A ("LLM-style")**: senses deliver raw values. Image = pixel arrays /
  RGB triples, audio = PCM samples, video = byte frames. Similarity = arithmetic
  distance over numbers. The memory system sees numbers.
- **APPROACH B ("human-style")**: senses deliver qualitative percepts.
  "I see color not values of color." A color percept is an opaque handle into a
  fixed percept vocabulary with similarity structure (this red is nearer that
  orange than to blue) — discriminable, composable, but never a triple of
  numbers to the memory system. Same for audio (pitch/timbre as heard) and video
  (motion-as-seen). Numbers may exist ONLY inside the transducer (the "retina"),
  which is outside the AI's reasoning, like human photoreceptors.

## Kill bars (frozen; amendments need Micah)

- **KB1 viability**: mean accuracy across the 6 tasks < 60% → approach KILLED
  as a viable sense.
- **KB2 head-to-head**: winner = higher mean accuracy. If |Δ| < 2pp AND ops
  ratio < 2× → TIE, no winner declared.
- **KB3 fragility**: winner's accuracy drops > 25pp on noise/adversarial
  fixtures → "fragile winner", no clean victory claim.
- **KB4 memory integration**: false-install rate > 10% on adversarial
  fixtures → FAILS the memory-integration bar regardless of accuracy.
- **KB5 determinism**: 3 runs byte-identical required. Nondeterminism →
  build rejected (fix the build, do not kill the approach).

## Tasks (6) and fixtures

| # | Task | Fixtures | Judgment |
|---|---|---|---|
| 1 | color-discrimination | 60 patch pairs, graded color distances | same / different |
| 2 | color-constancy | 40 surfaces × 3 illuminants | same-surface / different |
| 3 | shape-transform | 90 shapes (circle/triangle/square), rotated/scaled/translated | classify 3-way |
| 4 | pitch-discrimination | 60 tone pairs | same / different + direction |
| 5 | timbre-discrimination | 60 tones, same pitch, different harmonic content | classify 4-way |
| 6 | motion-direction | 60 short clips | 8-way direction + still |

Plus noise variants (deterministic precomputed noise) and adversarial variants
(trick lighting, distractor harmonics, camouflaged motion) of each.

Fixtures: real photographic/audio inputs where obtainable (documented per
fixture); physically-realistic procedural generation (real rasterization, real
color math, harmonic synthesis) where not. Pure synthetic toys are NOT allowed
as the primary fixture for any task.

## Metrics per approach

1. Accuracy per task + mean accuracy (equal task weights).
2. Cost: instrumented op counts (element-visit grain, defined in INTERFACE.md).
3. Robustness: accuracy on noise fixtures, accuracy on adversarial fixtures.
4. Memory integration: false-installation rate under the shared eliminative
   rule (install iff no contradictory installed belief of ≥ confidence;
   else withhold+audit). False install = installed belief contradicts
   ground truth.

## Deliverables

- `docs/lab/senses/rebuild/PREREG.md` (this file)
- `docs/lab/senses/rebuild/INTERFACE.md`
- `docs/lab/senses/rebuild/a_raw/` — Approach A Zag sources + build log
- `docs/lab/senses/rebuild/b_percept/` — Approach B Zag sources + build log
- `docs/lab/senses/rebuild/harness/` — fixtures, runner, scorer, raw results
- `docs/lab/senses/rebuild/VERDICT.md` — per-bar verdicts, kill decisions,
  decomposition tables, evidence pointers
