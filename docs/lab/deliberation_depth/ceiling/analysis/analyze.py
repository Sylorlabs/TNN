#!/usr/bin/env python3
"""H5B analysis (PREREG_H5B.md v1.1 G5/G6, kill bars i-v, saturation, cap-null, wason).

Reads the 108-cell sweep at ~/workspace/scratch-h5b/sweep/ and the frozen
H5 records at ~/workspace/scratch-h5/sweep/. Writes a JSON summary and
prints the human-readable report. Exit 0 iff all validity gates pass.
"""
import json
import os
import re
import sys

NEW = os.path.expanduser("~/workspace/scratch-h5b/sweep")
OLD = os.path.expanduser("~/workspace/scratch-h5/sweep")
BATS = ["admit", "revoke", "logic", "trap", "cost", "ceiling"]
CFGS = ["d1", "d2", "d4", "d8", "d16", "d32", "d64", "adaptive", "bound"]
OLD_CFG = {"d1": "d1", "d2": "d2", "d4": "d4", "d8": "d8", "d16": "deep16",
           "adaptive": "adaptive"}
fails = []
report = []


def note(s):
    report.append(s)
    print(s)


def check(name, cond, detail=""):
    note(("PASS " if cond else "FAIL ") + name + (" | " + detail if detail else ""))
    if not cond:
        fails.append(name)


def load_results(path):
    recs = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                r = json.loads(line)
                recs[r["id"]] = r
    return recs


def load_stops(path):
    """item id -> stop reason from VERDICT ledger detail."""
    stops = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except Exception:
                continue
            if e.get("action") == "VERDICT":
                m = re.search(r"stop=([a-z]+)", e.get("detail", ""))
                stops[e["item"]] = m.group(1) if m else "?"
    return stops


# ---------- load new sweep ----------
newr, newstop = {}, {}
for b in BATS:
    for c in CFGS:
        p = os.path.join(NEW, b, c, "a", "results.jsonl")
        newr[(b, c)] = load_results(p)
        newstop[(b, c)] = load_stops(os.path.join(NEW, b, c, "a", "ledger.jsonl"))

# ---------- G5 replication: H5B binary vs frozen H5 records ----------
note("== G5 replication (H5B binary, modes 0/1/2 vs frozen H5 records) ==")
n_mismatch = 0
for b in BATS[:5]:
    for c, oc in OLD_CFG.items():
        old = load_results(os.path.join(OLD, "%s_%s_A.jsonl" % (oc, b)))
        new = newr[(b, c)]
        if set(old) != set(new):
            check("G5 %s/%s id sets" % (b, c), False,
                  "old=%d new=%d" % (len(old), len(new)))
            continue
        bad = [i for i in old
               if (old[i]["verdict"], old[i]["confidence"],
                   old[i]["rounds_used"], old[i]["evidence_consumed"]) !=
               (new[i]["verdict"], new[i]["confidence"],
                new[i]["rounds_used"], new[i]["evidence_consumed"])]
        n_mismatch += len(bad)
        check("G5 %s/%s per-item exact" % (b, c), not bad,
              "n=%d mism=%d%s" % (len(old), len(bad), " e.g.%s" % bad[:2] if bad else ""))
# d32/d64 vs d16 on old batteries.
# AS-WRITTEN prereg gate (v1.1): expected d32/d64 == d16 by natural termination.
# MEASUREMENT FOUND: the background premise was false — the admit battery has
# 48 items with >16 evidence (up to 48), so d16 was a FIXED truncation there,
# not natural termination. Verdicts are identical everywhere (accuracy null
# holds); rounds differ only on admit's 48 long items. Harness exonerated:
# the per-item H5 replication above passed exactly.
for b in BATS[:5]:
    for c in ["d32", "d64"]:
        a, d16 = newr[(b, c)], newr[(b, "d16")]
        same = all(a[i]["verdict"] == d16[i]["verdict"] and
                   a[i]["rounds_used"] == d16[i]["rounds_used"] for i in a)
        vsame = all(a[i]["verdict"] == d16[i]["verdict"] for i in a)
        rd = sum(1 for i in a if a[i]["rounds_used"] != d16[i]["rounds_used"])
        check("G5-null(as-written) %s/%s == d16" % (b, c), same,
              "verdicts-identical=%s rounds-diffs=%d" % (vsame, rd))
        check("G5-null(corrected) %s/%s verdicts == d16" % (b, c), vsame, "")
note("total G5 field mismatches: %d" % n_mismatch)

# ---------- per-battery x config tables ----------
note("== accuracy / mean rounds / mean evidence ==")
acc, mrounds, mev = {}, {}, {}
for b in BATS:
    for c in CFGS:
        rs = list(newr[(b, c)].values())
        n = len(rs)
        acc[(b, c)] = sum(r["correct"] for r in rs) / n
        mrounds[(b, c)] = sum(r["rounds_used"] for r in rs) / n
        mev[(b, c)] = sum(r["evidence_consumed"] for r in rs) / n
