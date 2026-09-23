#!/usr/bin/env python3
"""G0 reproduction gate (glue only). PREREG_FROZEN_F2APPEAL.md §3.

For pass in {1,2}: run frozen sense A and B on all 185 original fixtures,
record judgment+confidence. Then join against truth.json's frozen records:
370/370 must match, and the two passes must be byte-identical. Any mismatch
-> HALT (prints GATE=HALT). Also writes the J-cache reused by R1/R2/R4.

Outputs: out_g0/jwave_run{N}.tsv (sense\\ttask\\tvariant\\tlogical\\tjudgment\\tconfidence),
out_g0/reproduction_report.txt.
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

CHAN = os.path.dirname(os.path.abspath(__file__))
TN = os.path.expanduser("~/workspace/tnn-lab")
FIXROOT = os.path.join(TN, "senses", "rebuild", "harness", "fixtures")
SENSE_A = os.path.join(TN, "senses", "rebuild", "a_raw", "sense")
SENSE_B = os.path.expanduser("~/workspace/kb4-f2/build_b/sense_b_rebuilt")
SENSES = {"A": SENSE_A, "B": SENSE_B}
TRUTH = os.path.join(TN, "prose-learning", "epistemic_wave", "kb4_rerun", "truth.json")
OUT = os.path.join(CHAN, "out_g0")
WORKERS = 12

def logical(task, relpath):
    base = relpath.rsplit("/", 1)[-1]
    if base.endswith(".img"):
        base = base[:-4]
    return "%s/%s" % (task, base)

def run_sense(spath, task, fx):
    q = subprocess.run([spath, task, fx], capture_output=True, text=True, timeout=120)
    if q.returncode != 0:
        raise RuntimeError("sense rc=%d: %s" % (q.returncode, q.stdout.strip()[:200]))
    j = c = None
    for line in q.stdout.splitlines():
        if line.startswith("judgment="):
            j = line[len("judgment="):]
        elif line.startswith("confidence="):
            c = line[len("confidence="):]
    if j is None or c is None:
        raise RuntimeError("no judgment/confidence: %r" % q.stdout[:200])
    return j, c

def one(args):
    tag, spath, task, variant, log, src = args
    j, c = run_sense(spath, task, src)
    return (tag, task, variant, log, j, c)

def main():
    man = json.load(open(os.path.join(CHAN, "..", "inputs_tcp", "blob_manifest.json")))
    runs = [int(x) for x in sys.argv[1:]] or [1, 2]
    os.makedirs(OUT, exist_ok=True)
    for run in runs:
        path = os.path.join(OUT, "jwave_run%d.tsv" % run)
        done = set()
        if os.path.exists(path):
            for line in open(path):
                p = line.rstrip("\n").split("\t")
                if len(p) >= 4:
                    done.add((p[0], p[3]))
        jobs = []
        for r in man:
            log = logical(r["task"], r["relpath"])
            src = os.path.join(FIXROOT, r["relpath"])
            for tag, spath in SENSES.items():
                if (tag, log) not in done:
                    jobs.append((tag, spath, r["task"], r["variant"], log, src))
        rows = {}
        for line in open(path) if os.path.exists(path) else []:
            p = line.rstrip("\n").split("\t")
            rows[(p[0], p[3])] = p
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            for (tag, task, variant, log, j, c) in ex.map(one, jobs):
                rows[(tag, log)] = [tag, task, variant, log, j, c]
        with open(path, "w") as f:
            for (tag, log) in sorted(rows):
                f.write("\t".join(rows[(tag, log)]) + "\n")
        print("pass %d: %d rows" % (run, len(rows)), flush=True)
    # byte-identical passes?
    l1 = open(os.path.join(OUT, "jwave_run1.tsv")).read()
    l2 = open(os.path.join(OUT, "jwave_run2.tsv")).read()
    ident = (l1 == l2)
    # join vs truth.json (score-time only). Mirror the frozen prep_truth_rows
    # filter EXACTLY: keys are (sense, task, variant, task+"/"+base) from the
    # manifest; truth.json carries primary/noise/adversarial duplicates per
    # stim, so the variant-qualified filter is required (noise rows excluded,
    # no (sense,task,logical) collisions in the selected set).
    truth = json.load(open(TRUTH))
    man = json.load(open(os.path.join(CHAN, "..", "inputs_tcp", "blob_manifest.json")))
    def mbase(r):
        b = r["relpath"].rsplit("/", 1)[-1]
        if b.endswith(".img"):
            b = b[:-4]
        return b
    keys = set()
    for r in man:
        for se in ("A", "B"):
            keys.add((se, r["task"], r["variant"], r["task"] + "/" + mbase(r)))
    tmap = {}
    for k, v in truth.items():
        se = k.split("/", 1)[0]
        kk = (se, v["task"], v["variant"], v["stim"])
        if kk in keys:
            tmap[(se, v["task"], v["variant"], v["stim"])] = (v["judgment"], str(v["confidence"]))
    mism = []
    total = 0
    for line in l1.splitlines():
        p = line.split("\t")
        tag, task, variant, log, j, c = p[0], p[1], p[2], p[3], p[4], p[5]
        key = (tag, task, variant, log)
        total += 1
        if key not in tmap:
            mism.append("NOTRUTH %s %s %s" % (tag, variant, log))
        elif tmap[key] != (j, c):
            mism.append("DIFF %s %s %s got=(%s,%s) frozen=(%s,%s)" % (tag, variant, log, j, c, tmap[key][0], tmap[key][1]))
    rep = []
    rep.append("G0 reproduction gate")
    rep.append("pass1==pass2 byte-identical: %s" % ident)
    rep.append("rows compared vs truth.json: %d" % total)
    rep.append("mismatches: %d" % len(mism))
    for m in mism[:20]:
        rep.append("  " + m)
    rep.append("GATE=" + ("PASS" if (ident and not mism and total == 370) else "HALT"))
    open(os.path.join(OUT, "reproduction_report.txt"), "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))
    sys.exit(0 if (ident and not mism and total == 370) else 1)

if __name__ == "__main__":
    main()
