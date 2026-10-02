#!/usr/bin/env python3
"""Build script for Experiment B (slot scale).
Builds slot_driver.zag against two cores:
  build_merged/ : slot-scale/strength_core.zag (current law + cite_mode)
  build_base/   : pristine strength-recycle/strength_core.zag (cite_mode
                  call sites stripped via the [CITEMODE] marker)
Run from ~/workspace/slot-scale (imports resolve relative to cwd).
"""
import os, shutil, subprocess, sys

W = "/home/hatch/workspace/slot-scale"
ZNC = "/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"

def build(name, core_src, checker_src):
    d = os.path.join(W, name)
    os.makedirs(d, exist_ok=True)
    shutil.copy(core_src, os.path.join(d, "strength_core.zag"))
    shutil.copy(checker_src, os.path.join(d, "strength_checker.zag"))
    sub = os.path.join(d, "substrate")
    shutil.rmtree(sub, ignore_errors=True)
    shutil.copytree("/home/hatch/workspace/strength-recycle/substrate", sub)
    drv = open(os.path.join(W, "slot_driver.zag")).read()
    if name == "build_base":
        drv = "\n".join(l for l in drv.split("\n") if "[CITEMODE]" not in l)
    open(os.path.join(d, "slot_driver.zag"), "w").write(drv)
    out = os.path.join(d, "slot_bin")
    r = subprocess.run([ZNC, "slot_driver.zag", "-o", "slot_bin"],
                       cwd=d, capture_output=True, text=True, timeout=600)
    print(f"--- {name} ---")
    errs = [l for l in (r.stdout + r.stderr).splitlines() if "error" in l.lower()]
    if r.returncode != 0 or not os.path.exists(out):
        print(r.stdout[-3000:])
        print(r.stderr[-3000:])
        sys.exit(f"BUILD FAILED: {name}")
    for l in errs[:5]:
        print(l)
    print(f"OK: {out} ({os.path.getsize(out)} bytes)")

build("build_merged",
      os.path.join(W, "strength_core.zag"),
      os.path.join(W, "strength_checker.zag"))
build("build_base",
      "/home/hatch/workspace/strength-recycle/strength_core.zag",
      "/home/hatch/workspace/strength-recycle/strength_checker.zag")
print("both builds OK")
