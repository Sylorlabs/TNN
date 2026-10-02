# VERDICT — video COMBINATION experiment (NEW 2026-09-26)

## Question
Can TNN's deliberate-memory machinery — the substrate that reproduced the
Big Buck Bunny clip bit-for-bit (PSNR inf / SSIM 1.0, all 24 frames, verdict
90e03018e01e) — DELIBERATELY COMBINE two memorized clips into a NEW video,
deciding HOW to combine and recording its reasons?

## Answer: CLEAN NEGATIVE
TNN did not combine the clips. The attempt ran end to end in pure Zag with
zero RNG: both memories were verified intact (48/48 recalled hashes match
ingest), content was measured, and then the composition step was REFUSED —
mechanically, reproducibly, byte-identically across two runs (rc=1 both).
The refusal is the result, not a failure to run: the mechanism checked for
the machinery composition requires, found it absent, and declined to fake it.

## The two memories
- **Bunny:** the existing verbatim store from the reproduction test
  (`video-repro/runs/work_verbatim`, 24 frames @ 8fps, 320x240, episode-1
  verbatim commits). Reused read-only; not re-ingested.
- **Pig (new):** "2024-06-01 LJUBLJANA ZOO LJUBLJANA - pig", author
  "NaIzletuSi (TM)", CC BY 3.0 via Wikimedia Commons. Source file
  `pig_source.webm` SHA-256
  `b1dbe434629a1b02ffec629089be56dfe58b13d2cbc2f7e44bc205b9fb63540a`
  (90,068,718 bytes). Segment t=3.0 s → 6.0 s (cut-free per ffmpeg scene
  detection over 0–12 s), 24 frames @ 8 fps, 320x240 Lanczos, raw PPM —
  same format as the bunny clip. All 24 frame SHAs distinct (real motion:
  the pig chews/moves at the fence). Full provenance in
  `source/PROVENANCE.md`. Ingested with the EXISTING `repro.zag` verbatim
  path — no new ingestion machinery.

## The attempt (pure Zag, zero RNG — `src/combine.zag`)
1. **Load** both verbatim stores into the arena.
2. **Verify** (white-box): deliberate recall of all 24+24 frames through
   `mem_recall` keyed on (frame,row) provenance; each recalled frame's
   FNV-1a/64 hash compared against the ingest-stage hash from the
   `trace_ingest_verbatim.txt` written at ingestion → **48/48 match**.
   Both clips are present in memory and losslessly recallable.
3. **Measure** (deterministic content measurements, recorded in the trace):
   `bunny_motion=24126181 pig_motion=135685678 bunny_meanlum=174 pig_meanlum=118`
   (motion = sum of frame-to-frame absolute byte differences; the pig clip
   carries ~5.6x the motion — consistent with the chewing/moving subject).
4. **Compose**: the composition step requires a *composition plan* — a
   deliberate record of HOW to combine and WHY, authored by deliberation.
   The binary checks for the machinery that could author or hold such a
   plan, finds none, and **refuses**: prints `COMBINE_REFUSED
   memories_intact=1 novelty_impossible=1`, writes
   `combine_refusal.txt`, exits rc=1.

## Deliberation trace (first-class deliverable)
The full trace is `traces/combine_refusal.txt` (byte-identical across both
runs, SHA-256 `97b9b5d98183c42ed885ede47a93202e96c73895bc624f5d7cef45b888389b0b`).
Condensed, it reads as the mechanism's own reasoning chain:
- both memories verified intact (48/48 recalled hashes match ingest);
- content measured (motion/luminance above);
- composition requires {propose, evaluate, select, synthesize} with reasons
  recorded; the substrate's op set is {mem_add, mem_recall} — 0 of 4 present;
- no composition plan exists in either store (all records are episode-1
  verbatim commits) and the mechanism has no organ that could author one;
- any blend/concat/overlay emitted here would be programmer-authored pixel
  arithmetic presented as TNN's deliberation — declined per the honesty rule;
- verdict: CLEAN NEGATIVE.

## White-box: WHERE does composition fail?
- `mem_recall` is keyed on (frame,row) provenance: it can only ever return
  byte sequences that were committed. There is no write path driven by a
  decision — `mem_add` is called only at ingestion, with source bytes.
