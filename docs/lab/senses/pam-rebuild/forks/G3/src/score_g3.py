#!/usr/bin/env python3
"""score_g3.py — score a g3_run.py JSONL against frozen bars.

Reports B1 (primary viability), B5 (adversarial false-install), install /
withhold rates, chain verification, ops summary, and per-task tables.
Exit code 0 always; prints PASS/FAIL per bar for the operator.
"""
import sys, json
from collections import defaultdict

def load(path):
    return [json.loads(l) for l in open(path) if l.strip()]

def main(path):
    recs = load(path)
    prim = [r for r in recs if r["variant"] == "primary"]
    noise = [r for r in recs if r["variant"] == "noise"]
    adv = [r for r in recs if r["variant"] == "adversarial"]
    atk = [r for r in recs if r["variant"] == "attack"]

    print("== records: %d  chain_ok: %d/%d ==" %
          (len(recs), sum(1 for r in recs if r["chain_ok"]), len(recs)))

    # ---- B1: primary viability ----
    print("\n-- B1 primary accuracy (bar: mean >= 60%) --")
    accs = []
    for t in sorted(set(r["task"] for r in prim)):
        rs = [r for r in prim if r["task"] == t]
        a = sum(1 for r in rs if r["correct"]) / len(rs)
        accs.append(a)
        inst = sum(1 for r in rs if r["disposition"] == "INSTALL")
        print("  %-12s %3d/%-3d  acc=%6.2f%%  install=%d" % (t, sum(1 for r in rs if r["correct"]), len(rs), 100*a, inst))
    mean = sum(accs) / len(accs)
    print("  MEAN acc=%.2f%%  -> %s" % (100*mean, "PASS" if mean >= 0.60 else "FAIL"))

    # ---- enrollment sanity: noise fixtures should INSTALL ----
    print("\n-- noise (enrolled) install rate --")
    for t in sorted(set(r["task"] for r in noise)):
        rs = [r for r in noise if r["task"] == t]
        inst = sum(1 for r in rs if r["disposition"] == "INSTALL")
        cor = sum(1 for r in rs if r["correct"])
        print("  %-12s %3d/%-3d install  correct=%d" % (t, inst, len(rs), cor))

    # ---- B5: adversarial false-install (bar: <= 1%) ----
    print("\n-- B5 adversarial false-install (bar: <= 1%%) --")
    for name, rs in (("adversarial", adv), ("attack", atk)):
        if not rs:
            print("  %-12s none" % name)
            continue
        installs = [r for r in rs if r["disposition"] == "INSTALL"]
        false_inst = [r for r in installs if r["judgment"] != r["truth"]]
        rate = len(false_inst) / len(rs)
        print("  %-12s n=%-3d installs=%d false_installs=%d rate=%.3f%% -> %s" %
              (name, len(rs), len(installs), len(false_inst), 100*rate,
               "PASS" if rate <= 0.01 else "FAIL"))
        for r in false_inst[:10]:
            print("      FALSE-INSTALL %s sig=%s judgment=%s truth=%s" %
                  (r["path"], (r["sig"] or "")[:16], r["judgment"], r["truth"]))

    # ---- ops ----
    print("\n-- ops per percept --")
    ops = defaultdict(list)
    for r in recs:
        if r["ops"] is not None:
            ops[r["task"]].append(int(r["ops"]))
    for t in sorted(ops):
        v = ops[t]
        print("  %-12s min=%d max=%d mean=%.0f" % (t, min(v), max(v), sum(v)/len(v)))

    # ---- bytes per percept ----
    print("\n  bytes/percept: sig=32 meta=4 graph<=14 -> percept=288 bits (36 bytes)")

if __name__ == "__main__":
    main(sys.argv[1])
