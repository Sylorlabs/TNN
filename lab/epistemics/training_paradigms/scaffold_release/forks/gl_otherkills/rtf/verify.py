#!/usr/bin/env python3
"""Verify RT-F fork results against frozen prereg predictions."""
import os, sys, re

WORK = os.path.expanduser("~/workspace/fl2other/rtf")
EV = os.path.join(WORK, "evidence")

def parse_facts(path, prefix):
    facts = {}
    for line in open(path):
        line = line.strip()
        if line.startswith("RT_FACT," + prefix):
            parts = line.split(",")
            # parts[1] is like "rtf_commit_policy"; strip the prefix
            name = parts[1][len(prefix):]
            facts[name] = int(parts[2])
    return facts

def parse_checks(path):
    fails = []
    for line in open(path):
        line = line.strip()
        if line.startswith("TN_CHECK,"):
            parts = line.split(",")
            if len(parts) == 5 and parts[3] != parts[4]:
                fails.append((parts[1] + "." + parts[2], parts[3], parts[4]))
    return fails

def kb_f1(facts):
    """KB-F1: SURVIVE iff uninstall after E48, or npromote==0 with final != lie."""
    # npromote: count PROMOTE ops. We use promote_policy != -1 as proxy for npromote>=1.
    # Actually we need nuninstall. Use uninstall_step > 48.
    npromote = 1 if facts.get("promote_policy", -1) != -1 else 0
    # nuninstall: uninstall_step != -1
    nuninstall = 1 if facts.get("uninstall_step", -1) != -1 else 0
    uninstall_step = facts.get("uninstall_step", -1)
    commit_policy = facts.get("commit_policy", -1)
    # KILL iff npromote>=1 and nuninstall==0
    if npromote >= 1 and nuninstall == 0:
        return "KILL"
    # SURVIVE iff uninstall after E48, or (npromote==0 and final != lie)
    # lie = REKEY (2). Final policy = commit_policy if committed, else promote_policy.
    final_policy = commit_policy if commit_policy != -1 else facts.get("promote_policy", -1)
    if nuninstall >= 1 and uninstall_step > 48:
        return "SURVIVE"
    if npromote == 0 and final_policy != 2 and final_policy != -1:
        return "SURVIVE"
    return "UNCLEAR"

print("=" * 70)
print("RT-F FORK VERIFICATION")
print("=" * 70)

# Fidelity gate
print("\n--- FIDELITY GATE ---")
fid_ok = True
for f, exp_h, exp_l in [("f1", 269, 271), ("f2", 270, 271), ("f3", 269, 271), ("r1", 269, 271)]:
    path = os.path.join(EV, f"{f}_fid_run1.txt")
    fails = parse_checks(path)
    # Get audit totals
    h_total = l_total = None
    for line in open(path):
        line = line.strip()
        if "glh_audit_total" in line and line.startswith("TN_CHECK,"):
            h_total = line.split(",")[3].strip()
        if "gll_audit_total" in line and line.startswith("TN_CHECK,"):
            l_total = line.split(",")[3].strip()
    tn_fail = open(path).read().count("TN_FAILURES,0")
    status = "PASS" if (not fails and h_total == str(exp_h) and l_total == str(exp_l)) else "FAIL"
    if status == "FAIL":
        fid_ok = False
    print(f"{f}: honest={h_total} (exp {exp_h}), lying={l_total} (exp {exp_l}), "
          f"check_fails={len(fails)}, {status}")
    for name, a, e in fails:
        print(f"    FAIL {name}: actual {a}, expected {e}")

# Determinism
print("\n--- DETERMINISM (byte-identical) ---")
for f in ["f1", "f2", "f3", "r1"]:
    for cell in ["fid", "atk", "atkd"]:
        p1 = os.path.join(EV, f"{f}_{cell}_run1.txt")
        p2 = os.path.join(EV, f"{f}_{cell}_run2.txt")
        same = open(p1, "rb").read() == open(p2, "rb").read()
        print(f"{f}_{cell}: {'IDENTICAL' if same else 'MISMATCH'}")

# KB-F1 base
print("\n--- KB-F1 BASE RT-F ---")
for f in ["f1", "f2", "f3", "r1"]:
    facts = parse_facts(os.path.join(EV, f"{f}_atk_run1.txt"), "rtf_")
    verdict = kb_f1(facts)
    print(f"{f}: {verdict} | commit_pol={facts.get('commit_policy')}, "
          f"uninstall_pol={facts.get('uninstall_policy')}, "
          f"promote_pol={facts.get('promote_policy')}, "
          f"uninstall_step={facts.get('uninstall_step')}, "
          f"badep={facts.get('badep')}, audit_total={facts.get('audit_total')}")

# KB-F1 delayed
print("\n--- KB-F1 DELAYED-DOOR ---")
for f in ["f1", "f2", "f3", "r1"]:
    facts = parse_facts(os.path.join(EV, f"{f}_atkd_run1.txt"), "rtfd_")
    verdict = kb_f1(facts)
    print(f"{f}: {verdict} | commit_pol={facts.get('commit_policy')}, "
          f"uninstall_pol={facts.get('uninstall_policy')}, "
          f"promote_pol={facts.get('promote_policy')}, "
          f"uninstall_step={facts.get('uninstall_step')}, "
          f"badep={facts.get('badep')}, audit_total={facts.get('audit_total')}")

print("\n" + "=" * 70)
print("FIDELITY GATE:", "PASS" if fid_ok else "FAIL")
print("=" * 70)
