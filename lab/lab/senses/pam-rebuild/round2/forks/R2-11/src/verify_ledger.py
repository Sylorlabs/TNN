#!/usr/bin/env python3
"""Verify an R2-11 hash-chained ledger.

Ledger line format (written by the Zag driver):
  seq \t task \t fixture \t judgment \t conf \t disp \t percept_hex \t prev_hash \t hash=<64hex>

Checks:
  1. each line's hash == sha256(core_line + "\n") where core_line is the
     line up to (not incl.) "\thash=".
  2. each line's prev_hash == previous line's hash ("0"*64 for the first).
  3. recompute the expected core from the TSV trial row and compare
     (seq, task, fixture, judgment, conf, disp, percept_hex must match).
Usage: verify_ledger.py <ledger.tsv> <trials.tsv>
"""
import hashlib, sys

def main():
    ledger_path, tsv_path = sys.argv[1], sys.argv[2]
    trials = {}
    DISPC = {"INSTALL": "0", "NOTE": "1", "DISCARD": "2"}
    for line in open(tsv_path):
        if not line.startswith("trial\t"):
            continue
        r = line.rstrip("\n").split("\t")
        # A: 15 cols, B: 17 cols; common prefix cols 1..9 (0-indexed)
        seq, task, fixture = r[1], r[2], r[3]
        judg, conf, disp, phex = r[5], r[6], DISPC.get(r[7], r[7]), r[9]
        trials[seq] = (task, fixture, judg, conf, disp, phex)
    prev = "0" * 64
    n = 0
    bad = 0
    for line in open(ledger_path):
        line = line.rstrip("\n")
        if not line:
            continue
        core, tag = line.rsplit("\thash=", 1)
        h = hashlib.sha256((core + "\n").encode()).hexdigest()
        if h != tag:
            print("HASH MISMATCH line %d" % (n + 1)); bad += 1
        parts = core.split("\t")
        seq = parts[0]
        if parts[7] != prev:
            print("CHAIN BREAK line %d" % (n + 1)); bad += 1
        if seq in trials:
            t, fx, j, c, d, ph = trials[seq]
            exp = "\t".join([seq, t, fx, j, c, d, ph, prev])
            if exp != core:
                print("CORE MISMATCH vs TSV line %d" % (n + 1)); bad += 1
        else:
            print("SEQ %s not in TSV" % seq); bad += 1
        prev = tag
        n += 1
    print("ledger lines: %d, problems: %d, head=%s" % (n, bad, prev[:16]))
    return 1 if bad else 0

sys.exit(main())
