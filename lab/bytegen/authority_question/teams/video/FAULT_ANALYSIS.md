# FAULT_ANALYSIS — video

**Premise:** video's native generation is `frame = F(plan, f)` with zero
cross-frame state (see PATH_MECHANICS.md). Every statement below is checked
against that fact.

## Fault model (video-specific)

Faults are defined at the artifact level — the bytes a viewer/judge/encoder
would consume — because the renderer's internal bytes are pure and
deterministic by construction. Nothing inside the renderer can "go wrong"
except a toolchain/hardware defect; the interesting faults are everything
that happens to the bytes *after* `o_emit_frame` / `f3_raster_visual` produce
them.

| ID | Fault | Video analog of | Mechanism |
|---|---|---|---|
| VF-1 | Bit-flips in frame bytes (single-bit, 64-byte burst, 1 KB burst) | audio 64-sample bit-flip test | Storage bit-rot, memory error on the writer, encoder corruption |
| VF-2 | Zeroed region (16×16 tile, quarter-frame, full frame) | audio full-block dropout | Partial/failed write, truncated transfer, decoder error concealment |
| VF-3 | Full frame dropout (file missing, 0-byte file) | audio 1292-block sustained corruption | Disk full mid-sequence, interrupted run, lost chunk |
| VF-4 | Wrong frame in slot (frame `f` duplicated into slot `f+1`; shuffled order) | — (no audio analog in the battery) | Container assembly bug (`f3_emit_avi` movi indexing), file rename error |
| VF-5 | Sub-floor tampering: ±1–2 LSB global dither shift, small-region tint offset, single-row shift | audio sub-floor low-bit corruption | Adversarial micro-edit, lossy re-encode below the detection floor |
| VF-6 | Plan corruption (wrong constant in `o_scene`, wrong keyframe, wrong `f`) | — | Authoring bug, bad merge — **not an output fault** |

The honest-limits rule applies exactly as in audio (HYBRID_SPEC §8):
VF-5-class faults that don't move a frame's statistics outside the detection
band are invisible, and that must be disclosed, not papered over.

## Where output feedback genuinely HELPS

Exactly one place, and it is **detection, not correction**:

1. **Detecting VF-1–VF-4 requires reading the artifact.** The renderer cannot
   know a disk flipped a bit. Reading back the written frame (or the AVI movi
   chunk) and comparing against plan-derived expectations is the only
   detection channel. This is legitimate output feedback — measurement of
   bytes the renderer emitted — and it is the *trigger* for healing.
2. **Correction is plan-pure re-render, not feedback.** Once a fault is
   detected in frame `f`, the correction map is `C(x) = F(plan, f)` — the
   constant map, Lipschitz 0, idempotent, one-step convergence, exactly as in
   audio HYBRID_SPEC §2. Re-rendering an uncorrupted frame is a byte-identical
   no-op (recurrence 1.0 by construction — PATH_MECHANICS), so false positives
   cost one frame re-render (~2.5 s for ocean, per VID-README) and change
   nothing. There is no safer correction: any "forward" correction that
   adjusts frame `f+1` to compensate frame `f`'s corruption is **causally
   wrong** — it distorts a clean frame to apologize for a corrupted one, and
   in video it is also *pointless*, because frame `f` exists as an
   independent file and can simply be rewritten.
3. **VF-4 (duplicated/shuffled frames) is detectable plan-side** via the
   temporal invariant the plan already guarantees: ocean's V-TEMP bar
   (per-pair mean|Δ|/255 ∈ [0.5%, 15%], measured 8.59–10.75%) and field-AVI's
   exact keyframe endpoints. A duplicated frame shows |Δ| ≈ 0 — far outside
   the authored motion band. No cross-frame *carried* state is needed to check
   this; it is a pairwise plan-derived predicate.

Note the asymmetry that makes video *easier* than audio here: audio's
exception path needs "detection precedes consumption" (double-buffered
blocks) because blocks flow into a continuous mix. Video frames are
independent files — detection can happen any time before downstream use, and
re-render is a file rewrite. The fault model assumption is weaker and the
healing is equally exact.

## Where output feedback would CORRUPT

### C1. A continuous per-frame servo creates a coherence tax where none exists

Audio measured a real tax: carried servo state dragged motif recurrence from
1.0 → 0.74 (HYBRID_SPEC §6, Attack 6). Video's native recurrence is exactly
1.0 — re-render frame `f` any time, get byte-identical bytes. A continuous
feedback loop (the video analog of v1's per-block servo: e.g. per-frame
gain chasing a frozen mean-luminance target, or per-frame "smoothness"
correction chasing the V-TEMP band) would inject cross-frame carried state
into a path that currently has none. Mechanically:

- Frame `f+1`'s pixels become a function of (plan, f+1, measured(frame f)).
- Re-render of frame `f+1` in isolation no longer reproduces the shipped
  bytes — recurrence drops below 1.0 by construction, and V-DET (clean rerun
  → byte-identical manifest) can only pass if the servo state is also
  re-derived, i.e. the whole sequence must be re-rendered in order.
- The tax is *created* by the loop. There is no RT-LONG-style capability on
  the other side of the trade (see C3): the loop buys nothing.

This is the single strongest anti-feedback fact in video: **feedback cannot
improve a recurrence of 1.0; it can only degrade it.**

### C2. A servo reintroduces the exact tells the lab already killed

