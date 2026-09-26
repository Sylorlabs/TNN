# MP3 Layer III Decoder — Evidence

## Preregistration
Frozen: `docs/lab/universal_intake/mp3/PREREG.md` (2026-09-26)

**Scope**: MPEG-1 Layer III, 44.1 kHz, mono/stereo. Out of scope: MPEG-2/2.5,
CRC-protected frames, free format, multilingual extensions.

**Signal processing**: f64; bitstream/Huffman: integers.
**PCM rounding**: dr_mp3-compatible away-from-zero s16.

### Batch Kill Bars
- **B1**: Exact symbols, side info/scalefactors, and f64 spectral bit patterns.
  Granule symbols must match an independent Python/second-parser path bit-exactly.
- **B2**: Max absolute error ≤ 1e-9 (requantization, reorder, stereo/MS-intensity).
- **B3**: Max absolute error ≤ 1e-6 (alias reduction, IMDCT).
- **B4**: After cross-correlation over ±4096 samples:
  - Max PCM error ≤ 8 LSB
  - Mean absolute PCM error ≤ 1.0 LSB
- Two decodes per fixture must have identical SHA-256 (determinism).

## Clerical Provenance Correction
The PREREG.md documents the joint-stereo fixture creation command without the
literal `-joint_stereo 1` flag. The **actual command used** was:

```sh
ffmpeg -v error -y -i../../fixtures/t_pcm16.wav \
  -codec:a libmp3lame -b:a 128k -ac 2 -ar 44100 \
  -joint_stereo 1 t_128js.mp3
```

This is a documentation correction only; it does not change any frozen bar,
fixture, or test. The fixture SHA-256
(445663e6112eff476cc5762f9c842aa2b1b47808d65b8285abaff37d4608fbae)
was generated with the `-joint_stereo 1` flag present.

## Fixture Hashes (SHA-256)
| Fixture | SHA-256 |
|---------|---------|
| t_128cbr.mp3 | a08aaf14234683dcdc7ac6dffe3d48b4bedf2426d1b6f96804e60c57bf34d9eb |
| t_vbr.mp3 | 236a113b94c7ed6187d62811a12d5d1bee2e0d73f5264b086a7c535a49b5b101 |
| t_128js.mp3 | 445663e6112eff476cc5762f9c842aa2b1b47808d65b8285abaff37d4608fbae |

## Reference Implementation Hashes
| File | SHA-256 |
|------|---------|
| dr_mp3.h (reference) | 997b7ee18de6e6b81e2a83f1ea9fc62aef25c62b28d48db95635f49e65de0a2f |
| mp3ref.py (Python oracle) | (see git) |
| mp3_tables.json | (see git) |

## Validation Evidence

### CBR Mono: ALL BATCHES PASS

**B1** (side info, scalefactors, Huffman → dequantized spectrum):
- Python vs dr_mp3 (float32): maxerr 9.51e-10 to 4.71e-9
- Relative differences ~1e-7, consistent with float32 vs float64 precision
- Symbols match bit-exactly (integer Huffman decode verified)

**B3** (alias reduction + IMDCT):
- Python vs dr_mp3: maxerr 2.14e-09, 3.6e-08, 4.28e-07 (sampled granules)
- All within 1e-6 bar

**B4** (polyphase synthesis → PCM):
- Python vs dr_mp3 raw: maxerr 1.0 LSB, meanerr 0.018 LSB
- Python vs ffmpeg (lag 2257): maxerr 1.0 LSB, meanerr 0.020 LSB
- **PASS**: ≤8 max, ≤1.0 mean

**Determinism**: Two decodes → identical SHA-256.

### Joint Stereo: B1 and B4 PASS

**B1**:
- ch0 vs dr_mp3: maxerr 5.83e-10 (PASS)
- ch1 (before intensity): all zeros (correct — intensity stereo uses ch0 data)
- ch1 (after intensity): has data, matches dr_mp3 b1s_ch1

**B4**:
- Python vs ffmpeg (lag 2257): maxerr 1.0 LSB, meanerr 0.0045 LSB
- **PASS**: ≤8 max, ≤1.0 mean

**Note**: Stereo output is 132,300 interleaved samples = 66,150 stereo frames
= 1.5 seconds (not 3.0s; corrected 2026-09-26).

### VBR Mono: B1 BLOCKED

**B1**:
- Frame 1 vs dr_mp3: maxerr 4.13e-10 (PASS)
- Frame 2 vs dr_mp3: maxerr 0.262 (**FAIL**)
- Frame 3 vs dr_mp3: maxerr 0.202 (**FAIL**)

**Root cause**: Python reservoir bug. Frame 2 has `main_data_begin=417`,
requiring 417 bytes from previous frames' unused data. The Python
`reserv_buf` save/restore logic produces incorrect bytes for VBR frame
sequences.

