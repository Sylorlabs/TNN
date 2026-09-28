#!/usr/bin/env python3
"""a_run.py — batch runner for Approach A sense binary (B2/B3 head-to-head).

Runs `senseA <task> <fixture>` over a fixture tree. Parses key=value.
Writes JSONL: path, task, variant, judgment, confidence, ops, debug_vec,
debug_bytes (len of debug_vec = A's percept bytes), truth, correct.
"""
import os, sys, json, subprocess

def parse_record(out):
    d = {}
    for line in out.split("\n"):
        if "=" in line:
            k, v = line.split("=", 1)
            d[k.strip()] = v.strip()
    return d

def run_tree(binary, fixture_root, out_path, flat_variant=None):
    recs = []
    for taskdir in sorted(os.listdir(fixture_root)):
        tdir = os.path.join(fixture_root, taskdir)
        if not os.path.isdir(tdir):
            continue
        task = taskdir[3:] if len(taskdir) > 3 and taskdir[2] == "_" else taskdir
        variants = []
        if flat_variant is not None:
            variants = [(flat_variant, tdir)]
        else:
            for variant in sorted(os.listdir(tdir)):
                vdir = os.path.join(tdir, variant)
                if os.path.isdir(vdir):
                    variants.append((variant, vdir))
        for variant, vdir in variants:
            for name in sorted(os.listdir(vdir)):
                if name.endswith(".truth"):
                    continue
                p = os.path.join(vdir, name)
                if not os.path.isfile(p):
                    continue
                r = subprocess.run([binary, task, p], capture_output=True)
                kv = parse_record(r.stdout.decode(errors="replace"))
                truth = None
                tp = p + ".truth"
                if os.path.exists(tp):
                    truth = open(tp).read().strip().split("=", 1)[-1]
                dv = kv.get("debug_vec", "")
                rec = {
                    "path": p, "task": task, "variant": variant,
                    "judgment": kv.get("judgment"),
                    "confidence": kv.get("confidence"), "ops": kv.get("ops"),
                    "debug_vec": dv, "debug_bytes": len(dv),
                    "truth": truth,
                    "correct": (kv.get("judgment") == truth) if truth else None,
                    "rc": r.returncode,
                }
                recs.append(rec)
    with open(out_path, "w") as f:
        for rec in recs:
            f.write(json.dumps(rec) + "\n")
    print("ran %d -> %s" % (len(recs), out_path))

if __name__ == "__main__":
    binary, fixture_root, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    flat = sys.argv[4] if len(sys.argv) > 4 else None
    run_tree(binary, fixture_root, out_path, flat)
