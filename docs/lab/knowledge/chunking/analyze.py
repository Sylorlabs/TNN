#!/usr/bin/env python3
"""Analyze chunking trial canonical logs. Deterministic; reads run1.log,
manifest.tsv, items.txt. Prints per-kind accuracy tables, kill bars KB1-KB4,
FIXED split fractions (from manifest offsets), cost ratios, W-sensitivity."""
import sys

WORK = "/home/hatch/workspace/tnn-lab/knowledge/chunking"

def load_manifest():
    man = {}
    with open(f"{WORK}/manifest.tsv") as f:
        header = f.readline()
        for line in f:
            p = line.rstrip("\n").split("\t")
            man[p[0]] = {"kind": p[1], "byte_len": int(p[2]),
                         "pos_marker": p[3], "pos_off": int(p[4]),
                         "neg_marker": p[5], "neg_off": int(p[6])}
    return man

def load_log(path):
    recs = {}
    with open(path) as f:
        for line in f:
            p = line.rstrip("\n").split("|")
            if len(p) == 6 and p[0].startswith("C_"):
                iid, label, arm, verdict = p[0], p[1], p[2], p[3]
                comps = int(p[4].split("=")[1]); chunks = int(p[5].split("=")[1])
                recs[(iid, arm)] = (label, verdict, comps, chunks)
    return recs

def acc(recs, man, arm, kinds):
    tot = ok = 0
    for iid, m in man.items():
        if m["kind"] not in kinds:
            continue
        label, verdict, _, _ = recs[(iid, arm)]
        tot += 1
        if verdict == label:
            ok += 1
    return ok, tot, (100.0 * ok / tot if tot else 0.0)

def main():
    man = load_manifest()
    recs = load_log(f"{WORK}/run1.log")
    arms = ["WHOLE", "FIXED64", "FIXED512", "ADAPTIVE", "DIAGUNION"]
    kindsets = {"S0": ["S0"], "S1": ["S1"], "S2": ["S2"], "S3": ["S3"],
                "LONG(S2+S3)": ["S2", "S3"], "LONGEST": ["L-S2", "L-S3"],
                "ALL": ["S0", "S1", "S2", "S3", "L-S2", "L-S3"]}

    print("=== per-kind accuracy (ok/total = %) ===")
    hdr = f"{'arm':<10}" + "".join(f"{k:>18}" for k in kindsets)
    print(hdr)
    table = {}
    for arm in arms:
        row = f"{arm:<10}"
        for k, ks in kindsets.items():
            ok, tot, pct = acc(recs, man, arm, ks)
            table[(arm, k)] = (ok, tot, pct)
            row += f"{ok:>8}/{tot:<3} {pct:>5.1f}"
        print(row)

    print("\n=== kill bars ===")
    # KB1: acc(ADAPTIVE) - acc(better of FIXED) >= 20pp on S2+S3
    a_ad = table[("ADAPTIVE", "LONG(S2+S3)")][2]
    a_fx = max(table[("FIXED64", "LONG(S2+S3)")][2],
               table[("FIXED512", "LONG(S2+S3)")][2])
    kb1 = a_ad - a_fx
    print(f"KB1: ADAPTIVE {a_ad:.1f}% - better-FIXED {a_fx:.1f}% = {kb1:+.1f}pp "
          f"(bar >= +20pp) -> {'MET' if kb1 >= 20 else 'NOT MET'}")
    # KB2: acc(WHOLE) - acc(FIXED64) >= 20pp on S2
    a_wh = table[("WHOLE", "S2")][2]
    a_f64 = table[("FIXED64", "S2")][2]
    kb2 = a_wh - a_f64
    print(f"KB2: WHOLE {a_wh:.1f}% - FIXED64 {a_f64:.1f}% = {kb2:+.1f}pp "
          f"(bar >= +20pp) -> {'MET' if kb2 >= 20 else 'NOT MET'}")
    # KB3: acc(WHOLE) >= 90% on LONGEST and zero crashes
    a_whl = table[("WHOLE", "LONGEST")][2]
    ok_l, tot_l, _ = table[("WHOLE", "LONGEST")][:3]
    print(f"KB3: WHOLE on LONGEST {ok_l}/{tot_l} = {a_whl:.1f}% "
          f"(bar >= 90%); crashes: 0 -> "
          f"{'MET' if a_whl >= 90 else 'NOT MET (accuracy clause; see prereg tension note)'}")
    # KB4: acc(ADAPTIVE) >= acc(WHOLE) on S3
    a_ad3 = table[("ADAPTIVE", "S3")][2]
    a_wh3 = table[("WHOLE", "S3")][2]
    print(f"KB4: ADAPTIVE {a_ad3:.1f}% >= WHOLE {a_wh3:.1f}% on S3 -> "
          f"{'MET' if a_ad3 >= a_wh3 else 'NOT MET'}")

    print("\n=== FIXED split fraction on S2 (POS/NEG in different windows) ===")
    for w, arm in ((64, "FIXED64"), (512, "FIXED512")):
        split = tot = 0
        for iid, m in man.items():
            if m["kind"] != "S2":
                continue
            tot += 1
            po = m["pos_off"] // w
            no = m["neg_off"] // w
            if po != no:
                split += 1
        print(f"{arm}: {split}/{tot} = {100.0*split/tot:.1f}% split")

    print("\n=== cost: total byte-comparisons per arm, mean ratio vs WHOLE ===")
    whole = {}
    arm_tot = {}
    for arm in arms:
        t = 0
        for iid in man:
            label, verdict, comps, chunks = recs[(iid, arm)]
            t += comps
            if arm == "WHOLE":
                whole[iid] = comps
        arm_tot[arm] = t
    for arm in arms:
        ratios = [recs[(iid, arm)][2] / whole[iid] for iid in man]
        mr = sum(ratios) / len(ratios)
        print(f"{arm}: total={t if False else arm_tot[arm]} "
              f"mean per-item ratio vs WHOLE = {mr:.2f}x")

    print("\n=== W-sensitivity (ADAPTIVE) ===")
    for w in (800, 1600, 3200):
        path = f"{WORK}/run_w{w}_1.log" if w != 1600 else f"{WORK}/run1.log"
        r = load_log(path)
        o2, t2, p2 = acc(r, man, "ADAPTIVE", ["S2", "S3"])
        o3, t3, p3 = acc(r, man, "ADAPTIVE", ["S3"])
        o0, t0, p0 = acc(r, man, "ADAPTIVE", ["S2"])
        print(f"W={w}: S2 {o0}/{t0} {p0:.1f}% | S3 {o3}/{t3} {p3:.1f}% | "
              f"S2+S3 {o2}/{t2} {p2:.1f}%")

if __name__ == "__main__":
    main()
