#!/usr/bin/env python3
"""Phase-3 final analysis: per-class semantic + residual-share comparison.
Reads battery3.log + baseline_decomp.json + phase-2 CSV.
Writes results/final_comparison.txt and results/final_comparison.json.
"""
import json, csv, os, math, collections
import numpy as np

P3 = os.path.expanduser('~/workspace/exact_audio_replication/phase3/results')
P2CSV = os.path.expanduser('~/workspace/exact_audio_replication/phase2/results/corpus_results_v6intake.csv')

def parse_battery():
    new = {}
    for ln in open(os.path.join(P3, 'battery3.log')):
        p = ln.strip().split('\t')
        if len(p) < 2 or p[1] != 'OK':
            continue
        d = {}
        for t in p[2:]:
            k, v = t.split('=', 1)
            try: d[k] = float(v) if '.' in v or 'e' in v.lower() else int(v)
            except: d[k] = v
        # byte_ident is bool-ish string
        d['byte_ident'] = (d.get('byte_ident') == 'True' or d.get('byte_ident') is True)
        new[p[0]] = d
    # fix byte_ident parsing (it came as 'True' string)
    for ln in open(os.path.join(P3, 'battery3.log')):
        p = ln.strip().split('\t')
        if len(p) >= 2 and p[1] == 'OK':
            new[p[0]]['byte_ident'] = ('byte_ident=True' in ln)
    return new

def main():
    new = parse_battery()
    base = {o['name']: o for o in json.load(open(os.path.join(P3, 'baseline_decomp.json')))}
    p2 = {r['name']: r for r in csv.DictReader(open(P2CSV))}
    print(f"battery clips: {len(new)}, baseline clips: {len(base)}")
    green = sum(1 for d in new.values() if d['byte_ident'])
    print(f"GATE: {green}/{len(new)} byte-identical (mode 10)")
    # per-class aggregates
    cls = collections.defaultdict(list)
    for name, d in new.items():
        if name not in base: continue
        c = name.split('-')[0]
        cls[c].append((base[name], d))
    out = {}
    print(f"\n{'class':<8} {'n':>4} {'sem_rms base':>12} {'sem_rms new':>11} {'gain%':>6} "
          f"{'corr base':>9} {'corr new':>8} {'nres base':>9} {'nres new':>8} {'nres gain%':>9}")
    for c in sorted(cls):
        v = cls[c]; n = len(v)
        sb = np.mean([b['sem_rms'] for b, d in v]); sn = np.mean([d['sem_rms'] for b, d in v])
        cb = np.mean([b['sem_corr'] for b, d in v]); cn = np.mean([d['sem_corr'] for b, d in v])
        nb = np.mean([b['nres_rms'] for b, d in v]); nn = np.mean([d['nres_rms'] for b, d in v])
        # residual bytes: gzip of nres section — use fsize delta as proxy + report impulse overhead
        print(f"{c:<8} {n:>4} {sb:>12.1f} {sn:>11.1f} {100*(sb-sn)/sb:>5.1f}% "
              f"{cb:>9.4f} {cn:>8.4f} {nb:>9.1f} {nn:>8.1f} {100*(nb-nn)/nb:>8.1f}%")
        out[c] = dict(n=n, sem_rms_base=sb, sem_rms_new=sn, corr_base=cb, corr_new=cn,
                      nres_base=nb, nres_new=nn)
    # H4 accepted clips
    print("\nH4 r2-gated acceptances (r2acc>0.10):")
    for name, d in sorted(new.items(), key=lambda kv: -kv[1].get('r2acc', 0)):
        if d.get('r2acc', 0) > 0.10 and name in base:
            b = base[name]
            print(f"  {name[:40]:<40} r2acc={d['r2acc']:.3f} sem {b['sem_rms']:.1f} -> {d['sem_rms']:.1f} "
                  f"({100*(b['sem_rms']-d['sem_rms'])/b['sem_rms']:+.1f}%) use_h was {b['use_h']}")
    # use_h counts
    uh_new = sum(1 for d in new.values() if d.get('use_h') == 1)
    uh_base = sum(1 for b in base.values() if b['use_h'] == 1)
    print(f"\nuse_h: baseline {uh_base} -> phase-3 {uh_new}")
    # HF check
    print("\nHF 12k+/16k+ ratios (new; 1.0 = matches source):")
    for c in sorted(cls):
        v = cls[c]
        h12 = np.mean([d.get('hf12x', 1) for b, d in v]); h16 = np.mean([d.get('hf16x', 1) for b, d in v])
        print(f"  {c:<8} 12-16k x{h12:.3f}  16k+ x{h16:.3f}")
    # worst regressions (honesty)
    regs = [(name, (base[name]['sem_rms']-d['sem_rms'])/base[name]['sem_rms'])
            for name, d in new.items() if name in base]
    regs.sort(key=lambda t: t[1])
    print("\nsmallest gains (honest tail):")
    for name, g in regs[:5]:
        print(f"  {name[:40]:<40} gain {g*100:+.1f}%")
    json.dump(out, open(os.path.join(P3, 'final_comparison.json'), 'w'), indent=1)
    print("\nanalyzed OK")

if __name__ == '__main__':
    main()
