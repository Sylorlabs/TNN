# B-γ — the monster fork (event assembler)

Position (b), study-then-invent, pushed at imagination beyond experience.
Every audible moment is a captured grain from a real recording; the system
invents only the arrangement. No oscillators, no resonators, no filtered
noise, no chirps, no booms, no pitch shifting, no ring modulation — under
any name.

## Quick start

```bash
cd imagination_discovery/aud/b_gamma
# 1. study (Python preprocessor; downloads 8 CC/PD recordings, uses 4 local
#    inspiration recordings; writes study_out/gamma.grpk — LOCAL ONLY)
python3 study.py
# 2. build the renderer (pure Zag)
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 \
  gamma.zag --no-zagd --no-analyze --no-foreground-cache -o gamma_bin
# 3. render + verify (3x determinism, A-NATIVE, no-copy audit)
python3 render_verify.py
# usage: ./gamma_bin <kids|planet|ocean|monster> <pack> <out.wav>
./gamma_bin monster study_out/gamma.grpk /tmp/raxith.wav
```

## Files

| File | What it is |
|---|---|
| `gamma.zag` | the renderer: pack loader, Q24 mix arena, place/reverse/morph, 4 score grammars, WAV writer. Pure Zag, zero RNG. |
| `study.py` | the study: segmentation, feature classification, per-subclass k-means voices, pack writer (v2). Deterministic. |
| `controls/kids_synth.zag` | Test-1 control (i): the banned toolkit's honest best attempt at the kids brief. NOT a deliverable path. |
| `audit.py` | no-copy audit: max 2 s-window xcorr vs any study source; gate 0.80. |
| `render_verify.py` | render 4 pieces × 3 runs, check byte-identical SHAs, A-NATIVE, audit. |
| `MONSTER.md` | the Raxith: committed creature description (written BEFORE rendering). |
| `STUDY_LOG.md` | sources, licenses, segmentation thresholds, vocabulary learned, declared gaps. |
| `TRANSFORMATION_LOG.md` | closed mechanism list (T1–T8), exclusion list, anti-rename defenses. |
| `MECHANISM.md` | architecture, determinism argument, honest limits. |
| `TEST_RESULTS.md` | K0–K3b results, SHAs, A-NATIVE table, grain inventory. |
| `blind/` | Test-1 blind set (judge_A/B/C.wav), sealed order, judging brief. |
| `render/` | the four deliverables (`b_gamma_{kids,planet,ocean,monster}.wav`). |

## Deliverables

| WAV | Length | SHA-256 (r0) |
|---|---|---|
| `render/b_gamma_kids.wav` | 30 s | `655978ec…68464b95` |
| `render/b_gamma_planet.wav` | 21 s | `71c5c7b0…768b5c50feb` |
| `render/b_gamma_ocean.wav` | 30 s | `e8db1a18…5364278bb` |
| `render/b_gamma_monster.wav` | 30 s | `6b0c9c57…2d844a9c` |

All: 44.1 kHz mono 16-bit, A-NATIVE PASS, 3/3 byte-identical reruns.

## What is NOT committed

`study_src/` (downloaded recordings), `study_out/` (pack, CSVs, logs),
`gamma_bin`, `controls/*_bin`, `.zagd` caches. Study materials are
local-only by the task's license hygiene rule.

## The claim (and its kill bars)

B-γ claims position (b) can stretch a studied vocabulary of real event
grains into unheard sounds — including a deliberately invented monster —
without the synth paradigm. One "sounds like a synth" from Micah kills a
piece's claim; the honest smaller claim is always ready. See
TEST_RESULTS.md for what's actually been judged (nothing yet — ears pending).
