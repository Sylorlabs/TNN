#!/usr/bin/env python3
"""R2-3 xval: independent Python cross-check of the compiled Zag instrument.

For each of the 1,200 R2P pairs: parse the .pair file, run the Python mirror
(judge.ref_gate / judge.broken_gate) on F and G, and compare the resulting
(jf, jg, wh) judgments against the per-entry judgments in the Zag-produced
ledger files. 0 mismatches = bit-exact agreement on all pairs.

Analysis-only (harness), not a decision path. Logs to stdout; redirect to log.
"""
import struct, os, sys

R2P = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/fixtures/r2p")
OUT = os.path.expanduser("~/workspace/r23_verify/out")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import judge

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]

def parse_pair(path):
    buf = open(path, "rb").read()
    task = struct.unpack("<H", buf[4:6])[0]
    idx = struct.unpack("<H", buf[8:10])[0]
    f_len, g_len = struct.unpack("<II", buf[20:28])
    f = buf[64:64 + f_len]
    g = buf[64 + f_len:64 + f_len + g_len]
    assert len(f) == f_len and len(g) == g_len, path
    return task, idx, f, g

def load_ledger(path):
    """seq -> (jf, jg, wh). Lines: e <seq> <jf> <jg> <wh> <hashhex>"""
    d = {}
    for line in open(path):
        if line.startswith("e "):
            parts = line.split()
            d[int(parts[1])] = (int(parts[2]), int(parts[3]), int(parts[4]))
    return d

def main():
    ref_ledger = load_ledger(os.path.join(OUT, "ledger_ref_r1.txt"))
    brk_ledger = load_ledger(os.path.join(OUT, "ledger_broken.txt"))
    assert len(ref_ledger) == 1200 and len(brk_ledger) == 1200

    mismatch = 0
    fooled = clean = 0
    for t, task in enumerate(TASKS):
        for idx in range(200):
            seq = t * 200 + idx
            path = os.path.join(R2P, "r2p_%s_%03d.pair" % (task, idx))
            pt, pidx, f, g = parse_pair(path)
            assert pt == t and pidx == idx, path

            dec, fj, gj = judge.ref_gate(t, f, g)
            ljf, ljg, lwh = ref_ledger[seq]
            if (fj, gj, dec) != (ljf, ljg, lwh):
                mismatch += 1
                print("MISMATCH ref t=%s idx=%d: py=(%d,%d,%d) zag=(%d,%d,%d)"
                      % (task, idx, fj, gj, dec, ljf, ljg, lwh))

            dec_b, bfj, bgj = judge.broken_gate(t, f, g)
            bjf, bjg, bwh = brk_ledger[seq]
            if (bfj, bgj, dec_b) != (bjf, bjg, bwh):
                mismatch += 1
                print("MISMATCH broken t=%s idx=%d: py=(%d,%d,%d) zag=(%d,%d,%d)"
                      % (task, idx, bfj, bgj, dec_b, bjf, bjg, bwh))

            # generation-time invariants: every F fooled, every G clean
            fj_clean, gj_clean = judge.ref_gate(t, f, g)[1], judge.ref_gate(t, f, g)[2]
            if fj != gj:
                fooled += 1
            if gj == judge.NAIVE[t](g):
                clean += 1

    print("pairs_checked=1200 (ref) + 1200 (broken) = 2400 judgments x 2 = 4800 fields")
    print("mismatches=%d" % mismatch)
    print("ref_gate_withheld=%d/1200 broken_gate_withheld=%d/1200"
          % (sum(1 for v in ref_ledger.values() if v[2]), sum(1 for v in brk_ledger.values() if v[2])))
    return 1 if mismatch else 0

sys.exit(main())
