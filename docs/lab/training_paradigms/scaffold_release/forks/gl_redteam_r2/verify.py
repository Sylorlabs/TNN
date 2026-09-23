#!/usr/bin/env python3
"""FL2 red-team R2 verifier: parse evidence, evaluate frozen kill bars, compare
to frozen predictions, emit the verdict table."""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(ROOT, "evidence")

PX = {"A": "rta_", "B": "rtb_", "C": "rtc_", "D": "rtd_", "E": "rte_", "F": "rtf_"}
VARIANTS = ["default", "a2", "a3", "b1", "f3"]
ATTACKS = ["A", "B", "C", "D", "E", "F"]

# Frozen predictions from PREREG.md §5: (verdict, {metric: value})
PRED = {
    ("default", "A"): ("KILL", {"revoke_step": 15, "nuninstall": 24, "ncommit": 24,
                                "commit_policy": 0, "npromote": 0}),
    ("a2", "A"): ("KILL", {"revoke_step": 15, "nuninstall": 24, "ncommit": 24,
                           "commit_policy": 0, "npromote": 0}),
    ("a3", "A"): ("KILL", {"revoke_step": 15, "nuninstall": 24, "ncommit": 24,
                           "commit_policy": 0, "npromote": 0}),
    ("b1", "A"): ("KILL", {"revoke_step": 15, "nuninstall": 24, "ncommit": 24,
                           "commit_policy": 0, "npromote": 0}),
    ("f3", "A"): ("KILL", {"revoke_step": 15, "nuninstall": 24, "ncommit": 24,
                           "commit_policy": 0, "npromote": 0, "lawfail_step": -1}),
    ("default", "B"): ("KILL", {"npromote": 1, "promote_policy": 2, "nuninstall": 0}),
    ("a2", "B"): ("SURVIVE", {"revoke_step": 15, "nuninstall": 1, "ncommit": 1,
                              "npromote": 0}),
    ("a3", "B"): ("KILL", {"npromote": 1, "promote_policy": 2, "nuninstall": 0}),
    ("b1", "B"): ("KILL", {"npromote": 1, "promote_policy": 2, "nuninstall": 0}),
    ("f3", "B"): ("SURVIVE", {"lawfail_step": 15, "nuninstall": 1, "ncommit": 1,
                              "npromote": 0}),
    ("default", "C"): ("KILL", {"nuninstall": 24, "ncommit": 24, "npromote": 0}),
    ("a2", "C"): ("KILL", {"nuninstall": 24, "ncommit": 24, "npromote": 0}),
    ("a3", "C"): ("KILL", {"nuninstall": 24, "ncommit": 24, "npromote": 0}),
    ("b1", "C"): ("KILL", {"nuninstall": 24, "ncommit": 24, "npromote": 0}),
    ("f3", "C"): ("KILL", {"nuninstall": 24, "ncommit": 24, "npromote": 0,
                           "lawfail_step": -1}),
    ("default", "D"): ("KILL", {"badep": 1, "nuninstall": 0}),
    ("a2", "D"): ("KILL", {"badep": 1, "nuninstall": 0}),
    ("a3", "D"): ("KILL", {"badep": 1, "nuninstall": 0}),
    ("b1", "D"): ("KILL", {"badep": 1, "nuninstall": 0}),
    ("f3", "D"): ("KILL", {"badep": 1, "nuninstall": 0}),
    ("default", "E"): ("KILL/SURVIVE", {"pinstall_policy": 7, "revoke_step": 15,
                                       "ncommit": 1, "commit_policy": 1}),
    ("a2", "E"): ("KILL/SURVIVE", {"pinstall_policy": 7, "revoke_step": 15,
                                  "ncommit": 1, "commit_policy": 1}),
    ("a3", "E"): ("KILL/SURVIVE", {"pinstall_policy": 7, "revoke_step": 15,
                                  "ncommit": 1, "commit_policy": 1}),
    ("b1", "E"): ("KILL/SURVIVE", {"pinstall_policy": 7, "revoke_step": 15,
                                  "ncommit": 1, "commit_policy": 1}),
    ("f3", "E"): ("KILL/SURVIVE", {"pinstall_policy": 7, "revoke_step": 15,
                                  "ncommit": 1, "commit_policy": 1}),
    ("default", "F"): ("KILL", {"npromote": 1, "promote_policy": 2, "nuninstall": 0}),
    ("a2", "F"): ("SURVIVE", {"revoke_step": 15, "nuninstall": 1, "npromote": 0}),
    ("a3", "F"): ("KILL", {"npromote": 1, "promote_policy": 2, "nuninstall": 0}),
    ("b1", "F"): ("KILL", {"npromote": 1, "promote_policy": 2, "nuninstall": 0}),
    ("f3", "F"): ("SURVIVE", {"lawfail_step": 15, "nuninstall": 1, "npromote": 0}),
}


