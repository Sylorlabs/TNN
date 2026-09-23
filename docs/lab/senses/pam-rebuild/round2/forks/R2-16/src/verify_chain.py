#!/usr/bin/env python3
"""verify_chain.py -- verify the hash chain of an R2-14 ledger file.

Each ledger line ends with " hash=<hex64>" where
  hash = hex(sha256(raw(prev_hash) + content)),
content = the line's bytes before " hash=", prev_hash starts as 64 ASCII '0'
characters. Reports OK/FAIL plus the failing line number.
"""
import sys, hashlib

def verify(path):
    prev = b"0" * 64
    n = 0
    with open(path, "rb") as f:
        for ln, raw in enumerate(f, 1):
            line = raw.rstrip(b"\n")
            if not line:
                continue
            i = line.rfind(b" hash=")
            assert i > 0, "line %d: no hash tag" % ln
            content, h = line[:i], line[i + 6:]
            calc = hashlib.sha256(bytes.fromhex(prev.decode()) + content).hexdigest()
            if calc.encode() != h:
                return False, ln, h.decode(), calc
            prev = h
            n += 1
    return True, n, None, None

def main():
    for path in sys.argv[1:]:
        ok, a, b, c = verify(path)
        if ok:
            print("%s: CHAIN-OK lines=%d" % (path, a))
        else:
            print("%s: CHAIN-FAIL at line %d got=%s want=%s" % (path, a, b, c))

if __name__ == "__main__":
    main()
