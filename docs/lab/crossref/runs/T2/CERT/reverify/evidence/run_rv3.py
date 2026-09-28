#!/usr/bin/env python3
"""RV3 runner: 3x old/new thincert per plant case; compare verdicts + attestation bytes.
Python glue only. Decisions made by the pinned Zag certifier binaries.
"""
import hashlib, os, subprocess, sys

TC = os.path.expanduser("~/workspace/certrebuild/work/thincert")
ROOT = os.path.expanduser("~/workspace/reverify/work/cert/rv3")

CASES = ["p1_empty", "p2a_exact", "p2b_over",
         "p3a_truncated_ev", "p3b_runs7", "p3c_ident0", "p3d_bad_manifest",
         "p4a_missing_module", "p4b_missing_evidence", "p4c_missing_manifest",
         "p5a_128", "p5b_129", "p5c1_bin_at_cap", "p5c2_bin_over_cap"]

def verdict_of(att):
    for line in open(att, errors="replace"):
        if line.startswith("verdict="):
            return line.strip().split("=", 1)[1]
    return "NO-VERDICT"

def run_case(case):
    d = ROOT + "/" + case
    man = d + "/MANIFEST.txt"
    bdir = d + "/builddir"
    binp = d + "/plant.bin"
    ev = d + "/evidence.txt"
    rows = []
    for label, exe in (("old", TC + "/thincert_old"), ("new", TC + "/thincert_new")):
        digests, rcs, vds = [], [], []
        for i in (1, 2, 3):
            att = d + "/att_%s_%d.txt" % (label, i)
            p = subprocess.run([exe, man, bdir, binp, ev, att],
                               capture_output=True, cwd=d, timeout=600)
            rcs.append(p.returncode)
            if os.path.exists(att):
                with open(att, "rb") as f:
                    digests.append(hashlib.sha256(f.read()).hexdigest())
                vds.append(verdict_of(att))
            else:
                digests.append("NO-ATTESTATION")
                vds.append("NO-VERDICT")
            if case == "p4c_missing_manifest" and i == 1:
                rows.append(("stderr_%s" % label, p.stderr.decode()[:120].strip()))
        rows.append((label, rcs, vds, digests))
    return rows

def main():
    only = sys.argv[1:] or CASES
    for case in only:
        print("=" * 20, case, "=" * 20)
        for row in run_case(case):
            print(row)
        sys.stdout.flush()

main()
