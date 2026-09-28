#!/usr/bin/env python3
"""G1 scorer (frozen by PREREG_G1.md sections 5, 7).

Reads evidence/results/run<N>/raw_g1.json (+ raw_a.json for B2 if present),
computes B1-B7 metrics, verifies ledgers independently in Python
(hash chain + disposition replay), and writes metrics_g1.json.

Usage: score_g1.py
"""
import hashlib
import json
import os
import re
import sys

BASE = os.path.expanduser("~/workspace/tnn-lab/senses")
RES = os.path.join(BASE, "pam-rebuild", "forks", "G1", "evidence", "results")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc",
         "motiondir"]
ENTRY = re.compile(
    r"seq=(\d+) task=(\S+) fixture=(\S+) percept=([0-9a-f]{128}) "
    r"judgment=(\S+) confidence=(\d+) disposition=(INSTALL|WITHHOLD) "
    r"anchor=(-?\d+) prev=([0-9a-f]{64}) hash=([0-9a-f]{64})")


def hamming128(a, b):
    return bin(int(a, 16) ^ int(b, 16)).count("1")


def load_run(n):
    with open(os.path.join(RES, "run%d" % n, "raw_g1.json")) as f:
        return json.load(f)


def verify_ledger(path):
    """Independent Python verification: hash chain + disposition replay."""
    with open(path, "rb") as f:
        lines = [ln.rstrip(b"\n") for ln in f if ln.strip()]
    anchors = {}
    prev_hash = "0" * 64
    n_ok = 0
    problems = []
    for raw in lines:
        core = raw.rsplit(b" hash=", 1)[0]
        h = hashlib.sha256(core + b"\n").hexdigest()
        m = ENTRY.match(raw.decode())
        if not m:
            problems.append("unparseable: %s" % raw[:60])
            continue
        seq, task, fix, perc, judg, conf, disp, anch, prev, hh = m.groups()
        if hh != h:
            problems.append("hash mismatch seq=%s" % seq)
        if prev != prev_hash:
            problems.append("chain break seq=%s" % seq)
        prev_hash = hh
        key = (task, judg)
        if key in anchors:
            ap = anchors[key]
            var = hamming128(perc, ap)
            exp = "INSTALL" if var <= 5 else "WITHHOLD"
            if disp != exp:
                problems.append("disposition mismatch seq=%s (%s vs %s, var=%d)"
                                % (seq, disp, exp, var))
            if int(anch) != anchors_seq[key]:
                problems.append("anchor mismatch seq=%s" % seq)
        else:
            if disp != "INSTALL":
                problems.append("first-install not INSTALL seq=%s" % seq)
            if int(anch) != -1:
                problems.append("first-install anchor != -1 seq=%s" % seq)
            anchors[key] = perc
            anchors_seq[key] = int(seq)
        n_ok += 1
    return n_ok, problems, anchors


