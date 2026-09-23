#!/usr/bin/env python3
"""run_battery.py — R2-13 FS-F battery runner (deterministic glue).

Runs the fsf binary over the frozen exact-10,000 fixture manifest
(manifest_10000.json, A2) in manifest order, threading the hash chain:
each trial's prevchain = previous trial's chain (GENESIS for the first).
Writes the ledger to <out>.

Usage: run_battery.py <binary> <mode> <fixtures_R2A_dir> <out_ledger>
"""
import os, subprocess, sys, time

BIN, MODE, FX, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
LEDGER = os.path.join(OUT, "LEDGER_%s.txt" % MODE)
os.makedirs(OUT, exist_ok=True)
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]

def fixtures():
    # FS-F A2: frozen exact-10,000 manifest (manifest_10000.json), deterministic order.
    # Supersedes the full 10,425-ledger walk (A1) and the 9,925 pool (original prereg).
    import json
    mf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "manifest_10000.json")
    out = []
    with open(mf) as f:
        man = json.load(f)
    assert len(man) == 10000, "manifest must list exactly 10000 fixtures"
    for e in man:
        p = os.path.join(FX, e["path"])
        out.append(p)
    return out

def main():
    fxs = fixtures()
    print("fixtures:", len(fxs), flush=True)
    prev = "GENESIS"
    n_err = 0
    t0 = time.time()
    with open(LEDGER, "w") as led:
        for i, fx in enumerate(fxs):
            bn = os.path.basename(fx)
            task = bn.split("_")[1]
            r = subprocess.run([BIN, fx, task, fx + ".truth", prev, MODE],
                               capture_output=True, text=True, timeout=180)
            rec = r.stdout
            if "chain=" not in rec:
                n_err += 1
                rec = ("approach=R2-13\nmode=%s\ntask=%s\nerror=no-chain rc=%d\nchain=%s\n"
                       % (MODE, task, r.returncode, prev))
            for line in rec.splitlines():
                if line.startswith("chain="):
                    prev = line[6:].strip()
                    break
            led.write(rec)
            if not rec.endswith("\n"):
                led.write("\n")
            if (i + 1) % 1000 == 0:
                print("  ...", i + 1, "elapsed %.0fs" % (time.time() - t0), flush=True)
    print("done. errors:", n_err, "final chain:", prev, "elapsed %.0fs" % (time.time() - t0), flush=True)

main()
