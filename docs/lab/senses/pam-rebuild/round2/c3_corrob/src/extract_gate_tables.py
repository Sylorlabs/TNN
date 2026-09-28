#!/usr/bin/env python3
"""Extract thr_of (deliberate.zag) and tol_of (memgate.zag) by script."""
import re, json, os

def extract(path, fname):
    src = open(path).read()
    i = src.find("fn " + fname)
    j = src.find("}", src.find("return", i))
    # find the closing brace of the function: first "\n}" after i
    k = src.find("\n}", i)
    body = src[i:k]
    vals = {}
    for m in re.finditer(r"if\(tc == (\d+)\) \{ return (\d+); \}", body):
        vals[int(m.group(1))] = int(m.group(2))
    m2 = re.search(r"\n    return (\d+);", body)
    if m2:
        vals["default"] = int(m2.group(1))
    return vals

base = os.path.expanduser("~")
thr = extract(base + "/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-4/src/deliberate.zag", "thr_of")
tol = extract(base + "/workspace/pam_round2/o1_delivery/memgate.zag", "tol_of")
# tol_of has no default; tc=5 falls through to `return 0`
tol_src = open(base + "/workspace/pam_round2/o1_delivery/memgate.zag").read()
i = tol_src.find("fn tol_of")
k = tol_src.find("\n}", i)
print("tol_of body:", repr(tol_src[i:k+2]))

out = {"thr_of": thr, "tol_of": tol,
       "tcode_names": ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gate_tables.json"), "w"), indent=2)
print(json.dumps(out, indent=2))
assert thr == {0: 400, 1: 50, 2: 60, 3: 1500, 4: 80, "default": 2}, thr
assert tol[0] == 8 and tol[4] == 120, tol
print("OK")
