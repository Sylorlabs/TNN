#!/usr/bin/env python3
"""V2-B: run vsense_b on P-spans, sharded. Outputs JSONL with judgments."""
import os, sys, subprocess, json

PSPANS = "/home/hatch/workspace/v2work/pspans"
VSENSE = "/tmp/vsense_b"
OUT = "/home/hatch/workspace/v2work"

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]

def parse_out(txt):
    d = {}
    for line in txt.split("\n"):
        if "=" in line:
            k, v = line.split("=", 1)
            d[k.strip()] = v.strip()
    return d

def main():
    shard, nsh = int(sys.argv[1]), int(sys.argv[2])
    files = sorted(f for f in os.listdir(PSPANS) if f.endswith(".r24"))
    files = [f for i, f in enumerate(files) if i % nsh == shard]
    out_path = os.path.join(OUT, f"prun_{shard}.jsonl")
    out = open(out_path, "w")
    for fi, fn in enumerate(files):
        # fn like r2n_colordisc_0000.r24.P1.r24
        parts = fn.split(".")
        pert = parts[-2]  # P1, P2, P3
        base = ".".join(parts[:-2])  # r2n_colordisc_0000.r24
        task = base.split("_")[1]
        if task not in TASKS:
            continue
        fp = os.path.join(PSPANS, fn)
        try:
            r = subprocess.run([VSENSE, task, fp], capture_output=True, text=True, timeout=30)
            d = parse_out(r.stdout)
            rec = {
                "src": base,
                "pert": pert,
                "task": task,
                "judgment": d.get("judgment", "?"),
                "conf": int(d.get("confidence", -1)),
                "rc": r.returncode,
            }
        except Exception as e:
            rec = {"src": base, "pert": pert, "task": task, "err": str(e)}
        out.write(json.dumps(rec) + "\n")
        if fi % 500 == 0:
            print(f"shard {shard}: {fi}/{len(files)}", flush=True)
    out.close()
    print(f"shard {shard} done", flush=True)

if __name__ == "__main__":
    main()
