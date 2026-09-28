#!/usr/bin/env python3
"""Scan the child corpus for the true source of the v1 child atom.

Method: for each candidate WAV, run the SAME harmonic extraction as
extract_atom.py (estimate_f0_autocorr + period-synchronous averaging with
the T/2 fallback), then normalized cross-correlation of the zero-mean
harmonic shapes (resampled to 256 bins). The true source must reproduce
the v1 harmonic at ~1.0 correlation; anything else is not the source.

Usage: find_child_source.py <v1_atom> <corpus_dir> <out_tsv>
"""
import sys, os, struct
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_atom import read_wav, estimate_f0_autocorr

def parse_v1_harm(path):
    b = open(path, 'rb').read()
    magic, ver = struct.unpack('<II', b[:8])
    assert magic == 0x4D4F5441 and ver == 1, (hex(magic), ver)
    T0 = struct.unpack('<d', b[8:16])[0]
    NBINS = struct.unpack('<q', b[16:24])[0]
    harm = np.array(struct.unpack('<%dd' % NBINS, b[24:24 + NBINS * 8]))
    return T0, harm

def extract_harm(x, sr, T0_hint):
    """Mirror of extract_atom.py's period-averaging block."""
    f0, seg_start = estimate_f0_autocorr(x, sr)
    if f0 < 60:
        return None, 0, 0
    T0 = sr / f0
    seg = x[seg_start:seg_start + sr].copy()
    if len(seg) < sr:
        seg = np.pad(seg, (0, sr - len(seg)))
    seg = seg - np.mean(seg)
    T_try = T0
    for _ in range(3):
        NBINS_try = int(round(T_try))
        if NBINS_try < 20:
            break
        nper_try = int(len(seg) / T_try) - 1
        if nper_try < 5:
            break
        pt = np.zeros((nper_try, NBINS_try))
        pos = 0.0
        for p in range(nper_try):
            idx = pos + np.arange(NBINS_try) * (T_try / NBINS_try)
            idx = np.clip(idx, 0, len(seg) - 1.001)
            i_lo = idx.astype(int)
            frac = idx - i_lo
            pt[p] = seg[i_lo] * (1 - frac) + seg[np.minimum(i_lo + 1, len(seg) - 1)] * frac
            pos += T_try
        h_try = np.mean(pt, axis=0)
        h_try = h_try - np.mean(h_try)
        zc_try = np.sum((h_try[:-1] * h_try[1:]) < 0)
        if zc_try == 2:
            return h_try, f0, seg_start
        T_try = T_try / 2.0
    return None, f0, seg_start

def shape_corr(a, b, n=256):
    """Normalized correlation of zero-mean shapes resampled to n bins."""
    ia = np.interp(np.linspace(0, 1, n), np.linspace(0, 1, len(a)), a)
    ib = np.interp(np.linspace(0, 1, n), np.linspace(0, 1, len(b)), b)
    ia = ia - np.mean(ia)
    ib = ib - np.mean(ib)
    na, nb = np.sqrt(np.sum(ia ** 2)), np.sqrt(np.sum(ib ** 2))
    if na < 1e-12 or nb < 1e-12:
        return 0.0
    return float(np.sum(ia * ib) / (na * nb))

def main():
    v1_atom, corpus_dir, out_tsv = sys.argv[1], sys.argv[2], sys.argv[3]
    T0_v1, harm_v1 = parse_v1_harm(v1_atom)
    f0_v1 = 44100.0 / T0_v1
    print(f"v1 child: T0={T0_v1:.3f} f0={f0_v1:.2f} Hz NBINS={len(harm_v1)}", flush=True)
    files = sorted(f for f in os.listdir(corpus_dir) if f.endswith('.wav'))
    rows = []
    for fi, fn in enumerate(files):
        p = os.path.join(corpus_dir, fn)
        try:
            sr, x = read_wav(p)
        except Exception as e:
            print(f"[{fi+1}/{len(files)}] {fn}: read FAIL {e}", flush=True)
            continue
        harm, f0, seg_start = extract_harm(x, sr, T0_v1)
        if harm is None:
            print(f"[{fi+1}/{len(files)}] {fn}: no voiced f0 (f0={f0:.1f})", flush=True)
            rows.append((fn, f0, seg_start, float('nan')))
            continue
        c = shape_corr(harm_v1, harm)
        print(f"[{fi+1}/{len(files)}] {fn}: f0={f0:7.2f} seg={seg_start:8d} corr={c:+.6f}", flush=True)
        rows.append((fn, f0, seg_start, c))
    rows.sort(key=lambda r: (r[3] != r[3], -(r[3] if r[3] == r[3] else -2)))
    with open(out_tsv, 'w') as f:
        f.write("file\tf0_hz\tseg_start\tcorr\n")
        for fn, f0, ss, c in rows:
            f.write(f"{fn}\t{f0:.2f}\t{ss}\t{c:.6f}\n")
    print(f"wrote {out_tsv}", flush=True)
    print("TOP 10:")
    for fn, f0, ss, c in rows[:10]:
        print(f"  {c:+.6f} {fn} f0={f0:.1f}")

if __name__ == '__main__':
    main()
