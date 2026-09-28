#!/usr/bin/env python3
"""rt_attacks.py — INDEPENDENT red team for Job 3 (affine-memorizer test).

Written from PREREG_JOB3.md section 5/10 and Crew E's REDTEAM_REPORT description.
Does NOT import the builder's memorizer prototype; every variant below is
reimplemented from the prereg spec text. The generator (gen3) is shared ground
truth (it defines the items). No RNG anywhere.

Attacks:
  1. fidelity      — reimplement the Crew-E affine memorizer; item-by-item diff
                     vs the Zag binary's memA/memB/memC outputs.
  2. noverify      — 2-parameter interpolation variant (fit on positions 0,1,
                     NO verification step); measure arm-B signature.
  2b. pairscan     — exhaustive: every position-pair-derived (s,o), every probe,
                     every train token — is any resulting output correct?
                     (proves noverify is optimal among 2-param tricks)
  2c. propagate    — (s,o) propagated through rule position maps (the smart
                     affine extension); control: must win reverse/rotleft on
                     arm A, must fail on arm B.
  3. quadmem       — 3-parameter (offset,slope,curve) memorizer; must recover
                     the full Crew-E signature on arm C, must NOT on arm B.
  4. freelta       — fully-general per-position-delta clone; must be 8/8 on
                     droplast/upperfirst on ALL arms (principled limit).
  5. combiner_audit— white-box: gen_* probe path touches no generator state.
"""
import sys, itertools
sys.path.insert(0, '/home/hatch/workspace/composition_followup/job3_affine/scratch')
from gen3 import tok, toklen, TRAIN, P0, P2, P3, is_sorted
RUN1 = '/home/hatch/workspace/composition_followup/job3_affine/runs/run1'

def pm(x): return x % 26
def apply_rule(r, s):
    if r == 0: return s[::-1]
    if r == 1: return s[:1] + s
    if r == 2: return s[1:] + s[:1] if s else s
    if r == 3: return s[:-1]
    if r == 4: return (s[:1].upper() + s[1:]) if s else s
    if r == 5: return bytes(sorted(s))
def p2_exp(a, b, p): return apply_rule(b, apply_rule(a, p))
PAIRS = [(a, b) for a in range(6) for b in range(6) if a != b]

def taught_for(arm):
    return {tok(arm,0,i): {r: apply_rule(r, tok(arm,0,i)) for r in range(6)} for i in TRAIN}

def fit_affine_rt(p, t):
    """Independent reimplementation of prereg section 5 M2 (raw-byte space)."""
    if len(p) != len(t) or len(p) < 2: return None
    d = [pm(x - y) for x, y in zip(p, t)]
    o, s = d[0], pm(d[1] - d[0])
    if all(pm(o + s*k) == d[k] for k in range(2, len(p))):
        return (s, o)
    return None

def transform_rt(out, s, o):
    r = bytearray()
    for k, c in enumerate(out):
        base = 65 if 65 <= c <= 90 else 97
        r.append(base + pm((c - base) + o + s*k))
    return bytes(r)

def mem_rt(arm, r, probe, taught):
    """Prereg section 5 P0 procedure."""
    if r == 5 and is_sorted(probe): return probe
    for t in taught:
        if len(t) != len(probe): continue
        f = fit_affine_rt(probe, t)
        if f: return transform_rt(taught[t][r], *f)
    return None

def mem2_rt(arm, a, b, probe, taught):
    m1 = None
    for t in taught:
        if len(t) != len(probe): continue
        f = fit_affine_rt(probe, t)
        if f:
            m1 = transform_rt(taught[t][a], *f); break
    if m1 is None: return None
    for t2 in taught:
        if len(t2) != len(m1): continue
        f2 = fit_affine_rt(m1, t2)
        if f2: return transform_rt(taught[t2][b], *f2)
    return None

def parse_zag(mode):
    items = {}
    for line in open(f'{RUN1}/{mode}.out'):
        t = line.split()
        if t[0] == 'P0':
            _, r, idx, ok, exp, got = t
            items[('P0', int(r), int(idx))] = got
        elif t[0] == 'P2':
            _, a, b, idx, ok, exp, got = t
            items[('P2', int(a), int(b), int(idx))] = got
        elif t[0] == 'P3':
            _, idx, ok, exp, got = t
            items[('P3', int(idx))] = got
    return items

