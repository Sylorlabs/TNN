#!/usr/bin/env python3
"""Crew 3: failure-envelope statistics from m3-deliberation traces.
Per session: candidate-set size, discriminator count, verdict mix.
Plus: spurious-match taxonomy for wrong-candidate cases."""
import re, pathlib
from collections import Counter

REPRO = pathlib.Path.home() / "workspace/growwithme_retry/redteam/repro"
RESEAL = pathlib.Path.home() / "workspace/growwithme_retry/redteam/docs/lab/growwithme/retry/probes_resealed"

def load_q(session):
    text = (RESEAL / f"immediate_S{session}.md").read_text()
    return re.findall(r"### (\S+)\nQ: (.*?)\nKey:", text, re.DOTALL)

def traces_for(session):
    text = (REPRO / f"D_rt1/snapshot_S{session}.txt").read_text()
    out = {}
    pat = re.compile(r"TRACE \d+ \|\| kind=m3-deliberation \|\| ref=(.*?) \|\| considered=(.*?) \|\| evidence=(.*?) \|\| verdict=(.*?) \|\| reason=")
    for m in pat.finditer(text):
        ref, cons, ev, ver = m.group(1), m.group(2), m.group(3), m.group(4)
        cands = re.findall(r"(F\d+-\d+):(\d+)", cons)
        more = re.search(r"\+(\d+) more", cons)
        nc = len(cands) + (int(more.group(1)) if more else 0)
        dm = re.search(r"disc:\{([^}]*)\}", ev)
        disc = [w for w in dm.group(1).split(",") if w] if dm else []
        cov = re.findall(r"(F\d+-\d+):(\d+)/(\d+)", ev)
        out.setdefault(ref, []).append(dict(nc=nc, nd=len(disc), disc=disc, cov=cov, ver=ver))
    return out

print("session | n | mean_nc | mean_nd | nd=0 frac | tie | single | union")
for s in range(1, 7):
    qs = load_q(s)
    tr = traces_for(s)
    ncs, nds, vers = [], [], []
    for qid, q in qs:
        ref = q.strip()[:40]
        t = tr.get(ref, [None])[-1]
        if t is None:
            print("  MISSING TRACE", s, qid); continue
        ncs.append(t["nc"]); nds.append(t["nd"]); vers.append(t["ver"])
    n = len(ncs)
    tie = sum(1 for v in vers if "tie" in v); sing = sum(1 for v in vers if v.startswith("single")); uni = n - tie - sing
    print(f"S{s} ({s*20} facts) | {n:3d} | {sum(ncs)/n:7.2f} | {sum(nds)/n:7.2f} | {sum(1 for d in nds if d==0)/n:8.2f} | {tie:3d} | {sing:3d} | {uni:3d}")

# discriminator word frequency among tie-withholds vs singles (which words stop discriminating)
print("\ndiscriminator words in TIE traces (top 20):")
tie_words = Counter(); sing_words = Counter()
for s in range(1, 7):
    qs = load_q(s); tr = traces_for(s)
    for qid, q in qs:
        t = tr.get(q.strip()[:40], [None])[-1]
        if t is None: continue
        (tie_words if "tie" in t["ver"] else sing_words).update(t["disc"])
print(" TIE:", tie_words.most_common(20))
print(" SINGLE:", sing_words.most_common(20))
