#!/usr/bin/env python3
"""score.py -- R2-14 battery scorer.

Usage: score.py <ledger> <listfile>
The ledger and listfile have one line per fixture in the same order.
Truth comes from <fixture-path>.truth.

Reports (as JSON to stdout):
  n, installs, false_installs, false_install_rate,
  per_family {fam: [false, total, rate]},
  recall (installs with judgment==truth, for control batteries),
  highconf: {wrong, flagged, rate} for conf>=700 and judgment!=truth.
"""
import json, sys, struct

def hdr_fam(path):
    d = open(path, "rb").read(32)
    return struct.unpack("<8I", d)[3]

def get_truth(p):
    t = open(p + ".truth").read().strip()
    if t.startswith("truth="):
        t = t[len("truth="):]
    return t.strip()

def parse_ledger(path):
    rows = []
    for line in open(path):
        p = dict(kv.split("=", 1) for kv in line.strip().split(" ")
                 if "=" in kv and not kv.startswith("hash="))
        rows.append(p)
    return rows

def main():
    ledger, listfile = sys.argv[1], sys.argv[2]
    rows = parse_ledger(ledger)
    paths = [l.rstrip("\n") for l in open(listfile)]
    assert len(rows) == len(paths), (len(rows), len(paths))
    fams = {}
    tasks = {}
    taskfams = {}
    n = fi = inst = rec = 0
    hc_wrong = hc_flag = 0
    for p, fx in zip(paths, rows):
        truth = get_truth(p)
        fam = hdr_fam(p)
        task = fx.get("task", "?")
        judg, disp, conf = fx["judgment"], fx["disp"], int(fx["conf"])
        n += 1
        f = fams.setdefault(fam, [0, 0])
        f[1] += 1
        t = tasks.setdefault(task, [0, 0])
        t[1] += 1
        tf = taskfams.setdefault("%s/f%d" % (task, fam), [0, 0])
        tf[1] += 1
        wrong = (judg != truth)
        if disp == "INSTALL":
            inst += 1
            if wrong:
                fi += 1
                f[0] += 1
                t[0] += 1
                tf[0] += 1
            else:
                rec += 1
        if conf >= 700 and wrong:
            hc_wrong += 1
            if disp != "INSTALL":
                hc_flag += 1
    def rates(d):
        return {k: [v[0], v[1], v[0] / v[1] if v[1] else 0]
                for k, v in sorted(d.items())}
    out = {
        "n": n,
        "installs": inst,
        "false_installs": fi,
        "false_install_rate": fi / n if n else 0,
        "recall": rec / n if n else 0,
        "per_family": rates(fams),
        "per_task": rates(tasks),
        "per_task_family": rates(taskfams),
        "highconf": {"wrong": hc_wrong, "flagged": hc_flag,
                     "rate": hc_flag / hc_wrong if hc_wrong else 1.0},
    }
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
