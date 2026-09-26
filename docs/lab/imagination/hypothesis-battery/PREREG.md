# PREREGISTRATION: Hypothesis Battery on Why Fusion Keeps Failing

**Ordered by:** Micah, 2026-09-26 ~10:01 PDT
**Frozen:** 2026-09-26 (this commit — before any test is run)
**Scope:** Diagnosis only. Step 6 (neck-anchored warp, cross-view) is the forward
build and is NOT touched. This battery explains the step-5 failure
(commit 9d4d83119a42, "still a sticker").

## Background (what step 5 established)

- Anatomy (PROPOSE side) works: snout=(63,220) at the true nose, facing picked by
  neck prominence (5.7x vs 3.8x), measured neck cut d_neck=154, head=6529px whole
  black head. Verified honest.
- Merge (SYNTHESIZE side) fails: centroid-anchored 2D warp, cross-view
  (side-view pig → front-view bunny), cov=551/1024 even at 1.5x "cover" scale,
  bunny's face visible below the blob.
- Baseline numbers this battery measures against (step-5 trace):
  cov=551/1024, iou=199/1024, slot=(124,0)-(215,104), neck line y=105,
  10/24 frames valid after gates.

## Shared metrics (all white-box, from the machinery's own numbers)

- `cov` — slot-mask pixels covered by the warped donor head, x/1024 (step-5: 551)
- `iou` — IoU(warped donor head, slot mask), x/1024 (step-5: 199)
- `neck_err` — px distance from the donor neck point mapped through the warp to
  the recipient neck target (neck line y=105 at slot center x). Computed exactly
  in the probe by replicating the warp math.
- `prom` — neck prominence x/1024 (step-5 frame 12: 5666)
- All probe executables are pure Zag, zero RNG; every probe run is executed
  TWICE and the outputs compared byte-identical (SHA-256 recorded).

## Effect-size conventions (preregistered, apply to all)

- A mechanism change is MEANINGFUL iff |Δcov| ≥ 100/1024 (~10pp) or
  neck_err changes by ≥ 20px.
- A limiter is CONVICTED iff its removal/improvement moves a metric by a
  meaningful amount in the direction of fixing the sticker.
- A limiter is EXONERATED iff its removal changes no metric by a meaningful
  amount (|Δcov| < 50/1024 AND Δneck_err < 10px).
- A hypothesis is KILLED iff its preregistered kill observation is met.
  Otherwise it is KEPT (possibly weakened — documented).

---

## H1 (MICAH'S): "it's not conscious about it"

**Statement:** The merge machinery has no representation of the scene as a
coherent 3D arrangement of anatomical parts. It pastes 2D textures without any
model of depth ordering, occlusion, or what lies behind visible surfaces.
Fusion = sticker because there is no "it" there — no 3D body the head belongs to.

**Tests (all three must be run):**

- **H1a — cross-frame anatomical consistency.** Probe `anatomies`: run the
  unmodified `v4_anatomy_frame` on all 24 donor frames; record per frame:
  valid, snout (px), donor centroid, facing (x1024), d_neck, prom, area,
  neck point. Measure: (i) snout-vs-true-nose deviation on valid frames
  (true nose located once by inspection on the stabilized frame_90 dump);
  (ii) facing flips between adjacent valid frames; (iii) prom < 2048 cases.
- **H1b — representation audit (white-box).** Inspect the full step-5 source
  (fusion4.zag + chunks, 11,820 lines) and the lmf 16-qword contract for ANY
  encoding of: depth ordering (which part is in front of which), occluded
  structure (what exists behind the neck / behind the head), or a 3D body
  model. Document every hit or the certified absence.
- **H1c — the tuck test (behavioral).** A 3D-aware head swap tucks the donor
  neck BEHIND the recipient's neck/body (occlusion at the join). Inspect
  `v4_composite`: does any code path place graft pixels behind recipient
  pixels? Measure the neck-band overlap: fraction of the donor head's neck
  region (d_neck ± 20px band) that the composite pastes OVER the recipient's
  body region (below neck line y=105).