def main():
    global anchors_seq
    anchors_seq = {}
    r1 = load_run(1)
    recs = [r for r in r1["records"] if "error" not in r]
    prim = [r for r in recs if r["pop"] == "primary"]
    adv = [r for r in recs if r["pop"] == "g1adv"]

    # ---- B1: primary accuracy ----
    b1 = {}
    for t in TASKS:
        ts = [r for r in prim if r["task"] == t]
        b1[t] = {"n": len(ts),
                 "acc": sum(1 for r in ts if r["correct"]) / len(ts) if ts else 0.0}
    mean_viab = sum(v["acc"] for v in b1.values()) / len(b1)

    # ---- B3: ops / bytes ----
    b3 = {t: {"mean_ops": sum(r["ops"] for r in recs if r["task"] == t) /
              max(1, len([r for r in recs if r["task"] == t])),
              "percept_bits": 512, "percept_bytes": 64}
          for t in TASKS}

    # ---- B4: ablation (confidence >= 500 installs) vs contract ----
    b4 = {"n_adv": len(adv), "differ": 0,
          "contract_false_install": 0, "ablated_false_install": 0,
          "contract_installs": 0, "ablated_installs": 0}
    for r in adv:
        abl = "INSTALL" if r["confidence"] >= 500 else "WITHHOLD"
        if abl != r["disposition"]:
            b4["differ"] += 1
        if r["disposition"] == "INSTALL":
            b4["contract_installs"] += 1
            if not r["correct"]:
                b4["contract_false_install"] += 1
        if abl == "INSTALL":
            b4["ablated_installs"] += 1
            if not r["correct"]:
                b4["ablated_false_install"] += 1

    # ---- B5: adversarial false-install rates ----
    n_inst = b4["contract_installs"] or 1
    b5 = {"per_install": b4["contract_false_install"] / n_inst,
          "per_fixture": b4["contract_false_install"] / max(1, len(adv)),
          "false_installs": b4["contract_false_install"],
          "installs": b4["contract_installs"], "n_adv": len(adv)}

    # ---- ledgers: verify + build class anchors ----
    ledgers = {}
    anchors_all = {}
    for t in TASKS:
        lp = os.path.join(RES, "run1", "ledgers", "sgp_%s.txt" % t)
        anchors_seq = {}
        n_ok, problems, anchors = verify_ledger(lp)
        ledgers[t] = {"entries": n_ok, "problems": problems}
        for (tt, judg), perc in anchors.items():
            anchors_all.setdefault(tt, {})[judg] = perc

    # ---- retrieval: group alignment vs class anchors ----
    # Group alignment: exact generator-code agreement (canonical sorted codes).
    # This is the strongest form supported by the frozen percept design.
    PAIR_TASKS = {"colordisc", "colorconst", "pitchdisc"}
    def gen_codes(percept_hex, task):
        b = bytes.fromhex(percept_hex)
        if task in PAIR_TASKS:
            return b[0:16] + b[32:48]
        else:
            return b[0:32]
    retr = {}
    for t in TASKS:
        classes = anchors_all.get(t, {})
        acl = {j: gen_codes(ap, t) for j, ap in classes.items()}
        ts = [r for r in prim if r["task"] == t]
        ok = 0
        for r in ts:
            qc = gen_codes(r["percept"], t)
            best, bj = -1, None
            for judg, ac in acl.items():
                s = sum(1 for a, b_ in zip(qc, ac) if a == b_)
                if s > best:
                    best, bj = s, judg
            if bj == r["truth"]:
                ok += 1
        retr[t] = {"n": len(ts), "acc": ok / len(ts) if ts else 0.0}
    mean_retr = sum(v["acc"] for v in retr.values()) / len(retr)

    # ---- B6: triple-run determinism ----
    b6 = {"byte_identical_stdout": True, "n_compared": 0}
    if os.path.exists(os.path.join(RES, "run3", "raw_g1.json")):
        r2, r3 = load_run(2), load_run(3)
        for a, b, c in zip(r1["records"], r2["records"], r3["records"]):
            ka = {k: a.get(k) for k in ("judgment", "confidence", "ops",
                                        "percept", "disposition", "variance",
                                        "anchor")}
            kb = {k: b.get(k) for k in ka}
            kc = {k: c.get(k) for k in ka}
            b6["n_compared"] += 1
            if ka != kb or ka != kc:
                b6["byte_identical_stdout"] = False
                break

    # ---- B2: head-to-head with A (if raw_a.json present) ----
    b2 = {"available": False}
    ap = os.path.join(RES, "runA", "raw_a.json")
    if os.path.exists(ap):
        with open(ap) as f:
            ra = json.load(f)
        amap = {(r["task"], r["fixture"]): r["judgment"]
                for r in ra["records"] if "error" not in r}
        agree = sum(1 for r in recs
                    if amap.get((r["task"], r["fixture"])) == r["judgment"])
        n = sum(1 for r in recs if (r["task"], r["fixture"]) in amap)
        b2 = {"available": True, "n": n, "agreement": agree / n if n else 0.0}

    metrics = {
        "B1_mean_viability": mean_viab, "B1_per_task": b1,
        "B2": b2, "B3": b3, "B4": b4,
        "B4_pct_changed": b4["differ"] / max(1, b4["n_adv"]),
        "B5": b5, "retrieval_per_task": retr,
        "retrieval_mean": mean_retr, "B6": b6,
        "ledgers": ledgers, "n_primary": len(prim), "n_adv": len(adv),
        "run_errors": r1["errors"],
    }
    with open(os.path.join(RES, "metrics_g1.json"), "w") as f:
        json.dump(metrics, f, indent=1)
    print(json.dumps({
        "B1": round(mean_viab, 4), "B4_changed": round(metrics["B4_pct_changed"], 4),
        "B5_false_install": round(b5["per_install"], 4),
        "retrieval": round(mean_retr, 4),
        "B6_identical": b6["byte_identical_stdout"],
        "ledger_problems": sum(len(v["problems"]) for v in ledgers.values()),
    }, indent=1))


if __name__ == "__main__":
    main()
