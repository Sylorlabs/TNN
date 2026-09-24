#!/usr/bin/env python3
"""build_b3536.py — assemble b3536.zag (lib + composition driver), compile
with the pinned znc toolchain, record SHAs. Build BEFORE any run (prereg §5).
"""
import hashlib
import os
import shutil
import subprocess
import sys

WORK = os.path.expanduser("~/workspace/b3536_scratch")
BUILD = os.path.join(WORK, "build")
REPO = os.path.expanduser("~/workspace/selfpam_run/tnn-lab")
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def gshow(commit, path, dst):
    r = subprocess.run(["git", "show", f"{commit}:{path}"],
                       capture_output=True, cwd=REPO)
    assert r.returncode == 0, f"git show failed {commit}:{path}"
    with open(dst, "wb") as f:
        f.write(r.stdout)


def main():
    os.makedirs(BUILD, exist_ok=True)
    # support substrates (R-36 commit carries both)
    gshow("6a30f5f9", "docs/lab/senses/pam-rebuild/round2/r36_repair/R33_NATIVE_IO_V1.zag",
          os.path.join(BUILD, "R33_NATIVE_IO_V1.zag"))
    gshow("6a30f5f9", "docs/lab/senses/pam-rebuild/round2/r36_repair/R33_NATIVE_SHA256_V2.zag",
          os.path.join(BUILD, "R33_NATIVE_SHA256_V2.zag"))
    # assemble
    with open(os.path.join(WORK, "b3536_lib.zag"), "rb") as f:
        lib = f.read()
    with open(os.path.join(WORK, "comp_drive.zag"), "rb") as f:
        drv = f.read()
    src = lib + b"\n// ================= composition driver =================\n" + drv
    src_path = os.path.join(BUILD, "b3536.zag")
    with open(src_path, "wb") as f:
        f.write(src)
    print(f"b3536.zag sha={sha(src)} bytes={len(src)}", flush=True)
    # compile (cwd = BUILD so @import resolves)
    r = subprocess.run([ZNC, "b3536.zag", "-o", "b3536"],
                       capture_output=True, text=True, cwd=BUILD, timeout=600)
    if r.returncode != 0 or not os.path.exists(os.path.join(BUILD, "b3536")):
        print("BUILD FAILED", r.stdout[-2000:], r.stderr[-2000:])
        sys.exit(1)
    print("built b3536 OK", flush=True)
    with open(os.path.join(BUILD, "b3536"), "rb") as f:
        print(f"b3536 binary sha={sha(f.read())}", flush=True)


if __name__ == "__main__":
    main()
