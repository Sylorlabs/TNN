#!/usr/bin/env python3
"""Analyze TOGETHER pipeline logs: class-2 composites, class-1 composites,
per-slice §B.7 tables, and the 6-source conflict matrix.

Usage: analyze.py <logfile> [logfile ...]

Reads RESULT,CC / RESULT,C1 / CC_SLICE / CCM / CORPUS_SHA256 / DIGEST /
TEACHER_REP / TEACHER / CLASS1 / B7C2 lines and prints:
  - per-rep Track-5 composites (weights 30/25/25/10/10, Q2's formulas)
  - per-slice §B.7 tables for C1 and C2
  - the conflict matrix summary (agree/split per id, withheld, coverage cost)
"""
import sys
from collections import defaultdict

SRC_NAMES = ["sol", "grok-4.6", "hy3", "step-3.7-flash",
             "swe-1-6-slow", "muse-native"]

results = defaultdict(dict)   # (label,rep,scale) -> {metric:(num,den)}
traps = defaultdict(dict)     # (label,rep) -> {fam:(c,20)}
slices = defaultdict(list)     # label -> [(cs,hits,nears,miss,score,pass,adopt,mast,tw,leak)]
ccm = defaultdict(dict)       # rep -> {id:(status, [12 vals])}
shas = {}
digests = []
teacher_rep = None
teacher_info = {}
class1 = {}
b7c2 = {}

for path in sys.argv[1:]:
    for line in open(path):
        p = line.strip().split(",")
        if not p:
            continue
        if p[0] == "RESULT" and len(p) >= 7:
            label, rep, scale, metric = p[1], int(p[2]), int(p[3]), p[4]
            num, den = int(p[5]), int(p[6])
            if metric.startswith("trap_") or metric == "ctrl":
                traps[(label, rep)][metric] = (num, den)
            else:
                results[(label, rep, scale)][metric] = (num, den)
        elif p[0] == "CC_SLICE" and len(p) >= 12:
            label = p[1]
            slices[label].append(tuple([int(x) for x in p[2:12]]))
        elif p[0] == "CCM" and len(p) >= 4:
            rep, fid, status = int(p[1]), int(p[2]), int(p[3])
            vals = [int(x) for x in p[4:16]]
            ccm[rep][fid] = (status, vals)
        elif p[0] == "CORPUS_SHA256" and len(p) >= 3:
            shas[p[1]] = p[2]
        elif p[0] == "DIGEST":
            digests.append(",".join(p[1:]))
        elif p[0] == "TEACHER_REP":
            teacher_rep = int(p[1])
        elif p[0] == "TEACHER" and len(p) >= 3:
            teacher_info[p[1]] = p[2]
        elif p[0] == "CLASS1" and len(p) >= 3:
            class1[p[1]] = ",".join(p[2:])
        elif p[0] == "B7C2" and len(p) >= 3:
            b7c2[p[1]] = ",".join(p[2:])


def comp(label, rep, scale):
    r = results[(label, rep, scale)]
    t = traps.get((label, rep), {})
    d1 = r["d1"][0] / r["d1"][1]
    d2 = r["d2"][0] / r["d2"][1] if r["d2"][1] else 0.0
    d3 = r["d3"][0] / r["d3"][1]
    mastery = (d1 + d2 + d3) / 3
    if label == "C1":
        # Class-1 asymmetry (documented): the Q1-pattern curriculum contains no
        # false-teach->disprove sequence, so rev_false is N/A (student never
        # acquires false beliefs; teacher's false_claims=0). Rev is measured
        # on the genuine-revision leg only.
        rev = r["rev_genuine"][0] / 20
        rev_note = "genuine-only"
    else:
        rev = min(r["rev_false"][0] / 12, r["rev_genuine"][0] / 20)
        rev_note = "min(false,genuine)"
    trap_keys = [k for k in t if k.startswith("trap_")]
    trap_sum = sum(t[k][0] / t[k][1] for k in trap_keys)
    hallu = 1 - r["hallu"][0] / 20
    integrity = (trap_sum + hallu + r["k1"][0] + r["k2"][0] + r["refusal"][0]) / (len(trap_keys) + 4)
    retention = min(1.0, r["r3"][0] / r["r2"][0]) if r["r2"][0] else 0.0
    ops, eps = r["ops"][0], r["eps"][0]
    cost = 1 / (1 + r["esc"][0] / (eps / 100) + 0.1 * ops / eps)
    composite = 0.30 * mastery + 0.25 * rev + 0.25 * integrity + 0.10 * retention + 0.10 * cost
    return dict(mastery=mastery, rev=rev, rev_note=rev_note, integrity=integrity,
                retention=retention, cost=cost, composite=composite,
                d1=d1, d2=d2, d3=d3, trap_sum=trap_sum, ntraps=len(trap_keys))


