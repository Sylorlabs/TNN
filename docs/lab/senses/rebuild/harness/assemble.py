#!/usr/bin/env python3
"""HARNESS-CREW verdict assembly: metrics.json -> RESULTS.md.

Full tables (per-task accuracy both approaches, ops, noise/adversarial
accuracy, false-install rates) + per-kill-bar evaluation KB1-KB5, all
COMPUTED from metrics. Does NOT write VERDICT.md kill decisions.
"""
import json, os, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(ROOT, "results")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
TASK_LABEL = {"colordisc": "color discrimination", "colorconst": "color constancy",
              "shapetrans": "shape transform", "pitchdisc": "pitch discrimination",
              "timbredisc": "timbre discrimination", "motiondir": "motion direction"}

def pct(x):
    return "%.1f%%" % (100 * x)

def main():
    with open(os.path.join(RES, "metrics.json")) as f:
        m = json.load(f)
    A, B = m["per_approach"]["A"], m["per_approach"]["B"]
    det = m["determinism"]
    L = []
    L.append("# SENSES REBUILD — Harness results")
    L.append("")
    L.append("Generated: %s (harness crew)" % datetime.datetime.now().isoformat(timespec="seconds"))
    L.append("Approach A = raw values (`a_raw/sense`), Approach B = qualitative percepts (`b_percept/sense`).")
    L.append("Runner errors (missing keys / bad vocab / nonzero exit): %d" % m["errors"])
    L.append("")
    L.append("## 1. Primary-fixture accuracy per task")
    L.append("")
    L.append("| task | A acc | B acc | Δ (B−A) | A n | B n |")
    L.append("|---|---|---|---|---|---|")
    for t in TASKS:
        a, b = A["tasks"][t]["primary"], B["tasks"][t]["primary"]
        d = b["accuracy"] - a["accuracy"]
        L.append("| %s | %s | %s | %+.1fpp | %d | %d |" % (
            TASK_LABEL[t], pct(a["accuracy"]), pct(b["accuracy"]), 100*d, a["n"], b["n"]))
    L.append("| **mean (equal weights)** | **%s** | **%s** | **%+.1fpp** | | |" % (
        pct(A["mean_primary"]), pct(B["mean_primary"]), 100*(B["mean_primary"]-A["mean_primary"])))
    L.append("")
    L.append("## 2. Instrumented ops (element-visit grain)")
    L.append("")
    L.append("| task | A ops | B ops | ratio B/A |")
    L.append("|---|---|---|---|")
    for t in TASKS:
        ao = sum(A["tasks"][t][v]["ops"] for v in ("primary","noise","adversarial"))
        bo = sum(B["tasks"][t][v]["ops"] for v in ("primary","noise","adversarial"))
        r = bo/ao if ao else float("nan")
        L.append("| %s | %d | %d | %.2f× |" % (TASK_LABEL[t], ao, bo, r))
    L.append("| **total** | **%d** | **%d** | **%.2f×** |" % (
        A["ops_total"], B["ops_total"],
        B["ops_total"]/A["ops_total"] if A["ops_total"] else float("nan")))
    L.append("")
    L.append("## 3. Robustness: noise and adversarial accuracy")
    L.append("")
    L.append("### noise fixtures (deterministic precomputed noise)")
    L.append("")
    L.append("| task | A | B | A n | B n |")
    L.append("|---|---|---|---|---|")
    for t in TASKS:
        a, b = A["tasks"][t]["noise"], B["tasks"][t]["noise"]
        L.append("| %s | %s | %s | %d | %d |" % (TASK_LABEL[t], pct(a["accuracy"]), pct(b["accuracy"]), a["n"], b["n"]))
    L.append("| **mean** | **%s** | **%s** | | |" % (pct(A["noise_acc"]), pct(B["noise_acc"])))
    L.append("")
    L.append("### adversarial fixtures")
    L.append("")
    L.append("| task | A | B | A n | B n |")
    L.append("|---|---|---|---|---|")
    for t in TASKS:
        a, b = A["tasks"][t]["adversarial"], B["tasks"][t]["adversarial"]
        L.append("| %s | %s | %s | %d | %d |" % (TASK_LABEL[t], pct(a["accuracy"]), pct(b["accuracy"]), a["n"], b["n"]))
    L.append("| **mean** | **%s** | **%s** | | |" % (pct(A["adv_acc"]), pct(B["adv_acc"])))
    L.append("")
    L.append("## 4. Memory integration (shared deliberate-memory rule)")
    L.append("")
    L.append("Rule (identical code path for both): INSTALL iff no contradictory installed")
    L.append("belief with confidence ≥ incoming exists in the (approach, task) stream;")
    L.append("else WITHHOLD + audit. False install = installed judgment contradicts .truth.")
    L.append("")
    L.append("|  | A | B |")
    L.append("|---|---|---|")
    for key, label in (("all_installs","installs (all fixtures)"),
                       ("all_false_installs","false installs (all fixtures)"),
                       ("withholds","withholds (all fixtures)"),
                       ("adv_installs","installs (adversarial)"),
                       ("adv_false_installs","false installs (adversarial)"),
                       ("adv_fixtures","adversarial fixtures")):
        L.append("| %s | %d | %d |" % (label, A["memory"][key], B["memory"][key]))
    L.append("| false-install rate, adversarial (per install) | %s | %s |" % (
        pct(A["memory"]["adv_false_install_rate"]), pct(B["memory"]["adv_false_install_rate"])))
    L.append("| false-install rate, adversarial (per fixture) | %s | %s |" % (
        pct(A["memory"]["adv_false_install_rate_per_fixture"]),
        pct(B["memory"]["adv_false_install_rate_per_fixture"])))
    L.append("| false-install rate, all fixtures (per install) | %s | %s |" % (
        pct(A["memory"]["all_false_install_rate"]), pct(B["memory"]["all_false_install_rate"])))
    L.append("")
    L.append("## 5. Kill-bar evaluation (computed)")
    L.append("")
    kb = {}
    # KB1
    for tag, P in (("A", A), ("B", B)):
        kb[("KB1", tag)] = "PASS" if P["mean_primary"] >= 0.60 else "FAIL"
    # KB2
    delta = B["mean_primary"] - A["mean_primary"]
    ops_ratio = max(A["ops_total"], B["ops_total"]) / max(1, min(A["ops_total"], B["ops_total"]))
    if abs(delta) < 0.02 and ops_ratio < 2.0:
        kb2 = "TIE (|Δ|=%.2fpp < 2pp and ops ratio=%.2f× < 2×); no winner declared" % (100*abs(delta), ops_ratio)
        winner = None
    else:
        winner = "B" if delta > 0 else "A"
        kb2 = "winner=%s (|Δ|=%.1fpp, ops ratio=%.2f×)" % (winner, 100*abs(delta), ops_ratio)
    # KB3
    for tag, P in (("A", A), ("B", B)):
        drop_n = P["mean_primary"] - P["noise_acc"]
        drop_a = P["mean_primary"] - P["adv_acc"]
        kb[("KB3", tag)] = ("FRAGILE (noise drop %.1fpp, adv drop %.1fpp)"
                            % (100*drop_n, 100*drop_a)
                            if (drop_n > 0.25 or drop_a > 0.25)
                            else "not fragile (noise drop %.1fpp, adv drop %.1fpp)"
                            % (100*drop_n, 100*drop_a))
    # KB4
    for tag, P in (("A", A), ("B", B)):
        r = P["memory"]["adv_false_install_rate"]
        kb[("KB4", tag)] = ("FAIL (%.1f%% > 10%%)" % (100*r)) if r > 0.10 else ("PASS (%.1f%% ≤ 10%%)" % (100*r))
    # KB5
    for tag in ("A", "B"):
        d = det[tag]
        kb[("KB5", tag)] = ("PASS (%d/%d samples byte-identical over 3 runs)" % (d["identical"], d["samples"])
                            if not d["failures"]
                            else "FAIL (%d nondeterministic: %s)" % (len(d["failures"]), "; ".join(d["failures"][:5])))
    L.append("| bar | A | B |")
    L.append("|---|---|---|")
    L.append("| KB1 viability (mean ≥ 60%%) | %s | %s |" % (kb[("KB1","A")], kb[("KB1","B")]))
    L.append("| KB2 head-to-head | %s | (see A column) |" % kb2)
    L.append("| KB3 fragility (winner drop > 25pp) | %s | %s |" % (kb[("KB3","A")], kb[("KB3","B")]))
    L.append("| KB4 memory integration (adv false-install ≤ 10%%) | %s | %s |" % (kb[("KB4","A")], kb[("KB4","B")]))
    L.append("| KB5 determinism (3× byte-identical) | %s | %s |" % (kb[("KB5","A")], kb[("KB5","B")]))
    L.append("")
    L.append("KB3 evaluated against the KB2 winner%s." % ((" = approach " + winner) if winner else " (tie: shown for both)"))
    L.append("")
    L.append("## 6. Notes")
    L.append("")
    L.append("- Fixture inventory: 60/40/90/60/60/60 primary, same counts noise, "
             "30/20/45/30/30/30 adversarial (925 fixtures + 925 .truth files).")
    L.append("- Noise is deterministic precomputed noise baked into fixture files "
             "(splitmix64, master seed 20260921); no RNG at scoring time.")
    L.append("- Determinism sample: first 10 primary fixtures per task, 3 runs each.")
    L.append("- Memory streams: one per (approach, task); all variants in sorted-path order; "
             "KB4 uses the adversarial-fixture subset.")
    L.append("- Ops counted by the sense binaries at element-visit grain per INTERFACE.md.")
    L.append("")
    with open(os.path.join(ROOT, "RESULTS.md"), "w") as f:
        f.write("\n".join(L) + "\n")
    print("wrote RESULTS.md")

if __name__ == "__main__":
    main()
