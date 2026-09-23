#!/usr/bin/env python3
"""D5 (head-to-head, gt policy), D2 (curriculum shift), D4 (noise) battery."""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legs import run_leg

VARIANTS = ["A", "B", "C"]
REPS = 3

# (battery, policy, curr)
PLAN = [
    ("d5", "gt", "std"),
    ("d2", "gt", "shift"),
    ("d4n10", "gt", "noise10"),
    ("d4n25", "gt", "noise25"),
]

def main():
    root = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath("work/d5d2d4")
    table = []
    for batt, pol, curr in PLAN:
        for v in VARIANTS:
            shas = set()
            reps = []
            for r in range(REPS):
                wd = os.path.join(root, batt, v, f"rep{r}")
                m = run_leg(v, pol, wd, 8000 + 37 * REPS + r, curr=curr)
                with open(os.path.join(wd, "metrics.json"), "w") as f:
                    json.dump(m, f, indent=1, sort_keys=True)
                reps.append(m)
                shas.add(m["canon_sha"])
            det = "IDENTICAL" if len(shas) == 1 else "DIVERGED"
            table.append(dict(battery=batt, variant=v, policy=pol, curr=curr,
                              reps=reps, determinism=det))
            r0 = reps[0]
            print(f"{batt} {v} {pol}/{curr} det={det} n={r0['n_proposals']} "
                  f"kinds={r0['kinds']} conf=[{r0['conf_min']},{r0['conf_max']}] "
                  f"term={r0['terminal']} conv={r0.get('converged')} "
                  f"turns={r0.get('turns')} B/prop={r0['bytes_per_proposal']}",
                  flush=True)
    with open(os.path.join(root, "d5d2d4_table.json"), "w") as f:
        json.dump(table, f, indent=1)
    print("wrote", os.path.join(root, "d5d2d4_table.json"))

if __name__ == "__main__":
    main()
