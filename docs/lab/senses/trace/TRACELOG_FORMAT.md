# SENSE-TRACE v1 — trace-log format, stage inventory, localization procedure

Permanent senses infrastructure (Micah order 2026-09-26, worker B white-box
trace foundation). Every intake stage in every sense records its input
checksum, output checksum, and parameters in a per-run trace log. Any future
defect localizes to the exact stage by checksum comparison.

## 1. Trace-log grammar (v1)

Deterministic, line-oriented, UTF-8. Same input + same params =>
byte-identical log (no timestamps, no PIDs, no addresses — this is load-bearing:
golden checksums must reproduce).

```
# SENSE-TRACE v1
RUN sense=<audio|image|video> format=<format-desc> src=<sha256hex> params=<k=v,...>
STAGE <seq> <sense>.<stage> in=<sha256hex|-> out=<sha256hex> in_len=<n> out_len=<n> params=<k=v,...>
HELD sha=<sha256hex> len=<n> desc=<text_with_underscores>
END rc=<rc>
```

- `src` = SHA-256 of the raw input bytes as read from disk.
- `in`/`out` = SHA-256 of the exact byte buffers the stage consumed / produced.
  Stage 0 (`raw_read`) has `in=-` (its input is the file on disk, identified by
  `src`).
- `params` = `k=v,k=v` (no spaces). Carries the stage's gate values and knobs
  (e.g. `bpp=24,comp=0,stride=1536`), plus provenance annotations:
  - `in_src=<sense>.<stage>` — this stage consumed an earlier stage's output
    that is NOT its immediate predecessor (e.g. pixel_copy re-reads the raw
    bytes; declares `in_src=image.raw_read`).
  - `fork_of=<sense>.<stage>` — this stage checksums a SLICE of an earlier
    stage's output (e.g. the audio head-sample stage). The slice is declared
    in params (`n_head=64`); the bytes are reproducible by rerunning the
    traced driver.

## 2. Linkage / provenance rules (what the verifier checks)

1. `RUN src` == `STAGE 0` out.
2. Stage seq numbers are 0,1,2,… with no gaps.
3. **Provenance closure:** every non-fork stage's `in` equals the RUN `src` or
   some earlier stage's `out`. A stage can never consume bytes that no traced
   stage produced. (This is the white-box property: the log is a closed
   provenance chain from raw input to held representation.)
4. Fork stages declare `fork_of=` pointing at an earlier stage.
5. `HELD sha` == last STAGE out, `HELD len` == last out_len.
6. `END rc=0`.
7. **Golden check (optional):** a goldens file (`name=sha` per line); any stage
   whose full name matches a golden key must have `out` == golden sha.

## 3. Stage inventory

### 3a. Audio — `audio_intake_trace.zag` (pure Zag)

Canonical intake: crew-P input organ, the standing forward sense. Intake idioms
VERBATIM from `docs/lab/audio_principles/crew_p/organ.zag`
(blob `6dbc673896718a2a223e8671e0ff451f60711c9d` @ origin/tnn-native-lab
`e8bb16a0b`): chunk-aware RIFF walk, PCM16/mono/44100 gate, `get_s16` with
CORRECT sign extension (`v>=32768 → v−65536`; the f3_get32 unsigned trap is not
present). Format recorded: `WAV/PCM16/mono/44100`.

| seq | stage | in | out | params |
|---|---|---|---|---|
| 0 | `audio.raw_read` | - | sha(raw file bytes) | `origin=file` |
| 1 | `audio.wav_parse` | sha(raw) | sha(data-chunk payload bytes) | `fmt_ok=1,dsamp=<n>,nsamp=<n>` |
| 2 | `audio.head_samples_0_63` | sha(payload[0..128]) | sha(stored head[0..128]) | `fork_of=audio.wav_parse,stored=1,n_head=64` |
| 3 | `audio.s16_extract` | sha(payload) | sha(s16 LE bytes) | `nsamp=<n>,sign_extend=1,conv=get_s16` |
| 4 | `audio.held_pcm` | sha(s16) | sha(s16) | `identity` |

HELD = the s16 LE bytes (TNN holds full 16-bit samples; loss enters only at
the descriptor stage, by design).

