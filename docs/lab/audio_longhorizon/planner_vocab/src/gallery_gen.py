#!/usr/bin/env python3
"""gallery_gen.py — self-contained gallery for the B-F1 planner/vocabulary verdict.
All WAVs embedded as data URIs; zero external loads. NEW-badged.
Usage: gallery_gen.py <planner_vocab_dir> <out_html>
Reads: evidence/analysis.json, VOCAB.md, runs/fresh (new renders),
       trials_control/runs/loopfresh (old 5-action renders).
Cases are picked from analysis.json: biggest win, a hold, an unexpressible
(if any), and d1 (the contour-growth showcase).
"""
import base64, json, os, sys, re

PV = sys.argv[1]
OUT = sys.argv[2]
TC = '/home/hatch/workspace/audio_longhorizon/trials_control'

def uri(path):
    with open(path, 'rb') as f:
        b = base64.b64encode(f.read()).decode()
    return 'data:audio/wav;base64,' + b

def audio_row(label, path):
    return ('<div class="clip"><div class="lbl">%s</div>'
            '<audio controls preload="none" src="%s"></audio></div>') % (label, uri(path))

an = json.load(open(os.path.join(PV, 'evidence', 'analysis.json')))
fresh = an['runs']['fresh']['cases']
# pick cases
by_improve = sorted(fresh, key=lambda c: c['errs'][0] - c['errs'][3], reverse=True)
best = by_improve[0]['depth']
worst = by_improve[-1]['depth']
# a hold case: smallest |err3-err0|
holds = sorted(fresh, key=lambda c: abs(c['errs'][3] - c['errs'][0]))
hold = holds[0]['depth']
picks = []
for d in (1, best, hold, worst):
    if d not in picks:
        picks.append(d)

def ref_of(depth):
    for line in open(os.path.join(TC, 'targets', 'loop20.txt')):
        pass
    lines = open(os.path.join(TC, 'targets', 'loop20.txt')).read().strip().split('\n')
    return lines[depth - 1].split(' ', 1)[1]

def ev_table(run):
    r = an['runs'][run]
    def pf(v, bar, lo=True):
        ok = (v <= bar) if lo else (v >= bar)
        return '%.3f %s' % (v, 'PASS' if ok else 'FAIL')
    rows = [
        ('ERR(3)/ERR(0) ≤ 0.80', pf(r['err_ratio'], 0.80)),
        ('Wilcoxon p < 0.01', '%.4g %s' % (r['wilcoxon_p'], 'PASS' if r['wilcoxon_p'] < 0.01 else 'FAIL')),
        ('≥16/20 improve', '%d/20 %s' % (r['strictly_improved'], 'PASS' if r['strictly_improved'] >= 16 else 'FAIL')),
        ('sign agreement ≥ 80%', '%.1f%% %s' % (100 * r['sign_agree_rate'], 'PASS' if r['sign_agree_rate'] >= 0.80 else 'FAIL')),
        ('unstable cases', str(r['unstable'])),
        ('sawtooth cases', str(r['sawtooth'])),
    ]
    return ''.join('<tr><td>%s</td><td>%s</td></tr>' % t for t in rows)

def case_notes(depth):
    j = open(os.path.join(PV, 'runs', 'fresh', 'journal.txt')).read()
    seg = []
    cap = False
    for line in j.split('\n'):
        if line.startswith('TARGET %d ' % depth):
            cap = True; seg = [line]; continue
        if cap:
            if line.startswith('TARGET '):
                break
            seg.append(line)
    notes = []
    for line in seg:
        if 'DELIBERATED grown' in line or 'DELIBERATED extended' in line:
            notes.append(line.strip())
        if 'no-progress-hold' in line and 'reason=no-progress-hold' in line:
            notes.append('held: ' + line.strip()[:160])
        if 'UNEXPRESSIBLE' in line:
            notes.append(line.strip())
    return notes[:4]

vocab = open(os.path.join(PV, 'VOCAB.md')).read()
# vocab table rows only
vrows = [l for l in vocab.split('\n') if l.startswith('| A')]

