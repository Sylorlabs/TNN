# AMENDMENT-01 — §I twin fixture provenance (2026-09-20)

Date: 2026-09-20. Amends `PREREG_SENSES_PHASE2_HARNESS.md` (frozen pre-build,
commit `448e1e21d326`).

## What changes

The frozen prereg's §I said the cross-cutting harness "authors its own four
audio and four vision twin pairs" for the save/reload twin-distinction
probes (`se2i-audio-twins`, `se2i-vision-twins`). That was written before the
sibling modality sources landed. The assignment requires twin reload
verification against the modality workers' **committed twin fixtures**
("read their files, don't invent"). This amendment corrects the provenance:
§I now reproduces **exact committed sibling fixtures**, four pairs per
modality, using the workers' own formulas, positions, and record layouts.

No check criterion changes: the probes still assert that each reloaded pair
is byte-distinct, provenance-distinct, and matches the independently
re-derived expected bytes. Only the fixture bytes' provenance changes
(invented → sibling-committed).

## Audio fixtures (from `phase2/audio/se2a_main.zag`, committed)

Base payload: 128 samples, `base(i) = ((i*7919+13)%30001)-15000` (signed
16-bit LE); record = `se_build(...,SE_ENC_PCM16LE,8000,1,payload)`, 336 B.

| §I pair k | Sibling check | Exact twin |
|---|---|---|
| 0 | `se2a-d01-sign-flip` | sample[10] sign-flipped |
| 1 | `se2a-d02-lsb-plus1` | sample[20] +1 |
| 2 | `se2a-d05-swap-adjacent` | samples[30] ↔ samples[31] |
| 3 | `se2a-d07-silence-vs-dither` | base = 128 zeros; twin = ±1 alternating dither |

## Vision fixtures (from `phase2/vision/se2v_main.zag`, committed)

| §I pair k | Sibling check | Exact twin |
|---|---|---|
| 0 | `se2v-twin-px-plus1` | 2×2 base bytes 10,20,…,120; twin byte[0] → 11 |
| 1 | `se2v-twin-px-permute` | 2×2 base; twin swaps pixels 0↔3 (bytes 0..2 ↔ 9..11) |
| 2 | `se2v-twin-row-swap` | 3×3 pattern `b[i]=(i*37+3*11+13)&255`; twin swaps rows 0↔2 (bytes 0..8 ↔ 18..26); 107 B records |
| 3 | `se2v-twin-size-1x1-vs-2x2` | base = 1×1 gray (128,128,128), 83 B record; twin = 2×2 base, 92 B record |

## Record layout (unchanged)

Records 8..15 = audio pairs (336 B each), records 16..23 = vision pairs
(92 B except k=2: 107 B; k=3 base: 83 B). The verify-mode probes re-derive
every expected byte from the formulas above and compare against the
fresh-process reloaded store.

## Why an amendment, not a silent fix

The frozen prereg explicitly blessed invented fixtures. Replacing them with
sibling-committed fixtures changes what the §I evidence means (it now ties
the cross-cutting save/reload guarantee to the exact bytes the modality
batteries qualified), so the change is recorded and committed before the
driver is modified.