# ---------------- attack 1: fidelity ----------------
def attack1():
    print("=== ATTACK 1: fidelity (independent reimplementation vs Zag) ===")
    total = mism = 0
    for mode, arm in [('memA','A'), ('memB','B'), ('memC','C')]:
        taught = taught_for(arm)
        zag = parse_zag(mode)
        for r in range(6):
            for j in range(8):
                idx = P0[r*8+j]; p = tok(arm,1,idx)
                g = mem_rt(arm, r, p, taught)
                z = zag[('P0', r, idx)]
                total += 1
                if (g.decode() if g is not None else '?') != z:
                    mism += 1; print('  MISM P0', r, idx, g, z)
        for pi, (a,b) in enumerate(PAIRS):
            for j in range(4):
                idx = P2[pi*4+j]; p = tok(arm,2,idx)
                g = mem2_rt(arm, a, b, p, taught)
                z = zag[('P2', a, b, idx)]
                total += 1
                if (g.decode() if g is not None else '?') != z:
                    mism += 1; print('  MISM P2', (a,b), idx, g, z)
    # P3 policy check on arm A (must be 0/8) and arm B (6/8)
    for mode, arm, exp3 in [('memA','A','0/8'), ('memB','B','6/8'), ('memC','C','6/8')]:
        taught = taught_for(arm); zag = parse_zag(mode)
        got3 = 0
        for idx in P3:
            p = tok(arm,3,idx); outs = [mem_rt(arm, r, p, taught) for r in range(6)]
            g = next((o for o in outs if o is not None), None)
            z = zag[('P3', idx)]
            if (g.decode() if g is not None else '?') != z:
                mism += 1; print('  MISM P3', idx, g, z)
            if g in (p, None): got3 += 1
            total += 1
        print(f'  {mode} P3 reimplementation: {got3}/8 (prereg predicts {exp3})')
    print(f'  {total} items, {mism} mismatches -> {"FAITHFUL" if mism==0 else "UNFAITHFUL"}')
    return mism == 0

# ---------------- attack 2: no-verify interpolation variant ----------------
def solve2(p, t, i, j):
    """Solve (s,o) from positions i,j only (no verification). Needs i!=j."""
    if len(p) != len(t): return None
    d = [pm(x - y) for x, y in zip(p, t)]
    # o + s*i = d[i], o + s*j = d[j]  ->  s = (d[j]-d[i])/(j-i) mod 26
    den = (j - i) % 26
    if den % 2 == 0: return None  # not invertible mod 26; skip (conservative)
    import math
    if math.gcd(den, 26) != 1: return None
    inv = pow(den, -1, 26)
    s = pm((d[j] - d[i]) * inv)
    o = pm(d[i] - s*i)
    return (s, o)

def noverify_p0(arm, r, probe, taught):
    for t in taught:
        if len(t) != len(probe) or len(t) < 2: continue
        f = solve2(probe, t, 0, 1)
        if f: return transform_rt(taught[t][r], *f)
    return None

def noverify_p2(arm, a, b, probe, taught):
    m1 = None
    for t in taught:
        if len(t) != len(probe) or len(t) < 2: continue
        f = solve2(probe, t, 0, 1)
        if f: m1 = transform_rt(taught[t][a], *f); break
    if m1 is None or len(m1) < 2: return None
    for t2 in taught:
        if len(t2) != len(m1): continue
        f2 = solve2(m1, t2, 0, 1)
        if f2: return transform_rt(taught[t2][b], *f2)
    return None

def attack2():
    print("=== ATTACK 2: no-verify interpolation variant on arm B ===")
    arm = 'B'; taught = taught_for(arm)
    p0 = [sum(1 for j in range(8)
              if noverify_p0(arm, r, tok(arm,1,P0[r*8+j]), taught) == apply_rule(r, tok(arm,1,P0[r*8+j])))
          for r in range(6)]
    p2ok = 0; pairhits = {}
    for pi, (a,b) in enumerate(PAIRS):
        h = 0
        for j in range(4):
            p = tok(arm,2,P2[pi*4+j])
            if noverify_p2(arm, a, b, p, taught) == p2_exp(a, b, p): h += 1; p2ok += 1
        if h: pairhits[(a,b)] = h
    print(f'  noverify armB: P0={p0}={sum(p0)}/48 P2={p2ok}/120 {pairhits}')
    # salt-invariance of the residual: every noverify arm-B hit must also be
    # an arm-A hit of the verified memorizer (degrees-of-freedom floor)
    armA = 'A'; taughtA = taught_for(armA)
    sub = True
    for r in range(6):
        for j in range(8):
            idx = P0[r*8+j]
            if noverify_p0('B', r, tok('B',1,idx), taught) == apply_rule(r, tok('B',1,idx)):
                if mem_rt('A', r, tok('A',1,idx), taughtA) != apply_rule(r, tok('A',1,idx)):
                    sub = False; print('  NOT-SUBSET P0', r, idx)
    print(f'  every noverify arm-B P0 hit is also a verified-memorizer arm-A hit: {sub}')
    return p0, p2ok, pairhits

