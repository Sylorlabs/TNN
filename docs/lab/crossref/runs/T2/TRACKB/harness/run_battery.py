#!/usr/bin/env python3
"""Run the D1 adversarial-regime battery: 5 regimes x 3 variants x 3 reps."""
import json, os, sys, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legs import run_leg

REGIMES = ["adopt_all", "r1storm", "r34storm", "revise_spam", "mixed"]
VARIANTS = ["A", "B", "C"]
REPS = 3

def main():
    root = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath("work/d1")
    only = sys.argv[2].split(",") if len(sys.argv) > 2 else None
    table = []
    for v in VARIANTS:
        for pol in REGIMES:
            if only and f"{v}:{pol}" not in only:
                continue
            shas = set()
            reps = []
            for r in range(REPS):
                wd = os.path.join(root, v, pol, f"rep{r}")
                m = run_leg(v, pol, wd, 7000 + 100 * REPS + r)
                with open(os.path.join(wd, "metrics.json"), "w") as f:
                    json.dump(m, f, indent=1, sort_keys=True)
                reps.append(m)
                shas.add(m["canon_sha"])
            det = "IDENTICAL" if len(shas) == 1 else "DIVERGED"
            row = dict(variant=v, policy=pol, reps=reps, determinism=det)
            table.append(row)
            r0 = reps[0]
            print(f"{v} {pol:11s} det={det} n={r0['n_proposals']} "
                  f"kinds={r0['kinds']} conf=[{r0['conf_min']},{r0['conf_max']}] "
                  f"term={r0['terminal']} conv={r0.get('converged')} "
                  f"turns={r0.get('turns')} B/prop={r0['bytes_per_proposal']}",
                  flush=True)
    with open(os.path.join(root, "d1_table.json"), "w") as f:
        json.dump(table, f, indent=1)
    print("wrote", os.path.join(root, "d1_table.json"))

if __name__ == "__main__":
    main()