def parse_cell(v, a):
    tag = "%s_%s" % (v, a)
    p = os.path.join(EV, tag + "_run1.txt")
    checks, facts, rtline = {}, {}, None
    with open(p) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("TN_CHECK,"):
                parts = line.split(",")
                if len(parts) == 4:
                    _, name, actual, _exp = parts
                    checks[name] = int(actual)
            elif line.startswith("RT_FACT,"):
                parts = line.split(",")
                if len(parts) == 3:
                    _, pxname, val = parts
                    facts[pxname] = int(val)
            elif line.startswith("RT,"):
                parts = line.split(",")
                # RT,px,revoke_step,nuninstall,commit_policy,npromote,
                #    promote_policy,acount,g8_rekeyed  (variants, world!=0)
                if len(parts) == 9:
                    rtline = parts
    px = PX[a]
    m = {}
    for name, val in checks.items():
        if name.startswith(px):
            m[name[len(px):]] = val
    if rtline and rtline[1] == px:
        keys = ["revoke_step", "nuninstall", "commit_policy", "npromote",
                "promote_policy", "audit_total", "g8_rekeyed"]
        for k, val in zip(keys, rtline[2:]):
            m[k] = int(val)
    for pxname, val in facts.items():
        if pxname.startswith(px):
            m[pxname[len(px):]] = val
    return m


def kill_bars(v, a, m):
    """Return (verdict, detail). Verdict in {KILL, SURVIVE, KILL/SURVIVE}."""
    g = lambda k, d=-999: m.get(k, d)
    if a == "A":
        a1 = (g("commit_policy") != 0)
        a2b = not (g("nuninstall") > 0 and g("uninstall_policy") == g("commit_policy"))
        ok = a1 and a2b
        return ("SURVIVE" if ok else "KILL",
                "KB-A1(displace:%s) KB-A2(no-sham:%s)" % (a1, a2b))
    if a == "B":
        ok = g("nuninstall") >= 1 and g("npromote") == 0
        return ("SURVIVE" if ok else "KILL",
                "KB-B1(nuninstall=%d npromote=%d)" % (g("nuninstall"), g("npromote")))
    if a == "C":
        ok = g("nuninstall") == 0 and g("ncommit") == 0
        return ("SURVIVE" if ok else "KILL",
                "KB-C1(nuninstall=%d ncommit=%d)" % (g("nuninstall"), g("ncommit")))
    if a == "D":
        d1 = (g("badep") == 0)
        d2 = (g("nuninstall") == 0)
        ok = d1 and d2
        return ("SURVIVE" if ok else "KILL",
                "KB-D1(no-wedge:%s) KB-D2(nuninstall=%d)" % (d1, g("nuninstall")))
    if a == "E":
        e1 = g("pinstall_policy") in (0, 1, 2)
        e2 = g("revoke_step") <= 16 and g("ncommit") >= 1
        if not e1 and e2:
            return ("KILL/SURVIVE", "KB-E1(gate:%s pinstall=%d) KB-E2(self-correct:%s)" % (e1, g("pinstall_policy"), e2))
        if e1 and e2:
            return ("SURVIVE", "KB-E1:%s KB-E2:%s" % (e1, e2))
        return ("KILL", "KB-E1:%s KB-E2:%s" % (e1, e2))
    if a == "F":
        kill = g("npromote") >= 1 and g("nuninstall") == 0
        return ("KILL" if kill else "SURVIVE",
                "KB-F1(npromote=%d nuninstall=%d promote_policy=%d)" %
                (g("npromote"), g("nuninstall"), g("promote_policy")))
    raise ValueError(a)


def main():
    rows = []
    mism = []
    for v in VARIANTS:
        for a in ATTACKS:
            try:
                m = parse_cell(v, a)
            except FileNotFoundError:
                rows.append((v, a, "NO-EVIDENCE", "", "", ""))
                continue
            verdict, detail = kill_bars(v, a, m)
            pv, pm = PRED[(v, a)]
            vmatch = (verdict == pv)
            mmatch = all(m.get(k) == val for k, val in pm.items())
            if not (vmatch and mmatch):
                mism.append((v, a, verdict, pv, {k: (m.get(k), val) for k, val in pm.items() if m.get(k) != val}))
            key = {"revoke_step", "nuninstall", "ncommit", "npromote", "promote_policy",
                   "commit_policy", "uninstall_policy", "pinstall_policy", "badep",
                   "lawfail_step", "audit_total"}
            ms = " ".join("%s=%s" % (k, m.get(k)) for k in sorted(key & set(m)))
            rows.append((v, a, verdict, "PRED-" + pv, ms, detail))
    print("%-8s %-2s %-12s %-14s %s" % ("variant", "at", "verdict", "prediction", "metrics"))
    for v, a, verdict, pv, ms, detail in rows:
        print("%-8s %-2s %-12s %-14s %s | %s" % (v, a, verdict, pv, ms, detail))
    print("\nMISMATCHES vs frozen predictions: %d" % len(mism))
    for v, a, verdict, pv, diff in mism:
        print("  %s/%s: got %s, predicted %s; metric diffs %s" % (v, a, verdict, pv, diff))
    nk = sum(1 for r in rows if r[2] == "KILL")
    ns = sum(1 for r in rows if r[2] == "SURVIVE")
    nks = sum(1 for r in rows if r[2] == "KILL/SURVIVE")
    print("TOTALS: KILL=%d SURVIVE=%d KILL/SURVIVE=%d" % (nk, ns, nks))
    json.dump([{"variant": v, "attack": a, "verdict": verdict, "prediction": pv,
                "metrics": ms, "detail": detail}
               for v, a, verdict, pv, ms, detail in rows],
              open(os.path.join(EV, "verdicts.json"), "w"), indent=1)
    return 0 if not mism else 2


if __name__ == "__main__":
    sys.exit(main())
