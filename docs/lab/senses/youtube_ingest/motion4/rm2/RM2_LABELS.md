# RM2 labels — genuine real-motion battery (hand-labeled 2026-09-24)

Labeling rubric (frozen B3_LABELS.md rubric + REVISION pair-level
vote-analysis procedure): each candidate viewed as frame0-vs-frame7
2x-upscale montage, plus an 8x8 per-block direction arrow map (7 pairs
overlaid). STILL = no discernible change. MOTION-<D> = clear uniform
translation, 8-way. AMBIG = zoom/expansion, rotation, cuts,
multi-motion, complex deformation, or any uncertainty (unsure -> AMBIG).
AMBIG excluded from scoring; distribution reported.

Pair-level vote analysis (numpy replica of frozen motion3.zag,
bit-verified against the verdict binary on 6 fixtures): for each of the
7 pairs, the winning direction bin; MOTION-D requires ≥5/7 pairs on one
direction AND whole-frame spatial coherence AND a clean viewing.
The viewing is the deciding gate — coherent votes on shimmer/sway
(OQSNhk5ICTI) or on waves (Eoo4HzILB-M) do not survive it.

Mining: 7-video corpus, baselines b in {2,3,4} (every 2nd/3rd/4th source
frame → 8-frame .vid, spans ≈16/24/32 source frames), candidate starts
every 15 source frames, scored by the replica; shortlist = top-2 motion
+ top-1 still-like per (video, baseline). Scripts in mining/.

## MOTION-D (11)

MOTION-E (6):
- rm2_uKNQCPXDNdc_b2_t3630 — forest camera pan E; whole-frame uniform
  translation; minor branch sway only. (7/7 pairs E)
- rm2_uKNQCPXDNdc_b3_t3615 — same forest pan, E. (7/7 E)
- rm2_uKNQCPXDNdc_b3_t3630 — same forest pan, E. (7/7 E)
- rm2_uKNQCPXDNdc_b4_t3615 — same forest pan, E. (7/7 E)
- rm2_uKNQCPXDNdc_b4_t3630 — same forest pan, E. (7/7 E)
- rm2_9AwUsf8HzVI_b3_t1695 — basketball camera pan E; court markings
  translate uniformly E; localized player motion. (7/7 E)

MOTION-W (4):
- rm2_9AwUsf8HzVI_b2_t0450 — basketball camera pan W; uniform W pan of
  court/crowd; localized player motion. (7/7 W)
- rm2_9AwUsf8HzVI_b2_t0465 — same play, W. (7/7 W)
- rm2_9AwUsf8HzVI_b4_t1740 — basketball camera pan W; uniform. (7/7 W)
- rm2_9AwUsf8HzVI_b4_t1755 — same play, W. (7/7 W)

MOTION-S (1):
- rm2_9AwUsf8HzVI_b3_t0285 — basketball camera tilt down S; uniform S
  translation of the frame; localized player motion. (7/7 S)

Note: camera-pan labels count as uniform translation (the frame-level
global motion is coherent translation); localized independent subject
motion does not veto the label. Where no coherent global motion exists
(deer, pedestrians), the label is AMBIG.

## STILL (6)

- rm2_OQSNhk5ICTI_b2_t3630 — rainbow scene, frame0≈frame7, weak
  incoherent pair votes.
- rm2_OQSNhk5ICTI_b3_t3615 — same, STILL.
- rm2_OQSNhk5ICTI_b4_t3615 — same, STILL.
- rm2_uKNQCPXDNdc_b2_t0000 — deer in forest, frame0≈frame7, zero votes.
- rm2_uKNQCPXDNdc_b3_t0000 — same, STILL.
- rm2_uKNQCPXDNdc_b4_t0060 — deer close-up, near-identical, zero votes.

## AMBIG (35)

Clouds/deformation (6): rm2_0_jNjpVxUt0_b2_t0465, rm2_0_jNjpVxUt0_b2_t0480,
rm2_0_jNjpVxUt0_b3_t0720, rm2_0_jNjpVxUt0_b3_t0765,
rm2_0_jNjpVxUt0_b4_t0705, rm2_0_jNjpVxUt0_b4_t0720 — timelapse clouds
drift N/NE coherently at the pair level but visibly deform between
frame0 and frame7 (B3b precedent applies).

Cloud shift, no coherence (1): rm2_0_jNjpVxUt0_b2_t0000.

Ocean waves (6): rm2_Eoo4HzILB-M_b2_t0195, rm2_Eoo4HzILB-M_b2_t0210,
rm2_Eoo4HzILB-M_b3_t0195, rm2_Eoo4HzILB-M_b3_t0210,
rm2_Eoo4HzILB-M_b4_t0180, rm2_Eoo4HzILB-M_b4_t0195 — breaking waves
shift E but are complex deformation; sky static (multi-region motion).

Atmospheric shimmer (6): rm2_OQSNhk5ICTI_b2_t1995,
rm2_OQSNhk5ICTI_b2_t2505, rm2_OQSNhk5ICTI_b3_t0075,
rm2_OQSNhk5ICTI_b3_t1995, rm2_OQSNhk5ICTI_b4_t0120,
rm2_OQSNhk5ICTI_b4_t5100 — arrow maps show radial/scattered votes
(shimmer, sway); 7/7 pair votes are misleading here; no coherent
translation survives viewing.

Pedestrians / multi-motion (9): rm2_bwJ-TNu0hGM_b2_t0000,
rm2_bwJ-TNu0hGM_b2_t1440, rm2_bwJ-TNu0hGM_b2_t1455,
rm2_bwJ-TNu0hGM_b3_t0000, rm2_bwJ-TNu0hGM_b3_t0675,
rm2_bwJ-TNu0hGM_b3_t1440, rm2_bwJ-TNu0hGM_b4_t0270,
rm2_bwJ-TNu0hGM_b4_t1425, rm2_bwJ-TNu0hGM_b4_t1440 — city street with
independently moving pedestrians; no coherent global motion (the t0000
windows show discernible pedestrian change despite ~zero block votes).

Deer walking (1): rm2_uKNQCPXDNdc_b2_t3480 — deer walks across the
frame; camera static; subject motion dominates, no global translation.

FPV drone (6): rm2_kcfs1-ryKWE_b2_t0615, rm2_kcfs1-ryKWE_b2_t0630,
rm2_kcfs1-ryKWE_b3_t1245, rm2_kcfs1-ryKWE_b3_t1260,
rm2_kcfs1-ryKWE_b4_t0615, rm2_kcfs1-ryKWE_b4_t0990 — forward/sideways
flight; arrow maps show expansion flow + parallax layers, not uniform
translation.

## Distribution

MOTION-D 11 (E 6, W 4, S 1), STILL 6, AMBIG 35. Baselines: b2 18,
b3 17, b4 17 clips. Labels frozen at this commit; no motion4 run has
seen them (motion4.zag does not exist yet).
