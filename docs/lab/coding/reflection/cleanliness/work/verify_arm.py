#!/usr/bin/env python3
"""verify_arm.py <arm>: compile every sources/<id>/<arm>.zag with pinned znc,
run, byte-compare stdout+rc against SPECS.json expected outputs. Pure glue."""
import json, subprocess, sys, pathlib

BASE = pathlib.Path.home() / "workspace/tnn-lab/coding/reflection/cleanliness"
ZNC = str(pathlib.Path.home() / "workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")

def main():
    arm = sys.argv[1]
    specs = {s["id"]: s for s in json.loads((BASE / "SPECS.json").read_text())["items"]}
    ok, bad = 0, []
    for sid, spec in sorted(specs.items()):
        src = BASE / "sources" / sid / f"{arm}.zag"
        if not src.exists():
            bad.append(f"{sid} missing"); continue
        binary = BASE / "work" / f"v_{arm}_{sid}"
        c = subprocess.run([ZNC, str(src), "-o", str(binary), "--no-zagd", "--no-analyze"],
                           capture_output=True, text=True, timeout=120)
        if c.returncode != 0 or not binary.exists():
            bad.append(f"{sid} COMPILE_FAIL {c.stderr.strip()[:120]}"); continue
        r = subprocess.run([str(binary)], capture_output=True, timeout=30)
        t = spec["tests"][0]
        expb = t["stdout"].encode("utf-8").decode("unicode_escape").encode("utf-8")
        if r.stdout == expb and r.returncode == t["rc"]:
            ok += 1
        else:
            bad.append(f"{sid} OUTPUT_MISMATCH got={r.stdout!r} rc={r.returncode}")
    print(f"arm: {arm} pass: {ok} fail: {len(bad)}")
    for b in bad:
        print(" FAIL", b)

if __name__ == "__main__":
    main()