**KILL BAR (preregistered):** H1 is KILLED iff the machinery demonstrably
maintains a 3D-consistent body model, i.e. ALL of: (a) snout within 5px of the
true nose on ≥8/10 valid frames AND zero facing flips AND prom ≥ 2048 on all
valid frames (3D-consistent tracking); AND (b) H1b finds an explicit
depth/occlusion representation in the records or code; AND (c) H1c finds a
tuck/behind mechanism in the compositor. If any of (a)/(b)/(c) fails,
H1 is KEPT.

---

## H2 (MICAH'S): "some external force is limiting it"

**Statement:** The sticker is caused by one or more external limiters, not the
core idea: the 2D warp, the slot machinery, the fixtures (shaky pig clip),
the znc toolchain. Each limiter gets its own ablation with its own
convict/exonerate bar. A limiter whose removal changes nothing is exonerated —
said plainly.

- **L1 — centroid anchoring (the 2D warp).** Ablation `neckplace`: keep
  everything identical but replace the centroid-anchored affine warp with a
  neck-anchored rigid placement (translate donor neck point → recipient neck
  target, scale = s_sim). Measure Δcov, Δiou, neck_err (→ ~0 by construction).
  CONVICT anchoring as a limiter iff neck_err drops ≥ 20px AND |Δcov| ≥ 100/1024.
  EXONERATE iff |Δcov| < 50/1024 and the residual sticker metrics are unchanged.
  (Note: this ablation is diagnostic; step 6 owns the real neck-anchored warp.)
- **L2 — slot machinery.** Ablation `slotvar`: measure the neck line from the
  first 12 recipient frames vs the last 12 (independent `v4_slot` runs).
  CONVICT iff the two neck lines differ by > 5px or either slot bbox differs
  by > 10px per side (slot machinery unstable → contributor).
  EXONERATE iff neck lines agree within ±3px and bboxes within ±5px.
- **L3 — fixture shake (shaky pig clip).** Ablation `shake`: run
  `v4_anatomy_frame` with stabilization ON (cum as measured) vs OFF (cum
  zeroed); measure median snout displacement across valid frames and the
  change in valid-frame count. The pipeline already stabilizes
  (shake_max=44, residual 24→20, use_stab=1).
  CONVICT shake as a live limiter iff median snout displacement > 10px or
  valid count changes by ≥ 3. EXONERATE iff median displacement < 5px and
  valid count unchanged (stabilization already handles it).
- **L4 — znc toolchain.** Audit + numeric cross-check. (i) Grep the
  measurement chain (`v4_snout`, `v4_neckcut`, `v4_moments`, `v4_eigenvec`,
  `v4_anatomy_frame`, `v4_head_region`) for known-bad patterns from the
  program's bug ledger: `as []i32`/`as []u32`/`as []u16` casts used with
  indexing, `.*` applied to non-pointer operands, `(1 as i64)<<` inside `&`
  tests, chained `s.field.subfield` access. (ii) Independent Python
  recomputation of d_neck and prom on frame 12 from the dumped dark mask
  (frame_91) and head mask (frame_92).
  CONVICT iff a known-bad pattern is live in the measurement chain AND the
  Python cross-check disagrees by > 2px. EXONERATE iff no live bad patterns
  and the cross-check agrees within 2px.
- **L5 — view mismatch.** Shared with H5 (below); H2 records its verdict.

**KILL BAR (preregistered):** H2 as a whole is KEPT iff ≥1 limiter is
CONVICTED. H2 is KILLED iff ALL of L1..L4 are EXONERATED and H5 is killed
(no external limiter explains a meaningful share of the sticker).

---

## H3 (crew's): the composition frontier

