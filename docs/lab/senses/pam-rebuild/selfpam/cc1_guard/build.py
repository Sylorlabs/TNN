#!/usr/bin/env python3
"""build.py — deterministic build of the CC1 guard verification binary.

Uses ONLY the pinned toolchain. Writes the binary to build/ (uncommitted).
Zero RNG anywhere in the build or the produced binary's execution path.
"""
import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
OUT = os.path.join(SRC, "build", "cc1_bin")

def main():
    os.makedirs(os.path.join(SRC, "build"), exist_ok=True)
    r = subprocess.run([ZNC, "main_cc1.zag", "-o", OUT],
                       cwd=SRC, capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    if r.returncode != 0:
        sys.stderr.write("BUILD FAILED\n")
        return 1
    # smoke: run twice, must be byte-identical
    a = subprocess.run([OUT], capture_output=True)
    b = subprocess.run([OUT], capture_output=True)
    if a.returncode != 0 or b.returncode != 0:
        sys.stderr.write("SMOKE RUN FAILED\n")
        return 1
    if a.stdout != b.stdout:
        sys.stderr.write("NONDETERMINISM: two runs differ\n")
        return 1
    sys.stdout.write(f"build ok: {OUT} (smoke 2x byte-identical)\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
