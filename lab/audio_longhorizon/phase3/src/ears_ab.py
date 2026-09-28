#!/usr/bin/env python3
"""Phase-3 ears test: blind A/B (semantic-old vs semantic-new) + waveform analysis.
Picks top-improved clips per class from battery3.log, plus 1 honest small-gain clip.
Builds a self-contained HTML gallery (data URIs, NEW-badged) under ~/workspace/your_files/.
"""
import struct, sys, os, csv, json, math, base64, subprocess, random
import numpy as np

P2RUN = os.path.expanduser('~/workspace/exact_audio_replication/phase2/run/full_v6')
P3RUN = os.path.expanduser('~/workspace/exact_audio_replication/phase3/run/full_v3')
P3BUILD = os.path.expanduser('~/workspace/exact_audio_replication/phase3/build')
CSV = os.path.expanduser('~/workspace/exact_audio_replication/phase2/results/corpus_results_v6intake.csv')
OUTDIR = os.path.expanduser('~/workspace/your_files/audio_phase3_AB')

def read_wav_samples(path):
    d = open(path, 'rb').read()
    off = 12
    while off + 8 < len(d):
        if d[off:off+4] == b'data':
            sz = struct.unpack('<I', d[off+4:off+8])[0]
            n = sz // 2
            return np.frombuffer(d[off+8:off+8+2*n], dtype='<i2').astype(np.float64)
        sz = struct.unpack('<I', d[off+4:off+8])[0]
        off += 8 + sz
    raise ValueError('no data')

def wav_datauri(path, label):
    raw = open(path, 'rb').read()
    b64 = base64.b64encode(raw).decode()
    return f'data:audio/wav;base64,{b64}'

def band_energy(x, sr, edges):
    n = len(x); w = np.hanning(n)
    X = np.abs(np.fft.rfft(x*w))**2
    fr = np.fft.rfftfreq(n, 1.0/sr)
    tot = X.sum() + 1e-30
    return [float(X[(fr>=edges[i])&(fr<edges[i+1])].sum()/tot) for i in range(len(edges)-1)]