Ocean round 3 was a rebuild *against* global post-process looks: tell repair
#3 killed the "global RGB retint" in favor of material-driven color
(depth→water color, sun diffuse, fresnel, foam, fog — VID-README). A
feedback loop that adjusts scene parameters from measured output — "frame 12
is dark, raise the sun for 13+" — is a global grade wearing a servo's
clothes. It fights the material law the plan authors, and it does so from a
measurement (frame brightness) that conflates scene content with lighting.
The audio battery's Attack 1 lesson applies verbatim: the loop's target is a
frozen literal the plan didn't author, and on any other scene it permanently
fights the plan toward that literal.

### C3. Self-referential events convert PAR video into AR video — importing the cascade

The hypothetical video analog of RESPOND: "spawn the breaker when the
rendered vortex brightness crosses X", "the bird looks at the brightest
pixel of the previous frame". Mechanically this makes frame `f+1`'s plan a
function of frame `f`'s bytes — a genuine output→input loop, the thing the
survey proved no native path does. Consequences, measured in audio terms:

- **Cascade:** audio RT-CASCADE showed a single fault derailing 5,791
  post-fault samples (~131 ms) in the AR fork vs 0 in PAR. In video, a
  corrupted frame `f` (VF-1) would not just corrupt frame `f` — it would
  divert the *scene*: the event predicate reads corrupted bytes, fires or
  misfires, and every subsequent frame is computed from a diverged plan.
  Healing requires re-deriving the whole tail, not re-rendering one frame.
  The fault blast radius goes from one file to the sequence.
- **It is also unnecessary.** Because generation is a pure function of the
  plan, "the brightest pixel of frame 29" is computable *plan-side without
  rendering* — run the same deterministic functions over the plan and read
  the answer. Output feedback is only irreplaceable when the forward map has
  hidden state or the measurement is of something outside the buffer (a
  physical display's calibration, a speaker in a room). For file-generation
  video, the buffer is the output; there is nothing to learn from the bytes
  that the plan doesn't already determine.

### C4. VF-6 (plan corruption) is the trap that feedback cannot fix

If `o_scene` has a wrong constant or a keyframe is mis-authored, every frame
renders "correctly" from a wrong plan. Output feedback *cannot* detect this:
the bytes match the (wrong) plan perfectly, so every plan-derived predicate
passes. A feedback loop that "corrects" toward measured output here would be
correcting toward the wrong plan's own output — a loop that converges on the
bug. The only fix is plan revision by the author (or TNN's deliberate
judgment), which is outside the authority question entirely. This bounds the
exception path: it heals *artifact* faults (VF-1–VF-4), never *plan* faults.

### C5. The dither channel: a concrete sub-floor illustration

Ocean's dither is ±2 LSB deterministic hash (`o_hash2(x*3+sy, f+700, 78)`).
A tamper that re-dithers or strips dither moves per-pixel values by ≤2 LSB —
frame RMS moves by a fraction of a percent, far below any sane detection
band, exactly like audio's 64-sample zeroing (×0.97 RMS, below the
[0.35×, 2.5×] floor). Disclosed as invisible. A feedback loop *could* be
tuned sensitive enough to catch it — and would then false-positive on every
clean frame, re-rendering the world to chase 2 LSB of hash. The band edges
are a real safety boundary: below the floor, abstention is the honest move.

## RESPOND-analog check: none found (verified)

Searched both paths for any element whose content depends on measured
rendered output:

| Candidate | Verdict |
|---|---|
| Foam advected "along the flow" (ocean) | Plan-pure: back-traced in the rotating frame from `(f, rot)`, never read from pixels |
| Vortex center migration (`o_scene`) | Plan-pure: `o_vn3(f * 64, …)` hash of the frame index |
| Wave/swell phase (`sx1 = wx - f*12/10`) | Plan-pure advection |
| Field-AVI keyframe interpolation | Plan-pure: `va + (vb-va)*t8/8`; g-series per-cell timing is `f3_hash2` of coordinates |
| Audio-video interleave (`apf = total/NF`) | Plan-pure interleave count |
| `f3_bird_scene` / `f3_boat_scene` subjects | Plan-pure functions of `(far, fr, NF)` |
| V-TEMP / V-SHARP / V-DET bars | Post-hoc judging (`verify_vid.py`), not generation input |

**Video has no RESPOND-class events.** There is nothing to latch, because
there is nothing the plan needs to learn from its own bytes.

## Summary table

| Feedback use | Helps? | Why |
|---|---|---|
| Detect artifact faults (VF-1–VF-4) by reading back frames | **Yes** — the only detection channel | Renderer can't see disk/encoder faults |
| Heal by plan-pure re-render of the faulted frame | **Yes** — exact, L=0, idempotent | Frame is `F(plan,f)`; false positive is a no-op |
| Continuous per-frame servo (leveling, smoothing) | **No** — corrupts | Creates a 1.0→<1.0 coherence tax; reintroduces killed tells (C1, C2) |
| Self-referential scene events keyed to rendered pixels | **No** — corrupts | Converts PAR→AR; cascade blast radius; computable plan-side anyway (C3) |
| Fixing a wrong plan (VF-6) via output measurement | **No** — impossible | Bytes match the wrong plan; loop converges on the bug (C4) |
| Sub-floor tamper (VF-5) | **Abstain** — honest floor | Below the band; chasing it false-positives on clean frames (C5) |
