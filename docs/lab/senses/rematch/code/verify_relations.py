#!/usr/bin/env python3
"""Verify the Python reimplementation of B's frozen relation tables
reproduces the instrumented B binary's judgments at hand-tuned values,
on all 925 round-1 fixtures. Must pass BEFORE any fitting.

Also sanity-checks timbre at hand thresholds (must match exactly) and
documents the expected motion divergence (centroid rule vs mcount rule,
CALIBRATION.md correction 1).
"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import relations as R

B_BIN = "/home/hatch/workspace/senses-rematch/b_inst/sense"
FIX = "/home/hatch/workspace/senses-rebuild/harness/fixtures"
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
TDIRS = {"colordisc": "t1_colordisc", "colorconst": "t2_colorconst",
         "shapetrans": "t3_shapetrans", "pitchdisc": "t4_pitchdisc",
         "timbredisc": "t5_timbredisc", "motiondir": "t6_motiondir"}

def run(task, fixture):
    p = subprocess.run([B_BIN, task, fixture], capture_output=True, text=True, timeout=180)
    assert p.returncode == 0, (task, fixture, p.stdout[:200])
    kv = {}
    for line in p.stdout.splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            kv[k.strip()] = v.strip()
    return kv

def main():
    mism = {"colordisc": 0, "colorconst": 0, "shapetrans": 0,
            "pitchdisc": 0, "timbredisc": 0, "motiondir": 0}
    total = 0
    motion_hand_match = 0
    for task in TASKS:
        d = os.path.join(FIX, TDIRS[task])
        for variant in ("primary", "noise", "adversarial"):
            vd = os.path.join(d, variant)
            if not os.path.isdir(vd):
                continue
            for f in sorted(os.listdir(vd)):
                if f.endswith(".truth"):
                    continue
                kv = run(task, os.path.join(vd, f))
                total += 1
                j = kv["judgment"]
                if task in ("colordisc", "colorconst"):
                    p1, p2 = int(kv["percept"]), int(kv["percept2"])
                    py = (R.b_color_judgment(p1, p2, 1) if task == "colordisc"
                          else R.b_colorconst_judgment(p1, p2, 1))
                elif task == "pitchdisc":
                    p1, p2 = int(kv["percept"]), int(kv["percept2"])
                    py = R.b_pitch_judgment(p1, p2, 0)
                elif task == "shapetrans":
                    tup = (int(kv["percept"]), int(kv["shape_curv"]), int(kv["shape_sym"]))
                    py = R.b_shape_judgment(tup, 0, (0, 1, 2))
                elif task == "timbredisc":
                    py = R.b_timbre_judgment(int(kv["timbre_crest"]),
                                             int(kv["timbre_bright"]),
                                             int(kv["timbre_form"]), 1150, 60, 1780)
                else:  # motiondir: expected divergence, recorded not failed
                    py = R.b_motion_judgment(int(kv["motion_mcount"]),
                                             int(kv["percept"]), 200)
                    if py == j:
                        motion_hand_match += 1
                    continue
                if py != j:
                    mism[task] += 1
                    if mism[task] <= 5:
                        print("MISMATCH", task, f, "binary=%s python=%s" % (j, py))
    print("checked: %d" % total)
    print("mismatches (must be 0):", mism)
    print("motiondir hand-t=200 agreement (expected divergence, doc only): %d" % motion_hand_match)
    bad = sum(v for k, v in mism.items() if k != "motiondir")
    sys.exit(1 if bad else 0)

main()
