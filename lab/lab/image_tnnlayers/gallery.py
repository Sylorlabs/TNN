#!/usr/bin/env python3
# gallery.py — build the self-contained image_tnnlayers_NEW/index.html
# All images embedded as data URIs; zero external loads.
import base64, io, os
from PIL import Image

WORK = os.path.expanduser("~/workspace/image_tnnlayers")
OUTDIR = os.path.expanduser("~/workspace/your_files/image_tnnlayers_NEW")
ZOOMDIR = os.path.expanduser("~/workspace/image_zoom_fork/run")
NLDIR = os.path.expanduser("~/workspace/image_nolayers/run")

def datauri(path, maxw=None):
    img = Image.open(path)
    if maxw and img.size[0] > maxw:
        img = img.resize((maxw, int(img.size[1]*maxw/img.size[0])), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}", img.size

def crop_uri(path, box, scale=4):
    img = Image.open(path).crop(box)
    img = img.resize((img.size[0]*scale, img.size[1]*scale), Image.NEAREST)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"

# Bridge-arch crop: the prominent left arch (verified visually on original)
ARCH = (110, 85, 230, 165)

def img_tag(uri, alt, w=None):
    ws = f' width="{w}"' if w else ''
    return f'<img src="{uri}" alt="{alt}"{ws} style="image-rendering:auto;max-width:100%"/>'

parts = []
parts.append("""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>TNN chooses its layers — image fork</title>
<style>
body{font-family:Georgia,serif;max-width:1100px;margin:2em auto;padding:0 1em;color:#222;background:#fafafa}
h1,h2{font-family:Helvetica,Arial,sans-serif}
table{border-collapse:collapse;margin:1em 0}
td,th{border:1px solid #999;padding:6px 12px;text-align:right}
th{background:#eee}
.cap{font-size:0.9em;color:#555;margin:0.4em 0 1.5em}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:1em}
pre{background:#f0f0f0;padding:1em;overflow-x:auto;font-size:0.85em}
.win{background:#e6f4e6}.lose{background:#f8e6e6}
</style></head><body>
<h1>TNN chooses its layers</h1>
<p>Micah's order, 2026-09-26: <i>"layers are clearly needed &mdash; but what
happens if TNN chooses its layers instead? Let's try that."</i> TNN surveyed
the 512&times;187 Albi fixture, chose its own layer decomposition (mechanisms,
order, vocabularies, scale set), and committed each layer only after measuring
it against a bar. The deliberation trace is part of the artifact.</p>
""")

# ---- headline numbers (filled from metrics) ----
import json
nums = json.load(open(os.path.join(WORK, "run", "metrics.json")))
parts.append("<h2>Headline numbers</h2>")
parts.append("""<table>
<tr><th>Approach</th><th>PSNR (dB)</th><th>SSIM</th><th>Residual</th><th>Knowledge bytes</th></tr>
<tr><td style="text-align:left">Hand-designed layered zoom</td><td>30.80</td><td>0.9620</td><td>19.9%</td><td>1,343,354</td></tr>
<tr><td style="text-align:left">No-layers (exemplar take/split)</td><td>29.27</td><td>0.9260</td><td>11.7%</td><td>2,505,092</td></tr>
<tr class="{cls}"><td style="text-align:left"><b>TNN-chooses-layers (this fork)</b></td><td><b>{psnr:.2f}</b></td><td><b>{ssim:.4f}</b></td><td><b>{res:.1f}%</b></td><td><b>{kb:,d}</b></td></tr>
</table>""".format(cls="win" if nums["psnr"]>=30.80 else "lose", **nums))
parts.append('<p class="cap">PSNR = mean of per-channel dB; SSIM = Gaussian-window, per-channel mean. '
'Pre-residual understanding renders only &mdash; the residual is the excluded error channel, same contract as the prior forks.</p>')

# ---- full renders ----
parts.append("<h2>Full renders: original | layered-zoom | no-layers | TNN-layers (understanding)</h2>")
orig_u, _ = datauri(os.path.expanduser("~/workspace/your_files/image_repro/original_512.bmp"), 512)
zoom_u, _ = datauri(os.path.join(ZOOMDIR, "render_understanding.bmp"), 512)
nl_u, _ = datauri(os.path.join(NLDIR, "render_understanding.bmp"), 512)
tl_u, _ = datauri(os.path.join(WORK, "run", "render_understanding.bmp"), 512)
parts.append('<div class="grid">')
for uri, cap in [(orig_u, "Original (sealed fixture)"),
                 (zoom_u, "Layered zoom understanding (30.80 dB)"),
                 (nl_u, "No-layers understanding (29.27 dB)"),
                 (tl_u, "TNN-layers understanding (%.2f dB)" % nums["psnr"])]:
    parts.append(f'<div>{img_tag(uri, cap, 512)}<p class="cap">{cap}</p></div>')
parts.append('</div>')

# ---- layer map ----
parts.append("<h2>TNN's own organization (layer map)</h2>")
lm_u, _ = datauri(os.path.join(WORK, "run", "render_layermap.bmp"), 512)
parts.append(img_tag(lm_u, "layer map", 512))
parts.append('<p class="cap">Which committed layer owns each pixel (first layer in TNN\'s try order '
'with |reconstruction| &ge; 27): blue = SMOOTH (quadtree mean+planar), '
'red = LINES (straight segments), green = SHAPES (exemplar patches), black = residual only.</p>')

# ---- bridge arch crops ----
parts.append("<h2>Bridge-arch crops: the pentagon test</h2>")
parts.append("<p>The zoom fork's edge stage drew straight chords through this arch curve and faceted it "
"into pentagons. Same 120&times;80 crop (4&times; nearest) from each understanding render:</p>")
parts.append('<div class="grid">')
for path, cap in [
    (os.path.expanduser("~/workspace/your_files/image_repro/original_512.bmp"), "Original"),
    (os.path.join(ZOOMDIR, "render_understanding.bmp"), "Layered zoom (pentagon artifact)"),
    (os.path.join(NLDIR, "render_understanding.bmp"), "No-layers"),
    (os.path.join(WORK, "run", "render_understanding.bmp"), "TNN-layers")]:
    parts.append(f'<div>{img_tag(crop_uri(path, ARCH), cap)}<p class="cap">{cap}</p></div>')
parts.append('</div>')

# ---- deliberation trace ----
parts.append("<h2>Deliberation trace</h2>")
trace = open(os.path.join(WORK, "run", "DELIBTRACE.txt")).read()
parts.append("<pre>" + trace.replace("&","&amp;").replace("<","&lt;")[:6000] + "</pre>")
parts.append('<p class="cap">Full trace in the repo: <tt>docs/lab/image_tnnlayers/run/DELIBTRACE.txt</tt></p>')

parts.append("</body></html>")
os.makedirs(OUTDIR, exist_ok=True)
html = "\n".join(parts)
open(os.path.join(OUTDIR, "index.html"), "w").write(html)
# verify self-contained
import re
ext = re.findall(r'src="(?!data:)([^"]+)"', html)
assert not ext, f"external loads: {ext}"
print(f"gallery ok: {len(html)} bytes, no external loads")
