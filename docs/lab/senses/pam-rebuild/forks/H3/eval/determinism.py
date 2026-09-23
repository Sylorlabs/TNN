#!/usr/bin/env python3
"""B6 determinism: 60 fixtures (10/task primary), 3 runs each. Byte-identical
stdout and ledger hashes. Also verifies ledger by independent recompute.
Usage: determinism.py <outdir>
"""
import subprocess, glob, os, re, json, sys, hashlib

H3 = os.path.expanduser("~/workspace/h3work/build/sense_h3")
FX = os.path.expanduser("~/workspace/tnn-lab/senses/rebuild/harness/fixtures")
TASKS = [
    ("colordisc", "t1_colordisc", ".img"),
    ("colorconst", "t2_colorconst", ".img"),
    ("shapetrans", "t3_shapetrans", ".img"),
    ("pitchdisc", "t4_pitchdisc", ".pcm"),
    ("timbredisc", "t5_timbredisc", ".pcm"),
    ("motiondir", "t6_motiondir", ".vid"),
]

def main():
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    fixtures = []
    for task, tdir, ext in TASKS:
        fs = sorted(glob.glob(os.path.join(FX, tdir, "primary", "*" + ext)))[:10]
        for f in fs:
            fixtures.append((task, f))
    print("fixtures:", len(fixtures), flush=True)
    # 3 runs
    runs = []
    for ri in range(3):
        rr = []
        for task, fx in fixtures:
            out = subprocess.run([H3, task, fx], capture_output=True, text=True).stdout
            rr.append(out)
        runs.append(rr)
        print("run %d done" % ri, flush=True)
    # byte-identity
    ok = True
    for i in range(len(fixtures)):
        if not (runs[0][i] == runs[1][i] == runs[2][i]):
            ok = False
            print("MISMATCH:", fixtures[i])
    print("byte-identical:", ok, flush=True)
    # ledger: single-mode uses prev=zeros for each; verify independent recompute
    lok = True
    for i, (task, fx) in enumerate(fixtures):
        d = dict(l.split("=", 1) for l in runs[0][i].strip().split("\n") if "=" in l)
        tr = d.get("transition", "").encode()
        ch = d.get("chain", "")
        exp = hashlib.sha256(bytes(32) + tr).hexdigest()
        if exp != ch:
            lok = False
            print("LEDGER MISMATCH:", fx, exp, ch)
    print("ledger recompute ok:", lok, flush=True)
    with open(os.path.join(outdir, "b6.json"), "w") as f:
        json.dump({"byte_identical": ok, "ledger_ok": lok, "n": len(fixtures)}, f)
    # save run0 for the record
    with open(os.path.join(outdir, "b6_run0.txt"), "w") as f:
        for (task, fx), out in zip(fixtures, runs[0]):
            f.write("### %s %s\n%s" % (task, fx, out))

if __name__ == "__main__":
    main()