hdr = "battery " + "".join("%8s" % c for c in CFGS)
note("ACC " + hdr)
for b in BATS:
    note("ACC %-7s" % b + "".join("%8.3f" % acc[(b, c)] for c in CFGS))
note("ROUNDS " + hdr)
for b in BATS:
    note("RND %-7s" % b + "".join("%8.2f" % mrounds[(b, c)] for c in CFGS))

# ---------- stop-reason distributions (adaptive, bound) ----------
note("== stop-reason distribution ==")
for b in BATS:
    for c in ["adaptive", "bound"]:
        dist = {}
        for i, s in newstop[(b, c)].items():
            dist[s] = dist.get(s, 0) + 1
        note("STOP %-7s %-8s %s" % (b, c, dict(sorted(dist.items()))))

# ---------- G6 cap-hit rates ----------
for b in BATS:
    for c in ["adaptive", "bound"]:
        hits = sum(1 for s in newstop[(b, c)].values() if s == "cap")
        check("G6 cap-hits %s/%s == 0" % (b, c), hits == 0, "hits=%d" % hits)

# ---------- kill bar (i): §6 unsafe on P ----------
aP, dP = acc[("ceiling", "adaptive")], acc[("ceiling", "d64")]
# P-only accuracy: recompute on P family
def famacc(b, c, fam):
    rs = [r for i, r in newr[(b, c)].items() if i.split("-")[1] == fam]
    return sum(r["correct"] for r in rs) / len(rs)
p_ad = famacc("ceiling", "adaptive", "P")
p_64 = famacc("ceiling", "d64", "P")
check("KB(i) §6 unsafe on P", p_ad < p_64 - 0.01,
      "adaptive=%.3f d64=%.3f" % (p_ad, p_64))
p5 = all(newr[("ceiling", "adaptive")][i]["rounds_used"] == 5
         for i in newr[("ceiling", "adaptive")] if i.split("-")[1] == "P")
check("KB(i) adaptive stops at 5 on 40/40 P", p5, "")

# ---------- kill bar (ii): overthinking on O ----------
o_items = [i for i in newr[("ceiling", "d4")] if i.split("-")[1] == "O"]
ot = sum(1 for i in o_items
         if newr[("ceiling", "d4")][i]["correct"] == 1
         and newr[("ceiling", "d64")][i]["correct"] == 0)
check("KB(ii) overthinking 40/40 on O", ot == 40, "rate=%d/40" % ot)

# ---------- kill bar (iii): D dose monotonicity ----------
doses = {}
for i, r in newr[("ceiling", "adaptive")].items():
    if i.split("-")[1] == "D":
        doses.setdefault(int(i.split("-")[2]), []).append(r["rounds_used"])
exp = {0: 2, 1: 3, 2: 4, 6: 8}
mono = all(all(x == exp[d] for x in v) for d, v in doses.items())
dacc = all(newr[("ceiling", "adaptive")][i]["correct"] == 1
           for i in newr[("ceiling", "adaptive")] if i.split("-")[1] == "D")
check("KB(iii) D adaptive rounds 2/3/4/8 by dose", mono,
      str({d: sorted(set(v)) for d, v in doses.items()}))
check("KB(iii) D adaptive accuracy 1.000", dacc, "")

# ---------- kill bar (iv): saturation points ----------
note("== saturation points ==")
FIXED = ["d1", "d2", "d4", "d8", "d16", "d32", "d64"]
for b in BATS:
    aa = [acc[(b, c)] for c in FIXED]
    mx = max(aa)
    S, flag = None, ""
    for j, c in enumerate(FIXED):
        if aa[j] == mx and all(x == mx for x in aa[j:]):
            S, flag = c, ("TOP-OF-SWEEP" if j == len(FIXED) - 1 and mx > aa[j-1] else "")
            break
    if S is None:
        S, flag = "NON-MONOTONE", ""
    note("SAT %-7s S=%-12s acc=%s" % (b, S, "/".join("%.3f" % x for x in aa)) + (" " + flag if flag else ""))

# ---------- kill bar (v): bound vs §6 ----------
note("== KB(v-a) firing counts: bound vs §6 ==")
for b in BATS:
    six = sum(1 for s in newstop[(b, "adaptive")].values() if s == "six")
    bnd = sum(1 for s in newstop[(b, "bound")].values() if s == "bound")
    note("FIRE %-7s six=%3d bound=%3d" % (b, six, bnd))

note("== KB(v-b) P: §6 stops at 5 wrong, bound refuses then correct ==")
p_ids = [i for i in newr[("ceiling", "adaptive")] if i.split("-")[1] == "P"]
refused = 0
for i in sorted(p_ids):
    ra, rb = newr[("ceiling", "adaptive")][i], newr[("ceiling", "bound")][i]
    sa, sb = newstop[("ceiling", "adaptive")][i], newstop[("ceiling", "bound")][i]
    f = int(i.split("-")[2])
    ok = (ra["rounds_used"] == 5 and sa == "six" and ra["correct"] == 0
          and rb["rounds_used"] == f and sb == "bound" and rb["correct"] == 1)
    refused += ok