**The head-sample stage (stage 2).** The input-verdict white-box found that
`hear()` never stores samples 0..63 (L1 bug — fabricated head, resonant LPC
gain rings). This stage extracts the 128 head bytes into their own buffer,
stores them, and checksums the stored bytes with `stored=1`. Golden head
checksum for `fixture_strike.wav`:

```
audio.head_samples_0_63 = f183085e661eabe4a09acf919b3c30bca568ea36828cd2ad3895eab45d996271
```

The sibling repairing `hear()` verifies the repair by emitting an identical-
format log (via `sense_trace_py.py`) and comparing its stage-2 `out` to this
golden. A fabricated or missing head fails the golden check at exactly this
stage (demonstrated: buggy trace → `FAIL: STAGE 2 audio.head_samples_0_63`).

### 3b. Image — `image_intake_trace.zag` (pure Zag)

Canonical intake: the BMP idiom shared byte-identically by all 6 files in the
image program (input verdict 2026-09-26). Intake block VERBATIM from
`docs/lab/image_exact_work/v3/ingest.zag`
(blob `1dd37cdb45f8ec0a2bc6abf1957d6e00a392cdde` @ origin/tnn-native-lab
`e8bb16a0b`): parse BMP header (magic `BM`, `bpp==24`, `comp==0` uncompressed
enforced, `off/w/h` LE) → stride `(w*3+3)/4*4` → copy pixels BGR bottom-up →
RGB top-down. What intake does NOT do: no color-space conversion, no scaling,
no quantization, no gamma, no dithering — pure byte reorder + orientation
flip. Format recorded: `BMP/24bpp/uncompressed`.

| seq | stage | in | out | params |
|---|---|---|---|---|
| 0 | `image.raw_read` | - | sha(raw file bytes) | `origin=file` |
| 1 | `image.bmp_header` | sha(raw) | sha(54-byte header) | `magic=BM,off=<n>,w=<n>,h=<n>,bpp=24,comp=0,stride=<n>` |
| 2 | `image.pixel_copy` | sha(raw) | sha(held pix, w*h*3 RGB top-down) | `w=<n>,h=<n>,stride=<n>,transform=BGR_bottomup_to_RGB_topdown,in_src=image.raw_read` |
| 3 | `image.held_pix` | sha(pix) | sha(pix) | `identity` |

HELD = the `pix` buffer — the observation every downstream layer deliberates
over (structure, edges, texture/zoom, residual all read `pix`).

### 3c. Video — `video_intake_trace.zag` (pure Zag)

Canonical intake: `read_ppm_gen` in
`docs/lab/imagination/video-composer-step2/src/composer.zag`
(blob `07d25816d1505046e5d221c4862e94f563097f1f` @ origin/tnn-native-lab
`e8bb16a0b`): raw PPM P6 reader, exact-size-checked verbatim byte copy; no
quantization, no chroma conversion, no resampling. All three composer lines
carry byte-identical reader bodies (`304ee68f7508e0f1`). Format recorded:
`PPM/P6`.

| seq | stage | in | out | params |
|---|---|---|---|---|
| 0 | `video.raw_read` | - | sha(raw file bytes) | `origin=file` |
| 1 | `video.ppm_header` | sha(raw) | sha(header bytes) | `magic=P6,w=<n>,h=<n>,maxval=255,hdr_len=<n>` |
| 2 | `video.raster_copy` | sha(raw) | sha(held frame, w*h*3) | `w=<n>,h=<n>,exact_size_check=n==p+need,copy=verbatim,in_src=video.raw_read` |
| 3 | `video.held_frame` | sha(frame) | sha(frame) | `identity` |

HELD = the held frame raster.

### 3d. Audio v5g `hear()` path (Python) — `sense_trace_py.py`

The long-memory v5g line's `hear()` (`imagination/rawbyte/v5/proto5g.py`, blob
`690ba2ed3b4458cdacda302dec2776e8a89c35d1`) is Python; it emits the identical
v1 grammar via `sense_trace_py.TraceLog` so one verifier checks both. Stage
map (numpy arrays hashed as `arr.tobytes()`; dtype+shape in params):

