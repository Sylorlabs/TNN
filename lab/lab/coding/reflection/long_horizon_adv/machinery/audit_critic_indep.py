#!/usr/bin/env python3
"""audit_critic_indep.py — LH-ADV-2026-09-22 critic independence audit.
Enforces: defined_fns(critic) ∩ defined_fns(emitter) ⊆ ALLOWLIST.
ALLOWLIST = contract-line parser helpers only (frozen in prereg).
Violation = trial VOID before scoring.
"""
import re, sys

ALLOWLIST = {
    "s_eq", "s_find", "s_has", "spec_kv", "num_val", "i64s",
    "line_get", "line_count", "sw", "cline",
    "c_desc", "c_win", "c_winl", "c_winr", "c_stage",
    "c_testin", "c_testout", "c_ntests",
    "d_field_count", "d_field_get",
    "main",  # language entry point, not shared logic
}

def defined_fns(path):
    src = open(path).read()
    # match "fn name(" at line start (allow leading whitespace)
    return set(re.findall(r'^\s*fn\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(', src, re.M))

def main():
    crit = sys.argv[1] if len(sys.argv) > 1 else "machinery/adv_critic.zag"
    emit = sys.argv[2] if len(sys.argv) > 2 else "machinery/adv_emit.zag"
    cf, ef = defined_fns(crit), defined_fns(emit)
    inter = (cf & ef) - ALLOWLIST
    print(f"critic fns: {len(cf)}, emitter fns: {len(ef)}")
    print(f"intersection beyond ALLOWLIST: {sorted(inter)}")
    if inter:
        print("AUDIT FAIL: shared non-allowlisted functions")
        sys.exit(1)
    print("AUDIT PASS")
    sys.exit(0)

if __name__ == "__main__":
    main()
