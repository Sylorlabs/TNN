#!/usr/bin/env python3
"""Build the S' probe driver (NOT the frozen fork).

Mirrors battery/build_driver.py's "s" config exactly, except the fork
source is redteam/fork_s_prime.zag and the build dir / binary are
build_sp / bin_sp. The frozen build_driver.py is never modified.
"""
import os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BAT = os.path.join(HERE, "..", "battery")
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")

def build():
    bdir = os.path.join(BAT, "build_sp")
    os.makedirs(bdir, exist_ok=True)
    tpl = open(os.path.join(BAT, "driver_template.zag")).read()
    src = (tpl.replace("%%HIST_TY%%", "ForkHist")
              .replace("%%FNEW%%", "s_init")
              .replace("%%FDECIDE%%", "s_decide")
              .replace("%%FWARRANT%%", "s_warrant")
              .replace("%%EVENT_BLOCK%%",
                       "s_note(ep as i32,et as i32,src as i32,key as i32,val as i32,hp);"))
    assert "%%" not in src, "unsubstituted placeholder"
    open(os.path.join(bdir, "driver_sp.zag"), "w").write(src)
    shutil.copyfile(os.path.join(HERE, "fork_s_prime.zag"),
                    os.path.join(bdir, "fork.zag"))
    r = subprocess.run([ZNC, "driver_sp.zag", "-o", "bin_sp"],
                       cwd=bdir, capture_output=True, text=True)
    if r.stdout:
        print(r.stdout[-1500:])
    if r.returncode != 0 or not os.path.exists(os.path.join(bdir, "bin_sp")):
        print(r.stderr[-3000:] if r.stderr else "", file=sys.stderr)
        print("PROBE BUILD FAILED", file=sys.stderr)
        sys.exit(1)
    print("built probe driver: sp")

if __name__ == "__main__":
    build()
