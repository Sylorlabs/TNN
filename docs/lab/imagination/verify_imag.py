#!/usr/bin/env python3
"""Independent verifier for the IMAGINATION-DESIGN Q1/Q2/Q3 trial runs.

Authored by hand from reading imagination/src/imagine.zag; it re-derives
every expected answer from the scene-install tables and the documented
query semantics rather than re-running the binary.  Comparisons that fail
are investigated against the frozen PREREG.md / code, not "fixed" to match.

Usage:
    python3 verify_imag.py --q1 q1m.txt --q1h q1h.txt
"""
import argparse, sys

MASK = 0xFFFFFFFF

def u32(v):
    return v & MASK

# ---------------- helpers (ported from ig_* reading, not from behavior) ----------------
def zcol(z): return z % 3
def zrow(z): return z // 3
def zone_of_xy(x, y):
    cx = min(x // 334, 2); cy = min(y // 334, 2)
    return cy * 3 + cx
def chroma(h): return 1 if 1000 <= h < 1072 else 0
def hue(h): return (h - 1000) // 6
def light(h): return ((h - 1000) % 6) // 2
def sat(h): return (h - 1000) % 2
def achrank(h):
    i = h - 2000
    if i <= 1: return 0
    if i == 2: return 1
    return 2
def lrank(h): return light(h) if chroma(h) == 1 else achrank(h)
def wheeldist(a, b):
    d = abs(a - b)
    if d > 6: d = 12 - d
    return d
def cdist(h1, h2):
    c1, c2 = chroma(h1), chroma(h2)
    if c1 == 1 and c2 == 1:
        return wheeldist(hue(h1), hue(h2)) + abs(light(h1) - light(h2)) + abs(sat(h1) - sat(h2))
    if c1 == 0 and c2 == 0:
        return abs(h1 - h2)
    return 4 + abs(lrank(h1) - lrank(h2))
def warmth(h):
    if chroma(h) == 0: return 1
    hu = hue(h)
    if hu <= 4: return 2
    if hu <= 7: return 1
    return 0

ST_THRESH = {1:972,2:1091,3:1155,4:1224,5:1297,6:1374,7:1456,8:1542,9:1634,10:1731,
             11:1834,12:1943,13:2059,14:2181,15:2311,16:2448,17:2594,18:2748,19:2911,
             20:3084,21:3268,22:3462,23:3668,24:3886}
def semitones(fa, fb):
    lo, hi = min(fa, fb), max(fa, fb)
    if lo <= 0: return 99
    r = hi * 1000 // lo
    s = 0
    for k in range(1, 25):
        if r >= ST_THRESH[k]: s = k
    return s
def tcode(st):
    if st == 0: return 0
    if st == 1: return 2
    if st == 2: return 1
    if st <= 4: return 1
    return 3

# ---------------- scene model ----------------
class Scene:
    def __init__(self): self.elems = []
    def place(self, dom, kind, a1, a2, a3, a4, a5, a6, a7, a8):
        self.elems.append([u32(v) for v in (dom, kind, a1, a2, a3, a4, a5, a6, a7, a8)])
        return len(self.elems) - 1
    def eattr(self, i, slot, v):
        self.elems[i][slot] = u32(v)
    def ew(self, i, s): return self.elems[i][s]
    def n(self): return len(self.elems)

def zone_of(sc, i, mode):
    if mode == 1: return sc.ew(i, 2)
    return zone_of_xy(sc.ew(i, 2), sc.ew(i, 3))

# ---------------- queries ----------------
def q_zonecount(sc, z, mode):
    return sum(1 for i in range(sc.n()) if zone_of(sc, i, mode) == z)
def q_farthest(sc, mode):
    n = sc.n(); bi, bj, bd = 0, (1 if n >= 2 else 0), -1
    for i in range(n):
        for j in range(i + 1, n):
            d = max(abs(zcol(zone_of(sc,i,mode)) - zcol(zone_of(sc,j,mode))),
                      abs(zrow(zone_of(sc,i,mode)) - zrow(zone_of(sc,j,mode))))
            if d > bd: bd, bi, bj = d, i, j
    return (bi, bj)
def q_warmest(sc, mode):
    n = sc.n()
    if n == 0: return -1
    bi = 0
    if mode == 1:
        bw = warmth(sc.ew(0, 3))
        for i in range(1, n):
            w = warmth(sc.ew(i, 3))
            if w > bw: bw, bi = w, i
    else:
        bw = sc.ew(0, 6) - sc.ew(0, 8)
        for i in range(1, n):
            w = sc.ew(i, 6) - sc.ew(i, 8)
            if w > bw: bw, bi = w, i
    return bi
def q_harmony(sc, a, b, mode):
    if mode == 1:
        h = 400 - 50 * cdist(sc.ew(a, 3), sc.ew(b, 3))
        return max(h, 0)
    dd = abs(sc.ew(a,6)-sc.ew(b,6)) + abs(sc.ew(a,7)-sc.ew(b,7)) + abs(sc.ew(a,8)-sc.ew(b,8))
    return max(400 - dd * 400 // 765, 0)
def q_leftmost(sc, mode):
    n = sc.n()
    if n == 0: return -1
    bi = 0
    if mode == 1:
        bc = zcol(sc.ew(0, 2))
        for i in range(1, n):
            c = zcol(sc.ew(i, 2))
            if c < bc: bc, bi = c, i
    else:
        bx = sc.ew(0, 2)
        for i in range(1, n):
            x = sc.ew(i, 2)
            if x < bx: bx, bi = x, i
    return bi
def q_contour(sc, mode):
    n = sc.n()
    if n < 2: return 2
    up = dn = fl = 0
    for i in range(n - 1):
        a, b = sc.ew(i, 2), sc.ew(i + 1, 2)
        if b > a: up = 1
        if b < a: dn = 1
        if b == a: fl = 1
    first, last = sc.ew(0, 2), sc.ew(n - 1, 2)
    if up == 1 and dn == 0 and last > first: return 4
    if dn == 1 and up == 0 and last < first: return 1
    if up == 0 and dn == 0: return 2
    if up == 1 and dn == 1:
        pk = 0
        for k in range(n):
            if sc.ew(k, 2) >= sc.ew(pk, 2): pk = k
        if 0 < pk < n - 1:
            ok = 1
            for m in range(pk):
                if sc.ew(m + 1, 2) < sc.ew(m, 2): ok = 0
            for m in range(pk, n - 1):
                if sc.ew(m + 1, 2) > sc.ew(m, 2): ok = 0
            if ok == 1: return 3
    return 0
def q_maxstep(sc, mode):
    n = sc.n()
    if n < 2: return -1
    bk, bd = 0, -1
    for k in range(n - 1):
        d = abs(sc.ew(k, 2) - sc.ew(k + 1, 2))
        if d > bd: bd, bk = d, k
    return bk
def q_tension(sc, a, b, mode):
    if mode == 1:
        return tcode(abs(sc.ew(a, 2) - sc.ew(b, 2)))
    return tcode(semitones(sc.ew(a, 2), sc.ew(b, 2)))
def q_laststable(sc, mode):
    n = sc.n()
    if n < 2: return 1
    return 1 if q_tension(sc, n - 2, n - 1, mode) == 0 else 0
def q_support(sc, i, mode):
    if mode == 1:
        rel = sc.ew(i, 3); cur = i; guard = 0
        while rel == 5 and guard < 40:
            cur = sc.ew(cur, 4)
            if cur >= sc.n(): return 0   # u32 read: -1 -> 4294967295, caught here
            rel = sc.ew(cur, 3); guard += 1
        return 1 if rel == 0 else 0
    z = sc.ew(i, 4)
    if z == 0: return 1
    n = sc.n()
    for j in range(n):
        if j == i: continue
        dx = abs(sc.ew(j, 2) - sc.ew(i, 2)); dy = abs(sc.ew(j, 3) - sc.ew(i, 3))
        ztop = sc.ew(j, 4) + sc.ew(j, 5)
        if dx <= 60 and dy <= 60 and ztop >= z - 20 and sc.ew(j, 5) >= sc.ew(i, 5):
            return 1
    return 0
def inv_rel(r):
    return {1:2, 2:1, 3:4, 4:3, 5:4}.get(r, r)
def q_relation(sc, a, b, mode):
    if mode == 1:
        ra, ta = sc.ew(a, 3), sc.ew(a, 4)
        if ta == b and ra != 0: return ra
        rb, tb = sc.ew(b, 3), sc.ew(b, 4)
        if tb == a and rb != 0: return inv_rel(rb)
        za, zb = sc.ew(a, 2), sc.ew(b, 2)
        if za == zb: return 6
        ca, cb = zcol(za), zcol(zb)
        if ca < cb: return 1
        if ca > cb: return 2
        ra2, rb2 = zrow(za), zrow(zb)
        if ra2 < rb2: return 3
        return 4
    xa, ya, za2 = sc.ew(a,2), sc.ew(a,3), sc.ew(a,4)
    xb, yb, zb2 = sc.ew(b,2), sc.ew(b,3), sc.ew(b,4)
    dx, dy = xb - xa, yb - ya
    if za2 > zb2 and abs(dx) <= 60 and abs(dy) <= 60: return 5
    if zb2 > za2 and abs(dx) <= 60 and abs(dy) <= 60: return 4
    if abs(dx) < 80 and abs(dy) < 80: return 6
    if abs(dx) >= abs(dy): return 1 if dx > 0 else 2
    return 4 if dy > 0 else 3
def q_topmost(sc, mode):
    n = sc.n()
    if n == 0: return -1
    if mode == 1:
        bi, bl = 0, -1
        for i in range(n):
            ln, cur, guard = 0, i, 0
            while sc.ew(cur, 3) == 5 and guard < 40:
                ln += 1; cur = sc.ew(cur, 4)
                if cur >= n: cur, guard = i, 99
                guard += 1
            if ln > bl: bl, bi = ln, i
        return bi
    bj, bz = 0, sc.ew(0, 4)
    for j in range(1, n):
        z = sc.ew(j, 4)
        if z > bz: bz, bj = z, j
    return bj

# ---------------- scene install tables (transcribed from ig_q1_scN pre blocks) ----------------
def install(mode, scene):
    sc = Scene()
    P = sc.place
    if scene == 1:
        if mode == 1:
            P(1,3,2,1003,3001,3101,3202,0,0,0); P(1,2,4,1015,3000,3100,3200,0,0,0)
            P(1,4,8,1023,3002,3101,3201,0,0,0); P(1,2,7,2004,3000,3100,3200,0,0,0)
        else:
            P(1,3,832,125,80,80,200,60,30,0); P(1,2,499,375,100,100,60,130,200,0)
            P(1,4,832,875,200,60,240,200,90,0); P(1,2,499,875,90,90,240,240,240,0)
    elif scene == 2:
        if mode == 1:
            P(1,1,1,1059,3002,3101,3201,0,0,0); P(1,2,0,2004,3000,3100,3200,0,0,0)
            P(1,3,5,1003,3001,3101,3202,0,0,0); P(1,4,8,1027,3002,3101,3201,0,0,0)
        else:
            P(1,1,499,125,200,120,20,60,160,0); P(1,2,166,125,110,110,240,240,225,0)
            P(1,3,832,375,90,90,200,60,30,0); P(1,4,832,875,170,50,240,90,20,0)
    elif scene == 3:
        if mode == 1:
            P(1,4,6,1003,3002,3101,3201,0,0,0); P(1,3,7,1023,3001,3101,3202,0,0,0)
            P(1,2,4,1015,3000,3100,3200,0,0,0); P(1,1,2,1059,3002,3101,3201,0,0,0)
        else:
            P(1,4,166,875,200,60,220,40,20,0); P(1,3,499,875,80,80,240,200,90,0)
            P(1,2,499,375,100,100,200,90,60,0); P(1,1,832,125,200,120,20,60,160,0)
    elif scene == 4:
        if mode == 1:
            P(1,2,0,2004,3000,3100,3200,0,0,0); P(1,2,2,2004,3000,3100,3200,0,0,0)
            P(1,1,6,1059,3002,3101,3201,0,0,0); P(1,1,8,1059,3002,3101,3201,0,0,0)
        else:
            P(1,2,166,125,120,120,240,240,225,0); P(1,2,832,125,120,120,240,240,225,0)
            P(1,1,166,875,200,120,120,170,230,0); P(1,1,832,875,200,120,120,170,230,0)
    elif scene == 5:
        if mode == 1:
            for b in (15,17,19,22): P(2,1,b,5000,0,0,0,0,0,0)
        else:
            for f in (262,294,330,392): P(2,1,f,250,800,0,0,0,0,0)
    elif scene == 6:
        if mode == 1:
            for b in (27,15,26,16): P(2,1,b,5002,0,0,0,0,0,0)
        else:
            for f in (523,262,494,277): P(2,1,f,150,800,0,0,0,0,0)
    elif scene == 7:
        if mode == 1:
            for b in (19,19,19,27): P(2,1,b,5000,0,0,0,0,0,0)
        else:
            P(2,1,330,250,800,0,0,0,0,0); P(2,1,330,250,800,0,0,0,0,0)
            P(2,1,330,250,800,0,0,0,0,0); P(2,1,523,500,800,0,0,0,0,0)
    elif scene == 8:
        if mode == 1:
            for b in (24,22,20,17): P(2,1,b,5001,0,0,0,0,0,0)
        else:
            for f in (440,392,349,294): P(2,1,f,300,800,0,0,0,0,0)
    elif scene == 9:
        if mode == 1:
            P(3,1,7,0,-1,5,0,0,0,0); P(3,1,7,5,0,3,0,0,0,0); P(3,1,7,5,1,1,0,0,0,0)
        else:
            P(3,1,200,850,0,200,0,0,0,0); P(3,1,200,850,200,120,0,0,0,0); P(3,1,200,850,320,40,0,0,0,0)
    elif scene == 10:
        if mode == 1:
            P(3,1,6,0,-1,4,0,0,0,0); P(3,1,8,0,-1,4,0,0,0,0); P(3,1,7,5,0,2,0,0,0,0)
        else:
            P(3,1,200,850,0,160,0,0,0,0); P(3,1,800,850,0,160,0,0,0,0); P(3,1,200,850,160,80,0,0,0,0)
    elif scene == 11:
        if mode == 1:
            P(3,1,6,0,-1,5,0,0,0,0); P(3,1,7,0,-1,4,0,0,0,0); P(3,1,8,0,-1,3,0,0,0,0)
        else:
            P(3,1,200,850,0,200,0,0,0,0); P(3,1,500,850,0,160,0,0,0,0); P(3,1,800,850,0,120,0,0,0,0)
    elif scene == 12:
        if mode == 1:
            P(3,1,6,0,-1,5,0,0,0,0); P(3,1,6,5,0,2,0,0,0,0)
            P(3,1,8,0,-1,4,0,0,0,0); P(3,1,8,5,2,1,0,0,0,0)
        else:
            P(3,1,200,850,0,200,0,0,0,0); P(3,1,200,850,200,80,0,0,0,0)
            P(3,1,800,850,0,160,0,0,0,0); P(3,1,800,850,160,40,0,0,0,0)
    return sc

def edit(mode, scene, sc):
    E = sc.eattr
    if scene == 1:
        E(2,2,6) if mode==1 else E(2,2,166)
    elif scene == 2:
        E(1,2,2) if mode==1 else E(1,2,832)
    elif scene == 3:
        if mode==1: E(3,2,5)
        else: E(3,2,832); E(3,3,375)
    elif scene == 4:
        if mode==1: E(2,2,4)
        else: E(2,2,499); E(2,3,375)
    elif scene == 5:
        E(3,2,24) if mode==1 else E(3,2,440)
    elif scene == 6:
        E(1,2,20) if mode==1 else E(1,2,349)
    elif scene == 7:
        if mode==1: E(3,2,19)
        else: E(3,2,330); E(3,3,250)
    elif scene == 8:
        E(0,2,22) if mode==1 else E(0,2,392)
    elif scene == 9:
        if mode==1: E(1,2,1); E(1,3,5); E(1,4,2)
        else: E(1,2,500)
    elif scene == 10:
        if mode==1: E(2,2,6); E(2,3,0); E(2,4,-1)
        else: E(2,4,0)
    elif scene == 11:
        if mode==1: E(2,2,7); E(2,3,5); E(2,4,1)
        else: E(2,2,500); E(2,4,160)
    elif scene == 12:
        if mode==1: E(3,2,6); E(3,4,1)
        else: E(3,2,200); E(3,4,280)

# ---------------- expected answers (one entry per question) ----------------
def expected(mode):
    out = {}  # (scene, qid) -> answer or (o1,o2) tuple
    for scene in range(1, 13):
        sc = install(mode, scene)
        if scene == 1:
            out[(1,1)] = q_zonecount(sc, 8, mode)
            out[(1,2)] = q_leftmost(sc, mode)
            edit(mode, scene, sc)
            out[(1,3)] = q_zonecount(sc, 6, mode)
        elif scene == 2:
            out[(2,1)] = q_farthest(sc, mode)
            out[(2,2)] = q_zonecount(sc, 5, mode)
            edit(mode, scene, sc)
            out[(2,3)] = q_zonecount(sc, 2, mode)
        elif scene == 3:
            out[(3,1)] = q_warmest(sc, mode)
            out[(3,2)] = q_harmony(sc, 0, 2, mode)
            edit(mode, scene, sc)
            out[(3,3)] = q_zonecount(sc, 5, mode)
        elif scene == 4:
            out[(4,1)] = q_farthest(sc, mode)
            out[(4,2)] = q_zonecount(sc, 4, mode)
            edit(mode, scene, sc)
            out[(4,3)] = q_zonecount(sc, 4, mode)
        elif scene == 5:
            out[(5,1)] = q_contour(sc, mode)
            out[(5,2)] = q_maxstep(sc, mode)
            edit(mode, scene, sc)
            out[(5,3)] = q_maxstep(sc, mode)
        elif scene == 6:
            out[(6,1)] = q_contour(sc, mode)
            out[(6,2)] = q_tension(sc, 0, 1, mode)
            edit(mode, scene, sc)
            out[(6,3)] = q_contour(sc, mode)
        elif scene == 7:
            out[(7,1)] = q_contour(sc, mode)
            out[(7,2)] = q_laststable(sc, mode)
            edit(mode, scene, sc)
            out[(7,3)] = q_contour(sc, mode)
        elif scene == 8:
            out[(8,1)] = q_contour(sc, mode)
            out[(8,2)] = q_maxstep(sc, mode)
            edit(mode, scene, sc)
            out[(8,3)] = q_maxstep(sc, mode)
        elif scene == 9:
            out[(9,1)] = q_support(sc, 2, mode)
            out[(9,2)] = q_topmost(sc, mode)
            edit(mode, scene, sc)
            out[(9,3)] = q_support(sc, 2, mode)
        elif scene == 10:
            out[(10,1)] = q_support(sc, 2, mode)
            out[(10,2)] = q_relation(sc, 0, 2, mode)
            edit(mode, scene, sc)
            out[(10,3)] = q_relation(sc, 0, 2, mode)
        elif scene == 11:
            out[(11,1)] = q_support(sc, 1, mode)
            out[(11,2)] = q_relation(sc, 0, 1, mode)
            edit(mode, scene, sc)
            out[(11,3)] = q_relation(sc, 1, 2, mode)
        elif scene == 12:
            out[(12,1)] = q_support(sc, 3, mode)
            out[(12,2)] = q_topmost(sc, mode)
            edit(mode, scene, sc)
            out[(12,3)] = q_topmost(sc, mode)
    return out

# Documented human preference per pair: side index (0 = first-listed).
# From Q3-SOURCES.md (verified 2026-09-22).
Q3_PREF = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 0, 7: 0, 8: 0}
Q3_TIER = {1: 'STRONG', 2: 'STRONG', 3: 'STRONG', 4: 'STRONG', 5: 'STRONG',
           6: 'MODERATE', 7: 'MODERATE', 8: 'MODERATE'}

def score_q3(m_path, h_path):
    def load(p):
        d = {}
        with open(p) as f:
            for line in f:
                t = line.split()
                if len(t) == 5 and t[0] == 'Q3':
                    d[(int(t[2]), int(t[3]))] = int(t[4])
        return d
    res = {}
    for mode, path in ((0, m_path), (1, h_path)):
        d = load(path)
        per = {}
        for p in range(1, 9):
            s0, s1 = d[(p, 0)], d[(p, 1)]
            if s0 > s1: pred = 0
            elif s1 > s0: pred = 1
            else: pred = 0  # frozen tie rule: first-listed
            per[p] = {'s0': s0, 's1': s1, 'tie': s0 == s1,
                      'pred': pred, 'ok': pred == Q3_PREF[p],
                      'tier': Q3_TIER[p]}
        res[mode] = per
    return res

def report_q3(m_path, h_path):
    res = score_q3(m_path, h_path)
    for mode in (0, 1):
        name = 'machine' if mode == 0 else 'human'
        per = res[mode]
        n_ok = sum(1 for p in per if per[p]['ok'])
        n_tie = sum(1 for p in per if per[p]['tie'])
        print(f"Q3 {name}: {n_ok}/8 correct (ties: {n_tie})")
        for p in range(1, 9):
            r = per[p]
            print(f"  pair {p} [{r['tier']}] side0={r['s0']} side1={r['s1']} "
                  f"pred={'tie->0' if r['tie'] else r['pred']} "
                  f"documented={Q3_PREF[p]} {'OK' if r['ok'] else 'MISS'}")
    m_ok = sum(1 for p in res[0] if res[0][p]['ok'])
    h_ok = sum(1 for p in res[1] if res[1][p]['ok'])
    best = max(m_ok, h_ok)
    agree1 = 'TNN design sense WORKS' if best >= 7 else ('MARGINAL' if best == 6 else 'FAIL')
    agree2 = 'mode winner' if abs(m_ok - h_ok) >= 3 else 'NO-DIFFERENTIATION'
    print(f"AGREE-1 (best mode {best}/8): {agree1}")
    print(f"AGREE-2 (|{m_ok}-{h_ok}|={abs(m_ok-h_ok)}): {agree2}")
    for tier in ('STRONG', 'MODERATE'):
        for mode in (0, 1):
            n = sum(1 for p in res[mode] if res[mode][p]['tier'] == tier and res[mode][p]['ok'])
            t = sum(1 for p in res[mode] if res[mode][p]['tier'] == tier)
            print(f"  {tier} {'machine' if mode==0 else 'human'}: {n}/{t}")
    return m_ok, h_ok

def parse_log(path):
    rows = []
    with open(path) as f:
        for line in f:
            t = line.split()
            if len(t) == 5 and t[0] == 'Q1':
                rows.append((int(t[1]), int(t[2]), int(t[3]), int(t[4])))
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--q1m', required=False, default=None)
    ap.add_argument('--q1h', required=False, default=None)
    ap.add_argument('--q3m', required=False, default=None)
    ap.add_argument('--q3h', required=False, default=None)
    args = ap.parse_args()
    rc = 0
    if args.q1m and args.q1h:
        rc |= q1_main(args)
    if args.q3m and args.q3h:
        m_ok, h_ok = report_q3(args.q3m, args.q3h)
    return rc


def q1_main(args):
    total_ok, total = 0, 0
    for mode, path in ((0, args.q1m), (1, args.q1h)):
        rows = parse_log(path)
        exp = expected(mode)
        # group farthest duplicates: qid 1 in scenes 2,4 appears twice
        grouped = {}
        for m_, s, q, a in rows:
            assert m_ == mode
            grouped.setdefault((s, q), []).append(a)
        ok, tot, fails = 0, 0, []
        for key in sorted(exp):
            e = exp[key]
            got = grouped.get(key)
            tot += 1
            if isinstance(e, tuple):
                match = got == [e[0], e[1]]
            else:
                match = got == [e]
            if match:
                ok += 1
            else:
                fails.append((key, e, got))
        print(f"mode={mode}: {ok}/{tot} questions match")
        for key, e, got in fails:
            print(f"  MISMATCH scene={key[0]} q={key[1]}: expected={e} got={got}")
        total_ok += ok; total += tot
        print(f"  (log had {len(rows)} lines; 36 questions expected, {38 if mode in (0,1) else 0} lines observed)")
    print(f"TOTAL: {total_ok}/{total}")
    return 0 if total_ok == total else 1

if __name__ == '__main__':
    sys.exit(main())
