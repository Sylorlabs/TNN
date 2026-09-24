#!/usr/bin/env python3
"""Fidelity check F2 (SPEC section 5): independent spot re-derivation.

A second, independently written implementation of ITEM_ENCODING_SPEC
sections 3-4 (no code shared with encode_items.py) re-translates every
10th source item in file order (deterministic sample) and byte-compares
each emitted line against the committed translation. Requires 100% match.

Usage: spotcheck.py <src_dir> <items_v2_dir>
"""
import json
import os
import re
import sys

OK = frozenset("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
               "abcdefghijklmnopqrstuvwxyz_.-")


def clean_id(s):
    return "".join(ch if ch in OK else "_" for ch in s)


def clean_text(s):
    out = []
    for ch in s.replace('"', "'").replace("\\", "/"):
        if ord(ch) >= 0x20:
            out.append(ch)
    return "".join(out)[:4000]


def js(obj):
    return json.dumps(obj, ensure_ascii=True)


def build(iid, tt, hyps, evrows, gt):
    assert 1 <= len(iid) <= 64 and all(c in OK for c in iid)
    assert 1 <= len(hyps) <= 16 and len(set(hyps)) == len(hyps)
    assert all(1 <= len(h) <= 64 and all(c in OK for c in h) for h in hyps)
    assert gt in hyps
    assert len(evrows) <= 64
    ev = []
    for k, (sup, att, tx) in enumerate(evrows, start=1):
        assert len(sup) + len(att) <= 16
        for h in list(sup) + list(att):
            assert h in hyps and isinstance(sup.get(h, att.get(h)), int)
        ev.append({"id": "e%d" % k, "supports": sup, "attacks": att,
                   "text": clean_text(tx)})
    return js({"id": iid, "task_type": tt,
               "input": {"hypotheses": [{"id": h, "label": clean_text(h)}
                                       for h in hyps],
                         "evidence": ev},
               "ground_truth": gt})


def t_admit(o):
    g = clean_id(o["ground_truth"])
    rows = list(o["input"].get("prior_same_task", [])) + [o["input"]["trial"]]
    ev = []
    for r in rows:
        if "disposition" in r:
            tx = "prior seq=%s fixture=%s judgment=%s disposition=%s "\
                 "confidence=%s" % (r["seq"], r["fixture"], r["judgment"],
                                    r["disposition"], r["confidence"])
        else:
            tx = "trial seq=%s tcode=%s judgment=%s confidence=%s measure=%s"\
                 % (r["seq"], r["tcode"], r["judgment"], r["confidence"],
                    r["measure"])
        ev.append(({g: int(r["confidence"])}, {}, tx))
    hyps = sorted(["ACCEPT_INSTALL", "CONFLICT_WITHHELD", "CORROBORATED",
                   "NEGATIVE_EVIDENCE", "PERMANENT_INSTALL",
                   "PROVISIONAL_INSTALL", "REVISE_INSTALL", "SUPPRESSED",
                   "WITHHELD"])
    return build(o["id"], o["task_type"], hyps, ev, g)


def t_revoke(o):
    g = clean_id(o["ground_truth"])
    hyps = sorted(["BROKEN", "HOLD", "KILL", "KILL_SURVIVE", "PASS",
                   "SURVIVE"])
    ev = []
    kind = o["input"].get("item_kind")

    def b2s(v):
        if v is True:
            return "true"
        if v is False:
            return "false"
        return str(v)
    if kind == "cell_verdict":
        obs = o["input"].get("observed", o["input"].get("observed_metrics"))
        prefix = "observed." if "observed" in o["input"] else "metrics."
        for k in sorted(obs):
            ev.append(({g: 500}, {}, "%s%s=%s" % (prefix, k, b2s(obs[k]))))
    elif kind == "kill_bar":
        ev.append(({g: 500}, {},
                   "kill_bar %s: %s" % (o["input"]["kill_bar"],
                                       o["input"]["kill_bar_definition"])))
    elif kind == "fidelity_gate":
        for k in sorted(o["input"]["observed"]):
            ev.append(({g: 500}, {},
                         "observed.%s=%s" % (k, b2s(o["input"]["observed"][k]))))
        ev.append(({g: 500}, {},
                   "fidelity_gate: %s" % o["input"]["fidelity_gate"]))
    else:
        raise AssertionError("bad kind " + o["id"])
    return build(o["id"], o["task_type"], hyps, ev, g)


