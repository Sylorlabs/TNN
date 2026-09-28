#!/usr/bin/env python3
"""Retention: re-run 10 stage binaries on original contract tests, byte-compare."""
import subprocess, os, sys, re, json

WORKDIR = os.path.expanduser("~/workspace/lh_trial")
RESULTS = os.path.join(WORKDIR, "results")
# 10 stages per prereg: A1, A5, A10, B3, B8, C2, C6, C8, plus 2 (A8, B6)
STAGES = ["A1", "A5", "A10", "B3", "B8", "C2", "C6", "C8", "A8", "B6"]

def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout

def main():
    # Load original metrics to get accepted outputs (we re-run and compare to contract)
    ok_all = True
    for stage in STAGES:
        binp = os.path.join(RESULTS, f"{stage}_bin")
        contract = open(os.path.join(WORKDIR, "contracts", f"{stage}.txt")).read()
        # Get spec to know if AGG/SORT
        # (we'll infer from stage: A8, B6, C7 are AGG; A9, B7, C8 are SORT)
        is_multi = stage in ("A8", "B6", "C7", "A9", "B7", "C8")
        tests = re.findall(r'TEST in="(.*)" out="(.*)"', contract)
        stage_ok = True
        for tin, tout in tests:
            if is_multi:
                recs = tin.split(";")
                cmd = [binp, str(len(recs))] + recs
            else:
                cmd = [binp, tin]
            rc, rout = run(cmd)
            rout_norm = rout.strip().replace("\n", ";")
            if rout_norm != tout:
                print(f"{stage}: MISMATCH got=[{rout_norm}] want=[{tout}]")
                stage_ok = False
                ok_all = False
        print(f"{stage}: {'PASS' if stage_ok else 'FAIL'} ({len(tests)} tests)")
    print("RETENTION:", "PASS (10/10 byte-identical)" if ok_all else "FAIL")
    return 0 if ok_all else 1

if __name__ == "__main__":
    sys.exit(main())
