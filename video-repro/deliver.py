#!/usr/bin/env python3
"""Build MP4s + full-frame gallery for the video native-reproduction test.
Outputs to ~/workspace/your_files/video_repro_new/ (badged NEW).
Usage: deliver.py
"""
import os, subprocess
from PIL import Image

W = os.path.expanduser("~/workspace/video-repro")
SRC = os.path.join(W, "source", "frames")
RUNS = os.path.join(W, "runs")
OUT = os.path.expanduser("~/workspace/your_files/video_repro_new")
os.makedirs(OUT, exist_ok=True)

def mp4(name, pattern, vfilter=None):
    out = os.path.join(OUT, name)
    cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", "8", "-i", pattern]
    if vfilter:
        cmd += ["-vf", vfilter]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-r", "8", out]
    subprocess.run(cmd, check=True)
    print("wrote", out)

mp4("original_NEW.mp4", os.path.join(SRC, "frame_%02d.ppm"))
mp4("native_verbatim_NEW.mp4", os.path.join(RUNS, "out_verbatim", "frame_%02d.ppm"))
mp4("native_encoded_NEW.mp4", os.path.join(RUNS, "out_encoded", "frame_%02d.ppm"))
mp4("bytecopy_NEW.mp4", os.path.join(RUNS, "bytecopy", "frame_%02d.ppm"))
mp4("floor_NEW.mp4", os.path.join(RUNS, "floor240", "floor_%02d.ppm"), "scale=320:240:flags=bilinear")

# full-frame PNGs for the gallery (byte-copy omitted: provably identical to original)
GAL = os.path.join(OUT, "gallery_frames")
os.makedirs(GAL, exist_ok=True)
cols = [
    ("original", SRC, "frame_{:02d}.ppm", None),
    ("native-verbatim", os.path.join(RUNS, "out_verbatim"), "frame_{:02d}.ppm", None),
    ("native-encoded", os.path.join(RUNS, "out_encoded"), "frame_{:02d}.ppm", None),
    ("floor", os.path.join(RUNS, "floor240"), "floor_{:02d}.ppm", (320, 240)),
]
for cname, d, pat, size in cols:
    for f in range(24):
        im = Image.open(os.path.join(d, pat.format(f))).convert("RGB")
        if size:
            im = im.resize(size, Image.BILINEAR)
        im.save(os.path.join(GAL, f"{cname}_{f:02d}.png"))

rows = []
for f in range(24):
    cells = "".join(
        f'<td><img src="gallery_frames/{c}_{f:02d}.png" width="320" height="240"></td>'
        for c in ["original", "native-verbatim", "native-encoded", "floor"]
    )
    rows.append(f"<tr><th>f{f:02d}</th>{cells}</tr>")

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>VIDEO NATIVE-REPRODUCTION TEST — NEW 2026-09-25</title>
<style>
body {{ font-family: sans-serif; background: #111; color: #eee; margin: 24px; }}
.badge {{ display:inline-block; background:#c00; color:#fff; font-weight:bold; padding:4px 12px; border-radius:6px; }}
table {{ border-collapse: collapse; }}
td, th {{ border: 1px solid #444; padding: 4px; text-align:center; }}
th {{ background:#222; }}
video {{ margin: 8px; background:#000; }}
.note {{ color:#aaa; max-width: 900px; }}
</style></head><body>
<h1><span class="badge">NEW</span> Video native-reproduction test <span class="badge">NEW</span></h1>
<p>Reference: Big Buck Bunny (2008), Blender Foundation, CC BY 3.0 — 24 frames, 320x240 @ 8fps, t=65.15s&rarr;68.15s.
All frames below are FULL frames at native size. Byte-copy control omitted from the grid: it is
provably pixel-identical to the original on all 24 frames (PSNR inf, SSIM 1.0000).</p>
<h2>Videos (8 fps)</h2>
<video width="320" height="240" controls loop><source src="original_NEW.mp4" type="video/mp4"></video>
<video width="320" height="240" controls loop><source src="native_verbatim_NEW.mp4" type="video/mp4"></video>
<video width="320" height="240" controls loop><source src="native_encoded_NEW.mp4" type="video/mp4"></video>
<video width="320" height="240" controls loop><source src="bytecopy_NEW.mp4" type="video/mp4"></video>
<video width="320" height="240" controls loop><source src="floor_NEW.mp4" type="video/mp4"></video>
<p class="note">Left to right: original, native-verbatim, native-encoded, byte-copy, floor.</p>
<h2>Full-frame grid (all 24 frames, 320x240)</h2>
<table>
<tr><th>frame</th><th>original</th><th>native-verbatim</th><th>native-encoded</th><th>floor (240&rarr;320 stretch)</th></tr>
{''.join(rows)}
</table>
<p class="note">Metrics (per-frame PSNR/SSIM vs original): native-verbatim inf/1.0000 (ties byte-copy ceiling) |
native-encoded 28.31 dB / 0.9195 | floor 11.19 dB / 0.5458. See VERDICT.md for the white-box trace.</p>
</body></html>"""

with open(os.path.join(OUT, "gallery_NEW.html"), "w") as fh:
    fh.write(html)
print("wrote", os.path.join(OUT, "gallery_NEW.html"))