**Statement (from the alignment synthesis):** "propose through synthesize is
the unsolved step-2 frontier" — parts are proposed fine; the failure lives
specifically in the SYNTHESIZE step (pose warp + photometric + composite),
not in PROPOSE (anatomy + slot).

**Tests:**

- **H3a — near-oracle propose.** The step-5 propose output is already
  near-oracle (verified: snout at true nose, measured neck, whole-head mask).
  Probe `neckplace` additionally feeds the VERIFIED neck point and the
  verified head mask into the CURRENT synthesize and measures cov/iou/neck_err
  vs the step-5 baseline. If the failure persists with near-oracle proposals,
  it localizes to synthesize.
- **H3b — oracle synthesize (best-case 2D composition).** Neck-anchored
  placement + identity photometric (T2, tex=1024) + verified mask: the best a
  2D composition can do. Measure cov/iou and the residual that even the oracle
  cannot fix (cross-view shape mismatch).

**KILL BAR (preregistered):** H3 is KEPT iff with near-oracle proposals the
synthesize metrics stay bad (cov < 650/1024 OR neck_err ≥ 20px) — failure
localizes to synthesize — AND the oracle-synthesize still cannot cover the
slot (cov < 700/1024), pinning the frontier at/below 2D composition.
H3 is KILLED iff near-oracle proposals fix the merge (cov ≥ 800/1024 AND
neck_err < 10px) — the frontier was propose after all.

---

## H4 (crew's): anatomy knowledge gap

**Statement:** The failure is a knowledge gap about anatomy, not machinery:
TNN doesn't know heads well enough. Giving it part-level head knowledge
(ears/eyes/snout as substructures) will improve the merge.

**Test — probe `parts`:** add part-level substructure detection to the donor
model, reusing the verified head mask: ear tips = the two farthest-apart
mask protrusions above the snout–neck axis (extremal points of the mask in
the upper half); eyes = the two darkest compact blobs inside the head
interior (darkness minima with local support). Record them as an extended
landmark set, then place with part-aware anchoring (ear tips → slot top
corners, snout → below centroid) and measure: Δcov vs baseline, and
part-separation = mean pairwise warped distance between ear-tip/eye/snout
landmarks normalized by warped head size (baseline: blob → collapsed).

**KILL BAR (preregistered):** H4 is KILLED iff adding ear/eye/snout
substructure knowledge moves cov by < 100/1024 AND part-separation does not
improve (landmarks remain collapsed into the blob) — knowledge wasn't the
gap. H4 is KEPT iff cov improves ≥ 100/1024 or parts become recognizably
separated after the warp.

---

## H5 (crew's): view-mismatch is the WHOLE story

**Statement:** Same-view donor input would just work. The sticker is entirely
the side-view-pig → front-view-bunny mismatch; fix the view, fix the fusion.

**Test — probe `viewcov`:** per-frame frontality score for all valid donor
frames: frontality = lam2/lam1 (x1024; rounder head = more frontal) combined
with facing angle. Rank frames; take the most-frontal ("closest-view-matched")
frame and measure its cov/iou/neck_err through the current pipeline geometry.
Correlate frontality vs per-frame best-case coverage across valid frames.

**KILL BAR (preregistered):** H5 is KEPT-as-complete iff the most
view-matched frame reaches cov ≥ 800/1024 AND neck_err < 10px (matching the
view fixes it). H5 is KILLED-as-complete iff substantial sticker-ness remains
at the best-matched view (cov < 700/1024 OR neck_err ≥ 20px) — view mismatch
is then at most a partial contributor, and the residual is quantified.

---

## Commit sequence (preregistered)

1. This PREREG.md — committed BEFORE any probe is built or run.
2. Probe sources + build log (determinism: two byte-identical runs each).
3. VERDICT.md — the scoreboard with numbers; each hypothesis KEPT/KILLED by
   its bar above. Evidence: probe logs (SHA-256), measurement tables.

All commits to `tnn-native-lab`, never main. No step-6 files touched.
