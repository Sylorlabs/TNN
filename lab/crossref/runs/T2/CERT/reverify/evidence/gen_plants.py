#!/usr/bin/env python3
"""RV3 plant battery generator (T2-CERT adversarial re-verification).

Generates 5 deterministic adversarial plants (+off-by-one subcases) as
thincert cases: builddir/ + MANIFEST.txt + plant.bin + evidence.txt.
Python is glue only (file generation); all verdicts come from the pinned
Zag certifier binaries (thincert_old / thincert_new).
Zero RNG: every byte is constructed deterministically.
"""
import hashlib, os, shutil, subprocess, sys

ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
ROOT = os.path.expanduser("~/workspace/reverify/work/cert/rv3")

CLEAN_ZAG = b"""// RV3 clean module: allowlisted tokens only, no loops, no structs, no nio_ defs.
fn main()void {
    _zag_println("rv3-clean");
}
"""

EV_FULL = b"""byte_identical=1
varies_with_state=1
exit_ok=1
rebuild_ok=1
runs=8
"""

EMPTY_SHA = hashlib.sha256(b"").hexdigest()

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()

def w(p, data):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(data)

def fresh(d):
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d + "/builddir")

def manifest(d, m_entries, bin_name, bin_sha):
    lines = []
    for name, h in m_entries:
        lines.append("M %s %s" % (name, h))
    lines.append("BIN %s %s" % (bin_name, bin_sha))
    w(d + "/MANIFEST.txt", ("\n".join(lines) + "\n").encode())

def build_clean_module(d):
    """Compile the clean module once with the pinned toolchain; return bin path."""
    src = d + "/builddir/variation.zag"
    w(src, CLEAN_ZAG)
    out = d + "/clean.bin"
    r = subprocess.run([ZNC, "build", src, "-o", out], capture_output=True, cwd=d + "/builddir")
    if r.returncode != 0 or not os.path.exists(out):
        print("BUILD FAILED", r.stderr.decode()[:500]); sys.exit(1)
    return out

# ---------------- P1: empty-input plant ----------------
d = ROOT + "/p1_empty"
fresh(d)
w(d + "/builddir/variation.zag", b"")
w(d + "/plant.bin", b"")
w(d + "/evidence.txt", EV_FULL)
manifest(d, [("variation.zag", EMPTY_SHA)], "plant.bin", EMPTY_SHA)

# ---------------- P2: max-size / oversize module ----------------
for tag, size in (("p2a_exact", 4194304), ("p2b_over", 4194305)):
    d = ROOT + "/" + tag
    fresh(d)
    binp = build_clean_module(d)
    bincopy = d + "/plant.bin"
    shutil.copy(binp, bincopy)
    pad_len = size - len(CLEAN_ZAG)
    # deterministic '//' comment padding (comments are stripped before token scans)
    pad = b"// PAD\n"
    reps, rem = divmod(pad_len, len(pad))
    body = CLEAN_ZAG + pad * reps + b"//" + b"X" * (rem - 2) + b"\n" if rem >= 3 else CLEAN_ZAG + pad * reps
    # exact-size fixup
    while len(body) < size:
        body += b"// Q\n"
    body = body[:size]
    assert len(body) == size, (tag, len(body))
    w(d + "/builddir/variation.zag", body)
    w(d + "/evidence.txt", EV_FULL)
    manifest(d, [("variation.zag", sha(d + "/builddir/variation.zag"))], "plant.bin", sha(bincopy))

# ---------------- P3: malformed / truncated evidence ----------------
p3mods = {
    "p3a_truncated_ev": b"byte_identical=1\nvar",
    "p3b_runs7": EV_FULL.replace(b"runs=8", b"runs=7"),
    "p3c_ident0": EV_FULL.replace(b"byte_identical=1", b"byte_identical=0"),
}
for tag, ev in p3mods.items():
    d = ROOT + "/" + tag
    fresh(d)
    binp = build_clean_module(d)
    bincopy = d + "/plant.bin"
    shutil.copy(binp, bincopy)
    w(d + "/evidence.txt", ev)
    manifest(d, [("variation.zag", sha(d + "/builddir/variation.zag"))], "plant.bin", sha(bincopy))
