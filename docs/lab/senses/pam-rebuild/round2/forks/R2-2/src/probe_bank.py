#!/usr/bin/env python3
"""Self-collision probe: every frozen bank entry must WITHHOLD its own class.

Runs the final sense2 binary on each of the 7 bank source fixtures.
Kill bar: zero self-collision installs (install must be 0 for all).

Usage: probe_bank.py <sense2-bin> <out.json>
"""
import os, sys, subprocess, json

SENSE2 = sys.argv[1]
OUTP = sys.argv[2]
LAB = "/home/hatch/workspace/tnn-lab"

BANK = [
    ("timbredisc", "senses/pam-rebuild/forks/G3/src/attack/t5_timbredisc/c003.pcm", "RICH", "G3-T5-boost-RICH"),
    ("shapetrans", "senses/pam-rebuild/forks/G3/src/attack/t3_shapetrans/c006.img", "CIRCLE", "G3-T3-occl-CIRCLE"),
    ("shapetrans", "senses/pam-rebuild/forks/G3/src/attack/t3_shapetrans/c008.img", "SQUARE", "G3-T3-occl-SQUARE"),
    ("motiondir", "senses/pam-rebuild/forks/G3/src/attack/t6_motiondir/c007.vid", "SE", "G3-T6-reversed-SE"),
    ("motiondir", "senses/pam-rebuild/forks/G3/src/attack/t6_motiondir/c009.vid", "NW", "G3-T6-reversed-NW"),
    ("colordisc", "senses/pam-rebuild/forks/H1/evidence/h1_adv/t1_colordisc/adv_h1/p003.img", "DIFFERENT", "H1-T1D-swaplum"),
    ("motiondir", "senses/pam-rebuild/forks/H1/evidence/h1_adv/t6_motiondir/adv_h1/p000.vid", "STILL", "H1-T6A-flicker"),
]

def parse(out):
    rec = {}
    for line in out.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            rec[k.strip()] = v.strip()
    return rec

results = []
for task, rel, truth, name in BANK:
    fx = os.path.join(LAB, rel)
    r = subprocess.run([SENSE2, fx, task, fx + ".truth", "GENESIS:probe"],
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise RuntimeError("sense2 failed on %s" % name)
    rec = parse(r.stdout)
    results.append({"name": name, "task": task, "truth": truth,
                    "class": rec.get("class"), "install": rec.get("install"),
                    "d_true": rec.get("d_true"), "d_false": rec.get("d_false")})
    print("%-22s class=%-8s install=%s d_true=%s d_false=%s" %
          (name, rec.get("class"), rec.get("install"), rec.get("d_true"), rec.get("d_false")))

n_install = sum(1 for x in results if x["install"] != "0")
print("self-collision installs: %d/7 %s" % (n_install, "PASS" if n_install == 0 else "KILL"))
json.dump(results, open(OUTP, "w"), indent=1, sort_keys=True)
sys.exit(1 if n_install else 0)
