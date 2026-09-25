#!/usr/bin/env python3
"""RT-E analyses for NEC v3c: E1 exact-rule (sim vs binary), E2 independence
(solo vs in-battery byte-identical), E3 rise-selectivity (V2=0, conf <= stated).
Usage: rte_v3c.py <workdir>
Expects rt{v}_rte_{learn,fatigue,solo_learn,solo_fatigue}_A.tsv in workdir.
"""
import sys
sys.path.insert(0, ".")
from sim_v3c import run as sim_run

W = sys.argv[1]
BAT = "/home/hatch/workspace/nec_v3b/job1/batteries"
MODES = {"26": "m26", "27": "m27", "28": "m28"}

def load6(fn):
    d = {}
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        d[(c[0], int(c[2]))] = (int(c[4]), int(c[5]))
    return d

for v, mode in MODES.items():
    print(f"===== variant {v} =====")
    for bat in ("learn", "fatigue", "solo_learn", "solo_fatigue"):
        sim_out, _ = sim_run(f"{BAT}/rte_{bat}.tsv", mode)
        d = load6(f"{W}/rt{v}_rte_{bat}_A.tsv")
        mm = 0
        for line in sim_out:
            c = line.rstrip("\n").split("\t")
            if d[(c[0], int(c[2]))][1] != int(c[5]): mm += 1
        print(f"E1 {bat}: mismatches={mm}/{len(d)}")
    # E2: solo attacked item vs in-battery trajectory
    solo_l = load6(f"{W}/rt{v}_rte_solo_learn_A.tsv")
    batt_l = load6(f"{W}/rt{v}_rte_learn_A.tsv")
    solo_f = load6(f"{W}/rt{v}_rte_solo_fatigue_A.tsv")
    batt_f = load6(f"{W}/rt{v}_rte_fatigue_A.tsv")
    # attacked item id: the one present in both solo and battery
    # E2: solo attacked item vs same-pattern items in the battery.
    # The solo battery holds one item with the attacked pattern (same f1/f5);
    # its depth->conf trajectory must equal every attacked-pattern item's.
    def traj(d, iid):
        return sorted((dep, d[(iid, dep)][1]) for (i2, dep) in d if i2 == iid)
    for name, solo_iid, batt_pre, batt in (
            ("learn", "rte-solo-learn", "rte-l-learn-", batt_l),
            ("fatigue", "rte-solo-fatigue", "rte-f-", batt_f)):
        s = traj(solo_l if name == "learn" else solo_f, solo_iid)
        n_batt = sorted({i2 for (i2, _) in batt if i2.startswith(batt_pre)})
        same = all(traj(batt, i2) == s for i2 in n_batt)
        print(f"E2 {name}: solo={solo_iid} traj={s} vs {len(n_batt)} in-battery items identical={same}")
    # E3: V2=0 on learn/fatigue; conf never exceeds stated rule
    for bat in ("learn", "fatigue"):
        sim_out, dsim = sim_run(f"{BAT}/rte_{bat}.tsv", mode)
        stated = {(i, dp): cm // 1000 for i, dp, sr, cp, tp, pr, cm in dsim}
        d = load6(f"{W}/rt{v}_rte_{bat}_A.tsv")
        byid = {}
        for (iid, dep), (corr, conf) in d.items(): byid.setdefault(iid, []).append((dep, corr, conf))
        v2 = 0; exc = 0
        for iid, seq in byid.items():
            seq = sorted(seq)
            for i in range(len(seq) - 1):
                (d0, c0, f0), (d1, c1, f1) = seq[i], seq[i + 1]
                if c0 == "0" and c1 == "0" and f1 > f0: v2 += 1
            for (dep, corr, conf) in seq:
                if conf > stated[(iid, dep)]: exc += 1
        print(f"E3 {bat}: V2={v2} conf_exceeds_stated={exc}")
