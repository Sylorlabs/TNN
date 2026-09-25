#!/usr/bin/env python3
"""JOB1 red-team attack battery generator (frozen spec: ADDENDUM_V3B_JOB1_PRERUN_2026-09-25.md).
Pure Python, zero RNG. All batteries: 7-col TSV (id, fam, depth, f1, f5, release, correct),
depth-major row order (d1 rows, then d2, ...; id order within a depth). f1=931, f5=1000
(inert for m20/nopool=1; valid 35-grid coords).
Depths default {1,2,4,8,16}.
"""
import os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
DEPTHS = [1, 2, 4, 8, 16]
F1, F5 = 931, 1000

def rows(items, depths=DEPTHS):
    """items: list of (iid, fam, pattern[list of 0/1 per depth], relmap{depth:rel}).
    Returns list of row strings in depth-major order."""
    by_d = {d: [] for d in depths}
    for iid, fam, pat, relmap in items:
        assert len(pat) == len(depths), (iid, len(pat))
        for d, c in zip(depths, pat):
            rel = relmap.get(d, 1)
            by_d[d].append((iid, f"{iid}\t{fam}\t{d}\t{F1}\t{F5}\t{rel}\t{c}"))
    out = []
    for d in depths:
        for iid, r in sorted(by_d[d]):
            out.append(r)
    return out

def write(fn, rowlist):
    p = os.path.join(OUT, fn)
    with open(p, "w") as f:
        f.write("\n".join(rowlist) + "\n")
    print(f"{fn}: {len(rowlist)} rows")

def fam_items(fam, prefix, patterns, per=5, relmap=None):
    """patterns: list of (pname, plist). per items per pattern."""
    items = []
    for pname, plist in patterns:
        for i in range(per):
            items.append((f"{prefix}-{pname}-{i:02d}", fam, plist, relmap or {}))
    return items

# ---------------- RT-A: adversarial class distributions ----------------
# rta_low: true rates 0.0-0.4 ; rta_mid: 0.6 ; rta_rate1: 1.0
L1 = [1,0,0,0,0]  # 0.2
L2 = [0,0,0,0,1]  # 0.2 wrong-first
L3 = [0,0,0,0,0]  # 0.0
L4 = [1,0,1,0,0]  # 0.4
M1 = [1,0,1,0,1]  # 0.6
R1 = [1,1,1,1,1]  # 1.0
rta = []
rta += fam_items("rta_low", "rta-low", [("L1",L1),("L2",L2),("L3",L3),("L4",L4)])
rta += fam_items("rta_mid", "rta-mid", [("M1",M1)], per=20)
rta += fam_items("rta_rate1", "rta-r1", [("R1",R1)], per=20)
write("rta_s1.tsv", rows(rta))

# ---------------- RT-B: ceiling-latch ordering attacks ----------------
# identical multiset {C,C,C,W,W}, four orders
WF = [0,0,1,1,1]  # wrong-first
CF = [1,1,1,0,0]  # correct-first
WM = [1,0,1,0,1]  # wrong-middle
WA = [1,1,0,1,0]  # alternating-ish
rtb = fam_items("rtb", "rtb", [("wf",WF),("cf",CF),("wm",WM),("wa",WA)])
write("rtb_s1.tsv", rows(rtb))

# ---------------- RT-C: abstention-composition perturbations ----------------
# Clean design: ONLY always-correct (conf 950 stable) + always-wrong
# (950@d1, 0@d2+ stable) items, so item confs/correctness are CONSTANT
# across d2..d16 and the ONLY G driver is the abstention pattern.
# G(F,d) = -0.05 * (fraction correct among released) on d2..d16, so removing
# correct-950 items raises G (pure composition). Variants = sparse
# abstentions "near" the frozen M6-abstains-at-d4 pattern.
ALLC = [1,1,1,1,1]
ALLW = [0,0,0,0,0]
def rtc_battery(abst):
    # abst: {iid: {depth:0}} ; 12 always-correct + 12 always-wrong
    items = []
    for i in range(12):
        iid = f"rtc-C{i:02d}"
        items.append((iid, "rtc", ALLC, abst.get(iid, {})))
    for i in range(12):
        iid = f"rtc-W{i:02d}"
        items.append((iid, "rtc", ALLW, abst.get(iid, {})))
    return items
