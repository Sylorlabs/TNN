#!/usr/bin/env python3
"""audit_critic_indep2.py — LH-ADV-2 independent-critic audit.

Checks:
  1. Symbol disjointness: defined_fns(adv2_critic) ∩ defined_fns(adv2_emit)
     ⊆ {main} and ∩ defined_fns(adv2_delib) ⊆ {main}.
  2. Prefix discipline: every fn defined in adv2_critic.zag is `main` or
     starts with `kx_` (no shared helper symbols by construction).
  3. Contamination log present.
  4. Behavioral spot-checks are reported separately (see calibration log);
     this audit covers the structural claim.
Prints AUDIT-PASS or AUDIT-FAIL <reason>. Decision-free, zero RNG.
"""
import re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MACH = os.path.join(HERE, "machinery")

def fns(path):
    src = open(path).read()
    return set(re.findall(r'^fn\s+([A-Za-z_][A-Za-z0-9_]*)', src, re.M))

def main():
    fc = fns(os.path.join(MACH, "adv2_critic.zag"))
    fe = fns(os.path.join(MACH, "adv2_emit.zag"))
    fd = fns(os.path.join(MACH, "adv2_delib.zag"))
    bad_e = (fc & fe) - {"main"}
    bad_d = (fc & fd) - {"main"}
    if bad_e:
        print(f"AUDIT-FAIL critic∩emitter shared: {sorted(bad_e)}")
        return 1
    if bad_d:
        print(f"AUDIT-FAIL critic∩delib shared: {sorted(bad_d)}")
        return 1
    bad_prefix = [f for f in fc if f != "main" and not f.startswith("kx_")]
    if bad_prefix:
        print(f"AUDIT-FAIL non-kx_ critic fns: {sorted(bad_prefix)}")
        return 1
    if not os.path.exists(os.path.join(MACH, "CONTAMINATION_LOG.md")):
        print("AUDIT-FAIL CONTAMINATION_LOG.md missing")
        return 1
    print(f"AUDIT-PASS critic_fns={len(fc)} emitter_fns={len(fe)} "
          f"delib_fns={len(fd)} shared_beyond_main=0")
    return 0

if __name__ == "__main__":
    sys.exit(main())
