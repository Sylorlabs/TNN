#!/usr/bin/env python3
"""Pilot evaluation: run the full R2-4 pipeline on N fixtures to validate the harness."""
import os
import sys
import json

# Use the canonical eval script as a module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import eval_r24_all as E

N = int(sys.argv[1]) if len(sys.argv) > 1 else 200

def main():
    # Override WORK to pilot dir
    pilot_work = os.path.join(os.path.dirname(__file__), "_pilot")
    os.makedirs(pilot_work, exist_ok=True)
    E.WORK = pilot_work
    # Limit trials
    orig_build = E.build_trials
    def limited_build():
        trials = orig_build()
        print("pilot: limiting %d trials to %d" % (len(trials), N), flush=True)
        return trials[:N]
    E.build_trials = limited_build
    # Run the full pipeline (override argv to get "all" command)
    sys.argv = ["pilot.py", "all"]
    E.main()
    # Print summary
    m = json.load(open(os.path.join(pilot_work, "metrics.json")))
    print("\n=== PILOT METRICS (N=%d) ===" % N)
    for k in sorted(m.keys()):
        if k.startswith("RK") or k.startswith("B"):
            print("%s: %s" % (k, m[k]))

if __name__ == "__main__":
    main()
