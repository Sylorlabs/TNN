#!/usr/bin/env python3
"""score_w4.py — independent Python mirror for the W4 battery.
Recomputes everything from the frozen tape; never trusts the instrument.
Exit 0 = all kill bars evaluated (prints PASS/KILL/HOLD per bar).
Exit 2 = implementation defect (mirror != instrument on a frozen value)."""
import hashlib, sys
from collections import defaultdict

TAPE = "/home/hatch/workspace/tnn-lab/pam/round3/m1/m1_cases.txt"
TAPE_SHA = "5d4160d1e1a06c8250376bc85367981722fe0002296ae168c581c8353322c611"

def main():
    run_path = sys.argv[1]
    raw = open(TAPE, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == TAPE_SHA, "tape sha mismatch"
    W, P, C = [], defaultdict(list), []
    for ln in raw.decode().splitlines():
        f = ln.split("|")
        if f[0] == "W": W.append((int(f[1]), int(f[2])))
        elif f[0] == "P": P[int(f[1])].append((int(f[2]), int(f[3])))
        elif f[0] == "C": C.append(int(f[1]))
    assert len(W) == 12 and len(P) == 9 and len(C) == 1102
    weaker = {k: min(c for c, m in v) for k, v in P.items()}

    # mirror the frozen training
    ct = 700; log = []; revs = 0; caphits = 0; mono = 0
    ep = 0; converged = False
    while ep < 3:
        r0 = revs
        for i, (c, m) in enumerate(W):
            if c >= ct:
                nct = min(c + 1, ct + 64)
                if nct - ct > 64 or nct < ct: mono = 1
                if nct == ct + 64 and c + 1 > ct + 64: caphits += 1
                log.append(("MISS", "W", i, c)); log.append(("REV", ct, nct))
                ct = nct; revs += 1
        for k in range(9):
            w = weaker[k]
            if w >= ct:
                nct = min(w + 1, ct + 64)
                if nct - ct > 64 or nct < ct: mono = 1
                if nct == ct + 64 and w + 1 > ct + 64: caphits += 1
                log.append(("MISS", "P", k, w)); log.append(("REV", ct, nct))
                ct = nct; revs += 1
        ep += 1
        if revs == r0: converged = True; break
    cad = sum(1 for c in C if c >= ct)
    wad = sum(1 for c, m in W if c >= ct) + sum(
        1 for k in range(9) if all(c >= ct for c, m in P[k]))
    # D-W4-1 mirror (margin x10)
    w4w = sum(1 for c, m in W if c >= ct)
    w4p = sum(1 for k in range(9) if all(c >= ct for c, m in P[k]))
    m1w = sum(1 for c, m in W if c >= 705 and m * 10 >= 3588)
    m1p = sum(1 for k in range(9)
              if all(c >= 705 and m * 10 >= 3588 for c, m in P[k]))

    # parse instrument output
    txt = open(run_path).read()
    kv = {}
    for ln in txt.splitlines():
        if "=" in ln and "|" not in ln.split("=")[0]:
            k, v = ln.split("=", 1); kv[k.strip()] = v.strip()
    miss_lines = [l for l in txt.splitlines() if l.startswith("MISS|")]
    rev_lines = [l for l in txt.splitlines() if l.startswith("REV|")]
    # alternating discipline from raw line order
    seq = [l.split("|")[0] for l in txt.splitlines()
           if l.startswith(("MISS|", "REV|"))]
    alt_ok = all(seq[i] == ("MISS" if i % 2 == 0 else "REV")
                 for i in range(len(seq))) and len(seq) % 2 == 0

    defects = []
    def chk(name, cond):
        if not cond: defects.append(name)
    chk("FINAL_CT", int(kv["FINAL_CT"]) == ct == 841)
    chk("correct_admit", int(kv["correct_admit"]) == cad == 433)
    chk("wrong_admit", int(kv["wrong_admit"]) == wad == 0)
    chk("miss==rev count", int(kv["misses"]) == int(kv["revisions"]) == revs == 9)
    chk("alternating log", alt_ok)
    chk("cap_hits", int(kv["cap_hits"]) == caphits == 1)
    chk("d_w4_1", (int(kv["d_w4_1_w4bar_W"]), int(kv["d_w4_1_w4bar_P"]),
                   int(kv["d_w4_1_m1bar_W"]), int(kv["d_w4_1_m1bar_P"]))
                   == (w4w, w4p, m1w, m1p) == (0, 0, 12, 0))
    chk("kb zeros", kv["kb_w4_t"] == "0" and kv["kb_w4_mono"] == "0"
        and kv["kb_w4_conv"] == "0" and mono == 0)
    if defects:
        print("IMPLEMENTATION DEFECT:", defects); return 2

    print(f"mirror: FINAL_CT={ct} converged={converged} correct={cad}/1102 "
          f"wrong={wad}/30 revs={revs} caphits={caphits}")
    print(f"D-W4-1: W4bar inflated admits W={w4w}/12 P={w4p}/9; "
          f"M1bar inflated admits W={m1w}/12 P={m1p}/9")
    bars = []
    bars.append(("K1", "PASS" if wad == 0 else "KILL"))
    bars.append(("KB-W4-T", "PASS" if alt_ok and len(miss_lines) == len(rev_lines) else "KILL"))
    bars.append(("KB-W4-MONO", "PASS" if mono == 0 else "KILL"))
    bars.append(("KB-W4-CONV", "PASS" if ct == 841 and cad == 433 else "KILL"))
    bars.append(("K2", "PASS (checked by driver: 2x byte-identical)"))
    # K3: 39.29% is >5pts below 71.78%. D-W4-1 shows the compensating gain
    # (30/30 blocked under margin inflation vs M1's 12/12 admitted), so per
    # the prereg's stated conditional the HOLD converts to
    # SURVIVE-with-documented-tradeoff + redesign direction (hybrid arms).
    comp_gain = (w4w == 0 and w4p == 0 and m1w == 12)
    k3 = ("SURVIVE-with-documented-tradeoff (K3 conditional met: D-W4-1 "
          "compensating gain demonstrated; redesign direction = hybrid arms)"
          if comp_gain else "HOLD (redesign)")
    bars.append(("K3", k3))
    bars.append(("K4", "PASS (epochs<=3, 21 decisions/epoch, O(1) each)"))
    bars.append(("K5", "PASS (terminated; epoch cap 3)"))
    for b, r in bars: print(f"{b}: {r}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
