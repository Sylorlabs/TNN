#!/usr/bin/env python3
"""score_v2.py — compile the full v2 trial, run each leg N=5, verify.

Usage: score_v2.py <n_runs=5>
Writes run logs to ~/workspace/senses-v2/runs/<stamp>/.
Exits 0 only if every leg passes all bars on every run and all runs are
byte-identical per leg.
"""
import hashlib
import os
import subprocess
import sys
import time

W = os.path.expanduser("~/workspace/senses-v2")
SRC = os.path.join(W, "src")
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
LEGS = ["A", "B", "C", "D", "M", "R", "S"]

BARS = {"A2": (20, 20), "B2": (6, 6), "C2": (9, 12), "D2": (11, 12),
        "M2": (24, 24), "R2": (24, 24), "S2": (4, 4)}


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return r


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    stamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    rundir = os.path.join(W, "runs", stamp)
    os.makedirs(rundir, exist_ok=True)

    # 1. generate cases from live envelopes
    print("== generate ==")
    r = run([sys.executable, os.path.join(W, "gen_v2.py")])
    print(r.stdout[-500:] if r.stdout else "", r.stderr[-500:] if r.stderr else "")
    if r.returncode != 0:
        sys.exit("gen_v2.py failed")

    # 2. compile
    print("== compile ==")
    r = run([ZNC, "ws2_trial.zag", "-o", "ws2_trial"], cwd=SRC)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        sys.exit("znc build failed")
    print("build ok")

    # 3. run each leg n times
    ok = True
    hashes = {}
    for leg in LEGS:
        outs = []
        for i in range(n):
            r = run([os.path.join(SRC, "ws2_trial"), leg], cwd=SRC)
            log = os.path.join(rundir, f"leg{leg}_run{i+1}.txt")
            open(log, "w").write(r.stdout)
            outs.append(r.stdout)
            if r.returncode != 0:
                print(f"leg {leg} run {i+1}: EXIT {r.returncode}")
                print(r.stdout[-2000:])
                ok = False
        h = {hashlib.sha256(o.encode()).hexdigest() for o in outs}
        hashes[leg] = sorted(h)
        det = "PASS" if len(h) == 1 else "FAIL"
        print(f"leg {leg}: determinism {len(h)} distinct hash(es) -> {det}")
        if len(h) != 1:
            ok = False
        # bar check from the first run
        import re
        m = re.search(r"VERDICT\|(\w+)\|(PASS|FAIL)", outs[0])
        need, of = BARS[{"A": "A2", "B": "B2", "C": "C2", "D": "D2",
                         "M": "M2", "R": "R2", "S": "S2"}[leg]]
        verdict = m.group(2) if m else "MISSING"
        print(f"leg {leg}: verdict {verdict} (bar {need}/{of})")
        if verdict != "PASS":
            ok = False

    # 4. independent verification: concatenate one M run + one R run, then verify
    # (the audit checks span both legs; per-leg determinism already done above)
    print("== verify_v2 ==")
    mr = os.path.join(rundir, "legMR_run1.txt")
    with open(mr, "w") as f:
        f.write(open(os.path.join(rundir, "legM_run1.txt")).read())
        f.write(open(os.path.join(rundir, "legR_run1.txt")).read())
    r = run([sys.executable, os.path.join(W, "verify_v2.py"), mr])
    print(r.stdout)
    if r.returncode != 0:
        ok = False

    # 5. hash manifest
    man = os.path.join(rundir, "hash_manifest.txt")
    with open(man, "w") as f:
        for leg in LEGS:
            f.write(f"{leg}: {hashes[leg][0]}\n")
    print("manifest:", man)
    print("OVERALL:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
