#!/usr/bin/env python3
"""RT-D fork verifier: parse evidence, evaluate frozen kill bars (KB-D1/D2),
compare against frozen PREREG.md predictions.

Pressure-audit counts (50 evict / 50 refuse) are verified via audit_total,
which includes them: F1/R1 = 309, F2 = 259, canon = 209 (wedge at E79 cuts
the per-episode audits to 1). total_contest - 64 cross-checks the count.
"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(ROOT, "evidence")
FORKS = ["canon", "f1", "f2", "r1"]

# Frozen predictions from PREREG.md: (verdict, {metric: value})
PRED_D = {
    "canon": ("KILL",    {"badep": 1, "nuninstall": 0, "npromote": 1,
                          "total_contest": 64, "quar_used": 64,
                          "audit_total": 209}),
    "f1":    ("SURVIVE", {"badep": 0, "nuninstall": 0, "npromote": 1,
                          "total_contest": 114, "quar_used": 64,
                          "audit_total": 309}),
    "f2":    ("SURVIVE", {"badep": 0, "nuninstall": 0, "npromote": 1,
                          "total_contest": 64, "quar_used": 64,
                          "audit_total": 259}),
    "r1":    ("SURVIVE", {"badep": 0, "nuninstall": 0, "npromote": 1,
                          "total_contest": 114, "quar_used": 64,
                          "audit_total": 309}),
}
PRED_UNIT = {
    "canon": {"n_ok": 128, "n_bad": 12, "find_1000": 0, "find_1139": -1,
              "val_1050": 5050},
    "f1":    {"n_ok": 140, "n_bad": 0, "n_evict": 12,
              "find_1000": -1, "find_1011": -1, "find_1012": 12,
              "find_1139": 11, "val_1050": 5050},
    "f2":    {"n_ok": 128, "n_bad": 0, "n_pressure": 12, "n_refuse": 12,
              "find_1000": 0, "find_1139": -1, "val_1050": 5050},
    "r1":    {"n_ok": 128, "n_bad": 12, "find_1000": 0, "find_1139": -1,
              "val_1050": 5050},
}


def parse_attack(fork):
    p = os.path.join(EV, "%s_D_run1.txt" % fork)
    m = {}
    with open(p) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("TN_CHECK,rtd_"):
                parts = line.split(",")
                if len(parts) == 4:
                    m[parts[1][4:]] = int(parts[2])
            elif line.startswith("RT_FACT,"):
                # RT_FACT,<px><name>,<val> e.g. RT_FACT,rtd_badep,1
                parts = line.split(",")
                if len(parts) == 3 and parts[1].startswith("rtd_"):
                    m[parts[1][4:]] = int(parts[2])
    return m


def parse_unit(fork):
    p = os.path.join(EV, "unit_%s_run1.txt" % fork)
    m = {}
    with open(p) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("UNIT,"):
                _, name, val = line.split(",")
                m[name] = int(val)
    return m


def main():
    mism = []
    print("=== RT-D attack cells ===")
    for fork in FORKS:
        m = parse_attack(fork)
        d1 = (m.get("badep") == 0)
        d2 = (m.get("nuninstall") == 0)
        verdict = "SURVIVE" if (d1 and d2) else "KILL"
        pv, pm = PRED_D[fork]
        vmatch = (verdict == pv)
        mdiff = {k: (m.get(k), v) for k, v in pm.items() if m.get(k) != v}
        stat = "OK " if (vmatch and not mdiff) else "MISS"
        if not (vmatch and not mdiff):
            mism.append((fork, "D", verdict, pv, mdiff))
        keys = ["badep", "nuninstall", "npromote", "total_contest",
                "quar_used", "audit_total", "promote_policy",
                "commit_policy", "uninstall_policy"]
        ms = " ".join("%s=%s" % (k, m.get(k)) for k in keys if k in m)
        print("%-6s %-7s %-4s KB-D1(no-wedge:%s) KB-D2(nuninstall=%s) | %s"
              % (fork, verdict, stat, d1, m.get("nuninstall"), ms))
    print("=== main-store unit floods ===")
    for fork in FORKS:
        m = parse_unit(fork)
        pm = PRED_UNIT[fork]
        mdiff = {k: (m.get(k), v) for k, v in pm.items() if m.get(k) != v}
        stat = "OK " if not mdiff else "MISS"
        if mdiff:
            mism.append((fork, "unit", None, None, mdiff))
        ms = " ".join("%s=%s" % (k, m.get(k)) for k in sorted(m))
        print("%-6s %-4s %s" % (fork, stat, ms))
    print("MISMATCHES: %d" % len(mism))
    for fork, cell, v, pv, diff in mism:
        print("  %s/%s: got %s predicted %s diff=%s" % (fork, cell, v, pv, diff))
    return 0 if not mism else 2


if __name__ == "__main__":
    sys.exit(main())
