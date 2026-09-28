#!/usr/bin/env python3
"""FE2 build self-check: compare fe2.zag predictions to audit_fe1.py predictions
on the frozen FE1 fixtures (indices 0..23). Prereg allows 0..23 as build self-checks.
NOT the verdict: verdict uses fresh held-out indices 24..47."""
import sys, os, subprocess, re

FE1 = os.path.expanduser("~/workspace/pam_round2/fe1_audit")
FE2 = os.path.expanduser("~/workspace/pam_round2/fe2_port/build/fe2")
DATA = os.path.join(FE1, "data")

# load audit_fe1 SEPS without running main (stub argv)
src = open(os.path.join(FE1, "audit_fe1.py")).read()
src = src.replace("DATA = sys.argv[1]", "DATA = ''").replace("OUT = sys.argv[2]", "OUT = ''")
g = {"__name__": "auditmod", "sys": sys, "os": os}
exec(compile(src, "audit_fe1.py", "exec"), g)
SEPS = g["SEPS"]
EXT = g["EXT"]

FAMS = ["PTC-4","PTC-5","TMB-4","TMB-5","COL-4","CCN-3","CCN-4","SHP-4","SHP-5","MOT-4","MOT-5"]

total_mismatch = 0
for fam in FAMS:
    ext = EXT[fam]
    paths = [os.path.join(DATA, f"rt3_{fam}_{i:04d}.{ext}") for i in range(24)]
    # audit predictions
    audit_preds = []
    for p in paths:
        pred, detail = SEPS[fam](p)
        audit_preds.append(pred)
    # fe2 predictions (one invocation)
    out = subprocess.run([FE2, fam] + paths, capture_output=True, text=True)
    if out.returncode != 0:
        print(f"{fam}: fe2 EXITED rc={out.returncode}: {out.stderr[:200]}")
        total_mismatch += 24
        continue
    fe2_preds = []
    for line in out.stdout.strip().split("\n"):
        m = re.search(r"prediction=([A-Z_]+)", line)
        fe2_preds.append(m.group(1) if m else "PARSE_FAIL")
    mm = [(i, a, b) for i, (a, b) in enumerate(zip(audit_preds, fe2_preds)) if a != b]
    total_mismatch += len(mm)
    print(f"{fam}: {24-len(mm)}/24 match" + ("" if not mm else f"  MISMATCH idx: {[(i,a,b) for i,a,b in mm[:6]]}"))
print("TOTAL MISMATCHES:", total_mismatch)
