#!/usr/bin/env python3
"""G2 B6 part 1: single-mode determinism (first 10 primary fixtures per task,
3 runs each, byte-identical) + full 925-fixture bad-record scan for the
'_TBD which' integration fixture."""
import os, subprocess

G2DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."))
G2BIN = os.path.join(G2DIR, "src", "sense")
ABIN = os.path.join(G2DIR, "evidence", "bin_A")
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
VARIANTS = ["primary", "noise", "adversarial"]
G2KEYS = ("judgment", "confidence", "ops", "disposition",
          "residual_norm", "pred_hash", "obs_hash", "residuals", "ledger")
AKEYS = ("judgment", "confidence", "ops")

def run(args):
    p = subprocess.run(args, capture_output=True, timeout=600)
    return p.returncode, p.stdout

def fixtures(task, tdir, ext, variant):
    d = os.path.join(HARNESS, tdir, variant)
    return sorted(os.path.join(d, f) for f in os.listdir(d)
                  if f.endswith(ext))

def complete(out, keys):
    kv = {}
    for line in out.decode("utf-8", "replace").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            kv[k] = v
    ok = all(k in kv for k in keys)
    if "residuals" in kv:
        ok = ok and len(kv["residuals"].split(",")) == 256
    return ok

# ---- determinism: first 10 primaries per task ----
det_ok = True
checked = 0
for task, tdir, ext in TASKS:
    for fx in fixtures(task, tdir, ext, "primary")[:10]:
        base = run([G2BIN, task, fx])
        for _ in range(2):
            if run([G2BIN, task, fx]) != base:
                det_ok = False
                print("DETERMINISM MISMATCH:", fx)
        checked += 1
print("single-mode determinism: %s (%d fixtures x3 runs)" %
      ("PASS" if det_ok else "FAIL", checked))

# ---- bad-record scan over all 925 harness fixtures, G2 and A ----
for label, binary, keys in (("G2", G2BIN, G2KEYS), ("A", ABIN, AKEYS)):
    bad = []
    n = 0
    for task, tdir, ext in TASKS:
        for variant in VARIANTS:
            for fx in fixtures(task, tdir, ext, variant):
                n += 1
                rc, out = run([binary, task, fx])
                if rc != 0 or not complete(out, keys):
                    bad.append((task, variant, os.path.basename(fx), rc))
    print("%s: %d/%d complete records, bad fixtures:" % (label, n - len(bad), n))
    for b in bad:
        print("  BAD:", b)
