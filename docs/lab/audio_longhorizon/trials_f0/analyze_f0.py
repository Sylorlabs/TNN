#!/usr/bin/env python3
# analyze_f0.py — OFFLINE analyzer for the F0 blind-spot attack (Phase B2c).
# Examiner, never examinee: reads Zag binary outputs + sealed corpus artifacts,
# aligns them, computes the prereg §4 bars. Pure statistics.
#
# GROUND TRUTH (corrected 2026-09-26 after column audit): PTDB-TUG .f0 rows are
# "c1 c2 c3 c4" where c2 is the laryngograph voicing flag (1.0=voiced),
# c1 is the laryngograph F0 in Hz when voiced (0.0 when unvoiced). Column c3
# (used by LOWF0_REPORT.md and by earlier revisions of this analyzer) is NOT
# the reference F0: it is garbage (750-1819 Hz) exactly in voiced frames and
# disagrees with c1 by median 74% where both are present. Voiced+inband frame
# totals below use c1/c2. The sealed WAV/.f0 fixtures are unchanged.
#
# Alignment: WAV clip = 5.0 s window starting at manifest window_start_s into
# the original PTDB utterance; .f0 frames are 10 ms over the original. The
# estimator frame f (2048-sample window, 1024 hop @44100) centers at
# t=(f*1024+1024)/44100 s of clip time; reference frame k centers at
# (k+0.5)*0.01 s of original time. Alignment validated in RUNLOG (systematic
# error minimum at the manifest offset).
import json, math, os, sys, glob

CORPUS = os.path.expanduser('~/workspace/audio_longhorizon/corpus')
LOWF0 = os.path.join(CORPUS, 'lowf0')
TRIALS = os.path.expanduser('~/workspace/audio_longhorizon/trials_f0')

def load_manifest():
    man = json.load(open(os.path.join(CORPUS, 'CLIP_MANIFEST.json')))
    d = {}
    for e in man:
        if 'lowf0' in e['path']:
            d[e['clip_id']] = (e['conversion']['window_start_s'], e['path'])
    return d

def load_lx(path):
    """Return (f0_c1 list, voiced_c2 list)."""
    f0, v = [], []
    with open(path) as fh:
        for line in fh:
            p = line.split()
            if len(p) < 2:
                continue
            f0.append(float(p[0]))
            v.append(1 if float(p[1]) == 1.0 else 0)
    return f0, v

def load_probe(path):
    frames = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line.startswith('fr='):
                continue
            d = {}
            for tok in line.split():
                k, vv = tok.split('=')
                d[k] = int(vv)
            frames.append(d)
    return frames

def band_of(r):
    if r < 80:
        return 'b1'
    if r < 100:
        return 'b2'
    return 'b3'

def is_octave(est_hz, ref_hz):
    if ref_hz <= 0 or est_hz <= 0:
        return False
    return (abs(est_hz - ref_hz / 2) / (ref_hz / 2) < 0.08 or
            abs(est_hz - 2 * ref_hz) / (2 * ref_hz) < 0.08)

def analyze_set(tag, probe_files, man, est_key='lf0', conf_key='lst'):
    """Score one estimator/guard output set over all clips.

    est_key/conf_key: probe columns for the estimate (mHz int) and the
    confident flag. 'lst' -> lf0/lst==1; 'gv' -> gf0/gv==1; 'sv' -> sf0/sv==1.
    """
    bands = {b: {'n': 0, 'conf': 0, 'within5': 0, 'oct': 0, 'cw': 0,
                 'errs': [], 'floor_min': None} for b in ('b1', 'b2', 'b3')}
    v_n = 0       # truth-voiced aligned frames
    v_miss = 0    # truth-voiced inband but estimator unvoiced/abstained
    u_n = 0       # truth-unvoiced aligned frames
    u_false = 0   # truth-unvoiced but estimator voiced confident
    oob_n = 0     # truth-voiced but F0 outside [55,125]
    oob_conf = 0  # ... and estimator confident (confidently-wrong by construction)
    jit = []
    prev = None
    n_align = 0
    for cid, path in probe_files:
        wstart = man[cid][0]
        f0v, vv = load_lx(os.path.join(LOWF0, cid + '.f0'))
        frames = load_probe(path)
        for fr in frames:
            t = (fr['fr'] * 1024 + 1024) / 44100.0
            k = int(round((t + wstart) / 0.01 - 0.5))
            if not (0 <= k < len(f0v)):
                continue
            n_align += 1
            voiced = vv[k] == 1
            r = f0v[k]
            if conf_key == 'lst':
                confident = fr.get('lst', 0) == 1
                est = fr.get('lf0', 0) / 1000.0
            elif conf_key == 'gv':
                confident = fr.get('gv', 0) == 1
                est = fr.get('gf0', 0) / 1000.0
            else:
                confident = fr.get('sv', 0) == 1
                est = fr.get('sf0', 0) / 1000.0
            if voiced:
                v_n += 1
                if not (55 <= r <= 125):
                    oob_n += 1
                    if confident:
                        oob_conf += 1
                    prev = None
                    continue
                b = band_of(r)
                bands[b]['n'] += 1
                if confident and est > 0:
                    bands[b]['conf'] += 1
                    e = abs(est - r) / r
                    bands[b]['errs'].append(e)
                    if e <= 0.05:
                        bands[b]['within5'] += 1
                    elif e > 0.20:
                        bands[b]['cw'] += 1
                        if is_octave(est, r):
                            bands[b]['oct'] += 1
                    if bands[b]['floor_min'] is None or r < bands[b]['floor_min']:
                        bands[b]['floor_min'] = r
                else:
                    v_miss += 1
                cur = (fr['fr'], est if confident else None, r)
                if prev is not None and confident and prev[1] is not None:
                    de = abs(est - prev[1])
                    dr = abs(r - prev[2])
                    denom = (est + prev[1]) / 2
                    if denom > 0:
                        jit.append(abs(de - dr) / denom)
                prev = cur
            else:
                u_n += 1
                if confident:
                    u_false += 1
                prev = None
    for b in bands:
        bands[b]['errs'].sort()
    jit.sort()
    N = sum(bands[b]['n'] for b in bands)
    C = sum(bands[b]['conf'] for b in bands)
    W = sum(bands[b]['within5'] for b in bands)
    return {
        'tag': tag, 'bands': bands, 'n_align': n_align,
        'N': N, 'C': C, 'W': W,
        'v_n': v_n, 'v_miss': v_miss, 'u_n': u_n, 'u_false': u_false,
        'oob_n': oob_n, 'oob_conf': oob_conf,
        'jit': jit,
    }

