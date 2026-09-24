#!/usr/bin/env python3
"""D1 discipline metrics per prereg §4-5. Pure analysis, zero RNG."""
import json
from collections import defaultdict

D = "/home/hatch/workspace/tnn-lab/deliberation_depth/depth1_discipline"
FORKS = ["d1a", "d1b", "d1c", "d1d", "d1e", "depth2"]
BATS = ["trap", "admit", "revoke", "logic", "rt_d1"]

part = {}
for l in open(f"{D}/analysis/partition.jsonl"):
    d = json.loads(l)
    part[d["id"]] = d["partition"]

def load(fork, b):
    rows = []
    for l in open(f"{D}/results/matrix/{fork}_{b}_r1.jsonl"):
        rows.append(json.loads(l))
    return rows

# per fork x battery metrics
M = {}
for fork in FORKS:
    for b in BATS:
        rows = load(fork, b)
        n = len(rows)
        acc = sum(r["correct"] for r in rows) / n
        withhold = sum(1 for r in rows if r["verdict"] == "WITHHOLD") / n
        cw = sum(1 for r in rows if r["correct"] == 0 and r["confidence"] >= 800) / n
        cc = [r["confidence"] for r in rows if r["correct"] == 1]
        cw_ = [r["confidence"] for r in rows if r["correct"] == 0]
        mc_c = sum(cc) / len(cc) if cc else 0
        mc_w = sum(cw_) / len(cw_) if cw_ else 0
        veto = sum(1 for r in rows if r.get("veto", 0) == 1) / n if "veto" in rows[0] else 0
        # per-partition accuracy
        s_rows = [r for r in rows if part[r["id"]] == "SINGLE"]
        m_rows = [r for r in rows if part[r["id"]] == "MULTI"]
        s_acc = sum(r["correct"] for r in s_rows) / len(s_rows) if s_rows else None
        m_acc = sum(r["correct"] for r in m_rows) / len(m_rows) if m_rows else None
        M[(fork, b)] = dict(n=n, acc=acc, withhold=withhold, cw=cw,
                            mc_c=mc_c, mc_w=mc_w, veto=veto,
                            s_acc=s_acc, m_acc=m_acc)

# false veto rate on admit+revoke+logic: P(vetoed and base-verdict-correct)
# base for C = A's verdict; base for E = B's verdict
base = {}
for b in ["admit", "revoke", "logic"]:
    for r in load("d1a", b):
        base[("d1a", r["id"])] = r["correct"]
    for r in load("d1b", b):
        base[("d1b", r["id"])] = r["correct"]

fv = {}
for fork, bfork in [("d1c", "d1a"), ("d1e", "d1b")]:
    tot = 0
    fv_n = 0
    for b in ["admit", "revoke", "logic"]:
        for r in load(fork, b):
            tot += 1
            if r.get("veto", 0) == 1 and base[(bfork, r["id"])] == 1:
                fv_n += 1
    fv[fork] = fv_n / tot if tot else 0

# red-team confident-wrong per fork on rt_d1
rt_cw = {}
for fork in ["d1b", "d1c", "d1d", "d1e"]:
    rows = load(fork, "rt_d1")
    bad = [r["id"] for r in rows if r["correct"] == 0 and r["confidence"] >= 800]
    rt_cw[fork] = bad

# cosmetic check: disagreement(C/E, depth2) = fraction of items with different verdict
dis = {}
for fork in ["d1c", "d1e"]:
    tot = 0
    diff = 0
    for b in BATS:
        ra = {r["id"]: r["verdict"] for r in load(fork, b)}
        rb = {r["id"]: r["verdict"] for r in load("depth2", b)}
        for i, v in ra.items():
            tot += 1
            if v != rb[i]:
                diff += 1
    dis[fork] = diff / tot

print("=== accuracy ===")
print("fork     " + "".join(f"{b:>10}" for b in BATS))
for fork in FORKS:
    print(f"{fork:>8} " + "".join(f"{M[(fork,b)]['acc']:10.3f}" for b in BATS))

print("\n=== confident-wrong rate (wrong & conf>=800) ===")
print("fork     " + "".join(f"{b:>10}" for b in BATS))
for fork in FORKS:
    print(f"{fork:>8} " + "".join(f"{M[(fork,b)]['cw']:10.3f}" for b in BATS))

print("\n=== withhold rate ===")
print("fork     " + "".join(f"{b:>10}" for b in BATS))
for fork in FORKS:
    print(f"{fork:>8} " + "".join(f"{M[(fork,b)]['withhold']:10.3f}" for b in BATS))

print("\n=== mean conf | correct / mean conf | wrong (trap) ===")
for fork in FORKS:
    print(f"{fork}: {M[(fork,'trap')]['mc_c']:.1f} / {M[(fork,'trap')]['mc_w']:.1f}")

