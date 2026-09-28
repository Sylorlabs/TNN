#!/usr/bin/env python3
"""Compare family selections + pass/fail between two run_recall.py console logs.
Usage: compare_runs.py <logA> <logB>   (must be byte-identical selections)
"""
import re, sys

def parse(path):
    rows = {}
    gate = None
    for line in open(path):
        m = re.match(r"^(r\d+|c\d+|s\d+|m\d+|o\d+|h\d+|w\d+|f\d+)\s+(\S+)\s+Y\s+Y\s+(PASS|FAIL)", line)
        if m:
            rows[m.group(1)] = (m.group(2), m.group(3))
        if line.startswith("gate:"):
            gate = line.strip()
    return rows, gate

a, ga = parse(sys.argv[1]); b, gb = parse(sys.argv[2])
assert set(a) == set(b) == set([f"r{i}" for i in range(1,4)] + [f"c{i}" for i in range(1,4)]
    + [f"s{i}" for i in range(1,4)] + [f"m{i}" for i in range(1,4)]
    + [f"o{i}" for i in range(1,4)] + [f"h{i}" for i in range(1,4)]
    + [f"w{i}" for i in range(1,4)] + [f"f{i}" for i in range(1,4)]), "spec id mismatch"
fam_diff = [(k, a[k][0], b[k][0]) for k in a if a[k][0] != b[k][0]]
pass_diff = [(k, a[k][1], b[k][1]) for k in a if a[k][1] != b[k][1]]
print("specs compared:", len(a))
print("family selection diffs:", fam_diff if fam_diff else "NONE — 24/24 byte-identical")
print("pass/fail diffs:", pass_diff if pass_diff else "NONE")
print("gate line equal:", ga == gb, "::", gb)
print("PASS" if not fam_diff and not pass_diff and ga == gb else "FAIL")
