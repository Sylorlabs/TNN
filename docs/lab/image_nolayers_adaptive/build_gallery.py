#!/usr/bin/env python3
# build_gallery.py — self-contained comparison gallery (data URIs, zero external loads).
import base64, os, sys

OUT = sys.argv[1]  # output dir for index.html
A = sys.argv[2]    # analysis png dir
# numbers passed as env or argv
PSNR_A, SSIM_A, RES_A, KB_A = sys.argv[3:7]
PSNR_R, SSIM_R, RES_R, KB_R = sys.argv[7:11]

def uri(p):
    d = open(p, 'rb').read()
    return "data:image/png;base64," + base64.b64encode(d).decode()

def img(p, w, cap):
    return f'<figure style="margin:8px"><img src="{uri(p)}" style="width:{w}px;image-rendering:auto;border:1px solid #444"><figcaption style="font-size:12px;color:#bbb">{cap}</figcaption></figure>'

os.makedirs(OUT, exist_ok=True)
# full renders: reuse analysis crops? full-size PNGs made separately
full_o = uri(f"{A}/full_original.png")
full_a = uri(f"{A}/full_adaptive.png")
full_r = uri(f"{A}/full_rigid.png")
full_z = uri(f"{A}/full_zoom.png")

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>No-layers adaptive-split — results</title>
<style>body{{background:#111;color:#ddd;font-family:system-ui,sans-serif;max-width:1200px;margin:auto;padding:20px}}
table{{border-collapse:collapse;margin:16px 0}}td,th{{border:1px solid #555;padding:6px 12px;text-align:right}}
th{{background:#222}}td:first-child,th:first-child{{text-align:left}}
.row{{display:flex;flex-wrap:wrap}}h2{{color:#9cf;margin-top:32px}}.new{{color:#8f8}}</style>
</head><body>
<h1>No-layers fork: the rigid grid is gone <span class="new">(NEW 2026-09-26)</span></h1>
<p>Same single vocabulary, same single deliberative pass, same residual contract —
the only change: regions are <b>content-delimited rectangles</b>, split positions chosen
by the CART rule (argmin over pixel cuts of flat-fit energy), recorded in the
deliberation trace. No thresholds, no tuned constants. Pure Zag, zero RNG,
byte-identical reruns x2.</p>
<h2>Head-to-head (pre-residual understanding)</h2>
<table><tr><th>Pipeline</th><th>PSNR</th><th>SSIM</th><th>Residual share</th><th>Knowledge bytes</th></tr>
<tr><td>Layered zoom fork</td><td>30.80 dB</td><td>0.9620</td><td>19.9%</td><td>1,343,354</td></tr>
<tr><td>No-layers, rigid grid</td><td>{PSNR_R} dB</td><td>{SSIM_R}</td><td>{RES_R}%</td><td>{KB_R}</td></tr>
<tr><td><b>No-layers, adaptive splits (this fork)</b></td><td><b>{PSNR_A} dB</b></td><td><b>{SSIM_A}</b></td><td><b>{RES_A}%</b></td><td><b>{KB_A}</b></td></tr>
</table>
<h2>Full renders (understanding only, no residual)</h2>
<div class="row">
<figure style="margin:8px"><img src="{full_o}" style="width:560px;border:1px solid #444"><figcaption style="font-size:12px;color:#bbb">original (sealed fixture)</figcaption></figure>
<figure style="margin:8px"><img src="{full_z}" style="width:560px;border:1px solid #444"><figcaption style="font-size:12px;color:#bbb">layered zoom (30.80 dB)</figcaption></figure>
<figure style="margin:8px"><img src="{full_r}" style="width:560px;border:1px solid #444"><figcaption style="font-size:12px;color:#bbb">no-layers rigid grid ({PSNR_R} dB)</figcaption></figure>
<figure style="margin:8px"><img src="{full_a}" style="width:560px;border:1px solid #444"><figcaption style="font-size:12px;color:#bbb">no-layers adaptive splits ({PSNR_A} dB) — NEW</figcaption></figure>
</div>
<h2>Pentagon check: bridge arch at 10x (Micah's catch — must stay smooth)</h2>
<p>The layered edge stage's greedy chord tracing turned this arch into a polygon.
The rigid no-layers fork eliminated it. Verifying the adaptive fork does not regress:</p>
<div class="row">
{img(f"{A}/arch10x_original.png", 380, "original arch (10x)")}
{img(f"{A}/arch10x_zoom.png", 380, "layered zoom arch (10x) — faceted")}
{img(f"{A}/arch10x_rigid.png", 380, "no-layers rigid arch (10x) — smooth")}
{img(f"{A}/arch10x_adaptive.png", 380, "no-layers ADAPTIVE arch (10x) — NEW, must be smooth")}
</div>
<h2>Error maps (mean abs error x6, brighter = worse)</h2>
<div class="row">
{img(f"{A}/errmap_rigid.png", 560, "rigid grid error map")}
{img(f"{A}/errmap_adaptive.png", 560, "adaptive splits error map — NEW")}
</div>
<h2>Where TNN looked closely (scale maps)</h2>
<div class="row">
{img(f"{A}/scalemap_rigid.png", 560, "rigid: dyadic grid scales")}
{img(f"{A}/scalemap_adaptive.png", 560, "adaptive: content rectangles — NEW")}
</div>
<p style="color:#888;font-size:13px">All images embedded as data URIs; this page loads zero external resources.
Evidence: code + docs + verdict committed to tnn-native-lab (never main).</p>
</body></html>"""

open(f"{OUT}/index.html", "w").write(html)
# verify zero external loads
h = open(f"{OUT}/index.html").read()
import re
bad = [m for m in re.finditer(r'src="(?!data:)', h)]
assert not bad, f"external loads found: {len(bad)}"
print(f"gallery written to {OUT}/index.html, self-contained OK")
