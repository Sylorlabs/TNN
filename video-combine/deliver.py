#!/usr/bin/env python3
"""Build deliverables for the video COMBINATION experiment.
Outputs to ~/workspace/your_files/video_combine_new/ (all badged NEW).
Usage: deliver.py
"""
import os, subprocess, hashlib

W = os.path.expanduser("~/workspace/video-combine")
REPRO = os.path.expanduser("~/workspace/video-repro")
PIG_SRC = os.path.join(W, "source", "frames")
BUNNY_SRC = os.path.join(REPRO, "source", "frames")
OUT = os.path.expanduser("~/workspace/your_files/video_combine_new")
os.makedirs(OUT, exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def run(cmd):
    subprocess.run(cmd, check=True)

def mp4_frames(name, pattern):
    out = os.path.join(OUT, name)
    run(["ffmpeg", "-v", "error", "-y", "-framerate", "8", "-i", pattern,
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "14", "-r", "8", out])
    print("wrote", out)

# (a) bunny source: the 24-frame reference clip (same bytes as video-repro reference)
bunny_ref = os.path.join(REPRO, "source", "reference.mp4")
run(["cp", bunny_ref, os.path.join(OUT, "bunny_NEW.mp4")])
print("wrote bunny_NEW.mp4 (copy of video-repro reference.mp4)")

# (b) pig source: 24 frames @8fps 320x240, same encoding as the bunny reference
mp4_frames("pig_NEW.mp4", os.path.join(PIG_SRC, "frame_%02d.ppm"))

# (c) TNN's combination: REFUSED (clean negative) -> explanatory slate, 3.0 s @8fps
slate = os.path.join(OUT, "tnn_combination_REFUSED_NEW.mp4")
lines = [
    (20, "TNN COMBINATION: REFUSED"),
    (60, "clean negative -- the machinery"),
    (80, "stores and re-emits only;"),
    (100, "it has no deliberation organ"),
    (120, "to compose a new video."),
    (160, "see VERDICT.md (white-box)"),
]
vf = "color=c=black:s=320x240:d=3:r=8"
for y, t in lines:
    t = t.replace(":", "\\:")
    vf += (",drawtext=fontfile=%s:text='%s':fontcolor=white:fontsize=14:x=10:y=%d"
           % (FONT, t, y))
run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", vf,
     "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "8", "-t", "3", slate])
print("wrote", slate)

# (d) DUMB baseline control: side-by-side concat (traditionalist compositing,
#     labeled as the control -- NEVER as TNN's work)
control = os.path.join(OUT, "dumb_control_sbs_NEW.mp4")
run(["ffmpeg", "-v", "error", "-y",
     "-i", os.path.join(OUT, "bunny_NEW.mp4"),
     "-i", os.path.join(OUT, "pig_NEW.mp4"),
     "-filter_complex", "[0:v][1:v]hstack=inputs=2",
     "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "8", control])
print("wrote", control)

# full-frame PNGs for the gallery
from PIL import Image
GAL = os.path.join(OUT, "gallery_frames")
os.makedirs(GAL, exist_ok=True)
for f in range(24):
    Image.open(os.path.join(BUNNY_SRC, "frame_%02d.ppm" % f)).convert("RGB") \
        .save(os.path.join(GAL, "bunny_%02d.png" % f))
    Image.open(os.path.join(PIG_SRC, "frame_%02d.ppm" % f)).convert("RGB") \
        .save(os.path.join(GAL, "pig_%02d.png" % f))
# slate + control frames (full frames, extracted from the actual mp4s)
run(["ffmpeg", "-v", "error", "-y", "-i", slate,
     os.path.join(GAL, "refused_%02d.png")])
run(["ffmpeg", "-v", "error", "-y", "-i", control,
     os.path.join(GAL, "control_%02d.png")])

rows = []
for f in range(24):
    cells = "".join(
        '<td><img src="gallery_frames/%s_%02d.png" width="%d" height="240"></td>'
        % (c, f, 320 if c != "control" else 640)
        for c in ["bunny", "pig", "refused", "control"]
    )
    rows.append("<tr><th>f%02d</th>%s</tr>" % (f, cells))

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

html = """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>VIDEO COMBINATION EXPERIMENT -- NEW 2026-09-26</title>
<style>
body { font-family: sans-serif; background: #111; color: #eee; margin: 24px; }
.badge { display:inline-block; background:#c00; color:#fff; font-weight:bold; padding:4px 12px; border-radius:6px; }
.badge-green { display:inline-block; background:#181; color:#fff; font-weight:bold; padding:4px 12px; border-radius:6px; }
table { border-collapse: collapse; }
td, th { border: 1px solid #444; padding: 4px; text-align:center; }
th { background:#222; }
video { margin: 8px; background:#000; }
.note { color:#aaa; max-width: 980px; }
.warn { color:#f88; max-width: 980px; font-weight: bold; }
</style></head><body>
<h1><span class="badge">NEW</span> Video combination experiment <span class="badge">NEW</span></h1>
<p>Question: can TNN's deliberate-memory machinery (the substrate that reproduced the bunny clip
bit-for-bit) DELIBERATELY COMBINE two memorized clips into a new video?</p>
<p class="warn">Answer: CLEAN NEGATIVE. TNN refused. The mechanism can only store and re-emit --
it has no deliberation organ (no propose/evaluate/select/synthesize), so any blend/concat/overlay
would be the programmer's composition, not TNN's deliberation. The refusal is mechanical and
reproducible: the combine binary (pure Zag, zero RNG) verified both memories intact
(48/48 recalled hashes match ingest) and then exited rc=1 with a written refusal trace,
byte-identical across two runs. Full white-box diagnosis in VERDICT.md.</p>
<h2>Videos (8 fps, full duration)</h2>
<video width="320" height="240" controls loop><source src="bunny_NEW.mp4" type="video/mp4"></video>
<video width="320" height="240" controls loop><source src="pig_NEW.mp4" type="video/mp4"></video>
<video width="320" height="240" controls loop><source src="tnn_combination_REFUSED_NEW.mp4" type="video/mp4"></video>
<video width="640" height="240" controls loop><source src="dumb_control_sbs_NEW.mp4" type="video/mp4"></video>
<p class="note">Left to right: (a) bunny source, (b) pig source, (c) TNN's combination = REFUSAL SLATE
(clean negative, not a video), (d) DUMB CONTROL: side-by-side concat -- traditionalist compositing,
shown only so the difference is visible. It is NOT TNN's work.</p>
<h2>Full-frame grid (all 24 frames)</h2>
<table>
<tr><th>frame</th><th>(a) bunny</th><th>(b) pig</th><th>(c) TNN: REFUSED</th><th>(d) DUMB CONTROL (sbs)</th></tr>
""" + ''.join(rows) + """</table>
<p class="note">SHA-256: bunny_NEW.mp4 """ + sha(os.path.join(OUT, "bunny_NEW.mp4")) + """<br>
pig_NEW.mp4 """ + sha(os.path.join(OUT, "pig_NEW.mp4")) + """<br>
tnn_combination_REFUSED_NEW.mp4 """ + sha(slate) + """<br>
dumb_control_sbs_NEW.mp4 """ + sha(control) + """</p>
<p class="note">Provenance: bunny = Big Buck Bunny (2008), Blender Foundation, CC BY 3.0
(see video-repro/source/PROVENANCE.md); pig = "2024-06-01 LJUBLJANA ZOO LJUBLJANA - pig",
NaIzletuSi (TM), CC BY 3.0 via Wikimedia Commons (see workdir source/PROVENANCE.md).</p>
</body></html>"""

with open(os.path.join(OUT, "gallery_NEW.html"), "w") as fh:
    fh.write(html)
print("wrote", os.path.join(OUT, "gallery_NEW.html"))
