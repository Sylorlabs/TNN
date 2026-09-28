#!/usr/bin/env python3
# WS1-B analyzer. Gates G1/G2/G3, bars ACC/OPS/LED/MEM/CPA/NW/ST-FLAT.
# Writes tables to stdout and ws1/WS1B_ANALYSIS.txt.
import os, json, hashlib, statistics, sys

HOME = os.environ["HOME"]
WS = HOME + "/workspace/cognition_ws/ws1"
RUNS = WS + "/runs"
IV = HOME + "/workspace/tnn-lab/deliberation_depth/items_v2"
out = open(WS + "/WS1B_ANALYSIS.txt", "w")

def emit(s=""):
    print(s); out.write(s + "\n")

manifest = json.load(open(RUNS + "/manifest.json"))
by_cell = {m["cell"]: m for m in manifest}
fails = []

def loadj(p):
    return [json.loads(l) for l in open(p) if l.strip()]

# battery spec: (tag prefix, n, per-cell item list source)
BATS = {
    "admit": ("d_%s_admit", 248, "%s/admit.jsonl" % IV),
    "revoke": ("d_%s_revoke", 113, "%s/revoke.jsonl" % IV),
    "logic": ("d_%s_logic", 264, "%s/logic.jsonl" % IV),
    "trap": ("d_%s_trap", 127, "%s/trap.jsonl" % IV),
    "cost": ("d_%s_cost", 125, "%s/cost.jsonl" % IV),
    "rtd1": ("rt_%s", 14, None),
    "refusal": ("rf_%s", 60, None),
    "stress": ("s_%s", 1270, None),
}
# regime label used in pair bars: AUTO=autopilot, FORCED=tocap, (fastref for refusal auto)
CFGMAP = {"autopilot": "AUTO", "tocap": "FORCED", "fastref": "AUTO"}

def tags(bat, cfg):
    pref = BATS[bat][0] % cfg
    return ["%s_r%d" % (pref, r) for r in (1, 2, 3)]

# ---------- G1/G2 ----------
emit("=== G1/G2 ===")
g1bad = g2bad = total = 0
for bat in BATS:
    for cfg in (["autopilot", "tocap"] if bat != "refusal" else ["fastref", "tocap"]):
        ts = tags(bat, cfg)
        total += 1
        files = ["%s.res.jsonl", "%s.led.jsonl"] if cfg != "fastref" else ["%s.res.jsonl"]
        ok = True
        for f in files:
            h = set()
            for t in ts:
                p = "%s/%s" % (RUNS, f % t)
                h.add(by_cell[t]["files"].get(p))
            if len(h) != 1 or None in h:
                ok = False
        if not ok:
            g1bad += 1; fails.append("G1 %s %s" % (bat, cfg))
        sigs = set()
        for t in ts:
            ms = loadj("%s/%s.met.jsonl" % (RUNS, t))
            sigs.add(tuple((m["id"], m["ops"], m["rounds"], m["ev"], m["correct"]) for m in ms))
        if len(sigs) != 1:
            g2bad += 1; fails.append("G2 %s %s" % (bat, cfg))
emit("G1 failures: %d/%d  G2 failures: %d/%d" % (g1bad, total, g2bad, total))

# ---------- G3 ----------
emit("=== G3 (vs bill anchors) ===")
g3bad = 0
for bat in ["admit", "revoke", "logic", "trap", "cost"]:
    for cfg in ["autopilot", "tocap"]:
        rs = loadj("%s/%s_r1.res.jsonl" % (RUNS, BATS[bat][0] % cfg))
        acc = sum(r["correct"] for r in rs) / len(rs)
        if abs(acc - 1.0) > 0.001:
            g3bad += 1; fails.append("G3 %s %s acc=%.3f" % (bat, cfg, acc))
emit("G3 failures: %d/10" % g3bad)

# ---------- pooled metrics ----------
acc, opsm, ledm = {}, {}, {}
for bat in BATS:
    cfgs = ["autopilot", "tocap"] if bat != "refusal" else ["fastref", "tocap"]
    for cfg in cfgs:
        allm, allr = [], []
        for t in tags(bat, cfg):
            allm += loadj("%s/%s.met.jsonl" % (RUNS, t))
            allr += loadj("%s/%s.res.jsonl" % (RUNS, t))
        n = len(allr) // 3
        lab = (bat, CFGMAP[cfg])
        acc[lab] = sum(r["correct"] for r in allr) / len(allr)
        opsm[lab] = sum(m["ops"] for m in allm) / len(allm)
        # ledger bytes/item from r1 ledger file size
        if cfg != "fastref":
            lp = "%s/%s_r1.led.jsonl" % (RUNS, BATS[bat][0] % cfg)
            ledm[lab] = os.path.getsize(lp) / n
        else:
            ledm[lab] = 0.0

emit("=== accuracy (pooled 3 runs) ===")
for bat in BATS:
    row = {"AUTO": acc[(bat, "AUTO")], "FORCED": acc[(bat, "FORCED")]}
    emit("%-8s n=%4d AUTO=%.4f FORCED=%.4f" % (bat, BATS[bat][1], row["AUTO"], row["FORCED"]))

emit("=== mean ops/item ===")
for bat in BATS:
    emit("%-8s AUTO=%8.1f FORCED=%8.1f ratio(F/A)=%.2f" %
         (bat, opsm[(bat, "AUTO")], opsm[(bat, "FORCED")],
          opsm[(bat, "FORCED")] / max(opsm[(bat, "AUTO")], 1e-9)))

