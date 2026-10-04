#!/usr/bin/env python3
"""Mechanical analysis of results_main.json: applies every preregistered
kill bar / decision rule verbatim. No interpretation, no rescue language.
Prints tables + decisions; writes verdict_summary.json.
"""
import json, sys

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
TNAMES = {"colordisc": "color-disc", "colorconst": "color-const",
          "shapetrans": "shape", "pitchdisc": "pitch",
          "timbredisc": "timbre", "motiondir": "motion"}

def main(path):
    r = json.load(open(path))
    budgets = r["budgets"]
    tf, adv, mem = r["test_fresh"], r["adv_r1"], r["memory"]
    ops = r["ops_test_fresh"]

    out = {"budgets": budgets}
    print("# SENSES-REMATCH learning curves (TEST-FRESH, fitted)\n")
    print("| budget | " + " | ".join("A " + TNAMES[t] for t in TASKS) +
          " | A mean | " + " | ".join("B " + TNAMES[t] for t in TASKS) + " | B mean |")
    print("|" + "---|" * 14)
    for b in budgets:
        ra = ["%.1f" % (100 * tf[b]["A"]["tasks"][t]["accuracy"]) for t in TASKS]
        rb = ["%.1f" % (100 * tf[b]["B"]["tasks"][t]["accuracy"]) for t in TASKS]
        ma = "%.1f" % (100 * tf[b]["A"]["mean"])
        mb = "%.1f" % (100 * tf[b]["B"]["mean"])
        print("| %s | %s | %s | %s | %s |" % (b, " | ".join(ra), ma,
                                              " | ".join(rb), mb))
        out.setdefault("means", {})[b] = {
            "A": tf[b]["A"]["mean"], "B": tf[b]["B"]["mean"]}

    # KB1: mean < 60% kills approach (TEST-FRESH)
    print("\n## KB1 (mean >= 60% on TEST-FRESH)")
    kb1 = {}
    for b in budgets:
        for ap in ("A", "B"):
            kb1.setdefault(ap, {})[b] = tf[b][ap]["mean"] >= 0.60
    for ap in ("A", "B"):
        print("  %s: %s" % (ap, {b: ("ALIVE" if kb1[ap][b] else "KILLED")
                                 for b in budgets}))
    out["kb1"] = kb1

    # KB2: higher mean wins; tie iff |d| < 2pp AND ops ratio < 2x
    print("\n## KB2 (winner by higher mean; tie iff |d|<2pp and ops<2x)")
    kb2 = {}
    ops_ratio = max(ops["A"], ops["B"]) / min(ops["A"], ops["B"])
    print("  ops TEST-FRESH: A=%d B=%d ratio=%.2fx" %
          (ops["A"], ops["B"], ops_ratio))
    for b in budgets:
        d = tf[b]["B"]["mean"] - tf[b]["A"]["mean"]
        if abs(d) < 0.02 and ops_ratio < 2.0:
            w = "TIE"
        else:
            w = "B" if d > 0 else "A"
        kb2[b] = {"winner": w, "delta_pp": 100 * d}
        print("  %s: delta=%+.1fpp winner=%s" % (b, 100 * d, w))
    out["kb2"] = kb2
    out["ops"] = ops
    out["ops_ratio"] = ops_ratio

    # KB3: winner's TEST_FRESH->ADV_R1 drop > 25pp => fragile winner
    print("\n## KB3 (winner drop on ADV-R1 > 25pp => fragile)")
    kb3 = {}
    for b in budgets:
        w = kb2[b]["winner"]
        if w == "TIE":
            kb3[b] = {"winner": "TIE", "drop_pp": None, "fragile": False}
            print("  %s: tie, no winner fragility" % b)
            continue
        drop = 100 * (tf[b][w]["mean"] - adv[b][w]["mean"])
        fragile = drop > 25.0
        kb3[b] = {"winner": w, "drop_pp": drop, "fragile": fragile}
        print("  %s: %s drop=%.1fpp fragile=%s" % (b, w, drop, fragile))
    out["kb3"] = kb3

    # robustness D
    print("\n## Robustness D = TEST-FRESH mean - ADV-R1 mean")
    rob = {}
    for b in budgets:
        da = 100 * (tf[b]["A"]["mean"] - adv[b]["A"]["mean"])
        db = 100 * (tf[b]["B"]["mean"] - adv[b]["B"]["mean"])
        rob[b] = {"D_A": da, "D_B": db, "gap": da - db}
        print("  %s: D_A=%.1fpp D_B=%.1fpp (D_A-D_B)=%+.1fpp" % (b, da, db, da - db))
    out["robustness"] = rob

    # KB4
    print("\n## KB4 (adv false-install rate <= 10%%)")
    kb4 = {}
    for b in budgets:
        for ap in ("A", "B"):
            m = mem[b][ap]
            rate = m["adv_false_install_rate"]
            kb4.setdefault(ap, {})[b] = {
                "rate": rate, "pass": rate <= 0.10,
                "adv_installs": m["adv_installs"],
                "adv_false": m["adv_false_installs"]}
            print("  %s %s: %.1f%% (%d/%d) %s" %
                  (b, ap, 100 * rate, m["adv_false_installs"],
                   m["adv_installs"], "PASS" if rate <= 0.10 else "FAIL"))
    out["kb4"] = kb4

    # plateau: earliest budget from which all subsequent steps < 1pp
    print("\n## Plateau (earliest budget after which every step |d|<1pp)")
    plat = {}
    for ap in ("A", "B"):
        means = [tf[b][ap]["mean"] for b in budgets]
        steps = [abs(means[i + 1] - means[i]) for i in range(len(means) - 1)]
        p = None
        for i in range(len(budgets)):
            if all(s < 0.01 for s in steps[i:]):
                p = budgets[i]
                break
        plat[ap] = {"plateau": p,
                    "steps_pp": [100 * s for s in steps]}
        print("  %s: plateau=%s steps=%s" %
              (ap, p, ["%.1fpp" % (100 * s) for s in steps]))
    out["plateau"] = plat

    # crossing: budgets where B_mean >= A_mean
    cross = [b for b in budgets
             if tf[b]["B"]["mean"] >= tf[b]["A"]["mean"]]
    print("\n## Crossing (B_mean >= A_mean): %s" % cross)
    out["crossing"] = cross

    # KB6 at T* = highest completed budget >= T3
    done_ge_t3 = [b for b in budgets if b in ("T3", "T4")]
    ts = done_ge_t3[-1] if done_ge_t3 else None
    print("\n## KB6 at T*=%s" % ts)
    kb6 = {"T*": ts, "decision": None}
    if ts:
        d = tf[ts]["B"]["mean"] - tf[ts]["A"]["mean"]
        bmean = tf[ts]["B"]["mean"]
        confirmed = (d >= 0.02) and (bmean >= 0.60)
        kb6.update({"delta_pp": 100 * d, "B_mean": bmean,
                    "confirmed": confirmed,
                    "decision": ("CROSSOVER CONFIRMED" if confirmed
                                 else "B STAYS DEAD")})
        print("  delta=%+.1fpp B_mean=%.1f%% -> %s" %
              (100 * d, 100 * bmean, kb6["decision"]))
    out["kb6"] = kb6

    # robustness verdict at T*
    print("\n## Robustness verdict at T*=%s" % ts)
    rv = {"T*": ts, "supported": None}
    if ts:
        t0, tstar = "T0", ts
        cond = (rob[tstar]["D_B"] < rob[tstar]["D_A"] and
                rob[tstar]["gap"] > rob[t0]["gap"])
        rv["supported"] = cond
        print("  D_B<D_A at T*: %s; gap grew vs T0: %s -> SUPPORTED=%s" %
              (rob[tstar]["D_B"] < rob[tstar]["D_A"],
               rob[tstar]["gap"] > rob[t0]["gap"], cond))
    out["robustness_verdict"] = rv

    json.dump(out, open(path.replace("results_", "verdict_summary_")
                        .replace(".json", ".json"), "w"), indent=1,
              sort_keys=True)
    print("\nwrote verdict summary")

main(sys.argv[1])
