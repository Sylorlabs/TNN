#!/usr/bin/env python3
"""Build the self-PAM composition with the pinned znc toolchain.

Builds (from this directory — znc resolves @import relative to CWD):
  main_smoke.zag   -> build/smoke_bin
  main_g1probe.zag -> build/g1probe_bin

Binaries land in build/ and are NOT committed (see README).
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
BUILD = os.path.join(HERE, "build")

TARGETS = [
    ("main_smoke.zag", "smoke_bin"),
    ("main_g1probe.zag", "g1probe_bin"),
]


def main():
    os.makedirs(BUILD, exist_ok=True)
    for src, out in TARGETS:
        dest = os.path.join(BUILD, out)
        if os.path.exists(dest):
            os.remove(dest)
        r = subprocess.run([ZNC, src, "-o", dest], cwd=HERE,
                           capture_output=True, text=True)
        # toolchain prints a zagd warning and analyzer notes on stdout/stderr;
        # fail only on real errors.
        if r.returncode != 0:
            print(f"BUILD FAILED: {src}", file=sys.stderr)
            print(r.stdout[-3000:], file=sys.stderr)
            print(r.stderr[-3000:], file=sys.stderr)
            sys.exit(1)
        print(f"built {src} -> build/{out}")
    print("OK")


if __name__ == "__main__":
    main()
