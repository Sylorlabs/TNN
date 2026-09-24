#!/usr/bin/env python3
"""Re-run one stream for given forks, 2x fresh, byte-identity check."""
import os, sys, shutil, subprocess, filecmp

HERE = os.path.dirname(os.path.abspath(__file__))
BAT = os.path.join(HERE, "..", "battery")
EVID = os.path.join(HERE, "evidence")
BINS = {"k": "build_k/bin_k", "l": "build_l/bin_l",
        "s": "build_s/bin_s", "sp": "build_sp/bin_sp"}

def main():
    stream, forks = sys.argv[1], sys.argv[2].split(",")
    sp = os.path.abspath(os.path.join(HERE, "streams", stream + ".txt"))
    for fork in forks:
        bbin = os.path.join(BAT, BINS[fork])
        leds = []
        for run in ("a", "b"):
            rdir = os.path.join(EVID, "runs_%s_%s_%s" % (fork, stream, run))
            if os.path.exists(rdir):
                shutil.rmtree(rdir)
            os.makedirs(rdir)
            lp = os.path.join(rdir, stream + ".ledger")
            cp = os.path.join(rdir, stream + ".cost")
            r = subprocess.run([bbin, sp, lp, cp, fork],
                               capture_output=True, text=True)
            if r.returncode != 0:
                print("RUN FAILED", fork, stream, run)
                print(r.stdout[-2000:]); print(r.stderr[-2000:])
                sys.exit(1)
            leds.append(lp)
        same = filecmp.cmp(leds[0], leds[1], shallow=False)
        print("fork=%s stream=%s byte-identical=%s" % (fork, stream, same))
        assert same

if __name__ == "__main__":
    main()
