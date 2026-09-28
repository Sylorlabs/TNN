#!/usr/bin/env python3
"""Crew 3: precise verdict classification incl. union cases (deviation c audit)."""
import re, pathlib
from collections import Counter

REPRO = pathlib.Path.home() / "workspace/growwithme_retry/redteam/repro"
RESEAL = pathlib.Path.home() / "workspace/growwithme_retry/redteam/docs/lab/growwithme/retry/probes_resealed"
STOP = set("""the and for with from that this are was were has have had will would can could
should must may might shall not no yes its his her their our your than then when where what which
who whom whose why how all any both each few more most other some such only own same too very just also
a an of to in on is it as at be by or if do does did""".split())

def load_probes(s):
    text = (RESEAL / f"immediate_S{s}.md").read_text()
    return [(m.group(1), m.group(2).strip(), m.group(3).split("\n")[0].strip())
            for m in re.finditer(r"### (\S+)\nQ: (.*?)\nKey: (.*?)\n", text, re.DOTALL)]

def norm(x):
    x = x.lower(); x = re.sub(r"[^a-z0-9 ]", " ", x); return re.sub(r"\s+", " ", x).strip()

def strip_note(a): return re.sub(r"\s*\[m3:.*?\]\s*$", "", a).strip()

def hit(ans, key):
    na, nk = norm(strip_note(ans)), norm(key)
    if nk in na or na in nk: return True
    kw = [w for w in nk.split() if len(w) > 3 and w not in STOP]
    return (sum(1 for w in kw if w in na) / len(kw) >= 0.70) if kw else nk in na

def traces(s):
    text = (REPRO / f"D_rt1/snapshot_S{s}.txt").read_text()
    out = {}
    pat = re.compile(r"TRACE \d+ \|\| kind=m3-deliberation \|\| ref=(.*?) \|\| considered=(.*?) \|\| evidence=(.*?) \|\| verdict=(.*?) \|\| reason=")
    for m in pat.finditer(text):
        out[m.group(1)] = (m.group(2), m.group(3), m.group(4))
    return out

cls = Counter(); union_rows = []
for s in range(1, 7):
    probes = load_probes(s)
    tr = traces(s)
    anss = [l[5:].strip() for l in (REPRO / f"D_rt1/probe_immediate_S{s}.txt").read_text().splitlines() if l.startswith("A || ")]
    for (qid, q, key), ans in zip(probes, anss):
        t = tr.get(q[:40])
        h = hit(ans, key)
        right = qid[:-2]
        if t is None:
            cls["depb-withhold-hit" if h else "depb-withhold-miss"] += 1
            continue
        cons, ev, ver = t
        if "tie-withhold" in ver:
            cls["tie-withhold"] += 1
        elif ver.startswith("union"):
            w, p = ver.replace("union ", "").split("+")
            cls["union-hit" if h else "union-miss"] += 1
            union_rows.append((s, qid, ver, cons, ev, "HIT" if h else "MISS", right))
        else:
            w = ver.replace("single ", "")
            cls["single-hit" if h else "single-miss"] += 1
print(dict(cls))
print("\nUNION verdicts:")
for r in union_rows:
    print(f"S{r[0]} {r[1]}: {r[2]} -> {r[5]} (right={r[6]})")
    print(f"    cons: {r[3][:120]}")
