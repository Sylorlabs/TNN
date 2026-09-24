#!/usr/bin/env python3
"""Score FS-GR2 red-team corpus runs.

Per candidate per corpus:
  FI-like        = disp=INSTALL and judgment != truth
  resolve rate   = outcome != UNRESOLVED
  correct-install= disp=INSTALL and judgment == truth
Plus substructure breakdowns for systematic-break detection.
"""
import os, json
from collections import Counter

RT = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/work_fsgr2/REDTEAM"
DIRS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

# (corpus, fixture_basename) -> truth ; plus mdir map for rtD
truth = {}
mdir = {}
for line in open(RT + "/corpora/MANIFEST.txt"):
    if line.startswith("#") or not line.strip():
        continue
    tag, fn, t = line.strip().split(" ")
    if tag == "rtD-mdir":
        mdir[fn] = t.split("=", 1)[1]
    else:
        truth[(tag, fn)] = t.split("=", 1)[1]

def sub(c, n):
    if c == "rtA":
        L = (4, 8, 16)[(n % 18) // 6]
        return ("L=%d,dir=%s,orient=%d" % (L, DIRS[n // 18], n % 6), "L=%d" % L)
    if c == "rtB":
        return ("dir=%s,seed=%d" % (DIRS[n // 5], n % 5), "dir=%s" % DIRS[n // 5])
    if c == "rtC":
        return ("dir=%s,ramp-orient=%d" % (DIRS[n // 8], n % 8), "dir=%s" % DIRS[n // 8])
    if c == "rtD":
        return ("dir=%s,seed=%d" % (DIRS[n // 5], n % 5), "dir=%s" % DIRS[n // 5])

report = {}
for m in (4, 5, 6, 7):
    for c in ("rtA", "rtB", "rtC", "rtD"):
        claim = [l.rstrip("\n").split("\t") for l in open("%s/claim_%s.tsv" % (RT, c))]
        raw = [l for l in open("%s/raw/mot%d_%s.raw" % (RT, m, c)) if l.strip()]
        assert len(claim) == len(raw), (m, c, len(claim), len(raw))
        rows = []
        for (path, cid), rl in zip(claim, raw):
            fn = os.path.basename(path)
            kv = dict(x.split("=", 1) for x in rl.strip().split(" ") if "=" in x)
            t = truth[(c, fn)]
            rows.append({"judgment": kv["judgment"], "outcome": kv["outcome"],
                         "disp": kv["disp"], "truth": t, "fn": fn,
                         "n": int(fn.split("_")[1].split(".")[0]),
                         "mdir": mdir.get(fn)})
        n = len(rows)
        fi = [r for r in rows if r["disp"] == "INSTALL" and r["judgment"] != r["truth"]]
        ci = [r for r in rows if r["disp"] == "INSTALL" and r["judgment"] == r["truth"]]
        res = [r for r in rows if r["outcome"] != "UNRESOLVED"]
        inst = [r for r in rows if r["disp"] == "INSTALL"]
        # echo sanity: sup's re-derived judgment vs formation judgment (claimid)
        echo_ok = all(r["judgment"] == DIRS[int(claim[i][1]) - 1] or claim[i][1] == "0"
                      for i, r in enumerate(rows))
        key = "mot%d/%s" % (m, c)
        report[key] = {
            "n": n,
            "fi_like": (len(fi), n),
            "resolve": (len(res), n),
            "correct_install": (len(ci), n),
            "n_install": len(inst),
            "echo_ok": echo_ok,
            "fi_sub": Counter(sub(c, r["n"])[1] for r in fi),
            "inst_sub": Counter(sub(c, r["n"])[1] for r in inst),
            "fi_rows": [(r["fn"], r["judgment"], r["truth"], r["outcome"],
                         r.get("mdir"), sub(c, r["n"])[0]) for r in fi],
        }

print(json.dumps(report, indent=1, default=str))
