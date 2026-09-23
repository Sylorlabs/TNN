#!/usr/bin/env python3
"""Score the R2-9 10k battery: B1 accuracy, B5 false installs, ops.
Reads batch percepts.tsv (fixture paths lab-relative, truth from .truth).
Pure analysis glue.
Usage: score_10k.py <percepts.tsv>   (cwd must be ~/workspace/tnn-lab)
"""
import os, sys

LAB = os.getcwd()

def truth_for(fx):
    with open(os.path.join(LAB, fx + ".truth")) as f:
        return f.read().strip().split("=", 1)[1].strip()

def main():
    p = sys.argv[1]
    n = ok = n_inst = n_false = 0
    ops = 0
    per = {}
    with open(p) as f:
        f.readline()
        for line in f:
            q = line.rstrip("\n").split("\t")
            if len(q) < 12:
                continue
            task, fx, judg, disp = q[1], q[2], q[3], q[5]
            truth = truth_for(fx)
            n += 1
            st = per.setdefault(task, {"n": 0, "ok": 0, "inst": 0, "false": 0})
            st["n"] += 1
            if judg == truth:
                ok += 1
                st["ok"] += 1
            if disp == "INSTALL":
                n_inst += 1
                st["inst"] += 1
                if judg != truth:
                    n_false += 1
                    st["false"] += 1
            ops += int(q[6])
    print(f"trials={n} accuracy={ok}/{n}={ok/n:.4f}")
    print(f"B5 false installs: {n_false}/{n}={n_false/n:.4f} (bar <= 0.03) -> {'PASS' if n_false/n <= 0.03 else 'FAIL'}")
    print(f"installs={n_inst} ({n_inst/n:.3f} of trials), total ops={ops}")
    for t in sorted(per):
        s = per[t]
        print(f"  {t}: acc={s['ok']}/{s['n']}={s['ok']/s['n']:.4f} installs={s['inst']} false={s['false']}")

if __name__ == "__main__":
    main()
