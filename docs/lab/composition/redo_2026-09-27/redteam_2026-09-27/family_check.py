"""Independent Python re-implementation of the srule_engine.zag hypothesis family.
Used by the red team to check whether the 12 teaching examples per rule
UNIQUE determine the induced program within the 40,500-candidate family.
Mirrors sr_apply / sr_sort_insert / sr_map_byte / sr_try_prog exactly.
"""
from itertools import product

def sr_map_byte(c, mode):
    if mode == 1 and 97 <= c <= 122: return c - 32
    if mode == 2 and 65 <= c <= 90: return c + 32
    return c

def sort_insert(s):
    a = list(s)
    for i in range(1, len(a)):
        key = a[i]; j = i - 1
        while j >= 0 and a[j] > key:
            a[j+1] = a[j]; j -= 1
        a[j+1] = key
    return a

def decode_ov(ov, n):
    if ov == 1: return 0
    if ov == 2: return 1
    if ov == 3: return n - 2
    if ov == 4: return n - 1
    return -1

def apply_prog(s, pre, la, src, fov, lov, mf, mm, ml):
    n = len(s)
    sc = sort_insert(s) if pre == 1 else list(s)
    m = n + la
    if m < 1: return None
    out = []
    for i in range(m):
        if i == 0 and fov != 0:
            si = decode_ov(fov, n)
        elif i == m - 1 and lov != 0:
            si = decode_ov(lov, n)
        else:
            if src == 0: si = i
            elif src == 1: si = n - 1 - i
            elif src == 2: si = (i + 1) % n
            elif src == 3: si = (i - 1 + n) % n
            elif src == 4: si = max(0, i - 1)
            elif src == 5: si = min(n - 1, i + 1)
        if si < 0 or si >= n: return None
        c = sc[si]
        if i != 0 and i != m - 1:
            c = sr_map_byte(c, mm)
        else:
            if i == m - 1: c = sr_map_byte(c, ml)
            if i == 0: c = sr_map_byte(c, mf)
        out.append(c)
    return bytes(out)

def find_consistent(examples):
    """examples: list of (in_bytes, out_bytes). Returns list of programs
    (pre,la,src,fov,lov,mf,mm,ml) consistent, in the engine's enumeration order."""
    la = None
    for (xb, yb) in examples:
        d = len(yb) - len(xb)
        if la is None: la = d
        elif d != la: return []
    if la < -2 or la > 2: return []
    # need >= 2 distinct inputs
    if len({xb for xb, yb in examples}) < 2: return []
    res = []
    for pre in (0, 1):
        for src in range(6):
            for fov in range(5):
                for lov in range(5):
                    for mf in range(3):
                        for mm in range(3):
                            for ml in range(3):
                                ok = True
                                for (xb, yb) in examples:
                                    if apply_prog(list(xb), pre, la, src, fov, lov, mf, mm, ml) != yb:
                                        ok = False; break
                                if ok:
                                    res.append((pre, la, src, fov, lov, mf, mm, ml))
    return res

# ---- token generator, mirrors drive_redo.py ----
def tok(i, saltC):
    n = 2 + (i % 4)
    cs = []
    for k in range(n):
        cs.append(97 + (i * 7 + k * saltC + k * k) % 26)
    return bytes(cs)

def true_rule(name, s):
    if name == "reverse": return s[::-1]
    if name == "dupfirst": return s[:1] + s
    if name == "droplast": return s[:-1]
    if name == "rotleft": return s[1:] + s[:1]
    if name == "upperfirst": return s[:1].upper() + s[1:]
    if name == "sortchars": return bytes(sorted(s))
    raise ValueError(name)

def main():
    rules = ["reverse", "dupfirst", "droplast", "rotleft", "upperfirst", "sortchars"]
    train_idx = list(range(0, 6)) + list(range(700, 706))
    probe_idx = list(range(6, 14))
    for r in rules:
        exs = [(tok(i, 13), true_rule(r, tok(i, 13))) for i in train_idx]
        con = find_consistent(exs)
        probes = [tok(i, 17) for i in probe_idx]
        # do all consistent programs agree on the 8 probe tokens?
        disagree_probe = 0
        for p in probes:
            outs = {apply_prog(list(p), *c) for c in con}
            outs.discard(None)
            if len(outs) > 1: disagree_probe += 1
        # do they agree on all byte-strings of length 1..5 over a..c?
        import itertools
        disagree_all = 0; total = 0; examples_hit = []
        for L in (1, 2, 3):
            for tup in itertools.product((97, 98, 99), repeat=L):
                total += 1
                s = bytes(tup)
                outs = {apply_prog(list(s), *c) for c in con}
                outs.discard(None)
                if len(outs) > 1: disagree_all += 1
                elif total <= 0: pass
        print(f"{r:12s} consistent={len(con):5d} first={con[0]} probe_disagree={disagree_probe}/8 abc123_disagree={disagree_all}/{total}")

if __name__ == "__main__":
    main()
