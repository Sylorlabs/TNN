#!/usr/bin/env python3
"""B-gamma render + verify driver.
1. Renders all four pieces, 3x each, checks byte-identical SHA-256 (K0).
2. Runs A-NATIVE checks (native_check.py) on each deliverable.
3. Runs the no-copy audit (audit.py) on kids.
"""
import hashlib, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "gamma_bin")
OUT = os.path.join(HERE, "render")
PACK = os.path.join(HERE, "study_out", "gamma.grpk")
NATIVE = os.path.join(HERE, "..", "native_check.py")

SUBJECTS = ["kids", "planet", "ocean", "monster"]

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def main():
    os.makedirs(OUT, exist_ok=True)
    assert os.path.exists(PACK), "no grain pack -- run study.py first"
    ok = True
    for s in SUBJECTS:
        paths = []
        for r in range(3):
            p = os.path.join(OUT, f"b_gamma_{s}_r{r}.wav")
            subprocess.run([BIN, s, PACK, p], check=True)
            paths.append(p)
        shas = [sha(p) for p in paths]
        det = shas[0] == shas[1] == shas[2]
        print(f"{s}: sha={shas[0][:16]}... 3/3 byte-identical: {det}")
        if not det:
            ok = False
        # keep r0 as the deliverable
        os.replace(paths[0], os.path.join(OUT, f"b_gamma_{s}.wav"))
        for p in paths[1:]:
            os.remove(p)
    print("--- A-NATIVE ---")
    for s in SUBJECTS:
        p = os.path.join(OUT, f"b_gamma_{s}.wav")
        r = subprocess.run(["python3", NATIVE, p], capture_output=True, text=True)
        tail = r.stdout.strip().splitlines()[-4:] if r.stdout.strip() else [r.stderr.strip()[-200:]]
        print(f"== {s}: rc={r.returncode}")
        for ln in tail:
            print("   " + ln)
        if r.returncode != 0:
            print(f"   NATIVE CHECK FAILED for {s}")
            ok = False
    print("--- no-copy audit (kids) ---")
    r = subprocess.run(["python3", os.path.join(HERE, "audit.py"),
                        os.path.join(OUT, "b_gamma_kids.wav")],
                       capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr[-500:])
        print("AUDIT FAILED")
        ok = False
    print("OVERALL:", "OK" if ok else "FAILURE")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
