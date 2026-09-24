#!/usr/bin/env python3
"""crosscheck_phase0.py -- per-fixture agreement of FS-E2 independent
formation judgments vs FS-E1's frozen ledger judgments (b_ctrl).
Usage: crosscheck_phase0.py <fse1_ledger> <fs2_tsv>
"""
import struct, sys

def hdr(path):
    d = open(path, "rb").read(32)
    magic, task, index, fam = struct.unpack("<8I", d)[:4]
    assert magic == 0x52324658, path
    return task, index, fam

def main():
    ledger, tsv = sys.argv[1], sys.argv[2]
    e1 = {}
    for line in open(ledger):
        p = dict(kv.split("=", 1) for kv in line.strip().split(" ")
                 if "=" in kv and not kv.startswith("hash="))
        e1[p["fixture"]] = p["judgment"]
    agree = disagree = missing = 0
    disag_rows = []
    for line in open(tsv):
        p, task, judg, truth, correct = line.rstrip("\n").split("\t")
        t, i, f = hdr(p)
        fid = "r2fx_t%d_i%d_f%d" % (t, i, f)
        j1 = e1.get(fid)
        if j1 is None:
            missing += 1
            continue
        if j1 == judg:
            agree += 1
        else:
            disagree += 1
            disag_rows.append((fid, j1, judg, truth))
    print("agree=%d disagree=%d missing=%d" % (agree, disagree, missing))
    for r in disag_rows[:20]:
        print("  DISAGREE %s fse1=%s fs2=%s truth=%s" % r)

if __name__ == "__main__":
    main()
