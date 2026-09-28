#!/usr/bin/env python3
"""B4 (no-interference) and KB-E2 checks for R2-11.

B4: percepts (percept_hex) and dispositions (judgment, conf, disp) must be
byte-identical between emit-on and emit-off runs, per trial.
KB-E2: no empty/phantom/unowned emission:
  - every emit-on trial has a real cited/render SHA (not "-")
  - fork A: equal=1 on every emit-on trial
  - every ledger line's seq exists in the TSV (no phantom ledger entries)

Usage: check_b4_kbe2.py <on.tsv> <off.tsv> <ledger.tsv>
"""
import sys

def load(path):
    return [l.rstrip("\n").split("\t") for l in open(path)
            if l.startswith("trial\t")]

def main():
    on_p, off_p, led_p = sys.argv[1], sys.argv[2], sys.argv[3]
    on, off = load(on_p), load(off_p)
    assert len(on) == len(off) == 10000, (len(on), len(off))
    fork = "A" if len(on[0]) == 15 else "B"

    # B4: compare judgment/conf/disp/percept_hex
    b4_bad = 0
    for a, b in zip(on, off):
        if (a[5], a[6], a[7], a[9]) != (b[5], b[6], b[7], b[9]):
            b4_bad += 1
            if b4_bad <= 3:
                print("B4 DIFF seq", a[1])
    print("B4: %d/10000 trials differ (on vs off)" % b4_bad)

    # KB-E2
    e2_bad = 0
    for r in on:
        if fork == "A":
            if r[11] == "-" or r[12] == "-" or r[13] != "1":
                e2_bad += 1
        else:
            if r[11] == "-":
                e2_bad += 1
    seqs = set(r[1] for r in on)
    led_seqs = [l.split("\t")[0] for l in open(led_p) if l.strip()]
    phantom = sum(1 for s in led_seqs if s not in seqs)
    print("KB-E2: %d bad emissions, %d phantom ledger seqs" % (e2_bad, phantom))
    print("B4 " + ("PASS" if b4_bad == 0 else "FAIL") +
          " | KB-E2 " + ("PASS" if e2_bad == 0 and phantom == 0 else "FAIL"))

main()
