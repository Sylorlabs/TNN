#!/usr/bin/env python3
"""Build the NEW AMBIG native-1080p gallery: single self-contained index.html,
base64-embedded clips. Same 7 categories/order/descriptions as the 480p gallery.
Honest per-clip resolution labels; nothing upscaled."""
import base64, os
HOME = '/home/hatch'
CLIPS = os.path.join(HOME, 'workspace/ambig_1080p/clips')
OUT = os.path.join(HOME, 'workspace/your_files/ambig_clips')

SECTIONS = [
    ("1. Clouds / deformation (6)",
     "Timelapse clouds drift N/NE coherently at the pair level but visibly deform between frame 0 and frame 7.",
     ["rm2_0_jNjpVxUt0_b2_t0465", "rm2_0_jNjpVxUt0_b2_t0480",
      "rm2_0_jNjpVxUt0_b3_t0720", "rm2_0_jNjpVxUt0_b3_t0765",
      "rm2_0_jNjpVxUt0_b4_t0705", "rm2_0_jNjpVxUt0_b4_t0720"]),
    ("2. Cloud shift, no coherence (1)", None,
     ["rm2_0_jNjpVxUt0_b2_t0000"]),
    ("3. Ocean waves (6)",
     "Breaking waves shift E but are complex deformation; sky static (multi-region motion).",
     ["rm2_Eoo4HzILB-M_b2_t0195", "rm2_Eoo4HzILB-M_b2_t0210",
      "rm2_Eoo4HzILB-M_b3_t0195", "rm2_Eoo4HzILB-M_b3_t0210",
      "rm2_Eoo4HzILB-M_b4_t0180", "rm2_Eoo4HzILB-M_b4_t0195"]),
    ("4. Atmospheric shimmer (6)",
     "Arrow maps show radial/scattered votes (shimmer, sway); pair-level votes are misleading; no coherent translation survives viewing.",
     ["rm2_OQSNhk5ICTI_b2_t1995", "rm2_OQSNhk5ICTI_b2_t2505",
      "rm2_OQSNhk5ICTI_b3_t0075", "rm2_OQSNhk5ICTI_b3_t1995",
      "rm2_OQSNhk5ICTI_b4_t0120", "rm2_OQSNhk5ICTI_b4_t5100"]),
    ("5. Pedestrians / multi-motion (9)",
     "City street with independently moving pedestrians; no coherent global motion (t0000 windows show discernible pedestrian change despite ~zero block votes).",
     ["rm2_bwJ-TNu0hGM_b2_t0000", "rm2_bwJ-TNu0hGM_b2_t1440", "rm2_bwJ-TNu0hGM_b2_t1455",
      "rm2_bwJ-TNu0hGM_b3_t0000", "rm2_bwJ-TNu0hGM_b3_t0675", "rm2_bwJ-TNu0hGM_b3_t1440",
      "rm2_bwJ-TNu0hGM_b4_t0270", "rm2_bwJ-TNu0hGM_b4_t1425", "rm2_bwJ-TNu0hGM_b4_t1440"]),
    ("6. Deer walking (1)",
     "Deer walks across the frame; camera static; subject motion dominates, no global translation.",
     ["rm2_uKNQCPXDNdc_b2_t3480"]),
    ("7. FPV drone (6)",
     "Forward/sideways flight; arrow maps show expansion flow + parallax layers, not uniform translation.",
     ["rm2_kcfs1-ryKWE_b2_t0615", "rm2_kcfs1-ryKWE_b2_t0630",
      "rm2_kcfs1-ryKWE_b3_t1245", "rm2_kcfs1-ryKWE_b3_t1260",
      "rm2_kcfs1-ryKWE_b4_t0615", "rm2_kcfs1-ryKWE_b4_t0990"]),
]

def clip_meta(name):
    vid = name[4:].split('_b')[0]
    if vid == '0_jNjpVxUt0':
        return "1080&times;1080 @25fps &middot; <b>NEW</b> native-1080p render"
    if vid == 'bwJ-TNu0hGM':
        return "1080&times;1080 @59.94fps &middot; <b>NEW</b> native-1080p render"
    if vid == 'OQSNhk5ICTI':
        return "480&times;480 @25fps &middot; native (best source YouTube offers)"
    if vid == 'Eoo4HzILB-M':
        return "480&times;480 @25fps &middot; native (1080p re-download throttled)"
    if vid == 'kcfs1-ryKWE':
        return "480&times;480 @30fps &middot; native (1080p re-download throttled)"
    if vid == 'uKNQCPXDNdc':
        return "360&times;360 @25fps &middot; native (1080p re-download throttled)"
    raise ValueError(name)

