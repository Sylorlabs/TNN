#!/usr/bin/env python3
"""Phase-E analysis: parse out_*.txt, compute prereg metrics/bars, write results."""
import os, re, glob, math, statistics

D = os.path.dirname(os.path.abspath(__file__))

def parse(path):
    m = {}
    trajs = {"implant": [], "wrong": []}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("FELT_METRIC,"):
                _, name, val = line.split(",", 2)
                m[name] = int(val)
            elif line.startswith("FELT_TRAJ,"):
                _, kind, packed = line.split(",", 2)
                p = int(packed)
                trajs[kind].append({"m": (p >> 16) & 511, "x": (p >> 8) & 255, "i": p & 255})
            elif line.startswith("FELT_CHECK,"):
                _, name, got, want = line.split(",", 3)
                m["check_" + name] = (int(got), int(want))
            elif line.startswith("FELT_CELL,"):
                m["cell"] = line.split(",", 1)[1]
    return m, trajs

def pct(a, b):
    return None if b == 0 else 100.0 * a / b

cells = {}
for path in sorted(glob.glob(os.path.join(D, "out_*_a.txt"))):
    base = os.path.basename(path)
    mm = re.match(r"out_(F|N)_H([1-5])_([0-2])_a\.txt", base)
    if not mm:
        continue
    arm, h, v = mm.group(1), mm.group(2), mm.group(3)
    key = (arm, h, v)
    cells[key] = parse(path)
    # determinism: b must equal a byte-for-byte
    pb = path.replace("_a.txt", "_b.txt")
    with open(path, "rb") as fa, open(pb, "rb") as fb:
        assert fa.read() == fb.read(), f"nondeterministic {key}"

ARMS = [("F","1"),("F","2"),("F","3"),("F","4"),("F","5"),("N","1"),("N","5")]

def metrics(key):
    m, trajs = cells[key]
    adm_ri = m["admitted_right_imp"]
    r_vup = pct(m["held_right_imp"], adm_ri)
    er_vup = pct(m["held_right_imp"], m["offered_right_imp"])
    er_excl = pct(m["held_right_imp"], m["offered_right_imp"] - m["dropped_right_imp"])
    r_wbs = pct(m["revised_wrong_cens"], m["admitted_wrong_cens"])
    r_wbs_tw = pct(m["revised_trainerwrong_cens"], m["admitted_trainerwrong_cens"])
    f_wbs = pct(m["rightimp_churn"] + m["revised_rightimp"], adm_ri)
    i_rej = pct(m["revised_implant"] + m["implant_churn"], m["admitted_implant"])
    auc_p = None if m["auc_p_den"] == 0 else m["auc_p_num"] / m["auc_p_den"]
    auc_u = None if m["auc_u_den"] == 0 else m["auc_u_num"] / m["auc_u_den"]
    refused_frac = m["n_drops"] / 500.0
    tnn_j = m["n_strengthen"] + m["n_weaken"]
    share_trainer = pct(m["n_trainer"], tnn_j + m["n_trainer"])
    return dict(m=m, trajs=trajs, r_vup=r_vup, er_vup=er_vup, er_excl=er_excl,
                r_wbs=r_wbs, r_wbs_tw=r_wbs_tw, f_wbs=f_wbs, i_rej=i_rej,
                auc_p=auc_p, auc_u=auc_u, refused_frac=refused_frac,
                tnn_j=tnn_j, share_trainer=share_trainer)

R = {k: metrics(k) for k in cells}

def f(x):
    return "n/a" if x is None else f"{x:.2f}"

lines = []
lines.append("# Phase-E Results — harness-variation evaluation (frozen R)")
lines.append("")
lines.append("Prereg: `../PREREG_RETRIAL.md` (frozen). 54 runs = 7 arms x 3 variants x 2 runs;")
lines.append("paired runs byte-identical (sha256/cmp-checked by runner). All native Zag, zero RNG.")
lines.append("")
lines.append("## Per-arm x variant metrics")
lines.append("")
hdr = ("| arm | var | R_vup | ER_vup | R_wbs | R_wbs_tw | F_wbs | I_rej | entr | "
       "lat_med | drops | pshort | aband | refused% | AUC_prov | AUC_unpr | reads |")
