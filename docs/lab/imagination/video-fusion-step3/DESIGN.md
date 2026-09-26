# STEP 3 — REALISTIC FUSION: Design

Date: 2026-09-26. Extends the Step-2 pure-Zag composer (`video-composer`) with a
**fusion organ**: part-level segmentation → part correspondence → realism
adaptation → temporally tracked synthesis. Same pinned compiler
(`znc_linux_x86_64_abed8aa1`), zero RNG in all decision paths.

## What was wrong with Step 2

Step 2's VERDICT was honest: genuine deliberation, but the winning plan was a
bunny-face corner sticker. Root cause: the plan language had no part-level
vocabulary (only whole-frame overlays/PIP/splits), and the rubric rewarded
preservation over transformation. Step 3 adds a part-level plan language:
segment parts, pick a donor part and a recipient slot, adapt, synthesize.

## The fusion organ (`src/chunks/fz1–fz4.zag`, assembled into `fusion.zag`)

New subcommand: `fusion_bin fuse <workA> <workB> <instr> <outdir>`.
All Step-2 subcommands (ingest/recall/compose/render/…) are preserved.

### 1. SEGMENT — three generic candidate strategies per memory

For each memory, from the middle frame plus full-sequence motion:

- **C1 — motion subject**: per-pixel motion energy E = Σ|gray(f+1)−gray(f)| over
  all 24 frames; mask = E > 85th percentile; largest connected component.
- **C2 — dark quintile part**: mask = gray < 20th percentile of the middle
  frame, 3-iteration morphological opening, hole filling, largest component.
- **C3 — bright quintile part**: mirror of C2 at the 80th percentile.

Every threshold (85th motion percentile, 20th/80th gray percentiles) is
**measured from the memory's own data**, not a constant. The trace records all
three candidates with area, bbox, centroid, motion-concentration
(ΣE inside / ΣE total), compactness (area / bbox area), and the score:

> score = motion_concentration × compactness

The subject is the argmax. Validity is enforced mechanically: candidates that
are tiny, fragmented, or border-dominated score near zero and lose openly.

### 2. CORRESPOND — direction + part mapping

- **Direction** (which memory hosts): recipient = argmax **subject centrality**
  (400·10000/(400+dist(centroid, frame center))). The more central subject is
  the more complete scene; the other memory donates a part. Measured, traced.
- **Donor part**: the donor memory's own subject (already part-level under its
  segmentation — e.g. the pig's dark head+shoulder region).
- **Recipient slot**: the recipient's motion subject is split by a **neck-line**
  — the minimum-motion row between the two strongest motion peaks in the
  subject's bbox (falls back to the vertical midpoint, recorded). Head vs body
  is decided by argmax **texture × upperness** (gradient-texture mean times
  (H−cy)/H). The slot is the winning part's bbox.
- **Anchor**: the recipient's saliency focus (Step-2 `perceive`) rect center —
  where the face is.

### 3. ADAPT — background, seam, lighting, shadow

- **Per-channel gain**: donor-part mean RGB vs recipient-slot mean RGB;
  gains clamped to [0.5, 3.0] so the donor keeps its identity (the clamp event
  is traced; the residual gap is reported, not hidden).
- **Light-direction gradient**: background = low-motion pixels (E < median);
  top-third vs bottom-third mean gray gives a vertical light tilt applied to
  the graft.
- **Seam**: graft alpha = donor mask → 17×17 box blur (8 px feather ramp);
  edge transfer shifts graft band pixels toward recipient band colors.
  Self-check metric: mean |graft − recipient| in the blend band, before vs
  after (raw=158 → adapted=72 on this test).
- **Shadow**: contact shadow below the graft; strength from background
  contrast (bg_q25 vs bg mean).

### 4. SYNTHESIZE — temporally tracked

- The donor part is centroid-tracked per frame (dark-threshold tracking in a
  dilated ROI); the drift is recorded as **part-selection evidence** (a bobbing
  part reads head-like).
- The graft **rides the recipient head's motion** (bright-pixel tracking in the
  slot ROI), because it replaces the recipient's head. An earlier revision rode
  the donor's motion and detached the graft from the face at high drift — the
  trace records the fix and the reasoning.
- 24 frames, alpha paste + shadow per frame, written as PPM.

### Refusals (honest scope)

Refuses when: not two 320×240×24 videos; verb not MERGE-class or not two
subjects; donor subject not the dark-part candidate; donor part < 500 px.
Refusals are written as `fuse_refusal.txt` with reasons.

## What "head" means here (read this before judging)

The organ has no semantic object recognition. "Head" is an operational proxy:
upper + high-texture part of the motion subject (recipient), dark + high-drift
part of the dark quintile (donor). The trace states this plainly. If the proxy
fails on some video pair, the trace — not a label — is where you'll see it.

## Determinism

Runs A and B: trace byte-identical, all 24 frames byte-identical
(`metrics/SHA256_A.txt`, `metrics/SHA256_B.txt` diff clean).
