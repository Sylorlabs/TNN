# STEP 3 — VERDICT: honest assessment of the fusion

Test: "merge the pig and the bunny together", 24 frames @ 8 fps, 320×240,
full 3 s. Judged on full frames and full duration.

## What TNN decided (its own measured reasoning)

**Segmentation** (three generic candidates per memory, score =
motion-concentration × compactness, all thresholds measured from the data):

| memory | C1 motion-subject | C2 dark-quintile | C3 bright-quintile | subject |
|---|---|---|---|---|
| bunny | score **1297** (area 7788, centroid (181,86)) | 10 | 6 | **C1** |
| pig | 142 | score **159** (area 4050, bbox (74,49)–(150,151)) | 109 | **C2** |

**Correspondence**: recipient = argmax subject centrality → **bunny** (9111 >
8810). Donor = pig, part = its C2 subject. Recipient neck-line at row 101;
head beats body 106–25 on texture×upperness → **slot = HEAD**, anchor (159,120)
from the saliency focus. Donor graft 130×173 @ 1.68× width-matched scale.

**Adaptation** (all measured): per-channel gains 3.0×/3.0×/3.0× (clamped from a
~6× measured ratio; clamp event traced); light-tilt ratio 257/256 (scene
measured nearly flat — reported, not invented); shadow strength 33/256 from
background contrast; edge-transfer shift +(61,88,95) with 8 px feather.
**Seam self-check: 158 → 72 gray levels** (mean |graft−recipient| in the blend
band). Donor drift_y = 71 recorded as part-selection evidence; the graft rides
the recipient head's motion (drift 5,2) because it replaces that head.

**Determinism**: runs A/B byte-identical (trace + all 24 frames;
`metrics/SHA256_*.txt` diff clean).

## What it made

A 24-frame video in which the pig's dark head+shoulder region is grafted over
the bunny's face, bunny ears remaining above, temporally stable, with a
feathered seam and a faint contact shadow. Full MP4 + frames in the gallery.

## Verdict: NOT a realistic fusion — a softened, tracked graft

This is a genuine advance over the Step-2 corner sticker: the graft actually
replaces the head region, it is temporally glued to the recipient's head, and
the seam/lighting/shadow adaptations are real measured operations with a
before/after metric. But a judge with full eyes still sees composited
segments. The exact mechanical boundaries, in order of visual weight:

1. **Part impurity (biggest).** The donor segment is head+shoulder
   (77×103 px), not a head. No valid neck split exists in the donor's motion
   field: camera shake dominates the pig's motion energy (mean 25.54 vs
   bunny 4.43), so the neck operator finds only shake peaks and the mechanism
   refuses them rather than faking anatomy. Result: the graft reads as a dark
   mass, not a distinct head — no snout, eyes, or ears resolve.
2. **Photometric gap.** Donor mean RGB (27,24,27) vs recipient slot
   (164,190,215): ~6× luminance gap. Gain clamped at 3.0× to preserve donor
   identity; edge transfer helps the band only. Residual seam = 72 gray
   levels — softened, plainly visible. A black pig head on a white bunny
   cannot be bridged by linear adaptation without destroying what makes it
   the pig's head; the trace reports the residual instead of hiding it.
3. **Pose.** Donor head pitched down-left vs recipient frontal. No pose
   normalization exists in the plan language (trace SELF_CHECK: unhandled).
4. **Frozen appearance.** The graft renders the f12 donor pose for all 24
   frames; the donor's bob is selection evidence, not rendered motion
   (trace SELF_CHECK: unhandled).

Nothing is faked: background tilt, lighting gain, and shadow strength are all
computed from measured scene statistics, and where measurement could not
bridge the gap the trace states the residual numerically. The honest summary:
**the fusion organ deliberates genuinely and adapts measurably, but its
output is a well-tracked composite segment, not a believable pig-headed
bunny.** Closing boundaries 1 and 2 needs head-only donor segmentation that
works under camera shake and identity-preserving photometric transfer beyond
linear gain — both are named, unbuilt, next steps.
