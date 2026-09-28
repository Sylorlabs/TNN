#!/usr/bin/env python3
"""Independent verification of attack_gate.zag's sha256 decision ledger.
Recomputes h_{n+1} = sha256(h_n || raw_line || decision_byte) from the
records file and the gate's decision output, using Python's hashlib
(independent of the Zag ns_sha256 implementation)."""
import hashlib, sys

def main(rec_path, gate_out_path):
    recs = {}
    with open(rec_path) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.strip():
                recs[line.split("|")[0]] = line
    h = bytes(32)
    n = 0
    decisions = {}
    for line in open(gate_out_path):
        line = line.rstrip("\n")
        if not line or line.startswith("LEDGER_HEAD") or line.startswith("N=") \
           or line.startswith("INSTALLS") or line.startswith("FALSE_") \
           or line.startswith("CONFLICTS"):
            continue
        parts = line.split("|")
        name, prog, admit, dec, wrong = parts[0], parts[1], parts[2], parts[3], parts[4]
        raw = recs[name]
        h = hashlib.sha256(h + raw.encode() + dec.encode()).digest()
        decisions[name] = (prog, admit, dec, wrong)
        n += 1
    # extract claimed head
    claimed = None
    for line in open(gate_out_path):
        if line.startswith("LEDGER_HEAD="):
            claimed = line.strip().split("=")[1]
    print(f"trials chained: {n}")
    print(f"recomputed head: {h.hex()}")
    print(f"gate head:       {claimed}")
    print("LEDGER " + ("VERIFIED" if h.hex() == claimed else "MISMATCH"))
    return h.hex() == claimed

if __name__ == "__main__":
    ok = main(sys.argv[1], sys.argv[2])
    sys.exit(0 if ok else 1)
