#!/usr/bin/env python3
"""Independently verify the R2-1 hash-chained ledger (B6).

Reconstructs the canonical record for each trial from output fields + fixture
bytes, recomputes SHA-256, and checks it matches the reported chain hash.
Also verifies the chain links (prev == previous chain).
"""
import csv, os, sys, struct, hashlib

FORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
EV = os.path.join(FORK, "evidence", "battery_run1")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]

def geom_str(t, f):
    if t in (0, 1):
        return "64x32x3" if f == 0 else "32x16x3"
    if t == 2:
        return "48x48x3" if f == 0 else "24x24x3"
    if t == 3:
        return "2160s16@4kHz"
    if t == 4:
        return "4000s16@8kHz"
    return "8f24x24g"

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    results = list(csv.DictReader(open(os.path.join(EV, "%s_results.csv" % mode))))
    # chain file: trial_idx fixture_id chain_hash
    chain_lines = open(os.path.join(EV, "%s_chain.txt" % mode)).read().strip().split("\n")
    assert len(results) == 10000 and len(chain_lines) == 10000
    prev = "00" * 32
    bad = 0
    for i, r in enumerate(results):
        idx = r["trial_idx"]
        fid = r["fixture_id"]
        fx = r["fixture_path"] if "fixture_path" in r else None
        # fixture path from trial index
        # (results.csv doesn't have fixture_path; look it up)
        # Actually run_battery.py didn't write fixture_path. Reconstruct:
        # fixture_id -> suite/<fid>.r2a
        fpath = os.path.join(FORK, "suite", fid + ".r2a")
        b = open(fpath, "rb").read()
        assert b[:4] == b"R2A1"
        taskidx, flen = struct.unpack("<II", b[4:12])
        goff = 12 + flen
        (glen,) = struct.unpack("<I", b[goff:goff+4])
        task = TASKS[taskidx]
        assert r["task"] == task, (r["task"], task)
        # parse tests
        tstr = r.get("tests", "")
        # tests field not in results.csv! run_battery didn't capture it.
        # Need to re-derive T1/T2 from decision? No.
        # Actually the binary outputs "tests=T1_formation:PASS;T2_disjoint:PASS"
        # but run_battery.py parse_output captures it as d["tests"].
        # I didn't write it to CSV. Let me check.
        print("ERROR: tests field not in CSV, cannot verify", file=sys.stderr)
        return 1

if __name__ == "__main__":
    main()
