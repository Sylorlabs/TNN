#!/usr/bin/env python3
"""FORK B white-box check: every derived span must be a verbatim copy of an
earlier span (or an L9 fixed concatenation of two earlier spans).
Anything else = novel-span synthesis = the negative is broken."""
import re, sys

def check(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"^LEDGER:\n(.*?)^AUDIT:", txt, re.M | re.S)
    if not m:
        return (path, "NO-LEDGER", 0, 0, 0, [])
    states = []  # (idx, src, lic, text)
    for line in m.group(1).splitlines():
        mm = re.match(r"^S(\d+) src=([a-z]+)( kid=K\d+)? lic=(-?\d+) p=\[([-\d]+),([-\d]+),([-\d]+)\][^:]*: (.*)$", line)
        if mm:
            states.append((int(mm.group(1)), mm.group(2), int(mm.group(4)), mm.group(7)))
    states.sort()
    derived_srcs = {"prop", "pbc", "subgoal"}
    n_der = n_ok = n_l9 = 0
    viol = []
    for pos, (idx, src, lic, text) in enumerate(states):
        if src not in derived_srcs:
            continue
        n_der += 1
        earlier = [t for (_, _, _, t) in states[:pos]]
        if any(text in e for e in earlier):
            n_ok += 1
            continue
        if lic == 9:
            # L9: fixed concatenation of two earlier spans
            ok = False
            for k in range(1, len(text)):
                if any(text[:k] in e for e in earlier) and any(text[k:] in e for e in earlier):
                    ok = True
                    break
            if ok:
                n_l9 += 1
                continue
        viol.append((idx, src, lic, text[:80]))
    status = "CLEAN" if not viol else "VIOLATIONS"
    return (path, status, n_der, n_ok, n_l9, viol)

tot_v = 0
for p in sys.argv[1:]:
    path, status, n_der, n_ok, n_l9, viol = check(p)
    print(f"{path}: {status} derived={n_der} verbatim={n_ok} l9concat={n_l9} violations={len(viol)}")
    for v in viol:
        print(f"    VIOL S{v[0]} src={v[1]} lic={v[2]}: {v[3]!r}")
    tot_v += len(viol)
print("TOTAL_VIOLATIONS:", tot_v)
sys.exit(1 if tot_v else 0)
