#!/usr/bin/env python3
"""3x determinism check for the rt4fix repaired assembly.

Runs the pure-Zag decider 3x over every fixed input set (both modes) and
verifies byte-identical stdout each time. Prints SHA256 of each output.
No RNG anywhere: decide.zag contains no random calls (verified by grep).
"""
import subprocess, hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DECIDE = HERE + "/src/decide"

INPUTS = []
for d in sorted(os.listdir(HERE + "/runs")):
    p = os.path.join(HERE, "runs", d, "decide_in.tsv")
    if os.path.isfile(p):
        INPUTS.append(p)

def sha(b):
    return hashlib.sha256(b).hexdigest()

ok = True
for inp in INPUTS:
    for mode in ("old", "new"):
        outs = []
        for i in range(3):
            r = subprocess.run([DECIDE, inp, mode], capture_output=True)
            assert r.returncode == 0, (inp, mode, r.stderr[:200])
            outs.append(r.stdout)
        s = [sha(o) for o in outs]
        same = s[0] == s[1] == s[2]
        ok = ok and same
        print("%s %s %s %s" % ("OK " if same else "DIFF", mode,
                               s[0][:16], os.path.relpath(inp, HERE)))
print("DETERMINISM:", "PASS 3x byte-identical" if ok else "FAIL")
sys.exit(0 if ok else 1)