# ---------------- attack 2b: exhaustive position-pair scan ----------------
def attack2b():
    print("=== ATTACK 2b: exhaustive position-pair scan (arm B) ===")
    arm = 'B'; taught = taught_for(arm)
    # For each probe, each train token, each position pair: does the resulting
    # transform output equal the TRUE rule output for ANY rule?
    best = {}
    for r in range(6):
        for j in range(8):
            idx = P0[r*8+j]; p = tok(arm,1,idx); n = len(p)
            exp = apply_rule(r, p); win = []
            for t in taught:
                if len(t) != n: continue
                for i, jj in itertools.combinations(range(n), 2):
                    f = solve2(p, t, i, jj)
                    if f and transform_rt(taught[t][r], *f) == exp:
                        win.append((i, jj))
            if win: best[('P0', r, idx)] = win
    # P2: scan ALL pairs (the chaining candidates), step-1 pair (0,1) then
    # exhaustive step-2 pairs — catches (3,5)-style accidents too
    for pi, (a, b) in enumerate(PAIRS):
        for j in range(4):
            idx = P2[pi*4+j]; p = tok(arm,2,idx); n = len(p)
            exp = p2_exp(a, b, p); win = []
            for t in taught:
                if len(t) != n: continue
                f = solve2(p, t, 0, 1)
                if not f: continue
                m1 = transform_rt(taught[t][a], *f)
                if len(m1) < 2: continue
                for t2 in taught:
                    if len(t2) != len(m1): continue
                    for i2, j2 in itertools.combinations(range(len(m1)), 2):
                        f2 = solve2(m1, t2, i2, j2)
                        if f2 and transform_rt(taught[t2][b], *f2) == exp:
                            win.append(((0,1),(i2,j2)))
                            break
                    if win: break
                if win: break
            if win: best[('P2',(a,b),idx)] = win[:2]
    print(f'  items with ANY winning position-pair: {len(best)}')
    for k, v in best.items(): print(f'    {k}: {v}')
    # The claim: winners are exactly the characterized floor (output pos <= 2)
    return best

# ---------------- attack 2c: propagation through position maps ----------------
def attack2c():
    print("=== ATTACK 2c: (s,o) propagation through rule position maps ===")
    # reverse: out delta'[k'] = o + s*(n-1-k')  -> still affine: (s2,o2) = (-s, o+s*(n-1))
    # rotleft: out delta'[k'] = o + s*((k'+1) % n) -> NOT affine (wrap). No single (s2,o2).
    for arm in ['A', 'B']:
        taught = taught_for(arm)
        rev = rot = 0
        for j in range(8):
            idx = P0[0*8+j]; p = tok(arm,1,idx); n = len(p)
            exp_rev = apply_rule(0, p); exp_rot = apply_rule(2, p)
            for t in taught:
                if len(t) != n: continue
                f = fit_affine_rt(p, t)
                if not f: continue
                s, o = f
                s2, o2 = pm(-s), pm(o + s*(n-1))
                if transform_rt(taught[t][0], s2, o2) == exp_rev: rev += 1; break
            for t in taught:
                if len(t) != n: continue
                f = fit_affine_rt(p, t)
                if not f: continue
                # rotleft: try to fit propagated map directly (no single affine exists)
                ok = False
                m1true = apply_rule(2, p)
                for t2 in taught:
                    if len(t2) != n: continue
                    # propagated delta at output k': o + s*((k'+1)%n); check vs true delta
                    if all(pm(o + s*((k+1) % n)) == pm(m1true[k]-t2[k]) for k in range(n)):
                        ok = True; break
                if ok: rot += 1; break
        print(f'  arm {arm}: reverse-via-propagation {rev}/8, rotleft-via-propagation {rot}/8')
    return True

