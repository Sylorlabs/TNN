#!/usr/bin/env python3
"""Verify streaming ledgers by independent recompute (hashlib.sha256).
Usage: verify_ledger.py <streamdir>
"""
import json, glob, os, sys, hashlib

def main():
    d = sys.argv[1]
    ok_all = True
    for jf in sorted(glob.glob(os.path.join(d, "stream_*.jsonl"))):
        task = os.path.basename(jf)[7:-6]
        rows = [json.loads(l) for l in open(jf)]
        prev = bytes(32)
        ok = True
        for r in rows:
            tr = r["transition"].encode()
            exp = hashlib.sha256(prev + tr).hexdigest()
            if exp != r["chain"]:
                ok = False
                print("MISMATCH", task, r["ep"])
                break
            prev = bytes.fromhex(r["chain"])
        ledger = open(os.path.join(d, "ledger_%s.txt" % task)).read().strip()
        if prev.hex() != ledger:
            ok = False
            print("LEDGER HEAD MISMATCH", task)
        print("%s: %d episodes, ledger %s" % (task, len(rows), "OK" if ok else "FAIL"))
        ok_all = ok_all and ok
    print("ALL:", "OK" if ok_all else "FAIL")

if __name__ == "__main__":
    main()
