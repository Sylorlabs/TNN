#!/usr/bin/env python3
"""record_live.py — record live search envelopes for the v2 legs.

Runs each v1 question through the live bridge (ws_bridge2.py) and saves
live/<factid>.json. One file per fact id; MTN.json holds the mountain query
for the B-live structural situations.

Usage: record_live.py <bridge.py> [--redo]
Fails loudly if any query returns zero usable results (transport shortfall
is data, but a missing envelope breaks the emitter).
"""
import json
import os
import subprocess
import sys

V1 = os.path.expanduser("~/workspace/senses-websearch/fixtures")
LIVE = os.path.expanduser("~/workspace/senses-v2/live")

QUERIES = []
d = json.load(open(os.path.join(V1, "real_search.json")))
for f in d["facts"]:
    QUERIES.append((f["id"], f["search_query"]))
QUERIES.append(("MTN", "tallest mountain in the world"))


def main():
    bridge = sys.argv[1]
    redo = "--redo" in sys.argv
    os.makedirs(LIVE, exist_ok=True)
    shortfalls = []
    for fid, q in QUERIES:
        p = os.path.join(LIVE, fid + ".json")
        if os.path.exists(p) and not redo:
            print(f"keep {fid}")
            continue
        r = subprocess.run([sys.executable, bridge, q, "6"],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            print(f"BRIDGE FAIL {fid}: {r.stderr[:200]}")
            shortfalls.append(fid)
            continue
        try:
            env = json.loads(r.stdout)
        except Exception as e:
            print(f"PARSE FAIL {fid}: {e}")
            shortfalls.append(fid)
            continue
        usable = [x for x in env.get("results", []) if x.get("title") and x.get("url")]
        env["fact_id"] = fid
        json.dump(env, open(p, "w"), indent=1)
        print(f"recorded {fid}: {len(usable)} usable results")
        if not usable:
            shortfalls.append(fid)
    if shortfalls:
        print(f"SHORTFALLS (zero usable results): {shortfalls}")
    else:
        print("all queries returned usable results")


if __name__ == "__main__":
    main()
