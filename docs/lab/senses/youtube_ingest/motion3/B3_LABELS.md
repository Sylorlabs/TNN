# B3 labels — real-footage battery (hand-labeled 2026-09-23)

Labeling rubric (PREREG_MOTION3.md §5): viewed frame0 vs frame7 side by
side (2x upscale, 4-up montages in work/b3_montage/). STILL = no
discernible change. MOTION-<D> = clear uniform translation, 8-way.
AMBIG = zoom/expansion, rotation, cuts, multi-motion, complex
deformation, or any uncertainty (unsure -> AMBIG). AMBIG excluded from
scoring; distribution reported.

## B3a — sampled windows (frozen sample: floor(i*W/8), i=0..7 per video)

REVISION 2026-09-23: pair-level vote analysis (independent Python
replica) showed the OQSNhk5ICTI "talking head" windows contain
substantial sub-perceptual pixel drift (whole-frame coherent votes,
E up to 517k per window) — they are NOT still at the pixel level.
Original STILL labels were from frame0-vs-frame7 eyeballing, which
missed it. Labels below reflect pixel-level ground truth:
- temporally+spatially coherent drift -> MOTION-D
- substantial but temporally incoherent motion -> AMBIG
- E~0 across all pairs -> STILL

STILL (12; verified E~0 on all 7 pairs):
0_jNjpVxUt0_w000
Eoo4HzILB-M_w000 Eoo4HzILB-M_w002 Eoo4HzILB-M_w004 Eoo4HzILB-M_w006
Eoo4HzILB-M_w008 Eoo4HzILB-M_w010 Eoo4HzILB-M_w012 Eoo4HzILB-M_w014
uKNQCPXDNdc_w015 uKNQCPXDNdc_w077 uKNQCPXDNdc_w093

MOTION-E (1):
OQSNhk5ICTI_w065
  (5/7 pairs vote E coherently, whole-frame spatial coherence;
   sub-perceptual drift — block-matcher-visible, not eye-visible
   in frame0-vs-frame7)

MOTION: no other B3a window met the clear-uniform-translation bar.
See B3b for real-motion detection tests.

AMBIG (43):
0_jNjpVxUt0_w003 0_jNjpVxUt0_w006 0_jNjpVxUt0_w010 0_jNjpVxUt0_w013
0_jNjpVxUt0_w016 0_jNjpVxUt0_w020 0_jNjpVxUt0_w023
9AwUsf8HzVI_w000 9AwUsf8HzVI_w007 9AwUsf8HzVI_w015 9AwUsf8HzVI_w022
9AwUsf8HzVI_w030 9AwUsf8HzVI_w037 9AwUsf8HzVI_w045 9AwUsf8HzVI_w052
bwJ-TNu0hGM_w000 bwJ-TNu0hGM_w017 bwJ-TNu0hGM_w034 bwJ-TNu0hGM_w052
bwJ-TNu0hGM_w069 bwJ-TNu0hGM_w086 bwJ-TNu0hGM_w104 bwJ-TNu0hGM_w121
kcfs1-ryKWE_w000 kcfs1-ryKWE_w008 kcfs1-ryKWE_w016 kcfs1-ryKWE_w025
kcfs1-ryKWE_w033 kcfs1-ryKWE_w041 kcfs1-ryKWE_w050 kcfs1-ryKWE_w058
uKNQCPXDNdc_w000 uKNQCPXDNdc_w062
uKNQCPXDNdc_w031 uKNQCPXDNdc_w046 uKNQCPXDNdc_w108
OQSNhk5ICTI_w000 OQSNhk5ICTI_w021 OQSNhk5ICTI_w043 OQSNhk5ICTI_w087
OQSNhk5ICTI_w109 OQSNhk5ICTI_w131 OQSNhk5ICTI_w153

## B3b — long-baseline real motion (supplemental; see PREREG amendment)

8-frame clips built from frame0 of 8 consecutive windows
(0_jNjpVxUt0, timelapse clouds), so frame0->frame7 spans ~210 source
frames (~8.4 s of timelapse). Real footage, real motion.

REVISION 2026-09-23: block-matcher evidence analysis (independent
Python replica) showed the dominant vote is E/NE, contradicting the
initial W eyeball label — and different cloud layers move in
conflicting directions (large high cloud vs small low clouds), with
deformation. No single uniform translation can be honestly claimed.
All 5 relabeled AMBIG. Method3's WITHHOLD (incoherent) is the correct
behavior here.

AMBIG (5): clouds_long_0 clouds_long_1 clouds_long_2 clouds_long_3 clouds_long_4
