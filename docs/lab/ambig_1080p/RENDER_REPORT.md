# AMBIG native-1080p re-render — RENDER_REPORT.md

35/35 clips staged in `~/workspace/ambig_1080p/clips/`. All renders native
(no upscaling, no interpolation, no retiming). Driver finished
2026-09-25T05:43:49Z ("DRIVER: ALL VIDEOS DONE").

## Per-video source table

| video | source used | codec | res | fps | sha256 | how obtained |
|---|---|---|---|---|---|---|
| 0_jNjpVxUt0 | fresh download | h264 (AVC) | 1920x1080 | 25/1 | 9919b8a3d3f4ce39800d9157b7a0e18fed5baebdd70e0b9719cd5c1a09819526 | yt-dlp format 137 (1080p AVC, preferred) |
| Eoo4HzILB-M | existing raw, HONESTLY CAPPED | av1 | 854x480 | 25/1 | 609f0ef94cb4b4397dfaa7c68fd7c1ca3437488a7481d712db4f84ee5877a83f | 6/6 retries failed (429/403/bot-check/IncompleteRead) |
| OQSNhk5ICTI | fresh download | h264 (AVC) | 640x480 | 25/1 | 0ceafc8d9f3b95e62df76f0495565b6e3d2457a5c3c221ca16827e00679ae77a | best AVC ≤1080p; NO 1080p format offered for this 4:3 source (max available 480p) |
| bwJ-TNu0hGM | fresh download | h264 (AVC) | 1920x1080 | 60000/1001 | 1f37abc4d41cf12b8eaef2225f7f36f205c143cc5a16e966ca001e0e308d716c | yt-dlp format 299 (1080p60 AVC, preferred) |
| kcfs1-ryKWE | existing raw, HONESTLY CAPPED | av1 | 854x480 | 30/1 | 01d22ee8f0634c86d7a4647cb0752dfcf7e7d2f633a27091f91308abdcf6b5b8 | 6/6 retries failed (IncompleteRead throttling, bot-check) |
| uKNQCPXDNdc | existing raw, HONESTLY CAPPED | vp9 | 640x360 | 25/1 | 899b361b40102f4bc8c5c385a8413fe7c9e58337dedc941ffccb9e18aa1c1f00 | 6/6 retries failed (bot-check/throttling) |

Fresh downloads: 3 (0_jNjpVxUt0, OQSNhk5ICTI, bwJ-TNu0hGM), all AVC per the
codec preference. Honestly capped: 3 (Eoo4HzILB-M, kcfs1-ryKWE, uKNQCPXDNdc) —
existing raws copied to `raw1080/<vid>.mp4` with `<vid>.CAPPED` marker files;
originals untouched. Capped clips are NOT upscaled; they render at native
480x480 (Eoo, kcfs) or 360x360 (uKN).

## FPS decisions (native fps preserved, no interpolation/duplication/retiming)

| video | old fps | new fps | decision |
|---|---|---|---|
| 0_jNjpVxUt0 | 25 | 25/1 | same — direct frame indices |
| Eoo4HzILB-M | 25 | 25/1 (capped) | same |
| OQSNhk5ICTI | 25 | 25/1 | same |
| bwJ-TNu0hGM | 30000/1001 | 60000/1001 | TIMESTAMP-MAPPED, ratio exactly 2.0 (see map below) |
| kcfs1-ryKWE | 30 | 30/1 (capped) | same |
| uKNQCPXDNdc | 25 | 25/1 (capped) | same |

bwJ timestamp map (new_frame = round(old_frame × 2.0), output fps stays native 60000/1001):
- b2_t0000: [0,4,8,12,16,20,24,28] (old [0,2,4,6,8,10,12,14])
- b2_t1440: [2880,2884,2888,2892,2896,2900,2904,2908] (old [1440..1454 step 2])
- b2_t1455: [2910,2914,2918,2922,2926,2930,2934,2938] (old [1455..1469 step 2])
- b3_t0000: [0,6,12,18,24,30,36,42] (old [0..21 step 3])
- b3_t0675: [1350,1356,1362,1368,1374,1380,1386,1392] (old [675..696 step 3])
- b3_t1440: [2880,2886,2892,2898,2904,2910,2916,2922] (old [1440..1461 step 3])
- b4_t0270: [540,548,556,564,572,580,588,596] (old [270..298 step 4])
- b4_t1425: [2850,2858,2866,2874,2882,2890,2898,2906] (old [1425..1453 step 4])
- b4_t1440: [2880,2888,2896,2904,2912,2920,2928,2936] (old [1440..1468 step 4])

## Identity audit — full 35-clip table (one-step pipeline)

