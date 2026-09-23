#!/usr/bin/env python3
"""Verify an R2-3 hash-chained ledger: recompute the chain, check final hash."""
import hashlib, sys

def main(path):
    lines = open(path).read().splitlines()
    assert lines[0] == "R2P-LEDGER-v1", lines[0]
    gate = lines[1].split("=", 1)[1]
    n = int(lines[2].split("=", 1)[1])
    h = hashlib.sha256(("R2P-LEDGER-v1" + gate).encode()).digest()
    count = 0
    for ln in lines[3:]:
        if ln.startswith("final="):
            final_claimed = ln.split("=", 1)[1]
            break
        assert ln.startswith("e "), ln
        _, seq, jf, jg, wh, hh = ln.split()
        seq, jf, jg, wh = int(seq), int(jf), int(jg), int(wh)
        h = hashlib.sha256(h + seq.to_bytes(4, "big") + bytes([jf, jg, wh])).digest()
        assert h.hex() == hh, "chain break at seq %d" % seq
        count += 1
    else:
        raise AssertionError("no final line")
    assert h.hex() == final_claimed, "final hash mismatch"
    if count != n:
        print("LEDGER CHAIN OK but count %d != header n=%d (incomplete run)" % (count, n))
    else:
        print("LEDGER OK: %d entries, gate=%s, final=%s" % (count, gate, h.hex()))

if __name__ == "__main__":
    main(sys.argv[1])
