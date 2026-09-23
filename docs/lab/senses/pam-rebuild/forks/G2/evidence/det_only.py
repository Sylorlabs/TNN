#!/usr/bin/env python3
"""G2 B6 single-mode determinism: first 10 primary fixtures per task,
3 runs each, byte-identical stdout. Usage: det_only.py"""
import os, subprocess, sys

G2DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."))
G2BIN = os.path.join(G2DIR, "src", "sense")
HARNESS = os.path.normpath(os.path.join(
    G2DIR, "..", "..", "..", "rebuild", "harness", "fixtures"))
TASKS = [
    ("colordisc", "t1_colordisc", ".img"),
    ("colorconst", "t2_colorconst", ".img"),
    ("shapetrans", "t3_shapetrans", ".img"),
    ("pitchdisc", "t4_pitchdisc", ".pcm"),
    ("timbredisc", "t5_timbredisc", ".pcm"),
    ("motiondir", "t6_motiondir", ".vid"),
]

def run(args):
    p = subprocess.run(args, capture_output=True, timeout=600)
    return p.returncode, p.stdout

det_ok = True
checked = 0
for task, tdir, ext in TASKS:
    d = os.path.join(HARNESS, tdir, "primary")
    fxs = sorted(os.path.join(d, f) for f in os.listdir(d)
                 if f.endswith(ext))[:10]
    for fx in fxs:
        base = run([G2BIN, task, fx])
        for _ in range(2):
            if run([G2BIN, task, fx]) != base:
                det_ok = False
                print("DETERMINISM MISMATCH:", fx, flush=True)
        checked += 1
    print("task %s done" % task, flush=True)
print("RESULT single-mode determinism: %s (%d fixtures x3)"
      % ("PASS" if det_ok else "FAIL", checked))