def analyze(path, sr=44100):
    x = read_wav_samples(path)
    n = len(x)
    rms = float(np.sqrt((x**2).mean()))
    peak = float(np.abs(x).max())
    zc = float(((x[:-1] < 0) != (x[1:] < 0)).sum() / (n/sr))  # zero-crossings/sec
    edges = [0, 250, 1000, 4000, 8000, 12000, 16000, sr/2]
    be = band_energy(x, sr, edges)
    # HNR via FFT autocorrelation on a 2-sec center excerpt (fast, deterministic)
    seg = x[n//2-44100:n//2+44100] if n > 88200 else x
    m = len(seg)
    a = seg - seg.mean()
    F = np.fft.rfft(a, n=2*m)
    ac = np.fft.irfft(F*np.conj(F), n=2*m)[:2000]
    ac = ac / (ac[0] + 1e-30)
    pk = float(ac[20:].max())
    hnr = float(10*np.log10(max(pk,1e-6)/max(1-pk,1e-6))) if pk < 0.999 else 99.0
    # envelope stationarity: std of 10ms RMS envelope / mean
    hop = sr // 100
    env = np.array([np.sqrt((x[i*hop:(i+1)*hop]**2).mean()) for i in range(n//hop)])
    env_cv = float(env.std() / (env.mean() + 1e-30))
    return dict(rms=rms, peak=peak, zc_per_s=zc, bands=be, hnr_db=hnr, env_cv=env_cv, n=n)

def main():
    # parse battery log
    new = {}
    for ln in open(os.path.expanduser('~/workspace/exact_audio_replication/phase3/results/battery3.log')):
        p = ln.strip().split('\t')
        if len(p) < 2 or p[1] != 'OK': continue
        d = dict(t.split('=') for t in p[2:])
        new[p[0]] = d
    base = {o['name']: o for o in json.load(open(
        os.path.expanduser('~/workspace/exact_audio_replication/phase3/results/baseline_decomp.json')))}
    # improvement per clip
    scored = []
    for name, d in new.items():
        if name in base and d.get('byte_ident') == 'True':
            imp = (base[name]['sem_rms'] - float(d['sem_rms'])) / base[name]['sem_rms']
            scored.append((imp, name))
    scored.sort(reverse=True)
    by_cls = {}
    for imp, name in scored:
        c = name.split('-')[0]
        by_cls.setdefault(c, []).append((imp, name))
    # pick: best per class + 1 smallest-gain (honest)
    picks = []
    for c in sorted(by_cls):
        picks.append((c, by_cls[c][0][1], by_cls[c][0][0], 'best'))
    worst = scored[-1]
    picks.append((worst[1].split('-')[0], worst[1], worst[0], 'smallest-gain'))
    rows = {r['name']: r for r in csv.DictReader(open(CSV))}
    os.makedirs(OUTDIR, exist_ok=True)
    rng = random.Random(20260926)  # deterministic blind order
    cards = []
    analysis = {}
    for cls, name, imp, kind in picks:
        src = rows[name]['clip']
        old_wav = os.path.join(P2RUN, name, 'sem.wav')
        m3 = os.path.join(P3RUN, name, 'm3.v6')
        new_wav = os.path.join(OUTDIR, f'{name}.new.wav')
        old_wav_c = os.path.join(OUTDIR, f'{name}.old.wav')
        subprocess.run([os.path.join(P3BUILD, 'reemit63'), m3, '11', new_wav],
                       capture_output=True, timeout=300)
        # copy old (phase-2 sem.wav) for the gallery
        open(old_wav_c, 'wb').write(open(old_wav, 'rb').read())
        a_old = analyze(old_wav_c); a_new = analyze(new_wav); a_src = analyze(src)
        analysis[name] = dict(old=a_old, new=a_new, src=a_src, imp=imp, kind=kind)
        # blind: randomly assign A/B
        if rng.random() < 0.5:
            A, B, Awhich = old_wav_c, new_wav, 'old'
        else:
            A, B, Awhich = new_wav, old_wav_c, 'new'
        cards.append(dict(name=name, cls=cls, imp=imp, kind=kind,
                          Auri=wav_datauri(A, 'A'), Buri=wav_datauri(B, 'B'),
                          Awhich=Awhich))
    json.dump(analysis, open(os.path.join(OUTDIR, 'waveform_analysis.json'), 'w'), indent=1)
    # reveal key (for after listening)
    reveal = {c['name']: c['Awhich'] for c in cards}
    json.dump(reveal, open(os.path.join(OUTDIR, 'reveal_key.json'), 'w'), indent=1)
    # build HTML
    band_names = ['0-250', '250-1k', '1k-4k', '4k-8k', '8k-12k', '12k-16k', '16k+']
    html = ['''<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Phase-3 Semantic Growth — Blind A/B (NEW)</title>
<style>body{font-family:system-ui,sans-serif;max-width:1000px;margin:2em auto;padding:0 1em;background:#fafafa}
.badge{display:inline-block;background:#c00;color:#fff;font-weight:700;padding:.2em .8em;border-radius:1em;margin-bottom:1em}
.card{background:#fff;border:1px solid #ddd;border-radius:12px;padding:1.2em;margin:1.5em 0}
audio{width:100%} table{border-collapse:collapse;margin:.8em 0;font-size:.85em}
td,th{border:1px solid #ddd;padding:.3em .6em;text-align:right} th{background:#f0f0f0}
.reveal{color:#888;font-size:.8em}</style></head><body>
<span class="badge">NEW</span>
<h1>Phase-3 Semantic Growth — Blind A/B Listening</h1>
<p>Each card: <b>A</b> and <b>B</b> are the OLD (phase-2) and NEW (phase-3) semantic renders in
random order. Waveform analysis (measured, not heard) is shown under each. The reveal key is at the
bottom — listen first.</p>''']
    for c in cards:
        an = analysis[c['name']]
        def row(lbl, d):
            bands = ' '.join(f'{v*100:.1f}%' for v in d['bands'])
            return (f"<tr><td>{lbl}</td><td>{d['rms']:.0f}</td><td>{d['peak']:.0f}</td>"
                    f"<td>{d['zc_per_s']:.0f}</td><td>{d['hnr_db']:.1f}</td>"
                    f"<td>{d['env_cv']:.3f}</td><td>{bands}</td></tr>")
        html.append(f'''<div class="card"><h2>{c['name']} <span class="reveal">({c['cls']}, {c['kind']}, semantic RMS gain {c['imp']*100:.1f}%)</span></h2>
<h3>A</h3><audio controls src="{c['Auri']}"></audio>
<h3>B</h3><audio controls src="{c['Buri']}"></audio>
<table><tr><th></th><th>RMS</th><th>peak</th><th>zc/s</th><th>HNR dB</th><th>env CV</th><th>bands 0-250/250-1k/1k-4k/4k-8k/8k-12k/12k-16k/16k+</th></tr>
{row('source', an['src'])}{row('old', an['old'])}{row('new', an['new'])}</table></div>''')
    html.append('<h2>Reveal key (A = which?)</h2><ul>')
    for c in cards:
        html.append(f"<li>{c['name']}: A = <b>{c['Awhich']}</b></li>")
    html.append('</ul><p class="reveal">Phase-3: transient-event channel + joint per-period amplitude. '
                'All renders deterministic, zero RNG. Gate 359/359 byte-identical held.</p></body></html>')
    open(os.path.join(OUTDIR, 'index.html'), 'w').write('\n'.join(html))
    # verify self-contained: no non-data src
    h = open(os.path.join(OUTDIR, 'index.html')).read()
    import re
    bad = re.findall(r'src="(?!data:)[^"]+"', h)
    print('cards:', len(cards), 'non-data src refs:', bad)
    print('wrote', os.path.join(OUTDIR, 'index.html'))

if __name__ == '__main__':
    main()
