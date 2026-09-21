#!/usr/bin/env python3
"""Cross-validation: independent Python implementation of the NATIVE R0 arm
rules (as documented in ARM_SPEC.md), compared SEG-row-for-row against the
Zag binary output. Catches logic bugs AND native miscompiles (e.g.
ZNC-2026-09-19-001) that byte-identical reruns alone cannot see.

Usage: xcheck.py <arms_bin> <input.bin>...
Exit 0 iff every arm matches on every input.
"""
import subprocess, sys

MASK64 = (1 << 64) - 1

def fnv1a(data: bytes) -> int:
    h = 1469598103934665603
    for b in data:
        h = ((h ^ b) * 1099511628211) & MASK64
    return h

def signed(h: int) -> int:
    return h if h < (1 << 63) else h - (1 << 64)

def umod1000003(h: int) -> int:
    return signed(h) % 1000003

# ---------------- predictive_surprise ----------------
def arm_predictive_surprise(buf: bytes):
    n = len(buf)
    trans = {}
    prev = [0] * 256
    for i in range(1, n):
        a, b = buf[i - 1], buf[i]
        trans[(a, b)] = trans.get((a, b), 0) + 1
        prev[a] += 1
    have_th = False
    p18 = 0
    if trans:
        rows = []
        for (a, b), c in trans.items():
            pfx = ((4 * c + 1) << 32) // (4 * prev[a] + 256)
            rows.append((pfx, a, b))
        rows.sort()
        p18 = rows[(18 * (len(rows) - 1)) // 100][0]
        have_th = True
    def cut(i):
        a, b = buf[i - 1], buf[i]
        c = trans.get((a, b), 0)
        if not have_th:
            return False
        if c == 0:
            return True
        return ((4 * c + 1) << 32) // (4 * prev[a] + 256) <= p18
    segs = []
    start = 0
    for i in range(1, n):
        if cut(i):
            segs.append((start, i - start))
            start = i
    if n - start > 0:
        segs.append((start, n - start))
    counts = {}
    for s, l in segs:
        key = bytes(buf[s:s + l])
        counts[key] = counts.get(key, 0) + 1
    ranked = sorted([k for k, c in counts.items() if c >= 3],
                    key=lambda k: (-counts[k], k))[:256]
    inv = {k: i for i, k in enumerate(ranked)}
    out = []
    for s, l in segs:
        key = bytes(buf[s:s + l])
        if key in inv:
            out.append((s, l, inv[key], 's'))
        else:
            out.append((s, l, umod1000003(fnv1a(key)), 'l'))
    return out

# ---------------- fixed_window ----------------
def arm_fixed_window(buf: bytes, w: int):
    n = len(buf)
    out = []
    i = 0
    while i < n:
        l = min(w, n - i)
        out.append((i, l, umod1000003(fnv1a(buf[i:i + l])), 'f'))
        i += w
    return out

# ---------------- MDL shared ----------------
def mdl_fit(buf: bytes, grounded: bool):
    n = len(buf)
    counts = {}
    for i in range(n):
        h = 1469598103934665603
        for L in range(1, 13):
            if i + L > n:
                break
            h = ((h ^ buf[i + L - 1]) * 1099511628211) & MASK64
            if L >= 2:
                key = bytes(buf[i:i + L])
                counts[key] = counts.get(key, 0) + 1
    cands = []
    for key, c in counts.items():
        if c >= 4:
            sav = (len(key) - 1) * c - (len(key) + 3)
            if sav > 0:
                cands.append([sav, len(key), c, key])
    cands.sort(key=lambda e: (-e[0], -e[1], -e[2], e[3]))
    if grounded and cands:
        G = min(len(cands), 8192)
        gset = set(e[3] for e in cands[:G])
        tot = {}
        hist = {}
        for i in range(n):
            h = 1469598103934665603
            for L in range(1, 13):
                if i + L > n:
                    break
                h = ((h ^ buf[i + L - 1]) * 1099511628211) & MASK64
                if L >= 2:
                    key = bytes(buf[i:i + L])
                    if key in gset and i + L < n:
                        tot[key] = tot.get(key, 0) + 1
                        hh = hist.setdefault(key, [0] * 256)
                        hh[buf[i + L]] += 1
        for e in cands[:G]:
            key = e[3]
            t = tot.get(key, 0)
            if t > 0:
                mxn = max(hist[key])
                gfp = max((mxn * 256) // t - 1, 0)
                e[0] = e[0] + (gfp * e[2] * e[1]) // 256
        cands.sort(key=lambda e: (-e[0], -e[1], -e[2], e[3]))
    return [(e[3], ) for e in cands[:256]]

def mdl_segment(buf: bytes, motifs):
    n = len(buf)
    byfirst = {}
    for mi, (key,) in enumerate(motifs):
        byfirst.setdefault(key[0], []).append((len(key), mi, key))
    out = []
    i = 0
    while i < n:
        best = None
        for L, mi, key in byfirst.get(buf[i], []):
            if i + L <= n and bytes(buf[i:i + L]) == key:
                if best is None or L > best[0]:
                    best = (L, mi)
        if best is not None:
            out.append((i, best[0], best[1], 'm'))
            i += best[0]
        else:
            out.append((i, 1, buf[i], 'r'))
            i += 1
    return out

def arm_adaptive_mdl(buf: bytes, grounded: bool):
    return mdl_segment(buf, mdl_fit(buf, grounded))

# ---------------- hierarchical_mdl ----------------
def arm_hierarchical_mdl(buf: bytes):
    motifs = mdl_fit(buf, False)
    n = len(buf)
    # stream base chunks
    def base_chunks():
        byfirst = {}
        for mi, (key,) in enumerate(motifs):
            byfirst.setdefault(key[0], []).append((len(key), mi, key))
        i = 0
        while i < n:
            best = None
            for L, mi, key in byfirst.get(buf[i], []):
                if i + L <= n and bytes(buf[i:i + L]) == key:
                    if best is None or L > best[0]:
                        best = (L, mi)
            if best is not None:
                yield (0, best[1], best[0], i)
                i += best[0]
            else:
                yield (1, buf[i], 1, i)
                i += 1
    chunks = list(base_chunks())
    pairs = {}
    for (k1, d1, _, _), (k2, d2, _, _) in zip(chunks, chunks[1:]):
        key = (k1 * 1024 + d1) * 2048 + (k2 * 1024 + d2)
        pairs[key] = pairs.get(key, 0) + 1
    ranked = sorted([ (c - 3, c, k) for k, c in pairs.items() if c >= 4 ],
                    key=lambda e: (-e[0], -e[1], e[2]))[:96]
    merges = {k: i for i, (_, _, k) in enumerate(ranked)}
    out = []
    i = 0
    while i < len(chunks):
        if i + 1 < len(chunks):
            k1, d1, l1, s1 = chunks[i]
            k2, d2, l2, s2 = chunks[i + 1]
            key = (k1 * 1024 + d1) * 2048 + (k2 * 1024 + d2)
            if key in merges:
                out.append((s1, l1 + l2, merges[key], 'h'))
                i += 2
                continue
        k, d, l, s = chunks[i]
        out.append((s, l, d, 'm' if k == 0 else 'r'))
        i += 1
    return out

# ---------------- raw_micro / random_chunks ----------------
def arm_raw_micro(buf: bytes):
    return [(i, 1, buf[i], 'r') for i in range(len(buf))]

def arm_random_chunks(buf: bytes):
    n = len(buf)
    out = []
    i = 0
    while i < n:
        s = 0
        for j in range(5):
            if i + j < n:
                s += (j + 3) * buf[i + j]
        h = (s + 17 * i) % 7
        L = 2 + h
        if i + L > n:
            L = n - i
        out.append((i, L, umod1000003(fnv1a(buf[i:i + L])), 'x'))
        i += L
    return out

ARMS = {
    'predictive_surprise': arm_predictive_surprise,
    'fixed_window_4': lambda b: arm_fixed_window(b, 4),
    'fixed_window_8': lambda b: arm_fixed_window(b, 8),
    'fixed_window_16': lambda b: arm_fixed_window(b, 16),
    'fixed_window_64': lambda b: arm_fixed_window(b, 64),
    'adaptive_mdl': lambda b: arm_adaptive_mdl(b, False),
    'grounded_adaptive_mdl': lambda b: arm_adaptive_mdl(b, True),
    'hierarchical_mdl': arm_hierarchical_mdl,
    'raw_micro': arm_raw_micro,
    'random_chunks': arm_random_chunks,
}

def parse_output(text):
    segs = []
    for line in text.splitlines():
        if line.startswith('SEG '):
            _, s, l, i, k = line.split(' ')
            segs.append((int(s), int(l), int(i), k))
    return segs

def main():
    arms_bin = sys.argv[1]
    files = sys.argv[2:]
    fails = 0
    for f in files:
        buf = open(f, 'rb').read()
        for name, fn in ARMS.items():
            p = subprocess.run([arms_bin, name], input=buf, capture_output=True)
            if p.returncode != 0:
                print(f'FAIL {name}/{f}: exit={p.returncode} {p.stdout[:100]}')
                fails += 1
                continue
            got = parse_output(p.stdout.decode())
            want = fn(buf)
            if got != want:
                fails += 1
                print(f'MISMATCH {name}/{f}: got {len(got)} segs, want {len(want)}')
                for g, w in zip(got, want):
                    if g != w:
                        print(f'  first diff: got {g} want {w}')
                        break
            else:
                print(f'OK {name}/{f}: {len(got)} segs')
    print('XCHECK ' + ('PASS' if fails == 0 else f'FAIL ({fails})'))
    return 1 if fails else 0

if __name__ == '__main__':
    sys.exit(main())
