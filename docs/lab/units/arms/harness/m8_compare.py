#!/usr/bin/env python3
# m8_compare.py — compare M8 artifact dirs byte-for-byte across all runs.
# Usage: m8_compare.py <dir>...  (the ten run dirs: 5 perturbations x 2 reruns)
# Exit 0 + "M8GATE PASS" iff every compared byte is identical across all dirs.
# Exit 1 + "M8GATE FAIL" with first-difference localization otherwise.
import sys, os, hashlib

FILES = ["store_hashes.txt", "store_chain.txt", "ledger.bin",
         "ledger_chain.txt", "alloc_trace.txt", "stdout.txt", "stderr.txt"]

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()

def main(dirs):
    names = sys.argv[1:]  # labels = the dir paths as given
    ok = True
    for fn in FILES:
        base = os.path.join(dirs[0], fn)
        if not os.path.exists(base):
            print(f"MISSING {names[0]}/{fn}")
            ok = False
            continue
        h0 = sha(base)
        for d, nm in zip(dirs[1:], names[1:]):
            p = os.path.join(d, fn)
            if not os.path.exists(p):
                print(f"MISSING {nm}/{fn}")
                ok = False
                continue
            h = sha(p)
            if h != h0:
                ok = False
                print(f"DIFF {fn}: {names[0]}={h0[:16]} {nm}={h[:16]}")
                if fn == "store_hashes.txt":
                    # localize to chunk
                    a = open(base).read().splitlines()
                    b = open(p).read().splitlines()
                    for i, (x, y) in enumerate(zip(a, b)):
                        if x != y:
                            print(f"  first differing chunk line {i}:")
                            print(f"    {names[0]}: {x}")
                            print(f"    {nm}: {y}")
                            break
    print("M8GATE " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: m8_compare.py <dir>... (at least 2)")
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
