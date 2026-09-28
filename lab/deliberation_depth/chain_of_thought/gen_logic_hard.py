#!/usr/bin/env python3
"""Generate the H5 chain-of-thought harder logic battery (logic_hard.jsonl).

Deterministic: all variation is pure index arithmetic. No RNG, no wall-clock,
no dict iteration. Verifies every item parses under the ITEM_FORMAT.md subset
(no quotes/backslashes in strings, id charset, caps).

Three families x 16 items = 48 items, task_type "logic":
  CE: chain-elimination   (5 hypotheses, 4 evidence, 3-hop kill chain)
  FP: misleading prefix   (3 hypotheses, wrong leader early, late overturn)
  DA: distractor accumulation (3 hypotheses, 6-7 sub-threshold premises)
"""
import json
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "logic_hard.jsonl"

SUP16 = 16
EV64 = 64


def ev(eid, supports, attacks, text):
    return {"id": eid, "supports": supports, "attacks": attacks, "text": text}


def check_item(it):
    assert 1 <= len(it["id"]) <= 64
    assert all(c.isalnum() or c in "_.-" for c in it["id"])
    nh = len(it["input"]["hypotheses"])
    assert 1 <= nh <= SUP16
    hids = [h["id"] for h in it["input"]["hypotheses"]]
    assert len(set(hids)) == nh
    nev = len(it["input"]["evidence"])
    assert 0 <= nev <= EV64
    eids = set()
    for e in it["input"]["evidence"]:
        assert e["id"] not in eids
        eids.add(e["id"])
        assert len(e["supports"]) <= SUP16 and len(e["attacks"]) <= SUP16
        for h in list(e["supports"]) + list(e["attacks"]):
            assert h in hids, (it["id"], h)
        for t in (e["text"],):
            assert '"' not in t and "\\" not in t
            assert all(ord(c) >= 32 or c in "\t" for c in t)
    assert it["ground_truth"] in hids
    line = json.dumps(it, separators=(",", ":"))
    assert len(line) <= 65536
    return line


def hset(prefix, n):
    return [{"id": "%s-H%d" % (prefix, k), "label": "candidate %d" % k}
            for k in range(n)]


items = []

# ---- Family CE: chain-elimination -------------------------------------------
# Roles: W1, W2 = early wrong leaders; K1, K2 = early-killed contenders;
# G = ground-truth survivor. Chain: e1 sets W1 + kills K1; e2 sets W2 + kills
# K2; e3 kills W1 and W2 at once and crowns G; e4 confirms G.
for i in range(16):
    s = i % 5                      # rotation of roles over H0..H4
    pat = (i // 5) % 3             # weight pattern 0/1/2
    w1 = (0 + s) % 5               # canonical W1=0
    w2 = (1 + s) % 5               # canonical W2=1
    g = (2 + s) % 5                # canonical G=2
    k1 = (3 + s) % 5
    k2 = (4 + s) % 5
    sup = [(600, 700, 800), (650, 750, 850), (550, 650, 750)][pat]
    atk = [950, 950, 900][pat]
    conf = [200, 250, 150][pat]
    H = lambda k: "CE-H%d" % k     # noqa: E731
    item = {
        "id": "LH-CE-%02d" % (i + 1),
        "task_type": "logic",
        "input": {
            "hypotheses": hset("CE", 5),
            "evidence": [
                ev("e1", {H(w1): sup[0]}, {H(k1): atk},
                   "premise 1: supports candidate %d, refutes candidate %d" % (w1, k1)),
                ev("e2", {H(w2): sup[1]}, {H(k2): atk},
                   "premise 2: supports candidate %d, refutes candidate %d" % (w2, k2)),
                ev("e3", {H(g): sup[2]}, {H(w1): atk, H(w2): atk},
                   "premise 3: supports candidate %d, refutes candidates %d and %d" % (g, w1, w2)),
                ev("e4", {H(g): conf}, {},
                   "premise 4: confirms candidate %d" % g),
            ],
        },
        "ground_truth": H(g),
    }
    items.append(item)

# ---- Family FP: misleading prefix -> flip ------------------------------------
# L=1 (items 0-7): one misleading premise, overturn at e2, settle at e3.
# L=2 (items 8-15): two misleading premises, overturn at e3, settle at e4.
for i in range(16):
    L = 1 if i < 8 else 2
    gt = i % 3
    w = (gt + 1) % 3               # wrong early leader
    n = (gt + 2) % 3              # neutral bystander
    H = lambda k: "FP-H%d" % k    # noqa: E731
    evs = []
    if L == 1:
        evs.append(ev("e1", {H(w): 700}, {},
                      "premise 1 (misleading): supports candidate %d" % w))
        evs.append(ev("e2", {H(gt): 800}, {H(w): 950},
                      "premise 2 (overturn): supports candidate %d, refutes candidate %d" % (gt, w)))
        evs.append(ev("e3", {H(gt): 300}, {},
                      "premise 3: confirms candidate %d" % gt))
        evs.append(ev("e4", {H(gt): 200}, {},
                      "premise 4: confirms candidate %d" % gt))
    else:
        evs.append(ev("e1", {H(w): 400}, {},
                      "premise 1 (misleading): supports candidate %d" % w))
        evs.append(ev("e2", {H(w): 400}, {},
                      "premise 2 (misleading): supports candidate %d" % w))
        evs.append(ev("e3", {H(gt): 800}, {H(w): 950},
                      "premise 3 (overturn): supports candidate %d, refutes candidate %d" % (gt, w)))
        evs.append(ev("e4", {H(gt): 300}, {H(w): 950},
                      "premise 4: confirms candidate %d, refutes candidate %d" % (gt, w)))
        evs.append(ev("e5", {H(gt): 200}, {},
                      "premise 5: confirms candidate %d" % gt))
    item = {
        "id": "LH-FP-%02d" % (i + 1),
        "task_type": "logic",
        "input": {"hypotheses": hset("FP", 3), "evidence": evs},
        "ground_truth": H(gt),
    }
    items.append(item)

# ---- Family DA: distractor accumulation ---------------------------------------
# 6-7 premises each supporting GT by 180-200 (sub-threshold alone); the leader
# is GT from round 1, but contenders are eliminated only once the accumulated
# margin crosses 900 (round 5-6).
for i in range(16):
    gt = i % 3
    n_ev = 6 + ((i // 3) % 2)
    wgt = 200 - 20 * ((i // 6) % 2)
    H = lambda k: "DA-H%d" % k    # noqa: E731
    evs = [ev("e%d" % (j + 1), {H(gt): wgt}, {},
               "premise %d: weak support for candidate %d (%d of %d)" % (j + 1, gt, j + 1, n_ev))
           for j in range(n_ev)]
    item = {
        "id": "LH-DA-%02d" % (i + 1),
        "task_type": "logic",
        "input": {"hypotheses": hset("DA", 3), "evidence": evs},
        "ground_truth": H(gt),
    }
    items.append(item)

lines = [check_item(it) for it in items]
assert len(lines) == 48
with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print("wrote %d items to %s" % (len(lines), OUT))