# p3d: malformed manifest (M line without hash)
d = ROOT + "/p3d_bad_manifest"
fresh(d)
binp = build_clean_module(d)
shutil.copy(binp, d + "/plant.bin")
w(d + "/evidence.txt", EV_FULL)
w(d + "/MANIFEST.txt", b"M variation.zag\nBIN plant.bin " + sha(d + "/plant.bin").encode() + b"\n")

# ---------------- P4: missing-input (inconclusive-row reasoning) ----------------
# p4a: manifest lists a module that does not exist in builddir
d = ROOT + "/p4a_missing_module"
fresh(d)
w(d + "/builddir/other.zag", CLEAN_ZAG)
w(d + "/plant.bin", b"")
w(d + "/evidence.txt", EV_FULL)
manifest(d, [("ghost.zag", "ab" * 32), ("other.zag", sha(d + "/builddir/other.zag"))], "plant.bin", EMPTY_SHA)
# p4b: evidence file missing entirely
d = ROOT + "/p4b_missing_evidence"
fresh(d)
binp = build_clean_module(d)
shutil.copy(binp, d + "/plant.bin")
# no evidence.txt written
manifest(d, [("variation.zag", sha(d + "/builddir/variation.zag"))], "plant.bin", sha(d + "/plant.bin"))
# p4c: manifest missing entirely -> certifier usage-IO error (exit 2)
d = ROOT + "/p4c_missing_manifest"
fresh(d)
w(d + "/builddir/variation.zag", CLEAN_ZAG)
w(d + "/plant.bin", b"")
w(d + "/evidence.txt", EV_FULL)
# no MANIFEST.txt

# ---------------- P5: threshold off-by-one ----------------
def many_files(d, n):
    entries = []
    for i in range(n):
        name = "f%03d.zag" % i
        body = b"// RV3-P5 file %03d\n" % i + CLEAN_ZAG
        w(d + "/builddir/" + name, body)
        entries.append((name, sha(d + "/builddir/" + name)))
    return entries

# p5a: exactly 128 files / 128 manifest entries (boundary PASS expected)
d = ROOT + "/p5a_128"
fresh(d)
entries = many_files(d, 128)
w(d + "/builddir/buildme.zag", CLEAN_ZAG)
r = subprocess.run([ZNC, "build", d + "/builddir/buildme.zag", "-o", d + "/plant.bin"],
                   capture_output=True, cwd=d + "/builddir")
assert r.returncode == 0
os.remove(d + "/builddir/buildme.zag")
w(d + "/evidence.txt", EV_FULL)
manifest(d, entries, "plant.bin", sha(d + "/plant.bin"))

# p5b: 129 files / 129 entries (boundary FAIL expected)
d = ROOT + "/p5b_129"
fresh(d)
entries = many_files(d, 129)
w(d + "/builddir/buildme.zag", CLEAN_ZAG)
r = subprocess.run([ZNC, "build", d + "/builddir/buildme.zag", "-o", d + "/plant.bin"],
                   capture_output=True, cwd=d + "/builddir")
assert r.returncode == 0
os.remove(d + "/builddir/buildme.zag")
w(d + "/evidence.txt", EV_FULL)
manifest(d, entries, "plant.bin", sha(d + "/plant.bin"))

# p5c: binary size cap 33554431 (at) vs 33554432 (over)
for tag, bsize in (("p5c1_bin_at_cap", 33554431), ("p5c2_bin_over_cap", 33554432)):
    d = ROOT + "/" + tag
    fresh(d)
    binp = build_clean_module(d)
    with open(binp, "rb") as f:
        base = f.read()
    assert len(base) < bsize
    with open(d + "/plant.bin", "wb") as f:
        f.write(base)
        f.write(b"\x00" * (bsize - len(base)))
    w(d + "/evidence.txt", EV_FULL)
    manifest(d, [("variation.zag", sha(d + "/builddir/variation.zag"))], "plant.bin", sha(d + "/plant.bin"))

print("generated:", sorted(os.listdir(ROOT)))
