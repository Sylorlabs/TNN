#!/usr/bin/env python3
"""Parse H-2 Phase-3 run transcripts into a metrics table for kill-bar judging."""
import re, sys
from pathlib import Path

EV = Path(__file__).resolve().parent.parent / "evidence"
NAMES = ["nuninstall","npromote","revoke_step","commit_step","promote_step",
         "ncommit","audit_total","total_contest","total_rekey","quar_used",
         "neg_signal_n","badep","nescrow_enter","nescrow_finalize","nescrow_rollback",
         "escrow_finalize_step","escrow_rollback_step","escrow_budget_used_max",
         "escrow_shadow_clean","escrow_entry_defect","commit_policy",
         "uninstall_policy","promote_policy","episodes_ok","tn_failures"]

def parse(path, prefix):
    m = {}
    for line in Path(path).read_text().splitlines():
        p = line.split(",")
        if p[0] == "TN_CHECK" and len(p) == 4 and p[1].startswith(prefix):
            m[p[1][len(prefix):]] = int(p[2])
        if p[0] == "RT_FACT" and len(p) == 3 and p[1].startswith(prefix):
            m[p[1][len(prefix):]] = int(p[2])
    fails = sum(1 for line in Path(path).read_text().splitlines()
                if line.startswith("TN_CHECK,") and line.split(",")[2] != line.split(",")[3])
    m["tn_failures"] = fails
    return m

cells = sys.argv[1:] or ["w1","w2h","w2l","w3a","w3b","w3ae","rta18","rta20","rtd","rte",
                         "ctl_h","fid","esc_ctl_B"]
PREFIX = {"w1":"w1_","w2h":"w2h_","w2l":"w2l_","w3a":"w3a_","w3b":"w3b_",
          "w3ae":"w3ae_","rta18":"rta8_","rta20":"rta0_","rtd":"rtd_","rte":"rte_",
          "ctl_h":"w2h_","esc_ctl_B":"rtb_","fid_h":"glh_","fid_l":"gll_"}
rows = {}
for c in cells:
    if c == "fid":
        for sub, px in (("fid_h","glh_"),("fid_l","gll_")):
            rows[sub] = parse(EV / "fid_run1.txt", px)
    else:
        rows[c] = parse(EV / f"{c}_run1.txt", PREFIX[c])

hdr = ["cell"] + NAMES
print("\t".join(hdr))
for c in cells:
    if c == "fid":
        for sub in ("fid_h","fid_l"):
            print("\t".join([sub] + [str(rows[sub].get(n, "?")) for n in NAMES]))
    else:
        print("\t".join([c] + [str(rows[c].get(n, "?")) for n in NAMES]))