def pct(a, b):
    return (a / b) if b else 0.0

def report(res):
    L = []
    L.append('=== %s ===' % res['tag'])
    L.append('aligned frames=%d truth-voiced=%d truth-unvoiced=%d' % (
        res['n_align'], res['v_n'], res['u_n']))
    L.append('inband voiced frames N=%d confident C=%d (coverage %.4f) within5 W=%d' % (
        res['N'], res['C'], pct(res['C'], res['N']), res['W']))
    L.append('HEADLINE within5/N (abstentions count as misses) = %.4f  [FIXED bar >= 0.90]' % pct(res['W'], res['N']))
    L.append('within5/C (of confident) = %.4f' % pct(res['W'], res['C']))
    L.append('voiced miss rate (truth-voiced inband, estimator silent) = %.4f  [%d/%d]' % (
        pct(res['v_miss'], res['N']), res['v_miss'], res['N']))
    L.append('unvoiced false-voice rate (truth-unvoiced, estimator confident) = %.4f  [%d/%d]' % (
        pct(res['u_false'], res['u_n']), res['u_false'], res['u_n']))
    L.append('truth-voiced but F0 outside [55,125]: n=%d estimator-confident=%d' % (
        res['oob_n'], res['oob_conf']))
    for b in ('b1', 'b2', 'b3'):
        d = res['bands'][b]
        e = d['errs']
        n = len(e)
        med = e[n // 2] if n else -1
        p90 = e[int(0.9 * n)] if n else -1
        mx = e[-1] if n else -1
        L.append(' %s: n=%d conf=%d within5=%d within5/n=%.4f med=%.4f p90=%.4f max=%.4f oct=%d cw_non_oct=%d floor_min=%s' % (
            b, d['n'], d['conf'], d['within5'], pct(d['within5'], d['n']),
            med, p90, mx, d['oct'], d['cw'] - d['oct'],
            ('%.1f' % d['floor_min']) if d['floor_min'] else 'none'))
    j = res['jit']
    if j:
        L.append('jitter |d_est-d_ref|/mean: n=%d med=%.4f p90=%.4f' % (
            len(j), j[len(j) // 2], j[int(0.9 * len(j))]))
    else:
        L.append('jitter: n=0')
    return '\n'.join(L)

def main():
    man = load_manifest()
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    outs = []
    if which in ('all', 'orig'):
        files = []
        for cid in sorted(man):
            p = os.path.join(TRIALS, 'out', 'probe_%s_r1.txt' % cid.split('-')[2])
            if os.path.exists(p):
                files.append((cid, p))
        if files:
            outs.append(report(analyze_set('ORIGINAL guard: lowband estimator (lf0/lst)', files, man)))
            outs.append(report(analyze_set('ORIGINAL guard: guard-low output (gf0/gv)', files, man,
                                            est_key='gf0', conf_key='gv')))
            outs.append(report(analyze_set('ORIGINAL guard: scope output (sf0/sv)', files, man,
                                            est_key='sf0', conf_key='sv')))
    if which in ('all', 'v2', 'fast'):
        tag = 'v2' if which in ('all', 'v2') else 'fast'
        files = []
        for cid in sorted(man):
            p = os.path.join(TRIALS, 'out', '%s_%s_r1.txt' % (tag, cid.split('-')[2]))
            if os.path.exists(p):
                files.append((cid, p))
        if files:
            outs.append(report(analyze_set('V2 estimator (lf0/lst)', files, man)))
            if which != 'fast':
                outs.append(report(analyze_set('V2 guard-low output (gf0/gv)', files, man,
                                                est_key='gf0', conf_key='gv')))
                outs.append(report(analyze_set('V2 scope output (sf0/sv)', files, man,
                                                est_key='sf0', conf_key='sv')))
    print('\n\n'.join(outs))

if __name__ == '__main__':
    main()
