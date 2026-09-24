#!/usr/bin/env python3
"""score_ablation.py -- R2-16 challenge->bank ablation (prereg bar 3).

Implements prereg §2.4 abl_bank WITHOUT touching the Zag mechanism:
the full-mode union ledger already records the formation's judgment and
confidence (its coarse feature) per fixture. This script:

1. Builds the frozen exemplar bank: 20 TRUE (formation judgment == truth)
   + 20 FALSE (judgment != truth) exemplars per task, selected
   deterministically (sorted by (conf, ledger_lineno), first 20 of each
   class) from the full-mode B-adv union ledger. Feature = conf.
2. Scores abl_bank on a battery ledger: for each fixture, 1-NN on conf
   against the 40 exemplars of its task; INSTALL iff the nearest exemplar
   is TRUE (ties -> FALSE/WITHHOLD, deterministic); the installed judgment
   is the formation's judgment. FI = INSTALL and judgment != truth.
3. Reports abl FI vs full FI and the >=2x bar.

No RNG. Deterministic. Pure glue/analysis.

Usage:
  score_ablation.py build-bank <union_ledger> <list> <truth_ledger> <bank_out>
  score_ablation.py score <union_ledger> <list> <truth_ledger> <bank>
"""
import json, re, os, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
FORK = os.path.normpath(os.path.join(HERE, ".."))

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
JMAP = {
    "colordisc": {"SAME": 0, "DIFFERENT": 1},
    "colorconst": {"SAME_SURFACE": 0, "DIFFERENT": 1},
    "shapetrans": {"CIRCLE": 0, "TRIANGLE": 1, "SQUARE": 2},
    "pitchdisc": {"SAME": 0, "HIGHER": 1, "LOWER": 2},
    "timbredisc": {"PURE": 0, "BRIGHT": 1, "DARK": 2, "RICH": 3},
    "motiondir": {"STILL": 0, "N": 1, "NE": 2, "E": 3, "SE": 4, "S": 5,
                  "SW": 6, "W": 7, "NW": 8},
}
LED_PAT = re.compile(
    r'fixture=r2fx_t(\d+)_i(\d+)_f(\d+)\s+task=(\w+)\s+judgment=(\S+)'
    r'\s+conf=(\d+)\s+challenge=\S+\s+outcome=(\S+)\s+disp=(\w+)')

def load_truth(truth_ledger):
    truth = {}
    with open(truth_ledger) as f:
        for line in f:
            d = json.loads(line)
            truth[d["id"]] = d["truth"]
    return truth

def load_list(list_path):
    with open(list_path) as f:
        return [l.strip() for l in f]

def parse_ledger(ledger_path):
    rows = []
    with open(ledger_path, "rb") as f:
        for lineno, raw in enumerate(f):
            line = raw.decode("utf-8", "replace")
            m = LED_PAT.search(line)
            if not m:
                continue
            t_idx, idx, fam, task, jname, conf, outcome, disp = m.groups()
            rows.append({"lineno": lineno, "task": task, "jname": jname,
                         "conf": int(conf), "disp": disp,
                         "fam": int(fam), "idx": int(idx)})
    return rows

def oid_for(list_path_entry):
    m = re.match(r'.*/((?:r2n|r2a|r2a2|r2h16)_(\w+)_(\d+))\.r2fx$',
                 list_path_entry)
    if not m:
        return None
    return m.group(1)

def join_truth(rows, paths, truth):
    out = []
    for r, p in zip(rows, paths):
        oid = oid_for(p)
        t = truth.get(oid)
        if t is None:
            continue
        jid = JMAP[r["task"]].get(r["jname"], -1)
        tid = JMAP[r["task"]].get(t, -1)
        r = dict(r)
        r["truth"] = t
        r["correct"] = (jid == tid and jid >= 0)
        out.append(r)
    return out

def build_bank(union_ledger, list_path, truth_ledger, bank_out):
    truth = load_truth(truth_ledger)
    paths = load_list(list_path)
    rows = join_truth(parse_ledger(union_ledger), paths, truth)
    bank = {}
    for task in TASKS:
        # First 20 TRUE / first 20 FALSE in battery (ledger) order.
        # Deterministic; the most literal reading of "drawn from r2n/r2a".
        tr = [r for r in rows if r["task"] == task and r["correct"]][:20]
        fa = [r for r in rows if r["task"] == task and not r["correct"]][:20]
        bank[task] = {
            "true": [r["conf"] for r in tr],
            "false": [r["conf"] for r in fa],
            "n_true_avail": sum(1 for r in rows if r["task"] == task and r["correct"]),
            "n_false_avail": sum(1 for r in rows if r["task"] == task and not r["correct"]),
        }
        print("%s: true=%d/20 (avail %d) false=%d/20 (avail %d)"
              % (task, len(tr), bank[task]["n_true_avail"],
                 len(fa), bank[task]["n_false_avail"]))
    with open(bank_out, "w") as f:
        json.dump(bank, f, indent=1, sort_keys=True)
    print("bank written:", bank_out)

def score(union_ledger, list_path, truth_ledger, bank_path):
    with open(bank_path) as f:
        bank = json.load(f)
    truth = load_truth(truth_ledger)
    paths = load_list(list_path)
    rows = join_truth(parse_ledger(union_ledger), paths, truth)
    fi = 0
    installs = 0
    per_task_fi = {}
    for r in rows:
        b = bank[r["task"]]
        best_d, best_label = None, None
        for lab, vals in (("true", b["true"]), ("false", b["false"])):
            for v in vals:
                d = abs(r["conf"] - v)
                if best_d is None or d < best_d:
                    best_d, best_label = d, lab
                # ties keep the earlier label; "true" scanned first, but a
                # tie at equal distance resolves to TRUE only if no FALSE is
                # strictly nearer. Enforce: ties -> FALSE.
                elif d == best_d and lab == "false":
                    best_label = "false"
        if best_label == "true":
            installs += 1
            if not r["correct"]:
                fi += 1
                per_task_fi[r["task"]] = per_task_fi.get(r["task"], 0) + 1
    n = len(rows)
    print("abl_bank: n=%d installs=%d FI=%d (%.3f%%)" % (n, installs, fi, 100.0 * fi / n))
    for t in TASKS:
        if per_task_fi.get(t):
            print("  %s FI=%d" % (t, per_task_fi[t]))
    return fi, n

def main():
    cmd = sys.argv[1]
    if cmd == "build-bank":
        build_bank(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif cmd == "score":
        fi, n = score(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        print("RESULT fi=%d n=%d" % (fi, n))
    else:
        raise SystemExit("unknown cmd")

if __name__ == "__main__":
    main()
