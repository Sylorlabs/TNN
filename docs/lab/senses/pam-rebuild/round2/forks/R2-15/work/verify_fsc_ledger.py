#!/usr/bin/env python3
"""verify_fsc_ledger.py — independent hash-chain verification for R2-15 ledgers.

Recomputes h0 = SHA256("FSC-LEDGER-v1" || mode || famfile) and each entry
h_{k+1} = SHA256(h_k || seq_BE4 || truth || vf || vg || af || ag || inst || sym),
comparing against the recorded hex hashes and the tail 'final' line.
Reports per-ledger OK/FAIL and entry counts. Analysis only; all decisions are Zag.
"""
import hashlib
import sys


def verify(path):
    lines = open(path).read().splitlines()
    assert lines[0] == "FSC-LEDGER-v1", path
    mode = famfile = None
    for ln in lines[1:3]:
        k, v = ln.split("=", 1)
        if k == "mode":
            mode = v
        elif k == "famfile":
            famfile = v
    h = hashlib.sha256(("FSC-LEDGER-v1" + mode + famfile).encode()).digest()
    n = 0
    for ln in lines:
        if not ln.startswith("e "):
            continue
        p = ln.split(" ")
        seq, truth, vf, vg, af, ag, inst, sym, hx = (
            int(p[1]), int(p[2]), int(p[3]), int(p[4]),
            int(p[5]), int(p[6]), int(p[7]), int(p[8]), p[9])
        body = (h + seq.to_bytes(4, "big")
                + bytes([truth, vf, vg, af, ag, inst, sym]))
        h = hashlib.sha256(body).digest()
        assert h.hex() == hx, (path, seq, h.hex(), hx)
        n += 1
    tail = [ln for ln in lines if ln.startswith("final=")][0].split("=", 1)[1]
    assert tail == h.hex(), (path, "tail mismatch")
    return n


if __name__ == "__main__":
    bad = 0
    for path in sys.argv[1:]:
        try:
            n = verify(path)
            print(f"OK {path} ({n} entries)")
        except AssertionError as e:
            bad += 1
            print(f"FAIL {path}: {e}")
    print("ALL CHAINS VALID" if bad == 0 else f"{bad} FAILURES")
    sys.exit(1 if bad else 0)