```
audio.wav_parse          in: wav bytes            out: payload bytes
audio.head_samples_0_63  in: payload[0:128]       out: stored head bytes (fork; stored=0 + out=- if missing = the bug)
audio.lpc64              in: payload bytes        out: a.tobytes()        (P=64 Levinson coeffs)
audio.residual           in: payload bytes        out: res.tobytes()
audio.pitch              in: res.tobytes()        out: str(pT).encode()  (autocorr lags 50..sr/20)
audio.t0_refine          in: res.tobytes()        out: pack('<dd',T0,NBINS)
audio.plm                in: res.tobytes()        out: plm.tobytes()      (phase-locked mean)
audio.period_pmf         in: res.tobytes()        out: PMF.tobytes()     (17-bin jitter PMF)
audio.kmeans64           in: nres.tobytes()       out: proto.tobytes()+q.tobytes()
audio.bigram_ep          in: q.tobytes()          out: bg.tobytes()+EP.tobytes()
audio.boost_calib        in: res.tobytes()        out: pack('<d',boost)
audio.held_m5g           in: model bytes          out: m5g file bytes     (RBLMEMv5)
```

Read-back path: `rb_longmem.zag` mode 9 (blob
`1b216693e164d51353830a71cc20938cbe51318f`) re-emits PCM from `m5g_*.bin`;
its stages (`m5g_read` → `reemit`) are traced by re-running the traced audio
driver on the re-emitted WAV and diffing HELD checksums.

## 4. Format-agnostic design

The trace library (`sense_trace.zag`) hashes raw bytes — it knows nothing
about WAV/BMP/PPM. Format-awareness lives in exactly two places, both
data-driven:

1. The RUN line's `format=` descriptor (free-form: `WAV/PCM16/mono/44100`,
   `BMP/24bpp/uncompressed`, `PPM/P6`, …). Micah's direction is that TNN must
   handle ANY image/video/audio format; a new format adds a new driver (or new
   stages) that records its own `format=` — the grammar, library, and verifier
   are unchanged.
2. Stage `params` (gate values like `bpp`, `comp`, `maxval`, `ch`, `sr`,
   `bits`) — the per-format acceptance criteria, recorded so a future debugger
   sees exactly what the intake asserted.

Stage NAMES are namespaced `<sense>.<stage>`; a future JPEG intake would emit
`image.jpeg_header`, `image.idct`, … under `format=JPEG/...` without colliding
with the BMP stages.

## 5. Localization procedure (the future debugger's playbook)

You have a bad output (wrong pixels, wrong samples, a downstream verdict that
moved). Localize it to the exact intake stage:

1. **Reproduce with tracing.** Run the sense's traced driver on the same input:
   `./<sense>_intake_trace <in> <out> <trace.log> on`
   (drivers live in this directory; build with `build.sh`).
2. **Verify the log.** `python3 trace_verify.py <trace.log>` — checks grammar,
   provenance closure, HELD binding. A structural break here means the trace
   itself is corrupt (rerun; logs are deterministic — two runs must be
   byte-identical).
3. **Check goldens.** `python3 trace_verify.py <trace.log> --goldens <goldens>`
   with the golden checksums for the fixture (this directory's goldens files,
   or the input-verdict evidence). The FIRST stage whose `out` diverges from
   golden is the defect stage — exactly like the pentagon investigation named
   the greedy chord-tracing mechanism in the edge stage by parsing the actual
   trace.
4. **No golden for this input?** Bisect by linkage instead: walk the stages and
   compare each stage's `out` against a known-good run's log for the same
   input (stage N's `out` != stage N+1's `in` can only happen across a fork —
   otherwise it is itself the defect: bytes changed between stages with no
   stage claiming the transform).
5. **Name the mechanism, not the vibe.** Open the driver source at the failing
   stage; the stage boundaries are the verbatim intake idioms pinned in §3.
   The defect is IN that stage's code (or in the parameters it asserted —
   check `params=` first: a `bpp=24` gate rejecting a valid file is a
   parameter defect, not a byte defect).
6. **Fix, then re-prove.** After repair: rerun traced → `trace_verify.py`
   PASS + golden PASS; rerun with tracing off → output byte-identical to
   tracing-on (zero-impact holds); commit the new golden if the fix
   legitimately changes a stage's output (document why in the commit message —
   a golden change is a verdict-level event).

## 6. Zero-impact contract

Tracing observes; it never alters. Proof obligations for any change to a
traced driver:

- `sha256(out_on) == sha256(out_off)` — outputs byte-identical tracing on vs off.
- `sha256(trace_on_run1) == sha256(trace_on_run2)` — logs deterministic.
- `trace_verify.py` PASS on the on-log.

Measured numbers are in `RUNLOG.md`.
