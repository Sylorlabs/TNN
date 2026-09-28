#!/usr/bin/env python3
"""G2 bad-record scan, sharded by task. Usage: badscan_shard.py <task>
Writes bad fixtures to ~/workspace/tmp_commit/g2eval/bad_<task>.txt"""
import os, subprocess, sys

TASK = sys.argv[1]
G2DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."))
G2BIN = os.path.join(G2DIR, "src", "sense")
HARNESS = os.path.normpath(os.path.join(
    G2DIR, "..", "..", "..", "rebuild", "harness", "fixtures"))
TD = {"colordisc": ("t1_colordisc", ".img"),
      "colorconst": ("t2_colorconst", ".img"),
      "shapetrans": ("t3_shapetrans", ".img"),
      "pitchdisc": ("t4_pitchdisc", ".pcm"),
      "timbredisc": ("t5_timbredisc", ".pcm"),
      "motiondir": ("t6_motiondir", ".vid")}[TASK]
KEYS = ("judgment", "confidence", "ops", "disposition",
        "residual_norm", "pred_hash", "obs_hash", "residuals", "ledger")

def complete(out):
    kv = {}
    for line in out.decode("utf-8", "replace").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            kv[k] = v
    ok = all(k in kv for k in KEYS)
    if "residuals" in kv:
        ok = ok and len(kv["residuals"].split(",")) == 256
    return ok

tdir, ext = TD
bad = []
n = 0
for variant in ("primary", "noise", "adversarial"):
    d = os.path.join(HARNESS, tdir, variant)
    for f in sorted(os.listdir(d)):
        if not f.endswith(ext):
            continue
        fx = os.path.join(d, f)
        n += 1
        p = subprocess.run([G2BIN, TASK, fx], capture_output=True,
                           timeout=600)
        if p.returncode != 0 or not complete(p.stdout):
            bad.append((variant, f, p.returncode))
out_p = os.path.expanduser("~/workspace/tmp_commit/g2eval/bad_%s.txt" % TASK)
with open(out_p, "w") as fo:
    fo.write("n=%d bad=%d\n" % (n, len(bad)))
    for b in bad:
        fo.write("BAD %s %s rc=%s\n" % b)
print("%s: n=%d bad=%d" % (TASK, n, len(bad)), flush=True)
for b in bad:
    print("  BAD:", b, flush=True)
