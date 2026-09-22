# GOAL-A PREREG — "Indistinguishable from human imagination"

Frozen 2026-09-22 ~06:20 UTC. Track owner: go-time subagent (grok-first).

## Bar (Micah, verbatim)
"Imagination works so well that you would've never guessed it was an AI that made it — you would've thought it came straight from a human's imagination." Covers images, audio, video. Judge: human eyes/ears (Micah), blind where possible.

## Method: HTRF loop all night
1. **TELL-HUNT** — grok-4.7 red-team agents enumerate what gives artifacts away as AI-made. Each tell → fix hypothesis → implement in Zag → re-render → re-attack.
2. **QUALITY LADDER** — measure first (resolution, symmetry, banding, color stats, temporal coherence, audio bipolarity/clipping/tuning), fix, verify. No vibe-based claims.
3. **BLIND EXPANSION** — grow the blind packet; every batch preregistered with a bar; Micah rates in the morning.
4. **HUMAN-REFERENCE STUDY** — grok-4.7 builds a positive model of "human-like" (imperfection patterns, micro-variation, intentionality cues), not just absence of AI tells.

## Baseline measurements (2026-09-22, 14 field BMPs, 240x240)

| file | unique colors | H-symmetry | edge | saturation | visual note |
|---|---|---|---|---|---|
| f3b1 | 19578 | 0.796 | 5.69 | 0.348 | tree-like blob on grain |
| f3b2 | 27323 | 0.705 | 8.64 | 0.466 | noisy texture |
| f3b3 | 21 | 0.758 | 1.53 | 0.988 | flat poster |
| f3b4 | 5 | 0.976 | 0.87 | 0.890 | near-mirror flat |
| f3b5 | 123 | 0.314 | 0.92 | 0.000 | gray nested squares (generative-tutorial look) |
| f3b6 | 238 | -0.010 | 1.76 | 0.000 | gray, asymmetric |
| f3n11 | 42620 | 0.252 | 11.55 | 0.363 | diagonal noise structure |
| f3n12 | 12847 | 0.236 | 6.63 | 0.413 | texture |
| f3n13 | 2614 | 0.921 | 1.65 | 0.395 | near-mirror |
| f3n14 | 530 | 0.997 | 0.50 | 0.297 | two-tone + soft blob, near-perfect mirror |
| f3n15 | 2 | 1.000 | 0.58 | 0.431 | PERFECT mirror, 2 colors |
| f3n16 | 13 | 0.875 | 1.14 | 0.994 | near-mirror |
| f3n17 | 26 | 0.784 | 6.05 | 0.958 | — |
| f3n18 | 15 | 0.893 | 2.4 | 0.793 | — |

## Kill bars / pass criteria
- **TELL-CLOSE bar**: a tell counts as closed only if the measured metric moves past the bar AND a fresh grok-4.7 red-team (not shown the fix) fails to name it. Bars: gradient-detrended H-symmetry < 0.30 on all shipped images (raw H-symmetry is confounded by vertical gradients — corrected 2026-09-22); no image with < 50 unique colors unless intentional flat-design brief; resolution ≥ 480x480 for hero images.
- **Blind bar**: each blind batch preregisters its own bar (default: Micah labels >50% of TNN pieces "human-made" or "can't tell", 0% "obviously AI" on forced choice).
- **Regression bar**: byte-identical reruns; no RNG; pure Zag generation; Python verification only; every quality claim measured before/after.
- **Audio bar**: carries over from tonight's hi-fi verification (bipolar, DC≈0, no clip, 44.1kHz, tuning exact).

## Non-goals tonight
- Re-rendering legacy 8kHz emitters (Micah's call, byte-identical preserved).
- Opening the sealed mood blind map (~/workspace/tnn-lab/imagination/hidden_files/mood_blind_map.txt) — NEVER.
- Sine-LUT replacement (audio track's pending work; this track measures and red-teams audio, doesn't rebuild the synth).
