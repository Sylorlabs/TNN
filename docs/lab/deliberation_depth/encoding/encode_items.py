#!/usr/bin/env python3
"""H5 item encoder — executable form of ITEM_ENCODING_SPEC.md v1 (frozen).

Mechanical, deterministic translation of the 877 frozen battery/red-team
items into the harness item format. No per-item hand-authored weights:
every weight is a fixed constant or a fixed scaling of a payload number.

Usage: encode_items.py <src_dir> <out_dir>
  src_dir: deliberation_depth/ (with batteries/, redteam/)
  out_dir: items_v2/ (written: admit.jsonl, revoke.jsonl, logic.jsonl,
           trap.jsonl, cost.jsonl)

Exit 0 on success; any spec assertion failure aborts with nonzero exit.
Deterministic: same frozen inputs -> byte-identical outputs.
"""
import json
import re
import string
import sys

ID_OK = set(string.ascii_letters + string.digits + "_.-")


def g2_map(s):
    """SPEC G2: charset mapping for ground truths / hypothesis ids."""
    return "".join(c if c in ID_OK else "_" for c in s)


def g3_sanitize(s):
    """SPEC G3: text sanitization."""
    s = s.replace('"', "'").replace("\\", "/")
    s = "".join(c for c in s if ord(c) >= 0x20)
    s = s.replace("\r", "")
    return s[:4000]


def assert_id(s, what):
    assert 1 <= len(s) <= 64 and all(c in ID_OK for c in s), \
        f"id charset violation in {what}: {s!r}"


def emit_item(o):
    """SPEC G7: fixed key order, integer weights, ascii JSON."""
    # o: dict with keys in fixed order already
    return json.dumps(o, ensure_ascii=True)


def make_item(item_id, task_type, hypotheses, evidence, ground_truth):
    """hypotheses: list of ids (order kept). evidence: list of
    (eid, supports dict, attacks dict, text)."""
    assert_id(item_id, "item id")
    assert 1 <= len(hypotheses) <= 16, f"hypothesis count: {item_id}"
    assert len(set(hypotheses)) == len(hypotheses), \
        f"duplicate hypothesis after G2 mapping: {item_id}"
    for h in hypotheses:
        assert_id(h, f"hypothesis of {item_id}")
    assert_id(ground_truth, f"ground_truth of {item_id}")
    assert ground_truth in hypotheses, \
        f"ground_truth not a hypothesis: {item_id}"
    assert len(evidence) <= 64, f"too much evidence: {item_id}"
    ev_out = []
    seen_eids = set()
    for (eid, supports, attacks, text) in evidence:
        assert_id(eid, f"evidence id of {item_id}")
        assert eid not in seen_eids, f"dup evidence id {eid} in {item_id}"
        seen_eids.add(eid)
        assert len(supports) + len(attacks) <= 16, \
            f"too many links in {eid} of {item_id}"
        for h in list(supports) + list(attacks):
            assert h in hypotheses, \
                f"link to unknown hypothesis {h} in {item_id}"
            assert isinstance(supports.get(h, attacks.get(h)), int), \
                f"non-integer weight in {item_id}"
        ev_out.append({
            "id": eid,
            "supports": supports,
            "attacks": attacks,
            "text": g3_sanitize(text),
        })
    hyps = [{"id": h, "label": g3_sanitize(h)} for h in hypotheses]
    return {
        "id": item_id,
        "task_type": task_type,
        "input": {"hypotheses": hyps, "evidence": ev_out},
        "ground_truth": ground_truth,
    }


# ---------------- admit ----------------
ADMIT_HYPS = sorted([
    "ACCEPT_INSTALL", "CONFLICT_WITHHELD", "CORROBORATED",
    "NEGATIVE_EVIDENCE", "PERMANENT_INSTALL", "PROVISIONAL_INSTALL",
    "REVISE_INSTALL", "SUPPRESSED", "WITHHELD",
])


