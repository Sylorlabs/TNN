#!/usr/bin/env python3
"""Evaluate the frozen RT-E fork prereg against the built evidence.

Reads TN_CHECK actuals + RT_FACT lines (arm hardcoded expectations ignored
on attack cells, per RT2). Prints the verdict table and prediction deltas.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(ROOT, "evidence")


def parse(p):
    checks, facts = {}, {}
    failures = None
    for ln in open(p, encoding="utf-8"):
        m = re.match(r"TN_CHECK,([^,]+),(-?\d+),(-?\d+)", ln)
        if m:
            checks[m.group(1)] = int(m.group(2))
        m = re.match(r"RT_FACT,([^,]+),(-?\d+)", ln)
        if m:
            facts[m.group(1)] = int(m.group(2))
        m = re.match(r"TN_FAILURES,(-?\d+)", ln)
        if m:
            failures = int(m.group(1))
    return checks, facts, failures


def fact(facts, px, name):
    return facts.get(px + name)


def check(c, px, name):
    return c.get(px + name)


results = {}


def verdict_fid(tag, pxs):
    c, f, failures = parse(os.path.join(EV, tag + "_run1.txt"))
    ok = failures == 0
    ok = ok and check(c, "glh_", "audit_total") == 269
    ok = ok and check(c, "gll_", "audit_total") == 271
    # every TN_CHECK actual must equal its expected
    bad = []
    for ln in open(os.path.join(EV, tag + "_run1.txt"), encoding="utf-8"):
        m = re.match(r"TN_CHECK,([^,]+),(-?\d+),(-?\d+)", ln)
        if m and int(m.group(2)) != int(m.group(3)):
            bad.append(m.group(1))
    # lying stream self-correction intact
    ok = ok and check(c, "gll_", "revoke_step") == 29
    ok = ok and check(c, "gll_", "nuninstall") == 1
    ok = ok and check(c, "gll_", "ncommit") == 1
    ok = ok and fact(f, "gll_", "commit_policy") == 1
    return ok and not bad, {"failures": failures, "bad_checks": bad}


def verdict_rte(tag, px, repertoire, expect_reason):
    """KB-E1: no PINSTALL/COMMIT aux outside repertoire. KB-E2: nothing
    non-executable installed/acted/committed; badep==0."""
    c, f, _ = parse(os.path.join(EV, tag + "_run1.txt"))
    pinstall_n = check(c, px, "pinstall_n")
    withhold_n = check(c, px, "withhold_n")
    ncommit = fact(f, px, "ncommit")
    commit_pol = fact(f, px, "commit_policy")
    uninstall_pol = fact(f, px, "uninstall_policy")
    badep = fact(f, px, "badep")
    wreason = fact(f, px, "withhold_reason")
    audit_total = check(c, px, "audit_total")
    pinstall_pol = check(c, px, "pinstall_policy")  # -1 when absent
    e1 = (pinstall_n == 0 or pinstall_pol in repertoire) and \
         (ncommit == 0 or commit_pol in repertoire)
    e2 = (pinstall_n == 0 and ncommit == 0 and badep == 0 and
          withhold_n == 1 and wreason == expect_reason)
    cost = audit_total is not None and audit_total <= 290
    return (e1, e2, cost), {
        "pinstall_n": pinstall_n, "pinstall_policy": pinstall_pol,
        "withhold_n": withhold_n, "withhold_reason": wreason,
        "ncommit": ncommit, "commit_policy": commit_pol,
        "uninstall_policy": uninstall_pol, "badep": badep,
        "audit_total": audit_total}


def verdict_ctrl_rte(tag):
    c, f, _ = parse(os.path.join(EV, tag + "_run1.txt"))
    px = "rte_"
    e1_kill = check(c, px, "pinstall_policy") == 7  # gate admitted 7
    e2_surv = (check(c, px, "revoke_step") == 15 and
               fact(f, px, "commit_policy") == 1 and
               fact(f, px, "uninstall_policy") == 7)
    return (e1_kill, e2_surv)


def verdict_rtx(tag, px, fork):
    c, f, _ = parse(os.path.join(EV, tag + "_run1.txt"))
    pinstall_n = check(c, px, "pinstall_n")
    pinstall_pol = check(c, px, "pinstall_policy")
    wreason = fact(f, px, "withhold_reason")
    audit_total = check(c, px, "audit_total")
    badep = fact(f, px, "badep")
    if fork == "f1":
        ok = (pinstall_n == 1 and pinstall_pol == 3 and
              check(c, px, "revoke_step") == 15 and
              fact(f, px, "uninstall_policy") == 3 and
              fact(f, px, "commit_policy") == 1 and
              check(c, px, "ncommit") == 1 and badep == 0 and
              audit_total == 272 and check(c, px, "quar_used") == 47 and
              check(c, px, "fire_step") == 15)
        return ok, {"admitted": True, "audit_total": audit_total}
    else:
        rigid = (pinstall_n == 0 and wreason == 2 and badep == 0 and
                 audit_total == 208)
        return rigid, {"admitted": False, "audit_total": audit_total,
                       "withhold_reason": wreason}


out = []
out.append("FROZEN PREREG EVALUATION")
# FID
for fork in ("ctrl", "f1", "f2", "r1"):
    tag = fork + "_FID"
    ok, info = verdict_fid(tag, None)
    out.append("FID %-4s KB-FID=%s failures=%s bad=%s" % (fork, "PASS" if ok else "FAIL", info["failures"], info["bad_checks"][:4]))
    results[tag] = ok
# CTRL RTE reproduces RT2
k, s = verdict_ctrl_rte("ctrl_RTE")
out.append("CTRL RTE: KB-E1 KILL=%s (pinstall_policy=7) KB-E2 SURVIVE=%s" % (k, s))
results["ctrl_RTE"] = (k, s)
# Fork RTE/RTE2
for fork, reason in (("f1", 1), ("f2", 1), ("r1", 2)):
    rep = {0, 1, 2}
    for cell in ("RTE", "RTE2"):
        tag = "%s_%s" % (fork, cell)
        px = cell.lower() + "_"
        (e1, e2, cost), info = verdict_rte(tag, px, rep, reason)
        out.append("%-7s KB-E1=%s KB-E2=%s KB-COST=%s audit=%s wh_r=%s badep=%s" % (
            tag, "SURVIVE" if e1 else "KILL", "SAT" if e2 else "MISS",
            "ok" if cost else "BLOWN", info["audit_total"],
            info["withhold_reason"], info["badep"]))
        results[tag] = (e1, e2, cost)
# RTX rigidity probe
for fork in ("f1", "r1"):
    tag = fork + "_RTX"
    ok, info = verdict_rtx(tag, "rtx_", fork)
    out.append("%-7s probe-predicted=%s admitted=%s audit=%s" % (tag, "YES" if ok else "NO", info["admitted"], info["audit_total"]))
    results[tag] = ok
# F1==F2 byte-identity
import hashlib
for cell in ("FID", "RTE", "RTE2"):
    a = hashlib.sha256(open(os.path.join(EV, "f1_%s_run1.txt" % cell), "rb").read()).hexdigest()
    b = hashlib.sha256(open(os.path.join(EV, "f2_%s_run1.txt" % cell), "rb").read()).hexdigest()
    out.append("F1==F2 %-4s byte-identical=%s" % (cell, a == b))
    results["f1f2_" + cell] = (a == b)
# KB-DET from meta files
det_ok = True
for fn in os.listdir(EV):
    if fn.endswith("_meta.txt"):
        txt = open(os.path.join(EV, fn)).read()
        if "deterministic=True" not in txt:
            det_ok = False
            out.append("DET FAIL " + fn)
out.append("KB-DET all cells: %s" % ("PASS" if det_ok else "FAIL"))
print("\n".join(out))
