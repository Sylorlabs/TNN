# FINDINGS_v10 — synthesize from understanding (NEW clips for Micah's ears)

**Date:** 2026-09-23
**Prereg:** `PREREG_v10.md` (committed `110da87d` BEFORE any fork render)

Micah's verdict on V9: one scene now (WIN), but choppy like chunks cut out of
a constant recording (LOSS). Directive: TNN must combine its UNDERSTANDING of
audio and SYNTHESIZE, not play/cut one clip. Try something other than gates.
Ask Sol for inspiration. Fork multiple approaches.

## What changed (paradigm)

Chunk assembly is GONE. No recorded atoms, no splicing, no gated on/off
events in any fork. All three renderers generate the playground from an
internal generative model with continuous state and smooth parameter
trajectories. Choppiness is impossible by construction in all three designs,
verified forensically (CHOP-1/2/3) and by source audit.

## Sol consultation

Round 1 (divergent): gpt-5.6-sol proposed articulatory/physical modeling
(glottal source + formant resonators); grok-4.6 proposed parallel parametric
additive channels. swe-1-6-slow and glm-5.3-flash-think-search returned 403
on the connector. Round 2 (convergent critique) attempted twice — provider
returned empty responses both times; fork designs were frozen on Sol round-1
+ analyst judgment. Full transcripts in `v10_sol/`.

## The three forks (all complete, all committed on tnn-native-lab)

| Fork | Paradigm | Commit | 9 bars | CHOP-3 unexpl. | Byte-ident. |
|---|---|---|---|---|---|
| A ARTIC | articulatory/physical: glottal-pulse child voices → formant resonators, syllabic-AM laughter via same vocal model, half-sine damped contact footsteps | `77d3ff3c` | 9/9 PASS, wide margins | 0 / 5 | cmp clean |
| B PARADD | parallel parametric additive: sine-LUT voice channels, bandpass-bursty laughter, damped-sine footsteps, slow-filtered noise air | `770a3181` | 9/9 PASS, thin margins | 1 / 2 (marginal) | cmp clean |
| C SPECSTAT | spectral-statistical resynthesis: one-time filter-bank analysis → band-energy statistics → resynthesis from one continuous noise excitation | `c40124a5` | 9/9 PASS | 0 / 0 | cmp clean |

Clips (all 30 s, 44.1 kHz, 16-bit mono):
- `clips/b_alpha_kids_1e_j_v10_artic.wav` — SHA-256 `57df7aa4015b3cde88615d34aa96ea1ac994845e0613bb96144ac990292ccd41`
- `clips/b_alpha_kids_1e_j_v10_paradd.wav` — SHA-256 `80af8b57e9ba181d1b3c9d79ad3f8e7a7c86a7569254f7a26a40c69c4ba58d73`
- `clips/b_alpha_kids_1e_j_v10_specstat.wav` — SHA-256 `05988a5ab88fcdeb6b6b5fc2c82a0cae7a5010bd9370bb9f031c9194b4c54c2e`

## Independent verification (coordinator, not the crews)

All three clip SHAs reproduce the crews' reported values exactly. The CHOP
instrument was re-run independently against every clip with each fork's
events file: ARTIC 5 spikes/0 unexplained, PARADD 2/1 (the 26.111 s spike
the crew honestly reported), SPECSTAT 0/0. Every forensic claim reproduced.

## Head-to-head verdict

**WINNER: Fork A (ARTIC).** Fewest unexplained CHOP-3 spikes (0, tied with C)
AND the widest nine-bar margins (G-DRIFT 193/800, G-FLUXm 174/350, G-STA
1.064 dB — all deep inside limits). Its physical voice-production model is
also the most likely to read as real children rather than texture.

Runner-up: Fork C (SPECSTAT) — 0 unexplained spikes, but thinner margins and
its own honest caveat (band-energy-shaped noise; may read as lively wash,
not distinct kids). Fork B (PARADD) third — 1 unexplained spike (marginal
kill-bar fail, honestly investigated as a natural event interaction) and the
thinnest margins.

## Honest choppiness assessment

The V9 failure mode is gone by construction AND by measurement: zero hard
discontinuities, zero silent gaps, and every spectral-flux spike in the
winning clip corresponds to a scripted scene event. No chunk boundaries
exist to be heard — there are no chunks. What ears must still judge:
whether ARTIC's physically-modeled voices sound like little children or
like convincing toys. No instrument can claim that. The clip earned the
right to reach Micah's ears; his verdict is the final gate.

## Incidents

- Fork B's crew died in a daemon restart; replacement resumed from its
  workdir (renderer + first render inherited, verified, iterated to v5).
- Forks B and A both committed to `main` instead of `tnn-native-lab`;
  deliverables re-landed on the authorized branch (blob SHAs verified
  byte-identical), `main` rewound to its pre-error state `293602fb`.
  Standing lesson: crews must pass the branch name explicitly; the
  coordinator verifies the branch on every crew commit.
