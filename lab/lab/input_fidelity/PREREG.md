# PREREG — Input Fidelity Battery (frozen 2026-09-27)

Micah's directive: "measure input faithfulness with real fixtures and show
input-vs-held side by side for his eyes and ears before any imagination is
judged." Exact replication is the gate before imagination.

## Objective

Measure, per modality, whether TNN's intake HOLDS what the input contains:
input file → TNN intake → held representation → re-emitted output, compared
against the input (or an independent reference decoder). This is MEASUREMENT +
DIAGNOSIS only. No repair, no redesign, no new mechanisms.

## Definitions of "faithful"

- **Image:** lossless formats (PNG, BMP) → held pixels BYTE-IDENTICAL to the
  reference decode (SHA-256 of held output == SHA-256 of reference). Lossy
  (JPEG baseline) → bounded honest diff vs reference decoder, mechanism named.
- **Audio:** lossless (WAV PCM, FLAC) → held PCM BYTE-IDENTICAL (SHA-256).
  MP3 → within the committed validated LSB bounds vs oracle/ffmpeg.
- **Video:** container+codec → frames byte-identical to reference. H.264 slice
  decode is BLOCKED at committed state → reported as an honest capability gap,
  not bar-scored.

## Frozen fixtures (sealed, docs/lab/universal_intake/MANIFEST.sha256)

| Fixture | SHA-256 (prefix) | Modality |
|---|---|---|
| fixtures/img_m320.png | 9e92cfb4 | image lossless |
| fixtures/img_m320.bmp | aae3ec31 | image lossless |
| fixtures/img_s16.png | f8b3f292 | image lossless |
| fixtures/img_odd.png | 29df9eb2 | image lossless |
| fixtures/img_m320_q95_444.jpg | 54d1614c | image lossy 4:4:4 |
| fixtures/img_m320_q90_420.jpg | f86f3a75 | image lossy 4:2:0 |
| fixtures/t_pcm16.wav | 27629ec7 | audio lossless |
| fixtures/t.flac | d76182c0 | audio lossless |
| fixtures/t24.flac | 6650e0a9 | audio lossless |
| mp3/fixtures/t_128cbr.mp3 | a08aaf14 | audio MP3 CBR |
| mp3/fixtures/t_128js.mp3 | 445663e6 | audio MP3 joint-stereo |
| fixtures/t.mp4 | 424f5cc7 | video container |

Fixtures are referenced by SHA; no fixture blobs are added by this battery.

## Protocol

1. Re-run the COMMITTED intake sources (docs/lab/universal_intake/src/*.zag,
   pinned toolchain) on the sealed fixtures in a lean workdir (~/workspace/
   scratch, cleaned after). Record held-output SHA-256; compare against the
   committed claim SHAs in docs/lab/universal_intake/VERDICT.md.
2. **Audio: waveform analysis FIRST** on input vs held — HNR, spectrum
   (centroid, 85% rolloff, >16kHz ratio), envelope stationarity (thirds RMS,
   crest, ZCR), spectral drift, loop-periodicity, transient regularity,
   hum/tonal (50/60 Hz + harmonics). No audio verdict without measurements.
   Agents cannot hear audio.
3. **Image/video: full frames only.** No crops (judge has full eyes).
4. For every fidelity gap: white-box the stage that loses information, name
   the mechanism, rank gaps by size (bits/LSB/dB/pixels affected).
5. Gallery: input-vs-held side by side, SELF-CONTAINED (every asset a data
   URI; grep `src="(?!data:)` before delivery). Label every artifact new vs
   previously-shown; never re-show an old artifact as a fresh demo.

## Bars

| Bar | Threshold |
|---|---|
| B1 image lossless | byte-identical (SHA-256 match) on all 4 PNG/BMP fixtures |
| B2 audio lossless | byte-identical (SHA-256 match) on WAV + both FLAC fixtures |
| B3 JPEG honest-lossy | 4:4:4 maxdiff ≤3, meandiff <0.4; 4:2:0 gap mechanism named and bounded |
| B4 MP3 | within committed validated bounds (oracle/ffmpeg LSB) |
| B5 video H.264 | NO BAR — capability gap reported honestly (slice decode blocked) |

## Scope notes

- Committed state ONLY. The working tree carries uncommitted MP3 changes
  (mp3dec.zag, mp3tab64.zag modified 2026-09-27) — explicitly OUT OF SCOPE;
  recorded as pending, not measured.
- image_exact_work v3 (BMP knowledge-path byte-identical, SHA 4ee3414b…) is
  prior evidence; this battery re-verifies the SHA claim, not the full path.
- video-fusion-v4 is a fusion (imagination) line, BLOCKED on an integration
  crash — out of scope except its PROVENANCE fixtures (PPM frames) as
  reference inputs for the video input path.
- Small frequent commits; workdirs cleaned after each measurement.
