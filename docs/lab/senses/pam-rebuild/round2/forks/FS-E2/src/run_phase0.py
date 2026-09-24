#!/usr/bin/env python3
"""run_phase0.py -- FS-E2 Phase 0 driver (glue only; all decisions in Zag).
Runs the independent fs2_form binary in batch mode over a fixture list,
compares each formation judgment against the .truth sidecar.
Usage: run_phase0.py <fs2_form> <listfile> <out.tsv>
TSV columns: fixture  task  judgment  truth  correct(1/0)
"""
import subprocess, sys

def get_truth(p):
    t = open(p + ".truth").read().strip()
    if t.startswith("truth="):
        t = t[len("truth="):]
    return t.strip()

def main():
    binary, listfile, out = sys.argv[1], sys.argv[2], sys.argv[3]
    paths = [l.rstrip("\n") for l in open(listfile) if l.strip()]
    r = subprocess.run([binary, "batch", listfile], capture_output=True,
                       text=True, timeout=3600)
    if r.returncode != 0:
        print("BINARY FAILED rc=%d" % r.returncode)
        print(r.stderr[-2000:])
        sys.exit(1)
    rows = {}
    for line in r.stdout.split("\n"):
        line = line.strip()
        if not line or line.startswith("error="):
            print("WARN: " + line[:120])
            continue
        parts = line.split("\t")
        kv = dict(k.split("=", 1) for k in parts[1:] if "=" in k)
        rows[parts[0]] = (kv.get("task", "?"), kv.get("judgment", "?"))
    n = 0
    with open(out, "w") as fh:
        for p in paths:
            task, judg = rows.get(p, ("?", "?"))
            truth = get_truth(p)
            correct = 1 if judg == truth else 0
            fh.write("%s\t%s\t%s\t%s\t%d\n" % (p, task, judg, truth, correct))
            n += 1
    missing = len(paths) - len(rows)
    print("wrote %d rows -> %s (missing=%d)" % (n, out, missing))

if __name__ == "__main__":
    main()
