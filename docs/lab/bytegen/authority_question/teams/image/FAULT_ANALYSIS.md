# FAULT_ANALYSIS — where output feedback would help vs corrupt (image)

Team Image, 2026-09-23. Fault models are concrete, mechanistically
grounded in the three native paths (PATH_MECHANICS.md), and stated so a
battery can implement them directly (see BATTERY_PREREG_DRAFT.md).

## F1 — Region corruption (post-render buffer damage)

**Model.** After rendering completes, a rectangular region of the pixel
buffer is damaged: bit-flips (top-bit flips = visible spikes), zeroing
(dropout tile), or a shifted/offset write (tearing). This is the image
analog of the audio block bit-flip test.

**Where feedback (as detect-and-reassert) HELPS.** Plan-pure region
re-render heals exactly on all three paths:

- Path C (disc.zag): pixel = F(coords, seed). Re-evaluating the region
  reproduces the original bytes bit-exactly — 0 differing bytes by
  construction. There is no carried state, so no ordering constraint.
- Path A (field.zag): replay the recorded strokes (`f3_sop`/`f3_spar`
  plan log) into a fresh arena, re-run `f3_raster_visual` (or `_g`) over
  the region. The stroke log IS the plan; replay is deterministic
  (:12–13). Heals to 0 differing bytes.
- Path B (toolkit): re-run the screen function over a fresh canvas
  restricted to the region, **replaying all layers in order**. This is
  where d_blend matters: a naive "re-blend the top layer's pixels" reads
  corrupted under-pixels and bakes the fault in. The correct re-render
  replays the full op sequence, so every d_blend read-back operand is
  itself plan-determined. Heals to 0 differing bytes.

Correction map is constant in the corruption (re-render output does not
depend on the damaged bytes), Lipschitz 0, idempotent, one-step — the
same contractivity proof as audio HYBRID_SPEC §2. A false positive is a
no-op (re-render of clean bytes = identical bytes).

**Where feedback CORRUPTS.** Any servo that "corrects" using measured
neighbors instead of the plan: e.g. a brightness servo that rebalances
the damaged region toward the mean of surrounding regions, or forward
compensation that brightens *future* (clean) regions to "make up for"
the damaged one. The audio Attack 6 verdict applies verbatim: forward
correction from a corrupted measurement is causally wrong — it distorts
clean pixels to compensate already-rendered damage, and the distortion
persists after the fault is gone. A measured-neighbor inpainting servo
additionally invents content the plan never authored — a truthfulness
violation, not just a rendering bug.

**Detection.** For image, detection can be *bit-exact*, stronger than
audio's band-based predicate: re-render the region to scratch, diff
against the buffer. Any differing byte = fault. No detection floor
exists for this fault class (audio's honest-limits floor — small
corruptions hiding inside the [0.35×, 2.5×] RMS band — has no image
analog here). Cost is the design question: full re-render doubles render
cost; the prereg proposes spot-check scheduling (see battery draft).

## F2 — Carried-state corruption mid-render

**Model.** Path A: field cells corrupted *during* stroke application
(e.g. a blotch stroke writes garbage into cells, or memory corruption
lands in the arena). Path B: canvas corrupted mid-layer-sequence. Path C:
immune — no carried state.

**Where feedback HELPS.** Exactly one form: **detect, then replay from
the plan** — the stroke log (Path A) or the op sequence (Path B) —
never "correct forward" from the corrupted intermediate. The replay must
start from a clean arena/canvas, because the corrupted cells/canvas are
inputs to every later stroke/layer (blotch blending reads cells; layers
paint over canvas). This is audio Attack 6's lesson restated for image:
healing = plan-pure reconstruction, not measured-state surgery.

