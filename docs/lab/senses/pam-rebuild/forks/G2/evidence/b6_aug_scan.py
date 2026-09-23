#!/usr/bin/env python3
"""G2 B6 part 3: augmentation-set single-mode accuracy (240 adversarial
fixtures from augment/augment.py), plus install/withhold disposition counts."""
import os, subprocess

G2DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."))
G2BIN = os.path.join(G2DIR, "src", "sense")
AUG = os.path.join(G2DIR, "augment", "out")
TASKS = [
    ("colordisc", "t1_colordisc", ".img"),
    ("colorconst", "t2_colorconst", ".img"),
    ("shapetrans", "t3_shapetrans", ".img"),
    ("pitchdisc", "t4_pitchdisc", ".pcm"),
    ("timbredisc", "t5_timbredisc", ".pcm"),
    ("motiondir", "t6_motiondir", ".vid"),
]

def truth_of(path):
    with open(path + ".truth") as f:
        return f.read().strip().split("=", 1)[1]

n = correct = 0
install = withhold = 0
for task, tdir, ext in TASKS:
    d = os.path.join(AUG, tdir)
    for f in sorted(os.listdir(d)):
        if not f.endswith(ext):
            continue
        fx = os.path.join(d, f)
        p = subprocess.run([G2BIN, task, fx], capture_output=True, timeout=600)
        kv = {}
        for line in p.stdout.decode("utf-8", "replace").splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                kv[k] = v
        assert p.returncode == 0 and "judgment" in kv, "AUG FAIL %s" % fx
        n += 1
        if kv["judgment"] == truth_of(fx):
            correct += 1
        if kv.get("disposition") == "INSTALL":
            install += 1
        else:
            withhold += 1
print("aug: %d fixtures, %d correct (%.2f%%), installs %d, withholds %d"
      % (n, correct, 100.0 * correct / n, install, withhold))
