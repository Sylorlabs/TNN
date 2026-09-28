#!/usr/bin/env python3
"""Write MANIFEST.r2p.sha256 over all R2P pair bytes."""
import hashlib, os, sys

R2P = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/fixtures/r2p")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]

lines = []
for task in TASKS:
    for idx in range(200):
        fn = "r2p_%s_%03d.pair" % (task, idx)
        fp = os.path.join(R2P, fn)
        h = hashlib.sha256(open(fp, "rb").read()).hexdigest()
        lines.append("%s  %s" % (h, fn))

out = os.path.join(R2P, "MANIFEST.r2p.sha256")
with open(out, "w") as f:
    f.write("\n".join(lines) + "\n")
print("wrote %s (%d entries)" % (out, len(lines)))