def encode_admit(o):
    gt = g2_map(o["ground_truth"])
    assert gt == o["ground_truth"], f"admit GT needed G2 mapping: {o['id']}"
    assert o["provenance"]["gate_program_verdict"] == o["ground_truth"], \
        f"admit GT != program verdict: {o['id']}"
    ev = []
    n = 0
    for r in list(o["input"].get("prior_same_task", [])) + [o["input"]["trial"]]:
        n += 1
        is_trial = (r is o["input"]["trial"])
        if is_trial:
            text = ("trial seq=%s tcode=%s judgment=%s confidence=%s measure=%s"
                    % (r["seq"], r["tcode"], r["judgment"],
                       r["confidence"], r["measure"]))
        else:
            text = ("prior seq=%s fixture=%s judgment=%s disposition=%s "
                    "confidence=%s"
                    % (r["seq"], r["fixture"], r["judgment"],
                       r["disposition"], r["confidence"]))
        w = int(r["confidence"])
        assert 0 <= w <= 1000, f"admit confidence out of range: {o['id']}"
        ev.append(("e%d" % n, {gt: w}, {}, text))
    return make_item(o["id"], o["task_type"], ADMIT_HYPS, ev, gt)


# ---------------- revoke ----------------
REVOKE_HYPS = sorted(["BROKEN", "HOLD", "KILL", "KILL_SURVIVE", "PASS",
                      "SURVIVE"])


def _bool_str(v):
    if v is True:
        return "true"
    if v is False:
        return "false"
    return str(v)


def encode_revoke(o):
    gt = g2_map(o["ground_truth"])
    p = o["provenance"]
    pv = p.get("program_derived_verdict") or p.get("bar_outcome") or \
        p.get("program_verdict")
    if pv is not None:
        assert pv == o["ground_truth"], \
            f"revoke GT != program verdict: {o['id']}"
    kind = o["input"].get("item_kind")
    ev = []
    n = 0

    def add(supports, text):
        nonlocal n
        n += 1
        ev.append(("e%d" % n, supports, {}, text))

    if kind == "cell_verdict" and "observed" in o["input"]:
        for k in sorted(o["input"]["observed"].keys()):
            add({gt: 500},
                "observed.%s=%s" % (k, _bool_str(o["input"]["observed"][k])))
    elif kind == "cell_verdict" and "observed_metrics" in o["input"]:
        for k in sorted(o["input"]["observed_metrics"].keys()):
            add({gt: 500}, "metrics.%s=%s"
                % (k, _bool_str(o["input"]["observed_metrics"][k])))
    elif kind == "kill_bar":
        add({gt: 500}, "kill_bar %s: %s"
            % (o["input"]["kill_bar"], o["input"]["kill_bar_definition"]))
    elif kind == "fidelity_gate":
        for k in sorted(o["input"]["observed"].keys()):
            add({gt: 500},
                "observed.%s=%s" % (k, _bool_str(o["input"]["observed"][k])))
        add({gt: 500}, "fidelity_gate: %s" % o["input"]["fidelity_gate"])
    else:
        raise AssertionError(f"unknown revoke shape: {o['id']}")
    assert n >= 1, f"revoke item with no evidence: {o['id']}"
    return make_item(o["id"], o["task_type"], REVOKE_HYPS, ev, gt)


# ---------------- logic ----------------
LOGIC_HYPS = sorted(["AFFIRM", "DENY", "NEUTRAL"])


def encode_logic(o):
    gt = g2_map(o["ground_truth"])
    assert gt == o["ground_truth"], f"logic GT needed G2 mapping: {o['id']}"
    ev = []
    for i, e in enumerate(o["input"]["evidence"], start=1):
        ev.append(("e%d" % i, {gt: 500}, {}, e))
    assert len(ev) >= 1, f"logic item with no evidence: {o['id']}"
    return make_item(o["id"], o["task_type"], LOGIC_HYPS, ev, gt)


# ---------------- trap ----------------
TRAP_WM = 100   # misleading weight (SPEC 4.4: 0 < Wm < 150)
TRAP_WC = 500   # corrective weight