cases_html = []
for d in picks:
    c = [x for x in fresh if x['depth'] == d][0]
    e = c['errs']
    ref = ref_of(d)
    refname = os.path.basename(ref)
    nr = os.path.join(PV, 'runs', 'fresh')
    old = os.path.join(TC, 'runs', 'loopfresh')
    clips = []
    clips.append(audio_row('reference (real clip)', ref))
    clips.append(audio_row('OLD 5-action: open-loop iter0', os.path.join(old, 'l%03d_iter0.wav' % d)))
    clips.append(audio_row('OLD 5-action: closed-loop iter3', os.path.join(old, 'l%03d_iter3.wav' % d)))
    clips.append(audio_row('NEW planner: open-loop iter0', os.path.join(nr, 'l%03d_iter0.wav' % d)))
    clips.append(audio_row('NEW planner: closed-loop iter3', os.path.join(nr, 'l%03d_iter3.wav' % d)))
    notes = ''.join('<li><code>%s</code></li>' % n for n in case_notes(d))
    cases_html.append('''
    <section class="case">
      <h3>Case d%d — <span class="mono">%s</span></h3>
      <p>Frozen-scorer ERR: iter0=%.3f → iter3=%.3f (f0_ref=%.1f Hz)%s%s</p>
      <div class="clips">%s</div>
      <ul class="notes">%s</ul>
    </section>''' % (d, refname, e[0], e[3], c['f0_ref'],
                     ' — SAWTOOTH' if c['sawtooth'] else '',
                     ' — UNSTABLE' if c['unstable'] else '',
                     ''.join(clips), notes or '<li>no growth events</li>'))

html = ('<!DOCTYPE html>\n'
'<html><head><meta charset="utf-8">\n'
'<title>NEW — B-F1 unified planner/vocabulary: closed-loop verdict</title>\n'
'<style>\n'
'body{font-family:system-ui,sans-serif;max-width:1000px;margin:2em auto;padding:0 1em;color:#1a1a1a}\n'
'.badge{display:inline-block;background:#0a7d2c;color:#fff;font-weight:700;padding:.2em .7em;border-radius:6px;margin-right:.6em}\n'
'.mono{font-family:ui-monospace,monospace;font-size:.9em}\n'
'table{border-collapse:collapse;margin:1em 0}td,th{border:1px solid #bbb;padding:.35em .7em;text-align:left}\n'
'.case{border:1px solid #ccc;border-radius:8px;padding:1em;margin:1.2em 0;background:#fafafa}\n'
'.clips{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:.6em}\n'
'.clip .lbl{font-size:.85em;font-weight:600;margin-bottom:.2em}\n'
'audio{width:100%}\n'
'.notes{font-size:.82em;color:#333}code{font-size:.85em}\n'
'h1{font-size:1.4em}h2{margin-top:1.6em}\n'
'.warn{background:#fff4e0;border:1px solid #e0a800;border-radius:6px;padding:.6em 1em}\n'
'</style></head><body>\n'
'<h1><span class="badge">NEW</span>B-F1 unified planner/vocabulary — closed-loop on real material</h1>\n'
'<p>2026-09-26. The planner grew its own action vocabulary from its measured\n'
'failures (no handed action set, no clamps), then re-ran the §2c closed-loop\n'
'battery on the same 20 real references. Numbers below are from the <b>frozen</b>\n'
'scorer — the planner\'s own native ERR never scores it.</p>\n'
'<h2>§2c battery vs bars (frozen scorer)</h2>\n'
'<h3>fresh state (vocabulary reset per target)</h3>\n'
'<table>' + ev_table('fresh') + '</table>\n'
'<h3>deep state (vocabulary accumulates across targets)</h3>\n'
'<table>' + ev_table('deep') + '</table>\n'
'<h2>What the planner grew (its recorded reasons)</h2>\n'
'<table><tr><th>ID</th><th>Form</th><th>Entered</th><th>Reason</th><th>Measured evidence</th></tr>\n'
+ ''.join('<tr>' + r + '</tr>' for r in vrows) + '</table>\n'
'<h2>Before / after — listen</h2>\n'
'<p>OLD = the 5-action renderer that failed §2c. NEW = the unified planner with\n'
'the grown vocabulary. iter0 is open-loop; iter3 is after 3 closed-loop corrections.</p>\n'
+ ''.join(cases_html) + '\n'
'<div class="warn"><b>How to read this:</b> the planner hears through its own\n'
'organ and optimizes its own native ERR; the frozen scorer judges independently.\n'
'Where PREDICT and measured diverge, the journal says so — that divergence is\n'
'reported in VERDICT.md, not hidden.</div>\n'
'</body></html>')

open(OUT, 'w').write(html)
print('wrote', OUT, os.path.getsize(OUT), 'bytes')
# self-containment check
srcs = re.findall(r'(?:src|href)="(.*?)"', html)
ext = [s for s in srcs if not s.startswith('data:')]
print('external refs:', ext if ext else 'NONE — self-contained OK')
print('audio elements:', len(re.findall(r'<audio', html)))