- The machinery lacks, specifically: (1) content representation beyond
  pixel rows (no segmentation, no objects, no "pig" or "bunny" as
  entities — the memories are rows of bytes with provenance keys);
  (2) candidate proposal; (3) evaluation/selection among candidates;
  (4) synthesis with recorded reasons.
- This is an architecture gap, not a capacity or determinism gap. The
  reproduction test proved the pipes are lossless (knowledge capture
  complete, machinery exact). This test proves there is no composer organ:
  a perfect memory with no imagination. The honest pairing is "the pipes
  don't leak, and the brain has no composer."

## Numbers
- **Determinism (every binary ran twice, byte-identical or it doesn't
  count):** pig ingest ×2 byte-identical (store SHA-256
  `c5f7fc6bf17634f2805e2478726dddb42b8885e365b89fce2a6c92bfa053d464`
  both runs); pig recall ×2 byte-identical; pig recall == source frames
  (24/24 frame SHAs); pig H_R == H_S 24/24; combine attempt rc=1 both
  runs; refusal traces byte-identical (SHA above). `run_combine.sh`:
  pass=5 fail=0.
- **Closeness measures vs sources:** N/A — no combination video was
  produced (clean negative). Integrity measures instead: 48/48 recalled
  hashes match ingest-stage hashes.
- **Content measurements:** bunny_motion=24126181, pig_motion=135685678,
  bunny_meanlum=174, pig_meanlum=118 (from the refusal trace).

## The dumb control
`dumb_control_sbs_NEW.mp4`: plain ffmpeg side-by-side concat of the two
reference clips (640x240, 24 frames @ 8fps). It is traditionalist
compositing, built OUTSIDE the Zag mechanism, labeled DUMB CONTROL —
shown only so the difference is visible. It is NOT TNN's work and is never
presented as such.

## Deliverables (all marked NEW)
- `~/workspace/your_files/video_combine_new/`: `bunny_NEW.mp4` (a),
  `pig_NEW.mp4` (b), `tnn_combination_REFUSED_NEW.mp4` (c — the refusal
  slate; TNN's "combination" is the documented refusal, not a video),
  `dumb_control_sbs_NEW.mp4` (d), `gallery_NEW.html` — full frames, full
  duration, never crops.
- This workdir: `VERDICT.md`, `src/combine.zag`, `run_combine.sh`,
  `deliver.py`, `source/PROVENANCE.md`, `traces/` (refusal + pig
  ingest/recall traces).

## Honest limits
- The refusal check's policy (what counts as composable machinery) was
  authored by the programmer; the absence it detects — no deliberation
  organ, no plan records, recall keyed to committed bytes only — is a fact
  about the mechanism, verified by the trace hashes, not an assertion.
- The substrate tested here is the minimal deliberate-memory substrate
  from the reproduction test, per the task's reuse directive. A different
  substrate (e.g. the video-imagination machinery) is a different
  experiment; this verdict covers this machinery only.
- Build note: the first `combine.zag` draft had a sentinel bug — it tested
  `hs < 0` to detect trace-read errors, but valid FNV hashes are negative
  as i64 when the top bit is set (e.g. bunny f=00 `e5c51c3a...`), so the
  memory check failed spuriously (rc=-75). Fixed by returning the hash
  out-of-band with a separate status code. All reported runs used the
  fixed binary; the bug never touched a committed artifact.

## Plain-English answer
TNN remembered both videos perfectly and then refused to combine them —
because it has no way to imagine. Its memory is a lossless vault with no
composer inside: it can return any frame it was given, but it cannot
decide how a pig and a rabbit should meet, because "decide" requires
machinery it doesn't have (proposing options, judging them, making new
pixels for the chosen one, saying why). Writing the combination for it
would have been my imagination wearing TNN's name — the experiment's
honesty rule forbids that, so the clean negative is the result. The next
question is not "better memory" (memory is already perfect) but "what
organ would let it compose" — a deliberation-and-synthesis organ the
current substrate was never built with.

## Reproduce
`./run_combine.sh` (expects rc=1 COMBINE_REFUSED at the combine step;
summary pass=5 fail=0) → `python3 deliver.py`. Toolchain:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
