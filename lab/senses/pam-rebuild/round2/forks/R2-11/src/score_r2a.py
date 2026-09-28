#!/usr/bin/env python3
"""Score an R2-11 battery TSV (fork A or B).

Fork A TSV (15 cols): trial seq task fixture truth judgment conf disp
  correct percept_hex ops cited_sha artifact_sha equal ledger_hash
Fork B TSV (17 cols): trial seq task fixture truth judgment conf disp
  correct percept_hex ops render_sha div_runs div_bytes div_first_start
  div_first_len ledger_hash
"""
import sys

PAYLOAD = {  # render/cited payload bytes per task
    "colordisc": 128 * 64 * 3, "colorconst": 128 * 64 * 3,
    "shapetrans": 96 * 96 * 3, "pitchdisc": 12800 * 2,
    "timbredisc": 12800 * 2, "motiondir": 8 * 64 * 64 * 3,
}

def main():
    path = sys.argv[1]
    rows = [l.rstrip("\n").split("\t") for l in open(path)
            if l.startswith("trial\t")]
    fork = "A" if len(rows[0]) == 15 else "B"
    n = len(rows)
    correct = sum(int(r[8]) for r in rows)
    inst = [r for r in rows if r[7] == "INSTALL"]
    false_inst = sum(1 for r in inst if r[8] == "0")
    ops = sum(int(r[10]) for r in rows)
    pbytes = sum(PAYLOAD[r[2]] for r in rows)
    print("fork %s trials=%d accuracy=%d/%d=%.4f" % (fork, n, correct, n, correct / n))
    print("installs=%d false_installs=%d false_rate=%.6f" % (
        len(inst), false_inst, false_inst / n))
    print("ops_total=%d ops_mean=%.1f" % (ops, ops / n))
    print("payload_bytes_total=%d bytes_per_percept=%.1f" % (pbytes, pbytes / n))
    if fork == "A":
        eq1 = sum(1 for r in rows if r[13] == "1")
        eq0 = sum(1 for r in rows if r[13] == "0")
        eqm = sum(1 for r in rows if r[13] == "-1")
        print("KB-E1 equal=1:%d equal=0:%d noemit:%d" % (eq1, eq0, eqm))
    else:
        dr = sum(int(r[12]) for r in rows)
        db = sum(int(r[13]) for r in rows)
        print("div_runs_total=%d div_bytes_total=%d div_bytes_mean=%.1f" % (dr, db, db / n))

main()