# ---------------- attack 3: quadratic-fit memorizer (degree ladder) ----------------
def fit_quad_rt(p, t):
    if len(p) != len(t) or len(p) < 3: return None
    d = [pm(x - y) for x, y in zip(p, t)]
    o = d[0]
    # solve s,q from k=1,2: s+q = d1-d0, 2s+4q = d2-d0
    import math
    # 2s+4q-(2s+2q) = 2q = (d2-d0) - 2*(d1-d0)
    rhs = pm((d[2]-d[0]) - 2*(d[1]-d[0]))
    if math.gcd(2, 26) != 1:
        # 2q = rhs mod 26: solvable iff rhs even; two solutions; try both
        if rhs % 2 == 1: return None
        sols = []
        for q in [rhs//2, rhs//2 + 13]:
            s = pm((d[1]-d[0]) - q)
            if all(pm(o + s*k + q*k*k) == d[k] for k in range(3, len(p))):
                sols.append((s, o, q))
        return sols[0] if sols else None
    return None

def transform_quad(out, s, o, q):
    r = bytearray()
    for k, c in enumerate(out):
        base = 65 if 65 <= c <= 90 else 97
        r.append(base + pm((c - base) + o + s*k + q*k*k))
    return bytes(r)

def qmem_p0(arm, r, probe, taught):
    if r == 5 and is_sorted(probe): return probe
    for t in taught:
        if len(t) != len(probe): continue
        if len(t) == 2:
            # 3 params need 3 points: fall back to the affine fit on len-2
            # (the vacuous floor; same power as the 2-param class there)
            f = fit_affine_rt(probe, t)
            if f: return transform_rt(taught[t][r], *f)
            continue
        f = fit_quad_rt(probe, t)
        if f: return transform_quad(taught[t][r], *f)
    return None

def qmem_p2(arm, a, b, probe, taught):
    m1 = None
    for t in taught:
        if len(t) != len(probe): continue
        if len(t) == 2:
            f = fit_affine_rt(probe, t)
            if f: m1 = transform_rt(taught[t][a], *f); break
            continue
        f = fit_quad_rt(probe, t)
        if f: m1 = transform_quad(taught[t][a], *f); break
    if m1 is None: return None
    for t2 in taught:
        if len(t2) != len(m1): continue
        if len(m1) == 2:
            f2 = fit_affine_rt(m1, t2)
            if f2: return transform_rt(taught[t2][b], *f2)
            continue
        f2 = fit_quad_rt(m1, t2)
        if f2: return transform_quad(taught[t2][b], *f2)
    return None

def attack3():
    print("=== ATTACK 3: quadratic-fit memorizer (degree ladder) ===")
    for arm in ['C', 'B']:
        taught = taught_for(arm)
        p0 = [sum(1 for j in range(8)
                  if qmem_p0(arm, r, tok(arm,1,P0[r*8+j]), taught) == apply_rule(r, tok(arm,1,P0[r*8+j])))
              for r in range(6)]
        p2ok = 0; pairhits = {}
        for pi, (a,b) in enumerate(PAIRS):
            h = 0
            for j in range(4):
                p = tok(arm,2,P2[pi*4+j])
                if qmem_p2(arm, a, b, p, taught) == p2_exp(a, b, p): h += 1; p2ok += 1
            if h: pairhits[(a,b)] = h
        print(f'  quadmem arm{arm}: P0={p0}={sum(p0)}/48 P2={p2ok}/120 {pairhits}')
    return True

# ---------------- attack 4: free-delta clone (principled limit) ----------------
def attack4():
    print("=== ATTACK 4: free-delta clone (principled limit) ===")
    def src_index(r, k, n):
        # input position feeding output position k under rule r
        if r == 0: return n - 1 - k      # reverse
        if r == 1: return 0 if k == 0 else k - 1  # dupfirst
        if r == 2: return (k + 1) % n    # rotleft
        return k                        # droplast / upperfirst / sortchars
    for arm in ['A', 'B', 'C']:
        taught = taught_for(arm)
        p0 = []
        for r in range(6):
            h = 0
            for j in range(8):
                idx = P0[r*8+j]; p = tok(arm,1,idx); n = len(p)
                t = next(t for t in taught if len(t) == n)
                tout = taught[t][r]
                exp = apply_rule(r, p)
                if len(tout) != len(exp):
                    continue
                got = bytearray()
                for k, c in enumerate(tout):
                    base = 65 if 65 <= c <= 90 else 97
                    got.append(base + pm((c - base) + (p[src_index(r, k, n)] - t[src_index(r, k, n)])))
                h += bytes(got) == exp
            p0.append(h)
        # (3,4) chaining: free-delta step-1 is exact for droplast (identity sigma)
        ch = 0
        for j in range(4):
            p = tok(arm,2,P2[19*4+j])
            m1 = apply_rule(3, p)  # exact: delta copied per position
            t2 = next(t for t in taught if len(t) >= len(m1))
            exp = p2_exp(3, 4, p)
            got = bytearray()
            for k, c in enumerate(taught[t2][4][:len(m1)]):
                base = 65 if 65 <= c <= 90 else 97
                got.append(base + pm((c - base) + (m1[k] - t2[k])))
            ch += bytes(got) == exp
        print(f'  freelta arm{arm}: P0={p0}={sum(p0)}/48 (3,4)={ch}/4')
    # prereg-specified clone: sigma=id for every rule (applies delta at output positions)
    print("  --- prereg-specified sigma=id clone (delta applied at output positions) ---")
    for arm in ['A', 'B', 'C']:
        taught = taught_for(arm)
        p0 = []
        for r in range(6):
            h = 0
            for j in range(8):
                idx = P0[r*8+j]; p = tok(arm,1,idx); n = len(p)
                t = next(t for t in taught if len(t) == n)
                tout = taught[t][r]
                exp = apply_rule(r, p)
                if len(tout) != len(exp) or len(tout) > n:
                    continue  # sigma=id clone undefined when output longer than input
                got = bytearray()
                for k, c in enumerate(tout):
                    base = 65 if 65 <= c <= 90 else 97
                    got.append(base + pm((c - base) + (p[k] - t[k])))
                h += bytes(got) == exp
            p0.append(h)
        print(f'  sigma=id clone arm{arm}: P0={p0}={sum(p0)}/48')
    return True

# ---------------- attack 5: combiner white-box audit ----------------
def attack5():
    print("=== ATTACK 5: combiner white-box audit ===")
    src = open('/home/hatch/workspace/composition_followup/job3_affine/affine_test.zag').read()
    # extract gen_p0/gen_p2/gen_p3 bodies
    import re
    bodies = {}
    for fn in ['gen_p0', 'gen_p2', 'gen_p3']:
        m = re.search(r'fn ' + fn + r'\(.*', src)
        start = src.index('{', m.start()) + 1
        depth = 1; i = start
        while depth:
            if src[i] == '{': depth += 1
            elif src[i] == '}': depth -= 1
            i += 1
        bodies[fn] = src[start:i-1]
    bad = ['salt_c', 'tokfill', 'train_index', 'taught', 'fit_affine', '_zag_arg',
           'p0_index', 'pmod26(7', 'mem_']
    leaks = {fn: [b for b in bad if b in body] for fn, body in bodies.items()}
    for fn, hits in leaks.items():
        print(f'  {fn}: generator-algebra references: {hits if hits else "NONE"}')
    sig_ok = all('taught' not in bodies[fn] and 'arm' not in bodies[fn].split(')')[0]
                  for fn in bodies)
    print(f'  gen_* signatures take only (probe, out) [+rule ids]: {sig_ok}')
    # cross-arm output-pattern identity: combiner ok-flags all 1 on all arms
    pats = {}
    for mode in ['genA','genB','genC']:
        flags = []
        for line in open(f'{RUN1}/{mode}.out'):
            t = line.split()
            if t[0] == 'P0': flags.append(t[3])
            elif t[0] == 'P2': flags.append(t[4])
            elif t[0] == 'P3': flags.append(t[2])
        pats[mode] = ''.join(flags)
    print(f'  ok-flag patterns identical across arms: {pats["genA"]==pats["genB"]==pats["genC"]} '
          f'(all ones: {set(pats["genA"])=={"1"}})')
    return all(not v for v in leaks.values())

if __name__ == '__main__':
    r1 = attack1()
    p0nv, p2nv, phnv = attack2()
    best = attack2b()
    attack2c()
    attack3()
    attack4()
    r5 = attack5()
    print()
    print(f"attack1 fidelity: {'PASS' if r1 else 'FAIL'}")
    print(f"attack5 combiner audit: {'PASS' if r5 else 'FAIL'}")
