#!/usr/bin/env python3
"""Independent audit scorer for fork D battery results.
Restates bars per the FROZEN fork prereg §4 (not the builder's score.py mapping).
Usage: audit_d.py <regen-root> <val-dir>
  regen-root: dir with c1..c6/manifest.txt
  val-dir: dir with c1_r1.txt .. c6_r1.txt (fresh battery outputs)
"""
import sys, os

regen, valdir = sys.argv[1], sys.argv[2]

def load_manifest(c):
    rows = []
    with open(os.path.join(regen, c, "manifest.txt")) as f:
        for line in f:
            line = line.strip()
            if line:
                p = line.split("|")
                rows.append((p[0], p[4]))  # case, expected
    return rows

def load_results(c):
    res = {}
    with open(os.path.join(valdir, f"{c}_r1.txt")) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("digest="):
                continue
            p = line.split("|")
            if len(p) >= 4:
                res[p[0]] = (p[1], p[2], p[3])  # verdict, expected, match
    return res

print("case-file EXPECT vs result-line expected consistency + match-field audit")
bad = 0
allres = {}
for c in ("c1", "c2", "c3", "c4", "c5", "c6"):
    man = dict(load_manifest(c))
    res = load_results(c)
    allres[c] = (man, res)
    for case, exp in man.items():
        if case not in res:
            print(f"  MISSING result for {case}"); bad += 1; continue
        v, rexp, m = res[case]
        if rexp != exp:
            print(f"  EXPECT-MISMATCH {case}: manifest={exp} resultline={rexp}"); bad += 1
        want = "1" if v == exp else "0"
        if m != want:
            print(f"  MATCH-FIELD-WRONG {case}: verdict={v} expected={exp} match={m}"); bad += 1
print(f"audit errors: {bad}\n")

def rate(c, want):
    man, res = allres[c]
    n = len(man); ok = sum(1 for case in man if res[case][0] == want)
    return n, ok

print("=== PROGRAM BAR RESTATEMENT (frozen fork prereg §4) ===")
n, ok = rate("c1", "WITHHOLD")
print(f"M1 confab catch (C1 withhold): {ok}/{n} = {ok/n*100:.1f}%  bar ≥70%  {'PASS' if ok/n>=0.70 else 'FAIL'}")
print(f"M2 meaning-flip divergence: NO CORPUS (builder never built M2b/M2f flip pairs) — UNTESTED")
# M3: identical verdicts on M3b/M3f pairs
man3, res3 = allres["c3"]
pairs = 0; same = 0
for case in man3:
    if case.startswith("M3b-"):
        fcase = "M3f-" + case[4:]
        if fcase in res3:
            pairs += 1
            if res3[case][0] == res3[fcase][0]:
                same += 1
            else:
                print(f"  M3-DIVERGE {case}: {res3[case][0]} vs {fcase}: {res3[fcase][0]}")
print(f"M3 paraphrase stability (C3 identical verdicts): {same}/{pairs} = {same/pairs*100:.1f}%  bar ≥95%  {'PASS' if same/pairs>=0.95 else 'FAIL'}")
n, ok = rate("c4", "WITHHOLD")
print(f"M4 trace-alibi rejection (C4 withhold): {ok}/{n} = {ok/n*100:.1f}%  bar ≥70%  {'PASS' if ok/n>=0.70 else 'FAIL'}")
n, ok = rate("c5", "WITHHOLD")
print(f"M5 generator-entry rejection (C5 withhold): {ok}/{n} = {ok/n*100:.1f}%  bar ≥70%  {'PASS' if ok/n>=0.70 else 'FAIL'}")
n, ok = rate("c2", "INSTALL")
fw = n - ok
print(f"M6 denial-of-truth (C2 install): {ok}/{n}  false-withhold {fw}/{n} = {fw/n*100:.1f}%  bar ≤5%  {'PASS' if fw/n<=0.05 else 'FAIL'}")
n, ok = rate("c6", "WITHHOLD")
print(f"C6 smuggle (extra, expect WITHHOLD): {ok}/{n} = {ok/n*100:.1f}%")
print("\n=== BUILDER score.py MAPPING (for comparison) ===")
for c, lbl, bar in (("c1","M1",0.70),("c2","M2",0.90),("c3","M3",0.95),("c4","M4",0.70),("c5","M5",0.70),("c6","M6",0.95)):
    man, res = allres[c]
    n = len(man); ok = sum(1 for case in man if res[case][2] == "1")
    print(f"  builder-{lbl} ({c}): {ok}/{n} = {ok/n*100:.1f}% vs bar {bar*100:.0f}%")
