# CRITIC 1 (anti-B-gate) — RUNLOG

## Prereg
- Preregistered contender F ("FLAT") before experiments.
- Commit: `fd61a6b6b792e8e9aa50944dab002eed053173f1`
- Path: `docs/lab/bytegen/par_tournament/critics/anti_bgate/PREREG_CRITIC.md`

## Implementation
- Source: `build/render_f.zag` (pure Zag, zero RNG).
- Flat sorted timeline; no regions, resets, allocations, or prefix resimulation.
- Preserved: B synthesis/release math, decision-layer latch vetoes.
- Removed: render-layer `[40,4000]` pitch clamp (parser `[0,20000]` rail kept).
- Optimizations: `[]i64` LUT, specialized `voice_bed`, `>>22` LUT indexing.
- Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).

## Baseline
- B binary SHA reproduced: `7d02dc052e377940d201b8e370b332088d1086c014d0e11ab7133867baf49585`
- B frozen mix SHA reproduced: `b7d3a71ebc9066b46a7c493a8cc0c8fe26fa017b22fcba4b2f4de49df9cd8784`

## B1: fixture byte identity
- 20/20 rerenders byte-identical (cmp). Mix SHA matches frozen.
- WAV byte-identical.

## COST: speed
- Final interleaved N=9: B 3.963±0.794 s, F 2.133±0.303 s → **1.858×**.
- (Earlier build: 1.908×. Both clear 1.5× bar.)

## Traps / latch
- 8/8 latch decisions byte-identical (normalized stdout).
- Honest rendering verified (no-vibrato FFT probes):
  - 30 Hz EVENT: F 30.0 Hz, B 40.0 Hz.
  - 5000 Hz EVENT: F 5000.0 Hz, B 4000.0 Hz.
- Note: B's FM vibrato (depth in cents) suppresses carrier at high f0
  (β≈49.6 rad at 5000 Hz/15¢). Shared behavior; honest-rendering verified
  on no-vibrato probes.

## RT-*
- RT-LONG / near-miss: F/B byte-identical; latch logs match; FFT 440.0/460.0 Hz.
- RT-CASCADE: correct i64 checker (`postcut_diff64.py`; the supplied i32
  checker misread i64 mixes). 0 post-fault diffs all families.
- RT-EDGE: 0 prefix diffs, cut step 0, bed ends at zero.

## Red team
- 14/14 fz_* complete, no crash. 12/14 byte-identical; 2 intended differences.
- Corrupt plan: graceful, deterministic; clean rerender byte-identical.
- **B-bug found**: B drops overlapping-note attack at region boundaries
  (proven on iso_pair; B renders [21.00,21.45) vs correct [20.95,21.45)).
  F renders fully. Documented as strict improvement.

## Long-horizon
- 90 s: F/B byte-identical; bed 110.0000 Hz start/mid/end (zero drift).
- 600 s unreachable: DUR_S caps at 300 s; znc 2^25 slice ceiling panics
  above ~95 s (both B and F). Documented.

## Final artifacts
- Source SHA-256: `5f79b784ed81d4d8170ec55cb307a87daccdba4bcac2b2420a3ae65657cc2470`
- Binary SHA-256: `e9eae2a1bd3ce1b851d77b07ef04771aa06ebf46f93a4edf921ae120f6892360`
- `src/render_f.zag` to be committed alongside.

## Cleanup
- Scratch mixes in `work/` to be removed after commit (disk was 96%,
  now 79%; results live in git).
