#!/usr/bin/env python3
"""Red-team scorer: each attack PASSES iff the implementation withstood it
(expected R-lines = the SECURE behavior). Any deviation = K7 FIRES.
Usage: score_rt.py <results-dir>"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from expectations_rt import rt_expectations

CHAIN_RE = re.compile(r"^R chain [0-9a-f]{16}$")

def fnv_chain(lines):
    h = 14695981039346656037
    for l in lines:
        for byte in l + b"\n":
            h = ((h ^ byte) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return "%016x" % h

def main():
    resdir = sys.argv[1]
    exp = rt_expectations()
    kills = []
    for pid in sorted(exp):
        path = os.path.join(resdir, pid + ".out")
        raw = open(path, "rb").read().split(b"\n")
        lines = [l for l in raw if l != b""]
        ok, msg = True, "withstood"
        if not lines or not CHAIN_RE.match(lines[-1].decode()):
            ok, msg = False, "missing/malformed chain line"
        else:
            body, chainline = lines[:-1], lines[-1].decode()
            if fnv_chain(body) != chainline.split()[-1]:
                ok, msg = False, "chain mismatch"
            else:
                rlines = [l.decode() for l in body if l.startswith(b"R ")]
                want = exp[pid]
                if rlines != want:
                    ok = False
                    for i, (g, e) in enumerate(zip(rlines, want)):
                        if g != e:
                            msg = f"KILL at R-line {i}: got {g!r} want {e!r}"
                            break
                    else:
                        msg = f"KILL: R-line count {len(rlines)} != {len(want)}"
        print(f"{pid}: {'WITHSTOOD' if ok else 'KILL'} — {msg}")
        if not ok:
            kills.append(pid)
    print()
    if kills:
        print(f"K7 FIRES — red team killed the claim via: {kills}")
        sys.exit(1)
    print("K7 HOLDS — all 6 red-team attacks failed to kill the claim")
    sys.exit(0)

if __name__ == "__main__":
    main()