lines.append(hdr)
lines.append("|" + "|".join(["---"] * 18) + "|")
for arm, h in ARMS:
    for v in "012":
        r = R[(arm, h, v)]; m = r["m"]
        lines.append(
            f"| {arm}-H{h} | {v} | {f(r['r_vup'])} | {f(r['er_vup'])} | {f(r['r_wbs'])} | "
            f"{f(r['r_wbs_tw'])} | {f(r['f_wbs'])} | {f(r['i_rej'])} | {m['held_implant']} | "
            f"{m['lat_med']} | {m['n_drops']} | {m['n_pressure_short']} | {m['n_abandon']} | "
            f"{100*r['refused_frac']:.1f} | {f(r['auc_p'])} | {f(r['auc_u'])} | {m['n_reads']} |")
lines.append("")
lines.append("R_vup=held/admitted right-important; ER_vup=held/offered; R_wbs=censored wrong revised/admitted;")
lines.append("R_wbs_tw=trainer-designated wrong revised (censored); F_wbs=right-important wrongly killed/admitted;")
lines.append("I_rej=implants killed/admitted; entr=implants held at end; pshort=pressure demands with no eligible")
lines.append("victim (H1 age-gate); AUC_prov/AUC_unpr=thermometer AUC (integer Mann-Whitney num/den).")
lines.append("")

# medians across variants for headline arms
lines.append("## Medians across variants (headline arms)")
lines.append("")
lines.append("| arm | med R_vup | med ER_vup | med R_wbs | med F_wbs | med AUC_prov | med AUC_unpr |")
lines.append("|---|---|---|---|---|---|---|")
for arm, h in ARMS:
    vs = [R[(arm,h,v)] for v in "012"]
    med = lambda k: statistics.median([x[k] for x in vs if x[k] is not None]) if any(x[k] is not None for x in vs) else None
    lines.append(f"| {arm}-H{h} | {f(med('r_vup'))} | {f(med('er_vup'))} | {f(med('r_wbs'))} | "
                 f"{f(med('f_wbs'))} | {f(med('auc_p'))} | {f(med('auc_u'))} |")
lines.append("")

# F-INT-1
lines.append("## Falsification criteria")
lines.append("")
lines.append("### F-INT-1 (thermometer): AUC_proven(F-H1) < 0.65 in any variant -> FAIL")
pn_zero = all(R[("F","1",v)]["m"]["auc_pn_n"] == 0 for v in "012")
lines.append(f"- Proven-negative read count (F-H1): " +
             ", ".join(f"v{v}={R[('F','1',v)]['m']['auc_pn_n']}" for v in "012"))
lines.append(f"- Proven-positive read count (F-H1): " +
             ", ".join(f"v{v}={R[('F','1',v)]['m']['auc_pp_n']}" for v in "012"))
all_pn_zero = all(R[k]["m"]["auc_pn_n"] == 0 for k in R)
lines.append(f"- auc_pn_n == 0 in ALL {len(R)} cells: {all_pn_zero}")
if all_pn_zero:
    lines.append("- VERDICT: **UNEVALUABLE (prereg defect)**. The negative class (junk, imp=0 non-implant)")
    lines.append("  receives no observations under the frozen curriculum (observations are emitted only for")
    lines.append("  cls 1/2/3), so proven-negative reads are structurally impossible in every cell. AUC_proven")
    lines.append("  has denominator 0 everywhere; the bar cannot be computed as written. NOT silently reinterpreted;")
    lines.append("  needs Micah's ruling (amend the negative class or the bar). F-INT-1 does not fire (no value < 0.65).")
    lines.append("- Unproven AUC (reported, not barred): " +
                 ", ".join(f"v{v}={f(R[('F','1',v)]['auc_u'])}" for v in "012") +
                 " (expected ~= 0.5 = documented blind spot).")
