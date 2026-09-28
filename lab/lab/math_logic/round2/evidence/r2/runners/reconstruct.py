#!/usr/bin/env python3
"""Reconstruct results_formal.json from .out.r0 files (runner overwrote JSON)."""
import os, re, json, hashlib, glob

EV = "/home/hatch/workspace/math_r2/eval"
OUT = f"{EV}/out"
R1 = "/home/hatch/workspace/math_r2/r1/problems"
BASE = "/home/hatch/workspace/tnn-lab/math_logic"

def sealed(path):
    d = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): continue
            pid, v = line.split(":")
            d[pid.strip()] = v.strip()
    return d

SEAL = {
    "B2R": sealed(f"{BASE}/problems/sealed/SEALED_B2.sol"),
    "B3R": sealed(f"{BASE}/problems/sealed/SEALED_B3.sol"),
    "B4R": sealed(f"{BASE}/problems/sealed/SEALED_B4.sol"),
    "B4X": sealed(f"{BASE}/round2/batteries/sealed/SEALED_B4X.sol"),
    "B6X": sealed(f"{BASE}/round2/batteries/sealed/SEALED_B6X.sol"),
}
SEAL["B2R"]["B2_07"] = "WITHHELD"  # F-SEAL-01

def vclass(v):
    if v in ("DERIVED", "DERIVED-WEIGHED"): return "derived"
    if v in ("REFUTED", "REFUTED-WEIGHED"): return "refuted"
    return "withheld"

def parse_out(path):
    with open(path, "rb") as f: data = f.read()
    txt = data.decode("utf-8", errors="replace")
    v = re.search(r"^VERDICT:\s*(\S+)", txt, re.M)
    c = re.search(r"^CONFIDENCE:\s*(\S+)", txt, re.M)
    d = re.search(r"^DERIVATIONS:\s*(\S+)", txt, re.M)
    # extract AUDIT section
    am = re.search(r"^AUDIT:\n(.*)", txt, re.M | re.S)
    audit = am.group(1).strip() if am else ""
    return (v.group(1) if v else "NO_VERDICT",
            c.group(1) if c else "?", d.group(1) if d else "?",
            hashlib.sha256(data).hexdigest(), audit)

results = {}
for bname in ["B2R", "B3R", "B4R", "B4X", "B6X"]:
    results[bname] = {}
    # find engines from files
    files = glob.glob(f"{OUT}/{bname}_*_.r0")  # not quite; use pattern
    # pattern: {bname}_{ename}_{pid}.r0, but ename may contain hyphens
    import re as re2
    seen = set()
    for fp in glob.glob(f"{OUT}/{bname}_*.r0"):
        bn = os.path.basename(fp)
        # strip bname_ prefix and .r0
        rest = bn[len(bname)+1:-3]
        # rest = {ename}_{pid}; pid is like B2_01, B4X_10, etc.
        m = re2.match(r"(.+)_(B\d+[A-Z]*_\d+|B\d+X_\d+)$", rest)
        if not m: continue
        ename, pid = m.group(1), m.group(2)
        seen.add((ename, pid))
    for ename, pid in sorted(seen):
        # check 3x byte-identical (normalize LEARN-FORM path if needed)
        shas = []
        for r_ in range(3):
            fp = f"{OUT}/{bname}_{ename}_{pid}.r{r_}"
            if not os.path.exists(fp): break
            with open(fp, "rb") as f: shas.append(hashlib.sha256(f.read()).hexdigest())
        erec = results[bname].setdefault(ename, {"problems": {}, "divergent": []})
        if len(shas) < 3:
            erec["problems"][pid] = {"status": "MISSING_RUNS"}
            continue
        # for formal engines, raw byte compare is fine (no path echo)
        if not (shas[0] == shas[1] == shas[2]):
            erec["divergent"].append(pid)
            erec["problems"][pid] = {"status": "DIVERGENT"}
            continue
        v, c, d, sha, audit = parse_out(f"{OUT}/{bname}_{ename}_{pid}.r0")
        vc = vclass(v)
        sv = SEAL[bname].get(pid, "?")
        svc = vclass(sv)
        solved = (vc == "derived" and svc == "derived") or (vc == "withheld" and svc == "withheld")
        erec["problems"][pid] = {
            "status": "ok", "verdict": v, "vclass": vc, "sealed": sv,
            "solved": solved, "incorrect": not solved,
            "confidence": c, "derivations": d, "sha": sha, "audit": audit,
        }
    for ename in results[bname]:
        erec = results[bname][ename]
        ps = [p for p in erec["problems"].values() if p.get("status") == "ok"]
        erec["agg"] = {
            "n": len(ps),
            "solved": sum(1 for p in ps if p["solved"]),
            "incorrect": sum(1 for p in ps if p["incorrect"]),
            "divergent": len(erec["divergent"]),
        }

with open(f"{EV}/results_formal_all.json", "w") as f:
    json.dump(results, f, indent=1)
print("reconstructed:", {b: {e: results[b][e]["agg"] for e in results[b]} for b in results})
