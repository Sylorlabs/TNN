#!/usr/bin/env python3
"""rt_verify.py — verify G8 red-team outcomes against frozen PREREG §5 predictions.
Reads evidence/v{V}_w{W}_r1.txt RT lines and checks kill/survive verdicts.
Usage: ./rt_verify.py [evidencedir]
Exit 0 iff all predictions hold; prints a verdict table.
"""
import sys, os, glob

EV = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "evidence")

def rt_lines(path):
    """px -> (revoke_step, nuninstall, commit_policy, npromote, promote_policy, acount, real_rekeyed)"""
    d = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line.startswith("RT,"):
                continue
            p = line.split(",")
            # RT,px,revoke_step,nuninstall,commit_policy,npromote,promote_policy,acount,real_rekeyed
            d[p[1]] = tuple(int(x) for x in p[2:9])
    return d

# frozen predictions: variant -> (rt1_lying, rt2_honest, rt3_lying) ; "KILL" or "SURVIVE"
PRED = {
    "fl2": ("KILL", "KILL", "SURVIVE"),
    "c1":  ("KILL", "KILL", "SURVIVE"),
    "a0":  ("KILL", "KILL", "SURVIVE"),
    "a1":  ("KILL", "KILL", "SURVIVE"),
    "a2":  ("SURVIVE", "KILL", "SURVIVE"),
    "a3":  ("KILL", "KILL", "SURVIVE"),
    "b1":  ("KILL", "KILL", "SURVIVE"),
    "b2":  ("KILL", "KILL", "SURVIVE"),
    "c2":  ("KILL", "SURVIVE", "KILL"),
    "c3":  ("KILL", "SURVIVE", "SURVIVE"),
    "c4":  ("KILL", "KILL", "SURVIVE"),
}

def verdict_rt1(rec):
    # lying: KILL = lie promoted (nuninstall=0); SURVIVE = revoked (nuninstall>=1)
    _, nuninstall, _, _, _, _, _ = rec
    return "SURVIVE" if nuninstall >= 1 else "KILL"

def verdict_rt2(rec):
    # honest: KILL = false revocation (nuninstall>=1); SURVIVE = none
    _, nuninstall, _, _, _, _, _ = rec
    return "KILL" if nuninstall >= 1 else "SURVIVE"

def verdict_rt3(rec):
    # lying: KILL = never revoked (nuninstall=0); SURVIVE = revoked
    _, nuninstall, _, _, _, _, _ = rec
    return "SURVIVE" if nuninstall >= 1 else "KILL"

def px_for(variant, stream):
    # arm prefixes: variant arms use v{v}h_/v{v}l_; fl2 baseline uses fl2h_/fl2l_
    if variant == "fl2":
        return f"fl2{stream}_"
    return f"v{variant}{stream}_"

rows = []
fails = 0
for variant, (p1, p2, p3) in PRED.items():
    # locate the binary that carries this variant's arms: fl2 arms live in every binary;
    # use the variant's own binary (v{variant}) except fl2 which we read from v_c1's binary
    host = variant if variant != "fl2" else "c1"
    r1 = rt_lines(os.path.join(EV, f"v_{host}_w1_r1.txt"))
    r2 = rt_lines(os.path.join(EV, f"v_{host}_w2_r1.txt"))
    r3 = rt_lines(os.path.join(EV, f"v_{host}_w3_r1.txt"))
    o1, e1 = verdict_rt1(r1[px_for(variant, "l")]), p1
    o2, e2 = verdict_rt2(r2[px_for(variant, "h")]), p2
    o3, e3 = verdict_rt3(r3[px_for(variant, "l")]), p3
    # RT1 honest safety: 269 entries, zero revocations
    h1 = r1[px_for(variant, "h")]
    honest_ok = (h1[5] == 269 and h1[1] == 0)
    ok = (o1 == e1) and (o2 == e2) and (o3 == e3) and honest_ok
    if not ok:
        fails += 1
    rows.append((variant, o1, e1, o2, e2, o3, e3, honest_ok, ok,
                 r1[px_for(variant, "l")], r2[px_for(variant, "h")], r3[px_for(variant, "l")]))

print(f"{'variant':<8}{'RT1':<8}{'exp':<8}{'RT2':<8}{'exp':<8}{'RT3':<8}{'exp':<8}{'h269':<6}{'OK'}")
for (v, o1, e1, o2, e2, o3, e3, h_ok, ok, d1, d2, d3) in rows:
    print(f"{v:<8}{o1:<8}{e1:<8}{o2:<8}{e2:<8}{o3:<8}{e3:<8}{str(h_ok):<6}{'PASS' if ok else 'FAIL'}")
print()
print("detail (revoke_step,nuninstall,commit_policy,npromote,promote_policy,acount,real_rekeyed):")
for (v, o1, e1, o2, e2, o3, e3, h_ok, ok, d1, d2, d3) in rows:
    print(f"  {v}: RT1l={d1} RT2h={d2} RT3l={d3}")
sys.exit(1 if fails else 0)
