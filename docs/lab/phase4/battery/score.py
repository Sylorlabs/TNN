#!/usr/bin/env python3
"""Phase-4 strict scorer: exact R-line sequence match + FNV chain recomputation.
Usage: score.py <results-dir> ; exits 0 iff every probe passes."""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from expectations import expectations

CHAIN_RE = re.compile(r"^R chain [0-9a-f]{16}$")

def fnv_chain(lines):
    h = 14695981039346656037
    for l in lines:
        for byte in l + b"\n":
            h = ((h ^ byte) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return "%016x" % h

def score_probe(resdir, pid, expected):
    path = os.path.join(resdir, pid + ".out")
    raw = open(path, "rb").read().split(b"\n")
    lines = [l for l in raw if l != b""]
    if not lines or not CHAIN_RE.match(lines[-1].decode()):
        return False, "missing/malformed chain line"
    body, chainline = lines[:-1], lines[-1].decode()
    if fnv_chain(body) != chainline.split()[-1]:
        return False, "chain mismatch (transcript tampered or nondeterministic emit)"
    rlines = [l.decode() for l in body if l.startswith(b"R ")]
    exp = expected[pid]
    if rlines != exp:
        for i, (g, e) in enumerate(zip(rlines, exp)):
            if g != e:
                return False, f"R-line {i} differs: got {g!r} want {e!r}"
        return False, f"R-line count differs: got {len(rlines)} want {len(exp)}"
    return True, "ok"

def main():
    resdir = sys.argv[1]
    exp = expectations()
    fails = []
    for pid in sorted(exp):
        ok, msg = score_probe(resdir, pid, exp)
        print(f"{pid}: {'PASS' if ok else 'FAIL'} — {msg}")
        if not ok:
            fails.append(pid)
    # kill-bar adjudication (frozen PREREG.md section 6)
    bars = {
        "K1 name-lookup discrimination (s1,s2,s3)": ["s1", "s2", "s3"],
        "K2 leakage (s2,s3,s4,s6)": ["s2", "s3", "s4", "s6"],
        "K3 withhold (s4,s5,s8)": ["s4", "s5", "s8"],
        "K4 belief (s5)": ["s5"],
        "K5 correction (s7)": ["s7"],
    }
    print()
    allok = True
    for bar, probes in bars.items():
        ok = all(p not in fails for p in probes)
        allok = allok and ok
        print(f"{bar}: {'HOLD' if ok else 'FIRED'}")
    print()
    print("BATTERY: " + ("ALL PASS" if not fails else f"FAILURES {fails}"))
    sys.exit(0 if not fails else 1)

if __name__ == "__main__":
    main()