Method (corrected mid-run): select+crop+scale=64:64 straight from the source
raw to rgb24 in ONE ffmpeg step, compared against the `.vid` fixtures
(regenerated from the OLD raws with the identical one-step pipeline).
The earlier PNG-mediated identity path inflated MADs with a YUV→RGB
conversion artifact (proven: direct path gave maxMAD=0/meanMAD=0 where the
PNG path gave 51/1.79 on the same capped clip). All numbers below are the
corrected one-step values.

Ruling applied per clip: (a) meanMAD ≤ 3.0; (b) channels with |diff| ≥ 20
confined to high-contrast edges and < 0.5% of channels; (c) 64px visual
side-by-side identical (all 35 reviewed in `audit/contact_sheet.png`).

| clip | maxMAD | meanMAD | (a) | ch≥20 | frac | (b) | edge-confined |
|---|---|---|---|---|---|---|---|
| rm2_0_jNjpVxUt0_b2_t0000 | 21 | 0.8346 | PASS | 4 | 0.0041% | PASS | 4/4 |
| rm2_0_jNjpVxUt0_b2_t0465 | 19 | 0.9044 | PASS | 0 | 0.0000% | PASS | 0/0 |
| rm2_0_jNjpVxUt0_b2_t0480 | 20 | 0.8064 | PASS | 1 | 0.0010% | PASS | 1/1 |
| rm2_0_jNjpVxUt0_b3_t0720 | 20 | 0.9190 | PASS | 2 | 0.0020% | PASS | 2/2 |
| rm2_0_jNjpVxUt0_b3_t0765 | 20 | 0.8562 | PASS | 1 | 0.0010% | PASS | 1/1 |
| rm2_0_jNjpVxUt0_b4_t0705 | 23 | 0.8966 | PASS | 3 | 0.0031% | PASS | 3/3 |
| rm2_0_jNjpVxUt0_b4_t0720 | 20 | 0.9059 | PASS | 1 | 0.0010% | PASS | 1/1 |
| rm2_Eoo4HzILB-M_b2_t0195 | 0 | 0.0000 | PASS | 0 | 0.0000% | PASS | 0/0 |
| rm2_Eoo4HzILB-M_b2_t0210 | 0 | 0.0000 | PASS | 0 | 0.0000% | PASS | 0/0 |
| rm2_Eoo4HzILB-M_b3_t0195 | 0 | 0.0000 | PASS | 0 | 0.0000% | PASS | 0/0 |
| rm2_Eoo4HzILB-M_b3_t0210 | 0 | 0.0000 | PASS | 0 | 0.0000% | PASS | 0/0 |
| rm2_Eoo4HzILB-M_b4_t0180 | 0 | 0.0000 | PASS | 0 | 0.0000% | PASS | 0/0 |
| rm2_Eoo4HzILB-M_b4_t0195 | 0 | 0.0000 | PASS | 0 | 0.0000% | PASS | 0/0 |
| rm2_OQSNhk5ICTI_b2_t1995 | 11 | 0.9342 | PASS | 0 | 0.0000% | PASS | 0/0 |
| rm2_OQSNhk5ICTI_b2_t2505 | 12 | 1.0136 | PASS | 0 | 0.0000% | PASS | 0/0 |
| rm2_OQSNhk5ICTI_b3_t0075 | 20 | 1.9411 | PASS | 2 | 0.0020% | PASS | 2/2 |
| rm2_OQSNhk5ICTI_b3_t1995 | 14 | 0.9631 | PASS | 0 | 0.0000% | PASS | 0/0 |
| rm2_OQSNhk5ICTI_b4_t0120 | 22 | 2.0512 | PASS | 4 | 0.0041% | PASS | 4/4 |
| rm2_OQSNhk5ICTI_b4_t5100 | 10 | 0.9744 | PASS | 0 | 0.0000% | PASS | 0/0 |
| rm2_bwJ-TNu0hGM_b2_t0000 | 29 | 2.7336 | PASS | 273 | 0.2777% | PASS | 273/273 |
| rm2_bwJ-TNu0hGM_b2_t1440 | 27 | 3.0894 | **FAIL (+0.09)** | 194 | 0.1973% | PASS | 194/194 |
| rm2_bwJ-TNu0hGM_b2_t1455 | 23 | 2.8532 | PASS | 113 | 0.1149% | PASS | 113/113 |
| rm2_bwJ-TNu0hGM_b3_t0000 | 29 | 2.7372 | PASS | 257 | 0.2614% | PASS | 257/257 |
| rm2_bwJ-TNu0hGM_b3_t0675 | 33 | 3.1344 | **FAIL (+0.13)** | 210 | 0.2136% | PASS | 210/210 |
| rm2_bwJ-TNu0hGM_b3_t1440 | 27 | 3.0382 | **FAIL (+0.04)** | 169 | 0.1719% | PASS | 169/169 |
| rm2_bwJ-TNu0hGM_b4_t0270 | 25 | 2.8539 | PASS | 134 | 0.1363% | PASS | 134/134 |
| rm2_bwJ-TNu0hGM_b4_t1425 | 27 | 3.1580 | **FAIL (+0.16)** | 223 | 0.2268% | PASS | 223/223 |
| rm2_bwJ-TNu0hGM_b4_t1440 | 27 | 2.9778 | PASS | 135 | 0.1373% | PASS | 135/135 |
| rm2_kcfs1-ryKWE_b2_t0615 | 0 | 0.0000 | PASS | 0 | 0.0000% | PASS | 0/0 |
| rm2_kcfs1-ryKWE_b2_t0630 | 0 | 0.0000 | PASS | 0 | 0.0000% | PASS | 0/0 |
| rm2_kcfs1-ryKWE_b3_t1245 | 0 | 0.0000 | PASS | 0 | 0.0000% | PASS | 0/0 |
| rm2_kcfs1-ryKWE_b3_t1260 | 0 | 0.0000 | PASS | 0 | 0.0000% | PASS | 0/0 |
| rm2_kcfs1-ryKWE_b4_t0615 | 0 | 0.0000 | PASS | 0 | 0.0000% | PASS | 0/0 |
| rm2_kcfs1-ryKWE_b4_t0990 | 0 | 0.0000 | PASS | 0 | 0.0000% | PASS | 0/0 |
| rm2_uKNQCPXDNdc_b2_t3480 | 0 | 0.0000 | PASS | 0 | 0.0000% | PASS | 0/0 |

