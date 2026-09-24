#!/usr/bin/env python3
"""RT4 RT-D edge-probe runner (HARNESS ONLY). Runs each probe through its
target binary: LOGIC -> logic_bin, R12 -> r12_v4. Informational only.
Usage: run_rtd.py <rtd_edge.tsv> <outdir>
"""
import subprocess, sys, os

BUILD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
LOGIC = os.path.join(BUILD, "logic_bin")
R12 = os.path.join(BUILD, "r12_v4")

def run_bin(path, arg):
    r = subprocess.run([path, arg], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("%s failed rc=%d: %s" % (path, r.returncode, r.stderr[:500]))
    return r.stdout

def main():
    corpus, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    probes = [ln.rstrip("\n").split("\t") for ln in open(corpus, encoding="utf-8")]
    for p in probes:
        assert len(p) == 6, p[0]

    loglines = ["%s\t%s\t%s\t0" % (p[0], p[3], p[4]) for p in probes if p[2] == "LOGIC"]
    r12lines = ["%s\t%s\t\t%s" % (p[0], p[3], p[4]) for p in probes if p[2] == "R12"]
    login = os.path.join(outdir, "logic_in.tsv")
    r12in = os.path.join(outdir, "r12_in.tsv")
    open(login, "w").write("\n".join(loglines) + "\n")
    open(r12in, "w").write("\n".join(r12lines) + "\n")
    logout = run_bin(LOGIC, login)
    r12out = run_bin(R12, r12in)
    open(os.path.join(outdir, "logic_out.txt"), "w").write(logout)
    open(os.path.join(outdir, "r12_out.txt"), "w").write(r12out)
    res = {}
    for ln in logout.splitlines():
        q = ln.split(" ", 2)
        res[q[0]] = ("LOGIC", q[1], q[2] if len(q) > 2 else "")
    for ln in r12out.splitlines():
        q = ln.split(" ", 2)
        res[q[0]] = ("R12", q[1], q[2] if len(q) > 2 else "")
    out = []
    for p in probes:
        tgt, tag, proof = res[p[0]]
        out.append("%s\t%s\t%s\t%s\t%s\t%s\t%s" % (p[0], p[1], tgt, tag, proof, p[5], p[3][:50]))
    open(os.path.join(outdir, "probes.tsv"), "w").write("\n".join(out) + "\n")
    print("probes=%d" % len(out))

if __name__ == "__main__":
    main()
