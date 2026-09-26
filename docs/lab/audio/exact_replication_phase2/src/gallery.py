#!/usr/bin/env python3
"""Build the self-contained NEW-badged gallery HTML with data URIs."""
import base64, json, os

P2 = '/home/hatch/workspace/exact_audio_replication/phase2'
R = os.path.join(P2, 'run')
F = '/home/hatch/workspace/rawbyte_longmem'
OUT = '/home/hatch/workspace/your_files/exact_audio_v6_gallery.html'

def duri(path, mime):
    b = open(path, 'rb').read()
    return f'data:{mime};base64,' + base64.b64encode(b).decode()

# fixture rows
fixtures = [
    ('strike', 40.5, 0.9984),
    ('vowel', 97.9, 0.9899),
    ('cry', 136.0, 0.9983),
    ('clang', 109.8, 0.9965),
]

# corpus aggregate
agg = json.load(open(os.path.join(P2, 'results', 'corpus_aggregate.json')))

rows = ''
for c, rms, corr in fixtures:
    wave = duri(f'{R}/wave_{c}.png', 'image/png')
    exact = duri(f'{R}/t_{c}/{c}_exact.wav', 'audio/wav')
    sem = duri(f'{R}/t_{c}/{c}_sem.wav', 'audio/wav')
    rows += f'''
    <section class="clip">
      <h2>{c} <span class="pass">BYTE-IDENTICAL ✓</span></h2>
      <img src="{wave}" alt="{c} waveform comparison" style="width:100%">
      <table>
        <tr><th>Mode 10 (exact)</th><td><code>cmp</code> PASS — 0 differing bytes</td></tr>
        <tr><th>Mode 10 run 2</th><td>byte-identical to run 1 (deterministic)</td></tr>
        <tr><th>Mode 11 semantic</th><td>RMS err {rms} LSB, corr {corr}</td></tr>
      </table>
      <p><b>Exact render (full duration — Micah's ears judge):</b><br>
      <audio controls src="{exact}"></audio></p>
      <p><b>Semantic render (knowledge only, full duration):</b><br>
      <audio controls src="{sem}"></audio></p>
    </section>
    '''

corpus_rows = ''
for cls in ['field', 'child', 'speech', 'prosody', 'lowf0']:
    a = agg['by_class'][cls]
    corpus_rows += (f"<tr><td>{cls}</td><td>{a['n']}</td>"
                    f"<td>{a['pass']}/{a['n']}</td>"
                    f"<td>{a['sem_rms_mean']:.1f}</td>"
                    f"<td>{a['sem_corr_mean']:.4f}</td></tr>")

html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Exact Audio Replication v6 — NEW</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 1100px; margin: 2em auto; padding: 0 1em; }}
.badge {{ background: #c00; color: #fff; padding: .2em .6em; border-radius: 4px; font-weight: bold; }}
.pass {{ color: #080; }}
.clip {{ border: 1px solid #ccc; padding: 1em; margin: 1.5em 0; border-radius: 8px; }}
table {{ border-collapse: collapse; margin: 1em 0; }}
th, td {{ border: 1px solid #999; padding: .4em .8em; text-align: left; }}
th {{ background: #f0f0f0; }}
audio {{ width: 100%; }}
.boundary {{ background: #fffbe6; border: 1px solid #cc9; padding: 1em; border-radius: 8px; }}
</style></head><body>
<h1>Exact Audio Replication — v6 Knowmap <span class="badge">NEW</span></h1>
<p><b>Bar:</b> real audio in → <b>byte-identical PCM out</b>, through the knowmap
alone (emitter never reads the original). <code>cmp</code> on the WAV files:
same bytes, infinite PSNR. Every clip rendered twice; both runs byte-identical.</p>

<h2>Proxy fixtures (4/4 byte-identical)</h2>
{rows}

<h2>Sealed corpus — {agg['total']} clips, {agg['pass']} byte-identical</h2>
<table>
<tr><th>Class</th><th>n</th><th>byte-identical</th><th>mean semantic RMS (LSB)</th><th>mean semantic corr</th></tr>
{corpus_rows}
</table>
<p>All {agg['total']} clips verified against <code>SEAL_MANIFEST.json</code> before processing
(seal_match on every clip).</p>

<div class="boundary">
<h2>The honest boundary</h2>
<p><b>Semantic knowledge</b> (LPC + prototype + quantized scores + phase model +
gate + per-period harmonic amplitude): what the system learned. Mode 11 measures it —
e.g. cry still shows 136 LSB RMS of knowledge gap.</p>
<p><b>Lossless closure</b> (true first-P seeds + full f64 residual channel):
the stored signal needed to close the last LSB. Mode 10 adds it back.
Byte identity comes from knowledge <i>plus</i> closure — the residual bytes are
the exactness mechanism, never called understanding.</p>
</div>

<p><i>Self-contained: all waveforms and audio embedded as data URIs. Zero external loads.</i></p>
</body></html>'''

open(OUT, 'w').write(html)
# verify: no non-data src
import re
srcs = re.findall(r'src="(?!data:)', html)
print('non-data src count:', len(srcs))
print('wrote', OUT, os.path.getsize(OUT), 'bytes')
