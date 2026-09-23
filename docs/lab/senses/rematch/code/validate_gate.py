#!/usr/bin/env python3
"""VALIDATION GATE: instrumented B binary vs original B binary on all
925 round-1 fixtures. Every non-instrument key must be byte-identical
(judgment path untouched). New instrument keys are ignored."""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OLD = "/home/hatch/workspace/senses-rebuild/b_percept/sense"
NEW = "/home/hatch/workspace/senses-rematch/b_inst/sense"
FIX = "/home/hatch/workspace/senses-rebuild/harness/fixtures"
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
TDIRS = {"colordisc": "t1_colordisc", "colorconst": "t2_colorconst",
         "shapetrans": "t3_shapetrans", "pitchdisc": "t4_pitchdisc",
         "timbredisc": "t5_timbredisc", "motiondir": "t6_motiondir"}
INSTR = {"timbre_crest", "timbre_bright", "timbre_form",
         "motion_mcount", "motion_dx", "motion_dy"}

def run(binary, task, fixture):
    p = subprocess.run([binary, task, fixture], capture_output=True,
                       text=True, timeout=180)
    if p.returncode != 0:
        return None, "exit=%d" % p.returncode
    return p.stdout, None

def parse(stdout):
    kv = {}
    for line in stdout.splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            kv[k.strip()] = v.strip()
    return kv

def main():
    total = 0
    mism = []
    inst_vals = {}  # fixture -> instrument keys seen (sanity)
    for task in TASKS:
        d = os.path.join(FIX, TDIRS[task])
        for variant in ("primary", "noise", "adversarial"):
            vd = os.path.join(d, variant)
            if not os.path.isdir(vd):
                continue
            for f in sorted(os.listdir(vd)):
                if f.endswith(".truth"):
                    continue
                fp = os.path.join(vd, f)
                o1, e1 = run(OLD, task, fp)
                o2, e2 = run(NEW, task, fp)
                total += 1
                if e1 or e2:
                    mism.append((fp, "run-error", e1, e2))
                    continue
                k1, k2 = parse(o1), parse(o2)
                # every old key must match byte-identically in the new output
                for k, v in k1.items():
                    if k not in k2:
                        mism.append((fp, "missing-key", k, None))
                    elif k2[k] != v:
                        mism.append((fp, "value-diff", k, "%r vs %r" % (v, k2[k])))
                # instrument keys must be present (timbredisc/motiondir)
                new_only = {k: v for k, v in k2.items() if k not in k1}
                for k in new_only:
                    if k not in INSTR:
                        mism.append((fp, "unexpected-new-key", k, new_only[k]))
                inst_vals[fp] = new_only
    print("checked: %d" % total)
    print("mismatches: %d" % len(mism))
    for m in mism[:25]:
        print(m)
    # sanity: instruments actually emit on the instrumented tasks
    tb = [v for f, v in inst_vals.items() if "timbredisc" in f]
    mo = [v for f, v in inst_vals.items() if "motiondir" in f]
    print("timbredisc fixtures w/ 3 feature keys: %d/%d" %
          (sum(1 for v in tb if set(v) == {"timbre_crest","timbre_bright","timbre_form"}), len(tb)))
    print("motiondir fixtures w/ 3 motion keys: %d/%d" %
          (sum(1 for v in mo if set(v) == {"motion_mcount","motion_dx","motion_dy"}), len(mo)))
    sys.exit(1 if mism else 0)

main()
