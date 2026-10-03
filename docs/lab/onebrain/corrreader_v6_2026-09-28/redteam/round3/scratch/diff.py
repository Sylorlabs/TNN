#!/usr/bin/env python3
"""Differential harness: strict-§2 reference vs the Zag probe (utterance.zag)."""
import subprocess, sys
sys.path.insert(0, "/tmp/r3")
from ou_ref import annotate

def probe(q):
    p = subprocess.run(["/tmp/r3/probe", q], capture_output=True, text=True)
    out = []
    for line in p.stdout.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        jpart, rest = line.split(":", 1)
        # format: j: 'tok' st=N
        try:
            st = int(rest.rsplit("st=", 1)[1])
            tok = rest.split("'", 2)[1]
        except Exception:
            continue
        out.append((tok, st))
    return out

def check(query):
    ref_sts, ref_toks = annotate(query)
    pr = probe(query)
    divs = []
    if len(pr) != len(ref_toks):
        return [("TOKCOUNT", len(ref_toks), len(pr), ref_toks,
                 [t for t, s in pr])]
    for j, ((rt, rs), (pt, ps)) in enumerate(zip(zip(ref_toks, ref_sts), pr)):
        if rt != pt:
            divs.append(("TOK", j, rt, pt, rs, ps))
        elif rs != ps:
            divs.append(("ST", j, rt, rs, ps))
    return divs

if __name__ == "__main__":
    unesc = "--unescape" in sys.argv
    queries = [l.rstrip("\n") for l in open(sys.argv[1]) if l.strip()]
    if unesc:
        queries = [q.encode().decode("unicode_escape") for q in queries]
    ndiv = 0
    for q in queries:
        d = check(q)
        if d:
            ndiv += 1
            print("DIVERGE:", q)
            for x in d:
                print("   ", x)
    print(f"checked={len(queries)} diverged={ndiv}")
