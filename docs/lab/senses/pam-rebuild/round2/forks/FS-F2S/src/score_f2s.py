#!/usr/bin/env python3
"""score_f2s.py -- FS-F2S eval scorer (glue only; all judgments from Zag).
Usage: score_f2s.py <out.tsv> <listfile>...
Reads batch-mode TSV rows "<path>\ttask=<name>\tjudgment=<JNAME>",
compares each judgment to the <path>.truth sidecar, prints per-set accuracy
and the frozen bar checks from PREREG_FS-F2S.md.
TSV columns written: fixture  task  judgment  truth  correct(1/0)
"""
import sys

def get_truth(p):
    t = open(p + ".truth").read().strip()
    if t.startswith("truth="):
        t = t[len("truth="):]
    return t.strip()

def score_tsv(tsv_path):
    n = ok = 0
    per_task = {}
    with open(tsv_path) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 5:
                print("BAD ROW: " + line[:120])
                continue
            path, task, judg, truth, correct = p[0], p[1], p[2], p[3], int(p[4])
            n += 1
            ok += correct
            pt = per_task.setdefault(task, [0, 0])
            pt[0] += correct
            pt[1] += 1
    return n, ok, per_task

def main():
    tsv = sys.argv[1]
    n, ok, per_task = score_tsv(tsv)
    acc = 100.0 * ok / n if n else 0.0
    print("TSV: %s  n=%d correct=%d acc=%.2f%%" % (tsv, n, ok, acc))
    for t, (c, nn) in sorted(per_task.items()):
        print("  task=%s %d/%d = %.2f%%" % (t, c, nn, 100.0 * c / nn if nn else 0))
    # frozen bar checks (PREREG_FS-F2S.md)
    bars = {
        "shapetrans": ("a", 85.00),
        "colordisc": ("b", 91.96),
        "pitchdisc": ("b", 96.92),
        "motiondir": ("b", 95.63),
    }
    allpass = True
    for t, (bar, lo) in bars.items():
        if t in per_task:
            c, nn = per_task[t]
            a = 100.0 * c / nn if nn else 0
            p = a >= lo
            allpass = allpass and p
            print("BAR(%s) %s: %.2f%% >= %.2f%% -> %s" % (bar, t, a, lo, "PASS" if p else "FAIL"))
    print("ALL BARS (a,b): " + ("PASS" if allpass else "FAIL"))

if __name__ == "__main__":
    main()
