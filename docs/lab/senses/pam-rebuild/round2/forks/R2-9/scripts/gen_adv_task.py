#!/usr/bin/env python3
"""Generate R2-9's adversarial fixtures for ONE task (parallel worker).
Replicates r2a_gen.py main()'s adversarial loop exactly for a single task:
same seeds (stream 500+taskidx, per-task idx counter across families),
same fixture ids, same output dirs. Deterministic; safe to run 6 in parallel.
Usage: gen_adv_task.py <taskidx> <outdir>
"""
import os, sys

LAB = os.path.expanduser("~/workspace/tnn-lab")
sys.path.insert(0, os.path.join(LAB, "senses", "pam-rebuild", "round2", "fixtures"))
sys.path.insert(0, os.path.join(LAB, "senses", "rebuild", "harness"))
import r2a_gen as G

def main():
    ti = int(sys.argv[1])
    out = sys.argv[2]
    task = G.TASKS[ti]
    adv_d = os.path.join(out, "adversarial")
    ext = G.EXTS[ti]
    idx = 0
    ann = {}
    for fti, fam, count in G.ADV_PLAN:
        if fti != ti:
            continue
        d = os.path.join(adv_d, fam)
        os.makedirs(d, exist_ok=True)
        fn = G.ADV_FN[fam]
        for j in range(count):
            rng = G.stream_rng(500 + ti, idx)
            fid = "r2a_%s_%04d" % (task, idx)
            path = os.path.join(d, fid + ext)
            if os.path.exists(path + ".truth"):
                idx += 1
                continue  # resume: deterministic, already written
            payload, dims, truth, a = fn(rng, 170)
            G.write_payload(path, ext, payload, dims)
            G.emit(fid, d, ext, truth, a)
            if a:
                ann[fid] = a
            idx += 1
        print("task %s family %s: %d (idx now %d)" % (task, fam, count, idx), flush=True)
    import json
    with open(os.path.join(out, "annotations_%s.json" % task), "w") as f:
        json.dump(ann, f, indent=1, sort_keys=True)
    print("DONE task %s: %d adversarial fixtures" % (task, idx), flush=True)

if __name__ == "__main__":
    main()
