#!/usr/bin/env python3
"""Independent GEN-1 (brief compliance) and GEN-2 (mode fidelity) verification
for the IMAGINATION-DESIGN Q2 legs.

Reads the E-lines emitted by imagination/src/imagine_bin, rebuilds each
design's scene independently, and mechanically checks:
  GEN-1: every emitted design satisfies ALL brief constraints, both the
         code's hard filters (read from ig_gen_* in imagine.zag) and the
         brief-text constraints (from frozen PREREG.md).
  GEN-2: every attribute word in the E-lines uses only its mode's vocabulary.
"""
import sys, re

# ---------------- scene model ----------------
def zcol(z): return z % 3
def zrow(z): return z // 3
def zone_of_xy(x, y):
    return min(y // 334, 2) * 3 + min(x // 334, 2)
def zmirror(z): return (z // 3) * 3 + (2 - (z % 3))

def warmth_h(h):  # human warmth per PREREG (hue sectors of b_percept)
    if not (1000 <= h < 1072): return 1  # achromatic -> neutral
    hu = (h - 1000) // 6
    if hu <= 4: return 2
    if hu <= 7: return 1
    return 0

def warm_m(r, g, b):  # machine warm rule from ig_warm_m
    return 1 if r > b + 40 else 0

def asym(zones):  # ig_s2_asym port
    return not all(zmirror(z) in zones for z in zones)

ST_THRESH = {1:972,2:1091,3:1155,4:1224,5:1297,6:1374,7:1456,8:1542,9:1634,10:1731,
             11:1834,12:1943,13:2059,14:2181,15:2311,16:2448,17:2594,18:2748,19:2911,
             20:3084,21:3268,22:3462,23:3668,24:3886}
def semitones(fa, fb):
    lo, hi = min(fa, fb), max(fa, fb)
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
def contour(vals):
    n = len(vals)
    up = any(vals[i+1] > vals[i] for i in range(n-1))
    dn = any(vals[i+1] < vals[i] for i in range(n-1))
    first, last = vals[0], vals[-1]
    if up and not dn and last > first: return 4
    if dn and not up and last < first: return 1
    if not up and not dn: return 2
    if up and dn:
        pk = max(range(n), key=lambda k: (vals[k], -k))  # first max index
        pk = next(k for k in range(n) if vals[k] == max(vals))
        if 0 < pk < n - 1:
            ok = all(vals[m+1] >= vals[m] for m in range(pk)) and \
                 all(vals[m+1] <= vals[m] for m in range(pk, n-1))
            if ok: return 3
    return 0

def parse(path):
    designs = {}  # (mode, brief) -> list of elems [dom,kind,a1..a8]
    with open(path) as f:
        for line in f:
            t = line.split()
            if t and t[0] == 'E' and len(t) == 14:
                mode, brief, elem = int(t[1]), int(t[2]), int(t[3])
                designs.setdefault((mode, brief), []).append([int(x) for x in t[4:]])
    return designs

# ---------------- GEN-2: vocabulary check ----------------
def gen2_check(mode, brief, elems):
    bad = []
    for i, e in enumerate(elems):
        dom, kind, a = e[0], e[1], e[2:]
        if mode == 0:
            if dom == 1:  # visual: x,y,w,h 0..1000 ; r,g,b 0..255
                for s, v in enumerate(a[:4], 1):
                    if not (0 <= v <= 1000): bad.append(f"e{i} a{s}={v} not 0..1000")
                for s, v in enumerate(a[4:7], 5):
                    if not (0 <= v <= 255): bad.append(f"e{i} rgb a{s}={v} not 0..255")
            elif dom == 2:  # audio: freq Hz, dur ms, amp 0..1000
                if not (20 <= a[0] <= 20000): bad.append(f"e{i} freq={a[0]}")
                if not (1 <= a[1] <= 100000): bad.append(f"e{i} dur={a[1]}")
                if not (0 <= a[2] <= 1000): bad.append(f"e{i} amp={a[2]}")
            elif dom == 3:  # struct: x,y,z cm 0..1000 ; size 1..500
                for s, v in enumerate(a[:3], 1):
                    if not (0 <= v <= 1000): bad.append(f"e{i} a{s}={v} not cm 0..1000")
                if not (1 <= a[3] <= 500): bad.append(f"e{i} size={a[3]} not 1..500")
            else: bad.append(f"e{i} bad dom {dom}")
            if a[7] != 0: bad.append(f"e{i} a8={a[7]} nonzero")
        else:
            if dom == 1:  # visual: zone 0..8; color 1000..1071/2000..2004; shape tuples
                if not (0 <= a[0] <= 8): bad.append(f"e{i} zone={a[0]}")
                if not ((1000 <= a[1] < 1072) or (2000 <= a[1] <= 2004)):
                    bad.append(f"e{i} color={a[1]} not a handle")
                if not (3000 <= a[2] <= 3003): bad.append(f"e{i} corners={a[2]}")
                if not (3100 <= a[3] <= 3102): bad.append(f"e{i} curv={a[3]}")
                if not (3200 <= a[4] <= 3203): bad.append(f"e{i} sym={a[4]}")
            elif dom == 2:  # audio: pitch-bin INDEX (code stores index, not 4000+ handle)
                if not (0 <= a[0] <= 47): bad.append(f"e{i} pitch={a[0]} not bin index")
                if not (5000 <= a[1] <= 5003): bad.append(f"e{i} timbre={a[1]}")
            elif dom == 3:  # struct: zone 0..8; rel 0..6; rel_target; size rank
                if not (0 <= a[0] <= 8): bad.append(f"e{i} zone={a[0]}")
                if not (0 <= a[1] <= 6): bad.append(f"e{i} rel={a[1]}")
                rt = a[2] if a[2] < 2**31 else a[2] - 2**32
                if not (rt == -1 or 0 <= rt < len(elems)): bad.append(f"e{i} relt={rt}")
                if not (1 <= a[3] <= 32): bad.append(f"e{i} sizerank={a[3]}")
            else: bad.append(f"e{i} bad dom {dom}")
    return bad

# ---------------- GEN-1: brief compliance ----------------
def check(name, cond, detail):
    return (name, bool(cond), detail)

def gen1_v1(mode, elems):
    out = []
    out.append(check("n<=4", len(elems) <= 4, f"n={len(elems)}"))
    out.append(check("grain-motif kind3 present", any(e[1] == 3 for e in elems), ""))
    if mode == 0:
        warm = all(warm_m(e[6], e[7], e[8]) == 1 for e in elems)
        out.append(check("warm palette (r>b+40 all)", warm,
                         str([(e[6], e[7], e[8]) for e in elems])))
        zones = [zone_of_xy(e[2], e[3]) for e in elems]
    else:
        warm = all(warmth_h(e[3]) == 2 for e in elems)
        out.append(check("warm palette (hue sector 0-4 all)", warm,
                         str([e[3] for e in elems])))
        zones = [e[2] for e in elems]
    out.append(check("text element (kind4) present", any(e[1] == 4 for e in elems), ""))
    out.append(check("hard: grain zone != circle zone", zones[0] != zones[1],
                     f"zones={zones}"))
    return out

def gen1_v2(mode, elems):
    out = []
    out.append(check("n==4", len(elems) == 4, f"n={len(elems)}"))
    out.append(check("two text elements", sum(1 for e in elems if e[1] == 4) == 2,
                     str([e[1] for e in elems])))
    if mode == 0:
        warms = [warm_m(e[6], e[7], e[8]) for e in elems]
        zones = [zone_of_xy(e[2], e[3]) for e in elems]
    else:
        warms = [1 if warmth_h(e[3]) == 2 else 0 for e in elems]
        zones = [e[2] for e in elems]
    out.append(check("exactly one warm accent", sum(warms) == 1, f"warms={warms}"))
    cool_dom = sum(1 for w in warms if w == 0) >= 3
    out.append(check("night feel (cool/neutral dominate)", cool_dom, f"warms={warms}"))
    out.append(check("hard: text zones 6..8", all(6 <= zones[i] <= 8 for i in (2, 3)),
                     f"text zones={[zones[2], zones[3]]}"))
    return out

def gen1_a1(mode, elems):
    out = []
    out.append(check("4 notes", len(elems) == 4, f"n={len(elems)}"))
    vals = [e[2] for e in elems]
    out.append(check("rising (each>=prev, last>first)",
                     all(vals[i+1] >= vals[i] for i in range(3)) and vals[3] > vals[0],
                     str(vals)))
    endv = 523 if mode == 0 else 27
    out.append(check("ends stable (ends at max table value)",
                     vals[3] == endv, f"last={vals[3]} max={endv}"))
    out.append(check("contour==4 (rising)", contour(vals) == 4, f"contour={contour(vals)}"))
    return out

def gen1_a2(mode, elems):
    out = []
    out.append(check("3 notes", len(elems) == 3, f"n={len(elems)}"))
    vals = [e[2] for e in elems]
    if mode == 0:
        tens = [tcode(semitones(vals[i], vals[i+1])) for i in range(2)]
    else:
        tens = [tcode(abs(vals[i] - vals[i+1])) for i in range(2)]
    out.append(check("tense intervals (max adj tension>=2)", max(tens) >= 2,
                     f"tensions={tens}"))
    c = contour(vals)
    out.append(check("contour != rising (not welcoming)", c != 4, f"contour={c}"))
    return out

def gen1_s1(mode, elems):
    out = []
    out.append(check("5 blocks", len(elems) == 5, f"n={len(elems)}"))
    if mode == 0:
        xyz = [(e[2], e[3], e[4]) for e in elems]
        sizes = [e[5] for e in elems]
        ranks = [s // 40 for s in sizes]
        imax = max(range(5), key=lambda i: sizes[i])
        out.append(check("largest at bottom (z==0)", xyz[imax][2] == 0,
                         f"max size idx={imax} z={xyz[imax][2]}"))
        # no overhang: each z>0 block has a below-block with size >= its own
        ok = True; det = []
        for i in range(5):
            x, y, z = xyz[i]
            if z > 0:
                below = [j for j in range(5) if j != i and abs(xyz[j][0]-x) <= 60
                         and abs(xyz[j][1]-y) <= 60
                         and xyz[j][2] + sizes[j] >= z - 20 and sizes[j] >= sizes[i]]
                if not below: ok = False; det.append(f"e{i} unsupported")
        out.append(check("no overhang (supported by >=size block)", ok, "; ".join(det)))
        out.append(check("all front-visible (same y)", len(set(p[1] for p in xyz)) == 1,
                         f"ys={sorted(set(p[1] for p in xyz))}"))
    else:
        zones = [e[2] for e in elems]
        rels = [e[3] for e in elems]
        relts = [e[4] if e[4] < 2**31 else -1 for e in elems]
        ranks = [e[5] for e in elems]
        imax = max(range(5), key=lambda i: ranks[i])
        # largest at bottom: STACKED_ON chain from largest ends at rel==0,
        # and the largest itself has rel==0 (nothing below it)
        out.append(check("largest at bottom (rel==0)", rels[imax] == 0,
                         f"max rank idx={imax} rel={rels[imax]}"))
        ok = True; det = []
        for i in range(5):
            cur, guard = i, 0
            while rels[cur] == 5 and guard < 40:
                below = relts[cur]
                if ranks[below] < ranks[cur]:
                    ok = False; det.append(f"e{i}: smaller below (overhang)")
                cur, guard = below, guard + 1
            if rels[cur] != 0:
                ok = False; det.append(f"e{i}: chain not grounded")
        out.append(check("no overhang (rank decreases upward, grounded)", ok, "; ".join(det)))
        out.append(check("all front-visible (bottom-row zones)", all(6 <= z <= 8 for z in zones),
                         f"zones={zones}"))
    return out

def gen1_s2(mode, elems):
    out = []
    out.append(check("4 stones", len(elems) == 4, f"n={len(elems)}"))
    if mode == 0:
        zones = [zone_of_xy(e[2], e[3]) for e in elems]
        mags = [e[5] for e in elems]
        ranks = sorted(mags)
    else:
        zones = [e[2] for e in elems]
        ranks = sorted(e[5] for e in elems)
    out.append(check("distinct zones", len(set(zones)) == 4, f"zones={zones}"))
    out.append(check("asymmetric (not all mirrors present)", asym(zones), f"zones={zones}"))
    out.append(check("one dominant stone (unique max)", ranks[-1] > ranks[-2], f"ranks={ranks}"))
    out.append(check("airy (>=3 empty zones)", 9 - len(set(zones)) >= 3,
                     f"empty={9-len(set(zones))}"))
    return out

GEN1 = {1: gen1_v1, 2: gen1_v2, 3: gen1_a1, 4: gen1_a2, 5: gen1_s1, 6: gen1_s2}
BRIEFS = {1: 'V1', 2: 'V2', 3: 'A1', 4: 'A2', 5: 'S1', 6: 'S2'}

def main():
    paths = {"m": sys.argv[1], "h": sys.argv[2]}
    g1_pass = g1_tot = 0
    g2_pass = g2_tot = 0
    print("=" * 78)
    print("GEN-1: brief compliance (ALL constraints must pass per design)")
    print("=" * 78)
    for mk, path in paths.items():
        designs = parse(path)
        print(f"\n--- mode {'MACHINE(0)' if mk=='m' else 'HUMAN(1)'}: {path}")
        for b in range(1, 7):
            key = (0 if mk == 'm' else 1, b)
            elems = designs[key]
            res = GEN1[b](0 if mk == 'm' else 1, elems)
            ok = all(r[1] for r in res)
            g1_tot += 1
            if ok: g1_pass += 1
            print(f"  brief {b} ({BRIEFS[b]}): {'PASS' if ok else 'FAIL'}")
            for name, passed, detail in res:
                print(f"      [{'OK' if passed else 'XX'}] {name}" + (f"  [{detail}]" if detail else ""))
    print(f"\nGEN-1: {g1_pass}/{g1_tot}")
    print("\n" + "=" * 78)
    print("GEN-2: mode vocabulary (ALL attributes in every E-line)")
    print("=" * 78)
    for mk, path in paths.items():
        designs = parse(path)
        print(f"\n--- mode {'MACHINE(0)' if mk=='m' else 'HUMAN(1)'}: {path}")
        for b in range(1, 7):
            key = (0 if mk == 'm' else 1, b)
            elems = designs[key]
            bad = gen2_check(0 if mk == 'm' else 1, b, elems)
            g2_tot += 1
            if not bad:
                g2_pass += 1
                print(f"  brief {b} ({BRIEFS[b]}): PASS ({len(elems)} elems, all attrs in vocab)")
            else:
                print(f"  brief {b} ({BRIEFS[b]}): FAIL")
                for x in bad: print(f"      [XX] {x}")
    print(f"\nGEN-2: {g2_pass}/{g2_tot}")

if __name__ == '__main__':
    main()
