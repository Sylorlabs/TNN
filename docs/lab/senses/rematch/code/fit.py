#!/usr/bin/env python3
"""Deterministic threshold fitting + evaluation for the senses rematch.

Inputs (cached binary records, JSONL from run_all.py):
  runs_TRAIN_T1.jsonl ... runs_TRAIN_T4.jsonl  (whichever budgets completed)
  runs_TEST_FRESH.jsonl, runs_TEST_R1.jsonl, runs_ADV_R1.jsonl

Per (approach, task, budget): sweep the preregistered grid (CALIBRATION.md)
on TRAIN; objective = training accuracy; deterministic tie-breaks.
T0 = hand-tuned values, no fitting.

Evaluates fitted judgments on TEST_FRESH (KB1, KB2, KB6, robustness),
TEST_R1 (secondary), ADV_R1 (KB3, robustness, KB4). KB4 uses the shared
apply_memory_rule from round-1 score.py.

Output: results_<stamp>.json + printed learning-curve tables.
Pure Python, zero RNG. All iteration orders sorted -> deterministic.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "/home/hatch/workspace/senses-rebuild/harness")
import relations as R
from score import apply_memory_rule

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
BUDGETS = ["T0", "T1", "T2", "T3", "T4"]

# grids: { (approach, task): [ (param, [grid...], hand) ] } ; None = not fitted
GRIDS = {
    ("A", "colordisc"): [("t", [10, 20, 30, 40, 50, 60, 80, 100], 40)],
    ("A", "colorconst"): [("t", [50, 75, 100, 125, 150, 175, 200, 250, 300], 150)],
    ("A", "shapetrans"): None,
    ("A", "pitchdisc"): [("t", [5000, 10000, 15000, 20000, 30000, 50000], 20000)],
    ("A", "timbredisc"): [("b1", [1020, 1040, 1060, 1075, 1100, 1130], 1075),
                           ("b2", [1300, 1350, 1400, 1450, 1500], 1400),
                           ("b3", [2600, 2800, 3000, 3200, 3400], 3000)],
    ("A", "motiondir"): [("t", [1, 2, 3, 4, 5], 3)],
    ("B", "colordisc"): [("k", [0, 1, 2, 3, 4], 1)],
    ("B", "colorconst"): [("k", [0, 1, 2, 3, 4], 1)],
    ("B", "pitchdisc"): [("k", [0, 1, 2, 3], 0)],
    ("B", "shapetrans"): [("m", [2, 3], 0), ("prio", [0, 1, 2, 3, 4, 5], 0)],
    ("B", "timbredisc"): [("tc", [1000, 1075, 1150, 1225, 1300], 1150),
                           ("tb", [40, 50, 60, 70, 80], 60),
                           ("tf", [1600, 1700, 1780, 1860, 1950], 1780)],
    ("B", "motiondir"): [("t", [100, 150, 200, 250, 300], 200)],
}
HAND_PARAMS = {k: ({p: h for (p, _g, h) in v} if v else {}) for k, v in GRIDS.items()}

def prio_dist(idx):
    return 0 if idx == 0 else 1  # CALIBRATION.md crew definition

def param_dist(param, g, h):
    if param == "prio":
        return prio_dist(g)
    return abs(g - h)

def fitted_judgment(approach, task, params, rec):
    s = rec["scores"]
    if approach == "A":
        if task == "colordisc":
            return R.a_color_judgment(s["dist"], params["t"])
        if task == "colorconst":
            return R.a_colorconst_judgment(s["dist"], params["t"])
        if task == "shapetrans":
            return rec["judgment"]  # not fitted
        if task == "pitchdisc":
            return R.a_pitch_judgment(s["dppm"], s["fam"], s["fbm"], params["t"])
        if task == "timbredisc":
            return R.a_timbre_judgment(s["r"], params["b1"], params["b2"], params["b3"])
        if task == "motiondir":
            return R.a_motion_judgment(s["mag"], s["dx"], s["dy"], params["t"])
    else:
        if task == "colordisc":
            return R.b_color_judgment(s["percept"], s["percept2"], params["k"])
        if task == "colorconst":
            return R.b_colorconst_judgment(s["percept"], s["percept2"], params["k"])
        if task == "pitchdisc":
            return R.b_pitch_judgment(s["percept"], s["percept2"], params["k"])
        if task == "shapetrans":
            tup = (s["percept"], s["shape_curv"], s["shape_sym"])
            return R.b_shape_judgment(tup, params["m"], R.PRIO_ORDERS[params["prio"]])
        if task == "timbredisc":
            return R.b_timbre_judgment(s["timbre_crest"], s["timbre_bright"],
                                       s["timbre_form"], params["tc"],
                                       params["tb"], params["tf"])
        if task == "motiondir":
            return R.b_motion_judgment(s["motion_mcount"], s["percept"], params["t"])
    raise ValueError((approach, task))

def accuracy(recs, approach, task, params):
    n = c = 0
    for r in recs:
        if r["approach"] != approach or r["task"] != task or "error" in r:
            continue
        n += 1
        if fitted_judgment(approach, task, params, r) == r["truth"]:
            c += 1
    return (c / n if n else 0.0), n

def sweep(approach, task, train_recs):
    grid = GRIDS[(approach, task)]
    if grid is None:
        return {}, None  # not fitted
    params = {p: h for (p, _g, h) in grid}
    for (p, vals, h) in grid:
        scored = []
        for i, g in enumerate(vals):
            trial = dict(params)
            trial[p] = g
            acc, _n = accuracy(train_recs, approach, task, trial)
            scored.append((acc, param_dist(p, g, h), i, g))
        best_acc = max(s[0] for s in scored)
        cand = [s for s in scored if s[0] == best_acc]
        cand.sort(key=lambda s: (s[1], s[2]))
        params[p] = cand[0][3]
    return params, None

def load(path):
    recs = []
    with open(path) as f:
        for line in f:
            recs.append(json.loads(line))
    return recs

def evaluate(recs, params_by_key):
    """params_by_key[(approach,task)] -> params. Returns per-approach per-task acc."""
    out = {}
    for approach in ("A", "B"):
        ta = {}
        for task in TASKS:
            acc, n = accuracy(recs, approach, task, params_by_key[(approach, task)])
            ta[task] = {"accuracy": acc, "n": n}
        mean = sum(ta[t]["accuracy"] for t in TASKS) / len(TASKS)
        out[approach] = {"tasks": ta, "mean": mean}
    return out

def kb4(recs_fresh, recs_adv, params_by_key):
    """Memory rule over streams (approach, task), primary then adversarial,
    sorted-path order. Returns per-approach adv false-install rate."""
    out = {}
    for approach in ("A", "B"):
        stream = []
        for variant, recs in (("primary", recs_fresh), ("adversarial", recs_adv)):
            for r in recs:
                if r["approach"] != approach or "error" in r:
                    continue
                stream.append((variant, r))
        stream.sort(key=lambda x: (0 if x[0] == "primary" else 1, x[1]["rel"]))
        installed = []
        adv_installs = adv_false = 0
        withholds = 0
        for variant, r in stream:
            j = fitted_judgment(approach, r["task"], params_by_key[(approach, r["task"])], r)
            action, entry = apply_memory_rule(installed, j, r["confidence"],
                                              r["truth"], r["rel"])
            if action == "INSTALL":
                if variant == "adversarial":
                    adv_installs += 1
                    if entry["false_install"]:
                        adv_false += 1
            else:
                withholds += 1
        out[approach] = {"adv_installs": adv_installs,
                         "adv_false_installs": adv_false,
                         "adv_false_install_rate": (adv_false / adv_installs
                                                    if adv_installs else 0.0),
                         "withholds": withholds}
    return out

def main():
    data = HERE + "/data"
    train = {}
    have = ["T0"]
    for b in ["T1", "T2", "T3", "T4"]:
        p = os.path.join(HERE, "runs_TRAIN_%s.jsonl" % b)
        if os.path.exists(p):
            train[b] = load(p)
            have.append(b)
    recs_fresh = load(os.path.join(HERE, "runs_TEST_FRESH.jsonl"))
    adv_path = os.path.join(HERE, "runs_ADV_R1.jsonl")
    recs_adv = load(adv_path) if os.path.exists(adv_path) else []
    r1_path = os.path.join(HERE, "runs_TEST_R1.jsonl")
    recs_r1 = load(r1_path) if os.path.exists(r1_path) else []

    fitted = {}   # budget -> {(approach,task): params}
    train_acc = {}
    for b in have:
        fitted[b] = {}
        train_acc[b] = {}
        for approach in ("A", "B"):
            for task in TASKS:
                if b == "T0":
                    params = dict(HAND_PARAMS[(approach, task)])
                else:
                    params, _ = sweep(approach, task, train[b])
                fitted[b][(approach, task)] = params
                if b != "T0":
                    acc, n = accuracy(train[b], approach, task, params)
                    train_acc[b][(approach, task)] = {"accuracy": acc, "n": n}

    ev_fresh, ev_r1, ev_adv = {}, {}, {}
    for b in have:
        ev_fresh[b] = evaluate(recs_fresh, fitted[b])
        ev_adv[b] = evaluate(recs_adv, fitted[b]) if recs_adv else None
        ev_r1[b] = evaluate(recs_r1, fitted[b]) if recs_r1 else None

    mem = {b: kb4(recs_fresh, recs_adv, fitted[b]) for b in have} if recs_adv else {}

    # ops on TEST_FRESH (fitted run = binary ops; fitting changes no binary work)
    ops = {}
    for approach in ("A", "B"):
        ops[approach] = sum(r["ops"] for r in recs_fresh
                            if r["approach"] == approach and "error" not in r)

    res = {"budgets": have, "fitted_params": {}, "train_acc": {},
           "test_fresh": {}, "test_r1": {}, "adv_r1": {}, "memory": mem,
           "ops_test_fresh": ops}
    for b in have:
        res["fitted_params"][b] = {"%s/%s" % k: v for k, v in fitted[b].items()}
        if b in train_acc:
            res["train_acc"][b] = {"%s/%s" % k: v for k, v in train_acc[b].items()}
        res["test_fresh"][b] = ev_fresh[b]
        if ev_r1[b]:
            res["test_r1"][b] = ev_r1[b]
        if ev_adv[b]:
            res["adv_r1"][b] = ev_adv[b]

    stamp = os.environ.get("STAMP", "main")
    outp = os.path.join(HERE, "results_%s.json" % stamp)
    with open(outp, "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
    print("wrote %s" % outp)

    # ---- learning-curve table ----
    print("\n=== TEST-FRESH accuracy (fitted) ===")
    hdr = ["budget"] + ["A_mean"] + ["A_" + t[:6] for t in TASKS] + ["B_mean"] + ["B_" + t[:6] for t in TASKS]
    print(" ".join("%10s" % h for h in hdr))
    for b in have:
        row = [b]
        for approach in ("A", "B"):
            e = ev_fresh[b][approach]
            row.append("%.3f" % e["mean"])
            row += ["%.3f" % e["tasks"][t]["accuracy"] for t in TASKS]
        # reorder to match hdr: A_mean, A tasks..., B_mean, B tasks...
        print(" ".join("%10s" % v for v in [row[0]] + row[1:8] + row[8:15]))

    print("\n=== ADV-R1 accuracy (fitted) ===")
    for b in have:
        if ev_adv[b]:
            print(b, "A=%.3f B=%.3f" % (ev_adv[b]["A"]["mean"], ev_adv[b]["B"]["mean"]))
    print("\n=== KB4 adv false-install rate ===")
    for b in have:
        if b in mem:
            print(b, "A=%.3f (%d/%d) B=%.3f (%d/%d)" % (
                mem[b]["A"]["adv_false_install_rate"], mem[b]["A"]["adv_false_installs"],
                mem[b]["A"]["adv_installs"], mem[b]["B"]["adv_false_install_rate"],
                mem[b]["B"]["adv_false_installs"], mem[b]["B"]["adv_installs"]))

main()
