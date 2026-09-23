#!/usr/bin/env python3
"""xval_fsc.py — Python<->Zag cross-validation for R2-15.

Parses every fixture batch file, recomputes the four naive judgments with the
independent numpy mirror (same code as gen_fsc.py's verifier), and compares
against the vf/vg/af/ag fields recorded in the Zag hash-chained ledgers.
Any mismatch = the Zag mechanism disagrees with its own spec. Analysis only.
"""
import os
import struct
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.expanduser("~/workspace/tnn-lab"),
                                "senses/pam-rebuild/round2/fixtures"))
import gen_fsc as G

FIX = os.path.join(os.path.expanduser("~/workspace/tnn-lab"),
                   "senses/pam-rebuild/round2/fixtures/fsc")
EV = os.path.join(os.path.expanduser("~/workspace/tnn-lab"),
                  "senses/pam-rebuild/round2/forks/R2-15/evidence")


def trials_in(path):
    data = open(path, "rb").read()
    off, out = 0, []
    while off < len(data):
        (tlen,) = struct.unpack_from("<I", data, off)
        body = data[off + 4:off + 4 + tlen]
        assert body[:4] == b"FSC1"
        truth, fam, idx = struct.unpack_from("<BBI", body, 4)
        p = 10
        blobs = []
        for _ in range(4):
            (bl,) = struct.unpack_from("<I", body, p)
            p += 4
            blobs.append(body[p:p + bl])
            p += bl
        out.append((truth, fam, idx, blobs))
        off += 4 + tlen
    return out


def ledger_rows(path):
    rows = []
    for ln in open(path):
        if ln.startswith("e "):
            p = ln.split(" ")
            rows.append(tuple(int(x) for x in p[2:8]))  # truth,vf,vg,af,ag,inst
    return rows


def main():
    mism, total = 0, 0
    for fn in sorted(os.listdir(FIX)):
        if not fn.endswith(".fsc"):
            continue
        fam = fn.split("_")[1]
        for mode in (0, 1):
            base = fn[:-4]
            led = os.path.join(EV, f"ledger_m{mode}_{base}_p1.txt")
            if not os.path.exists(led):
                continue
            trs = trials_in(os.path.join(FIX, fn))
            rows = ledger_rows(led)
            assert len(trs) == len(rows), (fn, len(trs), len(rows))
            for (truth, tfam, idx, blobs), row in zip(trs, rows):
                vf = G.naive_shape(blobs[0])
                vg = G.naive_shape(blobs[1])
                af = G.naive_pitch(blobs[2])
                ag = G.naive_pitch(blobs[3])
                total += 1
                if (truth, vf, vg, af, ag) != row[:5]:
                    mism += 1
                    print("MISMATCH", fn, idx, (truth, vf, vg, af, ag), row[:5])
    print(f"xval: {total} trials compared, {mism} mismatches")
    sys.exit(1 if mism else 0)


if __name__ == "__main__":
    main()
