#!/usr/bin/env python3
"""Verify RT-C fork-test cells against the frozen prereg predictions."""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(ROOT, "evidence")

# (verdict, {metric: expected})
PRED = {
    ("f1", "C"): ("SURVIVE", {"nuninstall": 0, "ncommit": 0, "revoke_step": -1,
                              "npromote": 1, "promote_policy": 1, "audit_total": 269,
                              "quar_used": 0}),
    ("f2", "C"): ("SURVIVE", {"nuninstall": 0, "ncommit": 0, "revoke_step": -1,
                              "npromote": 1, "promote_policy": 1, "audit_total": 269,
                              "quar_used": 0}),
    ("r1", "C"): ("SURVIVE", {"nuninstall": 0, "ncommit": 0, "revoke_step": -1,
                              "npromote": 1, "promote_policy": 1, "audit_total": 269,
                              "quar_used": 0}),
    ("n1", "C"): ("KILL", {"nuninstall": 2, "ncommit": 2, "revoke_step": 15,
                           "uninstall_policy": 1, "commit_policy": 2,
                           "npromote": 0, "audit_total": 274, "quar_used": 0}),
    ("f1", "A"): ("SURVIVE", {"nuninstall": 1, "ncommit": 1, "revoke_step": 15,
                              "uninstall_policy": 0, "commit_policy": 1,
                              "npromote": 0}),
    ("f2", "A"): ("KILL", {"nuninstall": 24, "ncommit": 24, "revoke_step": 15,
                           "uninstall_policy": 0, "commit_policy": 0,
                           "npromote": 0}),
    ("r1", "A"): ("KILL", {"nuninstall": 24, "ncommit": 24, "revoke_step": 15,
                           "uninstall_policy": 0, "commit_policy": 0,
                           "npromote": 0}),
    ("n1", "A"): ("SURVIVE", {"nuninstall": 1, "ncommit": 1, "revoke_step": 15,
                              "uninstall_policy": 0, "commit_policy": 1,
                              "npromote": 0}),
    ("f1", "P2"): ("SURVIVE", {"nuninstall": 0, "ncommit": 0, "revoke_step": -1,
                               "npromote": 1, "quar_used": 48, "audit_total": 269}),
    ("f2", "P2"): ("KILL", {"nuninstall": 24, "ncommit": 24, "revoke_step": 15,
                            "uninstall_policy": 1, "commit_policy": 1,
                            "npromote": 0}),
    ("r1", "P2"): ("KILL", {"nuninstall": 24, "ncommit": 24, "revoke_step": 15,
                            "uninstall_policy": 1, "commit_policy": 1,
                            "npromote": 0}),
    ("n1", "P2"): ("KILL", {"nuninstall": 2, "ncommit": 2, "revoke_step": 15,
                            "uninstall_policy": 1, "commit_policy": 2,
                            "npromote": 0}),
}

PX = {"C": "c_", "A": "a_", "P2": "p_"}


def parse(fork, cell):
    tag = "%s_%s" % (fork, cell)
    m = {}
    with open(os.path.join(EV, tag + "_run1.txt")) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("TN_CHECK,"):
                parts = line.split(",")
                if len(parts) == 4:
                    _, name, actual, _exp = parts
                    if name.startswith(fork + PX[cell]):
                        m[name[len(fork + PX[cell]):]] = int(actual)
            elif line.startswith("RT_FACT,"):
                parts = line.split(",")
                if len(parts) == 3:
                    _, pxname, val = parts
                    if pxname.startswith(fork + PX[cell]):
                        m[pxname[len(fork + PX[cell]):]] = int(val)
    return m


def bars(cell, m):
    g = lambda k, d=-999: m.get(k, d)
    if cell in ("C", "P2"):
        ok = g("nuninstall") == 0 and g("ncommit") == 0
        return ("SURVIVE" if ok else "KILL",
                "KB-C1(nuninstall=%d ncommit=%d)" % (g("nuninstall"), g("ncommit")))
    if cell == "A":
        a1 = g("commit_policy") != 0
        a2b = not (g("nuninstall") > 0 and g("uninstall_policy") == g("commit_policy"))
        ok = a1 and a2b
        return ("SURVIVE" if ok else "KILL",
                "KB-A1(displace:%s) KB-A2(no-sham:%s)" % (a1, a2b))
    raise ValueError(cell)


def main():
    mism = []
    print("%-6s %-4s %-8s %-10s %s" % ("fork", "cell", "verdict", "prediction", "metrics"))
    for fork in ("f1", "f2", "r1", "n1"):
        for cell in ("C", "A", "P2"):
            m = parse(fork, cell)
            verdict, detail = bars(cell, m)
            pv, pm = PRED[(fork, cell)]
            vmatch = (verdict == pv)
            mmatch = all(m.get(k) == v for k, v in pm.items())
            if not (vmatch and mmatch):
                mism.append((fork, cell, verdict, pv,
                             {k: (m.get(k), v) for k, v in pm.items() if m.get(k) != v}))
            key = ("revoke_step", "nuninstall", "ncommit", "npromote",
                   "promote_policy", "commit_policy", "uninstall_policy",
                   "quar_used", "audit_total", "total_contest", "total_rekey")
            ms = " ".join("%s=%s" % (k, m.get(k)) for k in key if k in m)
            print("%-6s %-4s %-8s %-10s %s | %s" % (fork, cell, verdict, "PRED-" + pv, ms, detail))
    print("\nMISMATCHES vs frozen predictions: %d" % len(mism))
    for fork, cell, verdict, pv, diff in mism:
        print("  %s/%s: got %s, predicted %s; metric diffs %s" % (fork, cell, verdict, pv, diff))
    nk = 0
    return 0 if not mism else 2


if __name__ == "__main__":
    sys.exit(main())
