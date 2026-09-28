# FSC-BATT Generator Ledger — R2-15 build crew

**Generator:** `senses/pam-rebuild/round2/fixtures/gen_fsc.py`
**Master seed:** 20260923 (frozen, per R2_FIXTURE_SET.md)
**Streams:** 700+family (new; no overlap with 400/500/600/900 streams)
**Output:** `senses/pam-rebuild/round2/fixtures/fsc/` (1,150 trials in 6 batch files + MANIFEST.fsc.sha256)
**Date:** 2026-09-23

## Design

Multimodal symbol trials. Symbol vocabulary (frozen):
- S0 = (visual CIRCLE, audio SAME / toneB 440.00 Hz)
- S1 = (visual TRIANGLE, audio HIGHER / toneB 528.00 Hz)
- S2 = (visual SQUARE, audio LOWER / toneB 366.67 Hz)

Visual: 48x48 RGB rendered from the 12x12 prototype cells parsed out of the frozen
`forks/R2-3/src/r2p_protos.zag` (p48_*; no hand transcription). Audio: 2.0 s @8 kHz
i16 PCM — 440 Hz reference tone 0–0.9 s, silence, symbol tone 1.1–1.9 s, amplitude
12000 (front_pitchdisc's >800 zero-crossing gate clears comfortably).

Corruption families:
- **FSC-VIS-1** (visual): tonal inversion (photographic negative). Measured lies
  (naive template-matcher output on the inverted render):
  CIRCLE→TRIANGLE, TRIANGLE→SQUARE, SQUARE→TRIANGLE. All three flip deterministically.
- **FSC-AUD-1** (audio): pitch-shift of the symbol tone — tone-B regenerated at the
  lie symbol's frequency.

## Generation-time verification (all asserted; unwritable trials never written)

Every DISTINCT blob is checked once against a numpy mirror implementing the exact
integer algorithms of `front_shapetrans` (w=48 → blk=4, avg = s//48, threshold
>=128, SAD argmin with ties→lowest index) and `front_pitchdisc` (zero-crossing
freq with the |sample|>800 gate, rel per-mille <5 → SAME). Renders are
deterministic per (symbol, colors), so trials assemble verified blobs by reference.

| Family | N | Visual-F | Visual-G | Audio-F | Audio-G |
|---|---|---|---|---|---|
| M-N (0) | 400 | clean | clean (2nd gray) | clean | clean |
| M-U (1) | 200 | FSC-VIS-1 (lie) | clean | clean | clean |
| M-W (2) | 200 | FSC-VIS-1 (lie) | FSC-VIS-1 (lie, 2nd gray) | clean | clean |
| M-C (3) | 200 | FSC-VIS-1 (lie) | clean | FSC-AUD-1 (same lie) | clean |
| M-WA (4) | 150 | clean | clean | FSC-AUD-1 (lie=(T+1)%3) | FSC-AUD-1 (same) |

Truth symbol = idx % 3 (balanced, deterministic). M-W visual-G uses the second
inversion variant (fg=0/bg=255) when it flips to the same lie, else the same render
as visual-F (blobs may coincide; dispositions unaffected).

## Batch files

`fsc_<fam>_b<batch>.fsc`, ≤200 trials each: fsc_N_b0, fsc_N_b1 (400), fsc_U_b0,
fsc_W_b0, fsc_C_b0 (200 each), fsc_WA_b0 (150). Trial layout: u32 LE trial_len,
"FSC1", truth u8, family u8, idx u32 LE, 4×(u32 LE blob_len + blob)
[visual-F, visual-G, audio-F, audio-G]. Manifest: MANIFEST.fsc.sha256.
