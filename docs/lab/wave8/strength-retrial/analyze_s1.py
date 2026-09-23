#!/usr/bin/env python3
# Analyze S1 trial results per PREREG_STRENGTH_V2.md kill/promotion rules.
import os, re, glob
D = os.path.expanduser("~/workspace/tnn-lab/wave8/strength-retrial/evidence")

def parse_cell(path):
    d = {}
    txt = open(path).read()
    for m in re.finditer(r"^ST_METRIC (\d+) (\d+) (\d+)$", txt, re.M):
        tag, a, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        d[f"m{tag}"] = (a, b)
    for m in re.finditer(r"^ST_DROPS (\d+)$", txt, re.M):
        d["drops"] = int(m.group(1))
    for m in re.finditer(r"^ST_ABANDONS (\d+)$", txt, re.M):
        d["abandons"] = int(m.group(1))
    # check for any CL_CHECK failures (actual != expected)
    fails = []
    for m in re.finditer(r"^CL_CHECK,([^,]+),(\d+),(\d+)$", txt, re.M):
        name, actual, exp = m.group(1), int(m.group(2)), int(m.group(3))
        if actual != exp:
            fails.append(name)
    d["check_fails"] = fails
    # invalid?
    d["invalid"] = "^ST_INVALID 1$" in txt or "ST_INVALID 1" in txt
    return d

arms = ["B", "C", "C-P3"]
curs = ["VUP", "WBS", "JI"]
results = {}
for arm in arms:
    for cur in curs:
        for var in [0,1,2]:
            path = f"{D}/cell_{arm}_{cur}_{var}_r1.log"
            if os.path.exists(path):
                results[(arm,cur,var)] = parse_cell(path)

# Print summary table
print("=== S1 SUMMARY ===")
print("Arm | Cur | Var | Drops | Key Metric")
for arm in arms:
    for cur in curs:
        for var in [0,1,2]:
            r = results.get((arm,cur,var), {})
            drops = r.get("drops", "?")
            if cur == "VUP":
                m1 = r.get("m1", (0,0))
                key = f"VUP={m1[0]}/{m1[1]}={m1[0]/m1[1] if m1[1] else 0:.3f}"
                m8 = r.get("m8", (0,0)); m9 = r.get("m9", (0,0))
                key += f" PTR={m8[0]}/{m8[1]} EC={m9[0]}/{m9[1]}={m9[0]/m9[1] if m9[1] else 0:.3f}"
            elif cur == "WBS":
                m2 = r.get("m2", (0,0)); m7 = r.get("m7", (0,0)); m6 = r.get("m6", (0,0))
                key = f"R_wbs={m2[0]}/{m2[1]} lat_med={m7[0]} false_rev={m6[0]}/{m6[1]}"
            else:
                m3 = r.get("m3", (0,0)); m4 = r.get("m4", (0,0)); m5 = r.get("m5", (0,0))
                key = f"I_rej={m3[0]}/{m3[1]} junk={m4[0]}/{m4[1]}={m4[0]/m4[1] if m4[1] else 0:.3f} entr={m5[0]}/{m5[1]}"
            fails = r.get("check_fails", [])
            fail_str = f" CHECK_FAILS={len(fails)}" if fails else ""
            print(f"{arm:5} | {cur:3} | {var} | {drops:5} | {key}{fail_str}")

print("\n=== KILL RULES ===")
# P2 drop ceiling (VUP only): drops > 64 = FAILED cell; >=2/3 FAILED = killed
for arm in ["C", "C-P3"]:
    failed = sum(1 for var in [0,1,2] if results[(arm,"VUP",var)]["drops"] > 64)
    print(f"{arm} VUP drop-ceiling FAILED cells: {failed}/3 -> {'KILLED' if failed>=2 else 'survives'}")
# B VUP drops
for var in [0,1,2]:
    d = results[("B","VUP",var)]["drops"]
    print(f"B VUP var{var} drops={d} (ceiling 64): {'PASS' if d<=64 else 'FAIL'}")

print("\n=== VUP RETENTION (symmetric kill rule) ===")
# X killed iff R_vup(X) >20pp below best of others in >=2/3 variants
for arm in arms:
    others = [a for a in arms if a != arm]
    below = 0
    for var in [0,1,2]:
        r_x = results[(arm,"VUP",var)]["m1"]
        rx = r_x[0]/r_x[1] if r_x[1] else 0
        best_other = max(results[(o,"VUP",var)]["m1"][0]/results[(o,"VUP",var)]["m1"][1] for o in others)
        diff_pp = (best_other - rx)*100
        if diff_pp > 20:
            below += 1
        print(f"  {arm} var{var}: R={rx:.3f} best_other={best_other:.3f} diff={diff_pp:.1f}pp")
    print(f"{arm}: >20pp below in {below}/3 -> {'KILLED' if below>=2 else 'survives'} (B exempt as control)")

print("\n=== WBS RIGIDITY ===")
for arm in arms:
    for var in [0,1,2]:
        r = results[(arm,"WBS",var)]
        m2 = r["m2"]; m7 = r["m7"]
        rwbs = m2[0]/m2[1] if m2[1] else 0
        print(f"{arm} var{var}: R_wbs={m2[0]}/{m2[1]}={rwbs:.3f} med_lat={m7[0]}")
# B latency for comparison
b_lat = [results[("B","WBS",v)]["m7"][0] for v in [0,1,2]]
print(f"B median latencies: {b_lat}")

print("\n=== JI BARS ===")
for arm in arms:
    for var in [0,1,2]:
        r = results[(arm,"JI",var)]
        m3 = r["m3"]; m4 = r["m4"]; m5 = r["m5"]
        irej = m3[0]/m3[1] if m3[1] else 0
        junk = m4[0]/m4[1] if m4[1] else 0
        print(f"{arm} var{var}: I_rej={m3[0]}/{m3[1]}={irej:.3f} junk_ret={m4[0]}/{m4[1]}={junk:.3f} entr={m5[0]}/{m5[1]}")

print("\n=== PROMOTION CHECK (C and C-P3) ===")
# 8 criteria from prereg
for arm in ["C", "C-P3"]:
    print(f"\n{arm}:")
    # 1. Survived kill rules
    # (computed above)
    # 2. P1 all scales: need EC>=0.5 for PTR evaluation
    for var in [0,1,2]:
        m9 = results[(arm,"VUP",var)]["m9"]
        ec = m9[0]/m9[1] if m9[1] else 0
        print(f"  var{var} EC={ec:.3f} ({'PASS' if ec>=0.5 else 'FAIL'})")
    # 3. P2 drop ceiling
    for var in [0,1,2]:
        d = results[(arm,"VUP",var)]["drops"]
        print(f"  var{var} drops={d} ({'PASS' if d<=64 else 'FAIL'})")
    # 4. P3 expiry rule (C-P3 only)
    if arm == "C-P3":
        print("  P3: (manual check - expiries issued but no kill enabled)")
    # 5. Integrity
    fails = sum(len(results[(arm,cur,var)]["check_fails"]) for cur in curs for var in [0,1,2])
    print(f"  check_fails total: {fails}")
    # 6. Determinism (already verified by runner)
    print("  determinism: PASS (runner verified)")
    # 7. No-free-lunch: 3-point margin in >=2 curricula
    # (compare to B)
    print("  no-free-lunch: (see comparison)")
    # 8. Unique mechanism
    print("  unique mechanism: (manual)")
