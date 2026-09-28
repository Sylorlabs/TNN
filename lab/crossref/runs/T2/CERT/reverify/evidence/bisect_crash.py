#!/usr/bin/env python3
"""Bisect thincert_old crash threshold on manifest entry count."""
import hashlib, os, shutil, subprocess

ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
TC = os.path.expanduser("~/workspace/certrebuild/work/thincert")
BASE = os.path.expanduser("~/workspace/reverify/work/cert/rv3/bisect")
CLEAN = b'// RV3-P5 file\nfn main()void {\n    _zag_println("rv3-clean");\n}\n'
EV = b"byte_identical=1\nvaries_with_state=1\nexit_ok=1\nrebuild_ok=1\nruns=8\n"

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def build_case(n):
    d = f"{BASE}/n{n}"
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d + "/builddir")
    entries = []
    for i in range(n):
        name = "f%03d.zag" % i
        body = b"// file %03d\n" % i + CLEAN
        open(d + "/builddir/" + name, "wb").write(body)
        entries.append((name, sha(d + "/builddir/" + name)))
    open(d + "/builddir/buildme.zag", "wb").write(CLEAN)
    subprocess.run([ZNC, "build", d + "/builddir/buildme.zag", "-o", d + "/plant.bin"],
                   capture_output=True, cwd=d + "/builddir", check=True)
    os.remove(d + "/builddir/buildme.zag")
    open(d + "/evidence.txt", "wb").write(EV)
    lines = ["M %s %s" % e for e in entries] + ["BIN plant.bin " + sha(d + "/plant.bin")]
    open(d + "/MANIFEST.txt", "w").write("\n".join(lines) + "\n")
    return d

for n in (3, 12, 13, 20, 64, 100, 127, 128):
    d = build_case(n)
    p = subprocess.run([TC + "/thincert_old", d + "/MANIFEST.txt", d + "/builddir",
                        d + "/plant.bin", d + "/evidence.txt", d + "/att.txt"],
                       capture_output=True, cwd=d, timeout=300)
    v = "?"
    if os.path.exists(d + "/att.txt"):
        for line in open(d + "/att.txt"):
            if line.startswith("verdict="):
                v = line.strip()
    print(f"n={n:3d} rc={p.returncode} {v} stderr={p.stderr.decode()[:60]!r}")