print("\n=== veto rate (trap / rt_d1) ===")
for fork in FORKS:
    print(f"{fork}: trap={M[(fork,'trap')]['veto']:.3f} rt_d1={M[(fork,'rt_d1')]['veto']:.3f}")

print("\nfalse_veto_rate (admit+revoke+logic): d1c=%.4f d1e=%.4f" % (fv["d1c"], fv["d1e"]))
print("red-team confident-wrong items:")
for fork, bad in rt_cw.items():
    print(f"  {fork}: {bad if bad else 'NONE'}")
print("disagreement vs depth2: d1c=%.3f d1e=%.3f" % (dis["d1c"], dis["d1e"]))

# kill bars
print("\n=== KILL BARS ===")
tA = M[("d1a", "trap")]["acc"]
tB = M[("d1b", "trap")]["acc"]
b_ok = (tB - tA) >= 0.10
b_nodrop = all(M[("d1b", b)]["acc"] - M[("d1a", b)]["acc"] > -0.02 for b in ["admit", "revoke", "logic"])
print(f"B: trap {tA:.3f}->{tB:.3f} (Δ={tB-tA:+.3f}, need ≥+0.10): {'PASS' if b_ok else 'FAIL'}")
for b in ["admit", "revoke", "logic"]:
    d = M[("d1b", b)]["acc"] - M[("d1a", b)]["acc"]
    print(f"   {b}: Δ={d:+.4f} (drop ≤0.02): {'ok' if d > -0.02 else 'DROP'}")
print(f"B SURVIVES: {b_ok and b_nodrop}")

cwA = M[("d1a", "trap")]["cw"]
cwC = M[("d1c", "trap")]["cw"]
c_ok = cwC <= 0.5 * cwA
c_fv = fv["d1c"] <= 0.05
print(f"C: trap_cw {cwA:.3f}->{cwC:.3f} (need ≤{0.5*cwA:.3f}): {'PASS' if c_ok else 'FAIL'}; false_veto={fv['d1c']:.4f} (≤0.05): {'PASS' if c_fv else 'FAIL'}")
print(f"C SURVIVES: {c_ok and c_fv}")

mwA = M[("d1a", "trap")]["mc_w"]
mwD = M[("d1d", "trap")]["mc_w"]
mcA = M[("d1a", "trap")]["mc_c"]
mcD = M[("d1d", "trap")]["mc_c"]
d_ok1 = mwD <= 0.6 * mwA
d_ok2 = mcD >= 0.9 * mcA
print(f"D: mean_conf_wrong {mwA:.1f}->{mwD:.1f} (need ≤{0.6*mwA:.1f}): {'PASS' if d_ok1 else 'FAIL'}")
print(f"D: mean_conf_correct {mcA:.1f}->{mcD:.1f} (need ≥{0.9*mcA:.1f}): {'PASS' if d_ok2 else 'FAIL'}")
print(f"D SURVIVES: {d_ok1 and d_ok2}")

e_ok = b_ok and b_nodrop and c_ok and c_fv and d_ok1 and d_ok2
# E must meet B, C, D bars jointly — recompute with E's numbers
tE = M[("d1e", "trap")]["acc"]
eb = (tE - tA) >= 0.10 and all(M[("d1e", b)]["acc"] - M[("d1a", b)]["acc"] > -0.02 for b in ["admit", "revoke", "logic"])
cwE = M[("d1e", "trap")]["cw"]
ec = (cwE <= 0.5 * cwA) and (fv["d1e"] <= 0.05)
mwE = M[("d1e", "trap")]["mc_w"]
mcE = M[("d1e", "trap")]["mc_c"]
ed = (mwE <= 0.6 * mwA) and (mcE >= 0.9 * mcA)
print(f"E: B-bar {eb}, C-bar {ec} (cw {cwA:.3f}->{cwE:.3f}, fv={fv['d1e']:.4f}), D-bar {ed} (mc_w {mwA:.1f}->{mwE:.1f}, mc_c {mcA:.1f}->{mcE:.1f})")
print(f"E SURVIVES: {eb and ec and ed}")

print("\nRed-team kill (confident-wrong on ANY rt_d1 item kills B-E):")
for fork in ["d1b", "d1c", "d1d", "d1e"]:
    print(f"  {fork}: {'KILLED' if rt_cw[fork] else 'survives'}")

json.dump({"metrics": {f"{k[0]}/{k[1]}": v for k, v in M.items()},
           "false_veto": fv, "rt_cw": rt_cw, "disagreement": dis},
          open(f"{D}/analysis/metrics.json", "w"), indent=1)
print("\nwrote analysis/metrics.json")
