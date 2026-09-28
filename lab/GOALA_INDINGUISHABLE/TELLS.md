# GOAL-A TELL-HUNT — TELLS.md

**Worker:** GOAL-A Worker 1 (tell-hunt), 2026-09-21/22 overnight.
**Reasoning provider:** gpt-5.6-sol via UnoRouter (grok-4.7 hard-stop, see FALLBACKS).
**Method:** measure first (Python/PIL/numpy on artifacts + Zag source reading), enumerate tells with a red-team, design Zag-concrete fixes (deterministic, `f3_hash2`-based, byte-identical), red-team each fix, blind re-attack with fresh analysts not shown the fix list.
**Scope:** 14 field BMPs (240×240), 2 AVIs (240×240, 8fps, 24f), audio incl. `f3song_hifi.wav` (44.1kHz). Audio tell-hunt only — no synth rebuild (sine-LUT is another track).
**Bars (from PREREG):** H-symmetry < 0.60 on all shipped images; no image < 50 unique colors unless intentional flat-design brief; hero images ≥ 480×480; byte-identical reruns; no RNG; pure Zag.

## Master tells table (ranked by detectability)

| rank | tell | medium | evidence (measured) | fix hypothesis (Zag-concrete) | predicted metric movement | red-team objection + resolution | status |
|---|---|---|---|---|---|---|---|
| 1 | I1 — Pervasive horizontal mirror symmetry | img | H-sym 0.79–1.00 on 10/14; f3n15 = **1.000**; f3n14 = 0.997; f3b4 = 0.976. Source found in code: `ig_zmirror` duplicated placements at imagine.zag:524, 1266–1269 | **F1**: at the `ig_zmirror` call sites, perturb the mirrored copy only (position/scale/color via `f3_hash2(element_id, zone, scene_seed)`) before `ig_place` | H-sym → **< 0.60** on all shipped images (expect 0.35–0.55) | Objection: fixed-range jitter reads as "mirror plus programmed jitter" / misregistration. Resolution: use *relational* adjustments (local occlusion, edge interruption, one color-area change), keep below misregistration threshold, preserve shared major-axis alignment | fixed-pending-Zag |
| 2 | V1 — No coherent subject (animated static) | vid | v1/v2 frames read as TV static; no stable contours, no identifiable subject in any of 24 frames | **F10**: persistent foreground silhouette (20–35% of frame) built from `f3_rect` + `f3_blotch`, drawn identically every frame in `f3_gen_v1`/`f3_gen_v2`; hash texture low-amplitude, subordinate | No-subject → stable connected foreground region; optical flow gains a distinct subject region | Objection: identical silhouette internals every frame = "sticker/clip-art" tell. Resolution: add scene integration — contact shadow, occlusion, lighting response — before shipping | fixed-pending-Zag |
| 3 | A1 — Exact integer-grid timing, zero expressive shaping | aud | Code ground truth: `f3_gen_song` places notes at integer frames 0,4,8,…,32. Measured onsets 245/727/1228/1718/2244 ms, IOIs 482/501/490/526 ≈ rigid 500 ms pulse, no rubato/phrase shaping | **F6**: in `f3_gen_song`, hash-derived onset offsets (±3–12 ms, phrase-aware: pickups lead, cadential notes lag), durations preserved, no adjacent-note crossing | Grid deviation 0 → 3–12 ms structured, deterministic | Objection: hash-correlated offsets create a timing fingerprint; repeated figures get identical groove errors. Resolution: one phrase-level curve + small per-note offsets, decorrelate, suppress variation on repeated-note runs | fixed-pending-Zag |
| 4 | I2 — Geometric-primitive vocabulary | img | f3b3 = five vertical bars (audio-visualizer look); f3b5 = recursive nested squares; f3n18 = stair-stepped dotted diagonals; f3n16 = LED-like rectangles | **F2**: hash-derived width/spacing/omission variation per primitive; long diagonals → overlapping `f3_band` + `f3_blotch` interruptions; nested squares get omitted levels + aspect changes | Motif-detector rates down; repeated-object spacing variance near-zero → deliberate nonzero | Objection: "organic interruption" becomes its own repeated motif; modular variation detectable. Resolution: bound per-brief, vary negative space too, not just RGB | fixed-pending-Zag |
| 5 | A2 — Scale-exercise composition, fragment length | aud | Code: melody = C-major pentatonic run up-down (bins 27,29,31,34,36,34,31,29,27) + block-chord bass + metronome kick every 8 frames. All pieces 2.6–3.1 s, 7–9 notes | none — compositional brief problem, not a synth defect | n/a | n/a — red-team note: longer generation changes the musical distribution; prefer framing/packaging fix unless product should emit complete pieces | open |
| 6 | I3 — 100% 1-pixel-sharp edges (mechanical rasterization) | img | All 7 geometric images: fraction of strong edges that are 1px transitions = **1.00** | **F3**: use existing `f3_rect(..., soft)` with `soft = 2 + (f3_hash2(x0,y0,seed) % 4)`; select edges by **structural role** (occluded/interior soft, silhouettes/anchors stay sharp), not a fixed % | 1px-sharp fraction 1.00 → 0.45–0.65 with continuous width distribution | Objection: fixed-% softening → arbitrary blur placement + bimodal edge-width population. Resolution: role-based selection, continuous narrow softness range, keep genuine sharp edges | fixed-pending-Zag |
| 7 | V3 — v2 near-static (a "video" that's a still) | vid | v2 mean frame diff 0.65/255; **14/23 transitions < 1.0/255**; f0–f23 diff only 4.55 | **F12**: in `f3_gen_v2`, phased structure (frames 0–4 establish, 5–15 move/reveal, 16–23 settle); frame-indexed band/gradient/subject params | Near-static transitions → ~0; min frame diff > 2.0/255 during active motion | Objection: hard phase boundaries = visible temporal seams; diff-target forces fake background motion after subject stops. Resolution: continuous interpolation between phases; apply diff target only during travel interval | fixed-pending-Zag |
| 8 | I4 — Dead-center composition | img | Visual-mass centroid in 0.45–0.55 (both axes) on **11/14** images | **F4**: scene-level horizontal bias in `ig_place` + major `field.zag` raster calls (dominant elements 0.6×, secondary 0.25×, some background unshifted), from `f3_hash2(scene_id, brief_id, seed)` | Centroid x 0.45–0.55 → spread 0.30–0.70; target < 4/14 remain in dead-center band | Objection: reads as "centered template + predictable displacement". Resolution: vary bias direction/magnitude per scene; leave some elements unshifted so it reads as intentional imbalance | fixed-pending-Zag |
| 9 | A3 — Flat dynamics | aud | Per-note peak CV = **0.154** (human ≈ 0.2–0.4). Code: every melody note energy=700, atk=1, dec=2 — literally constant | **F7**: hash-shaped gain (0.90–1.14×), attack/decay scaling on `f3_tone`/`f3_sweep`/`f3_harm` args in `f3_gen_song` | Peak CV 0.154 → 0.25–0.35, phrase-shaped | Objection: correlated loud+sharp+long notes sound mechanically linked; risk of clipping against the ±24000 limiter. Resolution: one phrase-level swell curve + per-note 0.96–1.06×; decorrelate attack/decay/gain; reduce aggregate level headroom first | fixed-pending-Zag |
| 10 | I5 — Absurd color-count spread + quantization fingerprint | img | Unique colors 2 (f3n15) … 42,620 (f3n11). 96%/98%/85% of channel values divisible by 8 in f3b3/f3n16/f3n17 (posterization) | **F5**: post-pass palette bands in `f3_build` (flat 16–64, painterly 128–1024); uneven channel steps (5/7/9/11, never `& 248`); `f3_dither` clamped to palette | Color counts cluster in deliberate bands; values %8==0 → < 25–40% | Objection: clamped dither → patterned halos; palette bands become their own classifier feature. Resolution: per-brief band tuning; hash tie-breaking in quantization, not uniform masks | fixed-pending-Zag |
| 11 | A4 — Sterile mono, dry, surgical voice separation | aud | Mono, zero room/reverb; voice separation **19.8 / 31.1 dB** | **F8**: deterministic room (short early reflections), per-event pan (−0.75…0.75), crossfeed in `f3_synth_hifi`; voice-dependent baseline positions | Separation → ~10–18 / 18–26 dB; nonzero room signature | Objection: per-event pan jumps = notes hopping between speakers; moving-room signature; hash-correlated loud+far-side notes. Resolution: fixed room per phrase; narrow pan for exposed melody; wide pan only at phrase boundaries | fixed-pending-Zag |
| 12 | I6 — Subject-less noise fields | img | f3b2/f3n12 = texture only; f3n11 reads as "corrupted JPEG / bad TV signal" (diagonal noise, H-sym 0.252) | none designed — needs compositional briefs with subjects, not a raster tweak | n/a | n/a | open |
| 13 | V2 — Unstructured pixel change, no motion path | vid | v1 mean frame diff 7.14/255 but zero coherent flow; f0–f23 diff 149.6 with no narrative arc | **F11**: fixed eased path (left→right + vertical arc) over 24 frames in `f3_gen_v1`/`f3_gen_v2`; rigid subject translation; secondary event tied to scene position | Optical flow spatially coherent, persisting 3+ frames; change concentrated at subject boundary | Objection: rigid translation = "sliding sticker"; 8fps easing collapses to teleport/brake artifacts; frame-10–14 event reads as scripted beat. Resolution: velocity-profile (not just position) easing; scene-coupling cues (contact shadow, occlusion); trigger event by position, not frame number | fixed-pending-Zag |
| 14 | A5 — Exact 12-TET, zero drift | aud | By construction: bin b = 110·2^(b/12) Hz; no pitch deviation anywhere | **F9**: ±1.5 cents/note hash microtuning + ±1 cent slow phrase drift, 12-TET base preserved; applied in `f3_gen_song` before `f3_tone` (never touch `sin_lut.zag`) | 0 → bounded ±1.5 cents/note | Red-team verdict: **safe to ship as-is** at this depth (only objection: beating in exposed unisons — keep bounds tight) | fixed-pending-Zag |
| 15 | A6 — Round-number peak-limiter fingerprint | aud | Peaks exactly **+24000** (f3song_hifi, f3mood_happy, piece_B) / **−24000** (f3mood_calm, piece_A) | none designed | n/a | n/a | open |
| 16 | I7 — Saturation presets (0.0 vs ~0.99) | img | f3b5/f3b6 sat = 0.000 (grayscale); f3b3/f3n16/f3n17 sat = 0.958–0.994 | none designed (partially covered by F5 palette bands) | n/a | n/a | open |
| 17 | V4 — No shot structure (no setup/action/endpoint) | vid | 3 s clips start/end arbitrarily; no loop closure; no cuts or beats | Partial: F10–F12 phases impose establish/move/settle | n/a | n/a | fixed-pending-Zag (partial) |
| 18 | A7 — Invariant timbre/envelope across notes | aud | Inferred from code (identical atk/dec/br per voice); **suggested measurement**: per-note normalized waveform correlation + spectral centroid/attack-slope comparison | none (timbre rebuild is the sine-LUT track's job; F7 varies envelopes only) | n/a | n/a | open |
| 19 | I8 — 240×240 icon-like canvas | img | All 14 images 240×240; PREREG bar: hero images ≥ 480×480 | none — format decision for Micah | n/a | n/a | open |
| 20 | V5 — 8fps / 240×240 / 3 s format limits | vid | Both videos | none — red-team consensus: content first, format later (smoother static is still static) | n/a | n/a | open |

## Fix catalog (Zag-concrete handoff for the implementing worker)

All fixes: deterministic, `f3_hash2`-based pseudo-variation only, byte-identical reruns, pure Zag. All were red-teamed; refinements below are **adopted** (ship the refined version, not the naive one).

**F1 — Break mirrored-copy correspondence** (`imagine.zag` @ `ig_zmirror` call sites ~524, 1266–1269 → `ig_place` in `scenes_inc.zag`).
Keep `ig_zmirror(z)` for the destination zone; perturb only the mirrored copy's `a1..a8` before `ig_place`. Adopted refinement: relational adjustments, not independent jitter — one small local occlusion, edge interruption, or color-area change per mirrored pair; preserve shared major-axis alignment; stay below misregistration threshold.
```zag
h = f3_hash2(element_id * 37 + kind, mirrored_zone * 19 + dom, scene_seed)
// apply to at most 1-2 secondary properties, e.g. a local blotch occlusion or edge break
```

**F2 — Break geometric-primitive vocabulary** (`f3_build` → `f3_novel` and geometric branches, `field.zag`).
Per-primitive hash variation: `width = base + (f3_hash2(index, layer, seed) % width_var)`; vary spacing, omit levels, change aspect ratios; long diagonals → overlapping `f3_band` + `f3_blotch` interruptions; vary negative space, not just RGB. Bounded per brief.

**F3 — Eliminate 1px edges** (geometric `f3_rect` call sites, `field.zag`).
`soft = 2 + (f3_hash2(x0, y0, seed) % 4)` on structurally selected edges: occluded/interior/brush-facing boundaries soften; silhouettes and high-contrast anchors stay sharp. Continuous narrow softness range; never a fixed global percentage.

**F4 — Off-center composition bias** (`ig_place` in `scenes_inc.zag` + major `f3_blotch`/`f3_band`/`f3_rect` calls in `field.zag`).
Scene-level `composition_dx = -max_shift + (f3_hash2(scene_id*29, brief_id*13, seed) * 2*max_shift)/1000`; dominant elements ×0.6, secondary ×0.25, some background unshifted; per-element hash decorrelates exact translation; clamp to canvas. Vary direction per scene.

**F5 — Palette pipeline** (post-pass in `f3_build`, `field.zag`; modify `f3_dither`).
Brief-specific palette bands (flat 16–64, painterly 128–1024, textured bounded); quantize to nearest palette color with `f3_hash2(x,y,seed)` tie-breaking; uneven channel steps (5/7/9/11 — never `& 248`); dither chooses between palette entries, clamped; palette entries hash-perturbed off multiples of 8.

**F6 — Structured onset timing** (`f3_gen_song`, `field.zag`, before `f3_tone`/`f3_sweep`/`f3_harm`).
Adopted refinement: one phrase-level timing curve + small per-note offsets (≤ ~6 ms), sign/role-aware (pickups lead, cadential notes lag); shift event end by same amount; decorrelate from velocity/pan hashes; suppress on repeated-note runs and ornaments.

**F7 — Hash-shaped dynamics** (`f3_gen_song` event args `e`/`atk`/`dec`/`br`).
Adopted refinement: phrase-level swell curve × per-note 0.96–1.06 gain; attack/decay/tuning drawn from *independent* hash seeds; accents at structural beats by rule, not hash; keep aggregate headroom below the ±24000 limiter.

**F8 — Deterministic room + voice interaction** (`f3_gen_song` spatial metadata; `f3_synth_hifi` mix).
Adopted refinement: one fixed early-reflection pattern per phrase (not per event); exposed melody panned narrow around its assigned position; wider pan only at phrase boundaries/entrances; crossfeed scaled to avoid event-by-event localization jumps.

**F9 — Bounded microtuning drift** (`f3_gen_song`, before frequency bins reach `f3_tone`).
±1.5 cents/note + ±1 cent slow phrase drift from `f3_hash2`; 12-TET base preserved; interpolate across sustained notes; never touch `sin_lut.zag`. Red-team: safe as specified.

**F10 — Persistent foreground subject** (`f3_gen_v1`/`f3_gen_v2`, `field.zag`).
Fixed silhouette (20–35% frame) from `f3_rect` + `f3_blotch` with 2–3 internal regions; identical geometry every frame; hash texture low-amplitude and subordinate. Adopted refinement: scene integration required — contact shadow, occlusion by foreground/background, lighting response — or it ships as a sticker.

**F11 — Eased motion path** (per-frame loop in `f3_gen_v1`/`f3_gen_v2`).
Fixed left→right path + vertical arc; ease via *velocity profile* (bounded accel/decel), not position-only easing; hold at start, settle at end; rigid `(dx,dy)` translation; secondary event triggered by subject *position*, plus scene-coupling cues (shadow/occlusion/scale-with-depth).

**F12 — v2 phase structure** (`f3_gen_v2`).
Continuous interpolation between establish/move/settle phase parameters (no hard cuts); frame-diff target (>2.0/255) applies only during travel; moving bands/gradients decelerate with the subject and stop cleanly.

## Positive model: what "human-made" looks like (target, not just tell-removal)

From the human-reference study — the Zag worker should aim *toward* these, since pure tell-removal leaves a detectable "remediated" signature (see blind re-attack):
1. **Deliberate imperfection** — irregularities that feel chosen (one awkward interval, an interrupted contour), not uniformly distributed noise.
2. **Asymmetry of intent** — balance present but one area more resolved/emotionally charged; correlated across features, not independent jitter per element.
3. **Evidence of revision** — pentimenti: partially buried shapes, softened former edges, abandoned compositional decisions visible at focal points.
4. **Focal hierarchy** — eye guided to a few dominant relationships; secondary marks support rather than compete.
5. **Micro-variation in marks** — repeated shapes vary in pressure/width/spacing while belonging to one visual language.
6. **Compositional tension** — near-alignments, almost-touches, uneven counterweights.
7. **Material-specific texture** — grain/drag/pooling that behaves like a *particular* medium, not generic hash noise.
8. **Meaningful edge quality** — crisp/feathered/eroded edges serving depth and emphasis.
9. **Audio: expressive timing + uneven dynamics + breath/hesitation** — small musically-structured deviations, phrase hierarchy, pauses before important entries.
10. **Audio: coherent non-uniform phrasing** — motifs recur with identity while endings/ornamentation change.

**Anti-patterns (do NOT do):** uniform noise/jitter everywhere (procedural filter look); one conspicuous planted "mistake" (reads as AI disguise); stacking many incompatible human signatures (checklist of stereotypes); optimizing metrics instead of composition (blind analyst *will* notice the 40–70% edge ratio and the <0.60 symmetry target as new fingerprints).

## Blind re-attack findings (fresh analysts, NOT shown the fix list)

After describing the post-fix artifacts, blind red-teams found these residual risks — the implementing worker must design verification against them:

**Images — strongest single test:** cross-image multiscale residual fingerprint. Strip low-frequency fields + fitted motifs from all 14 images, then compare high-frequency residuals (spatial autocorrelation, Fourier power by orientation, bit-plane stats, cross-image residual correlation at normalized coordinates). A shared hash-residual signature across the set is the decisive catch. Supporting tells: bimodal edge-width populations (untouched 1px vs softened 2–5px); palette-band jitter (values avoiding multiples of 8 *is itself* evidence of an anti-quantization pass); bounded motif perturbations over a shared scaffold (Hough/fit analysis); metric-optimized distributions (symmetry/centroid values suspiciously avoiding old ranges).

**Audio — strongest single test:** event-level multivariate residual fingerprint — [grid offset, cents error, normalized peak, duration, pan feature, reflection gains], rank-normalized, tested for cross-feature dependence and cross-clip tuple recurrence vs a permutation baseline. Catches: one hash feeding many parameters (timing+velocity+tuning+pan moving together); hard distribution edges at 3–12 ms / ±1.5 cents; identical early-reflection templates restarting per event; fixed ~14/22 dB separation floor.

**Video — strongest single test:** motion-compensated template persistence. Affine-register the silhouette from every frame to a reference; near-zero interior residuals across all 24 frames (especially through the frames 10–14 event) = a moved asset, not a rendered subject. Catches: trajectory fitting an easing function too well (tiny Bézier residuals, symmetric accel); hard-coded temporal landmarks (events at the same frame numbers across videos); motion isolated to a narrow boundary band with unchanged interior.

## Measurement log (this worker's own verification)

- Converted 14 BMP → PNG (PIL), viewed 8 directly; extracted 24 raw-RGB24 frames from each AVI by manual RIFF parsing (no cv2 on this VM); analyzed 7 WAVs with numpy.
- **Corrections:** an early onset-grid script had a min/max bug claiming "0.00000 s deviation" — corrected measurement: onsets at 245/727/1228/1718/2244 ms, IOIs 482/501/490/526 ms; code ground truth (`f3_gen_song`) confirms exact integer-frame placement (frames 0,4,8,…,32). Timing tell stands, evidence corrected.
- **Negative results (ruled out):** no exact wavetable-loop periodicity (autocorr < 0.999 at all lags); no duplicated 100 ms sample blocks; no temporally mirrored frame sequences; no exact duplicate frames; texture autocorrelation decays smoothly (no repeated kernel — the noise generator is fine).
- **New tells found by measurement:** 100% 1px-sharp edges on all 7 geometric images; 85–98% channel values divisible by 8 (f3b3/f3n16/f3n17); V-symmetry 0.964 (f3n18), 0.882 (f3n16), −0.868 (f3n14); centroid clustering 11/14 in 0.45–0.55; exact ±24000 peak limiter; `f3_gen_song` is a pentatonic scale exercise with identical per-note energy.
- Sol's "most human-like" pick (f3n11, low symmetry) disagrees with the PREREG note (f3n14, sunset-blob); recorded as judge disagreement, not resolved — both carry tells.

## Top 5 fixes to hand to the Zag worker (detectability reduction per effort)

1. **F1 (+refinement)** — mirror-perturbation at `ig_zmirror` call sites: kills the #1 tell (H-sym → <0.60), central 2-line change area.
2. **F4** — off-center composition bias in `ig_place`: fixes 11/14 centered images in one place.
3. **F6 (+refinement)** — structured onset timing in `f3_gen_song`: cheapest big audio win (event-list only, no synth changes).
4. **F3 (+refinement)** — role-based edge softening via existing `f3_rect(..., soft)`: removes the 1.00 1px-edge fingerprint.
5. **F10 (+refinement)** — persistent subject + scene integration in `f3_gen_v1`/`f3_gen_v2`: turns "animated static" into a watchable clip.

## FALLBACKS

- **2026-09-22 ~06:50 UTC (hard stop): grok-4.7 via ExperimentalLabs exhausted platform credits (HTTP 429 `insufficient_credits`, balance −$0.02).** First probe 23:28 PDT returned the 429; one long prompt SIGTERM'd at 90 s before the cause was known. Per the parent hard-stop directive, **zero** experientiallabs calls were made after diagnosis. All reasoning in this task (14 calls) went through **gpt-5.6-sol via UnoRouter** (`python3 ~/workspace/skills/unorouter/bin/unorouter.py chat … --model gpt-5.6-sol`), per Micah's standing fallback order. Labeled-section prompting (no verbatim demands, no JSON) carried over unchanged.
- **UnoRouter flakiness:** intermittent `choices: null` completions (3 prompts failed 4 retries each over ~200 s, then succeeded on later retry; no correlation with prompt length — 439–577 tokens failed while longer ones passed). Built `/tmp/tellhunt/ucall.py` (retry wrapper, 4 tries, exponential backoff, saves to file) — recommend the night crew reuse it.
- **No fallbacks needed for:** measurements (all local Python/PIL/numpy), artifact viewing, Zag source reading.
- **Open measurement gaps for the next worker:** A7 per-note timbre correlation (needs the metric before any fix); blind-packet growth; re-render + re-measure loop after F1–F12 land.
