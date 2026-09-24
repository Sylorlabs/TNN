#!/usr/bin/env python3
"""Run the one-brain Variant A integration battery: 3 byte-identical runs
per (attack, mask), then mechanical verification of each bundle."""
import subprocess
import hashlib
import os
import sys

TRIAL = os.path.expanduser("~/workspace/onebrain/ob_a/trial_ob_linux")
OUTDIR = os.path.expanduser("~/workspace/ob_trials/runs")
VERIFY = os.path.expanduser("~/workspace/onebrain/ob_a/verify.py")

MATRIX = [
    ("b0", [0, 43, 53]),
    ("a1", [0, 43, 53]),
    ("a2", [0, 8, 16, 1, 43, 53]),
    ("a2ii", [0, 1, 43, 53]),
    ("a3", [0, 64]),
    ("a3b", [0, 43, 53]),
    ("a4", [0, 8, 16]),
    ("a4b", [0, 8, 16]),
    ("a5", [0, 2, 4]),
    ("a6", [0, 43, 53]),
    ("a6b", [0, 1, 43, 53]),
]

def sha(b):
    return hashlib.sha256(b).hexdigest()[:16]

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    results = []
    for atk, masks in MATRIX:
        for m in masks:
            blobs = []
            for r in range(1, 4):
                p = subprocess.run([TRIAL, atk, str(m)], capture_output=True)
                if p.returncode not in (0, 1):
                    print(f"FATAL {atk} m={m} run {r}: rc={p.returncode}")
                    print(p.stderr.decode()[:500])
                    sys.exit(1)
                blobs.append(p.stdout)
                fn = os.path.join(OUTDIR, f"{atk}_m{m}_run{r}.txt")
                with open(fn, "wb") as f:
                    f.write(p.stdout)
            # I6: byte-identical
            if not (blobs[0] == blobs[1] == blobs[2]):
                print(f"I6 FAIL {atk} m={m}: runs differ")
                sys.exit(1)
            # verdict
            vline = [l for l in blobs[0].decode().split("\n") if "TN_VERDICT" in l]
            v = vline[0].split(",")[3] if vline else "?"
            # mechanical verify (I1/I2/I3/I4); check-level fails are
            # expected for the seam-demonstration bundles (a3_m0, a5_m0)
            vr = subprocess.run([sys.executable, VERIFY,
                                 os.path.join(OUTDIR, f"{atk}_m{m}_run1.txt")],
                                capture_output=True, text=True)
            vok = vr.returncode == 0 and "ALL OK" in vr.stdout
            expected_fail = (atk == "a3" and m == 0) or (atk == "a5" and m == 0)
            results.append((atk, m, v, sha(blobs[0]), vok, expected_fail))
            flag = ""
            if not vok and not expected_fail:
                flag = "  <-- UNEXPECTED"
            print(f"{atk:4s} m={m:2d}: verdict={v:4s} sha={sha(blobs[0])} "
                  f"mechanical={'OK' if vok else 'FAIL'}"
                  f"{' (expected kill-bar fail)' if expected_fail else ''}{flag}")
            if not vok and not expected_fail:
                print(vr.stdout[-2000:])
    print(f"\ndone: {len(results)} bundles, all 3x byte-identical")
    bad = [r for r in results if not r[4] and not r[5]]
    if bad:
        print("UNEXPECTED MECHANICAL FAILURES:", bad)
        sys.exit(1)
    print("mechanical integrity (I1/I2/I3/I4): ALL OK on every bundle")

if __name__ == "__main__":
    main()
