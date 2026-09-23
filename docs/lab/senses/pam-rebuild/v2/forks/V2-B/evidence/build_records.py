#!/usr/bin/env python3
"""Build vgate record files from R2-4's frozen sweep.jsonl + gexp G-judgments.
Record format: seq|tcode|fid|prog|jcode|judgment|confidence|pred|measure|phash|truth|jG|confG
Glue only; no decisions."""
import json, os

LAB = "/home/hatch/workspace/tnn-lab"
R24 = LAB + "/senses/pam-rebuild/round2/forks/R2-4"
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
PROG_OF = {"PASS": 0, "FAIL": 1, "UNRESOLVED": 2}
# judgment -> code (from R2-4 eval_r24_all.py JCODES)
JCODES = {
 "colordisc": {"SAME":0,"DIFFERENT":1},
 "colorconst": {"SAME":0,"DIFFERENT":1,"SAME_SURFACE":0},
 "shapetrans": {"SQUARE":0,"TRIANGLE":1,"CIRCLE":2},
 "pitchdisc": {"HIGHER":1,"LOWER":2,"SAME":0},
 "timbredisc": {"PURE":0,"DARK":1,"RICH":2,"BRIGHT":3},
 "motiondir": {"STILL":0,"N":1,"NE":2,"E":3,"SE":4,"S":5,"SW":6,"W":7,"NW":8},
}

def load():
    rows = [json.loads(l) for l in open(R24+"/evidence/clean/sweep.jsonl")]
    rows = [r for r in rows if "err" not in r]
    rows.sort(key=lambda r: r["seq"])
    gout = json.load(open("/home/hatch/workspace/v2work/gexp_out.json"))
    g = {}
    for s,(j,c,rc) in gout.items():
        if rc==0 and j is not None:
            # map G judgment string to code using the row's task later
            g[int(s)] = (j, int(c) if c else 0)
    return rows, g

def build(out_path):
    rows, g = load()
    n_no_g = 0
    with open(out_path, "w") as f:
        for r in rows:
            tc = TASKS.index(r["task"])
            prog = PROG_OF.get(r["prog"], 2)
            jc = JCODES[r["task"]].get(r["judgment"], -1)
            gj, gc = g.get(r["seq"], (None, 0))
            if gj is None:
                jg_code, confg = -1, 0
                n_no_g += 1
            else:
                jg_code = JCODES[r["task"]].get(gj, -1)
                confg = gc
                if jg_code < 0:
                    jg_code, confg = -1, 0
            f.write("%d|%d|%s|%d|%d|%s|%d|%d|%d|%s|%s|%d|%d\n" % (
                int(r["seq"]), tc, r["fid"], prog, jc, r["judgment"], int(r["conf"]),
                int(r["pred"]), int(r["measure"]), r.get("phash",""), r["truth"],
                jg_code, confg))
    print(f"wrote {out_path}: {len(rows)} records, {n_no_g} without G")

if __name__ == "__main__":
    import sys
    build(sys.argv[1])