emit("=== mean ledger bytes/item ===")
for bat in BATS:
    emit("%-8s AUTO=%7.0f FORCED=%7.0f" % (bat, ledm[(bat, "AUTO")], ledm[(bat, "FORCED")]))

# MEM pressure per 1000 decisions
emit("=== memory pressure per 1000 decisions (bytes) ===")
for bat in ["admit", "trap", "refusal", "stress"]:
    for lab in ["AUTO", "FORCED"]:
        tot = 1000 * (18040 + ledm[(bat, lab)]) + 20 * 1024 * 1024
        emit("%-8s %-6s %d" % (bat, lab, int(tot)))

# CPA: ops per correct decision
emit("=== ops per correct decision (CPA) ===")
for bat in BATS:
    cfgs = ["autopilot", "tocap"] if bat != "refusal" else ["fastref", "tocap"]
    for cfg in cfgs:
        lab = (bat, CFGMAP[cfg])
        allm, allr = [], []
        for t in tags(bat, cfg):
            allm += loadj("%s/%s.met.jsonl" % (RUNS, t))
            allr += loadj("%s/%s.res.jsonl" % (RUNS, t))
        nc = sum(r["correct"] for r in allr)
        cpa = (sum(m["ops"] for m in allm) / nc) if nc else float("inf")
        emit("%-8s %-6s correct=%d/%d CPA=%.1f" % (bat, CFGMAP[cfg], nc, len(allr), cpa))

# ---------- ACC/OPS/LED bars with tie-bands ----------
emit("=== pair bars (AUTO vs FORCED) ===")
bands = {"admit": 0.40, "revoke": 0.88, "logic": 0.38, "trap": 0.79,
         "cost": 0.80, "rtd1": 7.14, "refusal": 1.67, "perception": 7.14}
# perception from frozen bill evidence (F1=6/14, F2=12/14)
perception = {"AUTO": 6/14, "FORCED": 12/14}
nw_viol = []
for bat in ["admit", "revoke", "logic", "trap", "cost", "rtd1", "refusal"]:
    a, f = acc[(bat, "AUTO")], acc[(bat, "FORCED")]
    d = (f - a) * 100
    b = bands[bat]
    v = "FORCED WINS" if d > b else ("AUTO WINS" if d < -b else "TIE")
    if d < -b:
        nw_viol.append((bat, d))
    emit("%-8s ACC: AUTO=%.4f FORCED=%.4f d=%+.2fpp band=%.2f -> %s" % (bat, a, f, d, b, v))
a, f = perception["AUTO"], perception["FORCED"]
d = (f - a) * 100
v = "FORCED WINS" if d > bands["perception"] else "TIE"
emit("%-8s ACC: AUTO=%.4f FORCED=%.4f d=%+.2fpp band=%.2f -> %s (frozen bill evidence)" %
     ("perception", a, f, d, bands["perception"], v))
emit("NEVER-WORSE violations: %s" % (nw_viol if nw_viol else "NONE"))

# ---------- ST-FLAT ----------
emit("=== ST-FLAT (stress leg, 10 passes) ===")
for cfg in ["autopilot", "tocap"]:
    ms = []
    for t in tags("stress", cfg):
        ms += loadj("%s/%s.met.jsonl" % (RUNS, t))
    by_pass = {}
    for m in ms:
        p = int(m["id"].rsplit("_p", 1)[1])
        by_pass.setdefault(p, []).append(m)
    n0 = len(by_pass[1])
    ops_pp = [sum(m["ops"] for m in by_pass[p]) / len(by_pass[p]) for p in range(1, 11)]
    # per-pass ledger bytes: sum byte lengths of ledger lines whose "item" is in this pass
    led_raw = open("%s/%s_r1.led.jsonl" % (RUNS, BATS["stress"][0] % cfg), "rb").read().split(b"\n")
    led_pp = []
    for p in range(1, 11):
        ids = set(m["id"] for m in by_pass[p])
        tot = 0
        for ln in led_raw:
            if not ln:
                continue
            try:
                it = json.loads(ln).get("item", "")
            except Exception:
                continue
            if it in ids:
                tot += len(ln) + 1
        led_pp.append(tot / len(by_pass[p]))
    xs = list(range(1, 11))

    def slope_pct(ys):
        mx = sum(xs) / 10
        my = sum(ys) / 10
        sl = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
        return sl, (sl / my * 100) if my else 0.0

    def verdict(pct):
        return "FLAT" if abs(pct) <= 2 else ("COMPOUNDING" if pct > 0 else "DECAYING")

    s_ops, p_ops = slope_pct(ops_pp)
    s_led, p_led = slope_pct(led_pp)
    emit("%-9s ops/item per pass:   %s" % (cfg, " ".join("%.1f" % v for v in ops_pp)))
    emit("%-9s ops slope=%+.3f/pass (%+.2f%%/pass) -> %s" % (cfg, s_ops, p_ops, verdict(p_ops)))
    emit("%-9s ledger B/item/pass: %s" % (cfg, " ".join("%.0f" % v for v in led_pp)))
    emit("%-9s ledger slope=%+.2f B/pass (%+.2f%%/pass) -> %s" % (cfg, s_led, p_led, verdict(p_led)))

emit("=== FAILS ===")
emit("total fails: %d %s" % (len(fails), fails if fails else ""))
out.close()
