#!/usr/bin/env python3
"""Finer bisect of thincert_old crash: decouple manifest entries vs builddir files."""
import hashlib, os, shutil, subprocess

TC = os.path.expanduser("~/workspace/certrebuild/work/thincert")
BASE = os.path.expanduser("~/workspace/reverify/work/cert/rv3/bisect2")
CLEAN = b'// RV3-P5 file\nfn main()void {\n    _zag_println("rv3-clean");\n}\n'
EV = b"byte_identical=1\nvaries_with_state=1\nexit_ok=1\nrebuild_ok=1\nruns=8\n"

def sha(b):
    return hashlib.sha256(b).hexdigest()

def build_case(tag, n_man, n_files):
    d = f"{BASE}/{tag}"
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d + "/builddir")
    entries = []
    for i in range(n_man):
        name = "f%03d.zag" % i
        body = b"// file %03d\n" % i + CLEAN
        if i < n_files:
            open(d + "/builddir/" + name, "wb").write(body)
        entries.append((name, sha(body)))
    open(d + "/plant.bin", "wb").write(b"")
    open(d + "/evidence.txt", "wb").write(EV)
    lines = ["M %s %s" % e for e in entries] + ["BIN plant.bin " + sha(b"")]
    open(d + "/MANIFEST.txt", "w").write("\n".join(lines) + "\n")
    return d

def trial(tag, n_man, n_files):
    d = build_case(tag, n_man, n_files)
    p = subprocess.run([TC + "/thincert_old", d + "/MANIFEST.txt", d + "/builddir",
                        d + "/plant.bin", d + "/evidence.txt", d + "/att.txt"],
                       capture_output=True, cwd=d, timeout=300)
    v = "?"
    if os.path.exists(d + "/att.txt"):
        for line in open(d + "/att.txt"):
            if line.startswith("verdict="):
                v = line.strip()
            if line.startswith("R1=FAIL"):
                v += " " + line.strip()[:40]
    print(f"{tag:28s} man={n_man:3d} files={n_files:3d} rc={p.returncode} {v} err={p.stderr.decode()[:40]!r}", flush=True)

for n in (70, 80, 90):
    trial(f"n{n}", n, n)
trial("man100_files3", 100, 3)
trial("man3_files100", 3, 100)