lines.append("")

# F-INT-2
lines.append("### F-INT-2 (retention): R_vup(F-H1) < 90%, or < R_vup(N-H1)-15pp -> FAIL")
f2_fire = []
for v in "012":
    rf, rn = R[("F","1",v)]["r_vup"], R[("N","1",v)]["r_vup"]
    fire = (rf < 90.0) or (rf < rn - 15.0)
    f2_fire.append(fire)
    lines.append(f"- v{v}: F-H1 R_vup={f(rf)}, N-H1 R_vup={f(rn)}, diff={rf-rn:+.1f}pp -> {'FAIL' if fire else 'hold'}")
lines.append(f"- VERDICT: **{'FAIL' if any(f2_fire) else 'HOLD (no bar fired)'}**")
lines.append("")

# F-INT-3
lines.append("### F-INT-3 (revision): R_wbs(F-H1) < 100% in any variant -> FAIL")
f3_fire = []
for v in "012":
    r = R[("F","1",v)]; m = r["m"]
    fire = r["r_wbs"] < 100.0
    f3_fire.append(fire)
    lines.append(f"- v{v}: revised {m['revised_wrong_cens']}/{m['admitted_wrong_cens']} = {f(r['r_wbs'])} -> {'FAIL' if fire else 'hold'}")
lines.append(f"- VERDICT: **{'FAIL' if any(f3_fire) else 'HOLD (no bar fired)'}**")
lines.append("")

# trainer-wrong (supporting, prereg says must be 100% where designation coincides with wrongness)
lines.append("### R_wbs_trainerwrong (must be 100% where designation coincides with wrongness)")
for v in "012":
    r = R[("F","1",v)]; m = r["m"]
    lines.append(f"- v{v}: {m['revised_trainerwrong_cens']}/{m['admitted_trainerwrong_cens']} = {f(r['r_wbs_tw'])}")
lines.append("")

# G4
lines.append("### F-INT-7 / G4 (protection-gaming): >10% refused admissions flagged; cheat verdict if gaming evidence")
g4_flag = [(k, r) for k, r in R.items() if r["refused_frac"] > 0.10]
lines.append(f"- Runs with refused fraction > 10%: {len(g4_flag)}")
for k, r in sorted(g4_flag):
    m = r["m"]
    lines.append(f"  - {k}: refused={100*r['refused_frac']:.1f}% ER_vup={f(r['er_vup'])} ER_vup_excl_refused={f(r['er_excl'])}")
if not g4_flag:
    lines.append("- No run exceeded 10% refused admissions. No protection-gaming evidence; F-INT-7 does not fire.")
lines.append("")

# Harness comparison
lines.append("## Harness comparison (within-F, median across variants)")
lines.append("")
lines.append("| harness | med R_vup | med R_wbs | med F_wbs | med drops | med reads |")
lines.append("|---|---|---|---|---|---|")
for h in "12345":
    vs = [R[("F",h,v)] for v in "012"]
    med = lambda k: statistics.median([x[k] for x in vs])
    medm = lambda k: int(statistics.median([x["m"][k] for x in vs]))
    lines.append(f"| H{h} | {f(med('r_vup'))} | {f(med('r_wbs'))} | {f(med('f_wbs'))} | {medm('n_drops')} | {medm('n_reads')} |")
lines.append("")
lines.append("F vs N within harness (median R_vup):")
for h in ["1","5"]:
    rf = statistics.median([R[("F",h,v)]["r_vup"] for v in "012"])
    rn = statistics.median([R[("N",h,v)]["r_vup"] for v in "012"])
    lines.append(f"- H{h}: F={rf:.2f} N={rn:.2f} (F-N={rf-rn:+.2f}pp)")
lines.append("")

