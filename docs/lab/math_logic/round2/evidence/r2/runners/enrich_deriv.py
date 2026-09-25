#!/usr/bin/env python3
"""Enrich results_formal_quot.json with QUOT-native derivation counters.
Parses each problem's .r0 output file for:
  committed, conflicts, stats(inserts/enq/pop/subproofs), max committed depth.
Adds per-problem 'deriv' dict and per-battery 'deriv_totals'.
Usage: python3 enrich_deriv.py <results_formal_quot.json> <out_dir>
"""
import json, re, sys, os

res_path, out_dir = sys.argv[1], sys.argv[2]
R = json.load(open(res_path))

for bname, batt in R.items():
    if not isinstance(batt, dict) or "problems" not in batt:
        continue
    tot = {"inserts": 0, "enq": 0, "pop": 0, "subproofs": 0,
           "committed": 0, "conflicts": 0, "ok_problems": 0}
    for pid, p in batt["problems"].items():
        if p.get("status") != "ok":
            continue
        fp = os.path.join(out_dir, f"{bname}_QUOT_{pid}.r0")
        deriv = {}
        try:
            txt = open(fp).read()
        except OSError:
            txt = ""
        m = re.search(r"committed:\s*(\d+)", txt)
        deriv["committed"] = int(m.group(1)) if m else None
        m = re.search(r"conflicts:\s*(\d+)", txt)
        deriv["conflicts"] = int(m.group(1)) if m else None
        m = re.search(r"stats:\s*inserts=(\d+)\s+enq=(\d+)\s+pop=(\d+)\s+subproofs=(\d+)", txt)
        if m:
            deriv["inserts"] = int(m.group(1)); deriv["enq"] = int(m.group(2))
            deriv["pop"] = int(m.group(3)); deriv["subproofs"] = int(m.group(4))
        else:
            deriv["inserts"] = deriv["enq"] = deriv["pop"] = deriv["subproofs"] = None
        depths = [int(x) for x in re.findall(r"depth=(\d+)", txt)]
        deriv["max_depth"] = max(depths) if depths else None
        p["deriv"] = deriv
        tot["ok_problems"] += 1
        for k in ("inserts", "enq", "pop", "subproofs", "committed", "conflicts"):
            if deriv.get(k) is not None:
                tot[k] += deriv[k]
    batt["deriv_totals"] = tot

json.dump(R, open(res_path, "w"), indent=1)
print("enriched", res_path)
for bname, batt in R.items():
    if isinstance(batt, dict) and "deriv_totals" in batt:
        t = batt["deriv_totals"]
        print(f"  {bname}: ok={t['ok_problems']} committed={t['committed']} "
              f"inserts={t['inserts']} enq={t['enq']} pop={t['pop']} "
              f"subproofs={t['subproofs']} conflicts={t['conflicts']}")