**Where feedback CORRUPTS.** A controller that reads the corrupted cells
and adjusts *later* stroke parameters (e.g. "the field is too bright,
reduce blotch alpha for remaining strokes") bakes the corruption into
the plan's future — the same rail-pin/2-cycle class as audio Attack 4,
and it destroys the stroke log's authority: the log no longer describes
what was rendered. Once parameters move from measured cells, the plan
stops being the plan.

## F3 — Global operations (the gamma.zag lesson, native specimen found)

**Model.** A full-image post-pass whose parameters derive from the
*rendered output*: auto-contrast, histogram equalization, peak
normalization, DC removal.

**Native status.** The pixel paths are CLEAN: `d_emit_bmp`
(toolkit.zag), disc.zag's emitter, `f3_emit_bmp`/:2408 — all pack rows,
no output-derived gains (verified by read). **But the disease exists
natively in the audio emitters of the same file:** `f3_emit_wav` :1025–1039
(`peak` measured over the rendered mix; `if (peak > 28000) v = v*28000/peak`),
`f3_emit_wav_hifi` :1166–1184 (×24000/peak unconditionally), the legacy
video writer `f3_emit_avi` :1496–1512 (peak→28000), and the G-series video
writer `f3_emit_avi_g` (:1863–1881, ×24000/peak on the soundtrack).
These are four genuine output-feedback global gains, in production code, on
the image/video line's own soundtrack.

**Why it CORRUPTS (feedback admitted where none belonged).** A single
corrupted sample moves `peak`, so *every* sample's gain shifts — the
fault is amplified from one sample to all samples. Bit-identity across
content edits is dead (edit one stroke → global peak moves → every byte
changes; cf. ~/workspace/AGENTS.md gamma.zag note). And detection
becomes ill-defined: "plan-expected output" can no longer be computed
from the plan, because the gain is a function of the (possibly
corrupted) output. This is exactly why audio's hybrid spec derives
detection targets from the plan under render (HYBRID_SPEC §5), never
from rendered statistics.

**Implication for image authority.** If image ever grows an
auto-contrast/auto-levels post-pass (the natural "helpful" feedback —
"make the render pop"), it must be plan-derived (contrast curve from
stroke params/scene seed) or it inherits every pathology above. The
recommended rule forbids output-derived global gains outright.

## F4 — Seam / tiling artifacts

**Model.** Visible discontinuities: at tile boundaries (if tiled
rendering were used), at stroke-occlusion edges, at the impossible
triangle's miter lines (disc.zag arch: over/under carried *entirely* by
seam shading, :809–939 comments).

**Native status.** The paths avoid tiling by construction: disc.zag's
header explicitly bans axis-aligned primitive tiling ("latitude-parallel
bands (no tiling)"); field.zag rasterizes by bilinear interpolation from
one continuous field; toolkit paints one canvas. Seams that exist are
**authored content**: the arch's highlight-lip/dark-seam pairs ARE the
cyclic over/under signal; stroke occlusion order IS the depth signal
(f3_gen_g2 comment: "foreground mullion bar drawn AFTER the glow occludes
its left edge").

**Where feedback CORRUPTS.** A seam-detecting smoother (measure gradient
across a boundary, blur it down) cannot distinguish authored seams from
defect seams — the measurement contains no intent signal. Running it
would erase the arch's over/under shading: the one feature that makes
the impossible triangle read as impossible. Intent lives only in the
plan (stroke order, scene geometry); the output cannot reveal it. So
feedback has no information advantage over plan-pure re-render here —
only an information deficit.

**Where feedback HELPS.** Nowhere beyond F1: a seam that is a genuine
rendering defect (e.g. a torn tile from F1-style corruption at a tile
edge) heals by plan-pure region re-render, same as any region fault.
No seam-specific authority is needed or safe.

## F5 — Grain and dither (plan-pure adaptivity, not feedback)

**Model.** `f3_raster_g`'s shadow-growing grain (:2257–2290) and
disc.zag's ±3 LSB dither look like "the renderer adapting to the image"
— a tempting feedback precedent.

**Settled: not feedback.** The grain amplitude `gr=(gp+gt)·(384−luma)/256`
reads `luma` computed from the plan's cell values *in the same pure
function*, never from the output buffer; `gp`/`gt` are coordinate hashes.
Re-rasterization reproduces grain bit-exactly. Corruption of output
bytes does not move the grain model — so there is nothing for feedback
to "correct," and a feedback grain-matcher (measure output noise,
re-synthesize matching grain) would be fitting to corruption. Plan-pure
re-render already heals grain regions exactly (F1).

## F6 — Sub-threshold / invisible corruption

**Model.** A few low-bit flips in a smooth gradient: invisible to any
human eye, below any perceptual threshold.

**Honest position.** Bit-exact detection (F1) catches these; whether to
*correct* them is a policy question, not an authority question. The
recommended rule says: detection fires on any byte difference; correction
is the same plan-pure re-render regardless of magnitude. There is no
"too small to bother" feedback servo — a magnitude-gated servo would be
audio's v1 loop wearing a costume (a continuous controller with a dead
zone is still a continuous controller). Cheap, exact, boring: re-render.

## Summary table

| Fault | Plan-pure re-render heals? | Feedback helps? | Feedback corrupts? |
|---|---|---|---|
| F1 region corruption (buffer) | Yes, 0 differing bytes | Yes — detect-and-reassert ONLY | Neighbor-matching / forward compensation |
| F2 carried-state corruption (mid-render) | Yes — replay from plan | Yes — replay from plan ONLY | Parameter adjustment from measured cells |
| F3 output-derived global gain | N/A (prevention, not cure) | Never | Peak/normalize from output: amplifies faults, kills bit-identity, ill-defines detection |
| F4 seams | Yes (defect seams = F1) | No | Seam smoother erases authored over/under |
| F5 grain/dither | Yes, bit-exact | No (nothing to correct) | Grain-matcher fits to corruption |
| F6 sub-threshold flips | Yes | No servo needed | Magnitude-gated servo = v1 loop in costume |