listed = [l.strip() for l in open(os.path.join(HOME, 'workspace/video_rank_scratch/ambig_list.txt')) if l.strip()]
flat = [c for _, _, cs in SECTIONS for c in cs]
assert sorted(flat) == sorted(listed) and len(flat) == 35, "section/clip mismatch"

def b64(name):
    data = open(os.path.join(CLIPS, name + '.mp4'), 'rb').read()
    return base64.b64encode(data).decode()

parts = ["""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>RM2 AMBIG — 35 clips for human labeling (native-1080p re-render) [NEW]</title>
<style>
body{font-family:system-ui,sans-serif;max-width:1100px;margin:2em auto;padding:0 1em;background:#111;color:#ddd}
h1,h2{color:#fff} .cat{margin:2.5em 0} .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1em}
.clip{background:#1a1a1a;border-radius:8px;padding:.8em} .clip video{width:100%;border-radius:4px;background:#000}
.clip .nm{font-size:.8em;color:#9cf;margin:.4em 0 .2em} .clip .meta{font-size:.75em;color:#8a8;margin-bottom:.2em}
.note{font-size:.85em;color:#aaa;margin-bottom:1em}
.badge{display:inline-block;font-size:.7em;background:#063;color:#8f8;border-radius:4px;padding:.15em .5em;margin-left:.5em}
.badge-hold{display:inline-block;font-size:.7em;background:#333;color:#fc9;border-radius:4px;padding:.15em .5em;margin-left:.5em}
.honest{background:#161616;border:1px solid #333;border-radius:8px;padding:1em 1.2em;margin:1.5em 0;font-size:.9em}
.honest b{color:#fff}
</style></head><body>
<h1>RM2 AMBIG — 35 clips awaiting your verdict <span class="badge">NEW</span> <span class="badge-hold">HELD FOR MICAH'S EYES</span></h1>
<div class="honest">
<b>What changed vs the 480p set (kept as backup in <code>prev_480p/</code>):</b>
16 clips are re-rendered <b>natively at 1080&times;1080</b> from freshly downloaded 1080p YouTube sources
(clouds &times;7 @25fps, pedestrians &times;9 @59.94fps) &mdash; genuine detail, verified against the original fixtures.
The other 19 clips are shown at their <b>true native source resolution</b> (480&times;480 &times;18, 360&times;360 &times;1):
YouTube throttling blocked the 1080p re-downloads for three videos, and 480p is the best YouTube offers for the 4:3 rainbow source.
<b>Nothing here is upscaled, interpolated, or AI-enhanced</b> &mdash; every clip is 8 real source frames at native fps, H.264 CRF16,
center-square cropped. An independent red team signed off 35/35 on identity, frame order, native resolution, and no-blend/no-interpolation.
</div>
<p>Each clip loops seamlessly in your browser. The motion-4 system abstained on all of these
(AMBIG = zoom/expansion, rotation, cuts, multi-motion, complex deformation, or uncertainty).
No metric substitutes for your judgment. Mark each: <b>NEW / PREVIOUSLY SHOWN / REFERENCE</b> — and, per clip, what you actually see.</p>
<p style="color:#8f8">The lab froze these labels before the motion-4 pipeline ever saw them. What follows is the labelers' AMBIG rationale; it does not bind your verdict.</p>
"""]
for title, note, clips in SECTIONS:
    parts.append('\n<h2>%s</h2>\n' % title)
    if note:
        parts.append('<p class="note">%s</p>\n' % note)
    parts.append('<div class="grid">\n')
    for c in clips:
        parts.append('<div class="clip"><video controls loop muted preload="metadata" '
                     'src="data:video/mp4;base64,%s"></video><div class="nm">%s</div>'
                     '<div class="meta">%s</div></div>\n'
                     % (b64(c), c, clip_meta(c)))
    parts.append('</div>\n')
parts.append('</body></html>\n')
html = ''.join(parts)
open(os.path.join(OUT, 'index.html'), 'w').write(html)
print('wrote index.html, %d bytes, %d videos' % (len(html), html.count('<video')))