check("KB(v-b) bound refuses 5, stops at flip, correct 40/40 P", refused == 40,
      "%d/40" % refused)
# per-flip-round cross-tab
for f in [6, 12, 20, 40]:
    ids = [i for i in p_ids if int(i.split("-")[2]) == f]
    ar = sorted(set(newr[("ceiling", "adaptive")][i]["rounds_used"] for i in ids))
    br = sorted(set(newr[("ceiling", "bound")][i]["rounds_used"] for i in ids))
    ac = sum(newr[("ceiling", "adaptive")][i]["correct"] for i in ids)
    bc = sum(newr[("ceiling", "bound")][i]["correct"] for i in ids)
    note("P f=%2d: §6 rounds=%s acc=%d/10 | bound rounds=%s acc=%d/10"
         % (f, ar, ac, br, bc))

note("== KB(v-c) O: §6 stops at 5 correct, bound refuses then wrong ==")
o_ids = [i for i in newr[("ceiling", "adaptive")] if i.split("-")[1] == "O"]
refused_o = 0
for i in sorted(o_ids):
    ra, rb = newr[("ceiling", "adaptive")][i], newr[("ceiling", "bound")][i]
    sa, sb = newstop[("ceiling", "adaptive")][i], newstop[("ceiling", "bound")][i]
    f = int(i.split("-")[2])
    ok = (ra["rounds_used"] == 5 and sa == "six" and ra["correct"] == 1
          and rb["rounds_used"] == f and sb == "bound" and rb["correct"] == 0)
    refused_o += ok
check("KB(v-c) bound refuses 5, stops at flip, wrong 40/40 O", refused_o == 40,
      "%d/40" % refused_o)
for f in [6, 12, 20, 40]:
    ids = [i for i in o_ids if int(i.split("-")[2]) == f]
    ar = sorted(set(newr[("ceiling", "adaptive")][i]["rounds_used"] for i in ids))
    br = sorted(set(newr[("ceiling", "bound")][i]["rounds_used"] for i in ids))
    ac = sum(newr[("ceiling", "adaptive")][i]["correct"] for i in ids)
    bc = sum(newr[("ceiling", "bound")][i]["correct"] for i in ids)
    note("O f=%2d: §6 rounds=%s acc=%d/10 | bound rounds=%s acc=%d/10"
         % (f, ar, ac, br, bc))

note("== KB(v-d) accuracy/cost by stop reason ==")
for b in BATS:
    for c in ["adaptive", "bound"]:
        by = {}
        for i, r in newr[(b, c)].items():
            s = newstop[(b, c)][i]
            a, n, rd = by.get(s, (0, 0, 0))
            by[s] = (a + r["correct"], n + 1, rd + r["rounds_used"])
        for s, (a, n, rd) in sorted(by.items()):
            note("BYSTOP %-7s %-8s %-7s acc=%.3f meanrounds=%.2f n=%d"
                 % (b, c, s, a / n, rd / n, n))

# ---------- wason replication on P: d32 misses f40, d64 catches it ----------
note("== wason replication on P (f40) ==")
f40 = [i for i in p_ids if int(i.split("-")[2]) == 40]
w32 = sum(newr[("ceiling", "d32")][i]["correct"] for i in f40)
w64 = sum(newr[("ceiling", "d64")][i]["correct"] for i in f40)
ev32 = sorted(set(newr[("ceiling", "d32")][i]["evidence_consumed"] for i in f40))
check("wason P-f40: d32 misses (0/10), d64 catches (10/10)", w32 == 0 and w64 == 10,
      "d32=%d/10 d64=%d/10 ev32=%s" % (w32, w64, ev32))
# rounds==evidence until natural termination on P at d64
one2one = all(newr[("ceiling", "d64")][i]["rounds_used"] ==
              newr[("ceiling", "d64")][i]["evidence_consumed"] for i in p_ids)
check("wason P: rounds==evidence 1-to-1 at d64", one2one, "")

# ---------- bound accuracy == adaptive accuracy where exhaustion is safe ----------
for b in BATS[:5]:
    ba = sum(r["correct"] for r in newr[(b, "bound")].values()) / len(newr[(b, "bound")])
    aa = acc[(b, "adaptive")]
    check("bound acc == adaptive acc on %s" % b, abs(ba - aa) < 1e-9,
          "bound=%.3f adaptive=%.3f" % (ba, aa))
d_bnd = famacc("ceiling", "bound", "D")
d_ad = famacc("ceiling", "adaptive", "D")
check("bound acc == adaptive acc on D", abs(d_bnd - d_ad) < 1e-9 and d_bnd == 1.0,
      "bound=%.3f adaptive=%.3f" % (d_bnd, d_ad))

note("ANALYSIS %s (%d failures)" % ("PASS" if not fails else "FAIL", len(fails)))
with open(os.path.join(NEW, "analysis_summary.json"), "w") as f:
    json.dump({"fails": fails,
               "acc": {"%s/%s" % k: v for k, v in acc.items()},
               "mean_rounds": {"%s/%s" % k: v for k, v in mrounds.items()}},
              f, indent=1)
sys.exit(1 if fails else 0)
