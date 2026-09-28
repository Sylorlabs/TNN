#!/usr/bin/env python3
"""Differential test: Zag engine vs ref_dsl.py on 200 stress policies x 3 batteries.
New CLI: L1 translate_policy.py -> bytecode -> test_engine "<bc>" <r|p|n> json."""
import subprocess
import sys
import pathlib
import json

WORK = pathlib.Path(__file__).parent
BATTERIES = {
    "r": "/home/hatch/workspace/tnn-lab/rsi/autonomous_run_1/battery_r4c.csv",
    "p": "/home/hatch/workspace/tnn-lab/rsi/autonomous_run_1/proxy_battery.csv",
    "n": str(WORK / "novel_fields.csv"),
}
ENGINE = "/tmp/rsi2build/test_engine"
TRANSLATE = str(WORK / "translate_policy.py")
REF = str(WORK / "ref_dsl.py")
POL_DIR = WORK / "stress"

mismatch = 0
tested = 0
pols = sorted(POL_DIR.glob("stress_*.zpol"))
assert len(pols) == 200, f"expected 200 policies, got {len(pols)}"
for pol in pols:
    # L1: text -> bytecode
    t = subprocess.run(["python3", TRANSLATE, str(pol)],
                       capture_output=True, text=True)
    if t.returncode != 0:
        print(f"FAIL: L1 refused {pol.name}")
        print(t.stdout[:500], t.stderr[:500])
        sys.exit(1)
    bc = t.stdout.strip()
    for b, csv in BATTERIES.items():
        # Zag engine
        z = subprocess.run([ENGINE, bc, b, "json"],
                           capture_output=True, text=True)
        if z.returncode != 0:
            print(f"FAIL: zag refused {pol.name} battery {b} (rc={z.returncode})")
            print(z.stderr[:500])
            sys.exit(1)
        zrecs = [json.loads(l) for l in z.stdout.strip().split("\n")]
        # ref
        r = subprocess.run(["python3", REF, str(pol), csv],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"FAIL: ref refused {pol.name} battery {b}")
            sys.exit(1)
        rrecs = [json.loads(l) for l in r.stdout.strip().split("\n")]
        for zr, rr in zip(zrecs, rrecs):
            tested += 1
            if (zr["verdict"], zr["consulted"], zr["ops"]) != \
               (rr["verdict"], rr["consulted"], rr["ops"]):
                mismatch += 1
                print(f"MISMATCH {pol.name} battery {b} id={zr['id']}: "
                      f"zag={zr} ref={rr}")
                if mismatch > 10:
                    sys.exit(1)
    if int(pol.stem.split("_")[1]) % 50 == 49:
        print(f"  ... {pol.stem}/200 policies done, {tested} item-decisions, "
              f"{mismatch} mismatches", flush=True)
print(f"DONE: {tested} item-decisions, {mismatch} mismatches")
sys.exit(1 if mismatch else 0)
