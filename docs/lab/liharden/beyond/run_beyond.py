#!/usr/bin/env python3
"""BEYOND probe driver (round 2): fixture bundle -> beyond_bin <mech> on stdin.
- Iterates corrob/fixtures (Crew B frozen set) + beyond/fixtures (BEYOND additions).
- Emits M|pid|k=v meta lines from meta.txt (skips META=NONE entries).
- Prepends ARCH|/REG|/SENT| lines from pins/ (pin2+registry2 for T4_supersede).
- Runs every mech x every fixture, twice (determinism check).
Prints TSV: case, mech, rep, verdict.
"""
import os, subprocess, sys

BIN = os.path.expanduser("~/workspace/liharden/beyond/work/beyond_bin")
FIX1 = os.path.expanduser("~/workspace/liharden/corrob/fixtures")
FIX2 = os.path.expanduser("~/workspace/liharden/beyond/fixtures")
PINS = os.path.expanduser("~/workspace/liharden/beyond/pins")
MECHS = ["base", "ch1", "ch2", "ch2b", "ch3", "ch4",
         "g1", "g4", "g6", "g7", "g9",
         "w11", "w12", "w3", "w6"]

def pin_lines(case):
    lines = []
    pin = "pin2.txt" if case == "T4_supersede" else "pin1.txt"
    reg = "registry2.txt" if case == "T4_supersede" else "registry.txt"
    for fn, prefix in ((pin, "ARCH"), (reg, "REG")):
        p = os.path.join(PINS, fn)
        if os.path.exists(p):
            for l in open(p):
                l = l.strip()
                if l:
                    lines.append(prefix + "|" + l)
    return lines

def bundle(casedir, case):
    out = pin_lines(case)
    need = open(os.path.join(casedir, "need.txt")).read().strip()
    out.append("NEED|" + need)
    urls = {}
    for line in open(os.path.join(casedir, "urls.txt")):
        line = line.strip()
        if not line or "|" not in line:
            continue
        pid, url = line.split("|", 1)
        urls[pid.strip()] = url.strip()
        out.append("U|%s|%s" % (pid.strip(), url.strip()))
    pdir = os.path.join(casedir, "pages")
    for fn in sorted(os.listdir(pdir)):
        if not fn.endswith(".txt"):
            continue
        pid = fn[:-4]
        lines = [l.rstrip("\n") for l in open(os.path.join(pdir, fn))]
        out.append("P|" + pid)
        for l in lines[1:]:
            if l.strip():
                out.append(l.strip())
    # meta lines (after pages so page ids exist)
    mpath = os.path.join(casedir, "meta.txt")
    if os.path.exists(mpath):
        for line in open(mpath):
            line = line.strip()
            if not line or "|" not in line:
                continue
            pid, rest = line.split("|", 1)
            rest = rest.strip()
            if rest and rest != "META=NONE":
                out.append("M|%s|%s" % (pid.strip(), rest))
    return ("\n".join(out) + "\n").encode()

def run(mech, data):
    r = subprocess.run([BIN, mech], input=data, capture_output=True, timeout=30)
    if r.returncode != 0:
        return "ERROR rc=%d err=%s" % (r.returncode, r.stderr.decode()[-200:])
    return r.stdout.decode().strip()

def cases_in(d):
    return [("X:" + d, os.path.join(d, x)) for x in sorted(os.listdir(d))
            if os.path.isdir(os.path.join(d, x))] if os.path.isdir(d) else []

def main():
    todo = []
    for d in (FIX1, FIX2):
        for x in sorted(os.listdir(d)):
            if os.path.isdir(os.path.join(d, x)):
                src = "corrob" if d == FIX1 else "beyond"
                todo.append((src, x, os.path.join(d, x)))
    print("src\tcase\tmech\trep\tverdict")
    for src, case, cdir in todo:
        data = bundle(cdir, case)
        for mech in MECHS:
            outs = [run(mech, data), run(mech, data)]
            assert outs[0] == outs[1], "NONDETERMINISM %s %s: %r vs %r" % (case, mech, outs[0], outs[1])
            for rep, o in enumerate(outs, 1):
                print("%s\t%s\t%s\t%d\t%s" % (src, case, mech, rep, o))

if __name__ == "__main__":
    main()
