#!/usr/bin/env python3
"""HARNESS-CREW scorer: accuracy, ops, robustness, memory integration.

The deliberate-memory rule is implemented ONCE (apply_memory_rule) and used
identically for both approaches — parameterized only by the sense outputs
(judgment, confidence). Streams are per (approach, task); fixtures processed
in deterministic sorted-path order. All variants feed the stream; KB4 uses
the adversarial-fixture subset.

Output: results/metrics.json
"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(ROOT, "results")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
VARIANTS = ["primary", "noise", "adversarial"]

# ------------------------------------------------------------------
# SHARED deliberate-memory rule (INTERFACE.md). Single code path.
# Stream state: list of installed (judgment, confidence, fixture).
# INSTALL iff no contradictory installed belief with confidence >= incoming
# confidence exists in the stream; else WITHHOLD + audit entry.
# Returns ("INSTALL"|"WITHHOLD", audit_entry_or_None).
def apply_memory_rule(installed, judgment, confidence, truth, fixture):
    for (j, c, _fx) in installed:
        if j != judgment and c >= confidence:
            return ("WITHHOLD",
                    {"fixture": fixture, "judgment": judgment,
                     "confidence": confidence,
                     "blocked_by": {"judgment": j, "confidence": c}})
    installed.append((judgment, confidence, fixture))
    false_install = (judgment != truth)
    return ("INSTALL", {"fixture": fixture, "judgment": judgment,
                        "confidence": confidence, "truth": truth,
                        "false_install": false_install})
# ------------------------------------------------------------------

def main():
    with open(os.path.join(RES, "raw_results.json")) as f:
        data = json.load(f)
    runs = data["runs"]
    errors = data["errors"]

    m = {"per_approach": {}, "errors": len(errors),
         "determinism": data["determinism"]}
    for tag in ("A", "B"):
        ar = [r for r in runs if r["approach"] == tag]
        pa = {"tasks": {}, "mean_primary": 0.0, "ops_total": 0,
              "ops_by_task": {}, "noise_acc": 0.0, "adv_acc": 0.0,
              "memory": {}}
        accs = []
        for task in TASKS:
            tr = [r for r in ar if r["task"] == task]
            td = {}
            for v in VARIANTS:
                vr = [r for r in tr if r["variant"] == v]
                acc = sum(1 for r in vr if r["correct"]) / len(vr) if vr else 0.0
                td[v] = {"n": len(vr), "correct": sum(1 for r in vr if r["correct"]),
                         "accuracy": acc,
                         "ops": sum(r["ops"] for r in vr)}
            pa["tasks"][task] = td
            accs.append(td["primary"]["accuracy"])
            pa["ops_by_task"][task] = sum(td[v]["ops"] for v in VARIANTS)
        pa["mean_primary"] = sum(accs) / len(accs)
        pa["noise_acc"] = sum(pa["tasks"][t]["noise"]["accuracy"] for t in TASKS) / len(TASKS)
        pa["adv_acc"] = sum(pa["tasks"][t]["adversarial"]["accuracy"] for t in TASKS) / len(TASKS)
        pa["ops_total"] = sum(pa["ops_by_task"].values())

        # shared memory rule over streams (approach, task), all variants sorted
        mem = {"streams": {}, "adv_installs": 0, "adv_false_installs": 0,
               "all_installs": 0, "all_false_installs": 0, "withholds": 0,
               "audit": []}
        for task in TASKS:
            stream = sorted([r for r in ar if r["task"] == task],
                            key=lambda r: r["fixture"])
            installed = []
            s_installs = s_false = s_with = 0
            for r in stream:
                action, entry = apply_memory_rule(installed, r["judgment"],
                                                 r["confidence"], r["truth"],
                                                 r["fixture"])
                if action == "INSTALL":
                    s_installs += 1; mem["all_installs"] += 1
                    if entry["false_install"]:
                        s_false += 1; mem["all_false_installs"] += 1
                    if r["variant"] == "adversarial":
                        mem["adv_installs"] += 1
                        if entry["false_install"]:
                            mem["adv_false_installs"] += 1
                else:
                    s_with += 1; mem["withholds"] += 1
                    mem["audit"].append(entry)
            mem["streams"][task] = {"installs": s_installs,
                                    "false_installs": s_false,
                                    "withholds": s_with}
        mem["adv_false_install_rate"] = (mem["adv_false_installs"] / mem["adv_installs"]
                                         if mem["adv_installs"] else 0.0)
        adv_fixtures = sum(1 for t in TASKS
                           for r in ar if r["task"] == t and r["variant"] == "adversarial")
        mem["adv_fixtures"] = adv_fixtures
        mem["adv_false_install_rate_per_fixture"] = (mem["adv_false_installs"] / adv_fixtures
                                                     if adv_fixtures else 0.0)
        mem["all_false_install_rate"] = (mem["all_false_installs"] / mem["all_installs"]
                                         if mem["all_installs"] else 0.0)
        pa["memory"] = mem
        m["per_approach"][tag] = pa

    with open(os.path.join(RES, "metrics.json"), "w") as f:
        json.dump(m, f, indent=1)
    print(json.dumps({t: {k: v for k, v in
          (("mean_primary", m["per_approach"][t]["mean_primary"]),
           ("noise_acc", m["per_approach"][t]["noise_acc"]),
           ("adv_acc", m["per_approach"][t]["adv_acc"]),
           ("ops_total", m["per_approach"][t]["ops_total"]),
           ("adv_fir", m["per_approach"][t]["memory"]["adv_false_install_rate"]))
          } for t in ("A", "B")}, indent=1))
    print("errors: %d" % m["errors"])

if __name__ == "__main__":
    main()
