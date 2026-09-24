#!/usr/bin/env python3
"""H5 chain-of-thought trace-quality metrics Q1-Q4 (frozen PREREG_COT.md §2).

Deterministic: no RNG, no wall-clock, no dict-order dependence (item ids
sorted). Inputs: items jsonl, per-run ledger, per-run results jsonl.
Output: per-depth aggregate table (JSON + human-readable).

Cross-checks (fail loudly): #ROUND lines == rounds_used; final ROUND leader
== verdict; correct == (verdict == ground_truth).
"""
import hashlib
import json
import sys


def parse_kv(detail):
    d = {}
    for tok in detail.split(" "):
        if "=" in tok:
            k, v = tok.split("=", 1)
            d[k] = v
    return d


def load_items(path):
    items = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            items[o["id"]] = {
                "gt": o["ground_truth"],
                "hyps": [h["id"] for h in o["input"]["hypotheses"]],
                "ev": [{"supports": e.get("supports", {}),
                        "attacks": e.get("attacks", {})}
                       for e in o["input"]["evidence"]],
            }
    return items


def load_jsonl(path):
    recs = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            recs[o["id"]] = o
    return recs


def parse_ledger(path):
    """id -> list of events in order. Each event: (round, action, detail)."""
    segs = {}
    cur = None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            iid, action = o["item"], o["action"]
            if action == "BEGIN":
                cur = iid
                segs[cur] = []
            elif cur is not None and iid == cur:
                segs[cur].append((o["round"], action, o["detail"]))
                if action == "VERDICT":
                    cur = None
    return segs


def analyze_item(iid, item, events, rec):
    gt = item["gt"]
    hyps = item["hyps"]
    nev = len(item["ev"])
    rounds = {}          # r -> dict(leader, margin, conf)
    ev_rounds = []       # (r, c) EVIDENCE events
    elim_events = []     # (r, h) ELIMINATE / TEST-refuted
    prod_evidence_round = set()
    order = []
    alive = set(hyps)
    alive_snap = {}      # r -> frozenset alive at ROUND line
    consumed_at = {}     # r -> consumed count
    nconsumed = 0
    for (r, action, detail) in events:
        kv = parse_kv(detail)
        order.append((r, action))
        if action == "EVIDENCE":
            nconsumed = int(kv["c"])
            ev_rounds.append((r, nconsumed))
        elif action == "ELIMINATE":
            alive.discard(kv["h"])
            elim_events.append((r, kv["h"]))
        elif action == "TEST":
            if "refuted" in detail:
                alive.discard(kv["h"])
                elim_events.append((r, kv["h"]))
        elif action == "ROUND":
            rounds[int(kv["r"])] = {"leader": kv["leader"],
                                   "margin": int(kv["margin"]),
                                   "conf": int(kv["conf"])}
            alive_snap[int(kv["r"])] = frozenset(alive)
            consumed_at[int(kv["r"])] = nconsumed
        elif action == "VERDICT":
            verdict = kv["verdict"]
    # cross-checks
    R = rec["rounds_used"]
    assert len(rounds) == R, (iid, len(rounds), R)
    assert sorted(rounds) == list(range(1, R + 1)), iid
    assert rounds[R]["leader"] == verdict == rec["verdict"], iid
    assert rec["correct"] == (1 if verdict == gt else 0), iid

    # Q1: productive rounds
    prev_leader, prev_margin = hyps[0], 0
    productive = 0
    prod_round = set()
    ev_in_round = {}
    for (r, c) in ev_rounds:
        ev_in_round.setdefault(r, 0)
        ev_in_round[r] += 1
    elim_in_round = set(r for (r, h) in elim_events)
    for r in range(1, R + 1):
        info = rounds[r]
        prod = (r in ev_in_round or r in elim_in_round
                or info["leader"] != prev_leader
                or info["margin"] > prev_margin)
        if prod:
            productive += 1
            prod_round.add(r)
        prev_leader, prev_margin = info["leader"], info["margin"]
    q1_frac = productive / R if R else 0.0

    # Q2: premise leverage
    decisive = sum(1 for (r, c) in ev_rounds if r in prod_round)
    q2 = decisive / len(ev_rounds) if ev_rounds else 0.0

    # Q3: correct eliminations (only on correctly-decided items)
    q3 = sum(1 for (r, h) in elim_events if h != gt) if verdict == gt else 0

    # Q4: post-settlement idle rounds (unflippable version)
    first_unflip = None
    for r in range(1, R + 1):
        info = rounds[r]
        leader = info["leader"]
        margin = info["margin"]
        contenders = [h for h in alive_snap[r] if h != leader]
        c = consumed_at[r]
        worst = 0
        for s in contenders:
            swing = 0
            for e in item["ev"][c:]:
                swing += e["supports"].get(s, 0) + e["attacks"].get(leader, 0)
            if swing > worst:
                worst = swing
        if not contenders or margin > worst:
            first_unflip = r
            break
    if first_unflip is None:
        q4, never = 0, 1
    else:
        q4, never = R - first_unflip, 0

    return {"R": R, "q1_frac": q1_frac, "q1_count": productive,
            "q2": q2, "q2_n": len(ev_rounds), "q3": q3, "q4": q4,
            "never": never, "correct": rec["correct"], "verdict": verdict}


def measure(items_path, ledger_path, jsonl_path):
    items = load_items(items_path)
    segs = parse_ledger(ledger_path)
    recs = load_jsonl(jsonl_path)
    assert set(segs) == set(recs), "ledger/jsonl item mismatch"
    per = {}
    for iid in sorted(segs):
        assert iid in items, iid
        per[iid] = analyze_item(iid, items[iid], segs[iid], recs[iid])
    n = len(per)
    agg = {
        "n": n,
        "accuracy": sum(p["correct"] for p in per.values()) / n,
        "mean_rounds": sum(p["R"] for p in per.values()) / n,
        "Q1_PRF": sum(p["q1_frac"] for p in per.values()) / n,
        "Q1_productive_count": sum(p["q1_count"] for p in per.values()) / n,
        "Q2_PL": (sum(p["q2"] * p["q2_n"] for p in per.values())
                  / max(1, sum(p["q2_n"] for p in per.values()))),
        "Q3_CE": sum(p["q3"] for p in per.values()) / n,
        "Q4_PSIR": sum(p["q4"] for p in per.values()) / n,
        "never_unflippable_share": sum(p["never"] for p in per.values()) / n,
    }
    return agg, per


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    # args: label items ledgerA jsonlA ledgerB jsonlB  (A/B pooled)
    label, items_path = sys.argv[1], sys.argv[2]
    pairs = [(sys.argv[3], sys.argv[4]), (sys.argv[5], sys.argv[6])]
    pooled, per_all = [], {}
    shas = {"items": sha(items_path)}
    for li, (ledger_path, jsonl_path) in enumerate(pairs):
        shas["ledger_%s" % "AB"[li]] = sha(ledger_path)
        shas["jsonl_%s" % "AB"[li]] = sha(jsonl_path)
        agg, per = measure(items_path, ledger_path, jsonl_path)
        pooled.append(agg)
        for k, v in per.items():
            per_all[("AB"[li], k)] = v
    n0 = pooled[0]["n"]
    assert pooled[1]["n"] == n0
    out = {"label": label, "input_sha256": shas,
           "depths": {}, "note": "A/B pooled means"}
    # caller passes one depth per invocation; merge in driver below
    print(json.dumps({"label": label, "agg_A": pooled[0], "agg_B": pooled[1],
                      "shas": shas}))


if __name__ == "__main__":
    main()