31/35 pass all of (a)+(b); 4 bwJ clips **marginally fail (a)** (3.04–3.16,
1–5% over the 3.0 bar) while passing (b) with 100% edge confinement and (c)
visually identical. Notes on the 4:

- The bwJ source is a busy high-motion street scene; the 1080p60-AVC
  transcode legitimately differs more from the 480p29.97-AV1 transcode than
  the cloud scenes do (2.7–3.2 vs 0.8–0.9).
- Timestamp mapping verified correct: a 5-candidate frame test around the
  mapped frame for b2_t1440 (new frames 2878/2879/2880/2881 vs fixture frame
  0) gave meanMAD 4.52/3.41/3.24 — the mapped frame 2880 is the best match,
  so the excess is genuine transcode difference, not a mapping error.
- Not relitigated: the 3.0 bar stands as set; the 4 clips are flagged here
  for the red team / parent decision. They remain staged (correct video,
  correct timestamps, (b)+(c) pass).

## Output properties (verified per clip via ffprobe)

- All 35: h264, yuv420p, exactly 8 frames, CRF16 preset slow, center-square crop.
- 7 × 1080x1080 @ 25/1 (0_jNjpVxUt0, native 1080p)
- 9 × 1080x1080 @ 60000/1001 (bwJ-TNu0hGM, native 1080p60)
- 6 × 480x480 @ 25/1 (Eoo4HzILB-M, capped)
- 6 × 480x480 @ 25/1 (OQSNhk5ICTI, native 480p — best available)
- 6 × 480x480 @ 30/1 (kcfs1-ryKWE, capped)
- 1 × 360x360 @ 25/1 (uKNQCPXDNdc, capped)
- All 35 current SHA-256 values match their latest build_log.txt entries (0 mismatches).

## Backup locations (AV1 artifacts archived, not deleted)

- `clips_av1_backup/`: 7 inherited AV1-sourced clips from video 0 (pre-AVC-preference)
- `raw1080_av1_backup/0_jNjpVxUt0_format399_av1.mp4`: inherited AV1 raw
  (sha256 11daf85b983a39b211fac66b65b2aa29a8b292e2590d8db6b9e9b71b12bd418e)

## Pipeline notes / caveats

- Identity methodology corrected mid-run: the one-step direct source→64px
  path replaced the PNG-mediated path (which added a spurious YUV→RGB
  conversion, inflating MADs ~1.5×). All reported numbers are one-step.
- `audit_clip.py` was rewritten for the one-step path (takes explicit source
  + frame list); all 13 early clips were re-audited with it.
- Three VM reboots interrupted the serial driver (~00:12, ~02:08, ~04:42
  UTC); after each, staged clips were SHA-verified and the driver relaunched
  (idempotent: skips existing raws/clips). No clip was rendered twice with
  different bytes — all final SHAs are single-valued in the log.
- The build log contains superseded PNG-path audit lines and one
  sha256sum -c batch whose warnings came from matching both old AV1 and new
  AVC entries; the authoritative numbers are the latest one-step AUDIT block
  per clip (table above) and the final per-file SHA lines.
- Nothing committed; `~/workspace/your_files/ambig_clips/` and red-team
  directories untouched.