def encode_trap(o):
    hyps = [g2_map(x) for x in o["input"]["options"]]
    gt = g2_map(o["ground_truth"])
    shallow = g2_map(o["shallow_answer"])
    assert gt != shallow, f"trap GT == shallow_answer: {o['id']}"
    inp = o["input"]
    if inp.get("surface_evidence"):
        misleading = list(inp["surface_evidence"])
    else:
        misleading = list(inp["premises"])
    if inp.get("deep_evidence"):
        corrective = list(inp["deep_evidence"])
    elif inp.get("falsifying_instance"):
        corrective = [inp["falsifying_instance"]]
    else:
        corrective = [o["ground_truth_basis"]]
    assert len(misleading) >= 1, f"trap with no misleading evidence: {o['id']}"
    assert len(corrective) >= 1, \
        f"trap with no corrective evidence: {o['id']}"
    ev = []
    n = 0
    for m in misleading:
        n += 1
        ev.append(("e%d" % n, {shallow: TRAP_WM}, {}, m))
    for c in corrective:
        n += 1
        attacks = {shallow: TRAP_WC} if shallow != gt else {}
        ev.append(("e%d" % n, {gt: TRAP_WC}, attacks, c))
    return make_item(o["id"], o["task_type"], hyps, ev, gt)


# ---------------- cost ----------------
COST_D1_RE = re.compile(
    r"^(\w+) iff cumulative evidence score >= \+(\d+); "
    r"(\w+) iff <= -(\d+)$")
COST_PT = 250   # thousandths per score point (SPEC 4.5)


def encode_cost(o):
    hyps = [g2_map(x) for x in o["input"]["options"]]
    gt = g2_map(o["ground_truth"])
    ev = []
    n = 0
    if o["attack_class"] == "D1-balanced-treadmill":
        m = COST_D1_RE.match(o["input"]["decision_rule"])
        assert m, f"D1 decision_rule regex failed: {o['id']}"
        pos = g2_map(m.group(1).upper())
        neg = g2_map(m.group(3).upper())
        assert pos in hyps and neg in hyps and pos != neg, \
            f"D1 polarity/options mismatch: {o['id']}"
        for r in sorted(o["input"]["evidence_rounds"],
                       key=lambda r: r["round"]):
            n += 1
            d = int(r["score_delta"])
            assert d != 0, f"D1 zero delta: {o['id']}"
            w = COST_PT * abs(d)
            if d > 0:
                ev.append(("e%d" % n, {pos: w}, {}, r["text"]))
            else:
                ev.append(("e%d" % n, {neg: w}, {}, r["text"]))
    else:
        for r in sorted(o["input"]["evidence_rounds"],
                       key=lambda r: r["round"]):
            n += 1
            ev.append(("e%d" % n, {gt: 500}, {}, r["text"]))
    assert n >= 1, f"cost item with no rounds: {o['id']}"
    return make_item(o["id"], o["task_type"], hyps, ev, gt)


ENCODERS = {
    "admit_battery.jsonl": encode_admit,
    "revoke_battery.jsonl": encode_revoke,
    "logic_battery.jsonl": encode_logic,
    "trap_battery.jsonl": encode_trap,
    "cost_attacks.jsonl": encode_cost,
}
OUT_NAMES = {
    "admit_battery.jsonl": "admit.jsonl",
    "revoke_battery.jsonl": "revoke.jsonl",
    "logic_battery.jsonl": "logic.jsonl",
    "trap_battery.jsonl": "trap.jsonl",
    "cost_attacks.jsonl": "cost.jsonl",
}
SRC_SUBDIR = {
    "admit_battery.jsonl": "batteries",
    "revoke_battery.jsonl": "batteries",
    "logic_battery.jsonl": "batteries",
    "trap_battery.jsonl": "redteam",
    "cost_attacks.jsonl": "redteam",
}


def main():
    src_dir, out_dir = sys.argv[1], sys.argv[2]
    import os
    os.makedirs(out_dir, exist_ok=True)
    total = 0
    for src_name, enc in ENCODERS.items():
        src_path = os.path.join(src_dir, SRC_SUBDIR[src_name], src_name)
        out_path = os.path.join(out_dir, OUT_NAMES[src_name])
        with open(src_path, encoding="utf-8") as f:
            lines = [l for l in f.read().split("\n") if l.strip()]
        with open(out_path, "w", encoding="utf-8") as out:
            for line in lines:
                item = enc(json.loads(line))
                out.write(emit_item(item) + "\n")
                total += 1
        print(f"{src_name}: {len(lines)} -> {OUT_NAMES[src_name]}")
    print(f"total: {total}")
    assert total == 877, f"expected 877 items, got {total}"


if __name__ == "__main__":
    main()