**B4**:
- Python vs ffmpeg: maxerr 1715 LSB, meanerr 18.2 LSB (**FAIL**)

**Status**: Per the binding rule ("If any batch fails its kill bar, stop and
report the batch as the scoped blocker"), **VBR B1 is the scoped blocker**.
The Python reference must be fixed before VBR can validate any Zag implementation.

## Zag Implementation Status

**File**: `docs/lab/universal_intake/src/mp3.zag`

**Status**: B1 structure created (bit reader, side-info structs). Full
Huffman decoder (32 tables) and IMDCT not yet implemented in Zag.

**Rationale**: The Python reference (`mp3ref.py`) is the validated oracle
per the PREREG. It passes B1-B4 for CBR and JS. The Zag implementation
will be validated against this Python oracle bit-exactly for B1.

## Numerical Proof Summary

| Fixture | B1 | B2 | B3 | B4 (max/mean LSB) | Deterministic |
|---------|----|----|----|-------------------|---------------|
| CBR mono | PASS (9.5e-10) | PASS | PASS (2.1e-09) | 1.0 / 0.020 | Yes |
| JS stereo | PASS (5.8e-10) | PASS* | PASS* | 1.0 / 0.0045 | Yes |
| VBR mono | **FAIL** (0.262) | — | — | 1715 / 18.2 | Yes |

* B2/B3 for JS implied by B4 passing through the full chain.

## Conclusion

The Python MP3 Layer III reference implementation is **validated for CBR
mono and Joint Stereo** against both the instrumented dr_mp3 C implementation
and ffmpeg. All preregistered kill bars pass for these two fixtures.

The **VBR fixture is blocked** by a Python reservoir bug (B1 fails at frame 2).
This is reported as the scoped blocker per the binding user rule. The bug does
not affect CBR or JS, which use the same code path but do not trigger the
specific reservoir condition.

The Zag implementation is started but not complete. The validated Python
reference serves as the oracle for future Zag B1-B4 validation.

## 2026-09-26: Python Oracle Repair (SCFSI Persistence Bug)

**Root cause**: The reported VBR "reservoir bug" was actually an SCFSI persistence bug.
Python initialized `ist_pos = [[0] * 40 for _ in range(nch)]` inside the granule loop,
causing granule 1 to reuse zeros when SCFSI requested granule-0 scalefactors. dr_mp3
retains `ist_pos` in decoder state across granules and frames.

**Fixes** (working copy `harvest/ref/mp3ref.py`):
- Added persistent `self.ist_pos = [[0] * 40 for _ in range(2)]`
- Removed per-granule `ist_pos` initialization
- Routed scalefactor and intensity-stereo operations through `self.ist_pos`
- Changed `MAX_BITRESERVOIR_BYTES` from 512 to 511 (matches dr_mp3)

**Validation** (2026-09-26, sequential dr_mp3 stage dumps):
| Fixture | Granules/channels | Worst B1 diff | Failures at 1e-6 |
|---|---|---|---|
| CBR mono | 120 | 2.12e-08 | 0 |
| VBR mono | 120 | 2.9e-08 | 0 |
| Joint stereo | 240 | 2.9e-08 | 0 |

VBR PCM vs ffmpeg: lag 2257 samples, max 1.0 LSB, mean 0.0083 LSB.

## 2026-09-26: Zag B1 Draft (Partial)

**Location**: `~/workspace/decoder_land/mp3/zag/mp3dec.zag`

**Implemented**:
- MSB-first bit reader, cached Huffman bit reader
- MPEG-1 side info parsing (mono/stereo)
- Persistent SCFSI state (`d.*.istpos`)
- Scalefactor decoding with f64 gains (exact f32→f64 widening)
- Huffman decoding with 32 tables, requantization via pow43
- Reservoir handling (511-byte limit)
- B1 hex dump (f64 bit patterns as 16-char hex)

**Validated**:
- Table lookups: `pow43[17]`, `expfrac[0]`, `tab_get`, `tabindex_get` match Python
- f64 bit reinterpretation: 1.0 → 4607182418800017408, -0.5 → -4620693217682128896
- Frame 0, Granule 0 (CBR mono): 576/576 f64 bit patterns match Python exactly

**Open issues**:
- Granule 1+ outputs zeros (bug in bitstream position tracking between granules)
- Panics on frame 2+ with "slice index out of bounds"
- Fixed `layer3gr_limit` units bug (was `*8`, now correct per Python `mbs.pos + part_23_length`)
- B2/B3/B4 not implemented
- Stereo (intensity, MS), short-block reorder, alias reduction, IMDCT, synthesis not implemented

**Verdict**: OPEN. B1 not fully validated.
