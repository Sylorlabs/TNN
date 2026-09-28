#!/usr/bin/env python3
"""TRACKB-DISCRIM leg runner: one (variant, policy) -> JSON metrics file."""
import json, os, sys, hashlib
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H

def canon(props):
    return [(p["seq"], p["kind"], p["ss"], p["se"], p["conf"]) for p in props]

def metrics(res):
    props = res["proposals"]
    kinds = Counter(p["kind"] for p in props)
    confs = [p["conf"] for p in props]
    spans = [(p["ss"], p["se"]) for p in props]
    sc = Counter(spans)
    m = dict(
        variant=res["variant"], policy=res["policy"],
        n_proposals=len(props),
        kinds={str(k): v for k, v in sorted(kinds.items())},
        conf_min=min(confs) if confs else None,
        conf_max=max(confs) if confs else None,
        conf_mean=round(sum(confs)/len(confs), 2) if confs else None,
        distinct_spans=len(set(spans)),
        repro_spans=sum(1 for v in sc.values() if v > 1),
        reproposals=sum(v - 1 for v in sc.values() if v > 1),
        wall_s=round(res.get("wall_s", 0), 3),
    )
    if res["variant"] == "A":
        last = res["rounds"][-1]
        m["terminal_rc"] = last["rc"]
        m["converged"] = res["converged"]
        m["n_rounds"] = len(res["rounds"])
        m["tape_bytes"] = res["tape_bytes"]
        m["bytes_per_proposal"] = round(res["tape_bytes"]/len(props), 1) if props else None
        m["events"] = {str(k): v for k, v in res["events"].items()}
        tail = last["stdout_tail"]
        m["terminal"] = ("clean_end" if "VARA_END" in tail else
                         "decisions_exhausted" if "DECISIONS_EXHAUSTED" in tail else
                         f"rc{last['rc']}")
    elif res["variant"] == "B":
        m["turns"] = res["turns"]
        m["terminal_rc"] = res["rc"]
        m["terminal"] = "empty_batch" if res["rc"] == 0 else f"rc{res['rc']}"
        m["stdout_bytes"] = res["stdout_bytes"]
        m["bytes_per_proposal"] = round(res["stdout_bytes"]/len(props), 1) if props else None
    else:
        m["turns"] = res["turns"]
        m["terminal"] = res["terminal"]
        m["terminal_rc"] = res["rc"]
        m["stdout_bytes"] = res["stdout_bytes"]
        m["bytes_per_proposal"] = round(res["stdout_bytes"]/len(props), 1) if props else None
    m["canon_sha"] = hashlib.sha256(
        json.dumps(canon(props), sort_keys=True).encode()).hexdigest()[:16]
    return m

RUNNERS = {"A": H.runA, "B": H.runB, "C": H.runC}

def run_leg(variant, policy, workdir, sess_id, curr="std"):
    workdir = os.path.abspath(workdir)
    os.makedirs(workdir, exist_ok=True)
    res = RUNNERS[variant](policy, sess_id, workdir, curr=curr)
    m = metrics(res)
    m["sess_id"] = sess_id
    m["curr"] = curr
    # persist canonical proposal stream + decisions for audit
    with open(os.path.join(workdir, "canon.json"), "w") as f:
        json.dump(canon(res["proposals"]), f)
    with open(os.path.join(workdir, "decisions.json"), "w") as f:
        json.dump([[d[0], d[1], list(d[2]) if d[2] else None]
                   for d in res["decisions"]], f)
    return m

def main():
    variant, policy, workdir = sys.argv[1], sys.argv[2], sys.argv[3]
    sess_id = int(sys.argv[4]) if len(sys.argv) > 4 else 7000 + hash((variant, policy)) % 500
    m = run_leg(variant, policy, workdir, sess_id)
    out = os.path.join(workdir, "metrics.json")
    with open(out, "w") as f:
        json.dump(m, f, indent=1, sort_keys=True)
    print(json.dumps(m, sort_keys=True))

if __name__ == "__main__":
    main()
