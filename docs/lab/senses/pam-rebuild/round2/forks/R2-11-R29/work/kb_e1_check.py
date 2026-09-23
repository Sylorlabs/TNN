#!/usr/bin/env python3
"""KB-E1: fork A — every emitted payload byte must equal the cited source span.

Usage: kb_e1_check.py <forkA_run_base>
Joins percepts.tsv selections with artifacts/ and the source fixtures.
Reports per-artifact match/mismatch counts. Fork B is not checked here
(its divergence is declared and scored under KB-E7).
"""
import struct, sys, os, glob

def u32(b, o): return struct.unpack('<I', b[o:o+4])[0]

def main():
    base = sys.argv[1]
    P = []
    for tsv in sorted(glob.glob(base + '_sh?/percepts.tsv')):
        for l in open(tsv).read().splitlines()[1:]:
            P.append(l.split('\t'))
    # trial ids repeat across harness tasks -> artifact names collide and the
    # binary overwrites. Restrict KB-E1 to unique trial ids (all r211g_*).
    from collections import Counter
    _c = Counter(r[0] for r in P)
    _uniq = {k for k, v in _c.items() if v == 1}
    P = [r for r in P if r[0] in _uniq]
    print(f"KB-E1: checking {len(P)} rows with unique trial ids")
    art_dirs = sorted(glob.glob(base + '_sh?/artifacts'))
    arts = {}
    for d in art_dirs:
        for e in os.listdir(d):
            arts[e] = os.path.join(d, e)

    n_ok = n_bad = n_missing = 0
    bad = []
    for r in P:
        trial = r[0]
        nsel = int(r[7])
        sels = r[8].split(';') if r[8] else []
        src = open(r[2], 'rb').read()
        for i in range(nsel):
            kind_s, rest = sels[i].split(':')
            kind = int(kind_s)
            v = [int(x) for x in rest.split(',')]
            ext = '.aud' if kind == 0 else '.img' if kind == 1 else '.vid'
            name = f"{trial}.e{i}{ext}"
            ap = arts.get(name)
            if ap is None:
                n_missing += 1
                continue
            ab = open(ap, 'rb').read()
            if kind == 0:
                a, b = v[0], v[1]
                expect = src[a:b]
                got = ab[8:]
                hdr_ok = (u32(ab, 0) == u32(src, 0)) and (u32(ab, 4) == (b - a) // 2)
            elif kind == 1:
                x, y, rw, rh = v[0], v[1], v[2], v[3]
                sw = u32(src, 0)
                expect = b''.join(src[8 + ((y + yy) * sw + x) * 3: 8 + ((y + yy) * sw + x) * 3 + rw * 3]
                                  for yy in range(rh))
                got = ab[8:]
                hdr_ok = (u32(ab, 0) == rw) and (u32(ab, 4) == rh)
            else:
                x, y, rw, rh, f0, f1 = v
                sw, sh = u32(src, 4), u32(src, 8)
                fs = sw * sh * 3
                expect = b''.join(
                    b''.join(src[12 + (f0 + ff) * fs + ((y + yy) * sw + x) * 3:
                                   12 + (f0 + ff) * fs + ((y + yy) * sw + x) * 3 + rw * 3]
                            for yy in range(rh))
                    for ff in range(f1 - f0 + 1))
                got = ab[12:]
                hdr_ok = (u32(ab, 0) == f1 - f0 + 1) and (u32(ab, 4) == rw) and (u32(ab, 8) == rh)
            if hdr_ok and expect == got:
                n_ok += 1
            else:
                n_bad += 1
                if len(bad) < 5:
                    bad.append((name, len(expect), len(got), hdr_ok))
    print(f"KB-E1 fork A: ok={n_ok} bad={n_bad} missing={n_missing}")
    for b_ in bad:
        print('  BAD', b_)
    print('KB-E1:', 'PASS' if n_bad == 0 and n_missing == 0 else 'FAIL')

main()