def t_logic(o):
    g = clean_id(o["ground_truth"])
    hyps = sorted(["AFFIRM", "DENY", "NEUTRAL"])
    ev = [({g: 500}, {}, e) for e in o["input"]["evidence"]]
    return build(o["id"], o["task_type"], hyps, ev, g)


def t_trap(o):
    hyps = [clean_id(x) for x in o["input"]["options"]]
    g = clean_id(o["ground_truth"])
    s = clean_id(o["shallow_answer"])
    src = o["input"]
    mis = list(src["surface_evidence"]) if src.get("surface_evidence") \
        else list(src["premises"])
    cor = list(src["deep_evidence"]) if src.get("deep_evidence") \
        else ([src["falsifying_instance"]] if src.get("falsifying_instance")
              else [o["ground_truth_basis"]])
    ev = [({s: 100}, {}, m) for m in mis] + \
         [({g: 500}, {s: 500}, c) for c in cor]
    return build(o["id"], o["task_type"], hyps, ev, g)


DRE = re.compile(r"^(\w+) iff cumulative evidence score >= \+(\d+); "
                 r"(\w+) iff <= -(\d+)$")


def t_cost(o):
    hyps = [clean_id(x) for x in o["input"]["options"]]
    g = clean_id(o["ground_truth"])
    rounds = sorted(o["input"]["evidence_rounds"], key=lambda r: r["round"])
    ev = []
    if o["attack_class"] == "D1-balanced-treadmill":
        m = DRE.match(o["input"]["decision_rule"])
        assert m, o["id"]
        pos, neg = clean_id(m.group(1).upper()), clean_id(m.group(3).upper())
        assert pos in hyps and neg in hyps and pos != neg
        for r in rounds:
            d = int(r["score_delta"])
            w = 250 * abs(d)
            ev.append((({pos: w}, {}, r["text"]) if d > 0
                       else ({neg: w}, {}, r["text"])))
    else:
        for r in rounds:
            ev.append(({g: 500}, {}, r["text"]))
    return build(o["id"], o["task_type"], hyps, ev, g)


TABLE = [
    ("batteries/admit_battery.jsonl", "admit.jsonl", t_admit),
    ("batteries/revoke_battery.jsonl", "revoke.jsonl", t_revoke),
    ("batteries/logic_battery.jsonl", "logic.jsonl", t_logic),
    ("redteam/trap_battery.jsonl", "trap.jsonl", t_trap),
    ("redteam/cost_attacks.jsonl", "cost.jsonl", t_cost),
]


def main():
    src_dir, out_dir = sys.argv[1], sys.argv[2]
    checked = 0
    mism = []
    for rel, out_name, fn in TABLE:
        with open(os.path.join(src_dir, rel), encoding="utf-8") as f:
            src_lines = [l for l in f.read().split("\n") if l.strip()]
        with open(os.path.join(out_dir, out_name), encoding="utf-8") as f:
            out_lines = [l.rstrip("\n") for l in f if l.strip()]
        assert len(src_lines) == len(out_lines), (rel, len(src_lines),
                                                 len(out_lines))
        for i in range(0, len(src_lines), 10):
            expect = fn(json.loads(src_lines[i]))
            got = out_lines[i]
            checked += 1
            if expect != got:
                mism.append((rel, i, src_lines[i][:60]))
    print(f"F2: {checked - len(mism)}/{checked} spot items byte-identical")
    for m in mism[:10]:
        print("  MISMATCH:", m)
    sys.exit(1 if mism else 0)


if __name__ == "__main__":
    main()