rtc_variants = {
    "rtc_base": {},
    "rtc_v1": {"rtc-C00": {4:0}},                          # 1 correct abstains d4
    "rtc_v2": {"rtc-C00": {8:0}},                          # 1 correct abstains d8
    "rtc_v3": {"rtc-C00": {4:0}, "rtc-C01": {4:0}, "rtc-C02": {4:0}},  # 3 correct d4
    "rtc_v4": {"rtc-W00": {4:0}},                          # 1 wrong abstains d4
    "rtc_v5": {"rtc-C00": {2:0}},                          # 1 correct abstains d2
    "rtc_v6": {f"rtc-C{i:02d}": {16:0} for i in range(12)},# all correct abstain d16 (bound probe)
}
for vname, abst in rtc_variants.items():
    write(f"{vname}.tsv", rows(rtc_battery(abst)))

# ---------------- RT-D: distributional shift at scale ----------------
# s1 diet: low 8 (2/pattern), r1 8, mid 8, norm 16 (8 all-C + 8 all-W)
def rtd_diet(low_mult=1, r1_mult=1):
    items = []
    n = 0
    for pname, plist in [("L1",L1),("L2",L2),("L3",L3),("L4",L4)]:
        for i in range(2*low_mult):
            items.append((f"rtd-low-{pname}-{i:02d}", "rtd_low", plist, {})); n+=1
    for i in range(8*r1_mult):
        items.append((f"rtd-r1-{i:02d}", "rtd_r1", R1, {})); n+=1
    for i in range(8):
        items.append((f"rtd-mid-{i:02d}", "rtd_mid", M1, {})); n+=1
    for i in range(8):
        items.append((f"rtd-nc-{i:02d}", "rtd_norm", R1, {})); n+=1
    for i in range(8):
        items.append((f"rtd-nw-{i:02d}", "rtd_norm", L3, {})); n+=1
    return items
write("rtd_s1.tsv", rows(rtd_diet(1,1)))

def replicate(items, reps, tag):
    out = []
    for r in range(reps):
        suf = f"#rtd{tag}r{r:03d}" if tag=="100" else f"#rtd{tag}r{r:02d}"
        for iid, fam, pat, relmap in items:
            out.append((iid+suf, fam, pat, relmap))
    return rows(out)
write("rtd_s10.tsv", replicate(rtd_diet(3,2), 10, "10"))    # shifted: low x3, r1 x2
write("rtd_s100.tsv", replicate(rtd_diet(5,3), 100, "100")) # shifted: low x5, r1 x3

# ---------------- RT-E: personal-ledger gaming channel ----------------
# E1 learning pattern (0->1), E2 fatigue pattern (1->0), each + all-C / all-W controls
LEARN = [0,0,1,1,1]
FATIG = [1,1,1,0,0]
rte_l = fam_items("rte_learn", "rte-l", [("learn",LEARN)], per=10)
rte_l += fam_items("rte_learn", "rte-lc", [("allC",R1)], per=10)
rte_l += fam_items("rte_learn", "rte-lw", [("allW",L3)], per=10)
write("rte_learn.tsv", rows(rte_l))
rte_f = fam_items("rte_fatigue", "rte-f", [("fatig",FATIG)], per=10)
rte_f += fam_items("rte_fatigue", "rte-fc", [("allC",R1)], per=10)
rte_f += fam_items("rte_fatigue", "rte-fw", [("allW",L3)], per=10)
write("rte_fatigue.tsv", rows(rte_f))
# E2 independence: solo batteries for one attacked item of each pattern
write("rte_solo_learn.tsv", rows([("rte-solo-learn","rte_solo",LEARN,{})]))
write("rte_solo_fatigue.tsv", rows([("rte-solo-fatigue","rte_solo",FATIG,{})]))

# ---------------- RT-F: item-identity (63-byte id truncation) ----------------
# nec_cmp_id compares at most 63 bytes then requires NUL; ids >63 chars NEVER
# match their own slot -> every observation is a "first observation" (conf 950).
# 5 always-wrong items with 70-char ids vs 5 short-id controls (same patterns).
def long_id(tag, i):
    return f"rtf-{tag}-" + "A"*60 + f"-{i:02d}"   # 4+1+3+1+60+1+3 = 73 chars
rtf = []
for i in range(5):
    rtf.append((long_id("long", i), "rtf_long", L3, {}))
for i in range(5):
    rtf.append((f"rtf-short-{i:02d}", "rtf_short", L3, {}))
for i in range(5):
    rtf.append((long_id("longC", i), "rtf_long", R1, {}))
for i in range(5):
    rtf.append((f"rtf-shortC-{i:02d}", "rtf_short", R1, {}))
r = rows(rtf)
write("rtf_collide.tsv", r)
print("long id len:", len(long_id("long", 0)), "short id len:", len("rtf-short-00"))