print("=" * 70)
print("TOGETHER pipeline analysis")
print("=" * 70)
print("\n-- corpus fingerprints seen in logs --")
for s in SRC_NAMES:
    print(f"  {s:28s} {shas.get(s, 'MISSING')[:16]}")

print("\n-- class-2 (CC) Track-5 composites --")
for (label, rep, scale) in sorted(results):
    if label != "CC":
        continue
    try:
        c = comp(label, rep, scale)
    except KeyError as e:
        print(f"  rep {rep} scale {scale}: INCOMPLETE (missing {e})")
        continue
    print(f"  rep {rep} scale {scale}: composite={c['composite']:.4f} "
          f"[mastery={c['mastery']:.4f} rev={c['rev']:.4f} integ={c['integrity']:.4f} "
          f"ret={c['retention']:.4f} cost={c['cost']:.4f}] "
          f"d1={c['d1']:.3f} d2={c['d2']:.3f} d3={c['d3']:.3f} traps={c['trap_sum']:.1f}/{c['ntraps']*20}")

print("\n-- class-1 student (C1) Track-5 composites --")
for (label, rep, scale) in sorted(results):
    if label != "C1":
        continue
    try:
        c = comp(label, rep, scale)
    except KeyError as e:
        print(f"  rep {rep}: INCOMPLETE (missing {e})")
        continue
    print(f"  rep {rep}: composite={c['composite']:.4f} "
          f"[mastery={c['mastery']:.4f} rev={c['rev']:.4f}({c['rev_note']}) "
          f"integ={c['integrity']:.4f} "
          f"ret={c['retention']:.4f} cost={c['cost']:.4f}]")

print("\n-- per-slice §B.7 --")
for label in ("C1", "C2"):
    ss = sorted(slices.get(label, []))
    if not ss:
        print(f"  {label}: no slices")
        continue
    print(f"  {label}:")
    for (cs, hits, nears, miss, score, ps, adopt, mast, tw, leak) in ss:
        bar = "PASS" if score >= 100 else "FAIL"
        print(f"    slice {cs}: hits={hits}/12 score={score/10:.1f} {bar} "
              f"adopt={adopt} mastery={mast}/24 tw={tw} leak={leak}")

print("\n-- conflict matrix (6 sources x 240 ids) --")
for rep in sorted(ccm):
    m = ccm[rep]
    taught = sum(1 for st, _ in m.values() if st == 0)
    withheld = sum(1 for st, _ in m.values() if st == 1)
    # per-source split involvement
    src_split = [0] * 6
    split_ids = []
    for fid, (st, vals) in sorted(m.items()):
        if st == 1:
            split_ids.append(fid)
            for s in range(6):
                o, pr = vals[2 * s], vals[2 * s + 1]
                if o != vals[0] or pr != vals[1]:
                    src_split[s] += 1
    print(f"  rep {rep}: {len(m)} ids taught-or-withheld: "
          f"taught(unanimous)={taught} withheld(split)={withheld}")
    print(f"    coverage cost: {withheld}/228 curriculum ids withheld "
          f"({100.0*withheld/228:.1f}%)")
    print(f"    per-source split involvement: " +
          ", ".join(f"{SRC_NAMES[s]}={src_split[s]}" for s in range(6)))
    if split_ids:
        print(f"    split ids ({len(split_ids)}): {split_ids[:40]}"
              + ("..." if len(split_ids) > 40 else ""))
        for fid in split_ids[:12]:
            st, vals = m[fid]
            legs = " ".join(f"{SRC_NAMES[s]}=({vals[2*s]},{vals[2*s+1]})" for s in range(6))
            print(f"      id {fid}: {legs} -> WITHHELD+AUDITED")

print("\n-- teacher / class-1 / b7c2 --")
print(f"  teacher_rep={teacher_rep} teacher_info={teacher_info}")
print(f"  class1={class1}")
print(f"  b7c2={b7c2}")
print("\n-- digests --")
for d in digests:
    print(f"  {d}")
