#!/usr/bin/env python3
"""Run the full ST battery for a fork twice from fresh directories.

Usage: run_battery.py <fork> <streams_dir>

For run in (a, b): fresh dir runs_<fork>_<run>/; for each battery BAT:
    bin_<fork> <streams>/<BAT>.txt <BAT>.ledger <BAT>.cost <fork>
After both runs: cmp every ledger pair; report byte-identity.
Ledgers must be byte-identical (determinism); cost files are excluded
(timing side channel, nondeterministic by design).
"""
import sys, os, shutil, subprocess, filecmp

HERE = os.path.dirname(os.path.abspath(__file__))
BATS = ["ST-1", "ST-1N", "ST-2", "ST-3", "ST-3P", "ST-4", "ST-5",
        "ST-6", "CALIB", "RT-T1", "RT-T2", "RT-T3", "RT-T4"]

def run_all(fork, sdir):
    bbin = os.path.join(HERE, "build_%s" % fork, "bin_%s" % fork)
    assert os.path.exists(bbin), "missing binary for " + fork
    for run in ("a", "b"):
        rdir = os.path.join(HERE, "runs_%s_%s" % (fork, run))
        if os.path.exists(rdir):
            shutil.rmtree(rdir)
        os.makedirs(rdir)
        for bat in BATS:
            sp = os.path.abspath(os.path.join(sdir, bat + ".txt"))
            lp = os.path.join(rdir, bat + ".ledger")
            cp = os.path.join(rdir, bat + ".cost")
            r = subprocess.run([bbin, sp, lp, cp, fork],
                               capture_output=True, text=True)
            if r.returncode != 0:
                print("RUN FAILED fork=%s bat=%s run=%s" % (fork, bat, run))
                print(r.stdout[-2000:])
                print(r.stderr[-2000:], file=sys.stderr)
                sys.exit(1)
        print("fork=%s run=%s complete" % (fork, run))
    # byte-identity check on ledgers
    ok = True
    for bat in BATS:
        a = os.path.join(HERE, "runs_%s_a" % fork, bat + ".ledger")
        b = os.path.join(HERE, "runs_%s_b" % fork, bat + ".ledger")
        same = filecmp.cmp(a, b, shallow=False)
        print("ledger %s byte-identical: %s" % (bat, same))
        ok = ok and same
    print("FORK %s BYTE-IDENTICAL: %s" % (fork, ok))
    if not ok:
        sys.exit(1)

if __name__ == "__main__":
    run_all(sys.argv[1], sys.argv[2])