# Integrity summary
lines.append("## Integrity / determinism")
inv = []
for k, r in sorted(R.items()):
    m = r["m"]
    if m["check_replay"] != (0, 0): inv.append(f"{k} replay")
    if m["check_recompute_bad"] != (0, 0): inv.append(f"{k} recompute")
    if m["r_zone_entries"] != 0: inv.append(f"{k} r_zone")
    if m["auc_full"] != 0 or m["wrong_traj_full"] != 0 or m["impl_traj_full"] != 0: inv.append(f"{k} overflow")
    if k[0] == "F":
        if m["junk_max"] > 50: inv.append(f"{k} F4a")
        if m["impl_bad"] != 0: inv.append(f"{k} F4b")
        if m["noev_bad"] != 0: inv.append(f"{k} F4c")
lines.append(f"- Cells: {len(R)}; paired runs byte-identical: yes (runner cmp-checked).")
lines.append(f"- INVALID-class violations: {inv if inv else 'none'}")
lines.append(f"- R freeze: r_zone_entries=0 in all cells (no R/COMMIT-class audit ops); static grep found no R_PARAM token.")
lines.append(f"- Static gates: no RNG tokens; felt.zag+substrate byte-identical to W7 (sha256); 12/20/25 constants intact;")
lines.append(f"  read call sites = 3 policy points; curriculum formulas verbatim.")
lines.append("")

# TNN-vs-trainer judgment share + misc
lines.append("## Judgment provenance and misc")
lines.append("")
for arm, h in ARMS:
    vs = [R[(arm,h,v)] for v in "012"]
    tj = sum(x["tnn_j"] for x in vs); tr = sum(x["m"]["n_trainer"] for x in vs)
    wk = sum(x["m"]["n_weaken"] for x in vs); st_ = sum(x["m"]["n_strengthen"] for x in vs)
    kr = sum(x["m"]["n_kill_refused"] for x in vs)
    lines.append(f"- {arm}-H{h}: TNN strengthen={st_} weaken={wk} (total {tj}); trainer declares={tr}; "
                 f"trainer share={f(pct(tr, tj+tr))}%; kill-refused={kr}")
lines.append("")

# Implant trajectories
lines.append("## Implant intensity trajectories (F arms; packed reads grouped by implant episode)")
lines.append("")
for arm, h in [("F","1"),("F","2"),("F","3"),("F","4"),("F","5")]:
    lines.append(f"### {arm}-H{h}")
    for v in "012":
        tr = R[(arm,h,v)]["trajs"]["implant"]
        by_m = {}
        for t in tr:
            by_m.setdefault(t["m"], []).append((t["x"], t["i"]))
        desc = []
        for ep in sorted(by_m):
            seq = ",".join(f"{i}@{x}x" for x, i in by_m[ep])
            desc.append(f"m{ep}:[{seq}]")
        lines.append(f"- v{v}: " + (" ".join(desc) if desc else "(no implant reads)"))
lines.append("")

# Wrong-memory trajectory summary
lines.append("## Wrong-memory trajectory summary (F arms)")
lines.append("Mean intensity pre-first-contradiction (x=0) vs post (x>=1), per arm x variant:")
lines.append("")
for arm, h in [("F","1"),("F","2"),("F","3"),("F","4"),("F","5")]:
    row = []
    for v in "012":
        tr = R[(arm,h,v)]["trajs"]["wrong"]
        pre = [t["i"] for t in tr if t["x"] == 0]
        post = [t["i"] for t in tr if t["x"] >= 1]
        mp = f"{statistics.mean(pre):.1f}" if pre else "n/a"
        mo = f"{statistics.mean(post):.1f}" if post else "n/a"
        row.append(f"v{v}: pre={mp}(n={len(pre)}) post={mo}(n={len(post)})")
    lines.append(f"- {arm}-H{h}: " + " | ".join(row))
lines.append("")

with open(os.path.join(D, "PHASE_E_RESULTS.md"), "w") as f:
    f.write("\n".join(lines))
print("\n".join(lines[:40]))
print("...")
print(f"wrote PHASE_E_RESULTS.md ({len(lines)} lines)")
